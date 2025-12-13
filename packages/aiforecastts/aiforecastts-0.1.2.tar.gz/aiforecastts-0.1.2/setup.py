from setuptools import setup, find_packages

setup(
    name="aiforecastts",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "statsmodels>=0.14",
    ],
)
