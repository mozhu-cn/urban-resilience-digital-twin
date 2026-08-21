"""
Convenient entry point for the Urban Resilience Digital Twin.

    python run.py                 # full simulation + interactive 4D animation
    python run.py --no-animation  # headless run
    python run.py --experiments   # run the full experiment pipeline

See DigitalTwin/README.md for details.
"""

import sys


def main():
    args = sys.argv[1:]

    if "--experiments" in args:
        from DigitalTwin.experiments.run_all import main as exp_main
        exp_main()
        return

    # Strip --experiments so argparse in main.py never sees it
    filtered = [a for a in args if a != "--experiments"]
    sys.argv = [sys.argv[0]] + filtered

    from DigitalTwin.main import parse_args, run_simulation
    from DigitalTwin.visualization.digital_twin_viewer import create_animation

    args_obj = parse_args()
    from DigitalTwin.config import CONFIG

    cfg = dict(CONFIG)
    for key, arg_name in [("grid_size", "grid_size"), ("num_frames", "num_frames"),
                          ("total_hours", "total_hours"), ("rain_peak_mmh", "rain_peak"),
                          ("num_fleets", "num_fleets"), ("seed", "seed")]:
        value = getattr(args_obj, arg_name)
        if value is not None:
            cfg[key] = value

    result = run_simulation(cfg, save_csv=True, csv_path=args_obj.out_csv)
    (G_proj, grid_x, grid_y, grid_z, frame_data_list,
     dependency_edges, comm_nodes, nodes, power_nodes, cfg, _df) = result

    if not args_obj.no_animation:
        fig = create_animation(G_proj, grid_x, grid_y, grid_z, frame_data_list,
                               dependency_edges, comm_nodes, nodes, power_nodes, cfg)
        fig.show()
    print("\nSimulation completed.")


if __name__ == "__main__":
    main()
