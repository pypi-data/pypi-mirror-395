"""
RiskX - End-to-End Automated Risk Scoring Platform
==================================================

Setup configuration for PyPI distribution
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="riskx",
    version="0.1.1",
    author="Idriss Bado",
    author_email="idrissbadoolivier@gmail.com",
    description="End-to-End Automated Risk Scoring Platform for Credit, Fraud, and Churn Prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrissbado/RiskX",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
    ],
    extras_require={
        "full": [
            "xgboost>=1.5.0",
            "lightgbm>=3.3.0",
            "optuna>=2.10.0",
            "shap>=0.40.0",
            "sqlalchemy>=1.4.0",
            "requests>=2.26.0",
            "pyarrow>=6.0.0",
        ],
        "ml": [
            "xgboost>=1.5.0",
            "lightgbm>=3.3.0",
            "optuna>=2.10.0",
        ],
        "data": [
            "sqlalchemy>=1.4.0",
            "requests>=2.26.0",
            "pyarrow>=6.0.0",
            "openpyxl>=3.0.0",
        ],
        "explain": [
            "shap>=0.40.0",
        ],
        "azure": [
            "azure-ai-ml>=1.0.0",
            "azure-identity>=1.10.0",
        ],
        "aws": [
            "boto3>=1.20.0",
        ],
        "gcp": [
            "google-cloud-run>=0.5.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "riskx=riskx.cli.main:main",
        ],
    },
    keywords="risk-scoring credit-scoring fraud-detection ml automl risk-management financial-risk",
    project_urls={
        "Documentation": "https://github.com/idrissbado/RiskX/blob/main/README.md",
        "Source": "https://github.com/idrissbado/RiskX",
        "Tracker": "https://github.com/idrissbado/RiskX/issues",
    },
)
