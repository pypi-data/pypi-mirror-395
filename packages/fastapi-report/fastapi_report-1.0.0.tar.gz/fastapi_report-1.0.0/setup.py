"""Setup configuration for fastapi-report package."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="fastapi-report",
    version="1.0.0",
    author="FastAPI Report Contributors",
    author_email="",
    description="Universal FastAPI documentation generator - automatically document REST endpoints and MCP tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fastapi-report",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "pydantic>=2.0.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "hypothesis>=6.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "mcp": [
            "fastapi-mcp>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fastapi-report=fastapi_report.cli:main",
        ],
    },
    keywords="fastapi documentation openapi mcp api-documentation swagger",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/fastapi-report/issues",
        "Source": "https://github.com/yourusername/fastapi-report",
        "Documentation": "https://github.com/yourusername/fastapi-report#readme",
    },
)
