from setuptools import find_packages, setup

setup(
    name="earnings_call_tone_research",
    version="0.1.0",
    description="Analyze the tone of company earnings calls",
    author="Kurry Tran",
    packages=find_packages(include=["src", "src.*", "research", "research.*"]),
    package_dir={"": "."},
    python_requires=">=3.8",
    install_requires=[
        # Core data analysis
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        # NLP and ML
        "nltk>=3.8.0",
        "scikit-learn>=1.3.0",
        # API Integration
        "requests>=2.30.0",
        # File formats
        "pyarrow",
        # Utilities
        "tqdm",
        "pyyaml",
    ],
    extras_require={
        "dev": [
            "black>=23.9.1",
            "pylint>=2.17.5",
            "mypy>=1.5.1",
            "ruff>=0.0.290",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
)
