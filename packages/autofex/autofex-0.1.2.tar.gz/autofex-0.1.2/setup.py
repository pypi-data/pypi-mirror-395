"""
Setup script for AutoFE-X package.
"""

from setuptools import setup, find_packages
import os

# Read README
this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = """
        AutoFE-X: Automated Feature Engineering, Data Profiling, and Leakage Detection

        AutoFE-X provides a unified framework for building feature-centric ML pipelines. 
        It combines automated feature creation, dataset diagnostics, leakage risk assessment,
        benchmarking utilities, and graph-based feature lineage into a single, 
        lightweight and interpretable toolkit...

        Core capabilities include:
            - Automated generation of numerical, categorical, and interaction features
            - Comprehensive data quality and statistical profiling
            - Detection of target leakage and train–test inconsistencies
            - Comparative evaluation of feature sets across models
            - Traceable feature provenance using graph-based lineage tracking

    Designed to be efficient, transparent, and easy to integrate into both research workflows and production pipelines.
    """

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

try:
    requirements = read_requirements('requirements.txt')
except FileNotFoundError:
    requirements = [
        'pandas>=1.3.0,<2.3.0',
        'numpy>=1.20.0,<2.2.0',
        'scikit-learn>=1.0.0',
        'scipy>=1.7.0',
        'networkx>=2.6.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
    ]

setup(
    name="autofex",
    version="0.1.2",
    author="AutoFE-X",
    author_email="sudo.dev26@gmail.com",
    description="Automated Feature Engineering + Data Profiling + Leakage Detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudo-de/autofex",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Science",
        "Intended Audience :: Machine Learning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8,<3.14",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.800",
            "sphinx>=4.0.0",
            "jupyter>=1.0.0",
            "codecov>=2.1.0",
        ],
        "viz": [
            "plotly>=5.0.0",
            "graphviz>=0.17.0",
        ],
        "test": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "autofex=autofex.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
