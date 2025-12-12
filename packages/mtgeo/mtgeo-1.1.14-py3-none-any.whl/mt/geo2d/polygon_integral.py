'''Polygon in 2D.

A polygon is represented as a collection of 2D points in either clockwise or counter-clockwise order. It is stored in a numpy array of shape (N,2).
'''

import mt.base.casting as _bc

from .moments import Moments2d
from .polygon import Polygon


__all__ = ['trapezium_integral', 'signed_area', 'moment_x', 'moment_y', 'moment_xy', 'moment_xx', 'moment_yy', 'to_moments2d']


def trapezium_integral(poly, func):
    '''Applies the Shoelace algorithm to integrate a function over the interior of a polygon. Shoelace algorithm views the polygon as a sum of trapeziums.

    Parameters
    ----------
    poly : Polygon
        a polygon
    func : function
        a function that takes x1, y1, x2, y2 as input and returns a scalar

    Returns
    -------
    scalar
        the integral over the polygon's interior

    Notes
    -----
    We use OpenGL's convention here. x-axis points to the right side and y-axis points upward

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import trapezium_integral
    >>> from mt.geo2d.polygon import Polygon
    >>> poly = Polygon([[1,2]])
    >>> trapezium_integral(poly, None)
    0
    >>> poly = Polygon([[20,10],[30,20]])
    >>> trapezium_integral(poly, None)
    0
    >>> poly = Polygon([[1,1],[0,0],[1,0]])
    >>> trapezium_integral(poly, lambda x1, y1, x2, y2: x1*y2-x2*y1)
    1

    References
    ----------
    .. [1] Pham et al. Fast Polygonal Integration and Its Application in Extending Haar-like Features To Improve Object Detection. CVPR, 2010.
    .. [2] exterior algebra
    '''
    retval = 0
    poly = poly.points
    N = len(poly)
    if N <= 2:
        return 0
    for i in range(N):
        z1 = poly[i]
        z2 = poly[(i+1)%N]
        retval += func(z1[0], z1[1], z2[0], z2[1])
    return retval

def signed_area(poly):
    '''Returns the signed area of a polygon.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the signed area over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import signed_area
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[10,10],[20,10],[20,20]])
    >>> round(signed_area(poly), 3)
    -50.0
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 0.5*(x2-x1)*(y1+y2))


def moment_x(poly):
    '''Returns the integral of x over the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the moment `int(x, dx, dy)` over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import moment_x
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,4],[2,3],[3,2]])
    >>> round(moment_x(poly), 3)
    -2.667
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 1/6*(x2-x1)*(x1*(y1*2+y2) + x2*(y1+y2*2)))

def moment_y(poly):
    '''Returns the integral of y over the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the moment `int(y, dx, dy)` over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import moment_y
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,3],[2,2],[3,1]])
    >>> round(moment_y(poly), 3)
    -2.0
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 1/6*(x2-x1)*(y1*y1 + y1*y2 + y2*y2))

def moment_xy(poly):
    '''Returns the integral of x*y over the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the moment `int(x*y, dx, dy)` over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import moment_xy
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,3],[2,2],[3,1]])
    >>> round(moment_xy(poly), 3)
    -5.333
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 1/24*(x2-x1)*(y1*y1*(x1*3+x2) + y1*y2*2*(x1+x2) + y2*y2*(x1+x2*3)))

def moment_xx(poly):
    '''Returns the integral of x*x over the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the moment `int(x*x, dx, dy)` over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import moment_xx
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,3],[2,2],[3,1]])
    >>> round(moment_xx(poly), 3)
    -7.167
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 1/12*(x2-x1)*(x1*x1*(y1*3+y2) + x1*x2*2*(y1+y2) + x2*x2*(y1+y2*3)))

def moment_yy(poly):
    '''Returns the integral of y*y over the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    scalar
        the moment `int(y*y, dx, dy)` over the polygon's interior

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import moment_yy
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,3],[2,2],[3,1]])
    >>> round(moment_yy(poly), 3)
    -4.167
    '''
    return trapezium_integral(poly, lambda x1, y1, x2, y2: 1/12*(x2-x1)*(y1+y2)*(y1*y1+y2*y2))


def to_moments2d(poly):
    '''Computes all moments, up to 2nd-order of the polygon's interior.

    Parameters
    ----------
    poly : Polygon
        a polygon

    Returns
    -------
    Momens2d
        th ecollection of moments up to 2nd order

    Examples
    --------
    >>> from mt.geo2d.polygon_integral import to_moments2d
    >>> import mt.geo2d.polygon as mp
    >>> poly = mp.Polygon([[3,3],[2,2],[3,1]])
    >>> m = to_moments2d(poly)
    >>> round(m.m0, 3)
    -1.0
    >>> round(m.m1.sum(), 3)
    -4.667
    >>> round(m.m2.sum(), 3)
    -22.0
    >>> round(m.mean.sum(), 3)
    4.667
    >>> round(m.cov.sum(), 3)
    -22.444
    '''
    m0 = signed_area(poly)
    m1 = [moment_x(poly), moment_y(poly)]
    mxy = moment_xy(poly)
    m2 = [[moment_xx(poly), mxy], [mxy, moment_yy(poly)]]
    return Moments2d(m0, m1, m2)
_bc.register_cast(Polygon, Moments2d, to_moments2d)
