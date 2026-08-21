import networkx as nx
import random

def build_dependency_map(G_proj, power_nodes, comm_nodes, cfg):
    dependency_map = {}
    dependency_edges = []
    for c_node in comm_nodes:
        min_dist, nearest_p = float('inf'), None
        for p_node in power_nodes:
            try:
                dist = nx.shortest_path_length(G_proj, source=c_node, target=p_node, weight='length')
            except nx.NetworkXNoPath:
                dist = float('inf')
            if dist < min_dist:
                min_dist, nearest_p = dist, p_node
        if nearest_p is not None:
            dependency_map[c_node] = nearest_p
            dependency_edges.append((nearest_p, c_node))
            G_proj.nodes[c_node]['battery'] = random.uniform(cfg["battery_min_h"], cfg["battery_max_h"])
    return dependency_map, dependency_edges