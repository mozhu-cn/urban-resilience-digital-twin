"""
One-at-a-time sensitivity analysis of key framework parameters.

Factors
    rainfall intensity   : rain_peak_mmh x {0.7, 1.0, 1.3}
    drainage capacity    : base_drainage_mmh x {0.5, 1.0, 2.0}
    backup battery       : battery_min/max_h x {(1.5,2.5), (3,5), (6,8)}
    repair resources     : num_fleets x {1, 2, 4}

Outputs
    results/sensitivity_history.csv   frame-wise trajectories
    results/sensitivity_summary.csv   summary metrics per configuration
"""

import os
import sys

import pandas as pd

_PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

from DigitalTwin.experiments.scenarios import make_cfg, run_scenario  # noqa: E402

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    configs = []
    for factor in (0.7, 1.0, 1.3):
        configs.append((f"rain_{factor}", make_cfg(rain_peak_mmh=round(100.0 * factor, 1))))
    for factor in (0.5, 1.0, 2.0):
        configs.append((f"drain_{factor}", make_cfg(base_drainage_mmh=round(1.0 * factor, 2))))
    for lo, hi in ((1.5, 2.5), (3.0, 5.0), (6.0, 8.0)):
        configs.append((f"battery_{lo}-{hi}", make_cfg(battery_min_h=lo, battery_max_h=hi)))
    for n in (1, 2, 4):
        configs.append((f"fleets_{n}", make_cfg(num_fleets=n)))

    histories, summaries = [], []
    for name, cfg in configs:
        print(f"\n{'='*70}\nSensitivity run: {name}\n{'='*70}")
        history, summary = run_scenario(name, cfg)
        history = history.copy()
        history.insert(0, "scenario", name)
        histories.append(history)
        summaries.append(summary)
        print(f"   -> {summary}")
        # incremental persistence
        pd.concat(histories, ignore_index=True).to_csv(
            os.path.join(RESULTS_DIR, "sensitivity_history.csv"), index=False)
        pd.DataFrame(summaries).to_csv(
            os.path.join(RESULTS_DIR, "sensitivity_summary.csv"), index=False)

    summary_df = pd.DataFrame(summaries)
    print(f"\nSaved -> results/sensitivity_history.csv / sensitivity_summary.csv")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
