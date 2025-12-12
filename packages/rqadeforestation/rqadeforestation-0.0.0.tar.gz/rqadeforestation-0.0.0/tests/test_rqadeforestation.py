import numpy as np
from rqadeforestation import rqatrend, rqatrend_matrix, rqatrend_dask
import time
import dask.array as da

def test_rqatrend_versus_rqatrendmatrix() -> None:
    x = np.arange(1, 30, step=0.01)
    y = np.sin(x) + 0.1 * x
    assert np.all(rqatrend(y, 0.5, 10, 1) == rqatrend_matrix(np.tile(y, (5, 1)), 0.5, 10, 1))


def _vector_method(ts: np.ndarray, threshold: float) -> float:
    return rqatrend(ts.ravel(), threshold, 10, 1)  # scalar


def vector_method(darr, time_axis, threshold):
    return da.apply_along_axis(_vector_method, time_axis, darr, threshold=threshold)


def matrix_method(darr, time_axis, threshold):
    return rqatrend_dask(darr, timeseries_axis=time_axis, threshold=threshold)


def test_dask_rqatrend_versus_rqatrendmatrix() -> None:
    # ----- Synthetic multidimensional data -----
    # Shape: (batch, channels, time)
    batch = 5000
    channels = 4

    # Base timeseries
    x = np.arange(1, 30, step=0.01)
    y = np.sin(x) + 0.1 * x  # shape (2900,)

    # Create data, broadcast on first dimension
    time_axis = 0
    big_data = np.tile(y[:, None, None], (1, batch, channels))

    # Create data, broadcast on last dimension
    # time_axis = -1
    # big_data = np.tile(y[None, None, :], (batch, channels, 1))

    # Wrap in Dask
    # darr = da.from_array(big_data, chunks=(200, channels, -1))
    darr = da.from_array(big_data, chunks=400)

    print("Original shape:", darr.shape)
    print("Original chunks:", darr.chunks)

    y1 = vector_method(darr, time_axis, threshold=0.5)
    y2 = matrix_method(darr, time_axis, threshold=0.5)

    print("Computing vector method...")
    t0 = time.time()
    res1 = y1.compute()
    t1 = time.time()
    print("Slow method time: %.2f s" % (t1 - t0,))

    print("Computing matrix method...")
    t0 = time.time()
    res2 = y2.compute()
    t1 = time.time()
    print("Fast method time: %.2f s" % (t1 - t0,))

    # Sanity check
    print("Output shapes:", res1.shape, res2.shape)
    assert np.allclose(res1, res2)