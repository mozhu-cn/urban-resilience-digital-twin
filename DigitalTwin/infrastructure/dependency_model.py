"""
Interdependent network dependency mapping.

Builds the power -> communication dependency map using a defensive,
self-contained Dijkstra implementation. This intentionally does not rely on
networkx's internal weight-function machinery, which has shown intermittent
instability (crashes / AttributeError) with this MultiDiGraph dataset under
CPython 3.14; the algorithm here only reads plain edge 'length' attributes.
"""

import heapq

import networkx as nx
import random


def dijkstra_length(G, source, target):
    """Shortest path length (by 'length' attribute) between two nodes.

    G : networkx MultiDiGraph (osmnx-style: edge data dicts keyed per parallel
        edge). Defensive: non-dict edge data is treated as weight 1.0 and
        missing 'length' attributes fall back to 1.0.
    """
    adj = G._adj  # {node: {neighbor: {key: data}}}
    dist = {source: 0.0}
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if u == target:
            return d
        if d > dist.get(u, float('inf')):
            continue
        for v, edges in adj.get(u, {}).items():
            w = float('inf')
            if isinstance(edges, dict):
                for attr in edges.values():
                    if not isinstance(attr, dict):
                        continue
                    w = min(w, attr.get('length', 1.0))
            if w == float('inf'):
                w = 1.0
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    raise nx.NetworkXNoPath(f"No path between {source} and {target}")


def build_dependency_map(G_proj, power_nodes, comm_nodes, cfg):
    dependency_map = {}
    dependency_edges = []
    for c_node in comm_nodes:
        min_dist, nearest_p = float('inf'), None
        for p_node in power_nodes:
            try:
                dist = dijkstra_length(G_proj, c_node, p_node)
            except nx.NetworkXNoPath:
                dist = float('inf')
            if dist < min_dist:
                min_dist, nearest_p = dist, p_node
        if nearest_p is not None:
            dependency_map[c_node] = nearest_p
            dependency_edges.append((nearest_p, c_node))
            G_proj.nodes[c_node]['battery'] = random.uniform(cfg["battery_min_h"], cfg["battery_max_h"])
    return dependency_map, dependency_edges
