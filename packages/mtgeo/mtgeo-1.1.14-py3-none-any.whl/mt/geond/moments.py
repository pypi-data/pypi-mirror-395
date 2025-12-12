"""Raw moments up to 2nd order of ND points."""

from mt import np
import sys as _sys

import mt.base.casting as _bc

from ..geo import GeometricObject
from .point_list import PointList


__all__ = ["EPSILON", "Moments", "moments_from_pointlist"]


EPSILON = np.sqrt(_sys.float_info.epsilon)


class Moments(GeometricObject):
    """Raw moments up to 2nd order of points living in the same Euclidean space.

    Overloaded operators are negation, multiplication with a scalar and true division with a scalar.

    Parameters
    ----------
    m0 : scalar
        0th-order raw moment
    m1 : numpy 1d array of length D, where D is the `ndim` of the class
        1st-order raw moment
    m2 : numpy DxD matrix
        2nd-order raw moment

    Examples
    --------
    >>> import mt.geo2d.polygon as gp
    >>> poly = gp.Polygon([[0,0],[0,1],[1,2],[1,0]])
    >>> import mt.geond.moments as gm
    >>> from mt.base.casting import cast
    >>> m = cast(poly, gm.Moments2d)
    >>> m.m0
    4.0
    >>> m.m1
    array([2, 3])
    >>> m.m2
    array([[2, 2],
           [2, 5]])
    >>> m.mean
    array([0.5 , 0.75])
    >>> m.cov
    array([[0.25  , 0.125 ],
           [0.125 , 0.6875]])
    """

    def __init__(self, m0, m1, m2):
        self._m0 = np.float(m0)
        self._m1 = np.array(m1)
        self._m2 = np.array(m2)
        self._mean = None
        self._cov = None

    def __repr__(self):
        return "Moments(ndim={}, m0={}, mean={})".format(self.ndim, self.m0, self.mean)

    @property
    def m0(self):
        """0th-order moment"""
        return self._m0

    @property
    def m1(self):
        """1st-order moment"""
        return self._m1

    @property
    def m2(self):
        """2nd-order moment"""
        return self._m2

    @property
    def mean(self):
        """Returns the mean vector."""
        if self._mean is None:
            self._mean = (
                np.zeros(self.ndim) if abs(self.m0) < EPSILON else self.m1 / self.m0
            )
        return self._mean

    @property
    def cov(self):
        """Returns the covariance matrix."""
        if self._cov is None:
            self._cov = (
                np.eye(self.ndim)
                if abs(self.m0) < EPSILON
                else (self.m2 / self.m0) - np.outer(self.mean, self.mean)
            )
        return self._cov

    # ----- operators -----

    @property
    def ndim(self):
        return len(self.m1)

    def __neg__(self):
        """Returns a new instance where all the moments are negated."""
        return type(self)(-self.m0, -self.m1, -self.m2)

    def __mul__(self, scalar):
        """Returns a new instance where all the moments are multiplied by a scalar."""
        return type(self)(self.m0 * scalar, self.m1 * scalar, self.m2 * scalar)

    def __truediv__(self, scalar):
        """Returns a new instance where all the moments are divided by a scalar."""
        return type(self)(self.m0 / scalar, self.m1 / scalar, self.m2 / scalar)


def moments_from_pointlist(pl):
    """Constructs a Moments object from a list of points.

    Parameters
    ----------
    pl : PointList
        list of points from which the moments are computed

    Returns
    -------
    Moments, Moments2d or Moments3d
        raw moments of the point list, depending on the value of `ndim` provided
    """
    arr = pl.points
    m0 = len(arr)
    m1 = arr.sum(axis=0)
    m2 = np.dot(arr.T, arr)
    if arr.shape[1] == 2:
        return Moments2d(m0, m1, m2)
    if arr.shape[1] == 3:
        return Moments3d(m0, m1, m2)
    return Moments(m0, m1, m2)


_bc.register_cast(PointList, Moments, moments_from_pointlist)
