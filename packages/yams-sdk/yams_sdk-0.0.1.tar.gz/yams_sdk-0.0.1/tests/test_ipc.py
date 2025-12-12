"""Tests for ipc.py - Transport placeholders."""

from __future__ import annotations

import pytest

from yams_sdk.ipc import CliBridgeTransport, UnixSocketTransport


def test_unix_socket_transport_init():
    """Test UnixSocketTransport initialization."""
    transport = UnixSocketTransport()
    assert transport.socket_path is None

    transport = UnixSocketTransport("/var/run/yams.sock")
    assert transport.socket_path == "/var/run/yams.sock"


def test_unix_socket_transport_call_raises():
    """Test that call raises NotImplementedError."""
    transport = UnixSocketTransport()
    with pytest.raises(NotImplementedError, match="not implemented"):
        transport.call("test_method")


def test_cli_bridge_transport_init():
    """Test CliBridgeTransport initialization."""
    transport = CliBridgeTransport()
    assert transport.yams_path == "yams"

    transport = CliBridgeTransport("/usr/local/bin/yams")
    assert transport.yams_path == "/usr/local/bin/yams"


def test_cli_bridge_transport_call_raises():
    """Test that call raises NotImplementedError."""
    transport = CliBridgeTransport()
    with pytest.raises(NotImplementedError, match="not implemented"):
        transport.call("test_method", "arg1", "arg2")
