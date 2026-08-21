import networkx as nx

def move_fleets(fleets, G_temp, frame_duration_seconds, cfg, power_status, power_nodes):
    speed_mps = cfg["fleet_speed_kmh"] * 1000.0 / 3600.0
    move_distance = speed_mps * frame_duration_seconds
    for fleet in fleets:
        if fleet['target'] is None or len(fleet['path']) < 2:
            continue
        remaining_dist = move_distance
        while remaining_dist > 0 and len(fleet['path']) > 1:
            u = fleet['path'][0]
            v = fleet['path'][1]
            try:
                edge_len = G_temp[u][v]['weight']
            except KeyError:
                try:
                    new_path = nx.shortest_path(G_temp, source=fleet['pos'], target=fleet['target'], weight='weight')
                    fleet['path'] = new_path
                    break
                except nx.NetworkXNoPath:
                    if fleet['target'] in power_nodes and power_status[fleet['target']] == 'Repairing':
                        power_status[fleet['target']] = 'Flooded'
                    fleet['target'] = None
                    fleet['path'] = []
                    break
            dist_to_go = edge_len - fleet['progress']
            if remaining_dist >= dist_to_go:
                remaining_dist -= dist_to_go
                fleet['pos'] = v
                fleet['path'].pop(0)
                fleet['progress'] = 0.0
            else:
                fleet['progress'] += remaining_dist
                remaining_dist = 0
    return fleets, power_status

def assign_repair_targets(fleets, power_nodes, power_status, comm_battery, dependency_map, G_temp, cfg):
    """
    Assign idle fleets to flooded power nodes based on utility.
    Returns updated fleets and power_status.
    """
    from .optimization import compute_utility
    for fleet in fleets:
        if fleet['target'] is None or power_status.get(fleet['target']) in ('Restored', 'Active'):
            candidates = [p for p in power_nodes if power_status[p] == 'Flooded']
            targeted = [f['target'] for f in fleets if f['target'] is not None]
            candidates = [p for p in candidates if p not in targeted]
            if candidates:
                best = max(candidates, key=lambda p: compute_utility(p, power_status, comm_battery, dependency_map, cfg))
                if fleet['pos'] in G_temp and best in G_temp:
                    try:
                        path = nx.shortest_path(G_temp, source=fleet['pos'], target=best, weight='weight')
                        fleet['target'] = best
                        fleet['path'] = path
                        fleet['progress'] = 0.0
                        fleet['repair_remaining'] = cfg["repair_time_hours"] * 3600.0
                        power_status[best] = 'Repairing'
                    except nx.NetworkXNoPath:
                        pass
    return fleets, power_status