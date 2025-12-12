"""
Thermodynamic Truth Protocol - Setup Configuration
"""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_file(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="thermodynamic-truth",
    version="1.1.0",
    author="Kevin KULL",
    author_email="research@thermodynamic-truth.org",
    description="Byzantine Fault Tolerant Consensus Based on Thermodynamic Principles",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Kuonirad/thermo-truth-proto",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "grpcio>=1.50.0",
        "grpcio-tools>=1.50.0",
        "protobuf>=4.21.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
        ],
        "viz": [
            "matplotlib>=3.5.0",
            "seaborn>=0.12.0",
        ],
        "dashboard": [
            "flask>=2.2.0",
            "plotly>=5.11.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "matplotlib>=3.5.0",
            "seaborn>=0.12.0",
            "flask>=2.2.0",
            "plotly>=5.11.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "thermo-node=thermodynamic_truth.cli.node:main",
            "thermo-client=thermodynamic_truth.cli.client:main",
            "thermo-benchmark=thermodynamic_truth.cli.benchmark:main",
        ],
    },
    include_package_data=True,
    package_data={
        "thermodynamic_truth": [
            "network/*.proto",
        ],
    },
    zip_safe=False,
)
