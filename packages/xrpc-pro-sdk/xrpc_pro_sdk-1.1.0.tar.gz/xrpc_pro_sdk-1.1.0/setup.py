"""
Setup script for xRPC Python SDK
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="xrpc-pro-sdk",
    version="1.1.0",
    description="Official Python SDK for xRPC - Multi-chain RPC Gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="xRPC",
    author_email="support@xrpc.pro",
    url="https://app.xrpc.pro",
    project_urls={
        "Documentation": "https://docs.xrpc.pro",
        "Support": "https://t.me/xnode_support",
        "GitHub": "https://github.com/xrpcpro/xrpc-sdk-python",
    },
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "urllib3>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
    ],
    keywords=[
        "rpc",
        "ethereum",
        "blockchain",
        "web3",
        "json-rpc",
        "multi-chain",
        "polygon",
        "arbitrum",
        "optimism",
        "base",
        "beacon",
        "wss",
        "websocket",
        "python",
        "sdk",
        "api",
    ],
)

