"""
Pipeline principal — Rota Inteligente (Sabor Express).

Fluxo:
1. Carrega grafo da cidade (bairros + ruas)
2. Agrupa entregas com K-Means (zonas / entregadores)
3. Para cada zona, monta rota com vizinho mais próximo + A*
4. Compara com baseline manual e gera artefatos em /outputs
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.clustering import cluster_deliveries, load_entregas
from src.graph import CityGraph
from src.pathfinding import astar, nearest_neighbor_route
from src.visualize import (
    plot_city_graph,
    plot_clusters,
    plot_cost_comparison,
    plot_routes,
)


def baseline_manual_route(city: CityGraph, entregas) -> tuple[list[int], float]:
    """Simula rota manual: ordem do CSV, saindo e voltando ao hub."""
    hub = city.hub_id()
    order = [hub]
    total = 0.0
    current = hub
    for bairro_id in entregas["bairro_id"].tolist():
        bid = int(bairro_id)
        if bid == current:
            continue
        path, cost = astar(city, current, bid)
        total += cost
        order.append(bid)
        current = bid
    back, back_cost = astar(city, current, hub)
    total += back_cost
    order.append(hub)
    return order, total


def run(n_clusters: int = 3) -> dict:
    data_dir = ROOT / "data"
    out_dir = ROOT / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    city = CityGraph.from_csv(data_dir / "bairros.csv", data_dir / "ruas.csv")
    entregas = load_entregas(data_dir / "entregas.csv")

    clusters, enriched = cluster_deliveries(city, entregas, n_clusters=n_clusters)
    hub = city.hub_id()

    route_orders: dict[int, list[int]] = {}
    route_details = []
    optimized_total = 0.0

    for cluster in clusters:
        order, cost, segments = nearest_neighbor_route(city, hub, cluster.bairro_ids)
        route_orders[cluster.cluster_id] = order
        optimized_total += cost
        nomes = [city.nodes[n].nome for n in order]
        route_details.append(
            {
                "entregador": cluster.cluster_id,
                "pedidos": cluster.entrega_ids,
                "bairros_unicos": [city.nodes[b].nome for b in cluster.bairro_ids],
                "rota": nomes,
                "distancia_km": round(cost, 2),
                "segmentos_astar": [
                    [city.nodes[n].nome for n in seg] for seg in segments
                ],
            }
        )

    _, baseline_km = baseline_manual_route(city, entregas)
    economia_pct = ((baseline_km - optimized_total) / baseline_km) * 100 if baseline_km else 0

    plot_city_graph(city, out_dir / "01_grafo_cidade.png")
    plot_clusters(city, enriched, clusters, out_dir / "02_clusters_kmeans.png")
    plot_routes(city, route_orders, out_dir / "03_rotas_otimizadas.png")
    plot_cost_comparison(baseline_km, optimized_total, out_dir / "04_comparativo_distancia.png")

    summary = {
        "empresa": "Sabor Express",
        "hub": city.nodes[hub].nome,
        "total_entregas": int(len(entregas)),
        "entregadores": n_clusters,
        "distancia_baseline_km": round(baseline_km, 2),
        "distancia_otimizada_km": round(optimized_total, 2),
        "economia_percentual": round(economia_pct, 1),
        "rotas": route_details,
    }

    with open(out_dir / "resultado.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    enriched.to_csv(out_dir / "entregas_com_cluster.csv", index=False)

    print("=" * 60)
    print("ROTA INTELIGENTE — Sabor Express")
    print("=" * 60)
    print(f"Entregas: {summary['total_entregas']} | Entregadores: {n_clusters}")
    print(f"Baseline manual: {summary['distancia_baseline_km']} km")
    print(f"Solução IA:      {summary['distancia_otimizada_km']} km")
    print(f"Economia:        {summary['economia_percentual']}%")
    print("-" * 60)
    for rota in route_details:
        print(
            f"Entregador {rota['entregador']}: "
            f"{' → '.join(rota['rota'])} | {rota['distancia_km']} km"
        )
    print("-" * 60)
    print(f"Artefatos salvos em: {out_dir}")
    return summary


if __name__ == "__main__":
    run()
