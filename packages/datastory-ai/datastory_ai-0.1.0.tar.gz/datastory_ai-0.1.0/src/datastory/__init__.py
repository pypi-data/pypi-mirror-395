"""
DataStory - Automatic Storytelling from Data
============================================

Transform raw data into compelling business narratives automatically.

Basic Usage:
    >>> from datastory import narrate
    >>> report = narrate("sales.csv")
    >>> print(report)

Advanced Usage:
    >>> from datastory import DataStory
    >>> story = DataStory()
    >>> story.load("sales.csv")
    >>> insights = story.analyze()
    >>> narrative = story.generate_narrative()
    >>> story.export("report.pdf")

Author: Idriss Bado
License: MIT
Version: 0.1.0
"""

from .core.analyzer import DataAnalyzer
from .core.insights import InsightExtractor
from .narration.generator import NarrativeGenerator
from .loaders.data_loader import DataLoader
from .formatters.report_formatter import ReportFormatter

__version__ = "0.1.0"
__author__ = "Idriss Bado"
__all__ = ["narrate", "DataStory", "DataAnalyzer", "InsightExtractor", "NarrativeGenerator"]


class DataStory:
    """
    Main DataStory class for generating narrative reports from data.
    
    Example:
        >>> story = DataStory()
        >>> story.load("sales.csv")
        >>> narrative = story.generate_narrative()
        >>> print(narrative)
    """
    
    def __init__(self, config=None):
        """
        Initialize DataStory instance.
        
        Args:
            config (dict, optional): Configuration options for analysis and narrative style
        """
        self.config = config or {}
        self.loader = DataLoader()
        self.analyzer = DataAnalyzer()
        self.insight_extractor = InsightExtractor()
        self.narrative_generator = NarrativeGenerator(config)
        self.formatter = ReportFormatter()
        
        self.data = None
        self.analysis_results = None
        self.insights = None
        self.narrative = None
    
    def load(self, source, **kwargs):
        """
        Load data from various sources (CSV, Excel, JSON, DataFrame, etc.).
        
        Args:
            source: File path, URL, or pandas DataFrame
            **kwargs: Additional loading options
        
        Returns:
            self: For method chaining
        """
        self.data = self.loader.load(source, **kwargs)
        return self
    
    def analyze(self):
        """
        Perform comprehensive data analysis.
        
        Returns:
            dict: Analysis results including statistics, trends, patterns
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load() first.")
        
        self.analysis_results = self.analyzer.analyze(self.data)
        return self.analysis_results
    
    def extract_insights(self):
        """
        Extract meaningful insights from analysis results.
        
        Returns:
            list: List of Insight objects
        """
        if self.analysis_results is None:
            self.analyze()
        
        self.insights = self.insight_extractor.extract(self.data, self.analysis_results)
        return self.insights
    
    def generate_narrative(self):
        """
        Generate natural language narrative from insights.
        
        Returns:
            str: Complete narrative report
        """
        if self.insights is None:
            self.extract_insights()
        
        self.narrative = self.narrative_generator.generate(self.insights, self.data)
        return self.narrative
    
    def export(self, output_path, format="auto", include_charts=True):
        """
        Export narrative report to file.
        
        Args:
            output_path (str): Output file path
            format (str): Output format (auto, text, markdown, html, pdf)
            include_charts (bool): Include visualizations in report
        
        Returns:
            str: Path to exported file
        """
        if self.narrative is None:
            self.generate_narrative()
        
        return self.formatter.export(
            narrative=self.narrative,
            insights=self.insights,
            data=self.data,
            output_path=output_path,
            format=format,
            include_charts=include_charts
        )
    
    def __repr__(self):
        data_info = f"{len(self.data)} rows" if self.data is not None else "no data"
        insight_count = len(self.insights) if self.insights else 0
        return f"DataStory({data_info}, {insight_count} insights)"


def narrate(source, output_format="text", export_path=None, **kwargs):
    """
    One-line function to generate narrative from data.
    
    This is the simplest way to use DataStory:
    
    Example:
        >>> report = narrate("sales.csv")
        >>> print(report)
    
    Args:
        source: Data source (file path, URL, or DataFrame)
        output_format (str): Output format (text, markdown, html, pdf)
        export_path (str, optional): Save report to this path
        **kwargs: Additional configuration options
    
    Returns:
        str: Generated narrative report
    """
    story = DataStory(config=kwargs)
    story.load(source)
    narrative = story.generate_narrative()
    
    if export_path:
        story.export(export_path, format=output_format)
    
    return narrative
