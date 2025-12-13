import pandas as pd
import numpy as np
from dataclasses import dataclass
import pickle
from pathlib import Path
import fire
from importlib.resources import files
from scipy.spatial import KDTree


# Helper function for softmax
def _softmax(x):
    """Compute softmax values for each sets of scores in x."""
    if x.ndim == 1:
        x = x.reshape(1, -1)
    max_x = np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x - max_x)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


@dataclass
class RLModelBase:
    def compute_action_transition_proba(self, current_action=None):
        """
        Compute action transition probability matrix from episode transitions.
        
        Args:
            current_action: Optional[Union[int, str]] - Current action to compute transition probabilities for
            
        Returns:
            Union[dict, pd.DataFrame] - Transition probabilities or full transition matrix
        """
        try:
            # Load episode transitions
            file_path = Path(self.episodes_file)
            ext = file_path.suffix.lower()
            if ext == '.pkl':
                with open(file_path, 'rb') as f:
                    episode_transitions = pickle.load(f)
            elif ext == '.npy':
                episode_transitions = np.load(file_path, allow_pickle=True)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            # Extract action transitions
            action_transitions = [(t[1], episode_transitions[i + 1][1]) 
                                for i, t in enumerate(episode_transitions[:-1])]
            
            # Create DataFrame
            df_transitions = pd.DataFrame(action_transitions, columns=['current_action', 'next_action'])
            
            # Map action indices to names
            action_names = {0: 'go_long', 1: 'go_short', 2: 'do_nothing'}
            df_transitions['current_action'] = df_transitions['current_action'].map(action_names)
            df_transitions['next_action'] = df_transitions['next_action'].map(action_names)
            
            # Compute transition matrix
            transition_matrix = df_transitions.groupby(['current_action', 'next_action']).size().unstack(fill_value=0)
            
            # Ensure all actions are included
            all_actions = ['go_long', 'go_short', 'do_nothing']
            transition_matrix = transition_matrix.reindex(index=all_actions, columns=all_actions, fill_value=0)
            
            # Normalize to get probabilities
            row_sums = transition_matrix.sum(axis=1)
            transition_matrix = transition_matrix.div(row_sums, axis=0)
            
            # Handle rows with zero transitions (NaN values)
            transition_matrix = transition_matrix.fillna(1.0 / len(all_actions))  # Equal probabilities
            
            if current_action is not None:
                # Convert current_action to name if integer
                if isinstance(current_action, int):
                    current_action = action_names.get(current_action, current_action)
                
                # Check if current_action exists
                if current_action not in transition_matrix.index:
                    print(f"Current action '{current_action}' not found in transition matrix. Using default probabilities.")
                    return {action: 1.0 / len(all_actions) for action in all_actions}  # Equal probabilities
                
                return transition_matrix.loc[current_action].to_dict()
                
            return transition_matrix
            
        except Exception as e:
            print(f"Error computing transition probabilities: {e}")
            return {} if current_action is not None else pd.DataFrame()


@dataclass
class RLmodel_small(RLModelBase):
    sma_05: float
    sma_07: float
    sma_25: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/small_q_table.npy'
    state_index_file: str = f'{Path(__file__).resolve().parent}/small_state_to_index.npy'
    episodes_file: str = None

    def __post_init__(self):
        self.episodes_file = f'{Path(__file__).resolve().parent}/small_epitrans.npy'
    def load_qtable(self):
        with open(self.model_file_path, "rb") as f:
            q_table = np.load(f)
        return q_table

    def load_state_index(self):
        with open(self.state_index_file, "rb") as f:
            state_to_index = np.load(f, allow_pickle=True).item()
        return state_to_index

    def load_action_mapping(self):
        action_mapping = {"go_long": 0, "go_short": 1, "do_nothing": 2}
        return action_mapping

    def prep_state(self):
        state = np.array([[self.sma_05, self.sma_07, self.sma_25, self.sma_compare, self.is_short]])
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)
        return state

    def predict_action(self):
        state = self.prep_state()
        loaded_qtable = self.load_qtable()
        loaded_state_to_index = self.load_state_index()
        loaded_mapping = self.load_action_mapping()


        state_tuple = tuple(state.flatten())
        state_index = loaded_state_to_index.get(state_tuple, -1)
        if not state_index == -1:
            try:
                q_values = loaded_qtable[state_index]
            except ValueError as e:
                print(e)
        else:
            # Create a KDTree from the states in the loaded_state_to_index mapping
            state_tuples = [tuple(float(x) for x in state) for state in loaded_state_to_index.keys()]
            kdtree = KDTree(state_tuples)

            # Find the nearest neighbor to the current state
            distance, index = kdtree.query(state.flatten())
            nearest_state_tuple = state_tuples[index]
            new_state_index = loaded_state_to_index[nearest_state_tuple]
            q_values = loaded_qtable[new_state_index]
            #raise ValueError("State not found in the state index mapping.")
        # Compute probabilities using softmax

        def softmax(x):
            exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return exp_x / np.sum(exp_x)

        confidence = softmax(q_values)

        # Map probabilities to action names
        action_confidence = {
            action: confidence[index] for action, index in loaded_mapping.items()
        }
        best_action_index = np.argmax(q_values)

        action = [action for action, index in loaded_mapping.items() if index == best_action_index][0]
        # Get transition probabilities for the chosen action
        trans_proba = self.compute_action_transition_proba(current_action=action)
        trans_action = max(trans_proba.items(), key=lambda x: x[1])[0] if trans_proba else None

        results_dict = {
            "raw_state": state,
            "state_tuple": state_tuple,
            "best_action_index": best_action_index,
            "action": action,
            "confidence": action_confidence,
            "trans_proba": trans_proba,
            "trans_action": trans_action
        }
        return results_dict

@dataclass
class RLmodel_large(RLModelBase):
    opening: float
    high: float
    ema_26: float
    ema_12: float
    low: float
    mean_grad_hist: float
    close: float
    volume: float
    sma_25: float
    long_jcrosk: float
    short_kdj: int
    sma_compare: int
    ask: float
    bid: float
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/large_q_table.npy'
    state_index_file: str = f'{Path(__file__).resolve().parent}/large_state_to_index.npy'
    episodes_file: str = None

    def __post_init__(self):
        self.episodes_file = f'{Path(__file__).resolve().parent}/large_epitrans.npy'

    def load_qtable(self):
        with open(self.model_file_path, "rb") as f:
            q_table = np.load(f)
        return q_table

    def load_state_index(self):
        with open(self.state_index_file, "rb") as f:
            state_to_index = np.load(f, allow_pickle=True).item()
        return state_to_index

    def load_action_mapping(self):
        action_mapping = {"go_long": 0, "go_short": 1, "do_nothing": 2}
        return action_mapping

    def prep_state(self):
        state = np.array([[self.opening, self.high, \
                          self.ema_26, self.ema_12, self.low, self.mean_grad_hist, \
                          self.close, self.volume, self.sma_25, self.long_jcrosk, \
                          self.short_kdj, self.sma_compare, self.ask, self.bid, self.is_short]]
                    )

        # Check for NaN or Inf values in the state
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)

        return state

    def predict_action(self):
        state = self.prep_state()
        loaded_qtable = self.load_qtable()
        loaded_state_to_index = self.load_state_index()
        loaded_mapping = self.load_action_mapping()


        state_tuple = tuple(state.flatten())
        state_index = loaded_state_to_index.get(state_tuple, -1)
        if not state_index == -1:
            try:
                q_values = loaded_qtable[state_index]
            except ValueError as e:
                print(e)
        else:
            # Create a KDTree from the states in the loaded_state_to_index mapping
            state_tuples = list(loaded_state_to_index.keys())
            kdtree = KDTree(state_tuples)

            # Find the nearest neighbor to the current state
            distance, index = kdtree.query(state.flatten())
            nearest_state_tuple = state_tuples[index]
            new_state_index = loaded_state_to_index[nearest_state_tuple]
            q_values = loaded_qtable[new_state_index]
            #raise ValueError("State not found in the state index mapping.")
        # Compute probabilities using softmax

        def softmax(x):
            exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return exp_x / np.sum(exp_x)

        confidence = softmax(q_values)

        # Map probabilities to action names
        action_confidence = {
            action: confidence[index] for action, index in loaded_mapping.items()
        }
        best_action_index = np.argmax(q_values)

        action = [action for action, index in loaded_mapping.items() if index == best_action_index][0]
        # Get transition probabilities for the chosen action
        trans_proba = self.compute_action_transition_proba(current_action=action)
        trans_action = max(trans_proba.items(), key=lambda x: x[1])[0] if trans_proba else None

        results_dict = {
            "raw_state": state,
            "state_tuple": state_tuple,
            "best_action_index": best_action_index,
            "action": action,
            "confidence": action_confidence,
            "trans_proba": trans_proba,
            "trans_action": trans_action
        }
        return results_dict

@dataclass
class RLmodel_bids(RLModelBase):
    ask: float
    bid: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/bids_q_table.pkl'
    state_index_file: str = f'{Path(__file__).resolve().parent}/bids_state_to_index.pkl'
    episodes_file: str = f'{Path(__file__).resolve().parent}/bids_epitrans.pkl' # Set directly

    # Attributes to store loaded data and precomputed structures
    q_table: list = None
    state_to_index_dict: dict = None
    action_mapping: dict = None
    transition_matrix: pd.DataFrame = None
    kdtree: KDTree = None
    kdtree_index_map: dict = None # Maps KDTree leaf index to original state_index

    def __post_init__(self):
        # Load data once
        self._load_data()
        # Precompute transition matrix
        self.transition_matrix = self.compute_action_transition_proba() # Call base class method
        # Build KDTree for nearest neighbor search
        self._build_kdtree()

    def _load_data(self):
        """Loads Q-table, state index, and action mapping."""
        # Load Q-table
        try:
            with open(self.model_file_path, "rb") as f:
                # Assuming pkl contains the list directly
                self.q_table = pickle.load(f)
                if not isinstance(self.q_table, list):
                     # If it's not a list (e.g., numpy array), convert it
                     self.q_table = list(self.q_table)
        except FileNotFoundError:
            print(f"Error: Q-table file not found at {self.model_file_path}")
            self.q_table = [] # Initialize empty
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            self.q_table = []

        # Load state-to-index mapping
        try:
            with open(self.state_index_file, "rb") as f:
                 # Assuming pkl contains a dict or list of tuples convertible to dict
                loaded_state_index = pickle.load(f)
                if isinstance(loaded_state_index, list):
                    self.state_to_index_dict = dict(loaded_state_index)
                elif isinstance(loaded_state_index, dict):
                    self.state_to_index_dict = loaded_state_index
                else:
                     raise TypeError("Unsupported type for state_to_index pickle")
        except FileNotFoundError:
            print(f"Error: State index file not found at {self.state_index_file}")
            self.state_to_index_dict = {} # Initialize empty
        except Exception as e:
            print(f"Error loading state index: {e}")
            self.state_to_index_dict = {}

        # Define action mapping
        self.action_mapping = {"do_nothing": 0, "go_long": 1, "go_short": 2} # Assuming only these two actions for bids

    def _build_kdtree(self):
        """Builds KDTree from numeric states in the state index."""
        numeric_states = []
        self.kdtree_index_map = {} # Maps KDTree leaf index -> original state_index

        if not self.state_to_index_dict:
            print("Warning: State index dictionary is empty. Cannot build KDTree.")
            self.kdtree = None
            return

        state_dim = len(next(iter(self.state_to_index_dict.keys()))) # Get dimension from first key

        for state_tuple, original_index in self.state_to_index_dict.items():
            try:
                # Ensure state has the correct dimension before conversion
                if len(state_tuple) == state_dim:
                    numeric_state = [float(x) for x in state_tuple]
                    # Check for NaN/Inf after conversion
                    if np.all(np.isfinite(numeric_state)):
                         current_kdtree_index = len(numeric_states)
                         numeric_states.append(numeric_state)
                         self.kdtree_index_map[current_kdtree_index] = original_index
                    # else: # Optional: print warning for non-finite states skipped
                    #    print(f"Warning: Skipping non-finite state {state_tuple}")
            except (ValueError, TypeError):
                 # Optional: print warning for states that couldn't be converted
                 # print(f"Warning: Skipping non-numeric state {state_tuple}")
                continue # Skip states that cannot be converted to float

        if not numeric_states:
            print("Warning: No valid numeric states found to build KDTree.")
            self.kdtree = None
        else:
            try:
                numeric_states_array = np.array(numeric_states)
                self.kdtree = KDTree(numeric_states_array)
                #print(f"KDTree built successfully with {len(numeric_states)} states.")
            except Exception as e:
                print(f"Error building KDTree: {e}")
                self.kdtree = None


    # Remove old loading methods
    # def load_qtable(self):
    #     with open(self.model_file_path, "rb") as f:
    #         q_table = list(pickle.load(f))
    #     return q_table

    # def load_state_index(self):
    #     with open(self.state_index_file, "rb") as f:
    #         state_to_index = list(pickle.load(f).items())
    #     return state_to_index

    # def load_action_mapping(self):
    #     action_mapping = {"go_long": 0, "go_short": 1}
    #     return action_mapping

    def prep_state(self):
        state = np.array([[self.ask, self.bid, self.sma_compare, self.is_short]])
        # Check for NaN or Inf values in the state
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)
        return state

    # Removed find_nearest_numeric_state as KDTree is used now

    def predict_action(self):
        # Ensure data is loaded
        if self.q_table is None or self.state_to_index_dict is None or self.action_mapping is None:
             print("Error: Model data not loaded properly. Run __post_init__ or _load_data().")
             # Return a default/error state
             return {
                 "raw_state": None, "state_tuple": None, "best_action_index": -1,
                 "action": "error", "confidence": {}, "trans_proba": {}, "trans_action": "error"
             }

        state = self.prep_state()
        state_tuple = tuple(state.flatten())

        # Get the index for the current state from the pre-loaded dictionary
        state_index = self.state_to_index_dict.get(state_tuple, -1)

        # If state not found, use KDTree to find nearest neighbor
        if state_index == -1:
            if self.kdtree is None:
                 print("Warning: KDTree not available. Cannot find nearest state.")
                 # Fallback or error handling needed - e.g., return default action
                 # For now, let's assume a default action like 'do_nothing' if it existed,
                 # or handle based on the available actions. Let's return an error state for clarity.
                 return {
                     "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                     "action": "error_no_state_match", "confidence": {}, "trans_proba": {},
                     "trans_action": "error_no_state_match"
                 }

            try:
                query_state_numeric = np.array([float(x) for x in state_tuple])
                if not np.all(np.isfinite(query_state_numeric)):
                    print(f"Warning: Query state {state_tuple} contains non-finite values. Cannot use KDTree.")
                    # Handle non-finite query state - return error or default
                    return {
                         "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                         "action": "error_non_finite_state", "confidence": {}, "trans_proba": {},
                         "trans_action": "error_non_finite_state"
                     }

                distance, kdtree_idx = self.kdtree.query(query_state_numeric)
                # Map KDTree index back to the original state index
                state_index = self.kdtree_index_map.get(kdtree_idx, -1)

                if state_index == -1:
                     # This shouldn't happen if kdtree_index_map is built correctly
                     print(f"Error: KDTree index {kdtree_idx} not found in map.")
                     return {
                         "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                         "action": "error_kdtree_map", "confidence": {}, "trans_proba": {},
                         "trans_action": "error_kdtree_map"
                     }
                # print(f"State {state_tuple} not found. Using nearest state with index {state_index}.") # Optional debug print

            except Exception as e:
                print(f"Error during KDTree query or state conversion: {e}")
                # Handle KDTree query error - return error or default
                return {
                     "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                     "action": "error_kdtree_query", "confidence": {}, "trans_proba": {},
                     "trans_action": "error_kdtree_query"
                 }


        # Get Q-values using the found state_index from the pre-loaded Q-table
        try:
            q_values = np.array(self.q_table[state_index]) # Ensure it's a numpy array for operations
        except IndexError:
             print(f"Error: state_index {state_index} out of bounds for Q-table length {len(self.q_table)}.")
             return {
                 "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                 "action": "error_qtable_index", "confidence": {}, "trans_proba": {},
                 "trans_action": "error_qtable_index"
             }
        except Exception as e:
             print(f"Error accessing Q-table with index {state_index}: {e}")
             return {
                 "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                 "action": "error_qtable_access", "confidence": {}, "trans_proba": {},
                 "trans_action": "error_qtable_access"
             }

        # Add small noise only if needed for tie-breaking, consider removing if not necessary
        # norm_q_values = q_values + np.random.normal(0, 1e-6, size=q_values.shape)
        norm_q_values = q_values # Use original q_values

        # Compute probabilities using the external softmax function
        # Ensure q_values is 1D array before passing to _softmax
        if norm_q_values.ndim > 1:
             # Handle unexpected dimensions if necessary, e.g., flatten or raise error
             print(f"Warning: Q-values have unexpected shape {norm_q_values.shape}. Attempting to flatten.")
             norm_q_values = norm_q_values.flatten()

        # Check if number of q_values matches number of actions
        if len(norm_q_values) != len(self.action_mapping):
             print(f"Error: Number of Q-values ({len(norm_q_values)}) does not match number of actions ({len(self.action_mapping)}). State index: {state_index}")
             return {
                 "raw_state": state, "state_tuple": state_tuple, "best_action_index": -1,
                 "action": "error_qvalue_mismatch", "confidence": {}, "trans_proba": {},
                 "trans_action": "error_qvalue_mismatch"
             }

        confidence_array = _softmax(norm_q_values).flatten() # Use helper softmax

        # Map probabilities to action names using pre-loaded mapping
        action_confidence = {
            action: confidence_array[index] for action, index in self.action_mapping.items()
        }

        # Find the best action index
        best_action_index = np.argmax(norm_q_values)
        # Get action name from index
        action = [action for action, index in self.action_mapping.items()
                  if index == best_action_index]
        # Ensure action is found (should always be true if best_action_index is valid)
        action = action[0] if action else "error_action_not_found"


        # Get transition probabilities from the precomputed matrix
        trans_proba = {}
        if self.transition_matrix is not None and not self.transition_matrix.empty:
             if action in self.transition_matrix.index:
                 trans_proba = self.transition_matrix.loc[action].to_dict()
             else:
                 # Handle case where action might not be in the transition matrix index
                 # (e.g., if episode data was incomplete)
                 # Provide default uniform probabilities or handle as error
                 print(f"Warning: Action '{action}' not found in precomputed transition matrix index. Returning empty probabilities.")
                 # trans_proba = {act: 1.0/len(self.action_mapping) for act in self.action_mapping} # Option: Uniform proba
        else:
             print("Warning: Precomputed transition matrix is not available or empty.")


        # Determine transition action based on probabilities
        trans_action = max(trans_proba.items(), key=lambda x: x[1])[0] if trans_proba else action # Fallback to current action if no proba

        # Prepare results
        return {
            "raw_state": state,
            "state_tuple": state_tuple,
            "best_action_index": best_action_index,
            "action": action,
            "confidence": action_confidence,
            "trans_proba": trans_proba,
            "trans_action": trans_action
        }


def main(model_type: str, sma_05: float = None, sma_07: float = None, 
         sma_25: float = None, sma_compare: int = None, is_short: int = None,
         opening: float = None, high: float = None, ema_26: float = None,
         ema_12: float = None, low: float = None, mean_grad_hist: float = None,
         close: float = None, volume: float = None, long_jcrosk: float = None,
         short_kdj: int = None, ask: float = None, bid: float = None):
    """
    Main function to handle command line interface.
    
    Args:
        model_type: str - Type of model to use ('small', 'large', or 'bids')
        ... (other parameters specific to each model)
    """
    if model_type.lower() == "small":
        if any(x is None for x in [sma_05, sma_07, sma_25, sma_compare, is_short]):
            raise ValueError("Small model requires: sma_05, sma_07, sma_25, sma_compare, is_short")
        model = RLmodel_small(
            sma_05=float(sma_05),
            sma_07=float(sma_07),
            sma_25=float(sma_25),
            sma_compare=int(sma_compare),
            is_short=int(is_short)
        )
    elif model_type.lower() == "large":
        # Check and create large model
        if any(x is None for x in [opening, high, ema_26, ema_12, low, mean_grad_hist,
                                 close, volume, sma_25, long_jcrosk, short_kdj,
                                 sma_compare, ask, bid, is_short]):
            raise ValueError("Large model requires all parameters")
        model = RLmodel_large(
            opening=float(opening),
            high=float(high),
            ema_26=float(ema_26),
            ema_12=float(ema_12),
            low=float(low),
            mean_grad_hist=float(mean_grad_hist),
            close=float(close),
            volume=float(volume),
            sma_25=float(sma_25),
            long_jcrosk=float(long_jcrosk),
            short_kdj=int(short_kdj),
            sma_compare=int(sma_compare),
            ask=float(ask),
            bid=float(bid),
            is_short=int(is_short)
        )
    elif model_type.lower() == "bids":
        if any(x is None for x in [ask, bid, sma_compare, is_short]):
            raise ValueError("Bids model requires: ask, bid, sma_compare, is_short")
        model = RLmodel_bids(
            ask=float(ask),
            bid=float(bid),
            sma_compare=int(sma_compare),
            is_short=int(is_short)
        )
    else:
        raise ValueError("Invalid model type. Choose 'small', 'large', or 'bids'")

    result = model.predict_action()

    return result

# Use case
#print(RLmodel_large(1, 4, 0, 1, 0, 4, 7, 2, 3, 6, 0, 7, 0, 1, 0).predict_action())
#print(RLmodel_bids(1, 4, 0, 1).predict_action())



if __name__ == "__main__":
    fire.Fire(main)

