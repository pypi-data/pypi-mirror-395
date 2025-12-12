from setuptools import setup, find_packages

setup(
    name="audiofeatures",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "librosa",
        "numpy",
        "pandas",
        "soundfile"
    ],
    description="Extract MFCC, spectral, and pitch features from audio files",
)