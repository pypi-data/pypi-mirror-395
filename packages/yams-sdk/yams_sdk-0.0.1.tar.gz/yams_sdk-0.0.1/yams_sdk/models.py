from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

Value = Optional[Union[bool, int, float, str]]


@dataclass
class GraphInfo:
    id: str
    name: str
    directed: bool | None = None
    num_nodes: int | None = None
    num_edges: int | None = None


@dataclass
class Node:
    id: str
    labels: list[str] = field(default_factory=list)
    props: dict[str, Value] = field(default_factory=dict)


@dataclass
class Edge:
    id: str
    src: str
    dst: str
    label: str | None = None
    weight: float | None = None
    props: dict[str, Value] = field(default_factory=dict)
