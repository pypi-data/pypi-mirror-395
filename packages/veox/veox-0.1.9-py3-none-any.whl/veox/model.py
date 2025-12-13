"""Core data structures and validation helpers for the Veox package."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Mapping, Sequence


class VeoxDataError(ValueError):
    """Raised when training or inference data cannot be coerced into a matrix."""


def _ensure_row(row: Iterable[float], index: int) -> List[float]:
    try:
        coerced = [float(value) for value in row]
    except TypeError as exc:
        raise VeoxDataError(f"Row {index} is not iterable: {row!r}") from exc
    except ValueError as exc:
        raise VeoxDataError(f"Row {index} contains non-numeric data: {row!r}") from exc

    if not coerced:
        raise VeoxDataError(f"Row {index} is empty.")

    return coerced


def prepare_matrix(X: Sequence[Iterable[float]]) -> List[List[float]]:
    """Validate and normalize feature input into a dense float matrix."""
    if not isinstance(X, Sequence) or len(X) == 0:
        raise VeoxDataError("Input data must be a non-empty sequence of rows.")

    matrix = [_ensure_row(row, idx) for idx, row in enumerate(X)]
    expected_features = len(matrix[0])

    for idx, row in enumerate(matrix):
        if len(row) != expected_features:
            raise VeoxDataError(
                f"Row {idx} has {len(row)} features, expected {expected_features}."
            )

    return matrix


def compute_column_means(matrix: Sequence[Sequence[float]]) -> List[float]:
    """Compute column-wise means for a dense matrix."""
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    sums = [0.0] * n_cols

    for row in matrix:
        for col_idx, value in enumerate(row):
            sums[col_idx] += value

    return [total / n_rows for total in sums]


@dataclass
class VeoxState:
    """State container for fitted Veox models."""

    n_features: int
    column_means: List[float]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def is_fitted(self) -> bool:
        return self.n_features > 0 and len(self.column_means) == self.n_features

    def to_dict(self) -> Dict[str, object]:
        return {
            "n_features": self.n_features,
            "column_means": self.column_means,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> "VeoxState":
        created_at = payload.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return cls(
            n_features=int(payload["n_features"]),
            column_means=[float(value) for value in payload["column_means"]],
            created_at=created_at if isinstance(created_at, datetime) else datetime.now(timezone.utc),
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass
class DougConfig:
    """Runtime configuration for interacting with the DOUG scheduler."""

    base_url: str
    api_key: str | None = None
    timeout: float = 30.0

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "DougConfig | None":
        env = environ or os.environ
        base_url = env.get("VEOX_DOUG_BASE_URL")
        if not base_url:
            return None

        api_key = env.get("VEOX_DOUG_API_KEY")
        timeout_raw = env.get("VEOX_DOUG_TIMEOUT")
        timeout = float(timeout_raw) if timeout_raw else 30.0
        return cls(base_url=base_url, api_key=api_key, timeout=timeout)

    def headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

