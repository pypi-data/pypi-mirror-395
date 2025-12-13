import requests
import json
import time
from typing import Optional, Dict, Any, Union, Tuple
from urllib.parse import urljoin
import os

from .exceptions import APIError, VeoxError

class APIClient:
    """Low-level API wrapper for DOUG with robust error handling."""

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: tuple = (10, 300),  # (connect, read)
        retries: int = 3
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.retries = retries

        # Setup session with connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": f"veox/{__import__('veox').__version__}"
        })

        if api_key:
            self.session.headers["X-API-Key"] = api_key

        # Configure connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=retries
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """Make HTTP request with error handling."""
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))

        for attempt in range(self.retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt == self.retries:
                    if isinstance(e, requests.exceptions.ConnectionError):
                        raise APIError(f"Cannot connect to DOUG API at {self.base_url}. Is the server running?")
                    elif isinstance(e, requests.exceptions.Timeout):
                        raise APIError(f"Request timeout after {self.timeout} seconds")
                    elif isinstance(e, requests.exceptions.HTTPError):
                        if response.status_code == 401:
                            raise APIError("Invalid API key")
                        elif response.status_code == 404:
                            raise APIError(f"Endpoint not found: {endpoint}")
                        else:
                            raise APIError(f"HTTP {response.status_code}: {response.text}")
                    else:
                        raise APIError(f"Request failed: {e}")

                # Exponential backoff for retries
                time.sleep(2 ** attempt)

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request."""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, json_data: Optional[Dict] = None) -> requests.Response:
        """POST request."""
        return self._make_request("POST", endpoint, json_data=json_data)

    def patch(self, endpoint: str, json_data: Optional[Dict] = None) -> requests.Response:
        """PATCH request."""
        return self._make_request("PATCH", endpoint, json_data=json_data)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request."""
        return self._make_request("DELETE", endpoint)

    def submit_job(self, job_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Submit job via extended pipeline creation."""
        response = self.post("/v1/jobs_ext/create_with_pipeline", json_data=job_spec)
        return response.json()

    def list_datasets(self, task: Optional[str] = None) -> list:
        """List available datasets."""
        params = {}
        if task:
            params['task'] = task
        response = self.get("/v1/datasets", params=params)
        return response.json()

    def get_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """Get dataset details."""
        response = self.get(f"/v1/datasets/{dataset_name}")
        return response.json()

    def get_dataset_source(self, dataset_name: str) -> str:
        """Get dataset source code."""
        response = self.get(f"/v1/datasets/{dataset_name}/source")
        return response.text

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        response = self.get(f"/v1/jobs/{job_id}/status")
        return response.json()

    def get_job_progress(self, job_id: str) -> Dict[str, Any]:
        """Get job progress."""
        response = self.get(f"/v1/jobs/{job_id}/progress")
        return response.json()

    def get_job_report(self, job_id: str) -> Dict[str, Any]:
        """Get job report."""
        response = self.get(f"/v1/jobs/{job_id}/report")
        return response.json()

    def get_job_history(self, job_id: str, limit: int = 1000, include_individuals: bool = False) -> Dict[str, Any]:
        """Get job evolution history."""
        params = {"limit": limit, "include_individuals": include_individuals}
        response = self.get(f"/v1/jobs/{job_id}/history", params=params)
        return response.json()
    
    def list_workers(self) -> list:
        """List connected workers."""
        response = self.get("/v1/cluster/workers")
        return response.json()

    def pause_job(self, job_id: str) -> Dict[str, Any]:
        """Pause a job."""
        response = self.post(f"/v1/jobs/{job_id}/pause")
        return response.json()

    def resume_job(self, job_id: str) -> Dict[str, Any]:
        """Resume a job."""
        response = self.post(f"/v1/jobs/{job_id}/resume")
        return response.json()

    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job."""
        response = self.post(f"/v1/jobs/{job_id}/cancel")
        return response.json()

    def stream_job_events(
        self,
        job_id: str,
        event_processor: 'EvolutionEventProcessor',
        display_manager: 'DisplayManager'
    ) -> Tuple[list, Any]:
        """Stream job events with TQDM processing."""
        import sseclient

        url = f"{self.base_url}/v1/stream/jobs/{job_id}"
        sse_log = []

        try:
            response = self.session.get(url, stream=True, timeout=(30, 3600))
            response.raise_for_status()

            client = sseclient.SSEClient(response)

            for event in client.events():
                if event.event == 'message':
                    try:
                        event_data = json.loads(event.data)
                        sse_log.append(event.data)

                        # Process event with TQDM display
                        display_text = event_processor.process_event(event_data)
                        if display_text and display_manager.verbose:
                             display_manager.info(display_text)

                        # Handle job completion
                        event_type = event_data.get("type")
                        if event_type in {"job_completed", "job_failed", "stream_closed"}:
                            break
                        
                        # Also check status field
                        status = event_data.get("status")
                        if status in {"completed", "failed", "canceled", "cancelled"}:
                            break

                    except json.JSONDecodeError:
                        display_manager.warning(f"⚠️ Failed to parse event: {event.data[:100]}...")

        except KeyboardInterrupt:
            display_manager.warning("⚠️ Streaming interrupted by user")
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            # Let caller handle seamless fallback
            raise
        except Exception as e:
            display_manager.error(f"❌ Streaming failed: {e}")
            raise

        return sse_log, event_processor.state

