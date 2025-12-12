"""Tests for graph_store.py - InMemoryGraph operations."""

from __future__ import annotations

import json

from yams_sdk.graph_store import GEdge, GNode, InMemoryGraph


def test_gnode_default_props():
    """Test GNode with default empty props."""
    node = GNode(id="n1")
    assert node.id == "n1"
    assert node.props == {}


def test_gnode_with_props():
    """Test GNode with custom props."""
    node = GNode(id="n2", props={"key": "value"})
    assert node.props == {"key": "value"}


def test_gedge_default_props():
    """Test GEdge with default empty props."""
    edge = GEdge(id="e1", src="n1", dst="n2")
    assert edge.id == "e1"
    assert edge.src == "n1"
    assert edge.dst == "n2"
    assert edge.props == {}


def test_gedge_with_props():
    """Test GEdge with custom props."""
    edge = GEdge(id="e2", src="a", dst="b", props={"weight": 1.5})
    assert edge.props == {"weight": 1.5}


def test_inmemory_graph_init():
    """Test InMemoryGraph initialization."""
    g = InMemoryGraph("g1")
    assert g.id == "g1"
    assert g.name == "g1"
    assert g.nodes == {}
    assert g.edges == {}


def test_inmemory_graph_custom_name():
    """Test InMemoryGraph with custom name."""
    g = InMemoryGraph("g2", name="My Graph")
    assert g.id == "g2"
    assert g.name == "My Graph"


def test_to_graphjson_empty():
    """Test to_graphjson with empty graph."""
    g = InMemoryGraph("empty")
    gj = g.to_graphjson()
    assert gj["id"] == "empty"
    assert gj["name"] == "empty"
    assert gj["directed"] is True
    assert gj["nodes"] == []
    assert gj["edges"] == []


def test_to_graphjson_with_data():
    """Test to_graphjson with nodes and edges."""
    g = InMemoryGraph("g1")
    g.nodes["n1"] = GNode("n1", {"type": "func"})
    g.nodes["n2"] = GNode("n2", {"type": "var"})
    g.edges["e1"] = GEdge("e1", "n1", "n2", {"label": "uses"})

    gj = g.to_graphjson()
    assert len(gj["nodes"]) == 2
    assert len(gj["edges"]) == 1

    # Find node n1
    n1 = next(n for n in gj["nodes"] if n["id"] == "n1")
    assert n1["properties"] == {"type": "func"}
    assert n1["labels"] == []

    # Check edge
    e1 = gj["edges"][0]
    assert e1["id"] == "e1"
    assert e1["src"] == "n1"
    assert e1["dst"] == "n2"
    assert e1["properties"] == {"label": "uses"}


def test_apply_delta_add_node():
    """Test add_node delta operation."""
    g = InMemoryGraph("g1")
    delta = json.dumps({"op": "add_node", "id": "n1"})
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" in g.nodes


def test_apply_delta_add_node_idempotent():
    """Test add_node doesn't duplicate nodes."""
    g = InMemoryGraph("g1")
    delta = "\n".join(
        [
            json.dumps({"op": "add_node", "id": "n1"}),
            json.dumps({"op": "add_node", "id": "n1"}),
        ]
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 2  # Both ops applied
    assert len(g.nodes) == 1  # But only one node exists


def test_apply_delta_remove_node():
    """Test remove_node delta operation."""
    g = InMemoryGraph("g1")
    g.nodes["n1"] = GNode("n1")
    g.nodes["n2"] = GNode("n2")
    g.edges["e1"] = GEdge("e1", "n1", "n2")

    delta = json.dumps({"op": "remove_node", "id": "n1"})
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" not in g.nodes
    assert "n2" in g.nodes
    assert len(g.edges) == 0  # Edge removed with node


def test_apply_delta_remove_nonexistent_node():
    """Test remove_node on non-existent node."""
    g = InMemoryGraph("g1")
    delta = json.dumps({"op": "remove_node", "id": "nx"})
    count = g.apply_delta_jsonl(delta)
    assert count == 1  # Operation still counted


def test_apply_delta_add_edge():
    """Test add_edge delta operation."""
    g = InMemoryGraph("g1")
    delta = json.dumps({"op": "add_edge", "id": "e1", "src": "n1", "dst": "n2"})
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "e1" in g.edges
    assert g.edges["e1"].src == "n1"
    assert g.edges["e1"].dst == "n2"


def test_apply_delta_add_edge_auto_id():
    """Test add_edge generates ID if not provided."""
    g = InMemoryGraph("g1")
    delta = json.dumps({"op": "add_edge", "src": "n1", "dst": "n2"})
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert len(g.edges) == 1
    edge_id = list(g.edges.keys())[0]
    assert edge_id.startswith("e")


def test_apply_delta_remove_edge():
    """Test remove_edge delta operation."""
    g = InMemoryGraph("g1")
    g.edges["e1"] = GEdge("e1", "n1", "n2")

    delta = json.dumps({"op": "remove_edge", "id": "e1"})
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "e1" not in g.edges


def test_apply_delta_remove_nonexistent_edge():
    """Test remove_edge on non-existent edge."""
    g = InMemoryGraph("g1")
    delta = json.dumps({"op": "remove_edge", "id": "ex"})
    count = g.apply_delta_jsonl(delta)
    assert count == 1  # Operation still counted


def test_apply_delta_set_node_props():
    """Test set_node_props replaces all properties."""
    g = InMemoryGraph("g1")
    g.nodes["n1"] = GNode("n1", {"old": "value", "keep": "no"})

    delta = json.dumps(
        {
            "op": "set_node_props",
            "id": "n1",
            "properties": {"new": "value"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert g.nodes["n1"].props == {"new": "value"}


def test_apply_delta_set_node_props_creates_node():
    """Test set_node_props creates node if not exists."""
    g = InMemoryGraph("g1")

    delta = json.dumps(
        {
            "op": "set_node_props",
            "id": "n1",
            "properties": {"key": "value"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" in g.nodes
    assert g.nodes["n1"].props == {"key": "value"}


def test_apply_delta_merge_node_props():
    """Test merge_node_props merges properties."""
    g = InMemoryGraph("g1")
    g.nodes["n1"] = GNode("n1", {"existing": "value"})

    delta = json.dumps(
        {
            "op": "merge_node_props",
            "id": "n1",
            "properties": {"new": "prop"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert g.nodes["n1"].props == {"existing": "value", "new": "prop"}


def test_apply_delta_merge_node_props_creates_node():
    """Test merge_node_props creates node if not exists."""
    g = InMemoryGraph("g1")

    delta = json.dumps(
        {
            "op": "merge_node_props",
            "id": "n1",
            "properties": {"key": "value"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" in g.nodes


def test_apply_delta_set_edge_props():
    """Test set_edge_props replaces all edge properties."""
    g = InMemoryGraph("g1")
    g.edges["e1"] = GEdge("e1", "n1", "n2", {"old": "prop"})

    delta = json.dumps(
        {
            "op": "set_edge_props",
            "id": "e1",
            "properties": {"new": "prop"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert g.edges["e1"].props == {"new": "prop"}


def test_apply_delta_set_edge_props_nonexistent():
    """Test set_edge_props on non-existent edge does nothing."""
    g = InMemoryGraph("g1")

    delta = json.dumps(
        {
            "op": "set_edge_props",
            "id": "ex",
            "properties": {"key": "value"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1  # Operation counted
    assert len(g.edges) == 0  # But no edge created


def test_apply_delta_merge_edge_props():
    """Test merge_edge_props merges edge properties."""
    g = InMemoryGraph("g1")
    g.edges["e1"] = GEdge("e1", "n1", "n2", {"existing": "value"})

    delta = json.dumps(
        {
            "op": "merge_edge_props",
            "id": "e1",
            "properties": {"new": "prop"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert g.edges["e1"].props == {"existing": "value", "new": "prop"}


def test_apply_delta_merge_edge_props_nonexistent():
    """Test merge_edge_props on non-existent edge does nothing."""
    g = InMemoryGraph("g1")

    delta = json.dumps(
        {
            "op": "merge_edge_props",
            "id": "ex",
            "properties": {"key": "value"},
        }
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1  # Operation counted
    assert len(g.edges) == 0  # But no edge created


def test_apply_delta_unknown_operation():
    """Test unknown operations are ignored."""
    g = InMemoryGraph("g1")

    delta = json.dumps({"op": "unknown_op", "id": "x"})
    count = g.apply_delta_jsonl(delta)

    assert count == 0  # Unknown op not counted


def test_apply_delta_invalid_json_skipped():
    """Test invalid JSON lines are skipped."""
    g = InMemoryGraph("g1")

    delta = "\n".join(
        [
            "not valid json",
            json.dumps({"op": "add_node", "id": "n1"}),
        ]
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" in g.nodes


def test_apply_delta_empty_lines_skipped():
    """Test empty lines are skipped."""
    g = InMemoryGraph("g1")

    delta = "\n\n" + json.dumps({"op": "add_node", "id": "n1"}) + "\n\n"
    count = g.apply_delta_jsonl(delta)

    assert count == 1
    assert "n1" in g.nodes


def test_apply_delta_complex_scenario():
    """Test complex multi-operation delta."""
    g = InMemoryGraph("g1")

    delta = "\n".join(
        [
            json.dumps({"op": "add_node", "id": "n1"}),
            json.dumps({"op": "add_node", "id": "n2"}),
            json.dumps({"op": "add_node", "id": "n3"}),
            json.dumps({"op": "add_edge", "id": "e1", "src": "n1", "dst": "n2"}),
            json.dumps({"op": "add_edge", "id": "e2", "src": "n2", "dst": "n3"}),
            json.dumps({"op": "set_node_props", "id": "n1", "properties": {"type": "entry"}}),
            json.dumps({"op": "merge_edge_props", "id": "e1", "properties": {"weight": 1.0}}),
            json.dumps({"op": "remove_node", "id": "n3"}),  # Should also remove e2
        ]
    )
    count = g.apply_delta_jsonl(delta)

    assert count == 8
    assert len(g.nodes) == 2
    assert len(g.edges) == 1
    assert g.nodes["n1"].props == {"type": "entry"}
    assert g.edges["e1"].props == {"weight": 1.0}
