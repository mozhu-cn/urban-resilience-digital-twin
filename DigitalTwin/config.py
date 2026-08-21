"""
Global configuration for the Urban Resilience Digital Twin.

All tunable parameters of the simulation live here. Paths are resolved
relative to this file so that the package can be executed from any
working directory.
"""

import os

# Root directory of the DigitalTwin package (directory containing this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default cache file (OpenStreetMap graph + elevation), resolved under BASE_DIR
CACHE_FILE = os.path.join(BASE_DIR, "miyazaki_ultimate_cache.pkl")

CONFIG = {
    # ------------------------------------------------------------------ data
    "cache_file": CACHE_FILE,
    "grid_size": 650,                # 650 x 650 = 422,500 cells
    "city_center": (31.9077, 131.4205),   # Miyazaki City, Japan
    "dist_meters": 3000,             # OSM network radius around city center

    # ------------------------------------------------------------- physics
    "dt_ca_seconds": 10.0,           # seconds per CA sub-step
    "ca_steps_per_frame": 30,        # CA sub-steps per animation frame
    "total_hours": 8.0,              # total simulated event length (hours)
    "num_frames": 24,                # number of output frames
    "rain_peak_mmh": 100.0,          # peak rainfall intensity (mm/h)

    # ---------------------------------------------------------- thresholds
    "substation_flood_threshold": 0.5,   # water depth (m) that floods a substation
    "road_block_threshold": 0.3,         # water depth (m) that blocks a road

    # ------------------------------------------------------------- drainage
    "base_drainage_mmh": 1.0,            # base drainage rate (mm/h)
    "max_pipe_storage_m": 0.20,          # max subsurface storage capacity (m)

    # ------------------------------------------------------- infrastructure
    "num_power": 15,
    "num_comm": 40,
    "battery_min_h": 3.0,
    "battery_max_h": 5.0,

    # ---------------------------------------------------------- restoration
    "num_fleets": 2,
    "fleet_speed_kmh": 30.0,
    "repair_time_hours": 1.0,            # time to repair one substation (h)
    "gamma": 5.0,                        # urgency weight in utility function
    "epsilon": 0.01,                     # prevents division by zero

    # ---------------------------------------------------------------- random
    "seed": 42,
}
