from setuptools import setup, find_packages

setup(
    name="model-training",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
       "scikit-learn~=1.6.1",
       "joblib~=1.4.2",
       "pandas~=2.2.3",
       "numpy~=2.2.5",
       "git+https://github.com/remla25-team1/lib-ml.git@v1.0.2#egg=lib_ml"
    ],
    python_requires='>=3.10',
)