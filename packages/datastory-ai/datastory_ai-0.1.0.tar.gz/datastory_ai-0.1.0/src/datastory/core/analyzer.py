"""
Data Analyzer - Core statistical analysis engine
Performs comprehensive analysis on datasets without external ML libraries
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter


class DataAnalyzer:
    """
    Analyzes datasets to extract statistical insights, trends, and patterns.
    Pure Python implementation with pandas/numpy only.
    """
    
    def __init__(self):
        self.results = {}
    
    def analyze(self, data):
        """
        Perform comprehensive analysis on dataset.
        
        Args:
            data (pd.DataFrame): Input dataset
        
        Returns:
            dict: Analysis results with statistics, trends, patterns
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        
        results = {
            "overview": self._analyze_overview(data),
            "numeric_stats": self._analyze_numeric_columns(data),
            "categorical_stats": self._analyze_categorical_columns(data),
            "temporal_analysis": self._analyze_temporal_patterns(data),
            "correlations": self._find_correlations(data),
            "trends": self._detect_trends(data),
            "anomalies": self._detect_anomalies(data),
            "distributions": self._analyze_distributions(data)
        }
        
        self.results = results
        return results
    
    def _analyze_overview(self, data):
        """Generate dataset overview statistics."""
        return {
            "total_rows": len(data),
            "total_columns": len(data.columns),
            "columns": list(data.columns),
            "memory_usage": data.memory_usage(deep=True).sum(),
            "missing_values": data.isnull().sum().to_dict(),
            "data_types": data.dtypes.astype(str).to_dict(),
            "duplicate_rows": data.duplicated().sum()
        }
    
    def _analyze_numeric_columns(self, data):
        """Analyze numeric columns for statistics."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        stats = {}
        for col in numeric_cols:
            series = data[col].dropna()
            if len(series) == 0:
                continue
            
            stats[col] = {
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "q25": float(series.quantile(0.25)),
                "q75": float(series.quantile(0.75)),
                "sum": float(series.sum()),
                "count": int(series.count()),
                "variance": float(series.var()),
                "skewness": float(series.skew()) if len(series) > 2 else 0,
                "kurtosis": float(series.kurtosis()) if len(series) > 3 else 0
            }
        
        return stats
    
    def _analyze_categorical_columns(self, data):
        """Analyze categorical columns."""
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
        stats = {}
        for col in categorical_cols:
            series = data[col].dropna()
            if len(series) == 0:
                continue
            
            value_counts = series.value_counts()
            stats[col] = {
                "unique_values": int(series.nunique()),
                "most_common": value_counts.head(5).to_dict(),
                "least_common": value_counts.tail(5).to_dict(),
                "mode": str(series.mode()[0]) if len(series.mode()) > 0 else None,
                "diversity": float(series.nunique() / len(series)) if len(series) > 0 else 0
            }
        
        return stats
    
    def _analyze_temporal_patterns(self, data):
        """Detect and analyze time-based patterns."""
        date_cols = data.select_dtypes(include=['datetime64']).columns
        
        # Try to detect date columns that might be stored as strings
        potential_date_cols = []
        for col in data.select_dtypes(include=['object']).columns:
            try:
                pd.to_datetime(data[col].dropna().head(10))
                potential_date_cols.append(col)
            except:
                pass
        
        temporal_stats = {}
        
        for col in list(date_cols) + potential_date_cols:
            try:
                date_series = pd.to_datetime(data[col], errors='coerce').dropna()
                if len(date_series) == 0:
                    continue
                
                temporal_stats[col] = {
                    "earliest": str(date_series.min()),
                    "latest": str(date_series.max()),
                    "span_days": int((date_series.max() - date_series.min()).days),
                    "frequency": self._detect_frequency(date_series)
                }
            except:
                continue
        
        return temporal_stats
    
    def _detect_frequency(self, date_series):
        """Detect frequency of time series data."""
        if len(date_series) < 2:
            return "insufficient_data"
        
        sorted_dates = date_series.sort_values()
        diffs = sorted_dates.diff().dropna()
        
        if len(diffs) == 0:
            return "single_point"
        
        median_diff = diffs.median()
        
        if median_diff <= pd.Timedelta(days=1):
            return "daily"
        elif median_diff <= pd.Timedelta(days=7):
            return "weekly"
        elif median_diff <= pd.Timedelta(days=31):
            return "monthly"
        elif median_diff <= pd.Timedelta(days=92):
            return "quarterly"
        else:
            return "yearly"
    
    def _find_correlations(self, data):
        """Find correlations between numeric columns."""
        numeric_data = data.select_dtypes(include=[np.number])
        
        if numeric_data.shape[1] < 2:
            return {}
        
        corr_matrix = numeric_data.corr()
        
        # Extract strong correlations (absolute value > 0.5)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.5 and not np.isnan(corr_value):
                    strong_correlations.append({
                        "column1": corr_matrix.columns[i],
                        "column2": corr_matrix.columns[j],
                        "correlation": float(corr_value),
                        "strength": "strong" if abs(corr_value) > 0.7 else "moderate"
                    })
        
        return {
            "strong_correlations": strong_correlations,
            "correlation_matrix": corr_matrix.to_dict() if len(corr_matrix) > 0 else {}
        }
    
    def _detect_trends(self, data):
        """Detect trends in numeric columns."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        trends = {}
        for col in numeric_cols:
            series = data[col].dropna()
            if len(series) < 3:
                continue
            
            # Simple trend detection using linear regression
            x = np.arange(len(series))
            y = series.values
            
            # Calculate slope
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
                
                # Calculate percentage change
                start_val = y[0] if y[0] != 0 else 1
                end_val = y[-1]
                pct_change = ((end_val - start_val) / abs(start_val)) * 100
                
                trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
                
                trends[col] = {
                    "direction": trend_direction,
                    "slope": float(slope),
                    "percentage_change": float(pct_change),
                    "start_value": float(start_val),
                    "end_value": float(end_val),
                    "strength": "strong" if abs(pct_change) > 20 else "moderate" if abs(pct_change) > 5 else "weak"
                }
        
        return trends
    
    def _detect_anomalies(self, data):
        """Detect anomalies using IQR method."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        anomalies = {}
        for col in numeric_cols:
            series = data[col].dropna()
            if len(series) < 4:
                continue
            
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = series[(series < lower_bound) | (series > upper_bound)]
            
            if len(outliers) > 0:
                anomalies[col] = {
                    "count": int(len(outliers)),
                    "percentage": float(len(outliers) / len(series) * 100),
                    "values": outliers.head(10).tolist(),
                    "lower_bound": float(lower_bound),
                    "upper_bound": float(upper_bound)
                }
        
        return anomalies
    
    def _analyze_distributions(self, data):
        """Analyze data distributions."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        distributions = {}
        for col in numeric_cols:
            series = data[col].dropna()
            if len(series) < 2:
                continue
            
            # Create histogram bins
            hist, bin_edges = np.histogram(series, bins='auto')
            
            distributions[col] = {
                "histogram_counts": hist.tolist(),
                "bin_edges": bin_edges.tolist(),
                "is_normal": self._test_normality(series),
                "skew_type": "right-skewed" if series.skew() > 0.5 else "left-skewed" if series.skew() < -0.5 else "symmetric"
            }
        
        return distributions
    
    def _test_normality(self, series):
        """Simple normality test based on skewness and kurtosis."""
        if len(series) < 3:
            return False
        
        skewness = abs(series.skew())
        kurtosis = abs(series.kurtosis())
        
        # Rough approximation: normal if skewness < 0.5 and kurtosis < 3
        return skewness < 0.5 and kurtosis < 3
