"""
RiskX Monitoring - Model Performance and Data Drift Detection
============================================================

PSI, CSI, model performance tracking, and drift alerts.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import warnings
from datetime import datetime


class RiskMonitor:
    """
    Model monitoring and drift detection
    
    Features:
    - PSI (Population Stability Index)
    - CSI (Characteristic Stability Index)
    - Model performance tracking
    - Data drift detection
    - Alert system
    """
    
    def __init__(self, alert_threshold_psi: float = 0.25, alert_threshold_csi: float = 0.25):
        self.alert_threshold_psi = alert_threshold_psi
        self.alert_threshold_csi = alert_threshold_csi
        self.baseline_distributions = {}
        self.monitoring_history = []
    
    def calculate_psi(self, baseline: pd.Series, current: pd.Series, n_bins: int = 10) -> Dict:
        """
        Calculate Population Stability Index (PSI)
        
        PSI measures distribution shift between baseline and current data.
        
        PSI Interpretation:
        - PSI < 0.1: No significant change
        - 0.1 <= PSI < 0.25: Moderate change
        - PSI >= 0.25: Significant change (action needed)
        
        Args:
            baseline: Baseline distribution
            current: Current distribution
            n_bins: Number of bins
        
        Returns:
            Dictionary with PSI score and details
        """
        # Remove NaNs
        baseline_clean = baseline.dropna()
        current_clean = current.dropna()
        
        # Create bins from baseline
        try:
            _, bin_edges = pd.qcut(baseline_clean, q=n_bins, duplicates='drop', retbins=True)
        except:
            # Fall back to uniform bins if quantile fails
            bin_edges = np.linspace(baseline_clean.min(), baseline_clean.max(), n_bins + 1)
        
        # Bin both distributions
        baseline_binned = pd.cut(baseline_clean, bins=bin_edges, include_lowest=True)
        current_binned = pd.cut(current_clean, bins=bin_edges, include_lowest=True)
        
        # Calculate proportions
        baseline_dist = baseline_binned.value_counts(normalize=True).sort_index()
        current_dist = current_binned.value_counts(normalize=True).sort_index()
        
        # Align distributions
        all_bins = baseline_dist.index.union(current_dist.index)
        baseline_dist = baseline_dist.reindex(all_bins, fill_value=0.0001)
        current_dist = current_dist.reindex(all_bins, fill_value=0.0001)
        
        # Calculate PSI
        psi_values = (current_dist - baseline_dist) * np.log(current_dist / baseline_dist)
        psi = psi_values.sum()
        
        # Interpretation
        if psi < 0.1:
            interpretation = "No significant change"
            action = "No action needed"
        elif psi < 0.25:
            interpretation = "Moderate change"
            action = "Monitor closely"
        else:
            interpretation = "Significant change"
            action = "Investigate and consider retraining"
        
        return {
            'psi': float(psi),
            'interpretation': interpretation,
            'action': action,
            'bin_contributions': dict(zip([str(b) for b in all_bins], psi_values.values)),
            'baseline_mean': float(baseline_clean.mean()),
            'current_mean': float(current_clean.mean()),
            'baseline_std': float(baseline_clean.std()),
            'current_std': float(current_clean.std())
        }
    
    def calculate_csi(self, baseline: pd.Series, current: pd.Series, n_bins: int = 10) -> Dict:
        """
        Calculate Characteristic Stability Index (CSI)
        
        Similar to PSI but for categorical features.
        
        Args:
            baseline: Baseline distribution
            current: Current distribution
            n_bins: Number of bins (for numeric features)
        
        Returns:
            Dictionary with CSI score and details
        """
        # Check if categorical or numeric
        if pd.api.types.is_numeric_dtype(baseline):
            # Use PSI for numeric features
            return self.calculate_psi(baseline, current, n_bins)
        
        # For categorical features
        baseline_clean = baseline.dropna()
        current_clean = current.dropna()
        
        # Calculate proportions
        baseline_dist = baseline_clean.value_counts(normalize=True)
        current_dist = current_clean.value_counts(normalize=True)
        
        # Align distributions
        all_categories = baseline_dist.index.union(current_dist.index)
        baseline_dist = baseline_dist.reindex(all_categories, fill_value=0.0001)
        current_dist = current_dist.reindex(all_categories, fill_value=0.0001)
        
        # Calculate CSI
        csi_values = (current_dist - baseline_dist) * np.log(current_dist / baseline_dist)
        csi = csi_values.sum()
        
        # Interpretation
        if csi < 0.1:
            interpretation = "Stable"
            action = "No action needed"
        elif csi < 0.25:
            interpretation = "Moderate drift"
            action = "Monitor"
        else:
            interpretation = "Significant drift"
            action = "Investigate"
        
        return {
            'csi': float(csi),
            'interpretation': interpretation,
            'action': action,
            'category_contributions': dict(zip(all_categories, csi_values.values)),
            'new_categories': list(set(current_clean.unique()) - set(baseline_clean.unique())),
            'missing_categories': list(set(baseline_clean.unique()) - set(current_clean.unique()))
        }
    
    def monitor_dataset(self, baseline_df: pd.DataFrame, current_df: pd.DataFrame,
                       features: Optional[List[str]] = None) -> Dict:
        """
        Monitor entire dataset for drift
        
        Args:
            baseline_df: Baseline dataset
            current_df: Current dataset
            features: Features to monitor (None = all numeric)
        
        Returns:
            Monitoring report dictionary
        """
        if features is None:
            features = baseline_df.select_dtypes(include=[np.number]).columns.tolist()
        
        results = {}
        alerts = []
        
        for feature in features:
            if feature not in baseline_df.columns or feature not in current_df.columns:
                continue
            
            # Calculate PSI/CSI
            if pd.api.types.is_numeric_dtype(baseline_df[feature]):
                metric = self.calculate_psi(baseline_df[feature], current_df[feature])
                metric_name = 'psi'
            else:
                metric = self.calculate_csi(baseline_df[feature], current_df[feature])
                metric_name = 'csi'
            
            results[feature] = metric
            
            # Check for alerts
            score = metric[metric_name]
            if score >= self.alert_threshold_psi:
                alerts.append({
                    'feature': feature,
                    'metric': metric_name.upper(),
                    'score': score,
                    'interpretation': metric['interpretation'],
                    'action': metric['action']
                })
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'n_features_monitored': len(results),
            'n_alerts': len(alerts),
            'alerts': alerts,
            'feature_metrics': results,
            'overall_status': 'ALERT' if alerts else 'OK'
        }
        
        self.monitoring_history.append(report)
        
        print(f"✓ Monitored {len(results)} features")
        if alerts:
            print(f"⚠️  {len(alerts)} alert(s) detected!")
            for alert in alerts:
                print(f"   - {alert['feature']}: {alert['metric']}={alert['score']:.4f} ({alert['interpretation']})")
        
        return report
    
    def set_baseline(self, df: pd.DataFrame, features: Optional[List[str]] = None):
        """
        Set baseline distributions for monitoring
        
        Args:
            df: Baseline dataset
            features: Features to track (None = all)
        """
        if features is None:
            features = df.columns.tolist()
        
        for feature in features:
            if feature in df.columns:
                self.baseline_distributions[feature] = df[feature].copy()
        
        print(f"✓ Baseline set for {len(self.baseline_distributions)} features")
    
    def track_model_performance(self, y_true: pd.Series, y_pred: pd.Series,
                               y_proba: Optional[pd.Series] = None,
                               timestamp: Optional[str] = None) -> Dict:
        """
        Track model performance over time
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities
            timestamp: Timestamp (default: now)
        
        Returns:
            Performance metrics dictionary
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        from sklearn.metrics import roc_auc_score, confusion_matrix
        
        metrics = {
            'timestamp': timestamp or datetime.now().isoformat(),
            'n_samples': len(y_true),
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, average='binary', zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, average='binary', zero_division=0)),
            'f1': float(f1_score(y_true, y_pred, average='binary', zero_division=0))
        }
        
        # Add AUC if probabilities provided
        if y_proba is not None:
            metrics['auc'] = float(roc_auc_score(y_true, y_proba))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = {
            'tn': int(cm[0, 0]) if cm.shape[0] > 0 else 0,
            'fp': int(cm[0, 1]) if cm.shape[0] > 1 else 0,
            'fn': int(cm[1, 0]) if cm.shape[0] > 1 else 0,
            'tp': int(cm[1, 1]) if cm.shape[0] > 1 else 0
        }
        
        self.monitoring_history.append(metrics)
        
        print(f"✓ Performance tracked: AUC={metrics.get('auc', 'N/A')}, F1={metrics['f1']:.4f}")
        return metrics
    
    def detect_concept_drift(self, baseline_performance: Dict,
                            current_performance: Dict,
                            threshold: float = 0.05) -> Dict:
        """
        Detect concept drift by comparing performance
        
        Args:
            baseline_performance: Baseline metrics
            current_performance: Current metrics
            threshold: Degradation threshold for alerts
        
        Returns:
            Drift detection results
        """
        drift_detected = False
        degraded_metrics = []
        
        for metric in ['accuracy', 'precision', 'recall', 'f1', 'auc']:
            if metric in baseline_performance and metric in current_performance:
                baseline_value = baseline_performance[metric]
                current_value = current_performance[metric]
                degradation = baseline_value - current_value
                
                if degradation > threshold:
                    drift_detected = True
                    degraded_metrics.append({
                        'metric': metric,
                        'baseline': baseline_value,
                        'current': current_value,
                        'degradation': degradation
                    })
        
        result = {
            'drift_detected': drift_detected,
            'degraded_metrics': degraded_metrics,
            'action': 'Retrain model' if drift_detected else 'Continue monitoring'
        }
        
        if drift_detected:
            print(f"⚠️  Concept drift detected! {len(degraded_metrics)} metric(s) degraded")
        else:
            print("✓ No concept drift detected")
        
        return result
    
    def generate_monitoring_report(self) -> pd.DataFrame:
        """
        Generate comprehensive monitoring report
        
        Returns:
            DataFrame with monitoring history
        """
        if not self.monitoring_history:
            print("No monitoring history available")
            return pd.DataFrame()
        
        df_report = pd.DataFrame(self.monitoring_history)
        print(f"✓ Generated report with {len(df_report)} monitoring events")
        return df_report
    
    def export_alerts(self, filepath: str):
        """
        Export alerts to JSON file
        
        Args:
            filepath: Output file path
        """
        import json
        
        alerts = [
            event for event in self.monitoring_history
            if event.get('overall_status') == 'ALERT' or event.get('drift_detected')
        ]
        
        with open(filepath, 'w') as f:
            json.dump(alerts, f, indent=2)
        
        print(f"✓ Exported {len(alerts)} alert(s) to {filepath}")
