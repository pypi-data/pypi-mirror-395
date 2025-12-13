"""
HTTP Adapter for ForgeBase.

Provides REST API for executing UseCases via HTTP.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from urllib.parse import urlparse

from forgebase.adapters.adapter_base import AdapterBase


class HTTPAdapter(AdapterBase):
    """
    HTTP REST API adapter.

    Exposes UseCases via REST endpoints without heavy framework dependencies.

    Example::

        adapter = HTTPAdapter(usecases={'create_user': CreateUserUseCase()})
        adapter.serve(port=8000)
    """

    def __init__(self, usecases: dict[str, Any] | None = None):
        """
        Initialize HTTP adapter.

        :param usecases: Dictionary mapping names to UseCase instances
        :type usecases: Optional[Dict[str, Any]]
        """
        self.usecases = usecases or {}

    def serve(self, host: str = 'localhost', port: int = 8000) -> None:
        """
        Start HTTP server.

        :param host: Host to bind
        :type host: str
        :param port: Port to bind
        :type port: int
        """
        handler = self._make_handler()
        server = HTTPServer((host, port), handler)
        print(f"ForgeBase HTTP server running on http://{host}:{port}")
        server.serve_forever()

    def _make_handler(self):
        """Create request handler class."""
        adapter = self

        class ForgeBaseHandler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                """Handle GET requests."""
                path = urlparse(self.path).path

                if path == '/health':
                    self._send_json({'status': 'ok'})
                elif path == '/usecases':
                    self._send_json({
                        'usecases': list(adapter.usecases.keys())
                    })
                else:
                    self._send_error(404, 'Not found')

            def do_POST(self):  # noqa: N802
                """Handle POST requests."""
                path = urlparse(self.path).path

                if path.startswith('/usecases/') and path.endswith('/execute'):
                    usecase_name = path.split('/')[2]
                    self._execute_usecase(usecase_name)
                else:
                    self._send_error(404, 'Not found')

            def _execute_usecase(self, name: str):
                """Execute a UseCase."""
                if name not in adapter.usecases:
                    self._send_error(404, f"UseCase '{name}' not found")
                    return

                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length)
                    data = json.loads(body) if body else {}

                    usecase = adapter.usecases[name]
                    result = usecase.execute(**data)

                    self._send_json({
                        'success': True,
                        'result': str(result)
                    })
                except Exception as e:
                    self._send_error(500, str(e))

            def _send_json(self, data: dict):
                """Send JSON response."""
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            def _send_error(self, code: int, message: str):
                """Send error response."""
                self.send_response(code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': message}).encode())

            def log_message(self, format, *args):
                """Suppress default logging."""
                pass

        return ForgeBaseHandler

    def name(self) -> str:
        """Get adapter name."""
        return "HTTPAdapter"

    def module(self) -> str:
        """Get module name."""
        return "forgebase.adapters.http"

    def _instrument(self) -> None:
        """Instrument adapter."""
        pass
