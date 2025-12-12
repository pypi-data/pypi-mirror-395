
import numpy as np
from matplotlib.patches import Ellipse

def surface_area_on_the_ellipsoid(fi1, fi2, lamda1, lamda2):
    """
    Compute the surface area on the WGS84 ellipsoid between two latitude and longitude bounds.

    The method follows the formulas in Savric et al. (2020), doi: 10.1111/tgis.12636.

    Parameters
    ----------
    fi1 : float
        Lower latitude in **degrees**.
    fi2 : float
        Upper latitude in **degrees**.
    lamda1 : float
        Lower longitude in **degrees**.
    lamda2 : float
        Upper longitude in **degrees**.

    Returns
    -------
    float
        Surface area in square kilometers (km²).

    Notes
    -----
    - The ellipsoid parameters correspond to **WGS84**:
      - Semi-major axis (a): 6378137.0 m
      - Semi-minor axis (b): 6356752.3142 m
      - First eccentricity (e): 0.081819190842622
    - Useful reference: https://www.jpz.se/Html_filer/wgs_84.html
    """
    fi1, fi2 = np.radians(fi1), np.radians(fi2)
    lamda1, lamda2 = np.radians(lamda1), np.radians(lamda2)
    e = 0.081819190842622
    a = 6378137.0
    b = 6356752.3142

    part1 = ((b**2)/2)*(lamda2-lamda1)
    part2 = (np.sin(fi2)/(1-((e**2)*((np.sin(fi2))**2))))+((1/(2*e))*np.log((1+(e*np.sin(fi2)))/(1-(e*np.sin(fi2)))))
    part3 = (np.sin(fi1)/(1-((e**2)*((np.sin(fi1))**2))))+((1/(2*e))*np.log((1+(e*np.sin(fi1)))/(1-(e*np.sin(fi1)))))
    return (part1*(part2-part3))*0.000001

def ellipse(cov, centre, nstd, **kwargs):
    """
    Compute the parameters of an ellipse given a covariance matrix.

    The ellipse is defined by its eigen-decomposition and scaled by a number
    of standard deviations. Optionally, a `matplotlib.patches.Ellipse` object
    is returned for direct plotting.

    Parameters
    ----------
    cov : ndarray of shape (2, 2)
        Covariance matrix.
    centre : tuple of float
        Coordinates (x, y) of the ellipse center.
    nstd : float
        The number of standard deviations to determine the ellipse radius.
    **kwargs : dict
        Additional keyword arguments passed to `matplotlib.patches.Ellipse`.

    Returns
    -------
    centre : tuple
        The center of the ellipse.
    size : list
        The `[width, height]` of the ellipse.
    angle : float
        The rotation angle of the ellipse in degrees.
    eccentricity : float
        The ellipse eccentricity.
    ellipse : matplotlib.patches.Ellipse
        The ellipse patch object, ready for plotting.
    """
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    vx, vy = eigvecs[:,0][0], eigvecs[:,0][1]
    theta = np.arctan2(vy, vx)

    width, height = 2 * nstd * np.sqrt(eigvals)
    angle = np.degrees(theta)
    
    if not (np.isfinite(width) and np.isfinite(height) and width > 0 and height > 0):
        return centre, [np.nan, np.nan], angle, None, None

    a = max(width, height) / 2
    b = min(width, height) / 2
    eccentricity = np.sqrt(1 - (b**2 / a**2))

    ellipse = Ellipse(xy=centre, width=width, height=height, angle=angle, **kwargs)
    return centre, [width, height], angle, eccentricity, ellipse
