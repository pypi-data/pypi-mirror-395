from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="almufti-bin-badran",
    version="1.0.0",
    author="Almufti Development Team",
    author_email="dev@almufti.ai",
    description="A lightweight AI assistant with Arabic language support for mobile and offline use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/almufti-bin-badran",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "numpy>=1.23.0",
        "pandas>=1.5.0",
        "nltk>=3.8.1",
        "spacy>=3.5.0",
        "pyarabic>=0.6.15",
        "langdetect>=1.0.9",
        "sqlalchemy>=2.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "duckduckgo-search>=3.9.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pytest-cov>=4.1.0",
        ],
        "audio": [
            "librosa>=0.10.0",
            "soundfile>=0.12.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "almufti=almufti.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
