"""Main client module for Veox."""

import json
import time
import requests
import pandas as pd
import numpy as np
from typing import Optional, Union, List, Dict, Any, Tuple
from pathlib import Path
from dataclasses import asdict

from .api import APIClient
from .display import DisplayManager
from .event_processor import EvolutionEventProcessor
from .report_generator import ReportGenerator
from .pipeline_source_viewer import display_best_pipeline
from .config import JobConfig, APIConfig
from .datasets.loader import DatasetLoader
from .monitor import EvolutionMonitor

class Veox:
    """
    Veox client for DOUG (Distributed Optimization using Genetic algorithms).
    
    Provides an sklearn-style API for distributed evolution.
    """

    def __init__(
        self,
        api_url: str = "http://localhost:8088",
        api_key: Optional[str] = None,
        verbose: bool = False,
        debug: bool = False
    ):
        """
        Initialize the Veox client.

        Args:
            api_url: URL of the DOUG API server
            api_key: Optional API key for authentication
            verbose: Enable verbose logging
            debug: Enable debug logging
        """
        self._api = APIClient(api_url, api_key)
        self._display = DisplayManager(verbose=verbose, debug=debug)
        self._verbose = verbose
        self._debug = debug
        self._api_config = APIConfig(url=api_url, api_key=api_key)
        self._report_generator = ReportGenerator(self._api_config)
        self._monitor = EvolutionMonitor(self._api, self._display)
        # State tracking
        self.last_job_id: Optional[str] = None
        self.best_fitness: Optional[float] = None
        
        # Check available workers on initialization
        self._check_worker_count()

    def fit(
        self,
        X: Optional[Union[pd.DataFrame, str]] = None,
        y: Optional[Union[pd.Series, str]] = None,
        data: Optional[pd.DataFrame] = None,
        target_column: Optional[str] = None,
        dataset: Optional[str] = None,
        task: str = "binary",
        population: int = 50,
        generations: int = 10,
        name: Optional[str] = None,
        max_samples: Optional[int] = None,
        seed: Optional[int] = None,
        fitness: Optional[str] = None,
        timeout: Optional[int] = None,
        async_evolution: bool = False,
        async_threshold: float = 0.8,
        task_timeout: Optional[int] = None,
        show_pipeline: bool = True,
        use_polling: bool = False,
        poll_interval: float = 3.0,
        plot: bool = True
    ) -> 'Veox':
        """
        Start an evolution job to fit a pipeline.
        
        Args:
            X: Features (DataFrame) or path to CSV
            y: Target (Series) or target column name
            data: Helper to pass X and y in one DataFrame (requires target_column)
            target_column: Name of target column if data is provided
            dataset: Name of a built-in dataset or dataset ID on server
            task: Task type (binary, regression)
            population: Population size
            generations: Number of generations
            name: Optional name for the job
            max_samples: Max samples to use (subsampling)
            seed: Random seed
            fitness: Fitness function expression
            timeout: Job timeout in seconds
            async_evolution: Enable async evolution
            async_threshold: Threshold for async evolution
            task_timeout: Per-task timeout
            show_pipeline: Whether to display best pipeline source at the end (default True)
        
        Returns:
            self
        """
        # Handle data upload if needed
        dataset_id = dataset
        if X is not None or data is not None:
            dataset_id = self._upload_dataframe(X=X, y=y, data=data, target_column=target_column, task=task)
        elif not dataset:
            raise ValueError("Must provide either data (X, y) or a dataset name/ID")

        # Create job config
        config = JobConfig(
            task=task,
            population=population,
            generations=generations,
            dataset=dataset_id,
            name=name,
            max_samples=max_samples,
            seed=seed,
            fitness=fitness,
            timeout=timeout,
            async_evolution=async_evolution,
            async_threshold=async_threshold,
            task_timeout=task_timeout
        )

        self._display.info(f"Submitting evolution job for dataset '{dataset_id}'...")
        
        # Submit job
        job_spec = asdict(config)
        # Remove None values
        job_spec = {k: v for k, v in job_spec.items() if v is not None}
        
        # Rename dataset to dataset_id for API
        if 'dataset' in job_spec:
            job_spec['dataset_id'] = job_spec.pop('dataset')
        
        try:
            response = self._api.submit_job(job_spec)
            job_id = response['job_id']
            self.job_id = job_id  # Store for later use
            self._display.success(f"Job submitted: {job_id}")
            
            # Create event processor
            total_evals = population * generations # Approximation
            event_processor = EvolutionEventProcessor(
                verbose=self._verbose, 
                debug=self._debug,
                total_iterations=total_evals
            )
            
            # Hybrid Engine: Try streaming, fallback to polling
            stream_success = False

            if not use_polling:
                try:
                    self._display.info("Starting evolution stream...")
                    _, final_state = self._api.stream_job_events(
                        job_id,
                        event_processor=event_processor,
                        display_manager=self._display
                    )
                    stream_success = True
                except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
                    # Seamless fallback for premature closures without "failed" message
                    msg = str(e)
                    if "Response ended prematurely" in msg or "Connection broken" in msg:
                        self._display.info(f"⚠️ Stream connection unstable. Seamlessly switching to polling mode...")
                    else:
                        self._display.warning(f"⚠️ Stream connection unstable/closed. Switching to polling mode... ({msg})")
                    stream_success = False
                except Exception as e:
                    self._display.warning(f"⚠️ Stream error. Switching to polling mode... ({str(e)})")
                    stream_success = False

            if not stream_success or use_polling:
                self._poll_until_complete(job_id, poll_interval=poll_interval, event_processor=event_processor)
            
            # Use EvolutionMonitor for final detailed report
            self._monitor.print_final_report(job_id)

            # Show code if requested
            if show_pipeline:
                # Refresh status to get best run ID if not captured from stream
                try:
                    report = self._api.get_job_report(job_id)
                    best_fitness = report.get('best_fitness', float('-inf'))
                    
                    # Try to get run ID from processor state or report
                    run_id = event_processor.state.global_best_run_id
                    if not run_id and 'top_performers' in report and report['top_performers']:
                         run_id = report['top_performers'][0].get('run_id')
                         
                    if run_id:
                        display_best_pipeline(
                            self._api_config, 
                            run_id,
                            fitness=best_fitness if best_fitness != float('-inf') else None
                        )
                except Exception as e:
                    if self._debug:
                        self._display.warning(f"Could not display pipeline: {e}")

            # Plotting
            try:
                # Import here to avoid circular dependency
                from .plotting import plot_evolution
                history = self._api.get_job_history(job_id, include_individuals=True)
                plot_evolution(history, title=f"Evolution History: {name or job_id}")
            except ImportError:
                pass
            except Exception as e:
                if self._debug:
                     self._display.warning(f"Plotting failed: {e}")
            
            return self
            
        except requests.exceptions.HTTPError as e:
            self._display.error(f"Job submission failed: {e}")
            if e.response is not None:
                self._display.error(f"Server response: {e.response.text}")
            raise
        except KeyboardInterrupt:
            self._display.warning("Evolution interrupted by user.")
            return self

    def _poll_until_complete(
        self, 
        job_id: str, 
        poll_interval: float, 
        event_processor: 'EvolutionEventProcessor'
    ) -> None:
        """Poll job status until completion."""
        import random
        
        self._display.info(f"🔁 Polling mode active (interval={poll_interval}s)...")
        
        while True:
            # Jitter to avoid thundering herd if many clients
            sleep_time = poll_interval + random.uniform(-0.1, 0.1) * poll_interval
            time.sleep(sleep_time)
            
            try:
                progress = self._api.get_job_progress(job_id)
                
                # Check terminal status (flag or status check)
                is_terminal = progress.get("is_terminal")
                if is_terminal is None:
                    is_terminal = progress.get("status") in {"completed", "failed", "cancelled", "stopped", "canceled"}
                
                # Update progress bar
                if hasattr(event_processor, "update_from_progress"):
                    event_processor.update_from_progress(progress)
                else:
                    # Basic update if method missing
                    pct = progress.get("job_progress_pct", 0)
                    if hasattr(event_processor, "progress_bar") and event_processor.progress_bar:
                         completed = progress.get("total_completed_evaluations", 0)
                         if completed > event_processor.progress_bar.n:
                              event_processor.progress_bar.update(completed - event_processor.progress_bar.n)
                
                if is_terminal:
                    self._display.success(f"Job completed with status: {progress.get('status')}")
                    if hasattr(event_processor, "progress_bar") and event_processor.progress_bar:
                        event_processor.progress_bar.close()
                    break
                    
            except Exception as e:
                # Tolerate transient errors during polling
                if self._debug:
                     self._display.warning(f"Poll check failed: {e}")

    def _upload_dataframe(
        self, 
        X: Optional[Union[pd.DataFrame, str]] = None,
        y: Optional[Union[pd.Series, str]] = None,
        data: Optional[pd.DataFrame] = None,
        target_column: Optional[str] = None,
        task: str = "binary",
        name: Optional[str] = None
    ) -> str:
        """Upload a pandas dataframe to the server."""
        # Normalize inputs
        if data is None:
            if isinstance(X, str):
                data = pd.read_csv(X)
            elif isinstance(X, pd.DataFrame):
                data = X.copy()
            elif isinstance(X, list):
                data = pd.DataFrame(X)
            else:
                raise ValueError("X must be a path to CSV, a DataFrame, or a list")
            
            if y is not None:
                if isinstance(y, str):
                    target_column = y
                    # If y is just a name, assume it's in data or X
                elif isinstance(y, (pd.Series, list, np.ndarray)):
                    data['target'] = pd.Series(y)
                    target_column = 'target'
                else:
                    raise ValueError("y must be a target column name, Series, or list")
        
        if not target_column:
            raise ValueError("Must specify target_column")

        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in data")

        # Size check
        est_size = data.memory_usage(deep=True).sum()
        if est_size > 10 * 1024 * 1024:
            self._display.warning(f"⚠️ DataFrame is large ({est_size / 1024 / 1024:.1f} MB). Upload might take some time.")

        self._display.info("Uploading dataframe...")
        
        # Prepare payload with robust serialization
        payload = {
            "dataframe": {
                # Ensure ISO dates and handle serialization robustness
                "data": data.to_json(orient='records', date_format='iso', double_precision=10, default_handler=str),
                "dtypes": data.dtypes.astype(str).to_dict()
            },
            "target_column": target_column,
            "task": task,
            "name": name or f"upload_{int(time.time())}"
        }
        
        response = self._api.post("/v1/datasets/upload", json_data=payload)
        dataset_id = response.json()['dataset_id']
        self._display.success(f"Uploaded dataset: {dataset_id}")
        return dataset_id

    def pull_code(
        self,
        job_id: Optional[str] = None,
        run_id: Optional[str] = None,
        output_file: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Pull the python source code for the best pipeline of a job or a specific run.
        """
        if run_id:
            target_run_id = run_id
        elif job_id:
            target_run_id = self._get_best_run_id(job_id)
        elif hasattr(self, 'job_id') and self.job_id:
            target_run_id = self._get_best_run_id(self.job_id)
        else:
            raise ValueError("Must provide either job_id or run_id, or have run fit() previously")
            
        print(f"Fetching code for run {target_run_id}...")
        response = self._api.get(f"/v1/runs/{target_run_id}/pipeline/source")
        code = response.text
        
        if output_file:
            path = Path(output_file)
            path.write_text(code)
            print(f"Code saved to {path}")
        else:
            print("\n" + "="*80)
            print("PIPELINE SOURCE CODE")
            print("="*80)
            print(code)
            print("="*80 + "\n")
            
        return code

    def _get_best_run_id(self, job_id: str) -> str:
        """Fetch the best run ID for a job."""
        
        # Try to get run ID from 2 sources:
        # 1. First from report's top performers
        try:
             report = self._api.get(f"/v1/jobs/{job_id}/report").json()
             if 'top_performers' in report and report['top_performers']:
                  # Some top performers objects might contain run_id
                  best = report['top_performers'][0]
                  if 'run_id' in best:
                       return best['run_id']
        except Exception:
             pass

        # 2. Fallback to listing all runs
        runs = self._api.get(f"/v1/jobs/{job_id}/runs").json()
        if not runs:
            raise ValueError(f"No runs found for job {job_id}")
            
        # Filter valid runs
        valid_runs = [r for r in runs if r.get('fitness') is not None]
        if not valid_runs:
            raise ValueError("No valid runs with fitness found")
            
        best_run = max(valid_runs, key=lambda x: x['fitness'])
        return best_run['run_id']

    def status(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Get job status."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.get_job_status(job_id)

    def get_progress(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Get job progress with estimates."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.get_job_progress(job_id)

    def get_report(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive job report."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.get_job_report(job_id)

    def monitor_job(self, job_id: Optional[str] = None) -> None:
        """
        Print the detailed final report for a job using the EvolutionMonitor.
        Useful for inspecting past jobs.
        """
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        self._monitor.print_final_report(job_id)

    def list_workers(self) -> List[Dict[str, Any]]:
        """List active workers."""
        return self._api.list_workers()

    def get_worker_count(self) -> int:
        """Get the number of available workers."""
        try:
            return len(self.list_workers())
        except Exception:
            return 0

    def pause(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Pause a job."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.pause_job(job_id)

    def resume(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Resume a paused job."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.resume_job(job_id)

    def cancel(self, job_id: Optional[str] = None) -> Dict[str, Any]:
        """Cancel a job."""
        job_id = job_id or self.last_job_id
        if not job_id:
            raise ValueError("job_id is required (run fit() first or provide job_id)")
        return self._api.cancel_job(job_id)

    def pull_dataset_source(
        self,
        dataset_name: str,
        output_file: Optional[Union[str, Path]] = None
    ) -> str:
        """Pull dataset source code."""
        code = self._api.get_dataset_source(dataset_name)
        
        if output_file:
            path = Path(output_file)
            path.write_text(code)
            self._display.success(f"Dataset source saved to {path}")
        else:
            print("\n" + "="*80)
            print("DATASET SOURCE CODE")
            print("="*80)
            print(code)
            print("="*80 + "\n")
        
        return code

    def list_datasets(self, task: Optional[str] = None) -> List[str]:
        """List available datasets from server."""
        return self._api.list_datasets(task=task)

    def get_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """Get dataset information."""
        return self._api.get_dataset_info(dataset_name)

    def list_builtin_datasets(self) -> List[Dict[str, Any]]:
        """List available built-in datasets included in the package."""
        loader = DatasetLoader()
        return loader.list_datasets()

    def load_dataset(self, name: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Load a built-in dataset by name."""
        loader = DatasetLoader()
        return loader.load_dataset(name)

    def _check_worker_count(self) -> None:
        """Check available worker count and display status."""
        try:
            workers = self.list_workers()
            worker_count = len(workers)
            
            if self._verbose:
                self._display.info(f"📊 Connected to DOUG API at {self._api_config.url}")
                self._display.info(f"👷 Available workers: {worker_count}")
                
                # Show worker details if verbose
                if workers:
                    active_count = sum(1 for w in workers if w.get('status') == 'online' or w.get('active_tasks', 0) > 0)
                    self._display.info(f"   Active workers: {active_count}/{worker_count}")
                    
                    # Show some worker stats
                    total_tasks = sum(w.get('processed_tasks', 0) for w in workers)
                    if total_tasks > 0:
                        self._display.info(f"   Total tasks processed: {total_tasks}")
            else:
                # Always show worker count, even in non-verbose mode
                print(f"👷 Connected to DOUG API: {worker_count} workers available")
            
            # Warn if fewer than expected workers (40 is the target)
            if worker_count < 40:
                if worker_count < 10:
                    self._display.warning(f"⚠️  Low worker count ({worker_count}). For best performance, consider scaling to 40 workers.")
                elif worker_count < 40:
                    self._display.info(f"💡 Tip: Current worker count is {worker_count}. For high-concurrency workloads, consider scaling to 40 workers.")
            elif worker_count >= 40:
                self._display.success(f"✅ Excellent! {worker_count} workers available (target: 40+)")
                
        except Exception as e:
            # Don't fail initialization if worker check fails
            if self._debug:
                self._display.warning(f"⚠️  Could not check worker count: {e}")
            # In non-debug mode, silently continue
