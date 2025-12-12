from __future__ import annotations

import json


class MemoryTransport:
    """In-memory transport for tests/examples. Returns canned JSON results."""

    def __init__(self, fixtures: dict[str, str] | None = None):
        self.fixtures = fixtures or {}

    def call(self, method: str, a: str = "", b: str = "") -> str:
        key = f"{method}:{a}:{b}"
        if key in self.fixtures:
            return self.fixtures[key]
        if method == "list_graphs":
            return json.dumps(
                [
                    {
                        "id": "g1",
                        "name": "SystemArchitecture",
                        "stats": {"num_nodes": 10, "num_edges": 12},
                    },
                ]
            )
        if method == "export_graph":
            # Return GraphJSON stub
            return json.dumps(
                {
                    "id": a,
                    "name": a,
                    "nodes": [],
                    "edges": [],
                    "meta": {"stats": {"num_nodes": 0, "num_edges": 0}},
                }
            )
        if method == "import_graph":
            return json.dumps({"graph_id": "imported"})
        if method == "apply_delta_json":
            try:
                applied = len([ln for ln in b.splitlines() if ln.strip()])
            except Exception:
                applied = 0
            return json.dumps({"applied": applied})
        return json.dumps({"ok": True})
