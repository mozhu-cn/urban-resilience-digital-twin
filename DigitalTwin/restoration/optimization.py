def compute_utility(p, power_status, comm_battery, dependency_map, cfg):
    """Calculate priority score for a flooded power node."""
    total = 0.0
    for c, bat in comm_battery.items():
        if dependency_map.get(c) == p and bat > 0:
            total += 1.0 + cfg["gamma"] / (bat + cfg["epsilon"])
    return total