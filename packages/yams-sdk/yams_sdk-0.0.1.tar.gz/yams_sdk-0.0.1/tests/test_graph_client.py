from __future__ import annotations

import json

from yams_sdk.graph_client import GraphClient
from yams_sdk.transports import MemoryTransport


def test_list_graphs_memory_transport():
    client = GraphClient(MemoryTransport())
    gs = client.list_graphs()
    assert len(gs) == 1
    g = gs[0]
    assert g.id == "g1"
    assert g.name == "SystemArchitecture"
    assert g.num_nodes == 10
    assert g.num_edges == 12


def test_export_graph_returns_graphjson_bytes():
    client = GraphClient(MemoryTransport())
    blob = client.export_graph("g1")
    data = json.loads(blob.decode("utf-8"))
    assert data["id"] == "g1"
    assert data["nodes"] == []
    assert data["edges"] == []


def test_import_graph_and_delta_apply():
    client = GraphClient(MemoryTransport())
    gid = client.import_graph("graphjson", b"{}")
    assert gid == "imported"

    # Two operations
    applied = client.apply_delta_jsonl(
        "imported", '{"op":"add_node","id":"n1"}\n{"op":"add_node","id":"n2"}\n'
    )
    assert applied == 2
