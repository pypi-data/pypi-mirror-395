from __future__ import annotations

from pathlib import Path

from yams_sdk.schemas import (
    validate_graph_delta,
    validate_graphjson,
    validate_plugin_manifest,
)


def test_graphjson_schema_validation():
    g = {
        "id": "g1",
        "name": "Example",
        "directed": True,
        "nodes": [{"id": "n1", "labels": ["X"], "properties": {"k": "v"}}],
        "edges": [{"id": "e1", "src": "n1", "dst": "n1", "label": "self"}],
    }
    validate_graphjson(g)


def test_graph_delta_schema_validation():
    delta = [
        {"op": "add_node", "id": "n1", "ts": "2025-09-22T00:00:00Z"},
        {"op": "add_edge", "id": "e1", "src": "n1", "dst": "n1", "ts": "2025-09-22T00:00:01Z"},
        {"op": "set_node_props", "id": "n1", "properties": {"k": "v"}},
    ]
    validate_graph_delta(delta)


def test_plugin_manifest_validation_basic():
    # Minimal manifest for an External plugin implementing ghidra_analysis_v1
    m = {
        "name": "yams-ghidra-plugin",
        "version": "0.1.0",
        "transport": "external",
        "interfaces": ["ghidra_analysis_v1"],
        "entry": {"cmd": ["python", "plugins/yams-ghidra-plugin/plugin.py"]},
    }
    validate_plugin_manifest(m)


def test_wit_presence():
    # Ensure GraphAdapter WIT exists as part of the spec distribution
    # Check bundled location first (at project root level)
    import yams_sdk.schemas as schemas_mod

    spec_dir = Path(schemas_mod.__file__).parent.parent / "spec"
    bundled_wit = spec_dir / "wit" / "graph_adapter_v1.wit"
    if bundled_wit.exists():
        return  # Found in bundled location

    # Fall back to repo root (development mode)
    root = Path(__file__).resolve()
    for parent in root.parents:
        wit = parent / "docs" / "spec" / "wit" / "graph_adapter_v1.wit"
        if wit.exists():
            return  # Found in repo

    raise AssertionError(
        f"graph_adapter_v1.wit not found.\n"
        f"  Checked bundled: {bundled_wit}\n"
        f"  Checked repo parents from: {root}"
    )
