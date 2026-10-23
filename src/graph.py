"""Representação da cidade como grafo ponderado."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import pandas as pd


@dataclass(frozen=True)
class NodeInfo:
    id: int
    nome: str
    x: float
    y: float
    tipo: str


class CityGraph:
    """Grafo não-direcionado: vértices = bairros, arestas = ruas com peso."""

    def __init__(self, nodes: dict[int, NodeInfo], graph: nx.Graph):
        self.nodes = nodes
        self.graph = graph

    @classmethod
    def from_csv(cls, bairros_path: Path, ruas_path: Path) -> "CityGraph":
        bairros = pd.read_csv(bairros_path)
        ruas = pd.read_csv(ruas_path)

        nodes = {
            int(row.id): NodeInfo(
                id=int(row.id),
                nome=row.nome,
                x=float(row.x),
                y=float(row.y),
                tipo=row.tipo,
            )
            for row in bairros.itertuples(index=False)
        }

        g = nx.Graph()
        for node in nodes.values():
            g.add_node(node.id, nome=node.nome, x=node.x, y=node.y, tipo=node.tipo)

        for row in ruas.itertuples(index=False):
            g.add_edge(
                int(row.origem),
                int(row.destino),
                weight=float(row.distancia_km),
                tempo_min=float(row.tempo_min),
            )

        return cls(nodes=nodes, graph=g)

    def hub_id(self) -> int:
        for node in self.nodes.values():
            if node.tipo == "hub":
                return node.id
        return 0

    def euclidean(self, a: int, b: int) -> float:
        na, nb = self.nodes[a], self.nodes[b]
        return ((na.x - nb.x) ** 2 + (na.y - nb.y) ** 2) ** 0.5

    def path_cost(self, path: list[int], weight: str = "weight") -> float:
        if len(path) < 2:
            return 0.0
        total = 0.0
        for u, v in zip(path, path[1:]):
            total += float(self.graph[u][v][weight])
        return total
