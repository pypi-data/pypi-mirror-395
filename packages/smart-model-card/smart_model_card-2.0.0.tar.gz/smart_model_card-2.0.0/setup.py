from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="smart-model-card",
    version="1.0.2",
    author="Ankur Lohachab",
    author_email="ankur.lohachab@maastrichtuniversity.nl",
    description="Standardized AI/ML model cards with OMOP CDM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-model-card",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/smart-model-card/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "omop": [
            "smart-omop>=0.1.0",
            "matplotlib>=3.3.0",
        ],
        "viz": ["matplotlib>=3.3.0"],
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
        "all": [
            "smart-omop>=0.1.0",
            "matplotlib>=3.3.0",
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "smart-model-card=smart_model_card.cli:main",
        ],
    },
)
