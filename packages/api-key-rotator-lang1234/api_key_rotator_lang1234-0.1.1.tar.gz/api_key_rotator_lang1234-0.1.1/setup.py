"""Setup configuration for api-key-rotator package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="api-key-rotator-lang1234",
    version="0.1.1",
    author="xLang1234",
    description="A Python library for rotating API keys with automatic expiration handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xLang1234/api-key-rotator",
    project_urls={
        "Bug Tracker": "https://github.com/xLang1234/api-key-rotator/issues",
        "Documentation": "https://github.com/xLang1234/api-key-rotator#readme",
        "Source Code": "https://github.com/xLang1234/api-key-rotator",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
    },
    keywords="api, key, rotation, rate-limit, api-key, key-management, thread-safe",
    license="MIT",
    zip_safe=False,
)
