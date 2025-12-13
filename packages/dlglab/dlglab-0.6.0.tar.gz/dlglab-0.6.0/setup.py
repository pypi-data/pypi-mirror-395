from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dlglab",
    version="0.6.0",
    author="Chirag T",
    author_email="t.chiru2005@gmail.com",
    description="A simple package that prints hello world",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tchirag03/dlglab",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
