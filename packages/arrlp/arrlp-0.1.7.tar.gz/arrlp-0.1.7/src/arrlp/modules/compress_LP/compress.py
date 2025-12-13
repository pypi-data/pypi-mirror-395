#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-30
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : arrLP
# Module        : compress

"""
Compresses an array between values by normalizing, with possibility to saturate extrema.
"""



# %% Libraries
import numpy as np



# %% Function
def compress(array, /, max=1, min=0, *, dtype=None, white=None, black=None, white_percent=None, black_percent=None, saturate=None) :
    '''
    Compresses an array between values by normalizing, with possibility to saturate extrema.
    
    Parameters
    ----------
    array : np.ndarray
        Array to normalize.
    max : int or float or None
        white value in output. None for no changing of white
    min : int or float or None
        black value in output. None for no changing of black
    dtype : np.dtype or str or None
        dtype of output, None for same as input
    white : int or float or None
        white value in input. None for maximum
    black : int or float or None
        black value in input. None for minimum
    white_percent : int or None
        white percentage distribution in input if white is None.
    black_percent : int or None
        black percentage distribution in input if black is None.
    saturate : Any or bool or None
        If True, will saturate values above white and black. If Any, will replace by this value. If None no saturation.

    Returns
    -------
    array : np.ndarray
        Normalized and saturated copy of array.

    Examples
    --------
    >>> from arrlp import compress
    >>> array = np.arange(100, dtype=np.float32)
    ...
    >>> compress(array, 10, 5) # compresses array between 10 and 5
    >>> compress(array, white=50, black=40) # compresses array linearly so that 50 value is at 1 and 40 is at 0
    >>> compress(array, white=50, black=40, saturate=np.nan) # compresses array linearly so that 50 value is at 1 and 40 is at 0, replace outside values by np.nan
    >>> compress(array, white_percent=10, black=1) # compresses array linearly so that 10% of array will be white, and 1% black (without saturation)
    >>> compress(array, white_percent=10, black=1, saturate=True) # compresses array linearly so that 10% of array will be white, and 1% black (with saturation)
    '''

    # init
    array = np.asarray(array)
    if dtype is None :
        dtype = array.dtype

    # Get white/black
    if white is None :
        white = np.nanmax(array) if white_percent is None else np.nanpercentile(array, 100-white_percent)
    if black is None :
        black = np.nanmin(array) if black_percent is None else np.nanpercentile(array, black_percent)
    if white >= black :
        raise ValueError('white >= black is not possible while compressing')

    # Normalization
    if max is not None and min is not None and min >= max :
        raise ValueError('min >= max is not possible while compressing')
    if max is not None :
        array = normalization(array, value=max, norm=white, fix=black)
        white = max
    if min is not None :
        array = normalization(array, value=min, norm=black, fix=white)
        black = min
    if max is None and min is None :
        array = np.copy(array)

    # Saturation
    if saturate is not None :
        if saturate is True :
            sat_min, sat_max = min, max
        else :
            sat_min, sat_max = saturate, saturate
        array[array>max] = sat_max
        array[array<min] = sat_min
    
    return array.astype(dtype)



def normalization(array, /, value:float=None, norm:float=None, fix:float=None):
    '''Basic normalization process of array copy while keeping a fixed point'''

    if fix is None : fix = 0
    if norm is None : norm = max(np.nanmax(array),-np.nanmin(array))
    if value is None : value = 1*np.sign(norm)
    return (array-fix)/(norm-fix)*(value-fix) + fix



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)