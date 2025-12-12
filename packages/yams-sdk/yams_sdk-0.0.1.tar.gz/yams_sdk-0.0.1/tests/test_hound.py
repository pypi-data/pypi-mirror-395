"""Tests for hound.py - Hound graph loading."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from yams_sdk.hound import _to_value, load_hound_graphs


def test_to_value_primitives():
    """Test _to_value with primitive types."""
    assert _to_value("hello") == "hello"
    assert _to_value(42) == 42
    assert _to_value(3.14) == 3.14
    assert _to_value(True) is True
    assert _to_value(False) is False
    assert _to_value(None) is None


def test_to_value_json_serializable():
    """Test _to_value with JSON-serializable objects."""
    assert _to_value({"key": "value"}) == '{"key": "value"}'
    assert _to_value([1, 2, 3]) == "[1, 2, 3]"


def test_to_value_non_serializable():
    """Test _to_value falls back to str() for non-serializable."""

    class Custom:
        def __str__(self):
            return "custom_str"

    assert _to_value(Custom()) == "custom_str"


def test_load_hound_graphs_empty_dir():
    """Test loading from directory with no graphs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        (p / "graphs").mkdir()
        result = load_hound_graphs(tmpdir)
        assert result == []


def test_load_hound_graphs_single_graph():
    """Test loading a single Hound graph."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        graph_data = {
            "name": "test_graph",
            "focus": "analysis",
            "stats": {"nodes": 2, "edges": 1},
            "nodes": [
                {"id": "n1", "labels": ["Function"], "properties": {"name": "main"}},
                {"id": "n2", "labels": ["Variable"], "properties": {"type": "int"}},
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "n1",
                    "target": "n2",
                    "label": "uses",
                    "weight": 1.0,
                    "properties": {"count": 5},
                }
            ],
        }
        (graphs_dir / "graph_test.json").write_text(json.dumps(graph_data))

        result = load_hound_graphs(tmpdir)
        assert len(result) == 1

        name, gj = result[0]
        assert name == "test_graph"
        assert gj["id"] == "test_graph"
        assert gj["directed"] is True
        assert len(gj["nodes"]) == 2
        assert len(gj["edges"]) == 1

        # Check node structure
        node = gj["nodes"][0]
        assert node["id"] == "n1"
        assert node["labels"] == ["Function"]
        assert node["properties"]["name"] == "main"

        # Check edge structure
        edge = gj["edges"][0]
        assert edge["id"] == "e1"
        assert edge["src"] == "n1"
        assert edge["dst"] == "n2"
        assert edge["label"] == "uses"


def test_load_hound_graphs_alternative_fields():
    """Test loading with alternative field names (src/dst, key, internal_name)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        graph_data = {
            "internal_name": "internal_graph",
            "nodes": [
                {"key": "k1", "labels": [], "properties": {}},
                {"name": "named_node", "labels": [], "properties": {}},
            ],
            "edges": [
                {"id": "e1", "src": "k1", "dst": "named_node"},
            ],
        }
        (graphs_dir / "graph_alt.json").write_text(json.dumps(graph_data))

        result = load_hound_graphs(tmpdir)
        assert len(result) == 1

        name, gj = result[0]
        assert name == "internal_graph"
        assert gj["nodes"][0]["id"] == "k1"
        assert gj["nodes"][1]["id"] == "named_node"


def test_load_hound_graphs_fallback_to_filename():
    """Test that graph name falls back to filename stem."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        graph_data = {"nodes": [], "edges": []}
        (graphs_dir / "graph_myanalysis.json").write_text(json.dumps(graph_data))

        result = load_hound_graphs(tmpdir)
        name, _ = result[0]
        assert name == "myanalysis"


def test_load_hound_graphs_invalid_json_skipped():
    """Test that invalid JSON files are skipped."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        # Valid graph
        (graphs_dir / "graph_valid.json").write_text('{"name": "valid", "nodes": [], "edges": []}')
        # Invalid JSON
        (graphs_dir / "graph_invalid.json").write_text("not json at all {{{")

        result = load_hound_graphs(tmpdir)
        assert len(result) == 1
        assert result[0][0] == "valid"


def test_load_hound_graphs_multiple_sorted():
    """Test that multiple graphs are returned sorted by filename."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        for i in ["c", "a", "b"]:
            (graphs_dir / f"graph_{i}.json").write_text(
                json.dumps({"name": f"graph_{i}", "nodes": [], "edges": []})
            )

        result = load_hound_graphs(tmpdir)
        names = [r[0] for r in result]
        assert names == ["graph_a", "graph_b", "graph_c"]


def test_load_hound_graphs_null_fields():
    """Test handling of null/missing fields."""
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        graphs_dir = p / "graphs"
        graphs_dir.mkdir()

        graph_data = {
            "name": "sparse",
            "nodes": [{"id": "n1"}],  # Missing labels and properties
            "edges": [{"src": "n1", "dst": "n1"}],  # Missing id, label, weight
        }
        (graphs_dir / "graph_sparse.json").write_text(json.dumps(graph_data))

        result = load_hound_graphs(tmpdir)
        _, gj = result[0]

        node = gj["nodes"][0]
        assert node["labels"] == []
        assert node["properties"] == {}

        edge = gj["edges"][0]
        assert edge["id"] == ""
        assert edge["label"] is None
        assert edge["weight"] is None
