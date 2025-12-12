import os
import ctypes as ct
import numpy as np
import dask.array as da
import xarray as xr

class MallocVector(ct.Structure):
    _fields_ = [("pointer", ct.c_void_p),
                ("length", ct.c_int64),
                ("s1", ct.c_int64)]

class MallocMatrix(ct.Structure):
    _fields_ = [("pointer", ct.c_void_p),
                ("length", ct.c_int64),
                ("s1", ct.c_int64),
                ("s2", ct.c_int64)]

def mvptr(A):
    ptr = A.ctypes.data_as(ct.c_void_p)
    a = MallocVector(ptr, ct.c_int64(A.size), ct.c_int64(A.shape[0]))
    return ct.byref(a)

def mmptr(A):
    ptr = A.ctypes.data_as(ct.c_void_p)
    a = MallocMatrix(ptr, ct.c_int64(A.size), ct.c_int64(A.shape[1]), ct.c_int64(A.shape[0]))
    return ct.byref(a)

root_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(root_dir, "lib/rqatrend.so")
lib = ct.CDLL(filename)

def rqatrend(y: np.ndarray, threshold: float, border: int = 10, theiler: int = 1) -> float:
    """
    Calculate the RQA trend for a single time series.
    
    :param y: Input time series data as a numpy array.
    :param threshold: Threshold value for the RQA calculation.
    :param border: Border size for the RQA calculation.
    :param theiler: Theiler window size for the RQA calculation.
    :return: The RQA trend value.
    """
    py = mvptr(y.astype(np.float64))
    lib.rqatrend.argtypes = (ct.POINTER(MallocVector), ct.c_double, ct.c_int64, ct.c_int64)
    lib.rqatrend.restype = ct.c_double
    result_single = lib.rqatrend(py, threshold, border, theiler)
    return result_single


def rqatrend_matrix(matrix: np.ndarray, threshold: float, border: int = 10, theiler: int = 1) -> np.ndarray:
    """
    Calculate the RQA trend for a matrix of time series.
    
    :param matrix: Input time series data as a numpy array of shape (n_timeseries, series_length).
    :param threshold: Threshold value for the RQA calculation.
    :param border: Border size for the RQA calculation.
    :param theiler: Theiler window size for the RQA calculation.
    :return: Numpy array of all RQA trend values of size n_timeseries.
    """

    if not len(matrix.shape) == 2:
        raise Exception("Input to rqatrend_matrix must be 2d") 

    n = matrix.shape[0]
    result_several = np.ones(n)
    p_result_several = mvptr(result_several)
    p_matrix = mmptr(matrix.astype(np.float64))
    # arguments: result_vector, data, threshhold, border, theiler
    lib.rqatrend_inplace.argtypes = (ct.POINTER(MallocVector), ct.POINTER(MallocMatrix), ct.c_double, ct.c_int64, ct.c_int64)
    return_value = lib.rqatrend_inplace(p_result_several, p_matrix, threshold, border, theiler)
    return result_several

def rqatrend_xarray(x, threshold:float, border: int = 10, 
                    theiler: int=1, out_dtype = np.float64,
                    timeaxis_name = "time"):
    return xr.apply_ufunc(
        rqatrend,
        x.chunk({timeaxis_name: -1}),
        kwargs = {'threshold': threshold,'border':border,'theiler':theiler},
        input_core_dims = [[timeaxis_name]],
        output_core_dims = [[]],
        dask = "parallelized",
        vectorize=True,
    )


def rqatrend_dask(x: da.Array, timeseries_axis: int, threshold: float, border: int = 10, theiler: int = 1, out_dtype: type = np.float64) -> da.Array:
    """
    Apply rqatrend to a given dask array.

    Consider comparing this function's performance with a simple `dask.array.apply_along_axis`
    ```py
    import dask.array as da
    da.apply_along_axis(lambda ts: rqatrend(ts.ravel(), threshold, border, theiler), time_axis, darr)
    ```

    :param x: dask Array on which rqatrend should be computed.
    :param timeseries_axis: dask Array axis on which the rqatrend function should be applied
    :param threshold: Threshold value for the RQA calculation.
    :param border: Border size for the RQA calculation.
    :param theiler: Theiler window size for the RQA calculation.
    :param out_dtype: dtype of the output dask array, in case a smaller float representation is wanted, or similar. 
    :return: Dask array of all RQA trend values without the timeseries_axis dimension (it got aggregated by rqatrend).
    """
    # Rechunk so full timeseries axis is in one block
    # do this first so we can use the optimized chunks also for moveaxis
    x_rechunked = x.rechunk({timeseries_axis: -1})

    # Move timeseries axis to the end
    x_moved = da.moveaxis(x_rechunked, timeseries_axis, -1)

    def _block_wrapper(block):
        # block shape: (..., series_length)
        mat = block.reshape(-1, block.shape[-1])  # (n_timeseries, series_length)
        result = rqatrend_matrix(mat, threshold, border, theiler)  # (n_timeseries,)
        return result.reshape(block.shape[:-1])   # reduce last axis

    return x_moved.map_blocks(
        _block_wrapper,
        dtype=out_dtype,
        drop_axis=-1   # <---- tell Dask we removed the last axis
    )

def main() -> None:
    pass

main()
