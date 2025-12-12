from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ronet", 
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight deep learning framework built on NumPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohit-2304/ronet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas", 
    ],
)