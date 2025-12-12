"""Affine transformation in ND."""

from mt import np
from mt.base import logger
from mt.base.deprecated import deprecated_func

from ..geo import (
    GeometricObject,
    LieTransformer,
    transform,
    register_transform,
    register_transformable,
)
from .point_list import PointList
from .moments import Moments


__all__ = ["Aff", "transform_Aff_on_Moments", "transform_Aff_on_PointList"]


class Aff(LieTransformer, GeometricObject):
    """A transformer to perform affine transformations using the same transformation matrix in n-dim space.

    Examples
    --------
    >>> from mt import np, geond as gn
    >>> a = gn.Aff(weight=np.array([[1,-1],[-2,3]]), bias=np.array([3,4]))
    >>> a.bias
    array([3, 4])
    >>> a.weight
    array([[ 1, -1],
           [-2,  3]])
    >>> a.matrix
    array([[ 1., -1.,  3.],
           [-2.,  3.,  4.],
           [ 0.,  0.,  1.]])
    >>> ~a
    Aff(weight_diagonal=[3. 1.], bias=[-13. -10.])
    >>> a*~a
    Aff(weight_diagonal=[1. 1.], bias=[0. 0.])
    >>> ~a*a
    Aff(weight_diagonal=[1. 1.], bias=[0. 0.])
    >>> a/a
    Aff(weight_diagonal=[1. 1.], bias=[0. 0.])
    >>> a%a
    Aff(weight_diagonal=[1. 1.], bias=[0. 0.])
    >>> a*a
    Aff(weight_diagonal=[ 3 11], bias=[ 2 10])
    >>> a*a*a
    Aff(weight_diagonal=[11 41], bias=[-5 30])
    >>> (a*a)*a
    Aff(weight_diagonal=[11 41], bias=[-5 30])
    >>> a*(a*a)
    Aff(weight_diagonal=[11 41], bias=[-5 30])
    >>> b = gn.Aff(weight=np.array([[1,-1],[-3,2]]), bias=np.array([2,1]))
    >>> a*b
    Aff(weight_diagonal=[4 8], bias=[4 3])
    >>> b*a
    Aff(weight_diagonal=[3 9], bias=[1 0])
    >>> a.conjugate(b)
    Aff(weight_diagonal=[ 6. -3.], bias=[-18.  66.])
    """

    # ----- base adaptation -----

    @property
    def ndim(self):
        return self.dim

    def invert(self):
        """Lie inverse"""
        invWeight = np.linalg.inv(
            self.weight
        )  # slow, and assuming weight matrix is invertible
        return Aff(invWeight, np.dot(invWeight, -self.bias))

    def multiply(self, other):
        """a*b = Lie operator"""
        if not isinstance(other, Aff):
            raise ValueError(
                "Expecting 'other' to be an affine transformation, but {} received.".format(
                    other.__class__
                )
            )
        return Aff(np.dot(self.weight, other.weight), self << other.bias)

    # ----- data encapsulation -----

    @property
    def bias(self):
        """The bias component of the affine transformation matrix."""
        return self.__bias

    @bias.setter
    def bias(self, bias):
        if len(bias.shape) != 1:
            raise ValueError("Bias is not a vector, shape {}.".format(bias.shape))
        self.__bias = bias

    @property
    def weight(self):
        """The weight/linear component of the affine transformation matrix."""
        return self.__weight

    @weight.setter
    def weight(self, weight):
        if len(weight.shape) != 2:
            raise ValueError("bias has non-matrix shape {}.".format(weight.shape))
        self.__weight = weight

    # ----- derived properties -----

    @property
    def bias_dim(self):
        """Returns the dimension of the bias vector."""
        return self.bias.shape[0]

    @property
    def weight_shape(self):
        """Returns the shape of the weight matrix."""
        return self.weight.shape

    @property
    def dim(self):
        """Returns the dimension of the transformation."""
        val = self.bias_dim
        if self.weight_shape != (val, val):
            raise ValueError(
                f"Weight {self.weight.shape} does not have a square matrix shape {(val, val)}."
            )
        return val

    @property
    def matrix(self):
        """Returns the transformation matrix."""
        dim = self.dim
        a = np.empty((dim + 1, dim + 1))
        a[:dim, :dim] = self.weight
        a[:dim, dim] = self.bias
        a[dim, :dim] = 0
        a[dim, dim] = 1
        return a

    @property
    def det(self):
        """Returns the determinant of the transformation matrix."""
        return np.linalg.det(self.weight)  # slow method

    # ----- methods -----

    def __init__(self, weight=np.identity(3), bias=np.zeros(3), check_shapes=True):
        self.weight = weight
        self.bias = bias
        if check_shapes:
            _ = self.dim  # just to check shapes

    def __repr__(self):
        return "Aff(weight_diagonal={}, bias={})".format(
            self.weight.diagonal(), self.bias
        )


# ----- transform functions -----


def transform_Aff_on_Moments(aff_tfm, moments):
    """Transform the Moments using an affine transformation.

    Parameters
    ----------
    aff_tfm : Aff
        general affine transformation
    moments : Moments
        general moments

    Returns
    -------
    Moments
        affined-transformed moments
    """
    A = aff_tfm.weight
    old_m0 = moments.m0
    old_mean = moments.mean
    old_cov = moments.cov
    new_mean = A @ old_mean + aff_tfm.bias
    new_cov = A @ old_cov @ A.T
    new_m0 = old_m0 * abs(aff_tfm.det)
    new_m1 = new_m0 * new_mean
    new_m2 = new_m0 * (np.outer(new_mean, new_mean) + new_cov)
    return Moments(new_m0, new_m1, new_m2)


register_transform(Aff, Moments, transform_Aff_on_Moments)


def transform_Aff_on_ndarray(aff_tfm, point_array):
    """Transform an array of points using an affine transformation.

    Parameters
    ----------
    aff_tfm : Aff
        general affine transformation
    point_array : numpy.ndarray with last dimension having the same length as the dimensionality of the transformation
        a point array

    Returns
    -------
    numpy.ndarray
        affine-transformed point array
    """
    return point_array @ aff_tfm.weight.T + aff_tfm.bias


register_transform(Aff, np.ndarray, transform_Aff_on_ndarray)
register_transformable(Aff, np.ndarray, lambda x, y: x.ndim == y.shape[-1])


def transform_Aff_on_PointList(aff_tfm, point_list):
    """Transform a point list using an affine transformation.

    Parameters
    ----------
    aff_tfm : Aff
        general affine transformation
    point_list : PointList
        a point list

    Returns
    -------
    PointList
        affine-transformed point list
    """
    return PointList(point_list.points @ aff_tfm.weight.T + aff_tfm.bias, check=False)


register_transform(Aff, PointList, transform_Aff_on_PointList)
