"""Dummy DOUG server utilities for local testing."""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler
from typing import Any, Dict, Optional

import socketserver


@dataclass
class RecordedRequest:
    path: str
    headers: Dict[str, str]
    payload: Dict[str, Any]


class _RecordingHandler(BaseHTTPRequestHandler):
    response_payload: Dict[str, Any] = {"status": "queued", "job_id": "dummy-job"}
    last_request: Optional[RecordedRequest] = None
    status_code: int = 200

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body) if body else {}
        _RecordingHandler.last_request = RecordedRequest(
            path=self.path,
            headers=dict(self.headers),
            payload=payload,
        )

        response = json.dumps(self.response_payload).encode("utf-8")
        self.send_response(self.status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003 - required signature
        return


class _ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


@dataclass
class DummyDougServer:
    """Context manager for running a dummy DOUG server in tests or demos."""

    host: str = "127.0.0.1"
    port: int = 0
    handler: type[BaseHTTPRequestHandler] = _RecordingHandler
    _server: _ThreadedTCPServer = field(init=False)
    _thread: threading.Thread = field(init=False)

    def __post_init__(self) -> None:
        self._server = _ThreadedTCPServer((self.host, self.port), self.handler)
        self.port = self._server.server_address[1]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def last_request(self) -> Optional[RecordedRequest]:
        return self.handler.last_request  # type: ignore[return-value]

    def start(self) -> None:
        self._thread.start()

    def shutdown(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=1)

    def __enter__(self) -> "DummyDougServer":
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.shutdown()


def run_dummy_server(host: str = "0.0.0.0", port: int = 8088) -> None:
    """Run a blocking dummy DOUG server printing submissions to stdout."""

    class _LoggingHandler(_RecordingHandler):
        pass

    with DummyDougServer(host=host, port=port, handler=_LoggingHandler) as server:
        print(f"[veox] Dummy DOUG server listening on {server.url}")
        try:
            server._thread.join()  # type: ignore[attr-defined]
        except KeyboardInterrupt:
            print("[veox] Dummy DOUG server shutting down…")

