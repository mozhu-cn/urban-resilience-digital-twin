"""
Run the complete experiment pipeline:

    1. baselines    : main scenario vs static-flood / no-restoration baselines
    2. sensitivity  : one-at-a-time sensitivity analysis
    3. figures      : publication figures under results/

Usage:  python -m DigitalTwin.experiments.run_all
"""

import os
import sys

_PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PKG_DIR not in sys.path:
    sys.path.insert(0, _PKG_DIR)

from DigitalTwin.experiments import run_baselines, sensitivity, make_figures  # noqa: E402


def main():
    run_baselines.main()
    sensitivity.main()
    make_figures.main()
    print("\n>>> Experiment pipeline completed. See results/.")


if __name__ == "__main__":
    main()
