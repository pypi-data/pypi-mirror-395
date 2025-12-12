"""
RiskX - End-to-End Automated Risk Scoring Platform
===================================================

A comprehensive Python package for automated risk scoring, from data ingestion
to cloud deployment. Handles credit scoring, fraud detection, churn prediction,
and underwriting automation.

Author: Idriss Bado
Email: idrissbadoolivier@gmail.com
Version: 0.1.1
License: MIT
"""

from .core.data_connector import RiskDataConnector
from .core.data_cleaner import RiskCleaner
from .core.feature_engineering import RiskFeatureEngine
from .core.model_auto import RiskAutoModel
from .core.scoring_engine import ScoringEngine
from .core.monitoring import RiskMonitor
from .core.explainability import RiskExplain
from .pipelines.risk_pipeline import RiskPipeline
from .metrics.evaluation import RiskEvaluator

# CLI (optional)
try:
    from .cli.main import main as cli_main
except ImportError:
    cli_main = None

# Deployment (optional - requires cloud SDKs)
try:
    from .deployment import AzureMLDeployer, AWSLambdaDeployer, GCPCloudRunDeployer
except ImportError:
    AzureMLDeployer = AWSLambdaDeployer = GCPCloudRunDeployer = None

__version__ = "0.1.1"
__author__ = "Idriss Bado"
__email__ = "idrissbadoolivier@gmail.com"

__all__ = [
    "RiskDataConnector",
    "RiskCleaner",
    "RiskFeatureEngine",
    "RiskAutoModel",
    "ScoringEngine",
    "RiskMonitor",
    "RiskExplain",
    "RiskPipeline",
    "RiskEvaluator",
    "cli_main",
    "AzureMLDeployer",
    "AWSLambdaDeployer",
    "GCPCloudRunDeployer"
]
