from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oddoreven-merlin",  # package name on PyPI – you can change later
    version="0.1.0",
    author="Merlin",
    author_email="you@example.com",
    description="A simple Python library to check whether a number is odd or even",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # can be left empty if you don't have GitHub
    packages=find_packages(),
    python_requires=">=3.7",
)
