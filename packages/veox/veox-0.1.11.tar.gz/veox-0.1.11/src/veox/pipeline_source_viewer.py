"""Pipeline source code viewer for displaying best pipeline source in bright green."""

import sys
from typing import Optional, Dict, Any, List

import requests

# Handle both relative imports (when imported as module) and direct imports (when run as script)
try:
    from .config import APIConfig
except ImportError:
    # Fallback for when run directly as script
    from config import APIConfig


def _is_tty() -> bool:
    """Check if stdout is a TTY (terminal)."""
    return sys.stdout.isatty()


def _fetch_pipeline_full(api_config: APIConfig, run_id: str) -> Optional[Dict[str, Any]]:
    """Fetch full pipeline specification with source code from API."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    if api_config.api_key:
        session.headers.update({"X-API-Key": api_config.api_key})
    session.timeout = (api_config.connect_timeout, api_config.read_timeout)
    
    url = f"{api_config.url}/v1/runs/{run_id}/pipeline/full"
    try:
        response = session.get(url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def _sanitize_identifier(name: str, fallback: str) -> str:
    """Sanitize a name into a safe identifier without altering valid class names."""
    if not name:
        return fallback
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in name)
    if not cleaned:
        return fallback
    if cleaned[0].isdigit():
        cleaned = f"Stage_{cleaned}"
    return cleaned


def _build_pipeline_code(stages: List[Dict[str, Any]]) -> str:
    """Generate monolithic pipeline wrapper code that wires all stages together."""
    if not stages:
        return ""

    transform_entries: List[str] = []
    model_entries: List[str] = []
    fusion_ctor: Optional[str] = None

    for idx, stage in enumerate(stages):
        role_raw = stage.get("stage") or stage.get("role") or f"stage_{idx}"
        role = str(role_raw)
        name_candidate = stage.get("name") or stage.get("label") or stage.get("stage") or f"Stage{idx}"
        class_name = _sanitize_identifier(name_candidate, f"Stage{idx}")
        entry = f"            ('{role}', {class_name}()),"
        lower_role = role.lower()

        if lower_role.startswith("model"):
            model_entries.append(entry)
        elif "fusion" in lower_role:
            fusion_ctor = f"        self._fusion_stage = {class_name}()"
        else:
            transform_entries.append(entry)

    if not transform_entries and not model_entries:
        return ""

    if not fusion_ctor:
        fusion_ctor = "        self._fusion_stage = None"

    lines: List[str] = [
        "class DougBestPipeline:",
        "    def __init__(self):",
        "        self._transforms = [",
    ]
    lines.extend(transform_entries)
    lines.append("        ]")
    lines.append("        self._model_stages = [")
    lines.extend(model_entries)
    lines.append("        ]")
    lines.append(fusion_ctor)
    lines.append("        self._fitted = False")
    lines.append("")
    lines.append("    def _prepare_features(self, X, y=None, training=False):")
    lines.append("        data = X")
    lines.append("        for _, stage in self._transforms:")
    lines.append("            if training and hasattr(stage, 'fit'):")
    lines.append("                try:")
    lines.append("                    stage.fit(data, y)")
    lines.append("                except TypeError:")
    lines.append("                    stage.fit(data)")
    lines.append("            if hasattr(stage, 'transform'):")
    lines.append("                data = stage.transform(data)")
    lines.append("        return data")
    lines.append("")
    lines.append("    def fit(self, X, y):")
    lines.append("        features = self._prepare_features(X, y, training=True)")
    lines.append("        for _, model in self._model_stages:")
    lines.append("            model.fit(features, y)")
    lines.append("        self._fitted = True")
    lines.append("        return self")
    lines.append("")
    lines.append("    def predict_proba(self, X):")
    lines.append("        if not self._fitted:")
    lines.append("            raise RuntimeError('DougBestPipeline must call fit() before predict_proba().')")
    lines.append("        features = self._prepare_features(X, training=False)")
    lines.append("        probabilities = []")
    lines.append("        for _, model in self._model_stages:")
    lines.append("            if hasattr(model, 'predict_proba'):")
    lines.append("                probabilities.append(model.predict_proba(features))")
    lines.append("            elif hasattr(model, 'predict'):")
    lines.append("                preds = model.predict(features)")
    lines.append("                stacked = np.column_stack((1 - preds, preds))")
    lines.append("                probabilities.append(stacked)")
    lines.append("        if not probabilities:")
    lines.append("            raise RuntimeError('No probabilistic outputs available for prediction.')")
    lines.append("        fused = probabilities[0]")
    lines.append("        if self._fusion_stage and len(probabilities) > 1:")
    lines.append("            for extra in probabilities[1:]:")
    lines.append("                fused = self._fusion_stage.combine(fused, extra)")
    lines.append("            return fused")
    lines.append("        return fused")
    lines.append("")
    lines.append("    def predict(self, X):")
    lines.append("        proba = self.predict_proba(X)")
    lines.append("        if hasattr(proba, 'ndim') and proba.ndim > 1:")
    lines.append("            return np.argmax(proba, axis=1)")
    lines.append("        return (proba >= 0.5).astype(int)")

    return "\n".join(lines)


def _format_pipeline_source(pipeline_data: Dict[str, Any], run_id: str, fitness: Optional[float]) -> str:
    """Format pipeline source code for display."""
    lines = []
    
    # Color codes
    BRIGHT_GREEN = "\033[92m" if _is_tty() else ""
    BRIGHT_YELLOW = "\033[93m" if _is_tty() else ""
    BRIGHT_PINK = "\033[95m" if _is_tty() else ""
    BOLD = "\033[1m" if _is_tty() else ""
    RESET = "\033[0m" if _is_tty() else ""
    
    # Header
    banner = f"{BRIGHT_PINK}{'═' * 80}{RESET}" if _is_tty() else "=" * 80
    inner_banner = f"{BRIGHT_PINK}{BOLD}💖 SHOW ME THE CODE 💖{RESET}" if _is_tty() else "SHOW ME THE CODE"
    footer_banner = f"{BRIGHT_PINK}{BOLD}💖 END OF BEST CODE 💖{RESET}" if _is_tty() else "END OF BEST CODE"
    
    lines.append("")
    lines.append(banner)
    lines.append(f"{BOLD}🏆 BEST PIPELINE SOURCE CODE{RESET}")
    lines.append(banner)
    
    if fitness is not None:
        lines.append(f"Run ID: {run_id}")
        lines.append(f"Fitness: {fitness:.6f}")
    else:
        lines.append(f"Run ID: {run_id}")
    
    pipeline_id = pipeline_data.get("pipeline_id", "unknown")
    lines.append(f"Pipeline ID: {pipeline_id}")
    lines.append("")
    
    # Process stages as a single monolithic string
    stages = pipeline_data.get("stages", [])
    if not stages:
        lines.append("⚠️  No pipeline stages found in response.")
        lines.append(banner)
        return "\n".join(lines)
    
    code_chunks = []
    missing_chunks = 0
    for stage in stages:
        source_code = stage.get("source") or stage.get("code")
        if source_code:
            code_chunks.append(source_code.strip())
        else:
            missing_chunks += 1
    
    pipeline_code = _build_pipeline_code(stages)

    if not code_chunks:
        lines.append("⚠️  No source code published for this pipeline.")
        lines.append(banner)
        return "\n".join(lines)
    
    if missing_chunks:
        lines.append(f"⚠️  {missing_chunks} stage(s) omitted (no source provided).")
        lines.append("")
    
    monolithic_source = "\n\n".join(code_chunks)
    
    lines.append(banner)
    lines.append(inner_banner)
    lines.append(banner)
    for line in monolithic_source.splitlines():
        lines.append(f"{BRIGHT_GREEN}{line}{RESET}")
    if pipeline_code:
        lines.append("")  # Extra space between green and yellow code
        for line in pipeline_code.strip("\n").splitlines():
            lines.append(f"{BRIGHT_YELLOW}{line}{RESET}")
    lines.append(banner)
    lines.append(footer_banner)
    lines.append(banner)
    return "\n".join(lines)


def display_best_pipeline(api_config: APIConfig, run_id: str, fitness: Optional[float] = None) -> bool:
    """Fetch and display the best pipeline source code in bright green.
    
    Args:
        api_config: API configuration for making requests
        run_id: Run ID to fetch pipeline for
        fitness: Optional fitness value to display in header
        
    Returns:
        True if successfully displayed, False otherwise
    """
    if not run_id:
        print("⚠️  No run ID provided for best pipeline display.")
        return False
    
    # Fetch pipeline data
    pipeline_data = _fetch_pipeline_full(api_config, run_id)
    
    if not pipeline_data:
        print(f"⚠️  Could not fetch pipeline source for run {run_id}.")
        print("   This may happen if the run is still processing or the endpoint is unavailable.")
        return False
    
    # Format and display
    formatted_output = _format_pipeline_source(pipeline_data, run_id, fitness)
    print(formatted_output)
    
    return True
