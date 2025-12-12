"""Raw moments up to 2nd order of 3D points."""

from mt import tp, np, glm
import mt.base.casting as _bc

from ..geo import ThreeD
from ..geond import Moments, moments_from_pointlist, EPSILON
from .point_list import PointList3d


__all__ = ["Moments3d"]


class Moments3d(ThreeD, Moments):
    """Raw moments up to 2nd order of points living in 3D, implemnted in GLM.

    Overloaded operators are negation, multiplication with a scalar and true division with a scalar.

    Parameters
    ----------
    m0 : float
        0th-order raw moment
    m1 : glm.vec3
        1st-order raw moment
    m2 : glm.mat3 or numpy.ndarray
        2nd-order raw moment. If the input is numpy.ndarray, a row-major matrix is expected.
        Otherwise, a column-major matrix is expected.

    Attributes
    ----------
    m0 : float
        0th-order raw moment
    m1_glm : glm.vec3
        1st-order raw moment
    m1 : numpy.ndarray
        the numpy view of `m1_glm`
    m2_glm : glm.mat3
        2nd-order column-major raw moment
    m2 : numpy.ndarray
        the numpy view of `m2_glm`
    mean_glm : glm.vec3
        the mean of points
    mean : numpy.ndarray
        the numpy view of `mean_glm`
    cov_glm : glm.mat3
        the covariance matrix of points
    cov : numpy.ndarray
        the numpy view of `cov_glm`

    Examples
    --------
    >>> import numpy as np
    >>> from mt.geo3d.moments import Moments3d
    >>> gm.Moments3d(10, np.array([2,3,1]), np.array([[1,2,0],[3,4,0],[0,0,1]]))
    Moments3d(m0=10, mean=vec3( 0.2, 0.3, 0.1 ), cov=mat3x3(( 0.06, 0.24, -0.02 ), ( 0.14, 0.31, -0.03 ), ( -0.02, -0.03, 0.09 )))

    See Also
    --------
    Moments
        base class
    """

    def __init__(
        self,
        m0: float,
        m1: tp.Union[np.ndarray, glm.vec3],
        m2: tp.Union[np.ndarray, glm.mat3],
    ):
        self._m0 = m0
        self._m1 = glm.vec3(m1)
        if isinstance(m2, np.ndarray):
            self._m2 = glm.mat3(
                glm.vec3(m2[:, 0]), glm.vec3(m2[:, 1]), glm.vec3(m2[:, 2])
            )
        else:
            self._m2 = glm.mat3(m2)
        self._mean = None
        self._cov = None

    @property
    def m1_glm(self):
        return self._m1

    @property
    def m1(self):
        return np.frombuffer(self._m1.to_bytes(), dtype=np.float32)

    @property
    def m2_glm(self):
        return self._m2

    @property
    def m2(self):
        return np.frombuffer(self._m2.to_bytes(), dtype=np.float32).reshape(3, 3).T

    @property
    def mean_glm(self):
        """Returns the mean vector as a vec3."""
        if self._mean is None:
            self._mean = (
                glm.vec3() if glm.abs(self._m0) < EPSILON else self._m1 / self._m0
            )
        return self._mean

    @property
    def mean(self):
        """Returns the mean vector."""
        return np.frombuffer(self.mean_glm.to_bytes(), dtype=np.float32)

    @property
    def cov_glm(self):
        """Returns the column-major covariance matrix as a mat3."""
        if self._cov is None:
            mean = self.mean_glm
            self._cov = (
                glm.mat3()
                if glm.abs(self._m0) < EPSILON
                else (self._m2 / self._m0) - glm.outerProduct(mean, mean)
            )
        return self._cov

    @property
    def cov(self):
        """Returns the row-major covariance matrix as a numpy array."""
        return np.frombuffer(self.cov_glm.to_bytes(), dtype=np.float32).reshape(3, 3).T

    def __repr__(self):
        return "Moments3d(m0={}, mean={}, cov={})".format(
            self.m0, repr(self.mean_glm), repr(self.cov_glm)
        )


_bc.register_cast(Moments3d, Moments, lambda x: Moments(x.m0, x.m1, x.m2))
_bc.register_cast(Moments, Moments3d, lambda x: Moments3d(x.m0, x.m1, x.m2))
_bc.register_castable(Moments, Moments3d, lambda x: x.ndim == 3)


_bc.register_cast(PointList3d, Moments3d, moments_from_pointlist)
