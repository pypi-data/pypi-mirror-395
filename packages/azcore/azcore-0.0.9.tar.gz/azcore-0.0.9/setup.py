"""
Setup configuration for Azcore..
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    try:
        long_description = readme_file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        long_description = readme_file.read_text(encoding="utf-8", errors="ignore")

# Read requirements from requirements.txt and convert == to >= for compatibility
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    # Try different encodings (UTF-16 LE, UTF-8 with BOM, UTF-8)
    for encoding in ["utf-16-le", "utf-16", "utf-8-sig", "utf-8"]:
        try:
            with open(requirements_file, encoding=encoding, errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    # Remove BOM if present
                    line = line.lstrip('\ufeff')
                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    # Convert exact version pins (==) to minimum version (>=) for better compatibility
                    if "==" in line:
                        line = line.replace("==", ">=")
                    requirements.append(line)
            break  # Successfully read, exit loop
        except (UnicodeDecodeError, UnicodeError):
            requirements = []  # Reset and try next encoding
            continue

setup(
    name="azcore",
    version="0.0.9",
    author="Azrienlabs team",
    author_email="info@azrianlabs.com",
    description="A professional hierarchical multi-agent framework built on python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Azrienlabs/Az-Core",
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "mcp": [
            "langchain-mcp-adapters>=0.1.0",
        ],
        "rl": [
            "torch>=2.0.0",
            "sentence-transformers>=2.0.0",
            "scikit-learn>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "azcore": ["py.typed"],
    },
    entry_points={
        "console_scripts": [
            "azcore=azcore.cli.__main__:main",
        ],
    },
    zip_safe=False,
    keywords="Multi-agent agents ai framework hierarchical azcore reinforcement-learning",
    project_urls={
        "Bug Reports": "https://github.com/Azrienlabs/Az-Core/issues",
        "Source": "https://github.com/Azrienlabs/Az-Core",
        "Documentation": "https://docs.azrienlabs.com/",
    },
)
