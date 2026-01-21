from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from app.config import RUNS_DIR


def build_report_html(run_id: int, payload: dict) -> str:
    results = payload["results"]
    quality = results["quality"]
    triage = results["triage"]
    risk = results["risk"]
    explanation = results["explanation"]
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Murmur Screen Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 24px; color: #111; }}
    h1 {{ margin-bottom: 4px; }}
    .card {{ border: 1px solid #ddd; padding: 16px; border-radius: 8px; margin-bottom: 16px; }}
    .badge {{ padding: 6px 12px; border-radius: 20px; background: #e2e8f0; display: inline-block; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #eee; padding: 8px; text-align: left; }}
  </style>
</head>
<body>
  <h1>Murmur Screen Report</h1>
  <p>Run ID: {run_id}</p>

  <div class=\"card\">
    <h2>Summary</h2>
    <p><strong>Label:</strong> {results['predicted_label']}</p>
    <p><strong>Calibrated confidence:</strong> {results['calibrated_confidence']:.2f}</p>
    <p><strong>Raw confidence:</strong> {results['raw_confidence']:.2f}</p>
  </div>

  <div class=\"card\">
    <h2>Quality Gate</h2>
    <p class=\"badge\">{ 'PASS' if quality['pass'] else 'FAIL' }</p>
    <ul>
      {''.join([f"<li>{reason}</li>" for reason in quality['reasons']]) or '<li>No issues detected</li>'}
    </ul>
  </div>

  <div class=\"card\">
    <h2>Triage & Risk</h2>
    <p><strong>Triage:</strong> {triage['level']} ({triage['rule_fired']})</p>
    <p><strong>Urgency Score:</strong> {risk['urgency_score']:.1f} ({risk['category']})</p>
    <ul>
      {''.join([f"<li>{item}</li>" for item in risk['breakdown']])}
    </ul>
  </div>

  <div class=\"card\">
    <h2>Explanation</h2>
    <h3>Top Features</h3>
    <ul>
      {''.join([f"<li>{feat}</li>" for feat in explanation['top_features']])}
    </ul>
    <h3>Top Segments</h3>
    <ul>
      {''.join([f"<li>{seg['start']:.2f}s - {seg['end']:.2f}s (score {seg['score']:.2f})</li>" for seg in explanation['top_segments']])}
    </ul>
  </div>

  <div class=\"card\">
    <h2>Payload</h2>
    <pre>{json.dumps(payload, indent=2)}</pre>
  </div>

  <p>Disclaimer: This tool provides educational screening support only and does not provide medical diagnosis.</p>
</body>
</html>
"""


def save_report(run_id: int, payload: dict) -> Path:
    report_html = build_report_html(run_id, payload)
    run_dir = RUNS_DIR / str(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / "report.html"
    report_path.write_text(report_html, encoding="utf-8")
    return report_path


def render_pdf(report_path: Path) -> Optional[Path]:
    try:
        from weasyprint import HTML
    except Exception:
        return None
    pdf_path = report_path.with_suffix(".pdf")
    HTML(filename=str(report_path)).write_pdf(str(pdf_path))
    return pdf_path
