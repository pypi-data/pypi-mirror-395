#!/usr/bin/env python3
"""
whois-charman: A cross-blockchain event prediction exchange arbitrage platform.

This package provides tools for monitoring events across multiple prediction
markets, calculating arbitrage opportunities, and executing trades.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name="whois-charman",
    version="0.1.2",
    author="mroy",
    author_email="mroy@example.com",
    description="A cross-blockchain event prediction exchange arbitrage platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://git.me/dr/whois-charman",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "whois-task=whoischarman.cli.schedule:main",
        ],
    },
    include_package_data=True,
    package_data={
        "whoischarman": [
            "*.yaml",
            "*.yml",
            "*.json",
            "*.ini",
        ],
    },
    keywords=[
        "arbitrage",
        "prediction markets",
        "blockchain",
        "trading",
        "finance",
        "kalshi",
        "polymarket",
        "cryptocurrency",
        "betting",
        "financial analysis",
    ],
    project_urls={
        "Bug Reports": "https://git.me/dr/whois-charman/issues",
        "Source": "https://git.me/dr/whois-charman",
        "Documentation": "https://git.me/dr/whois-charman/docs",
    },
)