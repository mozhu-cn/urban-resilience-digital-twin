"""
Resilience Digital Twin for Miyazaki City
=========================================
- Terrain-informed cellular-automata flood model (Numba JIT accelerated)
- Interdependent power-communication network with delayed cascading failures
- Adaptive restoration scheduling with repair fleets under flood-constrained
  dynamic road networks
- Plotly 4D animation of the full disaster-response-recovery cycle

Usage
-----
    python main.py                          # run with default configuration
    python main.py --grid-size 200 --num-frames 12
    python main.py --no-animation           # headless run (no plot window)
"""

import argparse
import os
import random
import warnings

import networkx as nx
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from .config import CONFIG
from .data.osm_loader import load_or_fetch_data
from .data.terrain_processing import build_terrain_grid, get_xyz
from .flood_model.cellular_automata import ca_flood_step_jit
from .infrastructure.network_builder import select_infrastructure_nodes, update_road_weights
from .infrastructure.dependency_model import build_dependency_map
from .failure_model.cascading_failure import detect_power_failures, update_communication_batteries
from .restoration.fleet_scheduler import move_fleets, assign_repair_targets
from .visualization.digital_twin_viewer import create_animation

# ============================================================================
# Core Simulation Loop
# ============================================================================
def run_simulation(cfg, save_csv=True, csv_path=None, flood_mode="ca"):
    """Run the full digital twin simulation and return all outputs.

    Parameters
    ----------
    cfg : dict
        Configuration dictionary (see config.py).
    save_csv : bool
        Whether to persist the frame-wise history to CSV.
    csv_path : str or None
        Output path for the history CSV (default: DigitalTwin/simulation_history.csv).
    flood_mode : str
        "ca" uses the terrain-informed cellular-automata flood model;
        "static" uses a spatially uniform bathtub flood approximation
        (Baseline 1 in the paper).

    Returns
    -------
    (G_proj, grid_x, grid_y, grid_z, frame_data_list, dependency_edges,
     comm_nodes, nodes, power_nodes, cfg)
    """
    print("\n>>> [1/6] Loading data & cache...")
    G_proj, nodes, x_coords, y_coords, z_coords = load_or_fetch_data(cfg)

    print(">>> [2/6] Deploying infrastructure & dependencies...")
    power_nodes, comm_nodes = select_infrastructure_nodes(G_proj, nodes, cfg)
    dependency_map, dependency_edges = build_dependency_map(G_proj, power_nodes, comm_nodes, cfg)

    print(">>> [3/6] Building terrain grid...")
    grid_x, grid_y, grid_z, drain_rate, pipe_storage_init, x_min, x_max, y_min, y_max = build_terrain_grid(
        x_coords, y_coords, z_coords, cfg)
    grid_info = (x_min, x_max, y_min, y_max, cfg["grid_size"])

    # Baseline 1: spatially uniform drainage (median of the heterogeneous field)
    static_drain_per_step = float(np.median(drain_rate) * cfg["dt_ca_seconds"])

    # Time discretization
    dt_ca = cfg["dt_ca_seconds"]
    total_seconds = cfg["total_hours"] * 3600.0
    total_ca_steps = int(total_seconds / dt_ca)
    steps_per_frame = total_ca_steps // cfg["num_frames"]
    if steps_per_frame < 1:
        steps_per_frame = 1
        num_frames = total_ca_steps
    else:
        num_frames = cfg["num_frames"]
    frame_duration_seconds = dt_ca * steps_per_frame
    print(f"   -> Total {total_seconds/3600:.1f}h, CA steps: {total_ca_steps}, frames: {num_frames}")

    # Initial states
    W = np.zeros((cfg["grid_size"], cfg["grid_size"]), dtype=np.float64)
    pipe_storage = np.copy(pipe_storage_init)
    power_status = {p: 'Active' for p in power_nodes}   # Active/Flooded/Repairing/Restored
    comm_battery = {c: G_proj.nodes[c]['battery'] for c in comm_nodes}
    comm_initial_battery = dict(comm_battery)

    # Fleet initialization (start at city center)
    center_node = min(nodes, key=lambda n: (G_proj.nodes[n]['x']-np.mean(x_coords))**2 +
                                            (G_proj.nodes[n]['y']-np.mean(y_coords))**2)
    fleets = [{'id': i, 'pos': center_node, 'target': None, 'path': [],
               'progress': 0.0, 'repair_remaining': 0.0} for i in range(cfg["num_fleets"])]

    # Data recording
    history = []
    frame_data_list = []

    print(">>> [4/6] Pre-compiling JIT function...")
    _ = ca_flood_step_jit(grid_z, W, 0.0, dt_ca, drain_rate, pipe_storage)

    print(f">>> [5/6] Starting simulation ({num_frames} frames)...")
    for frame in range(num_frames):
        # Rainfall (sinusoidal peak, Chicago-storm approximation)
        t_ratio = frame / max(1, num_frames - 1)
        rain_mmh = cfg["rain_peak_mmh"] * np.sin(np.pi * t_ratio)
        rain_m_per_step = (rain_mmh / 3600.0 / 1000.0) * dt_ca

        # Run flood steps
        for _ in range(steps_per_frame):
            if flood_mode == "static":
                # Bathtub approximation: no inter-cell exchange, uniform drainage
                W = W + rain_m_per_step
                W = np.maximum(W - static_drain_per_step, 0.0)
            else:
                W, pipe_storage = ca_flood_step_jit(grid_z, W, rain_m_per_step, dt_ca, drain_rate, pipe_storage)

        # Physical damage detection
        power_status = detect_power_failures(G_proj, power_nodes, power_status, W, grid_info, cfg)

        # Update road weights and build temporary travel graph
        edge_weights = update_road_weights(G_proj, W, grid_info, cfg)
        G_temp = nx.Graph()
        for u, v, k, data in G_proj.edges(keys=True, data=True):
            w = edge_weights.get((u, v, k), data.get('length', float('inf')))
            if w < float('inf'):
                if G_temp.has_edge(u, v):
                    if w < G_temp[u][v]['weight']:
                        G_temp[u][v]['weight'] = w
                else:
                    G_temp.add_edge(u, v, weight=w)
        G_temp.add_nodes_from(G_proj.nodes())

        # Fleet scheduling: advance repairs in progress
        for fleet in fleets:
            if fleet['target'] is not None and power_status.get(fleet['target']) == 'Repairing':
                fleet['repair_remaining'] -= frame_duration_seconds
                if fleet['repair_remaining'] <= 0:
                    power_status[fleet['target']] = 'Restored'
                    fleet['target'] = None
                    fleet['path'] = []
                    fleet['repair_remaining'] = 0.0
        # Assign new targets to idle fleets
        fleets, power_status = assign_repair_targets(fleets, power_nodes, power_status, comm_battery,
                                                     dependency_map, G_temp, cfg)

        # Move fleets
        fleets, power_status = move_fleets(fleets, G_temp, frame_duration_seconds, cfg, power_status, power_nodes)

        # Update communication batteries
        comm_battery = update_communication_batteries(comm_nodes, comm_battery, dependency_map,
                                                      power_status, frame_duration_seconds)

        # Collect frame data
        active_p = [p for p in power_nodes if power_status[p] == 'Active']
        flooded_p = [p for p in power_nodes if power_status[p] == 'Flooded']
        repairing_p = [p for p in power_nodes if power_status[p] == 'Repairing']
        restored_p = [p for p in power_nodes if power_status[p] == 'Restored']
        comm_colors = [1 if comm_battery.get(c, 0) > 0 else 0 for c in comm_nodes]
        fleet_positions = [f['pos'] for f in fleets]

        flood_surface = np.where(W > 0.05, grid_z + W, np.nan)
        fd = {
            'water_z': flood_surface,
            'sx': get_xyz(G_proj, active_p)[0], 'sy': get_xyz(G_proj, active_p)[1], 'sz': get_xyz(G_proj, active_p)[2],
            'fx': get_xyz(G_proj, flooded_p)[0], 'fy': get_xyz(G_proj, flooded_p)[1], 'fz': get_xyz(G_proj, flooded_p)[2],
            'rx': get_xyz(G_proj, restored_p)[0], 'ry': get_xyz(G_proj, restored_p)[1], 'rz': get_xyz(G_proj, restored_p)[2],
            'repairx': get_xyz(G_proj, repairing_p)[0], 'repairy': get_xyz(G_proj, repairing_p)[1], 'repairz': get_xyz(G_proj, repairing_p)[2],
            'fleet_x': get_xyz(G_proj, fleet_positions)[0], 'fleet_y': get_xyz(G_proj, fleet_positions)[1],
            'fleet_z': [G_proj.nodes[n]['elevation']+2.0 for n in fleet_positions],
            'cc': comm_colors
        }
        frame_data_list.append(fd)

        max_depth = W.max()
        num_failed_comm = comm_colors.count(0)
        history.append({
            'frame': frame,
            'time_h': frame * frame_duration_seconds / 3600.0,
            'max_depth_m': max_depth,
            'active_power': len(active_p),
            'flooded_power': len(flooded_p),
            'repairing_power': len(repairing_p),
            'restored_power': len(restored_p),
            'failed_comm': num_failed_comm,
        })
        print(f"   [Frame {frame+1:02d}/{num_frames}] depth:{max_depth:.2f}m | flooded:{len(flooded_p)} "
              f"repairing:{len(repairing_p)} restored:{len(restored_p)} comm_failed:{num_failed_comm}")

    # Save history to CSV
    df = pd.DataFrame(history)
    if save_csv:
        out_path = csv_path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "simulation_history.csv")
        df.to_csv(out_path, index=False)
        print(f"   -> Simulation history saved to {out_path}")

    return (G_proj, grid_x, grid_y, grid_z, frame_data_list, dependency_edges,
            comm_nodes, nodes, power_nodes, cfg, df)


def parse_args():
    parser = argparse.ArgumentParser(description="Urban Resilience Digital Twin simulation")
    parser.add_argument("--grid-size", type=int, default=None, help="override grid size")
    parser.add_argument("--num-frames", type=int, default=None, help="override number of frames")
    parser.add_argument("--total-hours", type=float, default=None, help="override event length (h)")
    parser.add_argument("--rain-peak", type=float, default=None, help="override peak rainfall (mm/h)")
    parser.add_argument("--num-fleets", type=int, default=None, help="override number of repair fleets")
    parser.add_argument("--seed", type=int, default=None, help="override random seed")
    parser.add_argument("--out-csv", type=str, default=None, help="path for simulation history CSV")
    parser.add_argument("--no-animation", action="store_true", help="skip the interactive animation")
    return parser.parse_args()


# ============================================================================
# Main Entry
# ============================================================================
if __name__ == "__main__":
    args = parse_args()
    cfg = dict(CONFIG)
    for key, arg_name in [("grid_size", "grid_size"), ("num_frames", "num_frames"),
                          ("total_hours", "total_hours"), ("rain_peak_mmh", "rain_peak"),
                          ("num_fleets", "num_fleets"), ("seed", "seed")]:
        value = getattr(args, arg_name)
        if value is not None:
            cfg[key] = value

    result = run_simulation(cfg, save_csv=True, csv_path=args.out_csv)
    (G_proj, grid_x, grid_y, grid_z, frame_data_list,
     dependency_edges, comm_nodes, nodes, power_nodes, cfg, _df) = result

    if not args.no_animation:
        fig = create_animation(G_proj, grid_x, grid_y, grid_z, frame_data_list,
                               dependency_edges, comm_nodes, nodes, power_nodes, cfg)
        fig.show()
    print("\nSimulation completed.")
