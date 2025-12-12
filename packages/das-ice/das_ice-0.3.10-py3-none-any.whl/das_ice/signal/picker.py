import numpy as np

def sta_lta(da, sta_t, lta_t):
    '''
    Compute the Short-Term Average to Long-Term Average (STA/LTA) ratio for a DataArray.

    :param da: Input DataArray containing the signal data
    :type da: xr.DataArray
    :param sta_t: Time window for the short-term average (STA) in seconds
    :type sta_t: float
    :param lta_t: Time window for the long-term average (LTA) in seconds
    :type lta_t: float
    :return: DataArray containing the STA/LTA ratio
    :rtype: xr.DataArray
    '''
    
    # Compute the sampling frequency from the time coordinate
    freq = 1 / (np.int32(da.time[1] - da.time[0]) * 10**-9)
    
    # Compute STA/LTA ratio using rolling window averages
    sta_lta = (np.abs(da).rolling(time=int(sta_t * freq), center=True).mean()/
               np.abs(da).rolling(time=int(lta_t * freq), center=True).mean())
    
    return sta_lta

def find_event(sta_lta, on, off):
    '''
    Detect events based on the STA/LTA ratio exceeding given thresholds.

    :param sta_lta: Short-Term Average to Long-Term Average (STA/LTA) ratio
    :type sta_lta: xr.DataArray
    :param on: Threshold for the 'on' event (when STA/LTA exceeds this value)
    :type on: float
    :param off: Threshold for the 'off' event (when STA/LTA drops below this value)
    :type off: float
    :return: DataArray of event detections (1 for event, 0 for no event)
    :rtype: xr.DataArray
    '''
    
    # Detect when STA/LTA exceeds the 'on' threshold
    serie_on = sta_lta > on
    
    # Detect when STA/LTA drops below the 'off' threshold
    serie_off = sta_lta > off
    
    # XOR operation between 'on' and 'off' to detect transitions
    serie_onxoroff = serie_on ^ serie_off

    # Detect events based on conditions
    event = (serie_on & ~serie_onxoroff) | (serie_off & serie_onxoroff)
    
    return event