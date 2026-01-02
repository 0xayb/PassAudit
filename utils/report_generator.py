import json
import csv
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    
    def __init__(self):
        self.report_count = 0
    
    def export(self, result: Dict, output_path: str) -> None:
        path = Path(output_path)
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['report_version'] = '2.0'
        
        if path.suffix == '.json':
            self._export_json(result, path)
        elif path.suffix == '.csv':
            self._export_csv([result], path)
        else:
            raise ValueError("Output format must be .json or .csv")
        
        self.report_count += 1
    
    def export_batch(self, results: List[Dict], output_path: str) -> None:
        path = Path(output_path)
        
        # Add metadata to each result
        timestamp = datetime.now().isoformat()
        for result in results:
            result['timestamp'] = timestamp
            result['report_version'] = '2.0'
        
        if path.suffix == '.json':
            self._export_json_batch(results, path)
        elif path.suffix == '.csv':
            self._export_csv(results, path)
        else:
            raise ValueError("Output format must be .json or .csv")
        
        self.report_count += 1
    
    def _export_json(self, result: Dict, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    
    def _export_json_batch(self, results: List[Dict], path: Path) -> None:
        # Calculate summary statistics
        summary = self._calculate_summary(results)
        
        output = {
            'summary': summary,
            'results': results
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, results: List[Dict], path: Path) -> None:
        # Define fields to export (flatten the complex structure)
        fieldnames = [
            'password',
            'password_length',
            'score',
            'is_common',
            'entropy',
            'hash',
            'timestamp'
        ]
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for result in results:
                # Create a flattened row
                row = {
                    'password': result.get('password', '[hidden]'),
                    'password_length': result.get('password_length', 0),
                    'score': result.get('score', 0),
                    'is_common': result.get('is_common', False),
                    'entropy': f"{result.get('entropy', 0):.1f}",
                    'hash': result.get('hash', ''),
                    'timestamp': result.get('timestamp', '')
                }
                writer.writerow(row)
    
    def _calculate_summary(self, results: List[Dict]) -> Dict:
        if not results:
            return {}
        
        total = len(results)
        
        # Score distribution
        score_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for result in results:
            score = result.get('score', 0)
            score_counts[score] = score_counts.get(score, 0) + 1
        
        # Common passwords
        common_count = sum(1 for r in results if r.get('is_common', False))
        
        # Average metrics
        avg_length = sum(r.get('password_length', 0) for r in results) / total
        avg_entropy = sum(r.get('entropy', 0) for r in results) / total
        avg_score = sum(r.get('score', 0) for r in results) / total
        
        return {
            'total_analyzed': total,
            'common_passwords': common_count,
            'common_percentage': (common_count / total) * 100,
            'average_length': round(avg_length, 1),
            'average_entropy': round(avg_entropy, 1),
            'average_score': round(avg_score, 2),
            'score_distribution': score_counts,
            'weak_passwords': score_counts[0] + score_counts[1],
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_html_report(self, results: List[Dict], output_path: str) -> None:
        summary = self._calculate_summary(results)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .stat-label {{
            color: #666;
            margin-top: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        .score-0, .score-1 {{ color: #dc3545; }}
        .score-2 {{ color: #ffc107; }}
        .score-3, .score-4 {{ color: #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Analysis Report</h1>
        <p>Generated on: {summary.get('timestamp', 'N/A')}</p>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_analyzed', 0)}</div>
                <div class="stat-label">Total Passwords</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('average_score', 0)}</div>
                <div class="stat-label">Average Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('common_passwords', 0)}</div>
                <div class="stat-label">Compromised</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('weak_passwords', 0)}</div>
                <div class="stat-label">Weak Passwords</div>
            </div>
        </div>
        
        <h2>Score Distribution</h2>
        <table>
            <tr>
                <th>Score</th>
                <th>Count</th>
                <th>Percentage</th>
            </tr>
"""
        
        score_dist = summary.get('score_distribution', {})
        total = summary.get('total_analyzed', 1)
        
        for score in range(5):
            count = score_dist.get(score, 0)
            percentage = (count / total) * 100
            html_content += f"""
            <tr>
                <td class="score-{score}">Score {score}</td>
                <td>{count}</td>
                <td>{percentage:.1f}%</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def get_stats(self) -> dict:
        return {
            'total_reports_generated': self.report_count
        }