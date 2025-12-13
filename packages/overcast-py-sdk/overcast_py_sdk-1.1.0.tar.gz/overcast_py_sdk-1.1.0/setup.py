"""
Setup configuration for Overcast Python SDK
"""

from setuptools import setup, find_packages

long_description = "Simple incident detection and monitoring SDK for Python applications. Add automatic incident detection to any Python app with just 2 lines of code."

setup(
    name="overcast-py-sdk",
    version="1.1.0",
    author="Overcast Team",
    author_email="raghav@overcastsre.com",
    description="Simple incident detection and monitoring SDK for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/overcast/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    keywords="monitoring, incident detection, logging, observability, error tracking",
)
