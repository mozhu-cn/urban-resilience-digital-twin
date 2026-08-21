import random
import networkx as nx
import numpy as np

def select_infrastructure_nodes(G_proj, nodes, cfg):
    random.seed(cfg["seed"])
    power_nodes = random.sample(nodes, cfg["num_power"])
    remaining = list(set(nodes) - set(power_nodes))
    comm_nodes = random.sample(remaining, cfg["num_comm"])
    return power_nodes, comm_nodes

def update_road_weights(G_proj, W, grid_info, cfg):
    x_min, x_max, y_min, y_max, grid_size = grid_info
    from ..data.terrain_processing import get_grid_idx
    edge_weights = {}
    for u, v, k, data in G_proj.edges(keys=True, data=True):
        ux, uy = G_proj.nodes[u]['x'], G_proj.nodes[u]['y']
        vx, vy = G_proj.nodes[v]['x'], G_proj.nodes[v]['y']
        mx, my = (ux+vx)/2, (uy+vy)/2
        ix, iy = get_grid_idx(mx, my, x_min, x_max, y_min, y_max, grid_size)
        if W[ix, iy] > cfg["road_block_threshold"]:
            edge_weights[(u, v, k)] = float('inf')
        else:
            edge_weights[(u, v, k)] = data.get('length', 1.0)
    return edge_weights