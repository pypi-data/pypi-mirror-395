from __future__ import annotations

import json
from pathlib import Path


def _to_value(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    try:
        return json.dumps(v)
    except Exception:
        return str(v)


def load_hound_graphs(project_dir: str | Path) -> list[tuple[str, dict]]:
    """Load Hound graph_*.json files and convert each to GraphJSON v1 dict.

    Returns a list of (name, graphjson) tuples.
    """
    p = Path(project_dir)
    graphs_dir = p / "graphs"
    out: list[tuple[str, dict]] = []
    for gf in sorted(graphs_dir.glob("graph_*.json")):
        try:
            data = json.loads(gf.read_text())
        except Exception:
            continue
        name = data.get("name") or data.get("internal_name") or gf.stem.replace("graph_", "")
        gj = {
            "id": name,
            "name": name,
            "directed": True,
            "nodes": [],
            "edges": [],
            "meta": {
                "focus": data.get("focus"),
                "stats": data.get("stats", {}),
            },
        }
        for n in data.get("nodes", []) or []:
            gj["nodes"].append(
                {
                    "id": str(n.get("id") or n.get("name") or n.get("key") or ""),
                    "labels": n.get("labels") or [],
                    "properties": {k: _to_value(v) for k, v in (n.get("properties") or {}).items()},
                }
            )
        for e in data.get("edges", []) or []:
            gj["edges"].append(
                {
                    "id": str(e.get("id") or ""),
                    "src": str(e.get("source") or e.get("src") or ""),
                    "dst": str(e.get("target") or e.get("dst") or ""),
                    "label": e.get("label"),
                    "weight": e.get("weight"),
                    "properties": {k: _to_value(v) for k, v in (e.get("properties") or {}).items()},
                }
            )
        out.append((name, gj))
    return out
