"""
RiskX - End-to-End Automated Risk Scoring Platform
===================================================

A comprehensive Python package for automated risk scoring, from data ingestion
to cloud deployment. Handles credit scoring, fraud detection, churn prediction,
and underwriting automation.

Author: Idriss Bado
Email: idrissbadoolivier@gmail.com
Version: 0.1.0
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

__version__ = "0.1.0"
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
    "RiskEvaluator"
]
