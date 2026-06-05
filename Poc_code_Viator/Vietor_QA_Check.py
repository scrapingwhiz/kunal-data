import os.path

import pandas as pd
# import numpy as np
from datetime import datetime
# import re
# from collections import Counter
import warnings

warnings.filterwarnings('ignore')


class DataQualityChecker:
    def __init__(self):
        # Define expected headers in exact sequence
        self.expected_headers = [
            'Order', 'Customer Market', 'Customer Market Key', 'Region',
            'Destination Code', 'Destination', 'Service Name', 'Service code',
            'Modality Name', 'Modality Code', 'Modality Order', 'Company',
            'Min pax', 'Booking in advance', 'Search date', 'Calender Week',
            'Arrival date', 'Available Arrival date', 'Price', 'Currency',
            'Deliverable Date', 'Contract Info', 'Incomming Office Code',
            'Transfers- extracted info', 'Transfers - options',
            'Pick up point- extracted info', 'Pick up point- options',
            'Drop off -extracted info', 'Drop off -options',
            'Meals - extracted info', 'Meals : included/ excluded',
            'Start Time', 'End Time', 'Duration', 'Segmentation-duration',
            'Assistance/guided-extracted info', 'Assistance/guided',
            'Language -extracted info', 'Promotion Description',
            'Promotion', 'Supplier', 'Links', 'Modality Availability',
            'Tool Tip', 'Review', 'opiniones', 'Cancelaciones',
            'Mobile Data Information', 'Contractor', 'Product Line', 'Scope','file_name'
        ]

        self.qa_results = {}
        self.data_summary = {}

    def check_headers(self, df):
        """Check if headers match expected sequence"""
        actual_headers = list(df.columns)

        # Check if all expected headers are present
        missing_headers = set(self.expected_headers) - set(actual_headers)
        extra_headers = set(actual_headers) - set(self.expected_headers)

        # Check sequence
        sequence_match = actual_headers == self.expected_headers

        return {
            'total_expected': len(self.expected_headers),
            'total_actual': len(actual_headers),
            'missing_headers': list(missing_headers),
            'extra_headers': list(extra_headers),
            'sequence_match': sequence_match,
            'header_check_passed': len(missing_headers) == 0 and len(extra_headers) == 0 and sequence_match
        }

    def check_data_types(self, df):
        """Validate data types for key columns"""
        type_issues = {}

        # Order should be numeric
        if 'Order' in df.columns:
            non_numeric_orders = df[~df['Order'].astype(str).str.isdigit() | df['Order'].isna()]
            if not non_numeric_orders.empty:
                type_issues['Order'] = f"{len(non_numeric_orders)} non-numeric values"

        # Price should be numeric
        if 'Price' in df.columns:
            try:
                pd.to_numeric(df['Price'], errors='coerce')
                null_prices = df['Price'].isna().sum()
                if null_prices > 0:
                    type_issues['Price'] = f"{null_prices} non-numeric price values"
            except:
                type_issues['Price'] = "Price column contains invalid data types"

        # Date columns validation
        date_columns = ['Search date', 'Arrival date', 'Deliverable Date']
        for col in date_columns:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='coerce')
                    invalid_dates = df[col].isna().sum() if not df[col].isna().all() else len(df)
                    if invalid_dates > 0:
                        type_issues[col] = f"{invalid_dates} invalid date formats"
                except:
                    type_issues[col] = "Contains invalid date formats"

        return type_issues

    def check_mandatory_fields(self, df):
        """Check for missing values in critical fields"""
        mandatory_fields = ['Order', 'Price', 'Currency', 'Company',
                            "Modality Name",
                            "Search date",
                            "Calender Week",
                            "Arrival date",
                            "Currency",
                            ]
        missing_data = {}

        for field in mandatory_fields:
            if field in df.columns:
                missing_count = df[field].isna().sum() + (df[field] == '').sum()
                if missing_count > 0:
                    missing_data[field] = missing_count

        return missing_data

    def check_data_consistency(self, df):
        """Check for data consistency issues"""
        consistency_issues = {}

        # Check if Currency values are valid ISO codes
        if 'Currency' in df.columns:
            valid_currencies = [
                # 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD'
                'GBP', 'EUR', 'AUD', 'USD', 'MXN', 'CAD', 'INR'
            ]
            invalid_currencies = df[~df['Currency'].isin(valid_currencies) & df['Currency'].notna()]
            if not invalid_currencies.empty:
                consistency_issues['Currency'] = f"{len(invalid_currencies)} invalid currency codes"

        # Check price consistency (no negative prices)
        if 'Price' in df.columns:
            try:
                numeric_prices = pd.to_numeric(df['Price'], errors='coerce')
                negative_prices = (numeric_prices < 0).sum()
                if negative_prices > 0:
                    consistency_issues['Price'] = f"{negative_prices} negative price values"
            except:
                pass

        # Check Min pax consistency
        if 'Min pax' in df.columns:
            try:
                numeric_pax = pd.to_numeric(df['Min pax'], errors='coerce')
                invalid_pax = (numeric_pax <= 0).sum()
                if invalid_pax > 0:
                    consistency_issues['Min pax'] = f"{invalid_pax} invalid passenger counts"
            except:
                pass

        # Check Modality Name consistency
        if 'Modality Name' in df.columns:
            try:
                invalid_modality = df['Modality Name'].apply(
                    lambda x: not isinstance(x, str) or len(x.strip()) <= 3
                ).sum()
                invalid_modality_rows = df[
                    df['Modality Name'].apply(lambda x: not isinstance(x, str) or len(x.strip()) <= 7)]
                print(invalid_modality_rows[['Modality Name']])

                if invalid_modality > 0:
                    consistency_issues[
                        'Modality Name'] = f"{invalid_modality} invalid modality names (must be string and length > 10)"
            except Exception as e:
                print("Error checking Modality Name:", e)

        return consistency_issues

    def generate_data_summary(self, df):
        """Generate comprehensive data summary"""
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 ** 2,  # MB
            'duplicate_rows': df.duplicated().sum(),
        }

        # Column-wise statistics
        column_stats = {}
        for col in df.columns:
            stats = {
                'data_type': str(df[col].dtype),
                'null_count': df[col].isna().sum(),
                'null_percentage': (df[col].isna().sum() / len(df)) * 100,
                'unique_values': df[col].nunique(),
            }

            # Add specific stats for numeric columns
            if df[col].dtype in ['int64', 'float64'] or pd.api.types.is_numeric_dtype(df[col]):
                try:
                    numeric_data = pd.to_numeric(df[col], errors='coerce')
                    stats.update({
                        'mean': numeric_data.mean(),
                        'median': numeric_data.median(),
                        'min': numeric_data.min(),
                        'max': numeric_data.max(),
                    })
                except:
                    pass

            column_stats[col] = stats

        summary['column_statistics'] = column_stats

        # Top values for key categorical columns
        categorical_cols = ['Customer Market', 'Currency', 'Company', 'Supplier']
        top_values = {}
        for col in categorical_cols:
            if col in df.columns:
                top_values[col] = df[col].value_counts().head(5).to_dict()

        summary['top_values'] = top_values

        return summary

    def run_qa_check(self, df):
        """Run complete QA check"""
        print("🔍 Starting Data Quality Assessment...")

        # Header validation
        print("📋 Checking headers...")
        self.qa_results['headers'] = self.check_headers(df)

        # Data type validation
        print("🔢 Validating data types...")
        self.qa_results['data_types'] = self.check_data_types(df)

        # Mandatory fields check
        print("⚠️  Checking mandatory fields...")
        self.qa_results['mandatory_fields'] = self.check_mandatory_fields(df)

        # Consistency check
        print("🔄 Checking data consistency...")
        self.qa_results['consistency'] = self.check_data_consistency(df)

        # Generate summary
        print("📊 Generating data summary...")
        self.data_summary = self.generate_data_summary(df)

        print("✅ QA Check completed!")

        return self.qa_results, self.data_summary


def generate_html_report(qa_results, data_summary, df):
    """Generate modern HTML report"""

    # Calculate overall score
    total_checks = 4
    passed_checks = 0

    if qa_results['headers']['header_check_passed']:
        passed_checks += 1
    if len(qa_results['data_types']) == 0:
        passed_checks += 1
    if len(qa_results['mandatory_fields']) == 0:
        passed_checks += 1
    if len(qa_results['consistency']) == 0:
        passed_checks += 1

    overall_score = (passed_checks / total_checks) * 100

    # Status color based on score
    if overall_score >= 80:
        status_color = "#10b981"  # Green
        status_text = "EXCELLENT"
    elif overall_score >= 60:
        status_color = "#f59e0b"  # Yellow
        status_text = "GOOD"
    else:
        status_color = "#ef4444"  # Red
        status_text = "NEEDS ATTENTION"

    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Quality Assessment Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}

            .header {{
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}

            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                font-weight: 700;
            }}

            .header p {{
                font-size: 1.1rem;
                opacity: 0.9;
            }}

            .status-badge {{
                display: inline-block;
                background: {status_color};
                color: white;
                padding: 12px 24px;
                border-radius: 50px;
                font-weight: bold;
                font-size: 1.1rem;
                margin-top: 20px;
            }}

            .content {{
                padding: 40px;
            }}

            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}

            .metric-card {{
                background: #f8fafc;
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                border-left: 5px solid #3b82f6;
            }}

            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                color: #1e40af;
                margin-bottom: 5px;
            }}

            .metric-label {{
                color: #64748b;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .section {{
                margin-bottom: 40px;
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                border: 1px solid #e2e8f0;
            }}

            .section-title {{
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 20px;
                color: #1e40af;
                display: flex;
                align-items: center;
            }}

            .section-title::before {{
                content: "📊";
                margin-right: 10px;
            }}

            .qa-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                margin-bottom: 10px;
                background: #f1f5f9;
                border-radius: 10px;
                border-left: 4px solid #e2e8f0;
            }}

            .qa-item.success {{
                border-left-color: #10b981;
                background: #ecfdf5;
            }}

            .qa-item.error {{
                border-left-color: #ef4444;
                background: #fef2f2;
            }}

            .qa-item.warning {{
                border-left-color: #f59e0b;
                background: #fffbeb;
            }}

            .status-icon {{
                font-size: 1.2rem;
            }}

            .table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            .table th,
            .table td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}

            .table th {{
                background: #f8fafc;
                font-weight: 600;
                color: #475569;
            }}

            .progress-bar {{
                width: 100%;
                height: 20px;
                background: #e2e8f0;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 10px;
            }}

            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, {status_color} 0%, {status_color}dd 100%);
                width: {overall_score}%;
                transition: width 0.3s ease;
            }}

            .footer {{
                background: #f8fafc;
                padding: 30px;
                text-align: center;
                color: #64748b;
                border-top: 1px solid #e2e8f0;
            }}

            .highlight-box {{
                background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
                border: 1px solid #667eea44;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Data Quality Assessment</h1>
                <p>Comprehensive analysis and validation report</p>
                <div class="status-badge">{status_text} - {overall_score:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>

            <div class="content">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{data_summary['total_rows']:,}</div>
                        <div class="metric-label">Total Records</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data_summary['total_columns']}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data_summary['memory_usage']:.1f}MB</div>
                        <div class="metric-label">Memory Usage</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data_summary['duplicate_rows']}</div>
                        <div class="metric-label">Duplicate Records</div>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">Header Validation</div>
                    <div class="qa-item {'success' if qa_results['headers']['header_check_passed'] else 'error'}">
                        <span>Header Structure Check</span>
                        <span class="status-icon">{'✅' if qa_results['headers']['header_check_passed'] else '❌'}</span>
                    </div>
                    <div class="highlight-box">
                        <strong>Expected Headers:</strong> {qa_results['headers']['total_expected']}<br>
                        <strong>Actual Headers:</strong> {qa_results['headers']['total_actual']}<br>
                        <strong>Sequence Match:</strong> {'Yes' if qa_results['headers']['sequence_match'] else 'No'}<br>
    '''

    if qa_results['headers']['missing_headers']:
        html_content += f"<strong>Missing Headers:</strong> {', '.join(qa_results['headers']['missing_headers'])}<br>"

    if qa_results['headers']['extra_headers']:
        html_content += f"<strong>Extra Headers:</strong> {', '.join(qa_results['headers']['extra_headers'])}<br>"

    html_content += '''
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">Data Type Validation</div>
    '''

    if qa_results['data_types']:
        for field, issue in qa_results['data_types'].items():
            html_content += f'''
                    <div class="qa-item error">
                        <span>{field}: {issue}</span>
                        <span class="status-icon">⚠️</span>
                    </div>
            '''
    else:
        html_content += '''
                    <div class="qa-item success">
                        <span>All data types are valid</span>
                        <span class="status-icon">✅</span>
                    </div>
        '''

    html_content += '''
                </div>

                <div class="section">
                    <div class="section-title">Mandatory Fields Check</div>
    '''

    if qa_results['mandatory_fields']:
        for field, count in qa_results['mandatory_fields'].items():
            html_content += f'''
                    <div class="qa-item error">
                        <span>{field}: {count} missing values</span>
                        <span class="status-icon">❌</span>
                    </div>
            '''
    else:
        html_content += '''
                    <div class="qa-item success">
                        <span>All mandatory fields are populated</span>
                        <span class="status-icon">✅</span>
                    </div>
        '''

    html_content += '''
                </div>

                <div class="section">
                    <div class="section-title">Data Consistency Check</div>
    '''

    if qa_results['consistency']:
        for field, issue in qa_results['consistency'].items():
            html_content += f'''
                    <div class="qa-item warning">
                        <span>{field}: {issue}</span>
                        <span class="status-icon">⚠️</span>
                    </div>
            '''
    else:
        html_content += '''
                    <div class="qa-item success">
                        <span>Data consistency checks passed</span>
                        <span class="status-icon">✅</span>
                    </div>
        '''

    # Column Statistics Table
    html_content += '''
                </div>

                <div class="section">
                    <div class="section-title">Column Statistics</div>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Column Name</th>
                                <th>Data Type</th>
                                <th>Null Count</th>
                                <th>Null %</th>
                                <th>Unique Values</th>
                            </tr>
                        </thead>
                        <tbody>
    '''

    for col, stats in data_summary['column_statistics'].items():
        html_content += f'''
                            <tr>
                                <td>{col}</td>
                                <td>{stats['data_type']}</td>
                                <td>{stats['null_count']}</td>
                                <td>{stats['null_percentage']:.1f}%</td>
                                <td>{stats['unique_values']}</td>
                            </tr>
        '''

    html_content += '''
                        </tbody>
                    </table>
                </div>

                <div class="section">
                    <div class="section-title">Top Values Analysis</div>
    '''

    for col, values in data_summary['top_values'].items():
        if values:
            html_content += f'''
                    <div class="highlight-box">
                        <h4>{col}</h4>
                        <ul>
            '''
            for value, count in values.items():
                html_content += f'<li>{value}: {count} records</li>'
            html_content += '''
                        </ul>
                    </div>
            '''

    html_content += f'''
                </div>
            </div>

            <div class="footer">
                <p>Report generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p>Data Quality Assessment Tool v1.0</p>
            </div>
        </div>
    </body>
    </html>
    '''

    return html_content


# Example usage with your data
def main(df, basepath):
    qa_checker = DataQualityChecker()

    # Run QA Check
    qa_results, data_summary = qa_checker.run_qa_check(df)

    # Generate HTML Report
    html_report = generate_html_report(qa_results, data_summary, df)
    path = os.path.join(basepath, 'data_quality_report.html')
    # Save report to file
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_report)

    print("\n" + "=" * 50)
    print("📊 DATA QUALITY ASSESSMENT SUMMARY")
    print("=" * 50)

    # Print summary to console
    print(f"📋 Total Records: {data_summary['total_rows']:,}")
    print(f"📋 Total Columns: {data_summary['total_columns']}")
    print(f"💾 Memory Usage: {data_summary['memory_usage']:.1f}MB")
    print(f"🔄 Duplicate Records: {data_summary['duplicate_rows']}")

    print(f"\n🔍 HEADER VALIDATION:")
    print(f"   ✅ Expected Headers: {qa_results['headers']['total_expected']}")
    print(f"   📊 Actual Headers: {qa_results['headers']['total_actual']}")
    print(f"   🎯 Sequence Match: {'✅ Yes' if qa_results['headers']['sequence_match'] else '❌ No'}")

    if qa_results['headers']['missing_headers']:
        print(f"   ⚠️  Missing Headers: {', '.join(qa_results['headers']['missing_headers'])}")
        return None, None, None

    if qa_results['headers']['extra_headers']:
        print(f"   ⚠️  Extra Headers: {', '.join(qa_results['headers']['extra_headers'])}")
        return None, None, None

    print(f"\n🔢 DATA TYPE ISSUES:")
    if qa_results['data_types']:
        for field, issue in qa_results['data_types'].items():
            print(f"   ❌ {field}: {issue}")
            return None, None, None
    else:
        print("   ✅ No data type issues found")

    print(f"\n⚠️  MANDATORY FIELD ISSUES:")
    if qa_results['mandatory_fields']:
        for field, count in qa_results['mandatory_fields'].items():
            print(f"   ❌ {field}: {count} missing values")
            return None, None, None
    else:
        print("   ✅ All mandatory fields populated")

    print(f"\n🔄 CONSISTENCY ISSUES:")
    if qa_results['consistency']:
        for field, issue in qa_results['consistency'].items():
            print(f"   ⚠️  {field}: {issue}")
            return None, None, None
    else:
        print("   ✅ No consistency issues found")

    # Calculate and display overall score
    total_checks = 4
    passed_checks = 0

    if qa_results['headers']['header_check_passed']:
        passed_checks += 1
    if len(qa_results['data_types']) == 0:
        passed_checks += 1
    if len(qa_results['mandatory_fields']) == 0:
        passed_checks += 1
    if len(qa_results['consistency']) == 0:
        passed_checks += 1

    overall_score = (passed_checks / total_checks) * 100

    print(f"\n🎯 OVERALL QUALITY SCORE: {overall_score:.1f}%")

    if overall_score >= 80:
        print("🎉 EXCELLENT - Data quality is very good!")
    elif overall_score >= 60:
        print("👍 GOOD - Minor issues that should be addressed")
    else:
        print("⚠️  NEEDS ATTENTION - Several data quality issues found")
        return None, None, None

    print(f"\n📄 Detailed HTML report saved as: 'data_quality_report.html'")
    print("=" * 50)

    return qa_results, data_summary, html_report


# Additional utility functions for advanced analysis
def export_issues_to_csv(qa_results, df):
    """Export data quality issues to CSV for easy review"""
    issues_list = []

    # Header issues
    if not qa_results['headers']['header_check_passed']:
        for header in qa_results['headers']['missing_headers']:
            issues_list.append({
                'Issue_Type': 'Missing Header',
                'Field': header,
                'Description': 'Required header is missing',
                'Severity': 'High',
                'Row_Count': 'N/A'
            })

        for header in qa_results['headers']['extra_headers']:
            issues_list.append({
                'Issue_Type': 'Extra Header',
                'Field': header,
                'Description': 'Unexpected header found',
                'Severity': 'Medium',
                'Row_Count': 'N/A'
            })

    # Data type issues
    for field, issue in qa_results['data_types'].items():
        issues_list.append({
            'Issue_Type': 'Data Type',
            'Field': field,
            'Description': issue,
            'Severity': 'High',
            'Row_Count': issue.split()[0] if issue.split()[0].isdigit() else 'N/A'
        })

    # Mandatory field issues
    for field, count in qa_results['mandatory_fields'].items():
        issues_list.append({
            'Issue_Type': 'Missing Data',
            'Field': field,
            'Description': f'{count} missing values in mandatory field',
            'Severity': 'Critical',
            'Row_Count': count
        })

    # Consistency issues
    for field, issue in qa_results['consistency'].items():
        issues_list.append({
            'Issue_Type': 'Consistency',
            'Field': field,
            'Description': issue,
            'Severity': 'Medium',
            'Row_Count': issue.split()[0] if issue.split()[0].isdigit() else 'N/A'
        })

    if issues_list:
        issues_df = pd.DataFrame(issues_list)
        issues_df.to_csv('data_quality_issues.csv', index=False)
        print("📄 Issues exported to 'data_quality_issues.csv'")
        return issues_df
    else:
        print("✅ No issues found to export")
        return None


def generate_recommendations(qa_results, data_summary):
    """Generate actionable recommendations based on QA results"""
    recommendations = []

    # Header recommendations
    if not qa_results['headers']['header_check_passed']:
        recommendations.append({
            'Priority': 'Critical',
            'Category': 'Data Structure',
            'Issue': 'Header structure mismatch',
            'Recommendation': 'Ensure all required headers are present in the exact sequence specified. Missing headers should be added, and extra headers should be reviewed for necessity.',
            'Impact': 'High - Affects data processing and integration'
        })

    # Data type recommendations
    if qa_results['data_types']:
        recommendations.append({
            'Priority': 'High',
            'Category': 'Data Quality',
            'Issue': 'Invalid data types detected',
            'Recommendation': 'Clean and validate data types for numeric and date fields. Implement data validation rules during data entry.',
            'Impact': 'High - Affects calculations and analysis accuracy'
        })

    # Missing data recommendations
    if qa_results['mandatory_fields']:
        recommendations.append({
            'Priority': 'Critical',
            'Category': 'Data Completeness',
            'Issue': 'Missing values in mandatory fields',
            'Recommendation': 'Implement data validation rules to prevent empty mandatory fields. Review data collection processes.',
            'Impact': 'Critical - Essential for business operations'
        })

    # Consistency recommendations
    if qa_results['consistency']:
        recommendations.append({
            'Priority': 'Medium',
            'Category': 'Data Consistency',
            'Issue': 'Data consistency issues found',
            'Recommendation': 'Establish data standards and validation rules. Regular data quality monitoring should be implemented.',
            'Impact': 'Medium - Affects data reliability and reporting'
        })

    # Performance recommendations
    if data_summary['memory_usage'] > 100:  # MB
        recommendations.append({
            'Priority': 'Low',
            'Category': 'Performance',
            'Issue': 'Large memory usage',
            'Recommendation': 'Consider data optimization techniques such as data type optimization or data archiving for older records.',
            'Impact': 'Low - Affects processing performance'
        })

    # Duplicate data recommendations
    if data_summary['duplicate_rows'] > 0:
        recommendations.append({
            'Priority': 'Medium',
            'Category': 'Data Quality',
            'Issue': f"{data_summary['duplicate_rows']} duplicate records found",
            'Recommendation': 'Implement deduplication processes and establish unique key constraints to prevent duplicate entries.',
            'Impact': 'Medium - Affects data accuracy and storage efficiency'
        })

    return recommendations


# Run the complete analysis
if __name__ == "__main__":
    # For your actual data, replace the sample data loading with:
    df = pd.read_excel(r"C:\Users\dev11\Downloads\priceline_code\sample_for_vietor\XWIZ_POC_Viator_Output_29-09-2025.xlsx")
    # C:\Users\dev11\Downloads\priceline_code\sample_for_vietor\XWIZ_Viator.xlsx
    qa_results, data_summary, html_report = main(df)

    # Export issues to CSV
    issues_df = export_issues_to_csv(qa_results, pd.DataFrame(qa_results))

    # Generate recommendations
    recommendations = generate_recommendations(qa_results, data_summary)

    if recommendations:
        print(f"\n💡 RECOMMENDATIONS ({len(recommendations)} items):")
        print("-" * 50)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. [{rec['Priority']}] {rec['Category']}")
            print(f"   Issue: {rec['Issue']}")
            print(f"   Recommendation: {rec['Recommendation']}")
            print(f"   Impact: {rec['Impact']}")
            print()

        # Save recommendations to CSV
        rec_df = pd.DataFrame(recommendations)
        rec_df.to_csv('data_quality_recommendations.csv', index=False)
        print("📄 Recommendations saved to 'data_quality_recommendations.csv'")

    print(f"\n🎊 Analysis Complete! Files generated:")
    print("   • data_quality_report.html (Main Report)")
    print("   • data_quality_issues.csv (Issues List)")
    print("   • data_quality_recommendations.csv (Action Items)")
    print("\n" + "=" * 50)