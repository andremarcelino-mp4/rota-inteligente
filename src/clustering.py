"""Agrupamento de entregas por zona com K-Means."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from .graph import CityGraph


@dataclass
class DeliveryCluster:
    cluster_id: int
    bairro_ids: list[int]
    entrega_ids: list[str]
    centroid_xy: tuple[float, float]


def load_entregas(path) -> pd.DataFrame:
    return pd.read_csv(path)


def cluster_deliveries(
    city: CityGraph,
    entregas: pd.DataFrame,
    n_clusters: int = 3,
    random_state: int = 42,
) -> tuple[list[DeliveryCluster], pd.DataFrame]:
    """
    Agrupa pontos de entrega no espaço (x, y) dos bairros.
    Cada cluster representa a zona de um entregador.
    """
    coords = []
    for row in entregas.itertuples(index=False):
        node = city.nodes[int(row.bairro_id)]
        coords.append([node.x, node.y])

    X = np.array(coords, dtype=float)
    k = min(n_clusters, len(entregas))
    model = KMeans(n_clusters=k, n_init=10, random_state=random_state)
    labels = model.fit_predict(X)

    enriched = entregas.copy()
    enriched["cluster"] = labels
    enriched["x"] = X[:, 0]
    enriched["y"] = X[:, 1]

    clusters: list[DeliveryCluster] = []
    for cid in range(k):
        subset = enriched[enriched["cluster"] == cid]
        bairros = sorted({int(b) for b in subset["bairro_id"].tolist()})
        entrega_ids = subset["id"].tolist()
        cx, cy = model.cluster_centers_[cid]
        clusters.append(
            DeliveryCluster(
                cluster_id=cid,
                bairro_ids=bairros,
                entrega_ids=entrega_ids,
                centroid_xy=(float(cx), float(cy)),
            )
        )

    return clusters, enriched
