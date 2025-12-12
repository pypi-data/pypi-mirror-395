"""
Report Formatter - Exports narratives to various formats
Supports text, markdown, HTML, and PDF output
"""

from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO


class ReportFormatter:
    """
    Formats and exports narrative reports to various formats.
    """
    
    def __init__(self):
        self.format_handlers = {
            'text': self._export_text,
            'txt': self._export_text,
            'markdown': self._export_markdown,
            'md': self._export_markdown,
            'html': self._export_html,
            'pdf': self._export_pdf
        }
    
    def export(self, narrative, insights, data, output_path, format="auto", include_charts=True):
        """
        Export narrative report to file.
        
        Args:
            narrative (str): Generated narrative text
            insights (list): List of Insight objects
            data (pd.DataFrame): Original dataset
            output_path (str): Output file path
            format (str): Output format (auto, text, markdown, html, pdf)
            include_charts (bool): Include visualizations
        
        Returns:
            str: Path to exported file
        """
        output_path = Path(output_path)
        
        # Auto-detect format from extension
        if format == "auto":
            format = output_path.suffix.lower().lstrip('.')
            if not format:
                format = "text"
        
        # Get appropriate handler
        handler = self.format_handlers.get(format, self._export_text)
        
        # Export
        handler(narrative, insights, data, output_path, include_charts)
        
        return str(output_path)
    
    def _export_text(self, narrative, insights, data, output_path, include_charts):
        """Export as plain text."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(narrative)
            
            if include_charts:
                f.write("\n\n" + "=" * 50)
                f.write("\nNote: Charts are not available in text format.")
                f.write("\nExport to HTML or PDF for visual representations.")
    
    def _export_markdown(self, narrative, insights, data, output_path, include_charts):
        """Export as Markdown."""
        markdown_content = []
        
        # Title
        markdown_content.append("# DataStory Report\n")
        markdown_content.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n")
        markdown_content.append("---\n")
        
        # Convert narrative (already has some markdown-like formatting)
        markdown_content.append(narrative)
        
        # Add summary table if data is available
        if data is not None and include_charts:
            markdown_content.append("\n\n## Data Summary\n")
            markdown_content.append(f"- **Total Records**: {len(data):,}")
            markdown_content.append(f"- **Total Columns**: {len(data.columns)}")
            markdown_content.append(f"- **Insights Found**: {len(insights)}\n")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
    
    def _export_html(self, narrative, insights, data, output_path, include_charts):
        """Export as HTML with styling."""
        html_parts = []
        
        # HTML header with CSS
        html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DataStory Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .summary {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .insight {
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #3498db;
            background: #f8f9fa;
        }
        .critical { border-left-color: #e74c3c; }
        .high { border-left-color: #f39c12; }
        .medium { border-left-color: #3498db; }
        .low { border-left-color: #95a5a6; }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
        }
        .emoji { font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 DataStory Report</h1>
        <p><em>Generated on {date}</em></p>
        """.format(date=datetime.now().strftime('%B %d, %Y at %I:%M %p')))
        
        # Convert narrative to HTML
        narrative_html = self._convert_narrative_to_html(narrative)
        html_parts.append(narrative_html)
        
        # Add insights summary table
        if data is not None:
            html_parts.append("""
        <div class="summary">
            <h3>Dataset Overview</h3>
            <ul>
                <li><strong>Total Records:</strong> {rows:,}</li>
                <li><strong>Total Columns:</strong> {cols}</li>
                <li><strong>Insights Generated:</strong> {insights}</li>
            </ul>
        </div>
            """.format(rows=len(data), cols=len(data.columns), insights=len(insights)))
        
        # Add charts if requested
        if include_charts and data is not None:
            try:
                chart_html = self._generate_charts(data, insights)
                html_parts.append(chart_html)
            except Exception as e:
                html_parts.append(f'<p><em>Chart generation skipped: {str(e)}</em></p>')
        
        # Footer
        html_parts.append("""
        <div class="footer">
            <p>Powered by <strong>DataStory</strong> - Automatic Storytelling from Data</p>
            <p>Built by Idriss Bado</p>
        </div>
    </div>
</body>
</html>
        """)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))
    
    def _convert_narrative_to_html(self, narrative):
        """Convert plain narrative text to HTML."""
        html_lines = []
        
        for line in narrative.split('\n'):
            line = line.strip()
            
            if not line:
                continue
            
            # Headers (lines with === or --- underneath)
            if '===' in line or '---' in line:
                continue
            
            # Section headers (lines with emojis)
            if any(emoji in line for emoji in ['📊', '📈', '🔍', '⚠️', '💡']):
                html_lines.append(f'<h2>{line}</h2>')
            
            # Bold text (lines starting with **)
            elif line.startswith('**') and line.endswith('**'):
                html_lines.append(f'<h3>{line.strip("*")}</h3>')
            
            # List items
            elif line.startswith('•') or line.startswith('-'):
                html_lines.append(f'<li>{line.lstrip("•- ")}</li>')
            
            # Numbered items
            elif len(line) > 2 and line[0].isdigit() and line[1] == '.':
                html_lines.append(f'<li>{line.split(". ", 1)[1] if ". " in line else line}</li>')
            
            # Indicators
            elif line.startswith('🔴') or line.startswith('🟡') or line.startswith('🔵'):
                html_lines.append(f'<div class="insight">{line}</div>')
            
            # Regular paragraphs
            else:
                html_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(html_lines)
    
    def _generate_charts(self, data, insights):
        """Generate simple charts for HTML export."""
        chart_html = ['<h2>📊 Visual Summary</h2>']
        
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            
            # Create a simple chart
            numeric_cols = data.select_dtypes(include=['number']).columns[:4]  # Top 4
            
            if len(numeric_cols) > 0:
                fig, axes = plt.subplots(1, min(len(numeric_cols), 2), figsize=(12, 4))
                if len(numeric_cols) == 1:
                    axes = [axes]
                
                for idx, col in enumerate(numeric_cols[:2]):
                    ax = axes[idx] if len(numeric_cols) > 1 else axes[0]
                    data[col].plot(kind='hist', ax=ax, title=f'{col} Distribution', bins=20)
                    ax.set_ylabel('Frequency')
                
                plt.tight_layout()
                
                # Convert to base64
                buffer = BytesIO()
                plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode()
                plt.close()
                
                chart_html.append(f'<div class="chart-container">')
                chart_html.append(f'<img src="data:image/png;base64,{image_base64}" alt="Data Distribution" style="max-width: 100%;"/>')
                chart_html.append('</div>')
        
        except ImportError:
            chart_html.append('<p><em>Install matplotlib for chart generation: pip install matplotlib</em></p>')
        except Exception as e:
            chart_html.append(f'<p><em>Chart generation error: {str(e)}</em></p>')
        
        return '\n'.join(chart_html)
    
    def _export_pdf(self, narrative, insights, data, output_path, include_charts):
        """Export as PDF (requires additional libraries)."""
        try:
            # Try to use reportlab
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            doc = SimpleDocTemplate(str(output_path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("DataStory Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Content
            for line in narrative.split('\n'):
                if line.strip():
                    p = Paragraph(line, styles['Normal'])
                    story.append(p)
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            
        except ImportError:
            # Fallback: create HTML and suggest conversion
            html_path = output_path.with_suffix('.html')
            self._export_html(narrative, insights, data, html_path, include_charts)
            
            message = f"""PDF export requires additional libraries.

Options:
1. Install reportlab: pip install reportlab
2. Use the generated HTML file: {html_path}
3. Convert HTML to PDF using browser's print function

The report has been saved as HTML instead: {html_path}
"""
            print(message)
            
            # Also save instructions
            with open(output_path.with_suffix('.txt'), 'w') as f:
                f.write(message)
