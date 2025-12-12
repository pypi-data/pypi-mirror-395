"""Base plugin infrastructure for YAMS Python plugins using JSON-RPC over stdio."""

from __future__ import annotations

import json
import sys
from typing import Any, Callable


class BasePlugin:
    """Base class for YAMS external plugins using JSON-RPC over stdio.

    External plugins communicate with the YAMS daemon via newline-delimited
    JSON-RPC messages over stdin/stdout. This base class handles the protocol
    plumbing, letting subclasses focus on implementing plugin-specific logic.

    Subclasses should:
    1. Implement manifest() to return plugin metadata
    2. Implement init() to configure the plugin
    3. Implement health() to report plugin status
    4. Use @rpc decorator to expose RPC methods
    """

    def __init__(self) -> None:
        self._rpc_methods: dict[str, Callable] = {}
        # Register standard lifecycle methods
        self.register("handshake.manifest", self._handle_manifest)
        self.register("plugin.init", self._handle_init)
        self.register("plugin.health", self._handle_health)
        self.register("plugin.shutdown", self._handle_shutdown)

    def register(self, method_name: str, handler: Callable) -> None:
        """Register an RPC method handler."""
        self._rpc_methods[method_name] = handler

    def manifest(self) -> dict[str, Any]:
        """Return plugin manifest with name, version, and interfaces.

        Subclasses MUST override this method.

        Example:
            {
                "name": "my_plugin",
                "version": "1.0.0",
                "interfaces": ["content_extractor_v1"]
            }
        """
        raise NotImplementedError("Subclass must implement manifest()")

    def init(self, config: dict[str, Any]) -> None:
        """Initialize the plugin with provided configuration.

        Subclasses SHOULD override this method if they need configuration.

        Args:
            config: Configuration dictionary from daemon
        """
        pass

    def health(self) -> dict[str, Any]:
        """Return plugin health status.

        Subclasses SHOULD override this method.

        Returns:
            Health status dict, typically {"status": "ok"|"degraded"|"error", ...}
        """
        return {"status": "ok"}

    def shutdown(self) -> None:
        """Shutdown and cleanup plugin resources.

        Subclasses SHOULD override this if they need cleanup.
        """
        pass

    def _handle_manifest(self, **kwargs) -> dict[str, Any]:
        """Handle handshake.manifest RPC."""
        return self.manifest()

    def _handle_init(self, config: dict[str, Any] | None = None, **kwargs) -> dict[str, Any]:
        """Handle plugin.init RPC."""
        self.init(config or {})
        return {"status": "initialized"}

    def _handle_health(self, **kwargs) -> dict[str, Any]:
        """Handle plugin.health RPC."""
        return self.health()

    def _handle_shutdown(self, **kwargs) -> None:
        """Handle plugin.shutdown RPC."""
        self.shutdown()
        return None

    def _send_response(
        self, response_id: str | int | None, result: Any = None, error: dict[str, Any] | None = None
    ) -> None:
        """Send a JSON-RPC response to stdout."""
        response: dict[str, Any] = {"jsonrpc": "2.0", "id": response_id}
        if error is not None:
            response["error"] = error
        else:
            response["result"] = result
        print(json.dumps(response), flush=True)

    def _send_error(
        self, response_id: str | int | None, code: int, message: str, data: Any = None
    ) -> None:
        """Send a JSON-RPC error response."""
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        self._send_response(response_id, error=error)

    def _handle_request(self, request: dict[str, Any]) -> None:
        """Handle a single JSON-RPC request."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not method:
            self._send_error(req_id, -32600, "Invalid Request: missing method")
            return

        handler = self._rpc_methods.get(method)
        if not handler:
            self._send_error(req_id, -32601, f"Method not found: {method}")
            return

        try:
            # Support both dict and list params
            if isinstance(params, dict):
                result = handler(**params)
            elif isinstance(params, list):
                result = handler(*params)
            else:
                result = handler()

            # Notifications (no id) don't get responses
            if req_id is not None:
                self._send_response(req_id, result=result)
        except TypeError as e:
            self._send_error(req_id, -32602, f"Invalid params: {e}")
        except Exception as e:
            self._send_error(req_id, -32603, f"Internal error: {e}")

    def run(self) -> None:
        """Run the plugin's main loop, reading JSON-RPC requests from stdin.

        This method blocks and processes stdin line-by-line until EOF or shutdown.
        """
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                self._handle_request(request)
            except json.JSONDecodeError as e:
                # Parse error - send error if we can determine an id
                self._send_error(None, -32700, f"Parse error: {e}")
            except Exception as e:
                # Unexpected error in request handling
                self._send_error(None, -32603, f"Internal error: {e}")
