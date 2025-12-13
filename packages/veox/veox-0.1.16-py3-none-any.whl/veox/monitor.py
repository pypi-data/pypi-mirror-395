
import time
import sys
from typing import Dict, Any, List, Optional
from .display import DisplayManager
from .api import APIClient

class EvolutionMonitor:
    """
    Monitors and displays detailed evolution progress and results,
    mirroring the rich output of the distributed evolution demo.
    """

    def __init__(self, api_client: APIClient, display_manager: DisplayManager):
        self.api = api_client
        self.display = display_manager

    def print_final_report(self, job_id: str):
        """
        Prints a comprehensive final report for the job, including
        timings, slowest leases, failure distribution, and results summary.
        """
        try:
            # Fetch detailed lease information
            # Note: The demo script uses a direct request to /v1/jobs/{job_id}/leases
            # We'll use the API client helper if available, or raw request
            try:
                leases_data = self.api.get(f"/v1/jobs/{job_id}/leases").json()
                leases = leases_data.get("leases", [])
            except Exception:
                leases = []

            if leases:
                print("\n" + "="*80)
                print("⏱️  TIMING REPORT")
                print("="*80)
                
                completed_leases = [l for l in leases if l.get('status') == 'completed']
                if completed_leases:
                    queue_times = [l.get('queue_time_seconds') for l in completed_leases if l.get('queue_time_seconds') is not None]
                    exec_times = [l.get('execution_time_seconds') for l in completed_leases if l.get('execution_time_seconds') is not None]
                    total_times = [l.get('total_time_seconds') for l in completed_leases if l.get('total_time_seconds') is not None]
                    
                    if queue_times:
                        print(f"   Queue Time: avg {sum(queue_times)/len(queue_times):.1f}s, max {max(queue_times):.1f}s")
                    if exec_times:
                        print(f"   Execution Time: avg {sum(exec_times)/len(exec_times):.1f}s, max {max(exec_times):.1f}s")
                    if total_times:
                        print(f"   Total Time: avg {sum(total_times)/len(total_times):.1f}s, max {max(total_times):.1f}s")
                    
                    # Top 10 slowest leases
                    # Filter out leases with no total_time_seconds to avoid comparison errors
                    completed_with_times = [l for l in completed_leases if l.get('total_time_seconds') is not None]
                    sorted_leases = sorted(completed_with_times, key=lambda x: x.get('total_time_seconds') or 0, reverse=True)
                    
                    if sorted_leases:
                        print(f"\n🐌 Top 10 Slowest Leases:")
                        for i, lease in enumerate(sorted_leases[:10], 1):
                            lease_id = lease.get('lease_id', 'unknown')[:20]
                            total_time = lease.get('total_time_seconds') or 0
                            exec_time = lease.get('execution_time_seconds') or 0
                            worker = lease.get('worker_name', 'unknown')
                            print(f"   {i}. {lease_id}... ({total_time:.1f}s total, {exec_time:.1f}s exec) - {worker}")

            # Failure distribution
            try:
                response = self.api.get(f"/v1/jobs/{job_id}/failures")
                failures = response.json().get('failures', [])
            except Exception:
                failures = []

            if failures:
                print(f"\n❌ Failure Distribution:")
                for failure in failures[:5]:  # Show top 5 failure types
                    error_type = failure.get('error_type', 'unknown')
                    count = failure.get('failure_count', 0)
                    worker = failure.get('worker_name', 'unknown')
                    print(f"   • {error_type}: {count} failures ({worker})")
            
            # Reconcile Results count (optional, can be got from report or status)
            # The demo script used 'timeline' from state, here we might check the report
            
            print("="*80 + "\n")

        except Exception as e:
            self.display.error(f"⚠️  Could not generate detailed tracking summary: {e}")
            # print traceback in debug mode?
