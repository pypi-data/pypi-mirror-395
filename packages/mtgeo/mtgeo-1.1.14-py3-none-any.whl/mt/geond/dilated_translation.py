import math

from mt import np
import mt.base.casting as _bc
from ..geo import register_approx, register_transform, register_transformable
from .dilated_isometry import Dliso
from .dilatation import Dlt


__all__ = ["Dliso", "approx_Dliso_to_Dltra", "approx_Dlt_to_Dltra"]


class Dltra(Dliso):
    """Dilated translation = Translation following a uniform scaling.

    A dilated translation can be seen as both a dilatation and a dilated isometry.

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not true but cheeky
       MT is trying to advertise his paper!)
    """

    # ----- base adaptation -----

    @property
    def dim(self):
        """Returns the dimension of the transformation."""
        return self.offset.shape[0]

    @property
    def unitary(self):
        """The unitary matrix of the dilated translation."""
        return np.identity(self.ndim)  # returns identity

    @unitary.setter
    def unitary(self, unitary):
        raise TypeError("Unitary matrix is the identity matrix and is read-only.")

    # ----- derived properties -----

    @property
    def linear(self):
        """Returns the linear part of the affine transformation matrix of the dilated translation."""
        return np.identity(self.ndim) * self.scale

    # ----- methods -----

    def __init__(self, offset=np.zeros(2), scale=1):
        self.offset = offset
        self.scale = scale

    def __repr__(self):
        return "Dltra(offset={}, scale={})".format(self.offset, self.scale)

    # ----- base adaptation -----

    def multiply(self, other):
        if not isinstance(other, Dltra):
            return super(Dltra, self).multiply(other)
        return Dltra(self << other.offset, self.scale * other.scale)

    multiply.__doc__ = Dliso.multiply.__doc__

    def invert(self):
        invScale = 1 / self.scale
        return Dliso(self.offset * (-invScale), invScale)

    invert.__doc__ = Dliso.invert.__doc__

    # ----- matrix exponential -----

    def logm(self) -> tuple:
        """Returns the matrix logarithm of the transformation matrix.

        Returns
        -------
        u : float
            the linear part of the matrix logarithm in the form of a single scalar
        v : np.ndarray
            the translation part of the matrix logarithm in the form of a vector
        """
        if self.scale == 1:  # special case, deform to translation only
            return 0, self.offset
        u = math.log(self.scale)
        v = (u / (self.scale - 1)) * self.offset
        return u, v

    @classmethod
    def expm(cls, u: float, v: np.ndarray):
        """Returns the matrix exponential of a matrix living in the Lie algebra of Dltra.

        Returns
        -------
        u : float
            the linear part of the matrix in the form of a single scalar
        v : np.ndarray
            the translation part of the matrix in the form of a vector
        """
        if u == 0:  # special case, deform to translation only
            return Dltra(offset=v)  # scale == 1
        s = math.exp(u)
        t = ((s - 1) / u) * v
        return Dltra(offset=t, scale=s)

    def pow(self, k: float):
        """Raises the Dltra to a scalar power."""
        u, v = self.logm()
        return Dltra.expm(u * k, v * k)


# ----- casting -----


_bc.register_cast(Dltra, Dliso, lambda x: Dliso(offset=x.offset, scale=x.scale))
_bc.register_cast(
    Dltra,
    Dlt,
    lambda x: Dlt(offset=x.offset, scale=np.diag(x.scale), check_shapes=False),
)


# ----- approximation ------


def approx_Dliso_to_Dltra(obj):
    """Approximates an Dliso instance with a Dltra by ignoring the unitary part."""
    return Dltra(offset=obj.offset, scale=obj.scale)


register_approx(Dliso, Dltra, approx_Dliso_to_Dltra)


def approx_Dlt_to_Dltra(dlt):
    """Approximates a Dlt instance with a Dltra.

    We approximate the scale components with their arithmetic mean in this case for efficiency and numerical stability, breaking theoretical concerns. So use this function with care.

    Parameters
    ----------
    dlt : Dlt
        a dilatation

    Returns
    -------
    Dltra
        a dilated translation
    """
    return Dltra(offset=dlt.offset, scale=dlt.scale.mean())


register_approx(Dlt, Dltra, approx_Dlt_to_Dltra)


# ----- transform functions ------


def transform_Dltra_on_ndarray(dlt_tfm, point_array):
    """Transform an array of points using a dilated transalation.

    Parameters
    ----------
    dlt_tfm : Dltra
        a dilated translation
    point_array : numpy.ndarray with last dimension having the same length as the dimensionality of the transformation
        a point array

    Returns
    -------
    numpy.ndarray
        dilated-translated point array
    """
    return point_array * dlt_tfm.scale + dlt_tfm.bias


register_transform(Dltra, np.ndarray, transform_Dltra_on_ndarray)
register_transformable(Dltra, np.ndarray, lambda x, y: x.ndim == y.shape[-1])
