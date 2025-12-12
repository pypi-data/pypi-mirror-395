from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="aastha",
    version="0.1.0",
    author="Aastha",
    author_email="aastha@example.com",
    description="A CLI tool for drawing graphics with turtle and playing sounds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aastha/aastha",
    py_modules=["main", "cake", "heart", "virus", "disco"],
    package_data={"": ["*.wav"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "simpleaudio",
    ],
    entry_points={
        "console_scripts": [
            "aastha=main:main",
        ],
    },
)
