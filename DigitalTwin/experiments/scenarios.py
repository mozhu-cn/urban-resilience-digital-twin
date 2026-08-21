"""
Experiment scenarios for the Urban Resilience Digital Twin.

Main scenario, Baseline 1 (static bathtub flood) and Baseline 2
(no restoration) share the same simulation driver; they differ only in
flood_mode / num_fleets. Sensitivity runs vary one parameter at a time.
"""

import os
import sys

import numpy as np
import pandas as pd

# Make the DigitalTwin package importable from anywhere
_PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

from DigitalTwin.config import CONFIG  # noqa: E402
from DigitalTwin.main import run_simulation  # noqa: E402


def make_cfg(**overrides):
    """Return a fresh CONFIG copy with the given overrides applied."""
    cfg = dict(CONFIG)
    cfg.update(overrides)
    return cfg


def resilience_curve(history):
    """Communication-network resilience index Phi(t) = S_c(t) / N from history."""
    return 1.0 - history["failed_comm"].to_numpy(dtype=float) / CONFIG["num_comm"]


def run_scenario(name, cfg, flood_mode="ca", num_fleets=None):
    """Run one scenario; returns (history DataFrame, summary dict)."""
    if num_fleets is not None:
        cfg["num_fleets"] = num_fleets
    result = run_simulation(cfg, save_csv=False, flood_mode=flood_mode)
    history = result[-1]  # run_simulation now returns the history DataFrame last
    return history, summary_from_history(history, name)


def summary_from_history(history, name):
    """Compute paper-ready summary metrics for one scenario."""
    phi = resilience_curve(history)
    t = history["time_h"].to_numpy()
    T = t[-1] if len(t) else 1.0
    return {
        "scenario": name,
        "peak_depth_m": float(history["max_depth_m"].max()),
        "max_flooded_power": int(history["flooded_power"].max()),
        "restored_power_final": int(history["restored_power"].iloc[-1]),
        "max_failed_comm": int(history["failed_comm"].max()),
        "final_phi": float(phi[-1]),
        "min_phi": float(phi.min()),
        "resilience_auc": float(np.trapezoid(phi, t) / T) if len(t) > 1 else float(phi[-1]),
        "recovery_time_h": _recovery_time(t, phi),
    }


def _recovery_time(t, phi, target=0.95):
    """First time at which Phi recovers to `target` of its initial value (or NaN)."""
    initial = phi[0]
    if initial <= 0:
        return float("nan")
    thr = initial * target
    idx = np.where(phi >= thr)[0]
    return float(t[idx[0]]) if len(idx) else float("nan")
