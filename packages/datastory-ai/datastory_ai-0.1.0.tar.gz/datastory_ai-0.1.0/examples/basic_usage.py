"""
DataStory - Basic Usage Examples
=================================

Simple examples to get started with DataStory.
"""

# Example 1: One-Line Analysis
print("=" * 60)
print("Example 1: One-Line Analysis")
print("=" * 60)

from datastory import narrate

# Generate report from CSV file
report = narrate("sales.csv")
print(report)

# Example 2: Load and Analyze
print("\n" + "=" * 60)
print("Example 2: Step-by-Step Analysis")
print("=" * 60)

from datastory import DataStory

story = DataStory()
story.load("sales.csv")

# Get insights
insights = story.extract_insights()
print(f"Found {len(insights)} insights")

# Generate narrative
narrative = story.generate_narrative()
print(narrative)

# Example 3: Custom Configuration
print("\n" + "=" * 60)
print("Example 3: Custom Configuration")
print("=" * 60)

config = {
    "style": "business",
    "detail_level": "brief",
    "include_recommendations": True
}

story = DataStory(config=config)
story.load("sales.csv")
report = story.generate_narrative()
print(report)

# Example 4: Export to Different Formats
print("\n" + "=" * 60)
print("Example 4: Export Reports")
print("=" * 60)

story = DataStory()
story.load("sales.csv")
story.generate_narrative()

# Export to multiple formats
story.export("report.txt", format="text")
story.export("report.md", format="markdown")
story.export("report.html", format="html", include_charts=True)

print("✅ Reports exported successfully!")
print("  - report.txt")
print("  - report.md")
print("  - report.html")

# Example 5: Working with DataFrames
print("\n" + "=" * 60)
print("Example 5: Pandas DataFrame")
print("=" * 60)

import pandas as pd

# Create sample data
data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    'revenue': [100000, 120000, 115000, 140000, 155000],
    'customers': [250, 280, 265, 310, 330],
    'churn_rate': [5.2, 4.8, 5.5, 6.1, 5.0]
}

df = pd.DataFrame(data)

# Analyze DataFrame directly
story = DataStory()
story.load(df)
report = story.generate_narrative()
print(report)

print("\n" + "=" * 60)
print("✅ All examples completed!")
print("=" * 60)
