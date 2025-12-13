"""Report generation for Veox client."""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

import requests

from .config import APIConfig

class ReportGenerator:
    """Generates comprehensive reports for evolution jobs using the API."""

    def __init__(self, api_config: APIConfig):
        self.api_config = api_config
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"Content-Type": "application/json"})
        if self.api_config.api_key:
            session.headers.update({"X-API-Key": self.api_config.api_key})
        session.timeout = (self.api_config.connect_timeout, self.api_config.read_timeout)
        return session

    def get_job_report(self, job_id: str) -> Dict[str, Any]:
        url = f"{self.api_config.url}/v1/jobs/{job_id}/report"
        try:
            response = self.session.get(url)
            if response.status_code == 404:
                return {"status": "not_supported"}
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return {"status": "error"}

    def generate_final_report(self, job_id: str, artifacts_dir: Optional[Path] = None) -> str:
        start_time = time.time()
        report_data = self.get_job_report(job_id)
        fetch_time = time.time() - start_time

        status = report_data.get("status")
        if status in {"not_supported", "error"}:
            return f"ℹ️  Could not fetch server report (status: {status})."

        formatted_report = self._format_report(report_data, artifacts_dir, fetch_time)
        return formatted_report

    def _format_report(self, report_data: Dict[str, Any], artifacts_dir: Optional[Path] = None, fetch_time: float = 0.0) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append("📊 FINAL EVOLUTION REPORT")
        lines.append("=" * 80)
        lines.append(f"Job ID: {report_data.get('job_id')}")
        lines.append(f"Name: {report_data.get('name')}")
        lines.append(f"Status: {report_data.get('status')}")
        lines.append(f"Dataset: {report_data.get('dataset')}")
        lines.append(f"Task Type: {report_data.get('task_type')}")
        lines.append(f"Report fetched in: {fetch_time:.2f}s")
        lines.append("")

        lines.append("📈 SUMMARY STATISTICS")
        lines.append("-" * 40)
        lines.append(f"Total Results: {report_data.get('total_results', 0)}")
        lines.append(f"Evolved Results: {report_data.get('evolved_results', 0)}")
        lines.append(f"Baseline Results: {report_data.get('baseline_results', 0)}")
        
        best_fitness = report_data.get('best_fitness')
        best_fitness_str = f"{best_fitness:.6f}" if best_fitness is not None else "—"
        lines.append(f"Best Fitness: {best_fitness_str}")

        top_performers = report_data.get('top_performers', [])
        if top_performers:
            lines.append("")
            lines.append("🏆 TOP PERFORMERS")
            lines.append("-" * 40)
            for i, performer in enumerate(top_performers[:5], 1):
                candidate_id = performer.get('candidate_id', 'unknown')
                fitness = performer.get('fitness')
                generation = performer.get('generation', 0)
                is_baseline = 'BASELINE' in candidate_id
                marker = "[BASELINE]" if is_baseline else ""
                
                lines.append(f"#{i} | Fitness: {fitness:.6f} | Gen: {generation} | {candidate_id} {marker}")
        
        if artifacts_dir:
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            report_file = artifacts_dir / "final_report.txt"
            with open(report_file, 'w') as f:
                f.write("\n".join(lines))
            lines.append(f"\nReport saved to: {report_file}")

        return "\n".join(lines)

    # Alias for client compatibility if needed
    def generate_report(self, job_id: str) -> str:
        return self.generate_final_report(job_id)
