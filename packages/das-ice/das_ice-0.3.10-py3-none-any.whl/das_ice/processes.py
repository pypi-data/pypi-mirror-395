import xarray as xr
import numpy as np
import scipy

def std_local(da,nt=6,nx=4,ax_t='time',ax_x='distance'):
    '''
    Compute local standard deviation for a DataArray

    :param da: Variable on which compute the local standard deviation
    :type da: xr.DataArray
    :param nt: number of element in ax_t direction (default: 6)
    :type nt: int
    :param nx: number of element in ax_x direction (default: 4)
    :type nx: int
    :param ax_t: ax_t axis (default: 'time')
    :type ax_t: string
    :param ax_x: ax_x axis (default: 'distance')
    :type ax_x: string
    '''

    return da.rolling({ax_t:nt,ax_x:nx}).std(ax_t)

def strain_rate(da,ax_d='distance'):
    '''
    Compute strain rate from velocity mesurement

    :param da: Variable on which compute differentiate
    :type da: xr.DataArray
    :param ax_d: axis for differentiate (default: 'distance')
    :type ax_d: string
    '''

    return da.differentiate(ax_d)

def local_spectrogram(da,win,t_start,dB=True,**kwargs):
    '''
     Wrapper of `scipy.signal.welch` to performed PSD spectrogram
    :param self:
    :type self: xr.DataArray
    :param win: time length in seconds
    :type win: int
    :param t_start: data for the start
    :type t_start: str
    :param dB: value in dB
    :type dB: bool
    '''
    fs=1/(np.float64((da.time[1]-da.time[0]))*10**-9)
    # Sub data selection
    da_sel=da.sel(time=slice(t_start,None))
    # Find the number of win interval in the time serie
    nb_per=int(len(da_sel)/(win*fs))
    # select the right time length for the spectrogram
    da_sel=da_sel[0:np.int32(win*fs)*nb_per]

    freq,psd=scipy.signal.welch(da_sel.values.reshape(nb_per,int(win*fs)),fs,**kwargs)

    # Covert in dB
    if dB:
        psd=10*np.log10(psd)

    da_psd=xr.DataArray(np.transpose(psd),dims=['freq','time'])
    da_psd['freq']=freq

    tr_time=da_sel.time.values.reshape(nb_per,int(win*fs))
    da_psd['time']=tr_time[:,0]

    return da_psd