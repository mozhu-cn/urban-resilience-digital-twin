"""
Run the main scenario and the two baselines, persist results and summaries.

    Main scenario   : full framework (CA flood + cascading failures + restoration)
    Baseline 1      : static bathtub flood approximation (flood_mode="static")
    Baseline 2      : no restoration intervention (num_fleets=0)

Outputs
    results/baselines_history.csv   frame-wise trajectories of all scenarios
    results/baselines_summary.csv   summary metrics per scenario
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

    runs = [
        ("main",        make_cfg(),                          "ca",     None),
        ("baseline1_static_flood", make_cfg(),               "static", None),
        ("baseline2_no_restoration", make_cfg(num_fleets=0), "ca",     0),
    ]

    histories, summaries = [], []
    for name, cfg, mode, fleets in runs:
        print(f"\n{'='*70}\nScenario: {name} (flood_mode={mode}, fleets={fleets})\n{'='*70}")
        history, summary = run_scenario(name, cfg, flood_mode=mode, num_fleets=fleets)
        history = history.copy()
        history.insert(0, "scenario", name)
        histories.append(history)
        summaries.append(summary)
        print(f"   -> {summary}")
        # incremental persistence: each scenario is saved as it completes
        pd.concat(histories, ignore_index=True).to_csv(
            os.path.join(RESULTS_DIR, "baselines_history.csv"), index=False)
        pd.DataFrame(summaries).to_csv(
            os.path.join(RESULTS_DIR, "baselines_summary.csv"), index=False)

    summary_df = pd.DataFrame(summaries)
    print(f"\nSaved {len(all_history := pd.concat(histories, ignore_index=True))} "
          f"rows -> results/baselines_history.csv")
    print(f"Saved summary -> results/baselines_summary.csv")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
