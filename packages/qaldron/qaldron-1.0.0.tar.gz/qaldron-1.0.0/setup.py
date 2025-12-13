"""
QALDRON Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description with explicit UTF-8 encoding
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="qaldron",
    version="1.0.0",
    author="QALDRON Team",
    author_email="team@qaldron.dev",
    description="Quantum-Assisted Ledger for Distributed Autonomous Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qaldron/qaldron",
    packages=find_packages(exclude=["server", "server.*", "demo", "demo.*", "tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.17,<3",
        "scipy>=1.5",
        "pyyaml>=6.0",
        "cryptography>=41.0.0",
        "requests>=2.31.0",  # Added for SDK server communication
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qaldron=qaldron.cli:main",
            "qaldrond=qaldron.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "qaldron": ["config/*.yaml"],
    },
)
