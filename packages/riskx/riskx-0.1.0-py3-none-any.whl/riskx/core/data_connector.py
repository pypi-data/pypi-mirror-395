"""
Data Connector - Multi-Source Data Loading for RiskX
====================================================

Load data from CSV, Excel, SQL databases, APIs, and data lakes.
Automatically unify schemas and validate data types.
"""

import pandas as pd
import json
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import warnings


class RiskDataConnector:
    """
    Universal data connector for risk scoring models
    
    Supports:
    - CSV/Excel files
    - SQL databases
    - REST APIs
    - Data lakes
    - JSON/Parquet files
    """
    
    def __init__(self):
        self.data = None
        self.schema = {}
        self.source_info = {}
    
    def from_csv(self, path: str, **kwargs) -> 'RiskDataConnector':
        """
        Load data from CSV file
        
        Args:
            path: Path to CSV file
            **kwargs: Additional arguments for pd.read_csv
        
        Returns:
            Self for method chaining
        """
        self.data = pd.read_csv(path, **kwargs)
        self.source_info = {"type": "csv", "path": path}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from CSV: {path}")
        return self
    
    def from_excel(self, path: str, sheet_name: Optional[Union[str, int]] = 0, **kwargs) -> 'RiskDataConnector':
        """
        Load data from Excel file
        
        Args:
            path: Path to Excel file
            sheet_name: Sheet to read (default: first sheet)
            **kwargs: Additional arguments for pd.read_excel
        
        Returns:
            Self for method chaining
        """
        self.data = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
        self.source_info = {"type": "excel", "path": path, "sheet": sheet_name}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from Excel: {path}")
        return self
    
    def from_sql(self, connection_string: str, query: str, **kwargs) -> 'RiskDataConnector':
        """
        Load data from SQL database
        
        Args:
            connection_string: Database connection string
            query: SQL query to execute
            **kwargs: Additional arguments for pd.read_sql
        
        Returns:
            Self for method chaining
        """
        try:
            from sqlalchemy import create_engine
            engine = create_engine(connection_string)
            self.data = pd.read_sql(query, engine, **kwargs)
            self.source_info = {"type": "sql", "connection": connection_string, "query": query}
            self._detect_schema()
            print(f"✓ Loaded {len(self.data)} rows from SQL database")
            return self
        except ImportError:
            raise ImportError("sqlalchemy is required for SQL connections. Install with: pip install sqlalchemy")
    
    def from_api(self, url: str, headers: Optional[Dict[str, str]] = None, 
                 params: Optional[Dict[str, Any]] = None, **kwargs) -> 'RiskDataConnector':
        """
        Load data from REST API
        
        Args:
            url: API endpoint URL
            headers: HTTP headers
            params: Query parameters
            **kwargs: Additional arguments for requests.get
        
        Returns:
            Self for method chaining
        """
        try:
            import requests
            response = requests.get(url, headers=headers, params=params, **kwargs)
            response.raise_for_status()
            
            data_json = response.json()
            
            # Handle different response formats
            if isinstance(data_json, list):
                self.data = pd.DataFrame(data_json)
            elif isinstance(data_json, dict):
                if 'data' in data_json:
                    self.data = pd.DataFrame(data_json['data'])
                elif 'results' in data_json:
                    self.data = pd.DataFrame(data_json['results'])
                else:
                    self.data = pd.DataFrame([data_json])
            
            self.source_info = {"type": "api", "url": url}
            self._detect_schema()
            print(f"✓ Loaded {len(self.data)} rows from API: {url}")
            return self
        except ImportError:
            raise ImportError("requests is required for API connections. Install with: pip install requests")
    
    def from_json(self, path: str, **kwargs) -> 'RiskDataConnector':
        """Load data from JSON file"""
        with open(path, 'r') as f:
            data_json = json.load(f)
        
        if isinstance(data_json, list):
            self.data = pd.DataFrame(data_json)
        else:
            self.data = pd.DataFrame([data_json])
        
        self.source_info = {"type": "json", "path": path}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from JSON: {path}")
        return self
    
    def from_parquet(self, path: str, **kwargs) -> 'RiskDataConnector':
        """Load data from Parquet file"""
        self.data = pd.read_parquet(path, **kwargs)
        self.source_info = {"type": "parquet", "path": path}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from Parquet: {path}")
        return self
    
    def from_datalake(self, path: str, storage_options: Optional[Dict] = None, **kwargs) -> 'RiskDataConnector':
        """
        Load data from cloud data lake (Azure, AWS S3, GCP)
        
        Args:
            path: Path to data (e.g., 's3://bucket/key', 'abfs://container@account.dfs.core.windows.net/path')
            storage_options: Authentication credentials
            **kwargs: Additional arguments
        
        Returns:
            Self for method chaining
        """
        # Determine file type from extension
        path_lower = path.lower()
        
        if path_lower.endswith('.csv'):
            self.data = pd.read_csv(path, storage_options=storage_options, **kwargs)
        elif path_lower.endswith('.parquet'):
            self.data = pd.read_parquet(path, storage_options=storage_options, **kwargs)
        elif path_lower.endswith('.json'):
            self.data = pd.read_json(path, storage_options=storage_options, **kwargs)
        else:
            raise ValueError(f"Unsupported file format for datalake: {path}")
        
        self.source_info = {"type": "datalake", "path": path}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from data lake: {path}")
        return self
    
    def from_dataframe(self, df: pd.DataFrame) -> 'RiskDataConnector':
        """Load data from existing pandas DataFrame"""
        self.data = df.copy()
        self.source_info = {"type": "dataframe"}
        self._detect_schema()
        print(f"✓ Loaded {len(self.data)} rows from DataFrame")
        return self
    
    def _detect_schema(self):
        """Automatically detect and store schema information"""
        if self.data is None:
            return
        
        self.schema = {}
        for col in self.data.columns:
            dtype = str(self.data[col].dtype)
            null_count = self.data[col].isnull().sum()
            unique_count = self.data[col].nunique()
            
            self.schema[col] = {
                "dtype": dtype,
                "null_count": int(null_count),
                "null_pct": float(null_count / len(self.data) * 100),
                "unique_count": int(unique_count),
                "unique_pct": float(unique_count / len(self.data) * 100)
            }
    
    def unify_schema(self, target_schema: Dict[str, str]) -> 'RiskDataConnector':
        """
        Unify data schema to match target schema
        
        Args:
            target_schema: Dictionary mapping column names to target dtypes
        
        Returns:
            Self for method chaining
        """
        if self.data is None:
            raise ValueError("No data loaded. Call a from_* method first.")
        
        for col, dtype in target_schema.items():
            if col in self.data.columns:
                try:
                    if dtype == "int":
                        self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')
                    elif dtype == "float":
                        self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
                    elif dtype == "str":
                        self.data[col] = self.data[col].astype(str)
                    elif dtype == "datetime":
                        self.data[col] = pd.to_datetime(self.data[col], errors='coerce')
                    elif dtype == "bool":
                        self.data[col] = self.data[col].astype(bool)
                except Exception as e:
                    warnings.warn(f"Could not convert {col} to {dtype}: {e}")
        
        self._detect_schema()
        print(f"✓ Schema unified with {len(target_schema)} column conversions")
        return self
    
    def validate_columns(self, required_columns: List[str]) -> bool:
        """
        Validate that required columns exist
        
        Args:
            required_columns: List of required column names
        
        Returns:
            True if all columns present, False otherwise
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        missing = set(required_columns) - set(self.data.columns)
        
        if missing:
            warnings.warn(f"Missing columns: {missing}")
            return False
        
        print(f"✓ All {len(required_columns)} required columns present")
        return True
    
    def merge(self, other: 'RiskDataConnector', on: Union[str, List[str]], 
              how: str = 'inner', **kwargs) -> 'RiskDataConnector':
        """
        Merge with another RiskDataConnector
        
        Args:
            other: Another RiskDataConnector instance
            on: Column(s) to join on
            how: Type of join ('inner', 'left', 'right', 'outer')
            **kwargs: Additional arguments for pd.merge
        
        Returns:
            Self for method chaining
        """
        if self.data is None or other.data is None:
            raise ValueError("Both connectors must have data loaded")
        
        original_rows = len(self.data)
        self.data = pd.merge(self.data, other.data, on=on, how=how, **kwargs)
        self._detect_schema()
        
        print(f"✓ Merged datasets: {original_rows} → {len(self.data)} rows")
        return self
    
    def get_data(self) -> pd.DataFrame:
        """Get the loaded DataFrame"""
        if self.data is None:
            raise ValueError("No data loaded. Call a from_* method first.")
        return self.data
    
    def get_schema(self) -> Dict:
        """Get the detected schema"""
        return self.schema
    
    def summary(self) -> str:
        """Get a summary of the loaded data"""
        if self.data is None:
            return "No data loaded"
        
        lines = []
        lines.append("=" * 60)
        lines.append("RiskX Data Connector Summary")
        lines.append("=" * 60)
        lines.append(f"Source: {self.source_info.get('type', 'unknown')}")
        lines.append(f"Rows: {len(self.data):,}")
        lines.append(f"Columns: {len(self.data.columns)}")
        lines.append("")
        lines.append("Schema:")
        
        for col, info in list(self.schema.items())[:10]:
            lines.append(f"  {col:20} {info['dtype']:12} "
                        f"Nulls: {info['null_pct']:.1f}% "
                        f"Unique: {info['unique_count']}")
        
        if len(self.schema) > 10:
            lines.append(f"  ... and {len(self.schema) - 10} more columns")
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        if self.data is None:
            return "RiskDataConnector(no data loaded)"
        return f"RiskDataConnector({len(self.data)} rows × {len(self.data.columns)} columns)"
