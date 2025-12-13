"""Utilities for interacting with the DOUG scheduler via HTTP."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, MutableMapping
from urllib import error, request


class VeoxDougError(RuntimeError):
    """Raised when communication with the DOUG scheduler fails."""


@dataclass
class DougResponse:
    status: int
    body: Dict[str, Any]
    headers: Mapping[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "body": self.body, "headers": dict(self.headers)}


def post_json(
    url: str,
    payload: Mapping[str, Any],
    *,
    headers: Mapping[str, str] | None = None,
    timeout: float | None = None,
) -> DougResponse:
    data = json.dumps(payload).encode("utf-8")
    all_headers: MutableMapping[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if headers:
        all_headers.update(headers)

    req = request.Request(url, data=data, headers=dict(all_headers), method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                raise VeoxDougError(f"Non-JSON response from DOUG: {raw!r}") from None
            return DougResponse(status=resp.status, body=body, headers=dict(resp.headers))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise VeoxDougError(
            f"DOUG returned HTTP {exc.code} for {url}: {detail or exc.reason}"
        ) from exc
    except error.URLError as exc:
        raise VeoxDougError(f"Unable to reach DOUG at {url}: {exc.reason}") from exc

