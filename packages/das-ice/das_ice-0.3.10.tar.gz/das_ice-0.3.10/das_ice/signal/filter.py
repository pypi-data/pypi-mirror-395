import warnings
import xarray as xr
import numpy as np
from scipy.signal import butter, sosfiltfilt

class DecimationWarning(UserWarning):
    """Custom warning for decimation issues."""
    pass

def decimate(da, q_int, axis='time'):
    """
    Decimate an xarray.DataArray or Dataset along a specified axis by a given interval.

    Parameters:
    da : xarray.DataArray or xarray.Dataset
        The input data to be decimated.
    q_int : int
        The decimation interval. Must be a positive integer.
    axis : str, optional
        The dimension name along which to decimate. Default is 'time'.

    Returns:
    xarray.DataArray or xarray.Dataset
        The decimated data.

    Raises:
    ValueError:
        If q_int is not a positive integer.
    """
    if not isinstance(q_int, int) or q_int <= 0:
        raise ValueError("q_int must be a positive integer.")

    if axis not in da.dims:
        warnings.warn(f"{axis} is not in the dimensions of the DataArray or Dataset.", 
                      DecimationWarning, stacklevel=2)
        return da
    
    # Perform decimation along the specified axis
    return da.isel(**{axis: slice(0, None, q_int)})

def bandpass(da, lowcut, highcut, order=4, dim='time'):
    """
    Apply a bandpass filter to an xarray.DataArray along a specified dimension,
    lazily and Dask-compatible.
    """

    # 1. Check that the dimension exists
    if dim not in da.dims:
        raise ValueError(f"Dimension '{dim}' is not in the DataArray dims: {list(da.dims)}")

    # 2. Determine sampling frequency from coordinate spacing
    # assumes datetime64[ns] coordinates along `dim`
    dT = (da[dim][1] - da[dim][0]).values.astype(float)  # in nanoseconds
    fs = 1.0 / (dT * 1e-9)  # Hz

    # 3. Design Butterworth bandpass filter in SOS form
    sos = butter(order, [lowcut, highcut], fs=fs, btype='bandpass', output='sos')

    # 4. Function applied to raw NumPy / Dask blocks
    #    xarray.apply_ufunc moves `dim` to the LAST axis -> use axis=-1
    def apply_filter(data):
        return sosfiltfilt(sos, data, axis=-1)

    # 5. Use apply_ufunc to keep metadata, support Dask, and broadcast nicely
    da_bp = xr.apply_ufunc(apply_filter,
            da,
            input_core_dims=[[dim]],      # core dimension for the function
            output_core_dims=[[dim]],     # same core dimension for the output
            vectorize=True,               # loop over non-core dims
            dask="parallelized",          # make it Dask-parallel
            output_dtypes=[da.dtype],     # preserve dtype
            dask_gufunc_kwargs={"allow_rechunk": True})
    return da_bp
