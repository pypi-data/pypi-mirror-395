"""
Insight Extractor - Converts analysis results into actionable insights
"""

import pandas as pd
from typing import List, Dict, Any
from enum import Enum


class InsightType(Enum):
    """Types of insights that can be extracted."""
    TREND = "trend"
    ANOMALY = "anomaly"
    CORRELATION = "correlation"
    COMPARISON = "comparison"
    SUMMARY = "summary"
    RISK = "risk"
    OPPORTUNITY = "opportunity"


class InsightPriority(Enum):
    """Priority levels for insights."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class Insight:
    """Represents a single data insight."""
    
    def __init__(self, insight_type, title, description, priority=InsightPriority.MEDIUM, 
                 data=None, context=None):
        """
        Create a new insight.
        
        Args:
            insight_type (InsightType): Type of insight
            title (str): Short insight title
            description (str): Detailed description
            priority (InsightPriority): Importance level
            data (dict): Supporting data
            context (dict): Additional context
        """
        self.type = insight_type
        self.title = title
        self.description = description
        self.priority = priority
        self.data = data or {}
        self.context = context or {}
    
    def __repr__(self):
        return f"Insight({self.type.value}, priority={self.priority.value}, title='{self.title}')"
    
    def to_dict(self):
        """Convert insight to dictionary."""
        return {
            "type": self.type.value,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "data": self.data,
            "context": self.context
        }


class InsightExtractor:
    """
    Extracts meaningful business insights from analysis results.
    """
    
    def __init__(self):
        self.insights = []
    
    def extract(self, data, analysis_results):
        """
        Extract insights from analysis results.
        
        Args:
            data (pd.DataFrame): Original dataset
            analysis_results (dict): Results from DataAnalyzer
        
        Returns:
            list: List of Insight objects
        """
        self.insights = []
        
        # Extract different types of insights
        self._extract_trend_insights(analysis_results.get("trends", {}))
        self._extract_anomaly_insights(analysis_results.get("anomalies", {}))
        self._extract_correlation_insights(analysis_results.get("correlations", {}))
        self._extract_summary_insights(data, analysis_results.get("overview", {}))
        self._extract_numeric_insights(analysis_results.get("numeric_stats", {}))
        self._extract_categorical_insights(analysis_results.get("categorical_stats", {}))
        self._extract_temporal_insights(analysis_results.get("temporal_analysis", {}))
        self._extract_risk_insights(data, analysis_results)
        
        # Sort by priority
        self.insights.sort(key=lambda x: x.priority.value)
        
        return self.insights
    
    def _extract_trend_insights(self, trends):
        """Extract insights from trend analysis."""
        for column, trend_data in trends.items():
            pct_change = trend_data.get("percentage_change", 0)
            direction = trend_data.get("direction", "stable")
            strength = trend_data.get("strength", "weak")
            
            if abs(pct_change) > 10:  # Significant change
                priority = InsightPriority.HIGH if abs(pct_change) > 20 else InsightPriority.MEDIUM
                
                if direction == "increasing":
                    title = f"{column.replace('_', ' ').title()} Shows Strong Growth"
                    description = f"{column.replace('_', ' ').title()} increased by {abs(pct_change):.1f}% from {trend_data['start_value']:.2f} to {trend_data['end_value']:.2f}."
                elif direction == "decreasing":
                    title = f"{column.replace('_', ' ').title()} Declining"
                    description = f"{column.replace('_', ' ').title()} decreased by {abs(pct_change):.1f}% from {trend_data['start_value']:.2f} to {trend_data['end_value']:.2f}."
                else:
                    continue
                
                self.insights.append(Insight(
                    insight_type=InsightType.TREND,
                    title=title,
                    description=description,
                    priority=priority,
                    data=trend_data,
                    context={"column": column, "direction": direction, "strength": strength}
                ))
    
    def _extract_anomaly_insights(self, anomalies):
        """Extract insights from anomaly detection."""
        for column, anomaly_data in anomalies.items():
            count = anomaly_data.get("count", 0)
            percentage = anomaly_data.get("percentage", 0)
            
            if count > 0:
                priority = InsightPriority.HIGH if percentage > 5 else InsightPriority.MEDIUM
                
                title = f"Unusual Values Detected in {column.replace('_', ' ').title()}"
                description = f"Found {count} outliers ({percentage:.1f}% of data) in {column.replace('_', ' ').title()}. These values fall outside the normal range."
                
                self.insights.append(Insight(
                    insight_type=InsightType.ANOMALY,
                    title=title,
                    description=description,
                    priority=priority,
                    data=anomaly_data,
                    context={"column": column, "outlier_count": count}
                ))
    
    def _extract_correlation_insights(self, correlations):
        """Extract insights from correlation analysis."""
        strong_corrs = correlations.get("strong_correlations", [])
        
        for corr in strong_corrs[:5]:  # Top 5 correlations
            col1 = corr["column1"]
            col2 = corr["column2"]
            corr_value = corr["correlation"]
            
            priority = InsightPriority.MEDIUM
            
            if corr_value > 0:
                title = f"Strong Positive Link: {col1.replace('_', ' ').title()} and {col2.replace('_', ' ').title()}"
                description = f"{col1.replace('_', ' ').title()} and {col2.replace('_', ' ').title()} move together (correlation: {corr_value:.2f}). When one increases, the other tends to increase."
            else:
                title = f"Inverse Relationship: {col1.replace('_', ' ').title()} vs {col2.replace('_', ' ').title()}"
                description = f"{col1.replace('_', ' ').title()} and {col2.replace('_', ' ').title()} move in opposite directions (correlation: {corr_value:.2f}). When one increases, the other tends to decrease."
            
            self.insights.append(Insight(
                insight_type=InsightType.CORRELATION,
                title=title,
                description=description,
                priority=priority,
                data=corr,
                context={"columns": [col1, col2]}
            ))
    
    def _extract_summary_insights(self, data, overview):
        """Extract high-level summary insights."""
        total_rows = overview.get("total_rows", 0)
        total_cols = overview.get("total_columns", 0)
        missing = overview.get("missing_values", {})
        
        # Data completeness insight
        total_missing = sum(missing.values())
        total_cells = total_rows * total_cols
        
        if total_cells > 0:
            completeness = ((total_cells - total_missing) / total_cells) * 100
            
            if completeness < 95:
                priority = InsightPriority.HIGH if completeness < 80 else InsightPriority.MEDIUM
                
                title = "Data Completeness Issue"
                description = f"Dataset is {completeness:.1f}% complete. {total_missing:,} missing values detected across {total_cols} columns."
                
                self.insights.append(Insight(
                    insight_type=InsightType.SUMMARY,
                    title=title,
                    description=description,
                    priority=priority,
                    data={"completeness": completeness, "missing_count": total_missing},
                    context={"total_rows": total_rows, "total_columns": total_cols}
                ))
    
    def _extract_numeric_insights(self, numeric_stats):
        """Extract insights from numeric statistics."""
        for column, stats in numeric_stats.items():
            mean_val = stats.get("mean", 0)
            std_val = stats.get("std", 0)
            
            # High variability insight
            if std_val > 0 and mean_val != 0:
                cv = (std_val / abs(mean_val)) * 100  # Coefficient of variation
                
                if cv > 50:  # High variability
                    title = f"High Variability in {column.replace('_', ' ').title()}"
                    description = f"{column.replace('_', ' ').title()} shows high variability (CV: {cv:.1f}%). Values range from {stats['min']:.2f} to {stats['max']:.2f} with mean {mean_val:.2f}."
                    
                    self.insights.append(Insight(
                        insight_type=InsightType.SUMMARY,
                        title=title,
                        description=description,
                        priority=InsightPriority.LOW,
                        data=stats,
                        context={"column": column, "variability": "high"}
                    ))
    
    def _extract_categorical_insights(self, categorical_stats):
        """Extract insights from categorical data."""
        for column, stats in categorical_stats.items():
            unique_count = stats.get("unique_values", 0)
            most_common = stats.get("most_common", {})
            
            if most_common:
                top_category = list(most_common.keys())[0]
                top_count = list(most_common.values())[0]
                total = sum(most_common.values())
                
                if total > 0:
                    percentage = (top_count / total) * 100
                    
                    if percentage > 50:  # Dominant category
                        title = f"Dominant Category in {column.replace('_', ' ').title()}"
                        description = f"'{top_category}' dominates {column.replace('_', ' ').title()}, accounting for {percentage:.1f}% of all values."
                        
                        self.insights.append(Insight(
                            insight_type=InsightType.SUMMARY,
                            title=title,
                            description=description,
                            priority=InsightPriority.LOW,
                            data={"category": top_category, "percentage": percentage},
                            context={"column": column}
                        ))
    
    def _extract_temporal_insights(self, temporal_analysis):
        """Extract insights from temporal patterns."""
        for column, temporal_data in temporal_analysis.items():
            span_days = temporal_data.get("span_days", 0)
            frequency = temporal_data.get("frequency", "unknown")
            
            if span_days > 0:
                title = f"Time Coverage: {column.replace('_', ' ').title()}"
                
                if span_days < 30:
                    period = f"{span_days} days"
                elif span_days < 365:
                    period = f"{span_days / 30:.1f} months"
                else:
                    period = f"{span_days / 365:.1f} years"
                
                description = f"Data spans {period} from {temporal_data['earliest']} to {temporal_data['latest']}. Frequency: {frequency}."
                
                self.insights.append(Insight(
                    insight_type=InsightType.SUMMARY,
                    title=title,
                    description=description,
                    priority=InsightPriority.LOW,
                    data=temporal_data,
                    context={"column": column, "span": period}
                ))
    
    def _extract_risk_insights(self, data, analysis_results):
        """Extract risk-related insights."""
        numeric_stats = analysis_results.get("numeric_stats", {})
        
        # Check for columns that might indicate inventory/stock
        risk_keywords = ["stock", "inventory", "quantity", "balance", "available"]
        
        for column in data.columns:
            col_lower = column.lower()
            if any(keyword in col_lower for keyword in risk_keywords):
                if column in numeric_stats:
                    stats = numeric_stats[column]
                    min_val = stats.get("min", 0)
                    mean_val = stats.get("mean", 0)
                    
                    # Low stock warning
                    if min_val < mean_val * 0.2:  # Less than 20% of mean
                        title = f"Low Stock Risk: {column.replace('_', ' ').title()}"
                        description = f"Minimum {column.replace('_', ' ').lower()} is {min_val:.2f}, significantly below average of {mean_val:.2f}. Consider restocking."
                        
                        self.insights.append(Insight(
                            insight_type=InsightType.RISK,
                            title=title,
                            description=description,
                            priority=InsightPriority.HIGH,
                            data={"min": min_val, "mean": mean_val},
                            context={"column": column, "risk_type": "low_stock"}
                        ))
