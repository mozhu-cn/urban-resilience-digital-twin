import numpy as np

def compute_drainage_parameters(slope_norm, cfg):
    base_drain_mps = cfg["base_drainage_mmh"] / 3600.0 / 1000.0
    drainage_rate = base_drain_mps * (1 + 2.0 * slope_norm)
    pipe_storage_init = cfg["max_pipe_storage_m"] * (1 - 0.75 * slope_norm)
    return drainage_rate, pipe_storage_init