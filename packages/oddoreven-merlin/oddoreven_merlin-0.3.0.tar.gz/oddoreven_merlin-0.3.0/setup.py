from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oddoreven-merlin",
    version="0.3.0",  # 🔹 bumped version from 0.1.0 to 0.2.0
    author="Merlin",
    author_email="merlinfathima88@gmail.com",
    description="A simple Python library to check whether a number is odd or even",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={           # 🔹 this part is new
        "console_scripts": [
            "oddoreven=oddoreven.cli:main",
        ],
    },
)
