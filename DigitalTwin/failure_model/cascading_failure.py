from ..data.terrain_processing import get_grid_idx

def detect_power_failures(G_proj, power_nodes, power_status, W, grid_info, cfg):
    x_min, x_max, y_min, y_max, grid_size = grid_info
    for p in power_nodes:
        if power_status[p] == 'Active':
            px, py = G_proj.nodes[p]['x'], G_proj.nodes[p]['y']
            ix, iy = get_grid_idx(px, py, x_min, x_max, y_min, y_max, grid_size)
            if W[ix, iy] > cfg["substation_flood_threshold"]:
                power_status[p] = 'Flooded'
    return power_status

def update_communication_batteries(comm_nodes, comm_battery, dependency_map, power_status, frame_duration_seconds):
    for c in comm_nodes:
        if comm_battery[c] > 0:
            dep_p = dependency_map.get(c)
            if dep_p is not None and power_status.get(dep_p) in ('Flooded', 'Repairing'):
                comm_battery[c] -= frame_duration_seconds / 3600.0
                if comm_battery[c] < 0:
                    comm_battery[c] = 0
    return comm_battery