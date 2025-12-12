import h5py
import numpy as np
from xdas import DataArray
from xdas.virtual import VirtualSource
from datetime import datetime,timezone
import xarray as xr
from natsort import natsorted
import glob
import pandas as pd

def read_Terra15(fname,timezone=timezone.utc):
  '''
  Open file from Terra15 version 6 using xdas loader

  :param timezone: default (timezone.utc)
  :type timezone: timezone 
  '''

  with h5py.File(fname, "r") as file:
    ti=np.datetime64(datetime.fromtimestamp(file['data_product']['gps_time'][0],tz=timezone)).astype('datetime64[ms]')
    tf=np.datetime64(datetime.fromtimestamp(file['data_product']['gps_time'][-1],tz=timezone)).astype('datetime64[ms]')
    d0 = file.attrs['sensing_range_start']
    dx = file.attrs['dx']
    data = VirtualSource(file['data_product']['data'])
  nt, nd = data.shape
  t = {"tie_indices": [0, nt - 1], "tie_values": [ti, tf]}
  d = {"tie_indices": [0, nd - 1], "tie_values": [d0, d0+ (nd - 1) * dx]}
  return DataArray(data, {"time": t, "distance": d})


def dask_Terra15(fname,timezone=timezone.utc,**kwargs):
  '''
  Open data using xarray dask 

  :param timezone: default (timezone.utc)
  :type timezone: timezone 
  '''

  ds=xr.open_mfdataset(fname,engine='h5netcdf',group='/data_product',phony_dims='sort',concat_dim='phony_dim_0',combine='nested',**kwargs)

  ds=ds.rename({'phony_dim_0': 'time'})


  if isinstance(fname, list):
    da=xr.open_dataset(fname[0])
  else:
    da=xr.open_dataset(natsorted(glob.glob(fname))[0])

  d0 = da.attrs['sensing_range_start']
  dx = da.attrs['dx']

  nt, nd = ds.data.shape

  d = np.linspace(d0,d0+(nd-1)*dx,nd)

  ds=ds.rename({'phony_dim_1': 'distance'})
  ds['distance']=d


  # Convert timestamp in numpy datetime[ns]
  pdt0=ds['gps_time'].to_pandas()
  dt=da.attrs['dt_computer']
  pdt0 = pdt0.astype(float)
  pdt = np.linspace(pdt0[0],pdt0[0]+(nt-1)*dt,nt)
  
  #vectorized_function = np.vectorize(lambda x: datetime.fromtimestamp(x, tz=timezone))
  #pdt = vectorized_function(pdt)

  #pdt = pdt.apply(lambda x: datetime.fromtimestamp(x,tz=timezone))
  #ds['time']= [pd.Timestamp(datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc)).to_pydatetime() for ts in pdt]
  
  ti=datetime.fromtimestamp(pdt[0],tz=timezone.utc)
  tf=datetime.fromtimestamp(pdt[-1],tz=timezone.utc)
  ds['time']=pd.date_range(ti,tf,nt).values



  # Copy attributs
  ds.attrs=da.attrs
  ds.attrs['nt']=nt

  # drop unwanted variable
  ds=ds.drop_vars('posix_time')
  ds=ds.drop_vars('gps_time')
  ds=ds.data.rename('velocity')

  return ds

def dask_febus_one_file(fname, timezone=timezone.utc, **kwargs):
    """
    Open and process Febus DAS data using xarray with dask.

    :param fname: File name or pattern to load with xarray.
    :param timezone: Timezone for datetime conversion (default: UTC).
    :type timezone: timezone object
    :param kwargs: Additional arguments for xarray.open_mfdataset.
    :return: xarray DataArray with time and distance coordinates.
    """

    # Open file with h5py to extract metadata
    with h5py.File(fname, 'r') as fh5f:
        # Extract source and zone attributes for metadata
        src_attr = fh5f['localhost.localdomain']['Source1'].attrs
        zne_attr = fh5f['localhost.localdomain']['Source1']['Zone1'].attrs

        # Extract key parameters from attributes
        prf = zne_attr['PulseRateFreq'] / 1000  # Pulse rate frequency in kHz
        block_rate = zne_attr['BlockRate'] / 1000  # Block rate in kHz
        sampling_res = src_attr['SamplingRes']
        derivation_time = zne_attr['DerivationTime']
        origin = zne_attr['Origin']
        spacing = zne_attr['Spacing']
        gauge_length = zne_attr['GaugeLength']
        overlap = zne_attr['BlockOverlap'][0]  # Overlap percentage

        # Calculate spatial and temporal resolutions
        dt = spacing[1] * 1.e-3  # Temporal resolution in seconds
        dx = spacing[0]          # Spatial resolution in meters

        # Determine data shape and read block times
        channel = list(fh5f['localhost.localdomain']['Source1']['Zone1'].keys())[0]
        node = fh5f['localhost.localdomain']['Source1']['Zone1'][channel]
        block_times = fh5f['localhost.localdomain']['Source1']['time'][:]
        nb_block, block_time_size, block_space_size = node.shape

    # Calculate block-related parameters
    block_time_useful_size = int(100 / (100 + overlap) * block_time_size)
    block_time_overlap_size = int((block_time_size - block_time_useful_size) / 2)
    block_time_offset = (block_time_useful_size / 2) * dt

    # Determine start and end times for useful data in blocks
    block_time_useful_start_time = block_times - block_time_offset
    block_time_useful_end_time = block_time_useful_start_time + block_time_useful_size * dt

    # Open data with xarray using h5netcdf engine
    da = xr.open_mfdataset(
        fname,
        engine='h5netcdf',
        group='localhost.localdomain/Source1/Zone1/',
        phony_dims='sort',
        combine='nested',
        **kwargs
    )

    # Extract the channel data and calculate offsets
    t1, t2, d1 = da[channel].shape
    offset = int((t2 - block_time_useful_size) / 2)

    # Stack dimensions for easier manipulation
    da_stacked = da[channel][:, offset:block_time_useful_size + offset].stack(
        new_dim=('phony_dim_1', 'phony_dim_2')
    )

    # Generate time and distance coordinates
    time = block_time_useful_start_time[0] + np.arange(da_stacked.shape[1]) * dt
    ti = datetime.fromtimestamp(time[0], tz=timezone)
    tf = datetime.fromtimestamp(time[-1], tz=timezone)
    distance = np.arange(d1) * dx

    # Create new time and distance dimensions
    da_stacked = da_stacked.drop_vars(['new_dim', 'phony_dim_1', 'phony_dim_2'])
    da_stacked['new_dim'] = pd.date_range(ti, tf, periods=da_stacked.shape[1]).values
    da_stacked['phony_dim_3'] = distance

    # Rename dimensions for clarity
    da_stacked = da_stacked.rename({'phony_dim_3': 'distance', 'new_dim': 'time'})

    # Add attribut information. It might be nice to have them consistent between terra15 and febus
    da_stacked.attrs['dt']=dt
    da_stacked.attrs['dx']=dx
    da_stacked.attrs['overlap']=overlap

    # Transpose to have 'time' and 'distance' as primary coordinates
    return da_stacked.transpose()

def dask_febus(filenames, timezone=timezone.utc, concat_dim='time', **kwargs):
    """
    Load and combine multiple Febus DAS files using dask_febus_one_file.

    :param filenames: List of file paths to process.
    :param timezone: Timezone for datetime conversion (default: UTC).
    :type timezone: timezone object
    :param concat_dim: Dimension along which to concatenate the data (default: 'time').
    :param kwargs: Additional arguments to pass to dask_febus_one_file.
    :return: Combined xarray.DataArray object.
    """
    data_arrays = []

    for fname in filenames:
        try:
            # Load each file using dask_febus_one_file
            da = dask_febus_one_file(fname, timezone=timezone, **kwargs)
            data_arrays.append(da)
        except Exception as e:
            print(f"Error processing file {fname}: {e}")

    # Concatenate all data along the specified dimension
    combined_da = xr.concat(data_arrays, dim=concat_dim)

    return combined_da