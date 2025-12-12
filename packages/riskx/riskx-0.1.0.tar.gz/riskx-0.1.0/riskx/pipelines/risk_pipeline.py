"""
RiskX Pipeline - End-to-End Orchestration
========================================

Complete workflow orchestration from data loading to scoring.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import warnings

from riskx.core.data_connector import RiskDataConnector
from riskx.core.data_cleaner import RiskCleaner
from riskx.core.feature_engineering import RiskFeatureEngine
from riskx.core.model_auto import RiskAutoModel
from riskx.core.scoring_engine import ScoringEngine
from riskx.core.monitoring import RiskMonitor
from riskx.core.explainability import RiskExplain


class RiskPipeline:
    """
    Complete end-to-end risk scoring pipeline
    
    Workflow:
    1. Load data
    2. Clean and validate
    3. Engineer features
    4. Train models
    5. Score and interpret
    6. Monitor performance
    """
    
    def __init__(self, pipeline_name: str = "risk_pipeline"):
        self.pipeline_name = pipeline_name
        self.connector = RiskDataConnector()
        self.cleaner = RiskCleaner()
        self.feature_engine = RiskFeatureEngine()
        self.model = RiskAutoModel()
        self.scorer = None
        self.monitor = RiskMonitor()
        self.explainer = None
        
        self.data_raw = None
        self.data_clean = None
        self.data_features = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        
        self.pipeline_config = {}
        self.execution_log = []
    
    def load_data(self, source: str, **kwargs) -> pd.DataFrame:
        """
        Load data from source
        
        Args:
            source: Source type ('csv', 'excel', 'sql', 'api', etc.)
            **kwargs: Source-specific parameters
        
        Returns:
            Loaded DataFrame
        """
        self._log_step("Loading data", f"Source: {source}")
        
        if source == 'csv':
            self.data_raw = self.connector.from_csv(**kwargs)
        elif source == 'excel':
            self.data_raw = self.connector.from_excel(**kwargs)
        elif source == 'sql':
            self.data_raw = self.connector.from_sql(**kwargs)
        elif source == 'api':
            self.data_raw = self.connector.from_api(**kwargs)
        elif source == 'json':
            self.data_raw = self.connector.from_json(**kwargs)
        elif source == 'parquet':
            self.data_raw = self.connector.from_parquet(**kwargs)
        elif source == 'datalake':
            self.data_raw = self.connector.from_datalake(**kwargs)
        elif source == 'dataframe':
            self.data_raw = self.connector.from_dataframe(**kwargs)
        else:
            raise ValueError(f"Unknown source: {source}")
        
        self._log_step("Data loaded", f"Shape: {self.data_raw.shape}")
        return self.data_raw
    
    def clean_data(self, target_column: str, auto: bool = True, **kwargs) -> pd.DataFrame:
        """
        Clean and preprocess data
        
        Args:
            target_column: Target variable name
            auto: Use automated cleaning pipeline
            **kwargs: Cleaning parameters
        
        Returns:
            Cleaned DataFrame
        """
        self._log_step("Cleaning data", f"Target: {target_column}")
        
        if auto:
            self.data_clean = self.cleaner.auto_clean(self.data_raw, target_column=target_column)
        else:
            self.data_clean = self.data_raw.copy()
            # Manual cleaning steps
            if kwargs.get('handle_missing'):
                self.data_clean = self.cleaner.clean_missing(self.data_clean, strategy=kwargs.get('missing_strategy', 'auto'))
            if kwargs.get('handle_outliers'):
                self.data_clean = self.cleaner.clean_outliers(self.data_clean, method=kwargs.get('outlier_method', 'iqr'))
            if kwargs.get('encode_categorical'):
                cat_cols = self.data_clean.select_dtypes(include=['object']).columns.tolist()
                if target_column in cat_cols:
                    cat_cols.remove(target_column)
                self.data_clean = self.cleaner.encode_categorical(self.data_clean, columns=cat_cols)
        
        self._log_step("Data cleaned", f"Shape: {self.data_clean.shape}")
        return self.data_clean
    
    def engineer_features(self, target: str, auto: bool = True, **kwargs) -> pd.DataFrame:
        """
        Engineer risk-specific features
        
        Args:
            target: Target variable name
            auto: Use automated feature engineering
            **kwargs: Feature engineering parameters
        
        Returns:
            DataFrame with engineered features
        """
        self._log_step("Engineering features", f"Target: {target}")
        
        if auto:
            self.data_features = self.feature_engine.auto_features(
                self.data_clean,
                target=target,
                include_woe=kwargs.get('include_woe', True),
                include_time=kwargs.get('include_time', True),
                include_ratios=kwargs.get('include_ratios', True)
            )
        else:
            self.data_features = self.data_clean.copy()
            # Manual feature engineering
            if kwargs.get('compute_woe'):
                for col in kwargs.get('woe_columns', []):
                    self.feature_engine.compute_woe_iv(self.data_features, col, target)
        
        self._log_step("Features engineered", f"Shape: {self.data_features.shape}")
        return self.data_features
    
    def split_data(self, target: str, test_size: float = 0.2, random_state: int = 42):
        """
        Split data into train and test sets
        
        Args:
            target: Target variable name
            test_size: Test set proportion
            random_state: Random seed
        """
        from sklearn.model_selection import train_test_split
        
        self._log_step("Splitting data", f"Test size: {test_size}")
        
        X = self.data_features.drop(target, axis=1)
        y = self.data_features[target]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        self._log_step("Data split", f"Train: {len(self.X_train)}, Test: {len(self.X_test)}")
    
    def train_models(self, algorithms: List[str] = ['logistic', 'rf', 'xgboost'], **kwargs) -> Dict:
        """
        Train and compare models
        
        Args:
            algorithms: List of algorithms to train
            **kwargs: Training parameters
        
        Returns:
            Training results
        """
        self._log_step("Training models", f"Algorithms: {algorithms}")
        
        results = self.model.train_auto(
            self.X_train,
            self.y_train,
            X_val=self.X_test,
            y_val=self.y_test,
            algorithms=algorithms,
            metric=kwargs.get('metric', 'auc')
        )
        
        # Calibrate best model if requested
        if kwargs.get('calibrate', True):
            self.model.calibrate_model(self.X_train, self.y_train, method='isotonic')
        
        self._log_step("Models trained", f"Best score: {self.model.best_score:.4f}")
        return results
    
    def setup_scoring(self, score_min: int = 300, score_max: int = 850):
        """
        Setup scoring engine
        
        Args:
            score_min: Minimum score
            score_max: Maximum score
        """
        self._log_step("Setting up scoring engine", f"Range: {score_min}-{score_max}")
        
        best_model = self.model.get_best_model()
        self.scorer = ScoringEngine(best_model, score_min=score_min, score_max=score_max)
        
        self._log_step("Scoring engine ready", "")
    
    def setup_monitoring(self, alert_threshold: float = 0.25):
        """
        Setup monitoring with baseline
        
        Args:
            alert_threshold: PSI/CSI alert threshold
        """
        self._log_step("Setting up monitoring", f"Alert threshold: {alert_threshold}")
        
        self.monitor = RiskMonitor(alert_threshold_psi=alert_threshold, alert_threshold_csi=alert_threshold)
        self.monitor.set_baseline(self.X_train)
        
        self._log_step("Monitoring ready", f"Baseline: {len(self.X_train)} records")
    
    def setup_explainability(self):
        """Setup explainability"""
        self._log_step("Setting up explainability", "")
        
        self.explainer = RiskExplain(self.model.get_best_model())
        self.explainer.feature_names = self.X_train.columns.tolist()
        
        self._log_step("Explainability ready", "")
    
    def score_new_data(self, data: Union[pd.DataFrame, Dict], batch: bool = True) -> Union[pd.DataFrame, Dict]:
        """
        Score new applications
        
        Args:
            data: New data to score (DataFrame for batch, Dict for single)
            batch: Batch mode (True) or single mode (False)
        
        Returns:
            Scores (DataFrame for batch, Dict for single)
        """
        if self.scorer is None:
            raise ValueError("Scoring engine not set up. Call setup_scoring() first.")
        
        if batch:
            self._log_step("Batch scoring", f"Records: {len(data)}")
            results = self.scorer.score_batch(data)
        else:
            self._log_step("Single scoring", "")
            results = self.scorer.score_single(data)
        
        return results
    
    def monitor_new_data(self, data: pd.DataFrame) -> Dict:
        """
        Monitor new data for drift
        
        Args:
            data: New data to monitor
        
        Returns:
            Monitoring report
        """
        self._log_step("Monitoring data", f"Records: {len(data)}")
        
        report = self.monitor.monitor_dataset(self.X_train, data)
        
        return report
    
    def explain_predictions(self, data: pd.DataFrame, n_samples: int = 100) -> Dict:
        """
        Generate explanations for predictions
        
        Args:
            data: Data to explain
            n_samples: Number of samples for SHAP background
        
        Returns:
            Explanations dictionary
        """
        if self.explainer is None:
            self.setup_explainability()
        
        self._log_step("Generating explanations", f"Samples: {min(n_samples, len(data))}")
        
        sample_data = data.sample(min(n_samples, len(data)), random_state=42)
        explanations = self.explainer.explain_with_shap(sample_data)
        
        return explanations
    
    def run_full_pipeline(self, source: str, target: str, 
                         algorithms: List[str] = ['logistic', 'rf', 'xgboost'],
                         **kwargs) -> Dict:
        """
        Run complete end-to-end pipeline
        
        Args:
            source: Data source type
            target: Target variable name
            algorithms: ML algorithms to train
            **kwargs: Pipeline parameters
        
        Returns:
            Pipeline results dictionary
        """
        print(f"\n{'='*60}")
        print(f"RiskX Pipeline: {self.pipeline_name}")
        print(f"{'='*60}\n")
        
        # 1. Load data
        self.load_data(source, **kwargs.get('load_params', {}))
        
        # 2. Clean data
        self.clean_data(target, auto=kwargs.get('auto_clean', True))
        
        # 3. Engineer features
        self.engineer_features(target, auto=kwargs.get('auto_features', True))
        
        # 4. Split data
        self.split_data(target, test_size=kwargs.get('test_size', 0.2))
        
        # 5. Train models
        results = self.train_models(algorithms, **kwargs.get('train_params', {}))
        
        # 6. Setup scoring
        self.setup_scoring(
            score_min=kwargs.get('score_min', 300),
            score_max=kwargs.get('score_max', 850)
        )
        
        # 7. Setup monitoring
        self.setup_monitoring(alert_threshold=kwargs.get('alert_threshold', 0.25))
        
        # 8. Evaluate on test set
        test_scores = self.scorer.score_batch(self.X_test)
        
        # 9. Track performance
        from sklearn.metrics import roc_auc_score
        test_auc = roc_auc_score(self.y_test, test_scores['probability'])
        
        print(f"\n{'='*60}")
        print(f"Pipeline Complete!")
        print(f"Test AUC: {test_auc:.4f}")
        print(f"{'='*60}\n")
        
        return {
            'model_results': results,
            'test_auc': test_auc,
            'test_scores': test_scores,
            'execution_log': self.execution_log
        }
    
    def save_pipeline(self, filepath: str):
        """
        Save complete pipeline
        
        Args:
            filepath: Save path
        """
        import joblib
        
        pipeline_data = {
            'name': self.pipeline_name,
            'model': self.model,
            'scorer': self.scorer,
            'feature_engine': self.feature_engine,
            'cleaner': self.cleaner,
            'monitor': self.monitor,
            'config': self.pipeline_config,
            'log': self.execution_log
        }
        
        joblib.dump(pipeline_data, filepath)
        print(f"✓ Pipeline saved to {filepath}")
    
    def load_pipeline(self, filepath: str):
        """
        Load saved pipeline
        
        Args:
            filepath: Load path
        """
        import joblib
        
        pipeline_data = joblib.load(filepath)
        
        self.pipeline_name = pipeline_data['name']
        self.model = pipeline_data['model']
        self.scorer = pipeline_data['scorer']
        self.feature_engine = pipeline_data.get('feature_engine')
        self.cleaner = pipeline_data.get('cleaner')
        self.monitor = pipeline_data.get('monitor')
        self.pipeline_config = pipeline_data.get('config', {})
        self.execution_log = pipeline_data.get('log', [])
        
        print(f"✓ Pipeline loaded from {filepath}")
    
    def _log_step(self, step: str, details: str = ""):
        """Log pipeline step"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step,
            'details': details
        }
        self.execution_log.append(log_entry)
        print(f"[{step}] {details}")
    
    def get_execution_summary(self) -> pd.DataFrame:
        """Get pipeline execution summary"""
        return pd.DataFrame(self.execution_log)
