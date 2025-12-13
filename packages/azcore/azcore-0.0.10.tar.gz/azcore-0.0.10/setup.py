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

requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    try:
        with open(requirements_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "==" in line:
                    line = line.replace("==", ">=")
                requirements.append(line)
    except (UnicodeDecodeError, UnicodeError, IOError) as e:
        print(f"Warning: Could not read requirements.txt: {e}")
        requirements = []

setup(
    name="azcore",
    version="0.0.10",
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
