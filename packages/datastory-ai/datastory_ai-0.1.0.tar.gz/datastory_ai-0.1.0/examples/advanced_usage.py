"""
DataStory - Advanced Usage Examples
====================================

Advanced features and customization options.
"""

from datastory import DataStory
import pandas as pd

# Example 1: Detailed Analysis Access
print("=" * 60)
print("Example 1: Access Raw Analysis Results")
print("=" * 60)

story = DataStory()
story.load("sales.csv")

# Get detailed analysis
results = story.analyze()

print("Overview:")
print(f"  Rows: {results['overview']['total_rows']:,}")
print(f"  Columns: {results['overview']['total_columns']}")

print("\nTrends detected:")
for col, trend in results['trends'].items():
    print(f"  {col}: {trend['direction']} ({trend['percentage_change']:.1f}%)")

print("\nCorrelations:")
for corr in results['correlations'].get('strong_correlations', []):
    print(f"  {corr['column1']} <-> {corr['column2']}: {corr['correlation']:.2f}")

# Example 2: Custom Insight Filtering
print("\n" + "=" * 60)
print("Example 2: Filter Insights by Priority")
print("=" * 60)

story = DataStory()
story.load("sales.csv")

insights = story.extract_insights()

# Filter by priority
critical = [i for i in insights if i.priority.value == 1]
high = [i for i in insights if i.priority.value == 2]

print(f"Critical insights: {len(critical)}")
for insight in critical:
    print(f"  🔴 {insight.title}")

print(f"\nHigh-priority insights: {len(high)}")
for insight in high:
    print(f"  🟡 {insight.title}")

# Example 3: Multi-File Analysis
print("\n" + "=" * 60)
print("Example 3: Compare Multiple Datasets")
print("=" * 60)

files = ["sales_q1.csv", "sales_q2.csv", "sales_q3.csv"]

for file in files:
    try:
        story = DataStory(config={"detail_level": "brief"})
        story.load(file)
        narrative = story.generate_narrative()
        print(f"\n{file}:")
        print(narrative[:200] + "...")
    except FileNotFoundError:
        print(f"\n{file}: File not found (skipping)")

# Example 4: Custom Data Preprocessing
print("\n" + "=" * 60)
print("Example 4: Preprocess Data Before Analysis")
print("=" * 60)

# Load and clean data
df = pd.read_csv("sales.csv")

# Custom preprocessing
df = df.dropna()  # Remove missing values
df = df[df['revenue'] > 0]  # Filter valid data
df['month'] = pd.to_datetime(df['month'])  # Convert dates

# Analyze cleaned data
story = DataStory()
story.load(df)
report = story.generate_narrative()
print(report)

# Example 5: Batch Report Generation
print("\n" + "=" * 60)
print("Example 5: Batch Generate Reports")
print("=" * 60)

datasets = {
    "Sales Data": "sales.csv",
    "Customer Churn": "customer_churn.csv",
    "Inventory Status": "inventory.csv"
}

for name, file in datasets.items():
    try:
        print(f"\nProcessing: {name}")
        report = narrate(file, export_path=f"{name.lower().replace(' ', '_')}_report.html")
        print(f"  ✅ Report generated: {name.lower().replace(' ', '_')}_report.html")
    except FileNotFoundError:
        print(f"  ⚠️  File not found: {file}")

# Example 6: Integration with Data Pipeline
print("\n" + "=" * 60)
print("Example 6: Automated Daily Report")
print("=" * 60)

def generate_daily_report(data_source):
    """
    Generate automated daily report.
    
    Args:
        data_source: Path to data file or DataFrame
    
    Returns:
        str: Path to generated report
    """
    from datetime import datetime
    
    # Configure for daily reporting
    config = {
        "style": "business",
        "detail_level": "medium",
        "include_recommendations": True
    }
    
    story = DataStory(config=config)
    story.load(data_source)
    
    # Generate filename with date
    date_str = datetime.now().strftime("%Y%m%d")
    output_path = f"daily_report_{date_str}.html"
    
    story.export(output_path, format="html", include_charts=True)
    
    return output_path

# Simulate daily report
try:
    report_path = generate_daily_report("sales.csv")
    print(f"✅ Daily report generated: {report_path}")
except Exception as e:
    print(f"⚠️  Error: {e}")

print("\n" + "=" * 60)
print("✅ All advanced examples completed!")
print("=" * 60)
