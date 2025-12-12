"""
RiskX Explainability - Model Interpretability and Explanations
=============================================================

SHAP, LIME, feature importance, and reason code generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
import warnings


class RiskExplain:
    """
    Model explainability and interpretability
    
    Features:
    - SHAP values
    - LIME explanations
    - Feature importance
    - Global and local explanations
    - Reason code generation
    """
    
    def __init__(self, model: Any = None):
        self.model = model
        self.explainer = None
        self.feature_names = None
        self.shap_values_cache = None
    
    def explain_with_shap(self, X: pd.DataFrame, 
                         background_data: Optional[pd.DataFrame] = None,
                         n_samples: int = 100) -> Dict:
        """
        Generate SHAP explanations
        
        Args:
            X: Data to explain
            background_data: Background dataset for SHAP (optional)
            n_samples: Number of background samples
        
        Returns:
            Dictionary with SHAP values and summary
        """
        try:
            import shap
        except ImportError:
            raise ImportError("SHAP not installed. Install with: pip install shap")
        
        if self.model is None:
            raise ValueError("No model provided")
        
        self.feature_names = X.columns.tolist()
        
        # Create explainer
        if background_data is None:
            background_data = X.sample(min(n_samples, len(X)), random_state=42)
        
        try:
            # Try TreeExplainer for tree-based models
            self.explainer = shap.TreeExplainer(self.model)
            shap_values = self.explainer.shap_values(X)
        except:
            # Fall back to KernelExplainer
            if hasattr(self.model, 'predict_proba'):
                predict_fn = lambda x: self.model.predict_proba(x)[:, 1]
            else:
                predict_fn = self.model.predict
            
            self.explainer = shap.KernelExplainer(predict_fn, background_data)
            shap_values = self.explainer.shap_values(X)
        
        # Handle multi-output
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Take positive class
        
        self.shap_values_cache = shap_values
        
        # Calculate feature importance
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        feature_importance = dict(zip(self.feature_names, mean_abs_shap))
        sorted_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
        
        print(f"✓ SHAP values computed for {len(X)} samples")
        print(f"✓ Top 3 features: {list(sorted_importance.keys())[:3]}")
        
        return {
            'shap_values': shap_values,
            'feature_importance': sorted_importance,
            'base_value': self.explainer.expected_value if hasattr(self.explainer, 'expected_value') else None,
            'feature_names': self.feature_names
        }
    
    def explain_single_prediction(self, X_single: pd.DataFrame, 
                                  method: str = 'shap',
                                  n_features: int = 5) -> Dict:
        """
        Explain a single prediction
        
        Args:
            X_single: Single sample (1 row DataFrame)
            method: Explanation method ('shap' or 'lime')
            n_features: Number of top features to return
        
        Returns:
            Explanation dictionary
        """
        if method == 'shap':
            return self._explain_single_shap(X_single, n_features)
        elif method == 'lime':
            return self._explain_single_lime(X_single, n_features)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _explain_single_shap(self, X_single: pd.DataFrame, n_features: int) -> Dict:
        """Explain single prediction with SHAP"""
        try:
            import shap
        except ImportError:
            raise ImportError("SHAP not installed")
        
        if self.explainer is None:
            # Create explainer with single sample as background
            if hasattr(self.model, 'predict_proba'):
                predict_fn = lambda x: self.model.predict_proba(x)[:, 1]
            else:
                predict_fn = self.model.predict
            
            self.explainer = shap.KernelExplainer(predict_fn, X_single)
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(X_single)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Get prediction
        if hasattr(self.model, 'predict_proba'):
            prediction = self.model.predict_proba(X_single)[0, 1]
        else:
            prediction = self.model.predict(X_single)[0]
        
        # Top contributing features
        feature_contributions = dict(zip(X_single.columns, shap_values[0]))
        sorted_contrib = dict(sorted(feature_contributions.items(), key=lambda x: abs(x[1]), reverse=True))
        top_features = list(sorted_contrib.items())[:n_features]
        
        explanation = {
            'prediction': float(prediction),
            'base_value': self.explainer.expected_value if hasattr(self.explainer, 'expected_value') else 0.5,
            'shap_values': dict(sorted_contrib),
            'top_features': [
                {
                    'feature': feature,
                    'value': float(X_single[feature].iloc[0]),
                    'contribution': float(contrib),
                    'direction': 'increases' if contrib > 0 else 'decreases'
                }
                for feature, contrib in top_features
            ]
        }
        
        print(f"✓ Single prediction explained: pred={prediction:.4f}")
        return explanation
    
    def _explain_single_lime(self, X_single: pd.DataFrame, n_features: int) -> Dict:
        """Explain single prediction with LIME"""
        try:
            from lime.lime_tabular import LimeTabularExplainer
        except ImportError:
            raise ImportError("LIME not installed. Install with: pip install lime")
        
        # Create LIME explainer
        explainer = LimeTabularExplainer(
            X_single.values,
            feature_names=X_single.columns.tolist(),
            mode='classification' if hasattr(self.model, 'predict_proba') else 'regression'
        )
        
        # Get prediction
        if hasattr(self.model, 'predict_proba'):
            predict_fn = lambda x: self.model.predict_proba(pd.DataFrame(x, columns=X_single.columns))
            prediction = predict_fn(X_single.values)[0, 1]
        else:
            predict_fn = lambda x: self.model.predict(pd.DataFrame(x, columns=X_single.columns))
            prediction = predict_fn(X_single.values)[0]
        
        # Explain
        exp = explainer.explain_instance(
            X_single.values[0],
            predict_fn,
            num_features=n_features
        )
        
        # Extract explanation
        top_features = [
            {
                'feature': feature,
                'value': float(X_single[feature].iloc[0]),
                'weight': float(weight),
                'direction': 'increases' if weight > 0 else 'decreases'
            }
            for feature, weight in exp.as_list()
        ]
        
        explanation = {
            'prediction': float(prediction),
            'lime_explanation': exp.as_list(),
            'top_features': top_features
        }
        
        print(f"✓ LIME explanation generated: pred={prediction:.4f}")
        return explanation
    
    def global_feature_importance(self, X: pd.DataFrame, method: str = 'shap') -> pd.DataFrame:
        """
        Calculate global feature importance
        
        Args:
            X: Dataset
            method: Method ('shap', 'permutation', or 'model')
        
        Returns:
            DataFrame with feature importance
        """
        if method == 'shap':
            return self._global_importance_shap(X)
        elif method == 'permutation':
            return self._global_importance_permutation(X)
        elif method == 'model':
            return self._global_importance_model()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _global_importance_shap(self, X: pd.DataFrame) -> pd.DataFrame:
        """Global importance from SHAP"""
        if self.shap_values_cache is None:
            self.explain_with_shap(X)
        
        mean_abs_shap = np.abs(self.shap_values_cache).mean(axis=0)
        
        df_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': mean_abs_shap
        }).sort_values('importance', ascending=False)
        
        # Normalize to 0-1
        df_importance['importance_normalized'] = df_importance['importance'] / df_importance['importance'].sum()
        
        print(f"✓ Global feature importance calculated (SHAP)")
        return df_importance
    
    def _global_importance_permutation(self, X: pd.DataFrame) -> pd.DataFrame:
        """Global importance from permutation"""
        from sklearn.inspection import permutation_importance
        
        # Need y for permutation importance (not implemented in simple version)
        raise NotImplementedError("Permutation importance requires labels")
    
    def _global_importance_model(self) -> pd.DataFrame:
        """Global importance from model's built-in feature_importances_"""
        if not hasattr(self.model, 'feature_importances_'):
            raise ValueError("Model does not have feature_importances_ attribute")
        
        df_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Normalize
        df_importance['importance_normalized'] = df_importance['importance'] / df_importance['importance'].sum()
        
        print(f"✓ Global feature importance from model")
        return df_importance
    
    def generate_reason_codes(self, X_single: pd.DataFrame, 
                             prediction: float,
                             n_codes: int = 4) -> List[Dict]:
        """
        Generate interpretable reason codes
        
        Args:
            X_single: Single sample
            prediction: Model prediction
            n_codes: Number of reason codes
        
        Returns:
            List of reason code dictionaries
        """
        # Get explanation
        explanation = self.explain_single_prediction(X_single, method='shap', n_features=n_codes)
        
        # Convert to reason codes
        reason_codes = []
        
        for i, feature_info in enumerate(explanation['top_features']):
            feature = feature_info['feature']
            value = feature_info['value']
            contribution = feature_info['contribution']
            direction = feature_info['direction']
            
            # Generate human-readable description
            if contribution > 0:
                impact = "increases risk"
            else:
                impact = "decreases risk"
            
            reason_codes.append({
                'code': f'RC{i+1}',
                'feature': feature,
                'value': value,
                'contribution': abs(contribution),
                'direction': direction,
                'description': f'{feature.replace("_", " ").title()} ({value:.2f}) {impact}',
                'rank': i + 1
            })
        
        print(f"✓ Generated {len(reason_codes)} reason codes")
        return reason_codes
    
    def create_decision_tree_surrogate(self, X: pd.DataFrame, max_depth: int = 5) -> Any:
        """
        Create interpretable decision tree surrogate model
        
        Args:
            X: Training data
            max_depth: Maximum tree depth
        
        Returns:
            Fitted decision tree
        """
        from sklearn.tree import DecisionTreeClassifier
        
        # Get predictions from complex model
        if hasattr(self.model, 'predict_proba'):
            y_pred = (self.model.predict_proba(X)[:, 1] > 0.5).astype(int)
        else:
            y_pred = self.model.predict(X)
        
        # Train decision tree
        tree = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
        tree.fit(X, y_pred)
        
        # Calculate fidelity
        fidelity = (tree.predict(X) == y_pred).mean()
        
        print(f"✓ Decision tree surrogate created (fidelity={fidelity:.4f})")
        return tree
    
    def plot_feature_importance(self, X: pd.DataFrame, top_n: int = 10, save_path: Optional[str] = None):
        """
        Plot feature importance (requires matplotlib)
        
        Args:
            X: Dataset
            top_n: Number of top features to plot
            save_path: Path to save plot (optional)
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
            return
        
        # Get importance
        df_importance = self.global_feature_importance(X, method='shap')
        df_top = df_importance.head(top_n)
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.barh(df_top['feature'], df_top['importance_normalized'])
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Feature Importance')
        plt.gca().invert_yaxis()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            print(f"✓ Plot saved to {save_path}")
        else:
            plt.show()
    
    def export_explanations(self, explanations: List[Dict], filepath: str):
        """
        Export explanations to JSON
        
        Args:
            explanations: List of explanation dictionaries
            filepath: Output file path
        """
        import json
        
        with open(filepath, 'w') as f:
            json.dump(explanations, f, indent=2)
        
        print(f"✓ Exported {len(explanations)} explanations to {filepath}")
