import numpy as np
from numba import njit

@njit(fastmath=True)
def ca_flood_step_jit(Z, W, rain_m, dt, drain_rate, pipe_storage):
    W = W + rain_m
    H = Z + W

    # Four-direction water head differences
    dN = np.zeros_like(W); dN[1:,:] = np.maximum(0.0, H[1:,:] - H[:-1,:])
    dS = np.zeros_like(W); dS[:-1,:] = np.maximum(0.0, H[:-1,:] - H[1:,:])
    dW = np.zeros_like(W); dW[:,1:] = np.maximum(0.0, H[:,1:] - H[:,:-1])
    dE = np.zeros_like(W); dE[:,:-1] = np.maximum(0.0, H[:,:-1] - H[:,1:])
    total_d = dN + dS + dW + dE
    safe_total = np.where(total_d == 0, 1.0, total_d)

    outflow_limit = W * 0.12
    qN = (dN / safe_total) * outflow_limit
    qS = (dS / safe_total) * outflow_limit
    qW = (dW / safe_total) * outflow_limit
    qE = (dE / safe_total) * outflow_limit
    W_out = qN + qS + qW + qE

    W_in = np.zeros_like(W)
    W_in[1:,:] += qS[:-1,:]
    W_in[:-1,:] += qN[1:,:]
    W_in[:,1:] += qE[:,:-1]
    W_in[:,:-1] += qW[:,1:]

    W = W - W_out + W_in

    # Drainage (limited by pipe storage)
    drain_possible = drain_rate * dt
    actual_drain = np.minimum(W, drain_possible)
    actual_drain = np.minimum(actual_drain, pipe_storage)
    W -= actual_drain
    pipe_storage -= actual_drain
    W = np.maximum(W, 0.0)
    pipe_storage = np.maximum(pipe_storage, 0.0)
    return W, pipe_storage