from setuptools import setup, find_packages
from pathlib import Path

# Read README for the long description on PyPI
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else "Official Amorce Protocol SDK"

setup(
    name="amorce-sdk",
    version="0.2.1",  # MCP + HITL + verify_request + to_manifest_json
    description="Official Python SDK for the Amorce Agent Transaction Protocol (AATP)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Athena Architecture",
    author_email="dev@amorce.io",
    url="https://github.com/trebortGolin/amorce_py_sdk",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "httpx>=0.25.0",
        "tenacity>=8.0.0",
        "cryptography>=41.0.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "respx>=0.20.0",
            "mypy>=1.5.0",
        ],
        "gcp": [
            "google-cloud-secret-manager>=2.16.0",
            "firebase-admin>=6.2.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 4 - Beta",
    ],
)