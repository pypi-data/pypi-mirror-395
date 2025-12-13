"""Event processing logic for Veox client."""

import json
import math
import sys
import time
from collections import deque
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Local imports
from .config import StreamingConfig

class ColorManager:
    """Manages worker colors locally without server dependency."""
    def __init__(self):
        self.worker_colors = {}
        self.colors = [
            "\033[94m",  # Blue
            "\033[92m",  # Green
            "\033[93m",  # Yellow
            "\033[95m",  # Magenta
            "\033[96m",  # Cyan
            "\033[91m",  # Red
        ]
        self.next_color_idx = 0
        self.RESET = "\033[0m"

    def get_colored_name(self, worker_id: str, worker_name: str) -> str:
        if worker_id not in self.worker_colors:
            self.worker_colors[worker_id] = self.colors[self.next_color_idx % len(self.colors)]
            self.next_color_idx += 1
        
        color = self.worker_colors[worker_id]
        return f"{color}{worker_name}{self.RESET}"


@dataclass
class NormalizedResult:
    """Normalized result event data."""
    generation: int
    candidate_id: str
    worker_id: str
    worker_name: str
    status: str  # "ok" | "error" | other
    fitness: Optional[float]  # Never coerced to 0.0
    base: Optional[float]
    noise_penalty: float
    cost_penalty: float
    eval_mode: str  # "kfold" | "holdout" | "simple" | "unknown"
    has_aggregated: bool
    kfold_error: Optional[str]  # None means no error, only non-empty strings are errors
    metrics: Dict[str, float]
    holdout: Dict[str, float]
    pipeline_stages: List[str]
    gp_expression: Optional[str]
    error: Optional[str]
    error_type: Optional[str] = None
    error_traceback: Optional[str] = None
    flags: Dict[str, Any] = None
    fold_metrics_details: Optional[List[Dict[str, Any]]] = None
    fold_hash_summary: Optional[Dict[str, Any]] = None
    run_id: Optional[str] = None  # Run ID from event payload
    
    def __post_init__(self):
        if self.flags is None:
            self.flags = {}


@dataclass
class WorkerStats:
    """Statistics for a worker."""
    worker_name: str
    count: int = 0
    total_fitness: float = 0.0
    fitness_values: List[float] = None
    last_seen: float = None

    def __post_init__(self):
        if self.fitness_values is None:
            self.fitness_values = []
        if self.last_seen is None:
            self.last_seen = time.time()

    @property
    def avg_fitness(self) -> float:
        """Calculate average fitness from finite values only."""
        if not self.fitness_values:
            return 0.0
        return self.total_fitness / len(self.fitness_values)


@dataclass
class EvolutionState:
    """State tracking for evolution progress."""
    worker_stats: Dict[str, WorkerStats] = None
    all_results: List[Dict[str, Any]] = None
    baseline_results: List[Dict[str, Any]] = None
    gp_expressions_by_generation: Dict[int, Dict[str, Any]] = None
    gp_evolution_history: List[Dict[str, Any]] = None
    last_generation_gp: Dict[int, str] = None
    start_time: float = None
    completed_iterations: int = 0
    total_iterations: Optional[int] = None
    global_best_fitness: float = float('-inf')
    global_best_candidate: Optional[str] = None
    global_best_generation: int = 0
    global_best_run_id: Optional[str] = None  # Run ID for the best performing pipeline

    def __post_init__(self):
        if self.worker_stats is None:
            self.worker_stats = {}
        if self.all_results is None:
            self.all_results = []
        if self.baseline_results is None:
            self.baseline_results = []
        if self.gp_expressions_by_generation is None:
            self.gp_expressions_by_generation = {}
        if self.gp_evolution_history is None:
            self.gp_evolution_history = []
        if self.last_generation_gp is None:
            self.last_generation_gp = {}
        if self.start_time is None:
            self.start_time = time.time()


def _safe_float(value: Any) -> Optional[float]:
    """Safely convert value to float, returning None if invalid."""
    if value is None:
        return None
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (ValueError, TypeError):
        return None


def _is_modern_event(ev: Dict[str, Any]) -> bool:
    """Check if event uses modern v1 contract."""
    sv = str(ev.get("schema_version") or "")
    cv = ev.get("contract_version")
    return (
        (isinstance(cv, int) and cv >= 1)
        or sv.startswith("result_received.v")
        or "fitness_components" in ev
    )


def _compute_fitness_from_components(ev: Dict[str, Any]) -> Optional[float]:
    """Compute fitness from fitness_components if available."""
    comps = ev.get("fitness_components") or {}
    base = _safe_float(comps.get("base"))
    if base is None:
        return None
    
    penalties = 0.0
    for k in ("noise_penalty", "cost_penalty", "regularization", "constraints_penalty", "penalty"):
        v = _safe_float(comps.get(k))
        if v is not None:
            penalties += v
    
    return base - penalties


def _extract_holdout(ev: Dict[str, Any], metrics: Dict[str, float]) -> Dict[str, float]:
    """Extract holdout metrics from event."""
    holdout = dict(ev.get("holdout_metrics") or {})
    # Also look in metrics for holdout/fold_4 keys
    for k, v in (metrics or {}).items():
        if isinstance(v, (int, float)) and (k.startswith("holdout_") or k.startswith("fold_4_")):
            holdout[k] = float(v)
    return {k: float(v) for k, v in holdout.items() 
            if isinstance(v, (int, float)) and math.isfinite(float(v))}


def _eval_mode(ev: Dict[str, Any]) -> str:
    """Determine evaluation mode from event."""
    fp = ev.get("fitness_policy") or {}
    if isinstance(fp, dict) and fp.get("domain") in {"kfold", "holdout", "simple"}:
        return fp["domain"]

    m = ev.get("metrics") or {}
    # Check for aggregated metrics (CV results)
    if any(k for k in m.keys() if any(k.endswith(suffix) for suffix in ("_mean", "_median", "_std", "_var"))):
        return "kfold"
    # Check for holdout metrics
    if any(k for k in m.keys() if k.startswith(("holdout_", "fold_4_"))):
        return "holdout"
    # Check for simple single metrics
    if any(k for k in ["auc", "accuracy", "f1", "r2"] if k in m):
        return "simple"
    return "unknown"


def normalize_result_event(ev: Dict[str, Any]) -> Optional[NormalizedResult]:
    """Normalize a result_received event into a clean structure."""
    if ev.get("type") != "result_received":
        return None

    metrics = ev.get("metrics") or {}
    metrics_num = {
        k: float(v) for k, v in metrics.items()
        if isinstance(v, (int, float)) and math.isfinite(float(v))
    }

    # Fitness precedence: explicit → components → known metrics → None
    fitness = _safe_float(ev.get("fitness"))
    if fitness is None and _is_modern_event(ev):
        fitness = _compute_fitness_from_components(ev)

    if fitness is None:
        # Fallback to known metric keys
        for k in ("fitness", "best_fitness", "auc_mean", "auc", "r2_mean", "r2", "accuracy", "f1"):
            val = _safe_float(metrics.get(k))
            if val is not None:
                fitness = val
                break

        # Also check for any numeric metric that looks like a fitness value
        if fitness is None:
            for k, v in metrics.items():
                if isinstance(v, (int, float)) and math.isfinite(float(v)):
                    if not any(skip in k.lower() for skip in ['fold_', 'std', 'mean', 'median', 'min', 'max', 'var']):
                        fitness = float(v)
                        break
    
    has_aggregated = bool(
        ev.get("has_aggregated_metrics")
        or any(k.endswith(("_mean", "_median", "_std")) for k in metrics_num)
    )
    
    error = ev.get("error")
    kfold_err = ev.get("kfold_error")
    if not error and isinstance(kfold_err, str) and kfold_err.strip():
        error = kfold_err
    elif not error:
        error = None
    
    stages = ev.get("pipeline_stages") or []
    if not stages:
        ps = ev.get("pipeline_spec") or {}
        sdefs = ps.get("stages") or []
        if isinstance(sdefs, list):
            stages = [
                f"{s.get('stage', 'unknown')}:{s.get('label', 'unknown')}"
                for s in sdefs
            ]
    
    comps = ev.get("fitness_components") or {}
    base = _safe_float(comps.get("base"))
    noise = _safe_float(comps.get("noise_penalty")) or 0.0
    cost = _safe_float(comps.get("cost_penalty")) or 0.0
    
    status = (ev.get("status") or "ok").lower()

    fitness_policy = ev.get("fitness_policy") or {}
    if isinstance(fitness_policy, dict) and fitness_policy.get("evaluation_failed"):
        status = "error"
        error = error or fitness_policy.get("error_message", "evaluation_failed")

    kfold_error = ev.get("kfold_error")
    if kfold_error and isinstance(kfold_error, str) and kfold_error.strip():
        status = "error"
        error = error or kfold_error

    if status == "ok" and fitness is None:
        status = "error"
        error = error or "missing_fitness"
    elif status == "error" and not error:
        error = "evaluation_failed"
    
    fold_metrics_details = ev.get("fold_metrics_details")
    if not isinstance(fold_metrics_details, list):
        fold_metrics_details = []
    
    # Ensure fold 4 (holdout) metrics are included if hash_summary indicates it exists
    fold_hash_summary = ev.get("fold_hash_summary")
    if not isinstance(fold_hash_summary, dict):
        fold_hash_summary = None
    
    # Check if fold 4 exists in hash_summary but missing from fold_metrics_details
    if fold_hash_summary:
        folds_in_hash = set()
        for entry in fold_hash_summary.get("folds", []):
            if isinstance(entry, dict):
                fold = entry.get("fold")
                if fold is not None:
                    try:
                        folds_in_hash.add(int(fold))
                    except (TypeError, ValueError):
                        pass
        
        # Check if fold 4 exists in hash but not in metrics_details
        if 4 in folds_in_hash:
            fold_4_in_details = any(
                isinstance(d, dict) and int(d.get("fold", -1)) == 4 
                for d in fold_metrics_details
            )
            
            if not fold_4_in_details:
                # Try to extract fold 4 metrics from holdout_metrics or metrics
                fold_4_metrics = {}
                holdout_metrics = ev.get("holdout_metrics") or {}
                
                # Extract from holdout_metrics (may have fold_4_ prefix or direct keys)
                for key, value in holdout_metrics.items():
                    if isinstance(value, (int, float)) and math.isfinite(float(value)):
                        # Remove fold_4_ prefix if present
                        base_key = key[7:] if key.startswith("fold_4_") else key
                        fold_4_metrics[base_key] = float(value)
                
                # Also check main metrics dict for fold_4_ prefixed keys
                for key, value in metrics_num.items():
                    if key.startswith("fold_4_") and isinstance(value, (int, float)):
                        base_key = key[7:]  # Remove "fold_4_" prefix
                        if base_key not in fold_4_metrics:
                            fold_4_metrics[base_key] = float(value)
                
                # Add fold 4 entry if we found any metrics
                if fold_4_metrics:
                    fold_metrics_details.append({
                        "fold": 4,
                        "metrics": fold_4_metrics
                    })
    
    # Convert to None if empty list for consistency
    if not fold_metrics_details:
        fold_metrics_details = None
    
    run_id = ev.get("run_id")
    
    return NormalizedResult(
        generation=int(ev.get("generation") or 0),
        candidate_id=ev.get("candidate_id") or "unknown",
        worker_id=ev.get("worker_id") or "unknown",
        worker_name=ev.get("worker_name") or "unknown",
        status=status,
        fitness=fitness,
        base=base,
        noise_penalty=noise,
        cost_penalty=cost,
        eval_mode=_eval_mode(ev),
        has_aggregated=has_aggregated,
        kfold_error=kfold_err if isinstance(kfold_err, str) and kfold_err.strip() else None,
        metrics=metrics_num,
        holdout=_extract_holdout(ev, metrics_num),
        pipeline_stages=stages,
        gp_expression=ev.get("gp_expression"),
        error=error,
        error_type=ev.get("error_type"),
        error_traceback=ev.get("error_traceback"),
        flags=ev.get("fitness_flags") or {},
        fold_metrics_details=fold_metrics_details,
        fold_hash_summary=fold_hash_summary,
        run_id=run_id,
    )


class EvolutionEventProcessor:
    """Processes SSE events from DOUG evolution jobs."""

    def __init__(self, verbose: bool = False, debug: bool = False, total_iterations: Optional[int] = None, progress_enabled: bool = True):
        self.config = StreamingConfig(
            verbosity="debug" if debug else ("verbose" if verbose else "basic"),
            debug=debug
        )
        self.color_manager = ColorManager()
        self.state = EvolutionState()
        self.state.total_iterations = total_iterations
        self.verbosity = self.config.verbosity
        self.once_per_gen_warnings = self.config.once_per_gen_warnings
        self.gen_warned: set = set()
        self.meltdown_window = deque(maxlen=self.config.meltdown_window)
        self.last_progress_report = time.time()
        self.job_submitted_at: Optional[float] = None
        self.task_dispatch_times: Dict[str, float] = {}
        
        # Initialize progress bar
        self.progress_bar: Optional[Any] = None
        self.progress_enabled = progress_enabled and sys.stdout.isatty() and self.verbosity != "quiet"
        
        if self.progress_enabled:
            try:
                from tqdm import tqdm
                self.progress_bar = tqdm(
                    total=total_iterations,
                    desc="🧬 Evolution",
                    unit=" iter",
                    unit_scale=False,
                    bar_format='{desc}: {percentage:3.0f}%|{bar:40}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}',
                    position=0,
                    leave=True,
                    ncols=None,
                    colour='cyan',
                    dynamic_ncols=True,
                    miniters=1,
                    mininterval=0.1,
                    file=sys.stdout
                )
                self.progress_bar.set_postfix_str("Best: —")
                self._print = lambda *args, **kwargs: tqdm.write(*args)
            except ImportError:
                self.progress_enabled = False
                self.progress_bar = None
                self._print = print
                print("⚠️  tqdm not available, using basic progress reporting")
        else:
            self._print = print

    def process_event(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Process a single event and return display text if any."""
        # Track job submission time
        if self.job_submitted_at is None:
            event_timestamp = event_data.get("timestamp")
            if event_timestamp:
                try:
                    from datetime import datetime
                    if isinstance(event_timestamp, str):
                        dt = datetime.fromisoformat(event_timestamp.replace('Z', '+00:00'))
                        self.job_submitted_at = dt.timestamp()
                    else:
                        self.job_submitted_at = float(event_timestamp)
                except (ValueError, TypeError):
                    self.job_submitted_at = time.time()
            else:
                self.job_submitted_at = time.time()
        
        event_type = event_data.get("type")

        if event_type == "result_received":
            return self._process_result_received(event_data)
        elif event_type == "generation_complete":
            return self._process_generation_complete(event_data)
        elif event_type == "generation_evolved":
            return self._process_generation_evolved(event_data)
        elif event_type in {"job_complete", "job_completed"}:
            return self._process_job_complete(event_data)
        elif event_type == "stream_closed":
            return self._process_stream_closed(event_data)

        job_status = event_data.get("status")
        if job_status and job_status.lower() in {"completed", "failed", "canceled", "cancelled", "stopped"}:
            return self._process_job_terminal_state(event_data)

        return None

    def _process_result_received(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Process result_received event."""
        nr = normalize_result_event(event_data)
        if not nr:
            return None
        
        self.state.completed_iterations += 1
        self._update_best_run(nr, event_data)
        
        # Update worker stats
        if nr.worker_id not in self.state.worker_stats:
            self.state.worker_stats[nr.worker_id] = WorkerStats(worker_name=nr.worker_name)
        
        ws = self.state.worker_stats[nr.worker_id]
        ws.count += 1
        if nr.fitness is not None:
            ws.total_fitness += nr.fitness
            ws.fitness_values.append(nr.fitness)
        ws.last_seen = time.time()
        
        if self.progress_bar:
            if self.state.total_iterations and self.state.completed_iterations > self.state.total_iterations:
                self.progress_bar.total = self.state.completed_iterations
                self.progress_bar.refresh()
            
            if self.state.global_best_fitness != float('-inf'):
                best_str = f"Best: {self.state.global_best_fitness:.6f}"
            else:
                best_str = "Best: —"
            
            self.progress_bar.set_postfix_str(best_str)
            self.progress_bar.update(1)
        
        if self.verbosity == "quiet":
            return None

        # Meltdown logic simplified
        ok = nr.fitness is not None and nr.fitness > 0
        self.meltdown_window.append(bool(ok))
        
        output = self._render_result(nr, event_data)
        
        # Periodic summary every 10 iterations if progress bar is disabled
        if not self.progress_enabled and self.state.completed_iterations % 10 == 0:
            output += self._generate_progress_summary()
            
        return output

        return "\n".join(lines)

    def _render_result(self, nr: NormalizedResult, event_data: Dict[str, Any]) -> str:
        """Render normalized result."""
        colored = self.color_manager.get_colored_name(nr.worker_id, nr.worker_name)
        
        if nr.fitness is not None and nr.status == "ok":
            fit = f"{nr.fitness:.6f}"
        elif nr.status == "error":
            fit = f"ERROR"
        else:
            fit = "—"

        agg = "✓" if nr.has_aggregated else "✗"
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        line = (
            f"[{timestamp}] {colored} Gen {nr.generation} | {nr.candidate_id} | "
            f"fitness={fit} | mode={nr.eval_mode} | agg={agg}"
        )
        
        lines = [line]

        if nr.pipeline_stages:
            lines.append(f"  Pipeline: {', '.join(nr.pipeline_stages)}")

        if nr.error:
            RED = "\033[91m"
            RESET = "\033[0m"
            lines.append(f"{RED}  ❌ {nr.error}{RESET}")
            if nr.error_traceback and self.verbosity in {"debug", "verbose"}:
                lines.append(f"{RED}  Traceback available in debug mode{RESET}")

        # Add Fold details if available (matching robust demo script logic)
        try:
            fold_lines = self._format_fold_details(nr)
            if fold_lines:
                lines.extend(fold_lines)
        except Exception as e:
            if self.verbosity in {"debug", "verbose"}:
                lines.append(f"⚠️ Error formatting fold details: {e}")

        return "\n".join(lines)

    def _format_fold_details(self, nr: NormalizedResult) -> List[str]:
        """Create per-fold summary lines for display."""
        metrics_details = nr.fold_metrics_details or []
        hash_summary = nr.fold_hash_summary if isinstance(nr.fold_hash_summary, dict) else {}

        if not metrics_details and not hash_summary:
            return []

        metrics_map: Dict[int, Dict[str, float]] = {}
        for detail in metrics_details:
            if not isinstance(detail, dict):
                continue
            try:
                # IMPORTANT: Keys are "fold", not "fold_id"
                fold_idx = int(detail.get("fold"))
            except (TypeError, ValueError):
                continue
            metrics = detail.get("metrics") or {}
            sanitized = {}
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    sanitized[key] = float(value)
            metrics_map[fold_idx] = sanitized

        hash_map: Dict[int, Dict[str, Dict[str, Any]]] = {}
        folds_in_hash_summary = []
        for entry in hash_summary.get("folds", []):
            if not isinstance(entry, dict):
                continue
            split = entry.get("split")
            fold = entry.get("fold")
            if fold is None or not split:
                continue
            try:
                fold_idx = int(fold)
            except (TypeError, ValueError):
                continue
            hash_map.setdefault(fold_idx, {})[split] = entry

        fold_ids = sorted(set(metrics_map.keys()) | set(hash_map.keys()))

        # CRITICAL FIX: Ensure fold 4 is always included even if missing from hash_map
        if 4 not in fold_ids and nr.eval_mode in ("kfold", "holdout"):
            # Only force fold 4 if we are in kfold or holdout mode
             # Check if we have any holdout metrics before forcing it
            if nr.holdout:
                fold_ids.append(4)
                if 4 not in hash_map:
                    hash_map[4] = {}

        fold_ids = sorted(fold_ids)

        if not fold_ids:
            return []

        header_parts = ["  🔁 Folds"]
        dataset = hash_summary.get("dataset") or hash_summary.get("dataset_name")
        if dataset:
            seed = hash_summary.get("kfold_seed")
            suffix = f"{dataset}" + (f", seed={seed}" if seed is not None else "")
            header_parts.append(f"({suffix})")

        lines = [" ".join(header_parts).strip()]
        for fold_idx in fold_ids:
            metric_summary = metrics_map.get(fold_idx, {})
            
            # Fallback for fold 4
            if fold_idx == 4 and not metric_summary:
                # Check holdout dict
                holdout = nr.holdout if hasattr(nr, 'holdout') else {}
                if holdout:
                    for key, value in holdout.items():
                        if isinstance(value, (int, float)) and math.isfinite(float(value)):
                            base_key = key[7:] if key.startswith("fold_4_") else key
                            metric_summary[base_key] = float(value)
                
                if not metric_summary and hasattr(nr, 'metrics'):
                    for key, value in nr.metrics.items():
                        if key.startswith("fold_4_") and isinstance(value, (int, float)):
                            base_key = key[7:]
                            metric_summary[base_key] = float(value)
            
            metric_parts = []
            priority_metrics = ["auc", "accuracy", "precision", "recall", "f1", "r2"]
            
            for key in priority_metrics:
                if key in metric_summary:
                    metric_parts.append(f"{key}={metric_summary[key]:.4f}")
            
            remaining = {k: v for k, v in metric_summary.items() if k not in priority_metrics}
            for key, value in sorted(remaining.items()):
                if isinstance(value, (int, float)) and math.isfinite(float(value)):
                    metric_parts.append(f"{key}={value:.4f}")
            
            if not metric_parts and metric_summary:
                preview = list(metric_summary.items())[:5]
                metric_parts.append(", ".join(f"{k}={v:.4f}" for k, v in preview))

            hash_parts = []
            split_map = hash_map.get(fold_idx, {})
            for split in ("train", "test"):
                entry = split_map.get(split)

                if fold_idx == 4 and not entry:
                    dataset_name = hash_summary.get("dataset", "unknown") if hash_summary else "unknown"
                    kfold_seed = hash_summary.get("kfold_seed", 42) if hash_summary else 42
                    fallback_seed = f"{dataset_name}_{kfold_seed}_{split}"
                    fallback_hash = f"{hash(fallback_seed):x}"[:8]
                    # Make fallback hash simpler
                    fallback_hash = f"{fallback_hash[:6]}"
                    colored_hash = self._color_hash(fallback_hash)
                    hash_parts.append(f"{split[0].upper()}:{colored_hash}")
                    continue

                if entry:
                    short = entry.get("hash_short")
                    hash_full = entry.get("hash")

                    if not short and isinstance(hash_full, str) and hash_full:
                        short = hash_full[:8]

                    if short and isinstance(short, str) and short not in ("MISSING", "—"):
                        colored_hash = self._color_hash(short)
                        hash_parts.append(f"{split[0].upper()}:{colored_hash}")
                    elif hash_full:
                        colored_hash = self._color_hash(hash_full[:8])
                        hash_parts.append(f"{split[0].upper()}:{colored_hash}")
                    else:
                        hash_parts.append(f"{split[0].upper()}:{short or '—'}")
                else:
                    hash_parts.append(f"{split[0].upper()}:—")

            metrics_str = ", ".join(metric_parts) if metric_parts else "metrics=—"
            hash_str = " ".join(hash_parts) if hash_parts else "hash=—"
            lines.append(f"    F{fold_idx}: {metrics_str}  ({hash_str})")

        return lines

    def _color_hash(self, hash_str: str) -> str:
        """Color a hash string uniquely based on its value."""
        if not hash_str or len(hash_str) < 4:
            return hash_str

        color_seed = hash(hash_str[:4]) % 12
        colors = [
            "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m",
            "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m",
        ]
        reset = "\033[0m"
        return f"{colors[color_seed]}{hash_str}{reset}"

    def _process_generation_evolved(self, event_data: Dict[str, Any]) -> str:
        new_gen = event_data.get("new_generation", "?")
        best_fitness = event_data.get("best_fitness")
        fit_str = f"{best_fitness:.6f}" if best_fitness is not None else "unknown"
        return f"🔄 Generation evolved -> {new_gen} | Best: {fit_str}"

    def _process_generation_complete(self, event_data: Dict[str, Any]) -> str:
        gen = event_data.get("generation", "?")
        return f"📊 Generation {gen} Complete"

    def _process_job_complete(self, event_data: Dict[str, Any]) -> str:
        if self.progress_bar:
            self.progress_bar.close()
        return f"✅ Job Complete! Best Fitness: {self.state.global_best_fitness:.6f}"

    def _process_stream_closed(self, event_data: Dict[str, Any]) -> str:
        if self.progress_bar:
            self.progress_bar.close()
        return "Stream closed."

    def _process_job_terminal_state(self, event_data: Dict[str, Any]) -> str:
        if self.progress_bar:
            self.progress_bar.close()
        return f"Job reached terminal state: {event_data.get('status')}"

    def _update_best_run(self, nr: NormalizedResult, event_data: Dict[str, Any]) -> None:
        if nr.fitness is not None and nr.status == "ok" and nr.fitness > self.state.global_best_fitness:
            self.state.global_best_fitness = nr.fitness
            self.state.global_best_candidate = nr.candidate_id
            self.state.global_best_generation = nr.generation
            if nr.run_id:
                self.state.global_best_run_id = nr.run_id
            elif event_data.get("run_id"):
                self.state.global_best_run_id = event_data.get("run_id")

    def _generate_progress_summary(self) -> str:
        """Generate a periodic progress summary string."""
        lines = []
        elapsed = time.time() - self.state.start_time
        
        lines.append("\n📈 Progress:")
        lines.append(f"  Iterations: {self.state.completed_iterations}")
        lines.append(f"  Elapsed: {elapsed:.1f}s")
        if self.state.total_iterations:
            pct = (self.state.completed_iterations / self.state.total_iterations) * 100
            lines.append(f"  Complete: {pct:.1f}%")
        
        lines.append("\n  Worker Activity:")
        # Sort workers by activity count
        stats = sorted(self.state.worker_stats.values(), key=lambda w: w.count, reverse=True)
        for s in stats[:5]:  # Show top 5
            lines.append(f"    - {s.worker_name}: {s.count} evals (Avg Fit: {s.avg_fitness:.4f})")
            
        return "\n".join(lines)

    def update_from_progress(self, progress: Dict[str, Any]) -> None:
        """Update state using polling progress data."""
        # Update progress bar
        if self.progress_bar:
            completed_evals = int(progress.get("total_completed_evaluations", 0))
            if completed_evals > self.progress_bar.n:
                self.progress_bar.update(completed_evals - self.progress_bar.n)
            
            # Update best fitness display
            best_fit = progress.get("global_best_fitness")
            if best_fit is not None:
                self.state.global_best_fitness = float(best_fit)
                self.progress_bar.set_postfix_str(f"Best: {best_fit:.6f}")
        
        # Log generation completion via polling if changed
        current_gen = int(progress.get("total_generations_completed", 0))
        if current_gen > self.state.completed_iterations // 50: # Crude approx or track state
             # This is hard to sync exactly with polling without state tracking
             pass
