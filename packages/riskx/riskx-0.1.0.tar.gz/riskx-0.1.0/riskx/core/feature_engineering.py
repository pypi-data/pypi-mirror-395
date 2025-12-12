"""
Feature Engineering - Risk-Specific Feature Creation
===================================================

Weight of Evidence (WOE), Information Value (IV), binning,
behavioral features, transaction aggregations, and time-based features.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import warnings


class RiskFeatureEngine:
    """
    Automated feature engineering for risk scoring models
    
    Features:
    - Weight of Evidence (WOE) and Information Value (IV)
    - Automated optimal binning
    - Behavioral features
    - Transaction aggregations
    - Time-based features
    - Ratio and interaction features
    """
    
    def __init__(self):
        self.woe_maps = {}
        self.iv_scores = {}
        self.bin_edges = {}
    
    def compute_woe_iv(self, df: pd.DataFrame, feature: str, target: str, n_bins: int = 10) -> Tuple[pd.DataFrame, float]:
        """
        Compute Weight of Evidence (WOE) and Information Value (IV)
        
        Args:
            df: Input DataFrame
            feature: Feature column name
            target: Target column name (binary 0/1)
            n_bins: Number of bins for numeric features
        
        Returns:
            Tuple of (WOE DataFrame, IV score)
        """
        df_woe = df[[feature, target]].copy()
        
        # Bin numeric features
        if pd.api.types.is_numeric_dtype(df_woe[feature]):
            df_woe[f'{feature}_binned'] = pd.qcut(df_woe[feature], q=n_bins, duplicates='drop')
            feature_col = f'{feature}_binned'
        else:
            feature_col = feature
        
        # Calculate distributions
        total_good = df_woe[target].sum()
        total_bad = len(df_woe) - total_good
        
        woe_table = []
        
        for category in df_woe[feature_col].unique():
            if pd.isna(category):
                continue
            
            subset = df_woe[df_woe[feature_col] == category]
            n_good = subset[target].sum()
            n_bad = len(subset) - n_good
            
            # Avoid division by zero
            pct_good = (n_good / total_good) if total_good > 0 else 0.0001
            pct_bad = (n_bad / total_bad) if total_bad > 0 else 0.0001
            
            # WOE = ln(% of goods / % of bads)
            woe = np.log(pct_good / pct_bad) if pct_bad > 0 else 0
            
            # IV = (% of goods - % of bads) * WOE
            iv = (pct_good - pct_bad) * woe
            
            woe_table.append({
                'category': str(category),
                'n_records': len(subset),
                'n_good': int(n_good),
                'n_bad': int(n_bad),
                'pct_good': pct_good,
                'pct_bad': pct_bad,
                'woe': woe,
                'iv': iv
            })
        
        woe_df = pd.DataFrame(woe_table)
        total_iv = woe_df['iv'].sum()
        
        # Store for transformation
        self.woe_maps[feature] = dict(zip(woe_df['category'], woe_df['woe']))
        self.iv_scores[feature] = total_iv
        
        print(f"✓ WOE/IV for {feature}: IV = {total_iv:.4f}")
        return woe_df, total_iv
    
    def auto_bin(self, df: pd.DataFrame, column: str, n_bins: int = 10, 
                 method: str = "quantile") -> pd.DataFrame:
        """
        Automatic optimal binning for numeric features
        
        Args:
            df: Input DataFrame
            column: Column to bin
            n_bins: Number of bins
            method: Binning method ('quantile', 'uniform', 'kmeans')
        
        Returns:
            DataFrame with binned column
        """
        df_binned = df.copy()
        
        if not pd.api.types.is_numeric_dtype(df[column]):
            warnings.warn(f"{column} is not numeric, skipping binning")
            return df_binned
        
        if method == "quantile":
            df_binned[f'{column}_binned'], bin_edges = pd.qcut(
                df[column], q=n_bins, duplicates='drop', retbins=True, labels=False
            )
            self.bin_edges[column] = bin_edges
        
        elif method == "uniform":
            df_binned[f'{column}_binned'], bin_edges = pd.cut(
                df[column], bins=n_bins, duplicates='drop', retbins=True, labels=False
            )
            self.bin_edges[column] = bin_edges
        
        elif method == "kmeans":
            try:
                from sklearn.cluster import KMeans
                kmeans = KMeans(n_clusters=n_bins, random_state=42, n_init=10)
                df_binned[f'{column}_binned'] = kmeans.fit_predict(df[[column]])
            except ImportError:
                warnings.warn("scikit-learn required for kmeans binning")
                return df_binned
        
        print(f"✓ Binned {column} into {n_bins} bins using {method} method")
        return df_binned
    
    def behavioral_features(self, df: pd.DataFrame, customer_id: str, 
                           time_column: str, value_column: str) -> pd.DataFrame:
        """
        Create behavioral features from transaction data
        
        Features:
        - Recency (days since last transaction)
        - Frequency (number of transactions)
        - Monetary (total transaction value)
        - Average transaction value
        - Transaction velocity
        
        Args:
            df: Input DataFrame
            customer_id: Customer identifier column
            time_column: Transaction timestamp column
            value_column: Transaction value column
        
        Returns:
            DataFrame with behavioral features
        """
        df_behavior = df.copy()
        
        # Ensure datetime
        df_behavior[time_column] = pd.to_datetime(df_behavior[time_column])
        
        # Reference date (most recent)
        ref_date = df_behavior[time_column].max()
        
        # Aggregate by customer
        behavior_features = df_behavior.groupby(customer_id).agg({
            time_column: lambda x: (ref_date - x.max()).days,  # Recency
            value_column: ['count', 'sum', 'mean', 'std', 'min', 'max']  # Frequency & Monetary
        }).reset_index()
        
        # Flatten column names
        behavior_features.columns = [
            customer_id, 'recency_days', 'frequency_count', 
            'monetary_total', 'monetary_avg', 'monetary_std',
            'monetary_min', 'monetary_max'
        ]
        
        # Transaction velocity (transactions per day)
        date_range = df_behavior.groupby(customer_id)[time_column].agg(
            lambda x: (x.max() - x.min()).days + 1
        ).reset_index()
        date_range.columns = [customer_id, 'activity_days']
        
        behavior_features = behavior_features.merge(date_range, on=customer_id)
        behavior_features['transaction_velocity'] = (
            behavior_features['frequency_count'] / behavior_features['activity_days']
        )
        
        print(f"✓ Created {len(behavior_features.columns)-1} behavioral features")
        return behavior_features
    
    def transaction_features(self, df: pd.DataFrame, group_by: str,
                            agg_columns: List[str]) -> pd.DataFrame:
        """
        Create transaction aggregation features
        
        Args:
            df: Input DataFrame
            group_by: Column to group by (e.g., customer_id)
            agg_columns: Columns to aggregate
        
        Returns:
            DataFrame with aggregated features
        """
        agg_dict = {}
        
        for col in agg_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                agg_dict[col] = ['sum', 'mean', 'std', 'min', 'max', 'count']
            else:
                agg_dict[col] = ['count', 'nunique']
        
        trans_features = df.groupby(group_by).agg(agg_dict).reset_index()
        
        # Flatten column names
        trans_features.columns = [
            '_'.join(col).strip('_') if col[1] else col[0]
            for col in trans_features.columns.values
        ]
        
        print(f"✓ Created {len(trans_features.columns)-1} transaction features")
        return trans_features
    
    def time_features(self, df: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        Extract time-based features from datetime column
        
        Features:
        - Year, Month, Day
        - Day of week, Week of year
        - Quarter
        - Is weekend, Is month end
        - Days since epoch
        
        Args:
            df: Input DataFrame
            date_column: Datetime column name
        
        Returns:
            DataFrame with time features
        """
        df_time = df.copy()
        df_time[date_column] = pd.to_datetime(df_time[date_column])
        
        # Extract components
        df_time[f'{date_column}_year'] = df_time[date_column].dt.year
        df_time[f'{date_column}_month'] = df_time[date_column].dt.month
        df_time[f'{date_column}_day'] = df_time[date_column].dt.day
        df_time[f'{date_column}_dayofweek'] = df_time[date_column].dt.dayofweek
        df_time[f'{date_column}_quarter'] = df_time[date_column].dt.quarter
        df_time[f'{date_column}_weekofyear'] = df_time[date_column].dt.isocalendar().week
        
        # Binary features
        df_time[f'{date_column}_is_weekend'] = (df_time[date_column].dt.dayofweek >= 5).astype(int)
        df_time[f'{date_column}_is_month_end'] = df_time[date_column].dt.is_month_end.astype(int)
        df_time[f'{date_column}_is_month_start'] = df_time[date_column].dt.is_month_start.astype(int)
        df_time[f'{date_column}_is_quarter_end'] = df_time[date_column].dt.is_quarter_end.astype(int)
        
        # Days since epoch
        df_time[f'{date_column}_days_since_epoch'] = (
            df_time[date_column] - pd.Timestamp('1970-01-01')
        ).dt.days
        
        print(f"✓ Created 11 time features from {date_column}")
        return df_time
    
    def ratio_features(self, df: pd.DataFrame, numerator_cols: List[str],
                      denominator_cols: List[str], suffix: str = "_ratio") -> pd.DataFrame:
        """
        Create ratio features between columns
        
        Args:
            df: Input DataFrame
            numerator_cols: Numerator columns
            denominator_cols: Denominator columns
            suffix: Suffix for ratio columns
        
        Returns:
            DataFrame with ratio features
        """
        df_ratio = df.copy()
        
        for num_col in numerator_cols:
            for den_col in denominator_cols:
                if num_col != den_col:
                    ratio_col = f"{num_col}_{den_col}{suffix}"
                    df_ratio[ratio_col] = df_ratio[num_col] / (df_ratio[den_col] + 1e-10)
        
        n_ratios = len(numerator_cols) * len(denominator_cols) - len(numerator_cols)
        print(f"✓ Created {n_ratios} ratio features")
        return df_ratio
    
    def interaction_features(self, df: pd.DataFrame, columns: List[str],
                            max_interactions: int = 10) -> pd.DataFrame:
        """
        Create interaction features (products of pairs)
        
        Args:
            df: Input DataFrame
            columns: Columns to create interactions from
            max_interactions: Maximum number of interactions to create
        
        Returns:
            DataFrame with interaction features
        """
        df_interact = df.copy()
        
        interactions_created = 0
        
        for i, col1 in enumerate(columns):
            if interactions_created >= max_interactions:
                break
            
            for col2 in columns[i+1:]:
                if interactions_created >= max_interactions:
                    break
                
                if pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2]):
                    interact_col = f"{col1}_x_{col2}"
                    df_interact[interact_col] = df_interact[col1] * df_interact[col2]
                    interactions_created += 1
        
        print(f"✓ Created {interactions_created} interaction features")
        return df_interact
    
    def auto_features(self, df: pd.DataFrame, target: str,
                     include_woe: bool = True,
                     include_time: bool = True,
                     include_ratios: bool = True) -> pd.DataFrame:
        """
        Automated feature engineering pipeline
        
        Args:
            df: Input DataFrame
            target: Target variable name
            include_woe: Include WOE transformations
            include_time: Include time features
            include_ratios: Include ratio features
        
        Returns:
            DataFrame with engineered features
        """
        print("Starting automated feature engineering...")
        
        df_features = df.copy()
        
        # Identify feature types
        numeric_cols = df_features.select_dtypes(include=[np.number]).columns.tolist()
        if target in numeric_cols:
            numeric_cols.remove(target)
        
        date_cols = df_features.select_dtypes(include=['datetime64']).columns.tolist()
        
        # WOE/IV for important features
        if include_woe and target in df_features.columns:
            for col in numeric_cols[:5]:  # Top 5 numeric features
                try:
                    woe_df, iv = self.compute_woe_iv(df_features, col, target, n_bins=5)
                    # Add WOE-transformed column
                    df_features[f'{col}_woe'] = df_features[col].apply(
                        lambda x: self.woe_maps.get(col, {}).get(str(pd.qcut([x], q=5, duplicates='drop')[0]), 0)
                    )
                except:
                    pass
        
        # Time features
        if include_time and date_cols:
            for date_col in date_cols[:2]:  # First 2 date columns
                df_features = self.time_features(df_features, date_col)
        
        # Ratio features
        if include_ratios and len(numeric_cols) >= 2:
            df_features = self.ratio_features(
                df_features,
                numeric_cols[:3],  # First 3 numeric columns
                numeric_cols[:3],
                suffix="_ratio"
            )
        
        # Interaction features
        if len(numeric_cols) >= 2:
            df_features = self.interaction_features(df_features, numeric_cols[:5], max_interactions=5)
        
        n_new_features = len(df_features.columns) - len(df.columns)
        print(f"✓ Auto-feature engineering complete: {n_new_features} new features created")
        return df_features
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get IV scores for features (feature importance)"""
        return self.iv_scores
