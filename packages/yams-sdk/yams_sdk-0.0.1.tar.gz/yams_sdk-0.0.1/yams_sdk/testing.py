"""Testing utilities for YAMS plugins.

This module provides helpers for testing plugin implementations,
including mock transports, validation utilities, and test harnesses.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any


class PluginTestHarness:
    """Test harness for external JSON-RPC plugins.

    Spawns a plugin process and communicates via stdin/stdout.
    """

    def __init__(self, command: list[str]):
        """Initialize harness with plugin command.

        Args:
            command: Command to spawn plugin (e.g., ["python", "plugin.py"])
        """
        self.command = command
        self.process: subprocess.Popen | None = None
        self._request_id = 0

    def start(self) -> None:
        """Start the plugin process."""
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def stop(self) -> None:
        """Stop the plugin process."""
        if self.process:
            try:
                # Try graceful shutdown
                self.call("plugin.shutdown", {})
            except Exception:
                pass
            self.process.terminate()
            self.process.wait(timeout=5)
            self.process = None

    def call(self, method: str, params: Any) -> Any:
        """Call an RPC method on the plugin.

        Args:
            method: RPC method name
            params: Method parameters (dict or list)

        Returns:
            Result from plugin

        Raises:
            RuntimeError: If plugin returns an error
            TimeoutError: If no response received
        """
        if not self.process:
            raise RuntimeError("Plugin not started")

        self._request_id += 1
        request = {"jsonrpc": "2.0", "id": self._request_id, "method": method, "params": params}

        # Send request
        request_line = json.dumps(request) + "\n"
        self.process.stdin.write(request_line)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise TimeoutError("No response from plugin")

        response = json.loads(response_line)

        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"Plugin error: {error.get('message', error)}")

        return response.get("result")

    def handshake(self) -> dict[str, Any]:
        """Perform handshake and get manifest.

        Returns:
            Plugin manifest dict
        """
        return self.call("handshake.manifest", {})

    def init(self, config: dict[str, Any]) -> dict[str, Any]:
        """Initialize plugin with config.

        Args:
            config: Configuration dict

        Returns:
            Initialization result
        """
        return self.call("plugin.init", {"config": config})

    def health(self) -> dict[str, Any]:
        """Check plugin health.

        Returns:
            Health status dict
        """
        return self.call("plugin.health", {})

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a plugin manifest structure.

    Args:
        manifest: Manifest dict to validate

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    if not isinstance(manifest, dict):
        return ["Manifest must be a dictionary"]

    # Required fields
    if "name" not in manifest:
        errors.append("Missing required field: name")
    elif not isinstance(manifest["name"], str):
        errors.append("Field 'name' must be a string")

    if "version" not in manifest:
        errors.append("Missing required field: version")
    elif not isinstance(manifest["version"], str):
        errors.append("Field 'version' must be a string")

    if "interfaces" not in manifest:
        errors.append("Missing required field: interfaces")
    elif not isinstance(manifest["interfaces"], list):
        errors.append("Field 'interfaces' must be a list")
    else:
        for i, iface in enumerate(manifest["interfaces"]):
            if not isinstance(iface, (str, dict)):
                errors.append(f"Interface {i} must be string or dict")
            elif isinstance(iface, dict):
                if "id" not in iface:
                    errors.append(f"Interface {i} missing 'id' field")
                if "version" not in iface:
                    errors.append(f"Interface {i} missing 'version' field")

    return errors


def validate_health(health: dict[str, Any]) -> list[str]:
    """Validate a health response structure.

    Args:
        health: Health dict to validate

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    if not isinstance(health, dict):
        return ["Health must be a dictionary"]

    if "status" in health:
        if health["status"] not in ["ok", "degraded", "error"]:
            errors.append("Status must be 'ok', 'degraded', or 'error'")

    return errors


class MockContentExtractor:
    """Mock content extractor for testing."""

    def __init__(self, supported_types: list[tuple[str, str]]):
        """Initialize mock extractor.

        Args:
            supported_types: List of (mime_type, extension) tuples
        """
        self.supported_types = supported_types
        self.extract_calls = []

    def supports(self, mime_type: str, extension: str) -> bool:
        """Check if mime type is supported."""
        return (mime_type, extension) in self.supported_types

    def extract(self, content: bytes) -> dict[str, Any]:
        """Extract content (returns mock data)."""
        self.extract_calls.append(content)
        return {
            "text": f"Extracted text from {len(content)} bytes",
            "metadata": {"size": len(content)},
            "error": None,
        }
