"""There are many definitions of an ellipsoid. In our case, an ellipsoid is an affine transform of the unit sphere x^2+y^2+z^2=1."""

from mt import np, glm
from mt.base.casting import register_cast, register_castable, cast

from ..geo import (
    GeometricObject,
    ThreeD,
    register_transform,
    register_upper_bound,
    register_lower_bound,
)
from ..geond import Hyperellipsoid
from .affine import Aff3d
from .box import Box


__all__ = ["Ellipsoid", "transform_Aff3d_on_Ellipsoid"]


class Ellipsoid(ThreeD, GeometricObject):
    """Ellipsoid, defined as an affine transform the unit sphere x^2+y^2+z^2=1.

    If the unit sphere is parameterised by `(cos(t_1), sin(t_1)*cos(t_2), sin(t_1)*sin(t_2))` where
    `t_1 \in [0,\pi)` and `t_2 \in [0,2\pi)` then the ellipsoid is parameterised by
    `f0 + f1 cos(t_1) + f2 sin(t_1) cos(t_2) + f3 sin(t_1) sin(t_2)`, where `f0` is the bias
    vector, `f1, f2, f3` are the columns of the weight matrix from left to right respectively, of
    the affine transformation. They are also called called axes of the ellipsoid.

    Note that this representation is not unique, the same ellipsoid can be represented by an
    infinite number of affine transforms of the unit sphere. To make the representation more useful
    we further assert that when the axes are perpendicular (linearly independent), the ellipsoid is
    normalised. In other words, the weight matrix is a unitary matrix multiplied by a diagonal
    matrix. After normalisation there is almost surely a finite number of ways to represent the
    same ellipsoid, except for singular cases. You can normalise either at initialisation time, or
    later by invoking member function `normalised`.

    Parameters
    ----------
    aff_tfm : Aff3d
        a 3D affine transformation
    make_normalised : bool
        whether or not to adjust the affine transformation to make a normalised representation of
        the ellipsoid

    Examples
    --------
    >>> import numpy as np
    >>> from mt.geo3d import Aff3d, Ellipsoid
    >>> a = Aff3d(bias=np.array([2,3]), weight=np.diag([4,5]))
    >>> e = Ellipsoid(a)
    >>> e
    Ellipsoid(aff_tfm=Aff3d(weight_diagonal=[0. 0.], bias=[2 3]))
    >>> e.aff_tfm.matrix
    array([[0., 4., 2.],
           [5., 0., 3.],
           [0., 0., 1.]])
    """

    # ----- construction -----

    def __init__(self, aff_tfm, make_normalised=True):
        """Initialises an ellipsoid with an affine transformation."""
        if not isinstance(aff_tfm, Aff3d):
            raise ValueError("Only an instance of class `Aff3d` is accepted.")
        if make_normalised:
            U, S, VT = glm.svd3(aff_tfm.linear)
            aff_tfm = Aff3d(bias=aff_tfm.bias, linear=U * glm.mat3diag(S))
        self.aff_tfm = aff_tfm

    def __repr__(self):
        return "Ellipsoid(aff_tfm={})".format(self.aff_tfm)

    @property
    def volume(self):
        """The absolute volume of the ellipsoid's interior."""
        return (4 * np.pi / 3) * self.aff_tfm.det

    @property
    def surface_area(self):
        """The surface area of the ellipsoid."""
        raise NotImplementedError(
            "It's quite complicated to compute the surface area of an ellipsoid. I will only be implemented when there's a real demand. MT has to check with the Wiki page first."
        )

    def normalised(self):
        """Returns an equivalent ellipsoid where f1, f2 and f3 are perpendicular (linearly independent)."""
        return Ellipsoid(self.aff_tfm, make_normalised=True)


# ----- casting -----


register_cast(
    Ellipsoid,
    Hyperellipsoid,
    lambda x: Hyperellipsoid(x.aff_tfm, make_normalised=False),
)
register_cast(
    Hyperellipsoid, Ellipsoid, lambda x: Ellipsoid(x.aff_tfm, make_normalised=False)
)
register_castable(Hyperellipsoid, Ellipsoid, lambda x: x.ndim == 3)


# ----- bounding -----


def upper_bound_Ellipsoid_to_Box(obj):
    """Returns a bounding axis-aligned box of the ellipsoid.

    Parameters
    ----------
    obj : Ellipsoid
        the ellipsoid to be upper-bounded

    Returns
    -------
    Box
        a bounding Box of the ellipsoid
    """
    weight = obj.aff_tfm.weight
    c = off.aff_tfm.bias
    m = np.array([np.linalg.norm(weight[i]) for i in range(3)])
    return Box(min_coords=c - m, max_coords=c + m)


register_upper_bound(Ellipsoid, Box, upper_bound_Ellipsoid_to_Box)


def lower_bound_Box_to_Ellipsoid(x):
    """Returns an axis-aligned ellipsoid bounded by the given axis-aligned box.

    Parameters
    ----------
    x : Box
        the box from which the enclosed ellipsoid is computed

    Returns
    -------
    Ellipsoid
        the axis-aligned ellipsoid enclosed by the box
    """
    if not isinstance(x, Box):
        raise ValueError("Input type must be a `Box`, '{}' given.".format(x.__class__))
    return Ellipsoid(cast(x.dlt_tfm, Aff3d))


register_lower_bound(Box, Ellipsoid, lower_bound_Box_to_Ellipsoid)


# ----- transform functions -----


def transform_Aff3d_on_Ellipsoid(aff_tfm, obj):
    """Affine-transforms an Ellipsoid. The resultant Ellipsoid has affine transformation `aff_tfm*obj.aff_tfm`.

    Parameters
    ----------
    aff_tfm  : Aff3d
        an affine transformation
    obj : Ellipsoid
        an ellipsoid

    Returns
    -------
    Ellipsoid
        the affine-transformed ellipsoid
    """
    return Ellipsoid(aff_tfm * obj.aff_tfm)


register_transform(Aff3d, Ellipsoid, transform_Aff3d_on_Ellipsoid)
