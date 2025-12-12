from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def _bundled_spec() -> Path:
    """Return path to bundled spec directory (sibling of yams_sdk package)."""
    return Path(__file__).resolve().parent.parent / "spec"


def _repo_root() -> Path | None:
    """Resolve repo root based on this file location (for development)."""
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "docs" / "spec").exists():
            return parent
    return None


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def _find_schema_path(name: str) -> Path:
    """Find schema path, preferring bundled schemas, falling back to repo."""
    bundled = _bundled_spec()

    # Determine relative path for schema
    if name == "plugin_metadata":
        rel_path = "plugin_metadata.schema.json"
    else:
        rel_path = f"schemas/{name}.schema.json"

    # Try bundled path first (installed package or copied schemas)
    bundled_path = bundled / rel_path
    if bundled_path.exists():
        return bundled_path

    # Fall back to repo root (development mode)
    repo_root = _repo_root()
    if repo_root:
        repo_path = repo_root / "docs" / "spec" / rel_path
        if repo_path.exists():
            return repo_path

    repo_hint = "N/A"
    if repo_root:
        repo_hint = str(repo_root / "docs" / "spec" / rel_path)
    raise FileNotFoundError(
        f"Schema '{name}' not found. Checked:\n"
        f"  - Bundled: {bundled_path}\n"
        f"  - Repo: {repo_hint}"
    )


def load_schema(name: str) -> dict[str, Any]:
    """Load a spec schema by short name.

    Names: graphjson_v1, graph_delta_v1, provenance_v1,
           card_anchor_v1, plugin_metadata
    """
    path = _find_schema_path(name)
    return _load_json(path)


def validate(schema_name: str, instance: Any) -> None:
    """Validate instance against a schema.

    Raises jsonschema.ValidationError on failure.
    """
    schema = load_schema(schema_name)
    Draft202012Validator(schema).validate(instance)


def validate_graphjson(graph: dict[str, Any]) -> None:
    validate("graphjson_v1", graph)


def validate_graph_delta(delta: Any) -> None:
    validate("graph_delta_v1", delta)


def validate_plugin_manifest(manifest: dict[str, Any]) -> None:
    validate("plugin_metadata", manifest)
