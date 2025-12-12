'''Utilities for converting a rectangle into an octagon bounded by it.'''

from mt import np


__all__ = ['ISQRT2', 'approx_oct']


ISQRT2 = 1/np.sqrt(2)

# octagon to approximate a circle originating at (0,0) with radius 1
std_oct = np.array([
    (1,       0),
    (ISQRT2,  ISQRT2),
    (0,       1),
    (-ISQRT2, ISQRT2),
    (-1,      0),
    (-ISQRT2, -ISQRT2),
    (0,      -1),
    (ISQRT2, -ISQRT2),
])


def approx_oct(min_x, min_y, max_x, max_y):
    '''Converts a rectangle into an octagon inside it.

    Parameters
    ----------
    min_x : float
        min x-coordinate
    min_y : float
        min y-coordinate
    max_x : float
        max x-coordinate
    max_y : float
        max y-coordinate

    Returns
    -------
    polygon : numpy array
        list of 2D (x,y) points representing an octagon inside the rectangle (min_x, min_y, max_x, max_y)
    '''
    c = np.array([min_x + max_x, min_y + max_y])*0.5
    r = np.array([max_x, max_y]) - c
    return std_oct*r + c
