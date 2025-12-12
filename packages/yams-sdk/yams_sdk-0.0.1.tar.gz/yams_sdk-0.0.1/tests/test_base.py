"""Tests for base.py - BasePlugin JSON-RPC infrastructure."""

from __future__ import annotations

import io
import json
import sys
from typing import Any
from unittest.mock import patch

import pytest

from yams_sdk.base import BasePlugin


class SamplePlugin(BasePlugin):
    """Sample plugin implementation for testing."""

    def __init__(self):
        super().__init__()
        self.initialized = False
        self.shutdown_called = False
        self.init_config = None
        # Register a custom RPC method
        self.register("test.echo", self._echo)
        self.register("test.add", self._add)

    def manifest(self) -> dict[str, Any]:
        return {
            "name": "test_plugin",
            "version": "1.0.0",
            "interfaces": ["test_v1"],
        }

    def init(self, config: dict[str, Any]) -> None:
        self.initialized = True
        self.init_config = config

    def health(self) -> dict[str, Any]:
        return {"status": "ok", "initialized": self.initialized}

    def shutdown(self) -> None:
        self.shutdown_called = True

    def _echo(self, message: str = "") -> str:
        return message

    def _add(self, a: int, b: int) -> int:
        return a + b


class UnimplementedPlugin(BasePlugin):
    """Plugin that doesn't implement manifest()."""

    pass


def test_base_plugin_manifest_not_implemented():
    """Test that BasePlugin.manifest() raises NotImplementedError."""
    plugin = UnimplementedPlugin()
    with pytest.raises(NotImplementedError, match="must implement manifest"):
        plugin.manifest()


def test_sample_plugin_manifest():
    """Test manifest returns expected structure."""
    plugin = SamplePlugin()
    m = plugin.manifest()
    assert m["name"] == "test_plugin"
    assert m["version"] == "1.0.0"
    assert "test_v1" in m["interfaces"]


def test_plugin_init():
    """Test plugin initialization."""
    plugin = SamplePlugin()
    assert not plugin.initialized
    plugin.init({"key": "value"})
    assert plugin.initialized
    assert plugin.init_config == {"key": "value"}


def test_plugin_health():
    """Test plugin health check."""
    plugin = SamplePlugin()
    h = plugin.health()
    assert h["status"] == "ok"
    assert h["initialized"] is False

    plugin.init({})
    h = plugin.health()
    assert h["initialized"] is True


def test_plugin_shutdown():
    """Test plugin shutdown."""
    plugin = SamplePlugin()
    assert not plugin.shutdown_called
    plugin.shutdown()
    assert plugin.shutdown_called


def test_register_method():
    """Test registering RPC methods."""
    plugin = SamplePlugin()
    assert "test.echo" in plugin._rpc_methods
    assert "test.add" in plugin._rpc_methods
    assert "handshake.manifest" in plugin._rpc_methods


def test_send_response(capsys):
    """Test _send_response outputs JSON-RPC response."""
    plugin = SamplePlugin()
    plugin._send_response(1, result={"data": "test"})

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert response["result"] == {"data": "test"}


def test_send_response_with_error(capsys):
    """Test _send_response with error."""
    plugin = SamplePlugin()
    plugin._send_response(2, error={"code": -32600, "message": "Invalid"})

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["id"] == 2
    assert response["error"]["code"] == -32600


def test_send_error(capsys):
    """Test _send_error helper."""
    plugin = SamplePlugin()
    plugin._send_error(3, -32601, "Method not found", data={"method": "unknown"})

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32601
    assert response["error"]["message"] == "Method not found"
    assert response["error"]["data"] == {"method": "unknown"}


def test_handle_request_with_dict_params(capsys):
    """Test handling request with dict params."""
    plugin = SamplePlugin()
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "test.echo",
        "params": {"message": "hello"},
    }
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["result"] == "hello"


def test_handle_request_with_list_params(capsys):
    """Test handling request with list params."""
    plugin = SamplePlugin()
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "test.add",
        "params": [3, 5],
    }
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["result"] == 8


def test_handle_request_missing_method(capsys):
    """Test handling request with missing method."""
    plugin = SamplePlugin()
    request = {"jsonrpc": "2.0", "id": 1}
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32600
    assert "missing method" in response["error"]["message"]


def test_handle_request_method_not_found(capsys):
    """Test handling request for unknown method."""
    plugin = SamplePlugin()
    request = {"jsonrpc": "2.0", "id": 1, "method": "unknown.method"}
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32601
    assert "not found" in response["error"]["message"]


def test_handle_request_invalid_params(capsys):
    """Test handling request with invalid params (TypeError)."""
    plugin = SamplePlugin()
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "test.add",
        "params": {"wrong": "params"},  # add expects a, b
    }
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32602
    assert "Invalid params" in response["error"]["message"]


def test_handle_request_internal_error(capsys):
    """Test handling request that raises an exception."""
    plugin = SamplePlugin()

    def failing_method():
        raise ValueError("Something went wrong")

    plugin.register("test.fail", failing_method)

    request = {"jsonrpc": "2.0", "id": 1, "method": "test.fail"}
    plugin._handle_request(request)

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32603
    assert "Internal error" in response["error"]["message"]


def test_handle_request_notification_no_response(capsys):
    """Test that notifications (no id) don't produce responses."""
    plugin = SamplePlugin()
    request = {"jsonrpc": "2.0", "method": "test.echo", "params": {"message": "hi"}}
    plugin._handle_request(request)

    captured = capsys.readouterr()
    assert captured.out == ""


def test_lifecycle_handlers(capsys):
    """Test standard lifecycle RPC handlers."""
    plugin = SamplePlugin()

    # Test handshake.manifest
    request = {"jsonrpc": "2.0", "id": 1, "method": "handshake.manifest"}
    plugin._handle_request(request)
    response = json.loads(capsys.readouterr().out.strip())
    assert response["result"]["name"] == "test_plugin"

    # Test plugin.init
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "plugin.init",
        "params": {"config": {"setting": "value"}},
    }
    plugin._handle_request(request)
    response = json.loads(capsys.readouterr().out.strip())
    assert response["result"]["status"] == "initialized"

    # Test plugin.health
    request = {"jsonrpc": "2.0", "id": 3, "method": "plugin.health"}
    plugin._handle_request(request)
    response = json.loads(capsys.readouterr().out.strip())
    assert response["result"]["status"] == "ok"

    # Test plugin.shutdown
    request = {"jsonrpc": "2.0", "id": 4, "method": "plugin.shutdown"}
    plugin._handle_request(request)
    response = json.loads(capsys.readouterr().out.strip())
    assert response["result"] is None
    assert plugin.shutdown_called


def test_run_processes_stdin(capsys):
    """Test run() processes stdin line by line."""
    plugin = SamplePlugin()

    input_lines = [
        json.dumps({"jsonrpc": "2.0", "id": 1, "method": "test.echo", "params": {"message": "a"}}),
        "",  # Empty line should be skipped
        json.dumps({"jsonrpc": "2.0", "id": 2, "method": "test.add", "params": [1, 2]}),
    ]

    with patch.object(sys, "stdin", io.StringIO("\n".join(input_lines))):
        plugin.run()

    captured = capsys.readouterr()
    lines = [json.loads(line) for line in captured.out.strip().split("\n")]
    assert len(lines) == 2
    assert lines[0]["result"] == "a"
    assert lines[1]["result"] == 3


def test_run_handles_parse_error(capsys):
    """Test run() handles JSON parse errors."""
    plugin = SamplePlugin()

    input_lines = ["not valid json {{{"]

    with patch.object(sys, "stdin", io.StringIO("\n".join(input_lines))):
        plugin.run()

    captured = capsys.readouterr()
    response = json.loads(captured.out.strip())
    assert response["error"]["code"] == -32700
    assert "Parse error" in response["error"]["message"]
