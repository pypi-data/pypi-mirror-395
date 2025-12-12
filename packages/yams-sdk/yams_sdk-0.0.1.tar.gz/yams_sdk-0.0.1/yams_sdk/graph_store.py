from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GNode:
    id: str
    props: dict[str, Any] = field(default_factory=dict)


@dataclass
class GEdge:
    id: str
    src: str
    dst: str
    props: dict[str, Any] = field(default_factory=dict)


class InMemoryGraph:
    """Minimal in-memory GraphJSON-like store with delta apply.

    This is used for SDK-side validation and spec-driven tests, not as a
    production graph engine.
    """

    def __init__(self, graph_id: str, name: str | None = None):
        self.id = graph_id
        self.name = name or graph_id
        self.nodes: dict[str, GNode] = {}
        self.edges: dict[str, GEdge] = {}

    def to_graphjson(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "directed": True,
            "nodes": [
                {"id": n.id, "properties": dict(n.props), "labels": []} for n in self.nodes.values()
            ],
            "edges": [
                {
                    "id": e.id,
                    "src": e.src,
                    "dst": e.dst,
                    "properties": dict(e.props),
                }
                for e in self.edges.values()
            ],
        }

    def apply_delta_jsonl(self, jsonl: str) -> int:
        applied = 0
        for line in jsonl.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                op = json.loads(line)
            except Exception:
                continue
            kind = op.get("op")
            if kind == "add_node":
                nid = str(op["id"])  # may raise KeyError
                if nid not in self.nodes:
                    self.nodes[nid] = GNode(nid)
                applied += 1
            elif kind == "remove_node":
                nid = str(op["id"])
                if nid in self.nodes:
                    del self.nodes[nid]
                # Remove incident edges
                self.edges = {
                    eid: e for eid, e in self.edges.items() if e.src != nid and e.dst != nid
                }
                applied += 1
            elif kind == "add_edge":
                eid = str(op["id"]) if "id" in op else f"e{len(self.edges) + 1}"
                src = str(op["src"])  # required
                dst = str(op["dst"])  # required
                self.edges[eid] = GEdge(eid, src, dst)
                applied += 1
            elif kind == "remove_edge":
                eid = str(op["id"])
                if eid in self.edges:
                    del self.edges[eid]
                applied += 1
            elif kind == "set_node_props":
                nid = str(op["id"])
                props = op.get("properties") or {}
                node = self.nodes.setdefault(nid, GNode(nid))
                node.props = dict(props)
                applied += 1
            elif kind == "merge_node_props":
                nid = str(op["id"])
                props = op.get("properties") or {}
                node = self.nodes.setdefault(nid, GNode(nid))
                node.props.update(props)
                applied += 1
            elif kind == "set_edge_props":
                eid = str(op["id"])
                props = op.get("properties") or {}
                edge = self.edges.get(eid)
                if edge:
                    edge.props = dict(props)
                applied += 1
            elif kind == "merge_edge_props":
                eid = str(op["id"])
                props = op.get("properties") or {}
                edge = self.edges.get(eid)
                if edge:
                    edge.props.update(props)
                applied += 1
            else:
                # Unknown operation -> ignore
                pass
        return applied
