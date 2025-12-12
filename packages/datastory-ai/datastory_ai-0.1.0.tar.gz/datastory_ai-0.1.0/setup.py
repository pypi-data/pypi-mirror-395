"""
Setup configuration for DataStory package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="datastory-ai",
    version="0.1.0",
    author="Idriss Bado",
    author_email="your.email@example.com",
    description="Automatic Storytelling from Data - Turn raw data into compelling business narratives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/DataStory",
    project_urls={
        "Bug Tracker": "https://github.com/idrissbado/DataStory/issues",
        "Documentation": "https://github.com/idrissbado/DataStory#readme",
        "Source Code": "https://github.com/idrissbado/DataStory",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business",
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
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "full": [
            "matplotlib>=3.4.0",
            "openpyxl>=3.0.0",
            "reportlab>=3.6.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    keywords="data analysis, business intelligence, narrative, storytelling, automated reports, data science",
    entry_points={
        "console_scripts": [
            "datastory=datastory.__main__:main",
        ],
    },
)
