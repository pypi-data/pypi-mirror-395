from __future__ import annotations


class UnixSocketTransport:
    """Placeholder UNIX socket transport to the YAMS daemon.

    The daemon exposes an internal IPC protocol. This transport will connect to
    a future graph endpoint once available. For now, it raises NotImplementedError.
    """

    def __init__(self, socket_path: str | None = None):
        self.socket_path = socket_path

    def call(self, method: str, a: str = "", b: str = "") -> str:
        raise NotImplementedError("UnixSocketTransport not implemented yet")


class CliBridgeTransport:
    """Placeholder CLI bridge that would shell out to `yams`.

    In constrained environments it is preferable to use the daemon IPC.
    """

    def __init__(self, yams_path: str = "yams"):
        self.yams_path = yams_path

    def call(self, method: str, a: str = "", b: str = "") -> str:
        raise NotImplementedError("CliBridgeTransport not implemented yet")
