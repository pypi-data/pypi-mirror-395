"""
Narrative Generator - Converts insights into natural language stories
Pure Python implementation using templates and business language
"""

from typing import List, Dict
from datetime import datetime
import random


class NarrativeGenerator:
    """
    Generates natural language narratives from data insights.
    Uses template-based generation with business terminology.
    """
    
    def __init__(self, config=None):
        """
        Initialize narrative generator.
        
        Args:
            config (dict): Configuration for narrative style, tone, detail level
        """
        self.config = config or {}
        self.style = self.config.get("style", "business")  # business, casual, technical
        self.detail_level = self.config.get("detail_level", "medium")  # brief, medium, detailed
        self.include_recommendations = self.config.get("include_recommendations", True)
        
        # Business terminology templates
        self.trend_verbs = {
            "increasing": ["increased", "grew", "rose", "climbed", "surged", "improved"],
            "decreasing": ["decreased", "declined", "dropped", "fell", "reduced", "weakened"],
            "stable": ["remained stable", "stayed constant", "held steady", "maintained"]
        }
        
        self.impact_adjectives = {
            "high": ["significant", "substantial", "major", "notable", "considerable"],
            "medium": ["moderate", "noticeable", "meaningful", "measurable"],
            "low": ["slight", "minor", "modest", "small"]
        }
    
    def generate(self, insights, data=None):
        """
        Generate complete narrative from insights.
        
        Args:
            insights (list): List of Insight objects
            data (pd.DataFrame): Original dataset (for context)
        
        Returns:
            str: Complete narrative report
        """
        if not insights:
            return "No significant insights were found in the data."
        
        # Build narrative sections
        sections = []
        
        # 1. Executive Summary
        sections.append(self._generate_executive_summary(insights, data))
        
        # 2. Key Findings (group by type)
        sections.append(self._generate_key_findings(insights))
        
        # 3. Detailed Analysis
        if self.detail_level != "brief":
            sections.append(self._generate_detailed_analysis(insights))
        
        # 4. Risks and Opportunities
        risk_insights = [i for i in insights if i.type.value in ["risk", "opportunity"]]
        if risk_insights:
            sections.append(self._generate_risks_opportunities(risk_insights))
        
        # 5. Recommendations
        if self.include_recommendations:
            sections.append(self._generate_recommendations(insights))
        
        # Combine all sections
        narrative = "\n\n".join(filter(None, sections))
        
        return narrative
    
    def _generate_executive_summary(self, insights, data):
        """Generate executive summary section."""
        summary_parts = []
        
        # Header
        summary_parts.append("📊 EXECUTIVE SUMMARY")
        summary_parts.append("=" * 50)
        
        # Dataset overview
        if data is not None:
            rows, cols = data.shape
            summary_parts.append(f"Analyzed {rows:,} records across {cols} dimensions.\n")
        
        # Count insights by priority
        critical = sum(1 for i in insights if i.priority.value == 1)
        high = sum(1 for i in insights if i.priority.value == 2)
        
        # Top 3 insights
        top_insights = insights[:3]
        
        if critical > 0:
            summary_parts.append(f"🔴 {critical} critical finding{'s' if critical != 1 else ''} require immediate attention.")
        if high > 0:
            summary_parts.append(f"🟡 {high} high-priority insight{'s' if high != 1 else ''} identified.")
        
        summary_parts.append("\nKey Highlights:")
        for i, insight in enumerate(top_insights, 1):
            summary_parts.append(f"{i}. {insight.description}")
        
        return "\n".join(summary_parts)
    
    def _generate_key_findings(self, insights):
        """Generate key findings section."""
        findings = []
        
        findings.append("\n📈 KEY FINDINGS")
        findings.append("=" * 50)
        
        # Group insights by type
        trends = [i for i in insights if i.type.value == "trend"]
        anomalies = [i for i in insights if i.type.value == "anomaly"]
        correlations = [i for i in insights if i.type.value == "correlation"]
        
        # Trends
        if trends:
            findings.append("\n**Performance Trends:**")
            for trend in trends[:5]:  # Top 5 trends
                direction = trend.context.get("direction", "")
                verb = random.choice(self.trend_verbs.get(direction, ["changed"]))
                findings.append(f"• {trend.description}")
        
        # Anomalies
        if anomalies:
            findings.append("\n**Notable Anomalies:**")
            for anomaly in anomalies[:3]:  # Top 3 anomalies
                findings.append(f"• {anomaly.description}")
        
        # Correlations
        if correlations:
            findings.append("\n**Relationships Discovered:**")
            for corr in correlations[:3]:  # Top 3 correlations
                findings.append(f"• {corr.description}")
        
        return "\n".join(findings)
    
    def _generate_detailed_analysis(self, insights):
        """Generate detailed analysis section."""
        details = []
        
        details.append("\n🔍 DETAILED ANALYSIS")
        details.append("=" * 50)
        
        # Group by priority
        critical_insights = [i for i in insights if i.priority.value == 1]
        high_insights = [i for i in insights if i.priority.value == 2]
        medium_insights = [i for i in insights if i.priority.value == 3]
        
        if critical_insights:
            details.append("\n**Critical Findings:**")
            for insight in critical_insights:
                details.append(f"\n🔴 {insight.title}")
                details.append(f"   {insight.description}")
                details.append(f"   Impact: Critical - Requires immediate action")
        
        if high_insights:
            details.append("\n**High-Priority Insights:**")
            for insight in high_insights[:5]:  # Top 5
                details.append(f"\n🟡 {insight.title}")
                details.append(f"   {insight.description}")
        
        if self.detail_level == "detailed" and medium_insights:
            details.append("\n**Additional Observations:**")
            for insight in medium_insights[:5]:  # Top 5
                details.append(f"\n🔵 {insight.title}")
                details.append(f"   {insight.description}")
        
        return "\n".join(details)
    
    def _generate_risks_opportunities(self, risk_insights):
        """Generate risks and opportunities section."""
        content = []
        
        content.append("\n⚠️ RISKS & OPPORTUNITIES")
        content.append("=" * 50)
        
        risks = [i for i in risk_insights if i.type.value == "risk"]
        opportunities = [i for i in risk_insights if i.type.value == "opportunity"]
        
        if risks:
            content.append("\n**Identified Risks:**")
            for risk in risks:
                content.append(f"• {risk.description}")
        
        if opportunities:
            content.append("\n**Growth Opportunities:**")
            for opp in opportunities:
                content.append(f"• {opp.description}")
        
        return "\n".join(content)
    
    def _generate_recommendations(self, insights):
        """Generate recommendations based on insights."""
        recommendations = []
        
        recommendations.append("\n💡 RECOMMENDATIONS")
        recommendations.append("=" * 50)
        
        # Generate recommendations based on insight types
        action_items = []
        
        # Trend-based recommendations
        trends = [i for i in insights if i.type.value == "trend" and i.priority.value <= 2]
        for trend in trends[:3]:
            direction = trend.context.get("direction", "")
            column = trend.context.get("column", "metric")
            
            if direction == "decreasing":
                action_items.append(f"Investigate the decline in {column.replace('_', ' ')} and implement recovery strategies")
            elif direction == "increasing":
                action_items.append(f"Capitalize on the growth in {column.replace('_', ' ')} to maximize returns")
        
        # Risk-based recommendations
        risks = [i for i in insights if i.type.value == "risk"]
        for risk in risks:
            risk_type = risk.context.get("risk_type", "")
            if risk_type == "low_stock":
                column = risk.context.get("column", "inventory")
                action_items.append(f"Replenish {column.replace('_', ' ')} to avoid stockouts")
        
        # Anomaly-based recommendations
        anomalies = [i for i in insights if i.type.value == "anomaly" and i.priority.value <= 2]
        for anomaly in anomalies[:2]:
            column = anomaly.context.get("column", "metric")
            action_items.append(f"Review outliers in {column.replace('_', ' ')} to identify root causes")
        
        # Correlation-based recommendations
        correlations = [i for i in insights if i.type.value == "correlation"]
        if correlations:
            action_items.append("Leverage identified relationships between metrics for predictive insights")
        
        # Default recommendations if none generated
        if not action_items:
            action_items = [
                "Continue monitoring key metrics for emerging trends",
                "Establish baseline benchmarks for future comparison",
                "Implement data quality checks to improve analysis accuracy"
            ]
        
        for i, item in enumerate(action_items[:6], 1):  # Top 6 recommendations
            recommendations.append(f"{i}. {item}")
        
        # Footer
        recommendations.append("\n" + "=" * 50)
        recommendations.append(f"Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        recommendations.append("Powered by DataStory - Automatic Storytelling from Data")
        
        return "\n".join(recommendations)
    
    def _format_number(self, number):
        """Format numbers for readability."""
        if abs(number) >= 1_000_000:
            return f"{number / 1_000_000:.1f}M"
        elif abs(number) >= 1_000:
            return f"{number / 1_000:.1f}K"
        else:
            return f"{number:.2f}"
    
    def _choose_verb(self, direction):
        """Choose appropriate verb based on direction."""
        return random.choice(self.trend_verbs.get(direction, ["changed"]))
    
    def _get_impact_adjective(self, magnitude):
        """Get impact adjective based on magnitude."""
        if magnitude > 20:
            level = "high"
        elif magnitude > 10:
            level = "medium"
        else:
            level = "low"
        
        return random.choice(self.impact_adjectives.get(level, ["noticeable"]))
