#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-08-31
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : imgLP
# Module        : drift

"""
This function calculates the drift between two close images.
"""



# %% Libraries
import numpy as np
from imglp import crosscorrelate
from arrlp import correlate



# %% Function
def drift(image, image2, /, drift_max=None, *, do_hp=True, do_contrast_norm=False, fact=1, xp=np) :
    '''
    This function calculates the drift between two close images.
    
    Parameters
    ----------
    image : numpy.ndarray or cupy.ndarray
        first image to use.
    image2 : numpy.ndarray or cupy.ndarray
        second image to use.
    drift_max : float
        maximum drift in pixels.
    do_hp : bool
        True to apply high-pass filtering on images to avoid calculating drift on background
    do_contrast_norm : bool
        True to apply a contrast normalization making each local pic the same intensity
    fact : float
        factor to apply to change maximum drift.
    xp : numpy or cupy
        if cupy will calculate on GPU
    

    Returns
    -------
    dx : float
        drift in x : x1 = x0 + dx [pix].
    dy : float
        drift in y : y1 = y0 + dy [pix].

    Examples
    --------
    >>> from imglp import drift
    ...
    >>> dx, dy = drift(img1, img2) # TODO
    '''

    # Getting crop shape
    if drift_max is not None :
        drift_max = int(round(drift_max))
        drift_max = drift_max * fact
        cs = drift_max * 2 + 1
        shape = min(image.shape)
        shape = shape if shape%2==1 else shape-1
        cs = cs if cs < shape else shape
        cropshape = (cs, cs)
    else :
        cropshape = None

    # High pass filtering
    if do_hp :
        image = correlate(image, sigma=1) -  correlate(image, sigma=3)
        image2 = correlate(image2, sigma=1) -  correlate(image2, sigma=3)

    # Contrast normalization : locally all pics have same amplitude
    if do_contrast_norm :
        bg = correlate(image, sigma=5) # local background estimate (blur)
        sq = correlate(image**2, sigma=5) # local contrast (std) approx by sqrt( local variance )
        local_var = np.maximum(0.0, sq - bg**2)
        local_std = np.sqrt(local_var)
        local_std = np.maximum(local_std, 1e-6) # Avoid divide-by-zero
        image = (image - bg) / local_std
        bg = correlate(image2, sigma=5) # local background estimate (blur)
        sq = correlate(image2**2, sigma=5) # local contrast (std) approx by sqrt( local variance )
        local_var = np.maximum(0.0, sq - bg**2)
        local_std = np.sqrt(local_var)
        local_std = np.maximum(local_std, 1e-6) # Avoid divide-by-zero
        image2 = (image2 - bg) / local_std

    # Normalization
    image -= image.mean()
    image2 -= image2.mean()

    # Calculating crosscorrelation
    cc = crosscorrelate(image, image2, cropshape=cropshape, xp=xp)

    # Find integer peak
    iy, ix = xp.unravel_index(int(xp.argmax(cc)), cc.shape)

    # Ensure we are not on the border
    if not (0 < iy < cc.shape[0] - 1 and 0 < ix < cc.shape[1] - 1):
        raise ValueError('Drift CC peak is on border, probably drift_max is not big enough.')

    # Extract 3x3 neighborhood around the peak
    win = cc[iy-1:iy+2, ix-1:ix+2].astype(float)

    # Fit 2D quadratic to neighborhood
    dy_sub, dx_sub = subpixel_peak_2d(win)

    # Convert peak position to shift
    dy = (iy - cc.shape[0] // 2) + dy_sub
    dx = (ix - cc.shape[1] // 2) + dx_sub

    return dx, dy, cc



def subpixel_peak_2d(win):

    # Coordinates relative to center
    y, x = np.mgrid[-1:2, -1:2]

    # Flatten
    X = np.column_stack([
        x.ravel()**2,
        y.ravel()**2,
        x.ravel()*y.ravel(),
        x.ravel(),
        y.ravel(),
        np.ones(9)
    ])
    Z = win.ravel()

    # Solve least squares for coefficients
    coeffs, _, _, _ = np.linalg.lstsq(X, Z, rcond=None)
    a, b, c, d, e, f = coeffs

    # Solve for stationary point of quadratic surface
    A = np.array([[2*a, c],
                  [c,   2*b]])
    bvec = -np.array([d, e])

    try:
        offset = np.linalg.solve(A, bvec)
    except np.linalg.LinAlgError:
        offset = np.array([0.0, 0.0])  # fallback if singular

    dx_sub, dy_sub = offset
    return dy_sub, dx_sub


# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)