"""Algoritmos de busca em grafos: A* e BFS (referência)."""

from __future__ import annotations

import heapq
from collections import deque

from .graph import CityGraph


def astar(city: CityGraph, start: int, goal: int) -> tuple[list[int], float]:
    """
    A* com heurística euclidiana admissível.
    Retorna (caminho, custo_em_km).
    """
    if start == goal:
        return [start], 0.0

    open_heap: list[tuple[float, int]] = [(0.0, start)]
    g_score = {start: 0.0}
    came_from: dict[int, int] = {}
    closed: set[int] = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == goal:
            return _reconstruct(came_from, current), g_score[current]

        closed.add(current)
        for neighbor in city.graph.neighbors(current):
            tentative = g_score[current] + float(city.graph[current][neighbor]["weight"])
            if tentative < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                f = tentative + city.euclidean(neighbor, goal)
                heapq.heappush(open_heap, (f, neighbor))

    raise ValueError(f"Sem caminho entre {start} e {goal}")


def bfs_path(city: CityGraph, start: int, goal: int) -> list[int]:
    """BFS clássico (menor número de arestas, sem peso)."""
    if start == goal:
        return [start]

    queue = deque([start])
    came_from: dict[int, int | None] = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            path: list[int] = []
            while current is not None:
                path.append(current)
                current = came_from[current]  # type: ignore[assignment]
            return list(reversed(path))

        for neighbor in city.graph.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    raise ValueError(f"Sem caminho entre {start} e {goal}")


def nearest_neighbor_route(
    city: CityGraph, start: int, stops: list[int]
) -> tuple[list[int], float, list[list[int]]]:
    """
    Heurística do vizinho mais próximo entre pontos de entrega.
    Entre cada par consecutivo usa A* no grafo da cidade.
    Retorna (ordem dos bairros visitados incluindo retorno, custo total, segmentos A*).
    """
    remaining = list(dict.fromkeys(stops))  # únicos, preserva ordem inicial
    current = start
    order = [start]
    segments: list[list[int]] = []
    total = 0.0

    while remaining:
        best_node = None
        best_path: list[int] = []
        best_cost = float("inf")
        for candidate in remaining:
            path, cost = astar(city, current, candidate)
            if cost < best_cost:
                best_cost = cost
                best_node = candidate
                best_path = path
        assert best_node is not None
        segments.append(best_path)
        total += best_cost
        order.append(best_node)
        remaining.remove(best_node)
        current = best_node

    # retorno ao hub
    back_path, back_cost = astar(city, current, start)
    segments.append(back_path)
    total += back_cost
    order.append(start)
    return order, total, segments


def _reconstruct(came_from: dict[int, int], current: int) -> list[int]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
