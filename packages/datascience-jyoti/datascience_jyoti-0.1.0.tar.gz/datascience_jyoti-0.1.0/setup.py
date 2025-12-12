from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datascience-jyoti",  # Unique name for PyPI
    version="0.1.0",
    author="Jyoti Rahate",
    author_email="your.email@example.com",  # Add your email
    description="A collection of neural network implementations and soft computing algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jyotirahate/datascience",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "minisom",
        "neurodynex",
        "fuzzywuzzy",
        "python-Levenshtein",
        "scikit-fuzzy",
        "networkx",
        "numpy",
        "scipy",
        "matplotlib",
    ],
)
