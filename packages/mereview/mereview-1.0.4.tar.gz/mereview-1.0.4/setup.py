from setuptools import setup

setup(
    name="mereview",
    version="1.0.0",
    py_modules=["main"],
    install_requires=[
        "click>=8.1.0",
        "requests>=2.31.0",
        "nbformat>=5.9.0",
        "nbconvert>=7.9.0",
        "google-generativeai>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "mereview=main:main",
        ],
    },
    author="Your Name",
    description="A CLI tool for reviewing coding assignments and notebooks",
    python_requires=">=3.8",
)
