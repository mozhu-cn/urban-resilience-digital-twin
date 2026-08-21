import hashlib

import numpy as np
import scipy.ndimage as ndimage
from scipy.interpolate import griddata
from ..flood_model.drainage_model import compute_drainage_parameters

# Cache the terrain grid across runs that use identical coordinate arrays
# (the experiment pipeline re-uses the same cached OSM data many times).
_terrain_cache = {}

def _grid_cache_key(x_coords, y_coords, z_coords, grid_size):
    h = hashlib.sha1()
    for arr in (x_coords, y_coords, z_coords):
        h.update(np.ascontiguousarray(arr).tobytes())
    return (grid_size, h.hexdigest())

def build_terrain_grid(x_coords, y_coords, z_coords, cfg):
    key = _grid_cache_key(x_coords, y_coords, z_coords, cfg["grid_size"])
    if key in _terrain_cache:
        return _terrain_cache[key]

    x_min, x_max = x_coords.min(), x_coords.max()
    y_min, y_max = y_coords.min(), y_coords.max()
    grid_size = cfg["grid_size"]
    grid_x, grid_y = np.mgrid[x_min:x_max:complex(grid_size), y_min:y_max:complex(grid_size)]
    grid_z = griddata((x_coords, y_coords), z_coords, (grid_x, grid_y), method='linear')
    grid_z = np.where(np.isnan(grid_z),
                      griddata((x_coords, y_coords), z_coords, (grid_x, grid_y), method='nearest'),
                      grid_z)
    grid_z = ndimage.gaussian_filter(grid_z, sigma=0.8)

    # Slope-based drainage parameters
    dy, dx = np.gradient(grid_z)
    slope = np.sqrt(dx**2 + dy**2)
    slope_norm = (slope - slope.min()) / (slope.max() - slope.min() + 1e-9)
    drainage_rate, pipe_storage_init = compute_drainage_parameters(slope_norm, cfg)

    result = (grid_x, grid_y, grid_z, drainage_rate, pipe_storage_init, x_min, x_max, y_min, y_max)
    _terrain_cache[key] = result
    return result

def get_grid_idx(x, y, x_min, x_max, y_min, y_max, grid_size):
    ix = int((x - x_min) / (x_max - x_min) * (grid_size - 1))
    iy = int((y - y_min) / (y_max - y_min) * (grid_size - 1))
    return np.clip(ix, 0, grid_size-1), np.clip(iy, 0, grid_size-1)

def get_xyz(G_proj, nodes):
    return ([G_proj.nodes[n]['x'] for n in nodes],
            [G_proj.nodes[n]['y'] for n in nodes],
            [G_proj.nodes[n]['elevation'] for n in nodes])