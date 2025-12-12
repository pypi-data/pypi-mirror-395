"""Tests for schemas.py - Schema loading and validation."""

from __future__ import annotations

import pytest
from jsonschema import ValidationError

from yams_sdk.schemas import (
    _bundled_spec,
    _find_schema_path,
    _load_json,
    _repo_root,
    load_schema,
    validate,
    validate_graph_delta,
    validate_graphjson,
    validate_plugin_manifest,
)


def test_bundled_spec_path():
    """Test _bundled_spec returns path sibling to yams_sdk package."""
    path = _bundled_spec()
    assert path.name == "spec"
    assert path.parent.name == "yams-sdk"  # Parent is the repo root


def test_repo_root_found():
    """Test _repo_root finds parent YAMS repo if present."""
    root = _repo_root()
    # May be None in standalone SDK checkout, or Path in dev mode
    if root is not None:
        assert (root / "docs" / "spec").exists()


def test_load_json(tmp_path):
    """Test _load_json reads and parses JSON file."""
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "value"}')

    result = _load_json(test_file)
    assert result == {"key": "value"}


def test_find_schema_path_bundled():
    """Test _find_schema_path finds bundled schemas."""
    path = _find_schema_path("graphjson_v1")
    assert path.exists()
    assert path.name == "graphjson_v1.schema.json"


def test_find_schema_path_plugin_metadata():
    """Test _find_schema_path for plugin_metadata (special case)."""
    path = _find_schema_path("plugin_metadata")
    assert path.exists()
    assert path.name == "plugin_metadata.schema.json"


def test_find_schema_path_not_found():
    """Test _find_schema_path raises FileNotFoundError for missing schema."""
    with pytest.raises(FileNotFoundError, match="not found"):
        _find_schema_path("nonexistent_schema_v99")


def test_load_schema_graphjson():
    """Test load_schema loads graphjson_v1 schema."""
    schema = load_schema("graphjson_v1")
    assert "$schema" in schema or "type" in schema
    assert "properties" in schema


def test_load_schema_graph_delta():
    """Test load_schema loads graph_delta_v1 schema."""
    schema = load_schema("graph_delta_v1")
    assert "type" in schema or "$schema" in schema


def test_load_schema_plugin_metadata():
    """Test load_schema loads plugin_metadata schema."""
    schema = load_schema("plugin_metadata")
    assert "properties" in schema


def test_validate_valid():
    """Test validate passes for valid instance."""
    # This should not raise
    validate(
        "graphjson_v1",
        {
            "id": "g1",
            "name": "Test",
            "directed": True,
            "nodes": [],
            "edges": [],
        },
    )


def test_validate_invalid():
    """Test validate raises ValidationError for invalid instance."""
    with pytest.raises(ValidationError):
        validate("graphjson_v1", {"invalid": "schema"})


def test_validate_graphjson_valid():
    """Test validate_graphjson with valid graph."""
    validate_graphjson(
        {
            "id": "g1",
            "name": "Test",
            "directed": True,
            "nodes": [{"id": "n1", "labels": [], "properties": {}}],
            "edges": [],
        }
    )


def test_validate_graphjson_invalid():
    """Test validate_graphjson with invalid graph."""
    with pytest.raises(ValidationError):
        validate_graphjson({"missing": "required_fields"})


def test_validate_graph_delta_valid():
    """Test validate_graph_delta with valid delta."""
    validate_graph_delta(
        [
            {"op": "add_node", "id": "n1", "ts": "2025-01-01T00:00:00Z"},
        ]
    )


def test_validate_graph_delta_invalid():
    """Test validate_graph_delta with invalid delta."""
    with pytest.raises(ValidationError):
        validate_graph_delta({"not": "an_array"})


def test_validate_plugin_manifest_valid():
    """Test validate_plugin_manifest with valid manifest."""
    validate_plugin_manifest(
        {
            "name": "test-plugin",
            "version": "1.0.0",
            "transport": "external",
            "interfaces": ["content_extractor_v1"],
            "entry": {"cmd": ["python", "plugin.py"]},
        }
    )


def test_validate_plugin_manifest_invalid():
    """Test validate_plugin_manifest with invalid manifest."""
    with pytest.raises(ValidationError):
        validate_plugin_manifest({"name": "missing-required-fields"})


def test_validate_graphjson_with_node_properties():
    """Test validation allows arbitrary node properties."""
    validate_graphjson(
        {
            "id": "g1",
            "name": "Test",
            "directed": True,
            "nodes": [
                {
                    "id": "n1",
                    "labels": ["Function", "Entry"],
                    "properties": {
                        "name": "main",
                        "line_start": 10,
                        "is_entry": True,
                    },
                }
            ],
            "edges": [],
        }
    )


def test_validate_graphjson_with_edge_properties():
    """Test validation allows edge with properties."""
    validate_graphjson(
        {
            "id": "g1",
            "name": "Test",
            "directed": True,
            "nodes": [
                {"id": "n1", "labels": [], "properties": {}},
                {"id": "n2", "labels": [], "properties": {}},
            ],
            "edges": [
                {
                    "id": "e1",
                    "src": "n1",
                    "dst": "n2",
                    "label": "calls",
                    "weight": 1.5,
                    "properties": {"count": 42},
                }
            ],
        }
    )
