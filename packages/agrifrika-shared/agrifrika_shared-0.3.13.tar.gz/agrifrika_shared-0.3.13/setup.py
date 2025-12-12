"""
Setup configuration for agrifrika-shared package.

This package contains shared utilities, models, and AWS clients
for all Agrifrika microservices.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agrifrika-shared",
    version="0.3.13",
    author="Agrifrika Team",
    author_email="tech@agrifrika.com",
    description="Shared utilities and models for Agrifrika microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agrifrika/agrifrika-backend",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
            "boto3>=1.26.0",
            "moto>=4.0.0",
        ],
    },
)
