import pandas as pd
import numpy as np
from dataclasses import dataclass
import pickle
from pathlib import Path
import fire
from importlib.resources import files
from scipy.spatial import KDTree


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
class RLmodel50(RLModelBase):
    ask: float
    bid: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/bid50_q_table.npy'
    state_index_file: str = f'{Path(__file__).resolve().parent}/bid50_state_to_index.npy'
    episodes_file: str = None

    def __post_init__(self):
        self.episodes_file = f'{Path(__file__).resolve().parent}/bid50_epitrans.npy'

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
        state = np.array([[self.ask, self.bid, self.sma_compare, self.is_short]])

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
class RLmodel74(RLModelBase):
    ask: float
    bid: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/bid74_q_table.pkl'
    state_index_file: str = f'{Path(__file__).resolve().parent}/bid74_state_to_index.pkl'
    episodes_file: str = None

    def __post_init__(self):
        self.episodes_file = f'{Path(__file__).resolve().parent}/bid74_epitrans.pkl'

    def load_qtable(self):
        with open(self.model_file_path, "rb") as f:
            q_table = list(pickle.load(f))
        return q_table

    def load_state_index(self):
        with open(self.state_index_file, "rb") as f:
            state_to_index = list(pickle.load(f).items())
        return state_to_index

    def load_action_mapping(self):
        action_mapping = {"go_long": 0, "go_short": 1, "do_nothing": 2}
        return action_mapping

    def prep_state(self):
        state = np.array([[self.ask, self.bid, self.sma_compare, self.is_short]])
        # Check for NaN or Inf values in the state
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)
        return state

    def find_nearest_numeric_state(self, state_tuple, loaded_state_to_index):
        numeric_states = []
        numeric_indices = {}
        
        for state, idx in loaded_state_to_index:
            try:
                # Only process states with the same length as our input state
                if len(state) == len(state_tuple):
                    numeric_state = [float(x) for x in state]
                    numeric_states.append(numeric_state)
                    numeric_indices[len(numeric_states) - 1] = idx
            except (ValueError, TypeError):
                continue

        if not numeric_states:
            return -1

        numeric_states = np.array(numeric_states)
        query_state = np.array([float(x) for x in state_tuple])
        
        # Use Euclidean distance to find nearest neighbor
        distances = np.linalg.norm(numeric_states - query_state, axis=1)
        nearest_idx = np.argmin(distances)
        
        return numeric_indices[nearest_idx]

    def predict_action(self):
        state = self.prep_state()
        loaded_qtable = self.load_qtable()
        loaded_state_to_index = self.load_state_index()
        loaded_mapping = self.load_action_mapping()

        # Convert state to a tuple
        state_tuple = tuple(state.flatten())

        # Convert loaded_state_to_index to a dictionary for faster lookups
        state_to_index_dict = dict(loaded_state_to_index)

        # Get the index for the current state
        state_index = state_to_index_dict.get(state_tuple, -1)

        # If state not found, find nearest numeric state
        if state_index == -1:
            state_index = self.find_nearest_numeric_state(state_tuple, loaded_state_to_index)
            if state_index == -1:
                # Fallback to default action if no valid state found
                return {
                    "raw_state": state,
                    "state_tuple": state_tuple,
                    "best_action_index": loaded_mapping["do_nothing"],
                    "action": "do_nothing",
                    "confidence": {action: 1.0 if action == "do_nothing" else 0.0 
                                 for action in loaded_mapping},
                    "trans_proba": {},
                    "trans_action": "do_nothing"
                }

        # Get Q-values for the state
        q_values = loaded_qtable[state_index]
        # Normalize q_values to avoid overflow in softmax
        norm_q_values = q_values + np.random.normal(0, 1e-6, size=q_values.shape)

        # Compute probabilities using softmax
        def softmax(x):
            exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return exp_x / np.sum(exp_x)

        confidence = softmax(norm_q_values)

        # Map probabilities to action names
        action_confidence = {
            action: confidence[index] for action, index in loaded_mapping.items()
        }

        # Find the best action
        best_action_index = np.argmax(norm_q_values)
        action = [action for action, index in loaded_mapping.items() 
                 if index == best_action_index][0]

        # Find the action with the maximum confidence
        trans_action = max(action_confidence, key=action_confidence.get)

        # Handle transition probabilities
        try:
            trans_proba = self.compute_action_transition_proba(current_action=action)
        except KeyError:
            trans_proba = {}

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

@dataclass
class RLmodel86(RLModelBase):
    ask: float
    bid: float
    sma_compare: int
    is_short: int

    model_file_path: str = f'{Path(__file__).resolve().parent}/bid86_q_table.pkl'
    state_index_file: str = f'{Path(__file__).resolve().parent}/bid86_state_to_index.pkl'
    episodes_file: str = None

    def __post_init__(self):
        self.episodes_file = f'{Path(__file__).resolve().parent}/bid86_epitrans.pkl'

    def load_qtable(self):
        with open(self.model_file_path, "rb") as f:
            q_table = list(pickle.load(f))
        return q_table

    def load_state_index(self):
        with open(self.state_index_file, "rb") as f:
            state_to_index = list(pickle.load(f).items())
        return state_to_index

    def load_action_mapping(self):
        action_mapping = {"go_long": 0, "go_short": 1, "do_nothing": 2}
        return action_mapping

    def prep_state(self):
        state = np.array([[self.ask, self.bid, self.sma_compare, self.is_short]])
        # Check for NaN or Inf values in the state
        if not np.all(np.isfinite(state)):
            state = np.nan_to_num(state, nan=0.0, posinf=0.0, neginf=0.0)
        return state

    def find_nearest_numeric_state(self, state_tuple, loaded_state_to_index):
        numeric_states = []
        numeric_indices = {}
        
        for state, idx in loaded_state_to_index:
            try:
                # Only process states with the same length as our input state
                if len(state) == len(state_tuple):
                    numeric_state = [float(x) for x in state]
                    numeric_states.append(numeric_state)
                    numeric_indices[len(numeric_states) - 1] = idx
            except (ValueError, TypeError):
                continue

        if not numeric_states:
            return -1

        numeric_states = np.array(numeric_states)
        query_state = np.array([float(x) for x in state_tuple])
        
        # Use Euclidean distance to find nearest neighbor
        distances = np.linalg.norm(numeric_states - query_state, axis=1)
        nearest_idx = np.argmin(distances)
        
        return numeric_indices[nearest_idx]

    def predict_action(self):
        state = self.prep_state()
        loaded_qtable = self.load_qtable()
        loaded_state_to_index = self.load_state_index()
        loaded_mapping = self.load_action_mapping()

        # Convert state to a tuple
        state_tuple = tuple(state.flatten())

        # Convert loaded_state_to_index to a dictionary for faster lookups
        state_to_index_dict = dict(loaded_state_to_index)

        # Get the index for the current state
        state_index = state_to_index_dict.get(state_tuple, -1)

        # If state not found, find nearest numeric state
        if state_index == -1:
            state_index = self.find_nearest_numeric_state(state_tuple, loaded_state_to_index)
            if state_index == -1:
                # Fallback to default action if no valid state found
                return {
                    "raw_state": state,
                    "state_tuple": state_tuple,
                    "best_action_index": loaded_mapping["do_nothing"],
                    "action": "do_nothing",
                    "confidence": {action: 1.0 if action == "do_nothing" else 0.0 
                                 for action in loaded_mapping},
                    "trans_proba": {},
                    "trans_action": "do_nothing"
                }

        # Get Q-values for the state
        q_values = loaded_qtable[state_index]
        # Normalize q_values to avoid overflow in softmax
        norm_q_values = q_values + np.random.normal(0, 1e-6, size=q_values.shape)

        # Compute probabilities using softmax
        def softmax(x):
            exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
            return exp_x / np.sum(exp_x)

        confidence = softmax(norm_q_values)

        # Map probabilities to action names
        action_confidence = {
            action: confidence[index] for action, index in loaded_mapping.items()
        }

        # Find the best action
        best_action_index = np.argmax(norm_q_values)
        action = [action for action, index in loaded_mapping.items() 
                 if index == best_action_index][0]

        # Find the action with the maximum confidence
        trans_action = max(action_confidence, key=action_confidence.get)

        # Handle transition probabilities
        try:
            trans_proba = self.compute_action_transition_proba(current_action=action)
        except KeyError:
            trans_proba = {}

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

def main(model_type: str, sma_compare: int = None, is_short: int = None,
         ask: float = None, bid: float = None):
    """
    Main function to handle command line interface.
    
    Args:
        model_type: str - Type of model to use ('small', 'large', or 'bids')
        ... (other parameters specific to each model)
    """
    if model_type.lower() == "bid50":
        if any(x is None for x in [ask, bid, sma_compare, is_short]):
            raise ValueError("Bid50 model requires: ask, bid, sma_compare, is_short")
        model = RLmodel50(
            ask=float(ask),
            bid=float(bid),
            sma_compare=int(sma_compare),
            is_short=int(is_short)
        )
    elif model_type.lower() == "bid74":
        # Check and create large model
        if any(x is None for x in [ask, bid, sma_compare, is_short]):
            raise ValueError("Bid74 model requires ask, bid, sma_compare, is_short")
        model = RLmodel74(
            ask=float(ask),
            bid=float(bid),
            sma_compare=int(sma_compare),
            is_short=int(is_short)
        )
    elif model_type.lower() == "bid86":
        if any(x is None for x in [ask, bid, sma_compare, is_short]):
            raise ValueError("Bid86 model requires: ask, bid, sma_compare, is_short")
        model = RLmodel86(
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
#print(RLmodel86(1, 4, 0, 1).predict_action().get('action'))



if __name__ == "__main__":
    fire.Fire(main)

