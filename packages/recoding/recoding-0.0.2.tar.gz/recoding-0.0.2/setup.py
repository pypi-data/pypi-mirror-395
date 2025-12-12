from setuptools import setup, find_packages

setup(
    name="recoding",
    version="0.0.2",
    packages=find_packages(),
    author="bzNAK",
    description="recoding",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",

)