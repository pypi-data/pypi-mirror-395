"""There are many definitions of a hyperellipsoid. In our case, a hyperellipsoid is an affine transform of the unit hypersphere x^2+y^2+...=1."""

from mt import np
from mt.base.casting import register_cast, cast
from mt.base.deprecated import deprecated_func

from ..geo import (
    GeometricObject,
    register_transform,
    register_transformable,
    register_upper_bound,
    register_lower_bound,
)
from .affine import Aff
from .hyperbox import Hyperbox


__all__ = ["Hyperellipsoid", "transform_Aff_on_Hyperellipsoid"]


class Hyperellipsoid(GeometricObject):
    """Hyperellipsoid, defined as an affine transform the unit hypersphere x^2+y^2+z^2+...=1.

    If the unit hypersphere is parameterised by `(cos(t_1), sin(t_1)*cos(t_2), sin(t_1)*sin(t_2)*cos(t_3), ...)` where `t_1, t_2, ... \\in [0,\\pi)` but the last `t_{dim-1} \\in [0,2\\pi)` then the hyperellipsoid is parameterised by `f0 + f1 cos(t_1) + f2 sin(t_1) cos(t_2) + f3 sin(t_1) sin(t_2) sin(t_3) cos(t_4) + ...`, where `f0` is the bias vector, `f1, f2, ...` are the columns of the weight matrix from left to right respectively, of the affine transformation. They are also called called axes of the hyperellipsoid.

    Note that this representation is not unique, the same hyperellipsoid can be represented by an infinite number of affine transforms of the unit hypersphere. To make the representation more useful and more unique, we further assert that when the axes are perpendicular (linearly independent), the hyperellipsoid is normalised. In other words, the weight matrix is a unitary matrix multiplied by a diagonal matrix. After normalisation there can still be an infinite number of ways to represent the same hyperellipsoid, but only in singular cases. You can normalise either at initialisation time, or later by invoking member function `normalised`.

    Parameters
    ----------
    aff_tfm : Aff
        an affine transformation
    make_normalised : bool
        whether or not to adjust the affine transformation to make a normalised representation of the hyperellipsoid

    Examples
    --------
    >>> import numpy as np
    >>> from mt.geond.hyperellipsoid import Aff, Hyperellipsoid
    >>> a = Aff(bias=np.array([2,3]), weight=np.diag([4,5]))
    >>> e = Hyperellipsoid(a)
    >>> e
    Hyperellipsoid(aff_tfm=Aff(weight_diagonal=[0. 0.], bias=[2 3]))
    >>> e.aff_tfm.matrix
    array([[0., 4., 2.],
           [5., 0., 3.],
           [0., 0., 1.]])
    """

    # ----- base adaptation -----

    @property
    def ndim(self):
        return self.aff_tfm.bias

    # ----- construction ------

    def __init__(self, aff_tfm, make_normalised=True):
        """Initialises a hyperellipsoid with an affine transformation."""
        if not isinstance(aff_tfm, Aff):
            raise ValueError("Only an instance of class `Aff` is accepted.")
        if make_normalised:
            U, S, VT = np.linalg.svd(aff_tfm.weight, full_matrices=False)
            aff_tfm = Aff(bias=aff_tfm.bias, weight=U @ np.diag(S))
        self.aff_tfm = aff_tfm

    def __repr__(self):
        return "Hyperellipsoid(aff_tfm={})".format(self.aff_tfm)

    # ----- useful functions

    def normalised(self):
        """Returns an equivalent hyperellipsoid where f1 and f2 are perpendicular (linearly independent)."""
        return Hyperellipsoid(self.aff_tfm, make_normalised=True)


# ----- bounding -----


def upper_bound_Hyperellipsoid_to_Hyperbox(obj):
    """Returns a bounding axis-aligned box of the hyperellipsoid.

    Parameters
    ----------
    obj : Hyperellipsoid
        the hyperellipsoid to be upper-bounded

    Returns
    -------
    Hyperbox
        a bounding Hyperbox of the hyperellipsoid
    """
    weight = obj.aff_tfm.weight
    c = off.aff_tfm.bias
    m = np.array([np.linalg.norm(weight[i]) for i in range(self.ndim)])
    return Hyperbox(min_coords=c - m, max_coords=c + m)


register_upper_bound(Hyperellipsoid, Hyperbox, upper_bound_Hyperellipsoid_to_Hyperbox)


def lower_bound_Hyperbox_to_Hyperellipsoid(x):
    """Returns an axis-aligned hyperellipsoid bounded by the given axis-aligned box.

    Parameters
    ----------
    x : Hyperbox
        the box from which the enclosed hyperellipsoid is computed

    Returns
    -------
    Hyperellipsoid
        the axis-aligned hyperellipsoid enclosed by the box
    """
    if not isinstance(x, Hyperbox):
        raise ValueError(
            "Input type must be a `Hyperbox`, '{}' given.".format(x.__class__)
        )
    return Hyperellipsoid(cast(x.dlt_tfm, Aff))


register_lower_bound(Hyperbox, Hyperellipsoid, lower_bound_Hyperbox_to_Hyperellipsoid)


# ----- transform functions -----


def transform_Aff_on_Hyperellipsoid(aff_tfm, obj):
    """Affine-transforms a hyperellipsoid. The resultant Hyperellipsoid has affine transformation `aff_tfm*obj.aff_tfm`.

    Parameters
    ----------
    aff_tfm  : Aff
        an affine transformation
    obj : Hyperellipsoid
        a hyperellipsoid

    Returns
    -------
    Hyperellipsoid
        the affine-transformed hyperellipsoid
    """
    return Hyperellipsoid(aff_tfm * obj.aff_tfm)


register_transform(Aff, Hyperellipsoid, transform_Aff_on_Hyperellipsoid)
register_transformable(
    Aff, Hyperellipsoid, lambda aff_tfm, obj: aff_tfm.ndim == obj.ndim
)
