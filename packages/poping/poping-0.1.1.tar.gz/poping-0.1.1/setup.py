"""
Setup script for Poping SDK.
"""

from setuptools import setup, find_packages

setup(
    name="poping",
    version="0.1.1",
    description="Poping AI Agent SDK",
    author="Poping",
    packages=["src"],
    package_dir={"src": "src"},
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.10",
)
