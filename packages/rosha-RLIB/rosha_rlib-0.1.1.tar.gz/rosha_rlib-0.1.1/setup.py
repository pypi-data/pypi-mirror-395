from setuptools import setup, find_packages

setup(
    name="rosha_RLIB",                       # Library name (PyPI name)
    version="0.1.1",                   # Start with version 0.1.0
    author="Rosha Thankachan ",
    author_email="roshathankachan459@gmail.com",
    description="A simple AI helper library for generating responses, summarizing text, and formatting output.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),          # Automatically finds RLIB package
    install_requires=[
        "openai",                      # or any AI API dependency
        "requests"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
