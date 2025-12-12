from setuptools import setup, find_packages

setup(
    name="my-ai-lib-lena",  # Name MUST be unique on PyPI. Change if needed.
    version="0.1.0",
    description="A simple AI helper library for generating responses",
    author="Lena Mathew",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
)
