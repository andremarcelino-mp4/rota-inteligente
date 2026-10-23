"""Geração de diagramas e gráficos da solução."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from .graph import CityGraph
from .clustering import DeliveryCluster


COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]


def plot_city_graph(city: CityGraph, out_path: Path) -> None:
    pos = {nid: (n.x, n.y) for nid, n in city.nodes.items()}
    labels = {nid: n.nome for nid, n in city.nodes.items()}

    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_edges(city.graph, pos, ax=ax, width=1.5, edge_color="#888888")
    edge_labels = {
        (u, v): f"{d['weight']:.1f}km" for u, v, d in city.graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(city.graph, pos, edge_labels=edge_labels, font_size=7, ax=ax)

    hub = [city.hub_id()]
    others = [n for n in city.graph.nodes if n not in hub]
    nx.draw_networkx_nodes(city.graph, pos, nodelist=others, node_color="#4C78A8", node_size=700, ax=ax)
    nx.draw_networkx_nodes(city.graph, pos, nodelist=hub, node_color="#E45756", node_size=900, ax=ax)
    nx.draw_networkx_labels(city.graph, pos, labels=labels, font_size=8, ax=ax)

    ax.set_title("Grafo da cidade — Sabor Express (Centro = hub)")
    ax.set_axis_off()
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_clusters(
    city: CityGraph,
    enriched: pd.DataFrame,
    clusters: list[DeliveryCluster],
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))
    for cluster in clusters:
        color = COLORS[cluster.cluster_id % len(COLORS)]
        subset = enriched[enriched["cluster"] == cluster.cluster_id]
        ax.scatter(
            subset["x"],
            subset["y"],
            c=color,
            s=80,
            label=f"Zona {cluster.cluster_id} ({len(cluster.entrega_ids)} pedidos)",
            alpha=0.85,
            edgecolors="white",
        )
        cx, cy = cluster.centroid_xy
        ax.scatter([cx], [cy], c=color, s=220, marker="X", edgecolors="black")

    hub = city.nodes[city.hub_id()]
    ax.scatter([hub.x], [hub.y], c="#E45756", s=200, marker="*", label="Hub (Centro)", zorder=5)

    for nid, node in city.nodes.items():
        ax.annotate(node.nome, (node.x, node.y), textcoords="offset points", xytext=(4, 4), fontsize=7)

    ax.set_title("Clustering K-Means das entregas por zona")
    ax.set_xlabel("x (coordenada relativa)")
    ax.set_ylabel("y (coordenada relativa)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_routes(
    city: CityGraph,
    route_orders: dict[int, list[int]],
    out_path: Path,
) -> None:
    pos = {nid: (n.x, n.y) for nid, n in city.nodes.items()}
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw_networkx_edges(city.graph, pos, ax=ax, width=1.0, edge_color="#cccccc", alpha=0.7)
    nx.draw_networkx_nodes(city.graph, pos, node_color="#dddddd", node_size=500, ax=ax)
    labels = {nid: n.nome for nid, n in city.nodes.items()}
    nx.draw_networkx_labels(city.graph, pos, labels=labels, font_size=7, ax=ax)

    for cid, order in route_orders.items():
        color = COLORS[cid % len(COLORS)]
        for u, v in zip(order, order[1:]):
            if city.graph.has_edge(u, v):
                ax.annotate(
                    "",
                    xy=pos[v],
                    xytext=pos[u],
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.2, alpha=0.9),
                )
        ax.plot([], [], color=color, lw=2.5, label=f"Entregador {cid}")

    ax.set_title("Rotas otimizadas por entregador (A* + vizinho mais próximo)")
    ax.legend(loc="best")
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_cost_comparison(baseline_km: float, optimized_km: float, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(
        ["Manual (ordem CSV)", "IA (K-Means + A*)"],
        [baseline_km, optimized_km],
        color=["#E45756", "#54A24B"],
    )
    ax.set_ylabel("Distância total (km)")
    ax.set_title("Comparativo de distância total percorrida")
    for bar, value in zip(bars, [baseline_km, optimized_km]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.3, f"{value:.1f} km", ha="center")
    saving = ((baseline_km - optimized_km) / baseline_km) * 100 if baseline_km else 0
    ax.text(0.5, max(baseline_km, optimized_km) * 0.5, f"Economia: {saving:.1f}%", ha="center", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
