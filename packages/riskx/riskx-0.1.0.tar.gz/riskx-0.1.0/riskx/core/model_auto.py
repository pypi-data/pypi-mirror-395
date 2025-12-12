"""
RiskX Auto ML - Automated Model Training and Tuning
==================================================

Automated machine learning for risk scoring models with:
- Multiple algorithm support
- Hyperparameter tuning
- Model calibration
- Ensemble methods
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import warnings


class RiskAutoModel:
    """
    Automated ML for risk scoring
    
    Features:
    - AutoML with multiple algorithms
    - Hyperparameter optimization
    - Model calibration
    - Ensemble learning
    - Model persistence
    """
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_score = -np.inf
        self.feature_importance = {}
        self.calibrators = {}
    
    def train_auto(self, X_train: pd.DataFrame, y_train: pd.Series,
                   X_val: Optional[pd.DataFrame] = None,
                   y_val: Optional[pd.Series] = None,
                   algorithms: List[str] = ['logistic', 'rf', 'xgboost', 'lightgbm'],
                   metric: str = 'auc') -> Dict[str, Any]:
        """
        Automated training with multiple algorithms
        
        Args:
            X_train: Training features
            y_train: Training target
            X_val: Validation features
            y_val: Validation target
            algorithms: List of algorithms to try
            metric: Evaluation metric
        
        Returns:
            Training results dictionary
        """
        print(f"Training {len(algorithms)} models...")
        
        results = {}
        
        for algo in algorithms:
            print(f"Training {algo}...")
            
            try:
                if algo == 'logistic':
                    results[algo] = self._train_logistic(X_train, y_train, X_val, y_val)
                
                elif algo == 'rf':
                    results[algo] = self._train_random_forest(X_train, y_train, X_val, y_val)
                
                elif algo == 'xgboost':
                    results[algo] = self._train_xgboost(X_train, y_train, X_val, y_val)
                
                elif algo == 'lightgbm':
                    results[algo] = self._train_lightgbm(X_train, y_train, X_val, y_val)
                
                # Update best model
                score = results[algo]['val_score'] if X_val is not None else results[algo]['train_score']
                if score > self.best_score:
                    self.best_score = score
                    self.best_model = results[algo]['model']
                    print(f"✓ New best model: {algo} ({metric}={score:.4f})")
            
            except Exception as e:
                print(f"✗ Failed to train {algo}: {e}")
                continue
        
        return results
    
    def _train_logistic(self, X_train, y_train, X_val, y_val) -> Dict:
        """Train Logistic Regression"""
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import roc_auc_score
            
            model = LogisticRegression(max_iter=1000, random_state=42)
            model.fit(X_train, y_train)
            
            train_pred = model.predict_proba(X_train)[:, 1]
            train_score = roc_auc_score(y_train, train_pred)
            
            val_score = None
            if X_val is not None:
                val_pred = model.predict_proba(X_val)[:, 1]
                val_score = roc_auc_score(y_val, val_pred)
            
            self.models['logistic'] = model
            
            return {
                'model': model,
                'train_score': train_score,
                'val_score': val_score,
                'algorithm': 'logistic'
            }
        except ImportError:
            raise ImportError("scikit-learn required for Logistic Regression")
    
    def _train_random_forest(self, X_train, y_train, X_val, y_val) -> Dict:
        """Train Random Forest"""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.metrics import roc_auc_score
            
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=20,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train)
            
            train_pred = model.predict_proba(X_train)[:, 1]
            train_score = roc_auc_score(y_train, train_pred)
            
            val_score = None
            if X_val is not None:
                val_pred = model.predict_proba(X_val)[:, 1]
                val_score = roc_auc_score(y_val, val_pred)
            
            # Feature importance
            self.feature_importance['rf'] = dict(zip(X_train.columns, model.feature_importances_))
            self.models['rf'] = model
            
            return {
                'model': model,
                'train_score': train_score,
                'val_score': val_score,
                'feature_importance': self.feature_importance['rf'],
                'algorithm': 'random_forest'
            }
        except ImportError:
            raise ImportError("scikit-learn required for Random Forest")
    
    def _train_xgboost(self, X_train, y_train, X_val, y_val) -> Dict:
        """Train XGBoost"""
        try:
            import xgboost as xgb
            from sklearn.metrics import roc_auc_score
            
            model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            
            eval_set = [(X_val, y_val)] if X_val is not None else None
            model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
            
            train_pred = model.predict_proba(X_train)[:, 1]
            train_score = roc_auc_score(y_train, train_pred)
            
            val_score = None
            if X_val is not None:
                val_pred = model.predict_proba(X_val)[:, 1]
                val_score = roc_auc_score(y_val, val_pred)
            
            # Feature importance
            self.feature_importance['xgboost'] = dict(zip(X_train.columns, model.feature_importances_))
            self.models['xgboost'] = model
            
            return {
                'model': model,
                'train_score': train_score,
                'val_score': val_score,
                'feature_importance': self.feature_importance['xgboost'],
                'algorithm': 'xgboost'
            }
        except ImportError:
            warnings.warn("xgboost not installed, skipping")
            return None
    
    def _train_lightgbm(self, X_train, y_train, X_val, y_val) -> Dict:
        """Train LightGBM"""
        try:
            import lightgbm as lgb
            from sklearn.metrics import roc_auc_score
            
            model = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                num_leaves=31,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                verbose=-1
            )
            
            eval_set = [(X_val, y_val)] if X_val is not None else None
            model.fit(X_train, y_train, eval_set=eval_set)
            
            train_pred = model.predict_proba(X_train)[:, 1]
            train_score = roc_auc_score(y_train, train_pred)
            
            val_score = None
            if X_val is not None:
                val_pred = model.predict_proba(X_val)[:, 1]
                val_score = roc_auc_score(y_val, val_pred)
            
            # Feature importance
            self.feature_importance['lightgbm'] = dict(zip(X_train.columns, model.feature_importances_))
            self.models['lightgbm'] = model
            
            return {
                'model': model,
                'train_score': train_score,
                'val_score': val_score,
                'feature_importance': self.feature_importance['lightgbm'],
                'algorithm': 'lightgbm'
            }
        except ImportError:
            warnings.warn("lightgbm not installed, skipping")
            return None
    
    def calibrate_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                       method: str = 'isotonic') -> Any:
        """
        Calibrate model probabilities
        
        Args:
            X_train: Training features
            y_train: Training target
            method: Calibration method ('isotonic' or 'sigmoid')
        
        Returns:
            Calibrated model
        """
        if self.best_model is None:
            raise ValueError("No trained model available. Train a model first.")
        
        try:
            from sklearn.calibration import CalibratedClassifierCV
            
            calibrated_model = CalibratedClassifierCV(
                self.best_model,
                method=method,
                cv='prefit'
            )
            calibrated_model.fit(X_train, y_train)
            
            self.calibrators['best'] = calibrated_model
            print(f"✓ Model calibrated using {method} method")
            
            return calibrated_model
        
        except ImportError:
            raise ImportError("scikit-learn required for calibration")
    
    def create_ensemble(self, X_train: pd.DataFrame, y_train: pd.Series,
                       method: str = 'voting') -> Any:
        """
        Create ensemble from trained models
        
        Args:
            X_train: Training features
            y_train: Training target
            method: Ensemble method ('voting' or 'stacking')
        
        Returns:
            Ensemble model
        """
        if len(self.models) < 2:
            raise ValueError("Need at least 2 trained models for ensemble")
        
        try:
            from sklearn.ensemble import VotingClassifier, StackingClassifier
            from sklearn.linear_model import LogisticRegression
            
            estimators = [(name, model) for name, model in self.models.items()]
            
            if method == 'voting':
                ensemble = VotingClassifier(
                    estimators=estimators,
                    voting='soft',
                    n_jobs=-1
                )
            
            elif method == 'stacking':
                ensemble = StackingClassifier(
                    estimators=estimators,
                    final_estimator=LogisticRegression(),
                    cv=5,
                    n_jobs=-1
                )
            
            ensemble.fit(X_train, y_train)
            self.models['ensemble'] = ensemble
            
            print(f"✓ Created {method} ensemble from {len(estimators)} models")
            return ensemble
        
        except ImportError:
            raise ImportError("scikit-learn required for ensemble methods")
    
    def optimize_hyperparameters(self, X_train: pd.DataFrame, y_train: pd.Series,
                                algorithm: str = 'xgboost',
                                n_trials: int = 50) -> Dict:
        """
        Hyperparameter optimization using Optuna
        
        Args:
            X_train: Training features
            y_train: Training target
            algorithm: Algorithm to optimize
            n_trials: Number of optimization trials
        
        Returns:
            Best parameters dictionary
        """
        try:
            import optuna
            from sklearn.model_selection import cross_val_score
            
            def objective(trial):
                if algorithm == 'xgboost':
                    import xgboost as xgb
                    
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 50, 200),
                        'max_depth': trial.suggest_int('max_depth', 3, 10),
                        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                        'random_state': 42
                    }
                    
                    model = xgb.XGBClassifier(**params)
                
                elif algorithm == 'lightgbm':
                    import lightgbm as lgb
                    
                    params = {
                        'n_estimators': trial.suggest_int('n_estimators', 50, 200),
                        'max_depth': trial.suggest_int('max_depth', 3, 10),
                        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                        'num_leaves': trial.suggest_int('num_leaves', 20, 50),
                        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
                        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
                        'random_state': 42
                    }
                    
                    model = lgb.LGBMClassifier(**params, verbose=-1)
                
                else:
                    raise ValueError(f"Unsupported algorithm: {algorithm}")
                
                # Cross-validation score
                scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
                return scores.mean()
            
            study = optuna.create_study(direction='maximize')
            study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
            
            print(f"✓ Best AUC: {study.best_value:.4f}")
            print(f"✓ Best params: {study.best_params}")
            
            return study.best_params
        
        except ImportError:
            raise ImportError("optuna required for hyperparameter optimization")
    
    def get_best_model(self) -> Any:
        """Get best trained model"""
        return self.best_model
    
    def predict_proba(self, X: pd.DataFrame, use_calibrated: bool = False) -> np.ndarray:
        """
        Predict probabilities
        
        Args:
            X: Features
            use_calibrated: Use calibrated model if available
        
        Returns:
            Predicted probabilities
        """
        if use_calibrated and 'best' in self.calibrators:
            return self.calibrators['best'].predict_proba(X)[:, 1]
        elif self.best_model is not None:
            return self.best_model.predict_proba(X)[:, 1]
        else:
            raise ValueError("No trained model available")
    
    def save_model(self, path: str, model_name: str = 'best'):
        """
        Save model to disk
        
        Args:
            path: Save path
            model_name: Model to save ('best', 'ensemble', or specific algorithm)
        """
        import joblib
        
        if model_name == 'best':
            model = self.best_model
        elif model_name in self.models:
            model = self.models[model_name]
        else:
            raise ValueError(f"Model {model_name} not found")
        
        joblib.dump(model, path)
        print(f"✓ Model saved to {path}")
    
    def load_model(self, path: str):
        """Load model from disk"""
        import joblib
        
        model = joblib.load(path)
        self.best_model = model
        print(f"✓ Model loaded from {path}")
        return model
