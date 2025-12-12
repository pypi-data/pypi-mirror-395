from __future__ import annotations

import json

from yams_sdk.graph_store import InMemoryGraph
from yams_sdk.schemas import validate_graphjson


def test_delta_apply_and_export_parity():
    g = InMemoryGraph("g")
    delta = "\n".join(
        [
            json.dumps({"op": "add_node", "id": "n1"}),
            json.dumps({"op": "add_node", "id": "n2"}),
            json.dumps({"op": "add_edge", "id": "e1", "src": "n1", "dst": "n2"}),
            json.dumps({"op": "set_node_props", "id": "n1", "properties": {"name": "A"}}),
            json.dumps({"op": "merge_node_props", "id": "n1", "properties": {"role": "X"}}),
            json.dumps({"op": "set_edge_props", "id": "e1", "properties": {"w": 1}}),
        ]
    )
    applied = g.apply_delta_jsonl(delta)
    assert applied == 6
    gj = g.to_graphjson()
    # Validate against spec schema
    validate_graphjson(gj)
    # Check content
    nodes = {n["id"]: n for n in gj["nodes"]}
    assert nodes["n1"]["properties"]["name"] == "A"
    assert nodes["n1"]["properties"]["role"] == "X"
    edges = {e["id"]: e for e in gj["edges"]}
    assert edges["e1"]["src"] == "n1" and edges["e1"]["dst"] == "n2"
    assert edges["e1"]["properties"]["w"] == 1
