from __future__ import annotations

import json

from .models import GraphInfo


class Transport:
    """Abstract transport to the YAMS daemon.

    Implementations may use a UNIX socket, TCP, or subprocess CLI bridge.
    This scaffold defines the interface only.
    """

    def call(self, method: str, a: str = "", b: str = "") -> str:
        raise NotImplementedError


class GraphClient:
    """Client for GraphAdapter v1 via a Transport.

    Methods mirror docs/api/graph_adapter_v1.md and GraphJSON/Delta specs.
    """

    def __init__(self, transport: Transport):
        self._t = transport

    def list_graphs(self, filter_json: dict | None = None) -> list[GraphInfo]:
        payload = json.dumps(filter_json or {})
        resp = self._t.call("list_graphs", payload, "")
        arr = json.loads(resp)
        out: list[GraphInfo] = []
        for g in arr:
            out.append(
                GraphInfo(
                    id=g.get("id", ""),
                    name=g.get("name", ""),
                    directed=g.get("directed"),
                    num_nodes=g.get("stats", {}).get("num_nodes"),
                    num_edges=g.get("stats", {}).get("num_edges"),
                )
            )
        return out

    def export_graph(
        self, graph_id: str, fmt: str = "graphjson", options: dict | None = None
    ) -> bytes:
        opts = json.dumps({"format": fmt, **(options or {})})
        resp = self._t.call("export_graph", graph_id, opts)
        # Expect base64 or raw bytes by transport convention; scaffold assumes base64 in JSON
        try:
            blob = json.loads(resp)
            if isinstance(blob, dict) and "base64" in blob:
                import base64

                return base64.b64decode(blob["base64"])
        except Exception:
            pass
        # Fallback: return UTF-8 bytes of resp
        return resp.encode("utf-8")

    def import_graph(self, fmt: str, data: bytes, options: dict | None = None) -> str:
        import base64

        payload = json.dumps(
            {"format": fmt, "base64": base64.b64encode(data).decode("ascii"), **(options or {})}
        )
        resp = self._t.call("import_graph", payload, "")
        out = json.loads(resp)
        return out.get("graph_id", "")

    def apply_delta_jsonl(self, graph_id: str, delta_jsonl: str) -> int:
        resp = self._t.call("apply_delta_json", graph_id, delta_jsonl)
        out = json.loads(resp)
        return int(out.get("applied", 0))

    # Iteration methods are transport-dependent; a simple page-pull can be added later.
