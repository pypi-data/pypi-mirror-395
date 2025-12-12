"""
RiskX Model Evaluation - Comprehensive Model Assessment
======================================================

Model evaluation metrics for risk scoring models.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.metrics import (
    roc_auc_score, roc_curve, precision_recall_curve,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)


class RiskEvaluator:
    """
    Comprehensive model evaluation for risk scoring
    
    Features:
    - Classification metrics
    - ROC and PR curves
    - Calibration assessment
    - Business metrics (approval rates, etc.)
    """
    
    def __init__(self):
        self.evaluation_results = {}
    
    def evaluate_classification(self, y_true: pd.Series, y_pred: pd.Series,
                               y_proba: Optional[pd.Series] = None) -> Dict:
        """
        Evaluate classification performance
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities
        
        Returns:
            Evaluation metrics dictionary
        """
        metrics = {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, zero_division=0)),
            'f1': float(f1_score(y_true, y_pred, zero_division=0))
        }
        
        # Add AUC if probabilities provided
        if y_proba is not None:
            metrics['auc'] = float(roc_auc_score(y_true, y_proba))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = {
            'tn': int(cm[0, 0]),
            'fp': int(cm[0, 1]),
            'fn': int(cm[1, 0]),
            'tp': int(cm[1, 1])
        }
        
        # Derived metrics
        if metrics['confusion_matrix']['tp'] + metrics['confusion_matrix']['fn'] > 0:
            metrics['sensitivity'] = metrics['confusion_matrix']['tp'] / (
                metrics['confusion_matrix']['tp'] + metrics['confusion_matrix']['fn']
            )
        
        if metrics['confusion_matrix']['tn'] + metrics['confusion_matrix']['fp'] > 0:
            metrics['specificity'] = metrics['confusion_matrix']['tn'] / (
                metrics['confusion_matrix']['tn'] + metrics['confusion_matrix']['fp']
            )
        
        print(f"✓ Classification metrics: AUC={metrics.get('auc', 'N/A')}, F1={metrics['f1']:.4f}")
        self.evaluation_results['classification'] = metrics
        return metrics
    
    def evaluate_business_metrics(self, scores: pd.Series, y_true: pd.Series,
                                  approval_threshold: int = 640) -> Dict:
        """
        Evaluate business-relevant metrics
        
        Args:
            scores: Credit scores
            y_true: True default indicators
            approval_threshold: Score threshold for approval
        
        Returns:
            Business metrics dictionary
        """
        # Approval rate
        approved = (scores >= approval_threshold).sum()
        approval_rate = approved / len(scores)
        
        # Default rate among approved
        approved_mask = scores >= approval_threshold
        if approved > 0:
            default_rate_approved = y_true[approved_mask].mean()
        else:
            default_rate_approved = 0.0
        
        # Capture rate (% of good customers approved)
        good_customers = (y_true == 0).sum()
        if good_customers > 0:
            good_approved = ((scores >= approval_threshold) & (y_true == 0)).sum()
            capture_rate = good_approved / good_customers
        else:
            capture_rate = 0.0
        
        metrics = {
            'approval_rate': float(approval_rate),
            'approval_threshold': approval_threshold,
            'n_approved': int(approved),
            'default_rate_approved': float(default_rate_approved),
            'capture_rate': float(capture_rate)
        }
        
        print(f"✓ Business metrics: Approval rate={approval_rate:.2%}, Default rate={default_rate_approved:.2%}")
        self.evaluation_results['business'] = metrics
        return metrics
    
    def get_summary(self) -> pd.DataFrame:
        """Get evaluation summary"""
        return pd.DataFrame([self.evaluation_results])
