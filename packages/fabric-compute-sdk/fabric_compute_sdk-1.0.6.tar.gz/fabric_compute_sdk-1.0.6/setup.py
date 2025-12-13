"""Setup script for Fabric SDK"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fabric-compute-sdk",
    version="1.0.6",
    author="Carmel Labs, Inc.",
    author_email="hello@carmel.so",
    description="Official Python SDK for Fabric - Distributed AI Compute Network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Carmel-Labs-Inc/fabric-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "mypy>=1.5.0",
        ],
    },
)


