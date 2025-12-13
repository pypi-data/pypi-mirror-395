"""
Setup script for fraq-nettrade-abstractions package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fraq-nettrade-abstractions",
    version="0.1.5",
    author="FraQLabs",
    author_email="contact@fraqlabs.com",
    description="SDK for developing trading strategies in Python for FraQ NetTrade",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FraQLabs/FraQ-NetTrade",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        # No dependencies - pure Python type hints
    ],
    extras_require={
        "debug": ["debugpy>=1.6.0"],
    },
    keywords="trading backtesting algorithmic-trading quantitative-finance",
)