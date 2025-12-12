from setuptools import setup, find_packages
import os

def get_version():
    """Read version from version file"""
    version_file = os.path.join(os.path.dirname(__file__), "shade_privacy", "__version__.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.0.0"

def get_long_description():
    """Read README.md"""
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="shade-privacy",
    version=get_version(),
    author="Shade Privacy",
    author_email="ikinyapeter93@gmail.com",
    description="Python SDK for private cross-chain transactions with ZK proofs. Supports ETH, SOL, StarkNet, Base, Sei, AVAX, SUI + 13 chains.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/Shade-privacy/python-sdk",
    project_urls={
        "Homepage": "https://shadeprivacy.com",
        "Documentation": "https://docs.shadeprivacy.com",
        "Source Code": "https://github.com/Shade-privacy/python-sdk",
        "Bug Tracker": "https://github.com/Shade-privacy/python-sdk/issues",
        "Changelog": "https://github.com/Shade-privacy/python-sdk/releases",
        "Discord": "https://discord.gg/shade-privacy",
        "Twitter": "https://twitter.com/shade_privacy",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "websockets>=11.0.0",
        "pycryptodome>=3.17.0",
    ],
    keywords="privacy, blockchain, zk, zero-knowledge, cross-chain, ethereum, solana, starknet, cryptocurrency, web3",
)