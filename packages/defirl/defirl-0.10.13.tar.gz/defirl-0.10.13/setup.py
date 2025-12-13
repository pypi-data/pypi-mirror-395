try:
    from setuptools import setup, find_packages
    #from Cython.Build import cythonize
except ImportError as e:
    from distutils.core import setup, find_packages
    print(e)
setup(
    name='defirl',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        "": ["*.pkl"],
        "": ["*.npy"],
        "defirl": ["*.pkl"],
    },
    platforms='any',
    version='0.10.13',
    description='A reinforcement learning package for predicting buy and sell signals',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=58.1.0",
    	"wheel>=0.37.1",
        "scikit-learn>=1.4.0",
        "fire"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/defirl/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
