"""
Data Loader - Loads data from various sources
Supports CSV, Excel, JSON, Parquet, and pandas DataFrames
"""

import pandas as pd
from pathlib import Path
from typing import Union


class DataLoader:
    """
    Loads data from various file formats and sources.
    """
    
    def __init__(self):
        self.supported_formats = {
            '.csv': self._load_csv,
            '.xlsx': self._load_excel,
            '.xls': self._load_excel,
            '.json': self._load_json,
            '.parquet': self._load_parquet,
            '.pq': self._load_parquet
        }
    
    def load(self, source, **kwargs):
        """
        Load data from various sources.
        
        Args:
            source: File path (str/Path), URL (str), or pandas DataFrame
            **kwargs: Additional parameters for specific loaders
        
        Returns:
            pd.DataFrame: Loaded dataset
        
        Raises:
            ValueError: If source type is not supported
            FileNotFoundError: If file doesn't exist
        """
        # If already a DataFrame, return it
        if isinstance(source, pd.DataFrame):
            return source
        
        # Convert to Path if string
        if isinstance(source, str):
            # Check if it's a URL
            if source.startswith(('http://', 'https://')):
                return self._load_from_url(source, **kwargs)
            
            source = Path(source)
        
        # Check if file exists
        if not source.exists():
            raise FileNotFoundError(f"File not found: {source}")
        
        # Get file extension
        extension = source.suffix.lower()
        
        # Load based on extension
        if extension in self.supported_formats:
            return self.supported_formats[extension](source, **kwargs)
        else:
            # Try to infer from content
            return self._load_with_inference(source, **kwargs)
    
    def _load_csv(self, filepath, **kwargs):
        """Load CSV file."""
        # Set sensible defaults
        kwargs.setdefault('encoding', 'utf-8-sig')  # Handle BOM
        
        try:
            df = pd.read_csv(filepath, **kwargs)
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    df = pd.read_csv(filepath, encoding=encoding, **kwargs)
                    break
                except:
                    continue
            else:
                raise
        
        return self._postprocess(df)
    
    def _load_excel(self, filepath, **kwargs):
        """Load Excel file."""
        df = pd.read_excel(filepath, **kwargs)
        return self._postprocess(df)
    
    def _load_json(self, filepath, **kwargs):
        """Load JSON file."""
        # Try different orientations
        try:
            df = pd.read_json(filepath, **kwargs)
        except ValueError:
            # Try with lines=True for JSONL format
            try:
                df = pd.read_json(filepath, lines=True, **kwargs)
            except:
                # Try reading as regular JSON and converting
                import json
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                df = pd.DataFrame(data)
        
        return self._postprocess(df)
    
    def _load_parquet(self, filepath, **kwargs):
        """Load Parquet file."""
        df = pd.read_parquet(filepath, **kwargs)
        return self._postprocess(df)
    
    def _load_from_url(self, url, **kwargs):
        """Load data from URL."""
        # Infer format from URL
        if '.csv' in url.lower():
            df = pd.read_csv(url, **kwargs)
        elif '.json' in url.lower():
            df = pd.read_json(url, **kwargs)
        elif any(ext in url.lower() for ext in ['.xlsx', '.xls']):
            df = pd.read_excel(url, **kwargs)
        else:
            # Default to CSV
            df = pd.read_csv(url, **kwargs)
        
        return self._postprocess(df)
    
    def _load_with_inference(self, filepath, **kwargs):
        """Try to load file by inferring format from content."""
        # Try CSV first (most common)
        try:
            return self._load_csv(filepath, **kwargs)
        except:
            pass
        
        # Try JSON
        try:
            return self._load_json(filepath, **kwargs)
        except:
            pass
        
        raise ValueError(f"Unable to load file: {filepath}. Format not recognized.")
    
    def _postprocess(self, df):
        """
        Post-process loaded DataFrame.
        - Auto-detect and convert date columns
        - Strip whitespace from string columns
        - Convert numeric strings to numbers
        """
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Try to convert object columns to better types
        for col in df.select_dtypes(include=['object']).columns:
            # Strip whitespace from strings
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip() if hasattr(df[col].str, 'strip') else df[col]
            
            # Try to convert to numeric
            try:
                numeric_col = pd.to_numeric(df[col], errors='coerce')
                # If most values convert successfully, use numeric
                if numeric_col.notna().sum() / len(df) > 0.5:
                    df[col] = numeric_col
                    continue
            except:
                pass
            
            # Try to convert to datetime
            try:
                date_col = pd.to_datetime(df[col], errors='coerce')
                # If most values convert successfully, use datetime
                if date_col.notna().sum() / len(df) > 0.5:
                    df[col] = date_col
            except:
                pass
        
        return df
    
    def get_supported_formats(self):
        """Get list of supported file formats."""
        return list(self.supported_formats.keys())
