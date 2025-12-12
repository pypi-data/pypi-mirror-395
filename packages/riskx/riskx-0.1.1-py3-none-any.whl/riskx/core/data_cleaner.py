"""
Data Cleaner - Automated Data Cleaning for Risk Models
======================================================

Handle missing values, outliers, invalid categories, normalization,
and encoding specifically for risk scoring applications.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
import warnings


class RiskCleaner:
    """
    Automated data cleaning for risk scoring
    
    Features:
    - Missing value imputation
    - Outlier detection and handling
    - Type validation and correction
    - Categorical encoding
    - Normalization
    - Auto-cleaning pipeline
    """
    
    def __init__(self):
        self.cleaning_report = {}
        self.encoders = {}
        self.scalers = {}
    
    def profile(self, df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive data quality profile
        
        Args:
            df: Input DataFrame
        
        Returns:
            Dictionary with data quality metrics
        """
        profile = {
            "n_rows": len(df),
            "n_columns": len(df.columns),
            "columns": {}
        }
        
        for col in df.columns:
            col_profile = {
                "dtype": str(df[col].dtype),
                "missing_count": int(df[col].isnull().sum()),
                "missing_pct": float(df[col].isnull().sum() / len(df) * 100),
                "unique_count": int(df[col].nunique()),
                "unique_pct": float(df[col].nunique() / len(df) * 100)
            }
            
            # Numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_profile.update({
                    "mean": float(df[col].mean()) if not df[col].isnull().all() else None,
                    "std": float(df[col].std()) if not df[col].isnull().all() else None,
                    "min": float(df[col].min()) if not df[col].isnull().all() else None,
                    "max": float(df[col].max()) if not df[col].isnull().all() else None,
                    "median": float(df[col].median()) if not df[col].isnull().all() else None,
                    "zeros_count": int((df[col] == 0).sum()),
                    "negatives_count": int((df[col] < 0).sum())
                })
                
                # Detect outliers using IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                col_profile["outliers_count"] = int(outliers)
                col_profile["outliers_pct"] = float(outliers / len(df) * 100)
            
            # Categorical columns
            else:
                top_values = df[col].value_counts().head(5).to_dict()
                col_profile["top_values"] = {str(k): int(v) for k, v in top_values.items()}
            
            profile["columns"][col] = col_profile
        
        return profile
    
    def clean_missing(self, df: pd.DataFrame, strategy: str = "auto", 
                     fill_value: Optional[Union[int, float, str]] = None) -> pd.DataFrame:
        """
        Handle missing values
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values
                     'auto' - automatic based on data type
                     'mean' - fill with mean (numeric)
                     'median' - fill with median (numeric)
                     'mode' - fill with mode (categorical)
                     'forward' - forward fill
                     'drop' - drop rows with missing values
                     'fill' - fill with specific value
            fill_value: Value to use when strategy='fill'
        
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()
        
        for col in df_clean.columns:
            missing_count = df_clean[col].isnull().sum()
            
            if missing_count == 0:
                continue
            
            if strategy == "auto":
                # Numeric: use median
                if pd.api.types.is_numeric_dtype(df_clean[col]):
                    fill_val = df_clean[col].median()
                    df_clean[col].fillna(fill_val, inplace=True)
                # Categorical: use mode
                else:
                    mode_val = df_clean[col].mode()
                    if len(mode_val) > 0:
                        df_clean[col].fillna(mode_val[0], inplace=True)
            
            elif strategy == "mean" and pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col].fillna(df_clean[col].mean(), inplace=True)
            
            elif strategy == "median" and pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
            
            elif strategy == "mode":
                mode_val = df_clean[col].mode()
                if len(mode_val) > 0:
                    df_clean[col].fillna(mode_val[0], inplace=True)
            
            elif strategy == "forward":
                df_clean[col].fillna(method='ffill', inplace=True)
            
            elif strategy == "fill" and fill_value is not None:
                df_clean[col].fillna(fill_value, inplace=True)
        
        if strategy == "drop":
            df_clean.dropna(inplace=True)
        
        self.cleaning_report["missing_values"] = {
            "strategy": strategy,
            "rows_before": len(df),
            "rows_after": len(df_clean)
        }
        
        print(f"✓ Cleaned missing values: {len(df)} → {len(df_clean)} rows")
        return df_clean
    
    def clean_outliers(self, df: pd.DataFrame, method: str = "iqr", 
                      threshold: float = 1.5, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Detect and handle outliers
        
        Args:
            df: Input DataFrame
            method: Method for outlier detection
                   'iqr' - Interquartile Range
                   'zscore' - Z-score method
                   'clip' - Clip to percentiles
            threshold: Threshold multiplier (for IQR or Z-score)
            columns: Columns to check (None = all numeric columns)
        
        Returns:
            DataFrame with outliers handled
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        outliers_removed = 0
        
        for col in columns:
            if col not in df_clean.columns:
                continue
            
            if not pd.api.types.is_numeric_dtype(df_clean[col]):
                continue
            
            if method == "iqr":
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                # Cap outliers
                original_count = len(df_clean)
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
            
            elif method == "zscore":
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                
                z_scores = np.abs((df_clean[col] - mean) / std)
                df_clean = df_clean[z_scores < threshold]
                outliers_removed += (len(df) - len(df_clean))
            
            elif method == "clip":
                lower = df_clean[col].quantile(0.01)
                upper = df_clean[col].quantile(0.99)
                df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
        
        self.cleaning_report["outliers"] = {
            "method": method,
            "threshold": threshold,
            "columns_processed": len(columns),
            "outliers_handled": outliers_removed
        }
        
        print(f"✓ Handled outliers in {len(columns)} columns using {method} method")
        return df_clean
    
    def clean_types(self, df: pd.DataFrame, type_map: Optional[Dict[str, str]] = None) -> pd.DataFrame:
        """
        Validate and correct data types
        
        Args:
            df: Input DataFrame
            type_map: Dictionary mapping column names to target types
        
        Returns:
            DataFrame with corrected types
        """
        df_clean = df.copy()
        
        if type_map:
            for col, target_type in type_map.items():
                if col not in df_clean.columns:
                    continue
                
                try:
                    if target_type == "int":
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype('Int64')
                    elif target_type == "float":
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    elif target_type == "str":
                        df_clean[col] = df_clean[col].astype(str)
                    elif target_type == "datetime":
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    elif target_type == "category":
                        df_clean[col] = df_clean[col].astype('category')
                except Exception as e:
                    warnings.warn(f"Could not convert {col} to {target_type}: {e}")
        
        print(f"✓ Corrected types for {len(type_map) if type_map else 0} columns")
        return df_clean
    
    def encode_categorical(self, df: pd.DataFrame, columns: Optional[List[str]] = None,
                          method: str = "label") -> pd.DataFrame:
        """
        Encode categorical variables
        
        Args:
            df: Input DataFrame
            columns: Columns to encode (None = all object columns)
            method: Encoding method
                   'label' - Label encoding
                   'onehot' - One-hot encoding
        
        Returns:
            DataFrame with encoded variables
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if method == "label":
            for col in columns:
                if col not in df_clean.columns:
                    continue
                
                encoder = LabelEncoder()
                df_clean[col] = encoder.fit_transform(df_clean[col].astype(str))
                self.encoders[col] = encoder
        
        elif method == "onehot":
            df_clean = pd.get_dummies(df_clean, columns=columns, drop_first=True)
        
        print(f"✓ Encoded {len(columns)} categorical columns using {method} encoding")
        return df_clean
    
    def normalize(self, df: pd.DataFrame, columns: Optional[List[str]] = None,
                 method: str = "standard") -> pd.DataFrame:
        """
        Normalize numerical features
        
        Args:
            df: Input DataFrame
            columns: Columns to normalize (None = all numeric columns)
            method: Normalization method
                   'standard' - StandardScaler (mean=0, std=1)
                   'minmax' - MinMaxScaler (range 0-1)
        
        Returns:
            DataFrame with normalized features
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        if method == "standard":
            scaler = StandardScaler()
        elif method == "minmax":
            scaler = MinMaxScaler()
        else:
            raise ValueError(f"Unknown normalization method: {method}")
        
        df_clean[columns] = scaler.fit_transform(df_clean[columns])
        self.scalers[method] = scaler
        
        print(f"✓ Normalized {len(columns)} columns using {method} scaling")
        return df_clean
    
    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        df_clean = df.copy()
        original_len = len(df_clean)
        df_clean.drop_duplicates(subset=subset, inplace=True)
        duplicates_removed = original_len - len(df_clean)
        
        print(f"✓ Removed {duplicates_removed} duplicate rows")
        return df_clean
    
    def auto_clean(self, df: pd.DataFrame, target_column: Optional[str] = None) -> pd.DataFrame:
        """
        Automated cleaning pipeline
        
        Steps:
        1. Remove duplicates
        2. Handle missing values
        3. Handle outliers
        4. Encode categorical variables
        5. Normalize numeric features (excluding target)
        
        Args:
            df: Input DataFrame
            target_column: Target variable to exclude from normalization
        
        Returns:
            Cleaned DataFrame
        """
        print("Starting automated cleaning pipeline...")
        
        df_clean = df.copy()
        
        # Step 1: Remove duplicates
        df_clean = self.remove_duplicates(df_clean)
        
        # Step 2: Handle missing values
        df_clean = self.clean_missing(df_clean, strategy="auto")
        
        # Step 3: Handle outliers (less aggressive for risk models)
        df_clean = self.clean_outliers(df_clean, method="clip")
        
        # Step 4: Encode categorical variables
        cat_columns = df_clean.select_dtypes(include=['object', 'category']).columns.tolist()
        if target_column and target_column in cat_columns:
            cat_columns.remove(target_column)
        
        if cat_columns:
            df_clean = self.encode_categorical(df_clean, columns=cat_columns, method="label")
        
        # Step 5: Normalize numeric features (excluding target)
        num_columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        if target_column and target_column in num_columns:
            num_columns.remove(target_column)
        
        if num_columns:
            df_clean = self.normalize(df_clean, columns=num_columns, method="standard")
        
        print(f"✓ Auto-cleaning complete: {len(df)} → {len(df_clean)} rows, {len(df.columns)} → {len(df_clean.columns)} columns")
        return df_clean
    
    def get_report(self) -> Dict:
        """Get cleaning report"""
        return self.cleaning_report
