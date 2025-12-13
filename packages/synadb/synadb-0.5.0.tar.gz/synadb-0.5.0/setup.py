"""Setup script for SynaDB Python wrapper."""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="synadb",
    version="0.5.0",
    description="AI-native embedded database for ML/AI applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Golvis Tavarez",
    author_email="golvis@eyelid.ai",
    url="https://github.com/gtava5813/SynaDB",
    project_urls={
        "Homepage": "https://github.com/gtava5813/SynaDB",
        "Documentation": "https://github.com/gtava5813/SynaDB/wiki",
        "Repository": "https://github.com/gtava5813/SynaDB",
        "Issues": "https://github.com/gtava5813/SynaDB/issues",
    },
    packages=find_packages(),
    package_data={"synadb": ["*.so", "*.dylib", "*.dll"]},
    python_requires=">=3.8",
    install_requires=["numpy>=1.21.0"],
    extras_require={
        "ml": ["torch>=2.0.0", "datasets>=2.14.0", "transformers>=4.30.0"],
        "pandas": ["pandas>=1.3.0"],
        "dev": ["pytest>=7.0.0", "hypothesis>=6.0.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="database embedded ai ml machine-learning vector-database embeddings rag llm",
)
