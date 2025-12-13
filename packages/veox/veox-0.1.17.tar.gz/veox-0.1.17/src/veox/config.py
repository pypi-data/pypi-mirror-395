"""Configuration classes for DOUG evolution demos."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import os


@dataclass
class APIConfig:
    """API connection configuration."""
    url: str
    api_key: Optional[str] = None
    connect_timeout: int = 30
    read_timeout: int = 30


@dataclass
class JobConfig:
    """Job submission configuration."""
    task: str = "binary"  # binary, regression, optimization
    population: int = 50
    generations: int = 10
    dataset: str = "SECOM"
    name: Optional[str] = None
    max_samples: Optional[int] = None
    seed: Optional[int] = None
    fitness: Optional[str] = None
    timeout: Optional[int] = None  # Job-level timeout in seconds
    async_evolution: bool = False
    async_threshold: float = 0.8  # Job-level timeout in seconds
    task_timeout: Optional[int] = None  # Per-task timeout in seconds (overrides calculated value)


@dataclass
class StreamingConfig:
    """Event streaming configuration."""
    timeout: int = 900
    refresh_interval: float = 1.0
    show_details: bool = True
    show_pipeline: bool = True
    show_metrics: bool = True
    verbosity: str = "basic"  # "quiet" | "basic" | "verbose" | "debug"
    once_per_gen_warnings: bool = True
    meltdown_window: int = 30  # Consecutive results checked for meltdown detector
    debug: bool = False  # Enable debug logging for errors


@dataclass
class ArtifactsConfig:
    """Artifacts and output configuration."""
    directory: Optional[Path] = None
    save_payload: bool = True
    save_sse_log: bool = True
    save_summary: bool = True


@dataclass
class EvolutionDemoConfig:
    """Complete configuration for evolution demos."""
    api: APIConfig
    job: JobConfig
    streaming: StreamingConfig = field(default_factory=StreamingConfig)
    artifacts: ArtifactsConfig = field(default_factory=ArtifactsConfig)

    @classmethod
    def from_env(cls, **overrides) -> "EvolutionDemoConfig":
        """Create config from environment variables with optional overrides."""
        # Extract API config from overrides or environment
        api_url = overrides.pop("api_url", None) or os.environ.get("DOUG_API_URL", "http://127.0.0.1:8088")
        api_key = overrides.pop("api_key", None) or os.environ.get("DOUG_API_KEY", "local-dev")

        # Create defaults for components that weren't provided
        defaults = {
            "api": APIConfig(url=api_url, api_key=api_key),
            "job": JobConfig(),
            "streaming": StreamingConfig(),
            "artifacts": ArtifactsConfig(),
        }

        # Override defaults with provided values
        defaults.update(overrides)

        return cls(**defaults)
