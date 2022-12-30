"""
Various utilities for calculating mMandlebrot images.
"""

import logging

import numpy as np  # type: ignore

# Ignore numpy warnings from overflow in iterations.
# Needed as not checking for diverging point to speed things up.
# Test without ignoring errors then comment out.
np.seterr(all="ignore")

from mandlebrot.app_logging import setup_logging

log = logging.getLogger(__name__)

def complex_matrix(xmin: float, xmax: float, ymin: float, ymax: float, pixel_density: int) -> np.ndarray:
    """
    Constructs complex array of points for image.

    Args:
        xmin:           minimum x value (real)
        xmax:           maximum x value (real)
        ymin:           minimum y value (imaginary)
        ymax:           maximum y value (imaginary)
        pixel_density:  Number of pixels (points) in x and y ranges.

    Returns:
        Array of complex points making up image space.
    """
    # Construct real and imaginary arrays.
    re_part = np.linspace(xmin, xmax, int((xmax - xmin) * pixel_density))
    im_part = np.linspace(ymin, ymax, int((ymax - ymin) * pixel_density))

    # Construct and return arracy of complex points for image.
    return re_part[np.newaxis, :] + im_part[:, np.newaxis] * 1j


def get_members(c_pts: np.ndarray, num_iterations: int) -> np.ndarray:
    """
    Returns complex points that are stable, that is,
    don't diverge at maximum iterations.
    Args:
        c_pts:          Array of complex points in image.
        num_iterations: Number of iterations to check for divergence
    Retutns:
        Returns array of complex points that are stable.
    """
    mask = is_stable(c_pts, num_iterations)  # type: ignore[arg-type]
    return c_pts[mask]


def is_stable(c_pt: int, num_iterations: int) -> bool:
    """
    Checks if point is stable, i.e. reaches iteration limit
    without diverging.
    Args:
        c_pt:           Complex point (component) in image to test.
        num_iterations: Number of iterations to check for divergence.
    Returns:
        Returns true if not diverging at max iterations.
    """
    z_pt = 0
    for _ in range(num_iterations):
        z_pt = z_pt**2 + c_pt
    return abs(z_pt) <= 2
