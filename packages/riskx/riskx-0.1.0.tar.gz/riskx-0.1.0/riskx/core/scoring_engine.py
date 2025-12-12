"""
RiskX Scoring Engine - Real-Time Risk Scoring
============================================

Production-ready scoring engine with:
- Real-time predictions
- Batch scoring
- Score binning and interpretation
- API-ready endpoints
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
import json
from datetime import datetime


class ScoringEngine:
    """
    Production scoring engine for risk models
    
    Features:
    - Real-time single predictions
    - Batch scoring
    - Score binning and rating
    - Reason code generation
    - Score interpretation
    """
    
    def __init__(self, model: Any = None, score_min: int = 300, score_max: int = 850):
        self.model = model
        self.score_min = score_min
        self.score_max = score_max
        self.score_bins = self._create_default_bins()
        self.feature_names = None
    
    def _create_default_bins(self) -> Dict:
        """Create default score bins and ratings"""
        return {
            'Poor': (300, 579),
            'Fair': (580, 669),
            'Good': (670, 739),
            'Very Good': (740, 799),
            'Excellent': (800, 850)
        }
    
    def score_single(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a single customer/application
        
        Args:
            features: Feature dictionary
        
        Returns:
            Scoring result dictionary
        """
        if self.model is None:
            raise ValueError("No model loaded. Load a model first.")
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Predict probability
        prob = self.model.predict_proba(df)[:, 1][0]
        
        # Convert to score
        score = self._prob_to_score(prob)
        
        # Get rating
        rating = self._score_to_rating(score)
        
        # Generate reason codes (top contributing features)
        reason_codes = self._generate_reason_codes(df)
        
        result = {
            'score': int(score),
            'probability': float(prob),
            'rating': rating,
            'risk_level': self._get_risk_level(score),
            'reason_codes': reason_codes,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def score_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Score multiple customers/applications
        
        Args:
            df: Features DataFrame
        
        Returns:
            DataFrame with scores added
        """
        if self.model is None:
            raise ValueError("No model loaded. Load a model first.")
        
        # Predict probabilities
        probs = self.model.predict_proba(df)[:, 1]
        
        # Convert to scores
        scores = np.vectorize(self._prob_to_score)(probs)
        
        # Add to DataFrame
        df_scored = df.copy()
        df_scored['probability'] = probs
        df_scored['score'] = scores.astype(int)
        df_scored['rating'] = np.vectorize(self._score_to_rating)(scores)
        df_scored['risk_level'] = np.vectorize(self._get_risk_level)(scores)
        
        print(f"✓ Scored {len(df)} records")
        return df_scored
    
    def _prob_to_score(self, prob: float) -> int:
        """
        Convert probability to credit score scale
        
        Uses a logarithmic transformation to map [0,1] probabilities
        to the score range (default 300-850)
        """
        # Avoid log(0) and log(1)
        prob = np.clip(prob, 0.001, 0.999)
        
        # Log-odds transformation
        log_odds = np.log(prob / (1 - prob))
        
        # Normalize to score range
        # Typical log-odds range: [-6, 6]
        normalized = (log_odds + 6) / 12  # Map to [0, 1]
        score = self.score_min + normalized * (self.score_max - self.score_min)
        
        return int(np.clip(score, self.score_min, self.score_max))
    
    def _score_to_rating(self, score: int) -> str:
        """Convert score to rating category"""
        for rating, (low, high) in self.score_bins.items():
            if low <= score <= high:
                return rating
        return 'Unknown'
    
    def _get_risk_level(self, score: int) -> str:
        """Get risk level from score"""
        if score >= 740:
            return 'Low'
        elif score >= 670:
            return 'Medium'
        elif score >= 580:
            return 'High'
        else:
            return 'Very High'
    
    def _generate_reason_codes(self, df: pd.DataFrame, top_n: int = 3) -> List[Dict]:
        """
        Generate reason codes explaining score
        
        Returns top N most influential features
        """
        if not hasattr(self.model, 'feature_importances_'):
            return []
        
        # Get feature importances
        importances = self.model.feature_importances_
        feature_names = df.columns.tolist()
        
        # Sort by importance
        indices = np.argsort(importances)[::-1][:top_n]
        
        reason_codes = []
        for i, idx in enumerate(indices):
            reason_codes.append({
                'code': f'RC{i+1}',
                'feature': feature_names[idx],
                'value': float(df.iloc[0, idx]),
                'importance': float(importances[idx]),
                'description': f'{feature_names[idx]} contributed to this score'
            })
        
        return reason_codes
    
    def set_custom_bins(self, bins: Dict[str, tuple]):
        """
        Set custom score bins
        
        Args:
            bins: Dictionary mapping rating names to (low, high) tuples
        """
        self.score_bins = bins
        print(f"✓ Custom score bins set: {len(bins)} categories")
    
    def interpret_score(self, score: int) -> Dict[str, Any]:
        """
        Provide interpretation of a score
        
        Args:
            score: Credit score to interpret
        
        Returns:
            Interpretation dictionary
        """
        rating = self._score_to_rating(score)
        risk_level = self._get_risk_level(score)
        
        # Approval recommendation
        if score >= 700:
            recommendation = "Approve"
            approval_probability = 0.9
        elif score >= 640:
            recommendation = "Review"
            approval_probability = 0.6
        else:
            recommendation = "Decline"
            approval_probability = 0.2
        
        # Interest rate suggestion (example)
        if score >= 750:
            suggested_rate = 3.5
        elif score >= 700:
            suggested_rate = 5.0
        elif score >= 650:
            suggested_rate = 7.5
        elif score >= 600:
            suggested_rate = 10.0
        else:
            suggested_rate = 15.0
        
        return {
            'score': score,
            'rating': rating,
            'risk_level': risk_level,
            'recommendation': recommendation,
            'approval_probability': approval_probability,
            'suggested_interest_rate': suggested_rate,
            'percentile': self._score_to_percentile(score)
        }
    
    def _score_to_percentile(self, score: int) -> int:
        """Convert score to percentile (approximate)"""
        # Simplified percentile mapping
        normalized = (score - self.score_min) / (self.score_max - self.score_min)
        percentile = int(normalized * 100)
        return np.clip(percentile, 0, 99)
    
    def load_model(self, model: Any):
        """Load a trained model"""
        self.model = model
        print("✓ Model loaded into scoring engine")
    
    def export_api_spec(self) -> Dict:
        """
        Export API specification for integration
        
        Returns:
            OpenAPI-like specification
        """
        spec = {
            'endpoints': {
                '/score/single': {
                    'method': 'POST',
                    'description': 'Score a single application',
                    'input': {
                        'type': 'object',
                        'properties': {
                            'features': {
                                'type': 'object',
                                'description': 'Feature dictionary'
                            }
                        }
                    },
                    'output': {
                        'score': 'int',
                        'probability': 'float',
                        'rating': 'string',
                        'risk_level': 'string',
                        'reason_codes': 'array'
                    }
                },
                '/score/batch': {
                    'method': 'POST',
                    'description': 'Score multiple applications',
                    'input': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'description': 'Feature dictionary'
                        }
                    },
                    'output': {
                        'type': 'array',
                        'items': {
                            'score': 'int',
                            'probability': 'float',
                            'rating': 'string'
                        }
                    }
                }
            },
            'score_range': {
                'min': self.score_min,
                'max': self.score_max
            },
            'ratings': self.score_bins
        }
        
        return spec
    
    def generate_scorecard(self, feature_weights: Dict[str, float]) -> pd.DataFrame:
        """
        Generate a traditional scorecard from feature weights
        
        Args:
            feature_weights: Feature to weight mapping
        
        Returns:
            Scorecard DataFrame
        """
        scorecard = []
        
        for feature, weight in feature_weights.items():
            # Convert weight to points (example)
            points = int(weight * 100)
            
            scorecard.append({
                'Feature': feature,
                'Weight': weight,
                'Points': points,
                'Description': f'Contribution of {feature}'
            })
        
        df_scorecard = pd.DataFrame(scorecard)
        df_scorecard = df_scorecard.sort_values('Points', ascending=False)
        
        print(f"✓ Scorecard generated with {len(scorecard)} features")
        return df_scorecard
    
    def simulate_score_distribution(self, n_samples: int = 10000) -> pd.DataFrame:
        """
        Simulate score distribution for testing
        
        Args:
            n_samples: Number of samples to simulate
        
        Returns:
            DataFrame with simulated scores
        """
        # Generate random probabilities from beta distribution
        # Beta(2,5) gives realistic distribution of scores
        probs = np.random.beta(2, 5, n_samples)
        
        # Convert to scores
        scores = np.vectorize(self._prob_to_score)(probs)
        
        df_sim = pd.DataFrame({
            'probability': probs,
            'score': scores,
            'rating': np.vectorize(self._score_to_rating)(scores),
            'risk_level': np.vectorize(self._get_risk_level)(scores)
        })
        
        print(f"✓ Simulated {n_samples} score records")
        print("\nScore Distribution:")
        print(df_sim['rating'].value_counts().sort_index())
        
        return df_sim
