"""Affine transformation in 3D."""

from mt import tp, np, glm
import mt.base.casting as _bc

from ..geo import ThreeD, register_transform, register_transformable
from ..geond import Aff
from .moments import Moments3d
from .point_list import PointList3d


__all__ = [
    "Aff3d",
    "transform_Aff3d_on_Moments3d",
    "transform_Aff3d_on_PointList3d",
    "rot3d_x",
    "rot3d_y",
    "rot3d_z",
]


class Aff3d(ThreeD, Aff):
    """Affine transformation in 3D.

    The 3D affine transformation defined here consists of a linear/weight part and an offset/bias
    part.

    Attributes
    ----------
    offset : glm.vec3
        the bias vector
    bias : numpy.ndarray
        the numpy view of `offset`
    linear : glm.mat3
        the weight matrix
    weight : numpy.ndarray
        the numpy view of `linear`

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not really, cheeky MT is trying to advertise his paper!)
    """

    # ----- static methods -----

    @staticmethod
    def from_matrix(mat: np.ndarray):
        """Obtains an Aff3d instance from a non-singular affine transformation matrix.

        Parameters
        ----------
        mat : a 3x3 array
            a non-singular affine transformation matrix

        Returns
        -------
        Aff3d
            An instance representing the transformation

        Notes
        -----
        For speed reasons, no checking is involved.
        """
        return Aff3d(offset=mat[:3, 3], linear=mat[:3, :3])

    # ----- base adaptation -----

    @property
    def ndim(self):  # reimplementation to enforce constantness
        return 3

    def multiply(self, other):
        if not isinstance(other, Aff3d):
            return super(Aff3d, self).multiply(other)
        return Aff3d(
            offset=self.linear * other.offset + self.offset,
            linear=self.linear * other.linear,
        )

    multiply.__doc__ = Aff.multiply.__doc__

    def invert(self):
        invLinear = glm.inverse(self.linear)
        invOffset = invLinear * (-self.offset)
        return Aff3d(offset=invOffset, linear=invLinear)

    invert.__doc__ = Aff.invert.__doc__

    @property
    def bias(self):
        return np.frombuffer(self.__offset.to_bytes(), dtype=np.float32)

    bias.__doc__ = Aff.bias.__doc__

    @bias.setter
    def bias(self, bias):
        raise TypeError("Bias vector is read-only. Use self.offset vector instead.")

    @property
    def bias_dim(self):
        return 3

    bias_dim.__doc__ = Aff.bias_dim.__doc__

    @property
    def weight(self):
        return np.frombuffer(self.__linear.to_bytes(), dtype=np.float32).reshape(3, 3).T

    weight.__doc__ = Aff.weight.__doc__

    @weight.setter
    def weight(self, weight):
        raise TypeError("Weight matrix is read-only. Use self.linear instead.")

    @property
    def weight_shape(self):
        return (3, 3)

    weight_shape.__doc__ = Aff.weight_shape.__doc__

    # ----- data encapsulation -----

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, value: tp.Union[np.ndarray, glm.vec3]):
        self.__offset = glm.vec3(value)

    @property
    def linear(self):
        return self.__linear

    @linear.setter
    def linear(self, value: tp.Union[np.ndarray, glm.mat3]):
        if isinstance(value, np.ndarray):
            self.__linear = glm.mat3(
                glm.vec3(value[:, 0]), glm.vec3(value[:, 1]), glm.vec3(value[:, 2])
            )
        else:
            self.__linear = glm.mat3(value)

    # ----- derived properties -----

    @property
    def affine(self):
        return glm.mat4(
            glm.vec4(self.linear[0], 0),
            glm.vec4(self.linear[1], 0),
            glm.vec4(self.linear[2], 0),
            glm.vec4(self.offset, 1),
        )

    @property
    def matrix(self):
        return np.array(self.affine)

    matrix.__doc__ = Aff.matrix.__doc__

    @property
    def det(self):
        return glm.determinant(self.linear)

    det.__doc__ = Aff.det.__doc__

    # ----- methods -----

    def __init__(
        self,
        offset=np.zeros(3),
        linear: tp.Union[np.ndarray, glm.mat3] = glm.mat3(),
    ):
        self.offset = offset
        self.linear = linear

    def __repr__(self):
        return f"Aff3d(offset={repr(self.offset)}, linear={repr(self.linear)})"


# ----- casting -----


_bc.register_cast(
    Aff3d, Aff, lambda x: Aff(weights=x.weight, bias=x.offset, check_shapes=False)
)
_bc.register_cast(
    Aff, Aff3d, lambda x: Aff3d(weight=x.weight, bias=x.bias, check_shape=False)
)
_bc.register_castable(Aff, Aff3d, lambda x: x.ndim == 3)


# ----- transform functions -----


def transform_Aff3d_on_Moments3d(aff_tfm, moments):
    """Transform a Moments3d using a 3D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff3d
        3D affine transformation
    moments : Moments3d
        3D moments

    Returns
    -------
    Moments3d
        affined-transformed 3D moments
    """
    A = aff_tfm.linear
    old_m0 = moments.m0
    old_mean = moments.mean_glm
    old_cov = moments.cov_glm
    new_mean = A * old_mean + aff_tfm.offset
    new_cov = A * old_cov * glm.transpose(A.T)
    new_m0 = old_m0 * abs(aff_tfm.det)
    new_m1 = new_m0 * new_mean
    new_m2 = new_m0 * (np.outer(new_mean, new_mean) + new_cov)
    return Moments3d(new_m0, new_m1, new_m2)


register_transform(Aff3d, Moments3d, transform_Aff3d_on_Moments3d)


def transform_Aff3d_on_ndarray(aff_tfm, point_array):
    """Transform an array of 3D points using a 3D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff3d or Aff
        a 3D affine transformation
    point_array : numpy.ndarray with last dimension having the same length as the dimensionality of the transformation
        an array of 3D points

    Returns
    -------
    numpy.ndarray
        affine-transformed point array
    """
    return point_array @ aff_tfm.weight.T + aff_tfm.bias


register_transform(Aff3d, np.ndarray, transform_Aff3d_on_ndarray)
register_transformable(Aff3d, np.ndarray, lambda x, y: y.shape[-1] == 3)


def transform_Aff3d_on_PointList3d(aff_tfm, point_list):
    """Transform a 3D point list using a 3D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff3d
        a 3D affine transformation
    point_list : PointList3d
        a 3D point list

    Returns
    -------
    PointList3d
        affine-transformed point list
    """
    return PointList3d(point_list.points @ aff_tfm.weight.T + aff_tfm.bias, check=False)


register_transform(Aff3d, PointList3d, transform_Aff3d_on_PointList3d)


# ---- utilities -----


def rot3d_x(angle: float):
    """Gets 3D rotation about the x-axis (roll rotation).

    Parameters
    ----------
    angle : float
        the angle to rotate

    Returns
    -------
    tfm : Aff3d
        The output rotation
    """

    sa = glm.sin(angle)
    ca = glm.cos(angle)
    weight = np.array([[1.0, 0.0, 0.0], [0.0, ca, -sa], [0.0, sa, ca]])
    return Aff3d(linear=weight)


def rot3d_y(angle: float):
    """Gets 3D rotation about the y-axis (pitch rotation).

    Parameters
    ----------
    angle : float
        the angle to rotate

    Returns
    -------
    tfm : Aff3d
        The output rotation
    """

    sa = glm.sin(angle)
    ca = glm.cos(angle)
    weight = np.array([[ca, 0.0, sa], [0.0, 1.0, 0.0], [-sa, 0.0, ca]])
    return Aff3d(linear=weight)


def rot3d_z(angle: float):
    """Gets 3D rotation about the z-axis (yaw rotation).

    Parameters
    ----------
    angle : float
        the angle to rotate

    Returns
    -------
    tfm : Aff3d
        The output rotation
    """

    sa = glm.sin(angle)
    ca = glm.cos(angle)
    weight = np.array([[ca, -sa, 0.0], [sa, ca, 0.0], [0.0, 0.0, 1.0]])
    return Aff3d(linear=weight)
