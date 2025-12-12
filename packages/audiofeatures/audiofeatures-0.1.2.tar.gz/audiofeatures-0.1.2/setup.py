from setuptools import setup, find_packages

# Read README.md for PyPI description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="audiofeatures",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "librosa",
        "numpy",
        "pandas",
        "soundfile"
    ],
    description="Extract MFCC, spectral, and pitch features from audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
