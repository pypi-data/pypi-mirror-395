"""
Setup script for XiaoShi AI Hub Python SDK

This setup.py is maintained for backward compatibility.
The primary configuration is in pyproject.toml.
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read the README file
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Python SDK for XiaoShi AI Hub"

# Read version from __init__.py
version = "1.1.2"
init_file = Path(__file__).parent / "xiaoshiai_hub" / "__init__.py"
if init_file.exists():
    with open(init_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

# Core dependencies
install_requires = [
    "requests>=2.20.0,<3.0.0",
    "tqdm>=4.62.0,<5.0.0",
]

# Optional dependencies
extras_require = {
    # Upload functionality (requires Git operations)
    "upload": [
        "gitpython>=3.1.0,<4.0.0",
    ],

    # Encryption support (provided by xpai-enc)
    # Note: xpai-enc must be installed separately from GitHub
    # pip install git+https://github.com/poxiaoyun/xpai-enc.git
    "encryption": [
        # xpai-enc is not on PyPI, must be installed manually
        # Listed here for documentation purposes only
    ],

    # Development dependencies
    "dev": [
        # Testing
        "pytest>=6.0,<8.0",
        "pytest-cov>=2.0,<5.0",
        "pytest-mock>=3.6.0,<4.0.0",

        # Code formatting
        "black>=22.0,<24.0",
        "isort>=5.10.0,<6.0.0",

        # Linting
        "flake8>=4.0,<7.0",

        # Type checking
        "mypy>=0.950,<2.0",
        "types-requests>=2.20.0",

        # Building and publishing
        "build>=0.8.0,<2.0.0",
        "twine>=4.0.0,<5.0.0",

        # Optional features (for testing)
        "gitpython>=3.1.0,<4.0.0",
    ],

    # Testing only (minimal test dependencies)
    "test": [
        "pytest>=6.0,<8.0",
        "pytest-cov>=2.0,<5.0",
        "pytest-mock>=3.6.0,<4.0.0",
    ],

    # Documentation
    "docs": [
        "sphinx>=4.0,<7.0",
        "sphinx-rtd-theme>=1.0,<2.0",
        "myst-parser>=0.18,<2.0",
    ],
}

# Convenience extras
extras_require["all"] = list(set(
    extras_require["upload"]
    # Note: encryption requires manual installation of xpai-enc
))

# Full installation (all features + dev tools)
extras_require["full"] = list(set(
    extras_require["all"] +
    extras_require["dev"]
))

setup(
    # Package metadata
    name="xiaoshiai-hub",
    version=version,
    author="XiaoShi AI",
    author_email="support@xiaoshiai.cn",
    maintainer="XiaoShi AI Team",
    maintainer_email="support@xiaoshiai.cn",

    # Description
    description="Python SDK for XiaoShi AI Hub - Upload, download, and manage AI models and datasets with xpai-enc encryption support",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # URLs
    url="https://github.com/poxiaoyun/moha-sdk",
    project_urls={
        "Homepage": "https://github.com/poxiaoyun/moha-sdk",
        "Repository": "https://github.com/poxiaoyun/moha-sdk",
        "Issues": "https://github.com/poxiaoyun/XiaoShi-Moha/moha-sdk",
    },

    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    include_package_data=True,

    # Requirements
    python_requires=">=3.7",
    install_requires=install_requires,
    extras_require=extras_require,

    # Classifiers
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",

        # Intended audience
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        # Topics
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",

        # License
        "License :: OSI Approved :: Apache Software License",

        # Operating systems
        "Operating System :: OS Independent",

        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",

        # Additional classifiers
        "Typing :: Typed",
    ],

    # Keywords for PyPI search
    keywords=[
        "xiaoshi",
        "ai-hub",
        "machine-learning",
        "deep-learning",
        "model-hub",
        "dataset",
        "encryption",
        "xpai-enc",
        "sdk",
        "api-client",
        "model-encryption",
    ],

    # Entry points
    entry_points={
        "console_scripts": [
            "moha=xiaoshiai_hub.cli:main",
        ],
    },

    # Package data
    package_data={
        "xiaoshiai_hub": ["py.typed"],
    },

    # Zip safe
    zip_safe=False,
)
