from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="autodatamind",
    version="0.1.0",
    author="Idriss Olivier Bado",
    author_email="idrissbadoolivier@gmail.com",
    description="Zero-code automated data analysis, machine learning, and deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/autodatamind",
    project_urls={
        "Bug Tracker": "https://github.com/idrissbado/autodatamind/issues",
        "Documentation": "https://github.com/idrissbado/autodatamind#readme",
        "Source Code": "https://github.com/idrissbado/autodatamind",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords=[
        "automated-ml",
        "automl",
        "deep-learning",
        "machine-learning",
        "data-analysis",
        "zero-code",
        "data-science",
        "artificial-intelligence",
        "neural-networks",
        "pandas-automation",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
