from itertools import product
import dask.array as da
import numpy as np
import xarray as xr
import torch
from memory_profiler import profile
import plotly.graph_objects as go

def MFP_2D_series(ds,delta_t,stations,zrange=[0,100],freqrange=[100,200],xrange=[0,50],vrange=[2500,3500],dz=1,dx=1,dv=250):
    '''
    Perform Matched Field Processing (MFP) on 2D series data to compute beamforming power 
    over a range of spatial coordinates, velocities, and frequencies.

    :param ds: Input data as an xarray DataArray containing waveform data. 
               Must include 'distance' and 'time' coordinates.
    :type ds: xarray.DataArray

    :param delta_t: Time window size (in seconds) for processing the data in small chunks.
    :type delta_t: float

    :param stations: List of station coordinates used for processing.
    :type stations: list of tuples or ndarray of shape (n_stations, 2)

    :param zrange: Range of depths to compute (start and end), default is [0, 100].
    :type zrange: list of float or int

    :param freqrange: Frequency range for processing in Hz (start and end), default is [100, 200].
    :type freqrange: list of float

    :param xrange: Range of horizontal x-coordinates to search (start and end), default is [0, 50].
    :type xrange: list of float or int

    :param vrange: Velocity range to search in m/s (start and end), default is [1000, 6000].
    :type vrange: list of float or int

    :param dz: Spacing between grid points in the depth dimension (z), default is 1.
    :type dz: float or int

    :param dx: Spacing between grid points in the horizontal x dimension, default is 1.
    :type dx: float or int

    :param dv: Spacing between velocities, default is 100.
    :type dv: float or int

    :return: A 3D xarray DataArray containing the computed beampower values. The dimensions are
             'velocity', 'true_time', 'x', 'z'.
    :rtype: xarray.DataArray
    '''
    sampling_rate=(ds.time[1]-ds.time[0]).values.astype(float)*10**-9
    # defined number of sample per time series
    dn=int(delta_t/sampling_rate)
    # build a data cube with a dimention for each time series
    ll=[]
    true_time=[]
    din=int(len(ds.time)/dn)
    for i in range(din):
        tmp=ds[:,i*dn:(i+1)*dn]
        new_time = np.arange(dn) * sampling_rate
        true_time.append(tmp.time[0].values)
        tmp = tmp.assign_coords(time=new_time)
        ll.append(tmp)
    ds_cube=xr.concat(ll,dim='true_time')
    # Normalized
    ds_cube_norm=(ds_cube**2).sum(dim='time')**0.5
    ds_cube=ds_cube/ds_cube_norm
    # Fiber signal processing
    multi_waveform_spectra=torch.fft.fft(torch.from_numpy(ds_cube.values),axis=2).to(dtype=torch.complex128)
    # Normalized over each frequencies
    spectral_norm = torch.abs(multi_waveform_spectra) # Spectral norm
    # Replace 0 values with 1
    spectral_norm[spectral_norm == 0] = 1
    multi_waveform_spectra = multi_waveform_spectra/spectral_norm
    #
    freqs = torch.fft.fftfreq(len(ds_cube.time),sampling_rate)
    omega = 2 * torch.pi * freqs
    # frequency sampling
    freq_idx = torch.where((freqs >= freqrange[0]) & (freqs <= freqrange[1]))[0]
    omega_lim = omega[freq_idx]
    waveform_spectra_lim = multi_waveform_spectra[:,:,freq_idx]
    K = waveform_spectra_lim[:,:, None, :] * waveform_spectra_lim.conj()[:,None, :, :]
    diag_idxs = torch.arange(K.shape[1])
    zero_spectra = torch.zeros(omega_lim.shape, dtype=torch.cdouble)
    K[:,diag_idxs, diag_idxs, :] = zero_spectra
    K = da.from_array(K.numpy())
    # Compute grid
    x_coords = torch.arange(xrange[0], xrange[1] + dx, dx)
    z_coords = torch.arange(zrange[0], zrange[1] + dz, dz)
    v_coords=torch.arange(vrange[0], vrange[1] + dv, dv)
    gridpoints = torch.tensor(list(product(x_coords, z_coords)))

    stations=torch.tensor(stations).to(dtype=torch.complex128)
    distances_to_all_gridpoints = torch.linalg.norm(gridpoints[:, None, :] - stations[None, :, :], axis=2)
    # Compute traveltimes
    traveltimes=distances_to_all_gridpoints[None,:,:]/v_coords[:,None,None]
    greens_functions = torch.exp(-1j * omega_lim[None, None,None, :] * traveltimes[:, :, :, None])
    # move critical part to dask
    greens_functions_dask = da.from_array(greens_functions.numpy(), chunks='auto')
    S = (greens_functions_dask[:, :,:, None,:]*greens_functions_dask.conj()[:,:, None, :,:])
    # Perform the einsum operation
    beampowers_d = da.einsum("vlgijw, ljiw -> vlg", S[:, None , :, :, :, :], K).real
    beampowers = beampowers_d.compute()
    bp = beampowers.reshape(len(v_coords),din, len(x_coords), len(z_coords))

    res=xr.DataArray(bp,dims=['velocity','true_time','x','z'])
    res['velocity']=v_coords
    res['true_time']=true_time
    res['x']=x_coords
    res['z']=z_coords

    res=res.transpose("z","x","velocity","true_time")/((stations.shape[0]-1)*stations.shape[0]*len(omega_lim))
    
    return res

@profile
def MFP_3D_series(ds,delta_t,stations,xrange=[-100,100],yrange=[-100,100],zrange=[-100,100],vrange=[2500,2500],freqrange=[100,200],dx=5,dy=5,dz=5,dv=250,n_fft=None):
    '''
    Perform Matched Field Processing (MFP) on 3D series data to compute beamforming power 
    over a range of spatial coordinates, velocities, and frequencies.

    :param ds: Input data as an xarray DataArray containing waveform data. 
               Must include 'distance' and 'time' coordinates.
    :type ds: xarray.DataArray

    :param delta_t: Time window size (in seconds) for processing the data in small chunks.
    :type delta_t: float

    :param stations: List of station coordinates used for processing.
    :type stations: list of tuples or ndarray of shape (n_stations, 3)

    :param xrange: Range of horizontal x-coordinates to search (start and end), default is [-100, 100].
    :type xrange: list of float or int

    :param yrange: Range of horizontal y-coordinates to search (start and end), default is [-100, 100].
    :type yrange: list of float or int

    :param zrange: Range of depths to compute (start and end), default is [-100, 100].
    :type zrange: list of float or int

    :param vrange: Velocity range to search in m/s (start and end), default is [2500, 2500].
    :type vrange: list of float or int

    :param freqrange: Frequency range for processing in Hz (start and end), default is [100, 200].
    :type freqrange: list of float

    :param dx: Spacing between grid points in the horizontal x dimension, default is 5.
    :type dx: float or int

    :param dy: Spacing between grid points in the horizontal y dimension, default is 5.
    :type dy: float or int

    :param dz: Spacing between grid points in the depth dimension (z), default is 5.
    :type dz: float or int

    :param dv: Spacing between velocities, default is 250.
    :type dv: float or int

    :param n_fft: n in torch.fft.fft function
    :type dv: int

    :return: A 4D xarray DataArray containing the computed beampower values. The dimensions are
             'velocity', 'true_time', 'x', 'y', 'z'.
    :rtype: xarray.DataArray
    '''
    
    sampling_rate=(ds.time[1]-ds.time[0]).values.astype(float)*10**-9
    # defined number of sample per time series
    dn=int(delta_t/sampling_rate)
    # build a data cube with a dimention for each time series
    ll=[]
    true_time=[]
    din=int(len(ds.time)/dn)
    for i in range(din):
        tmp=ds[:,i*dn:(i+1)*dn]
        new_time = np.arange(dn) * sampling_rate
        true_time.append(tmp.time[0].values)
        tmp = tmp.assign_coords(time=new_time)
        ll.append(tmp)
    ds_cube=xr.concat(ll,dim='true_time')
    ############
    ##
    ############
    if n_fft is None:
        n_fft=len(ds_cube.time)
    else:
        sampling_rate*=len(ds_cube.time)/n_fft


    # Fiber signal processing
    multi_waveform_spectra=torch.fft.fft(torch.from_numpy(ds_cube.values),axis=2,n=n_fft).to(dtype=torch.complex128)
    freqs = torch.fft.fftfreq(n_fft,sampling_rate)
    # Normalized over each frequencies
    spectral_norm = torch.abs(multi_waveform_spectra) # Spectral norm
    # Replace 0 values with 1
    spectral_norm[spectral_norm == 0] = 1
    multi_waveform_spectra = multi_waveform_spectra/spectral_norm
    #
    omega = 2 * torch.pi * freqs
    # frequency sampling
    freq_idx = torch.where((freqs >= freqrange[0]) & (freqs <= freqrange[1]))[0]
    omega_lim = omega[freq_idx]
    waveform_spectra_lim = multi_waveform_spectra[:,:,freq_idx]
    


    K = waveform_spectra_lim[:,:, None, :] * waveform_spectra_lim.conj()[:,None, :, :]
    diag_idxs = torch.arange(K.shape[1])
    zero_spectra = torch.zeros(omega_lim.shape, dtype=torch.cdouble)
    K[:,diag_idxs, diag_idxs, :] = zero_spectra
    K = da.from_array(K.numpy())
    
    # Compute grid
    x_coords = torch.arange(xrange[0], xrange[1] + dx, dx)
    y_coords = torch.arange(yrange[0], yrange[1] + dy, dy)
    z_coords = torch.arange(zrange[0], zrange[1] + dz, dz)
    v_coords=torch.arange(vrange[0], vrange[1] + dv, dv)
    gridpoints = torch.tensor(list(product(x_coords, y_coords, z_coords)))

    stations=torch.tensor(stations).to(dtype=torch.complex128)
    distances_to_all_gridpoints = torch.linalg.norm(gridpoints[:, None, :] - stations[None, :, :], axis=2)

    # Compute traveltimes
    traveltimes=distances_to_all_gridpoints[None,:,:]/v_coords[:,None,None]
    greens_functions = torch.exp(-1j * omega_lim[None, None,None, :] * traveltimes[:, :, :, None])
    # move critical part to dask
    greens_functions_dask = da.from_array(greens_functions.numpy(), chunks='auto')
    S = (greens_functions_dask[:, :,:, None,:]*greens_functions_dask.conj()[:,:, None, :,:])
    # Perform the einsum operation
    beampowers_d = da.einsum("vlgijw, ljiw -> vlg", S[:, None , :, :, :, :], K).real
    beampowers = beampowers_d.compute()
    bp = beampowers.reshape(len(v_coords),din, len(x_coords), len(y_coords), len(z_coords))

    res=xr.DataArray(bp,dims=['velocity','true_time','x','y','z'])
    res['velocity']=v_coords
    res['true_time']=true_time
    res['x']=x_coords
    res['y']=y_coords
    res['z']=z_coords

    res=res.transpose("x","y","z","velocity","true_time")/((stations.shape[0]-1)*stations.shape[0]*len(omega_lim))
    
    return res



def artificial_sources_freq(sensors,sources,velocity,sampling_rate=100,window_length=200):
    '''
    Generate synthetic source waveforms based on artificial sources using frequency domain 
    wavelet transforms for seismic-like data simulation.

    :param sensors: Coordinates of the sensors receiving the signal.
    :type sensors: ndarray of shape (n_sensors, 3)

    :param sources: Coordinates of the sources generating the signal.
    :type sources: ndarray of shape (n_sources, 3)

    :param velocity: Velocity of wave propagation (m/s).
    :type velocity: float

    :param sampling_rate: Sampling rate of the signals (Hz), default is 100.
    :type sampling_rate: float

    :param window_length: Length of the time window for the wavelet (samples), default is 200.
    :type window_length: int

    :return: A xarray DataArray containing the generated waveforms.
    :rtype: xarray.DataArray
    '''
    
    tsensors=torch.tensor(sensors).to(dtype=torch.complex128)
    tsources=torch.tensor(sources).to(dtype=torch.complex128)
    distances = torch.linalg.norm(tsensors - tsources, axis=1)

    traveltimes = (distances / velocity)
    
    # define source wavelet
    times = np.arange(0, window_length + 1 / sampling_rate, 1 / sampling_rate)
    
    # compute frequencies
    freqs = torch.fft.fftfreq(len(times), 1 / sampling_rate)
    omega = 2 * np.pi * freqs

    #wavelet = torch.fft.fft(torch.from_numpy(ricker(len(times), scale*sampling_rate)))

    waveform_spectra = torch.exp(-1j * omega[None, :] * traveltimes[:, None])
    waveforms = torch.fft.ifft(waveform_spectra, axis=1).real

    da=xr.DataArray(waveforms,dims=['distance','time'])
    da['time']=times*10**9
    return da

def plot_MFP3D(MFP3d,sensors,true_source=None):
    '''
    Visualize the results of the 3D Matched Field Processing (MFP) using a 3D surface plot
    with interactive animation to show beamforming power distribution at different depths.

    :param MFP3d: The output from the MFP 3D processing.
    :type MFP3d: xarray.DataArray

    :param sensors: Coordinates of the sensors used for processing.
    :type sensors: ndarray of shape (n_sensors, 3)

    :param true_source: Coordinates of the true source, if known (optional).
    :type true_source: list or tuple of 3 float values

    :return: A Plotly figure containing the 3D surface plot and scatter plots for sources and sensors.
    :rtype: plotly.graph_objects.Figure
    '''
    sources=MFP3d.where(MFP3d == MFP3d.max(), drop=True).coords
    x = MFP3d.x.values
    y = MFP3d.y.values
    z = MFP3d.z.values
    vv=np.max(np.abs(MFP3d.values))
    matching_index = int(np.where(MFP3d.z.values == sources['z'].values)[0])
    # Create initial surface trace
    initial_surface = go.Surface(
        x=x,
        y=y,
        z=np.full_like(MFP3d[...,matching_index].T, z[matching_index]),
        surfacecolor=MFP3d[...,matching_index].T,
        colorscale='RdBu_r',
        opacity=1,
        showscale=True,
        cmin=-vv,
        cmax=vv
    )

    # Create the figure with the initial surface
    fig = go.Figure(data=[initial_surface])

    # Add scatter points for sources
    fig.add_trace(go.Scatter3d(
        x=sources['x'],
        y=sources['y'],
        z=sources['z'],
        mode='markers',
        marker=dict(size=10, color='red'),
        name='Found Sources'
    ))

    if true_source is not None:
        fig.add_trace(go.Scatter3d(
            x=[true_source[0]],
            y=[true_source[1]],
            z=[true_source[2]],
            mode='markers',
            marker=dict(size=5, color='blue'),
            name='True Sources'
        ))
    

    # Add scatter points for Black Holseismice
    fig.add_trace(go.Scatter3d(
        x=sensors[:,0],
        y=sensors[:,1],
        z=sensors[:,2],
        mode='markers',
        marker=dict(size=5, color='black', symbol='diamond'),
        name='Sensors'
    ))

    # Create frames for animation
    frames = []
    for i in range(len(z)):
        frame = go.Frame(
            data=[go.Surface(
                z=np.full_like(MFP3d[...,i].T, z[i]),
                surfacecolor=MFP3d[...,i].T,
                colorscale='RdBu_r',
                opacity=1,
                showscale=True,
                cmin=-vv,
                cmax=vv
            )],
            name=f"{z[i]:.2f}"
        )
        frames.append(frame)

    fig.frames = frames

    # Create slider
    sliders = [dict(
        active=matching_index,
        yanchor="top",
        xanchor="left",
        currentvalue=dict(
            font=dict(size=16),
            prefix="Z: ",
            visible=True,
            xanchor="right"
        ),
        transition=dict(duration=300, easing="cubic-in-out"),
        pad=dict(b=10, t=50),
        len=0.9,
        x=0.1,
        y=0,
        steps=[dict(
            label=f"{z[i]:.2f}",
            method="animate",
            args=[[f"{z[i]:.2f}"], dict(
                frame=dict(duration=300, redraw=True),
                mode="immediate",
                transition=dict(duration=300)
            )]
        ) for i in range(len(z))]
    )]


    # Update layout
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=0,
            x=0,
            xanchor="left",
            yanchor="top"
        )],
        sliders=sliders,
        scene=dict(
            xaxis=dict(title='Longitude', range=[x.min(), x.max()]),
            yaxis=dict(title='Latitude', range=[y.min(), y.max()]),
            zaxis=dict(title='Altitude', range=[z.min(), z.max()]),
        ),
        scene_camera=dict(eye=dict(x=2, y=2, z=2)),
        width=1000,
        height=800,
        margin=dict(r=20, l=20, b=20, t=20),
        legend=dict(
            x=0, 
            y=1, 
            traceorder='normal',
            orientation='h',
            xanchor='left', 
            yanchor='bottom'
        )
    )
    return fig
