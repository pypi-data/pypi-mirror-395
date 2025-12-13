# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="EC312",
    version="0.5",
    description="Bibliothèque de fonctions pour le cours de machine learning du STAPS de Reims",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yvan Pavlov",
    author_email="yvanpratviel@yahoo.fr",
    license="STAPS",
    classifiers=[
        "Intended Audience :: Education",
        "License :: OSI Approved",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent"
    ],
    packages=["EC312"],
    include_package_data=True,
    install_requires=["numpy", "matplotlib", "scikit-learn", "pandas"]
)