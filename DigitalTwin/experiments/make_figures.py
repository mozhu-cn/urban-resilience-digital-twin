"""
Generate publication-quality figures for the paper.

    fig1_study_area.png        terrain + road network + infrastructure layout
    fig2_flood_evolution.png   three flood snapshots (buffer / peak / recession)
    fig3_resilience_curves.png Phi(t) of main scenario vs baselines
    fig4_sensitivity.png       one-at-a-time sensitivity of key parameters

All figures are saved under results/. Matplotlib uses the Agg backend so the
script runs headless.
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

from DigitalTwin.config import CONFIG  # noqa: E402
from DigitalTwin.main import run_simulation  # noqa: E402
from DigitalTwin.experiments.scenarios import make_cfg, resilience_curve  # noqa: E402

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results")

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def load_main_result():
    """Run (or reuse) the main scenario and return (result tuple, history)."""
    print(">>> Running main scenario to collect frame data ...")
    result = run_simulation(make_cfg(), save_csv=False)
    return result


def fig1_study_area(result):
    G_proj, grid_x, grid_y, grid_z, frame_data, dep_edges, comm_nodes, nodes, power_nodes, cfg, _ = result
    fig, ax = plt.subplots(figsize=(7.5, 6))
    im = ax.pcolormesh(grid_x, grid_y, grid_z, cmap="terrain", shading="auto")
    plt.colorbar(im, ax=ax, label="Elevation (m)", shrink=0.8)

    for u, v in list(G_proj.edges())[::3]:
        ax.plot([G_proj.nodes[u]["x"], G_proj.nodes[v]["x"]],
                [G_proj.nodes[u]["y"], G_proj.nodes[v]["y"]],
                color="white", linewidth=0.4, alpha=0.55)
    px = [G_proj.nodes[n]["x"] for n in power_nodes]
    py = [G_proj.nodes[n]["y"] for n in power_nodes]
    cx = [G_proj.nodes[n]["x"] for n in comm_nodes]
    cy = [G_proj.nodes[n]["y"] for n in comm_nodes]
    ax.scatter(px, py, marker="s", s=60, c="red", edgecolors="black", linewidths=0.5,
               label="Power substations (15)", zorder=5)
    ax.scatter(cx, cy, marker="D", s=30, c="cyan", edgecolors="black", linewidths=0.4,
               label="Communication stations (40)", zorder=5)
    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_title("Study area: Miyazaki City terrain, road network and deployed infrastructure")
    ax.legend(loc="lower right")
    fig.savefig(os.path.join(RESULTS_DIR, "fig1_study_area.png"))
    plt.close(fig)
    print("   -> fig1_study_area.png")


def fig2_flood_evolution(result):
    G_proj, grid_x, grid_y, grid_z, frame_data, dep_edges, comm_nodes, nodes, power_nodes, cfg, _ = result
    n = len(frame_data)
    picks = [0, n // 2, n - 1]
    labels = ["Early stage (buffer)", "Peak rainfall (saturation)", "Late stage (recession)"]
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.4))
    for ax, idx, lab in zip(axes, picks, labels):
        fd = frame_data[idx]
        depth = np.nan_to_num(fd["water_z"] - grid_z, nan=0.0)
        im = ax.pcolormesh(grid_x, grid_y, depth, cmap="Blues", shading="auto",
                           vmin=0, vmax=max(1.0, float(depth.max())))
        ax.scatter(fd["fx"], fd["fy"], marker="x", s=70, c="black",
                   linewidths=1.2, label="Flooded substation", zorder=5)
        ax.scatter(fd["rx"], fd["ry"], marker="s", s=40, c="lime",
                   edgecolors="black", linewidths=0.4, label="Restored", zorder=5)
        ax.scatter(fd["sx"], fd["sy"], marker="s", s=25, c="red",
                   edgecolors="black", linewidths=0.3, label="Active", zorder=5)
        t = fd.get("t", idx * cfg["total_hours"] / n)
        ax.set_title(f"{lab}\n(t = {t:.1f} h, max depth {depth.max():.2f} m)")
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
    axes[0].legend(loc="upper left", fontsize=7)
    fig.suptitle("Spatial evolution of flood depth under the extreme rainfall scenario", y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "fig2_flood_evolution.png"))
    plt.close(fig)
    print("   -> fig2_flood_evolution.png")


def fig3_resilience_curves():
    history = pd.read_csv(os.path.join(RESULTS_DIR, "baselines_history.csv"))
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    styles = {
        "main": ("#d62728", "-", "Proposed framework (adaptive restoration)"),
        "baseline1_static_flood": ("#1f77b4", "--", "Baseline 1: static bathtub flood"),
        "baseline2_no_restoration": ("#7f7f7f", ":", "Baseline 2: no restoration"),
    }
    for name, (color, ls, lab) in styles.items():
        sub = history[history["scenario"] == name]
        phi = resilience_curve(sub)
        ax.plot(sub["time_h"], phi, color=color, linestyle=ls, linewidth=2, label=lab)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Communication network resilience  $\\Phi(t)$")
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("System resilience trajectories: proposed framework vs baselines")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "fig3_resilience_curves.png"))
    plt.close(fig)
    print("   -> fig3_resilience_curves.png")


def fig4_sensitivity():
    summary = pd.read_csv(os.path.join(RESULTS_DIR, "sensitivity_summary.csv"))
    fig, axes = plt.subplots(1, 4, figsize=(13.5, 3.6))

    def panel(ax, names, xticks, xlabel, metric="max_failed_comm"):
        data = [summary[summary["scenario"] == nm][metric].iloc[0] for nm in names]
        ax.bar(range(len(names)), data, color="#4C72B0", edgecolor="black", linewidth=0.5)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(xticks)
        ax.set_xlabel(xlabel)
        ax.set_ylabel({"max_failed_comm": "Max failed comm. stations",
                       "peak_depth_m": "Peak flood depth (m)",
                       "resilience_auc": "Resilience AUC"} [metric])
        for i, v in enumerate(data):
            ax.text(i, v + 0.3, f"{v:.2f}" if isinstance(v, float) else str(v),
                    ha="center", fontsize=8)

    panel(axes[0], [f"rain_{f}" for f in (0.7, 1.0, 1.3)], ["0.7x", "1.0x", "1.3x"],
          "Rainfall intensity factor", "peak_depth_m")
    panel(axes[1], [f"drain_{f}" for f in (0.5, 1.0, 2.0)], ["0.5x", "1.0x", "2.0x"],
          "Drainage capacity factor", "peak_depth_m")
    panel(axes[2], ["battery_1.5-2.5", "battery_3.0-5.0", "battery_6.0-8.0"],
          ["1.5-2.5 h", "3-5 h", "6-8 h"], "Backup battery duration", "max_failed_comm")
    panel(axes[3], ["fleets_1", "fleets_2", "fleets_4"], ["1", "2", "4"],
          "Number of repair fleets", "max_failed_comm")

    fig.suptitle("One-at-a-time sensitivity analysis of framework parameters", y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(RESULTS_DIR, "fig4_sensitivity.png"))
    plt.close(fig)
    print("   -> fig4_sensitivity.png")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    result = load_main_result()
    fig1_study_area(result)
    fig2_flood_evolution(result)
    fig3_resilience_curves()
    fig4_sensitivity()
    print("\nAll figures written to results/.")


if __name__ == "__main__":
    main()
