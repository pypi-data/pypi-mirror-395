"""Hyperrectangle."""

from mt import np
from ..geo import GeometricObject, join_volume, register_join_volume
from .dilatation import Dlt
from .iou import iou_impl

__all__ = ["Hyperbox"]


class Hyperbox(GeometricObject):
    """Axis-aligned n-dimensional hyperrectangle.

    An axis-aligned n-dimensional box/hyperrectangle is defined as the set of points of the hypercube [-1,1]^n transformed by a dilatation.

    Note that is is a many-to-one representation. For each box, there are up to 2^n dilatations that map the hypbercube [-1,1]^n to it.

    Parameters
    ----------
    min_coords : 1d array or Dlt
        array of minimum coordinate values for all the dimensions, or the dilatation if self. In case of the latter, the `max_coords` argument is ignored.
    max_coords : 1d array
        array of maximum coordinate values for all the dimensions. If it is None, then `min_coords` represents `max_coords` and the minimum coordinate values are assumed 0.
    force_valid : bool
        whether or not to sort out `min_coords` and `max_coords` to make the the minus point meet the min_coords and the plus point meet the max_coords.

    Attributes
    ----------
    dlt_tfm : Dlt
        the dilatation equivalent, which can be get/set
    dim : int
        number of dimensions
    minus_pt : point
        the (-1,)^n point after being transformed by the dilatation
    plus_pt : point
        the (+1,)^n point after being transformed by the dilatation
    min_coords : point
        minimum coordinates
    max_coords : point
        maximum coordinates
    center_pt : point
        center point
    size : size/point
        box size
    """

    # ----- data encapsulation -----

    @property
    def dlt_tfm(self):
        """the dilatation"""
        return self.__dlt_tfm

    @dlt_tfm.setter
    def dlt_tfm(self, dlt_tfm):
        self.__dlt_tfm = dlt_tfm

    # ----- derived properties -----

    @classmethod
    def ndim(self):
        """The dimensionality"""
        return self.dim

    @property
    def dim(self):
        """The dimensionality"""
        return self.dlt_tfm.dim

    @property
    def minus_pt(self):
        """The (-1,)^n point after being transformed by the dilatation."""
        return self.dlt_tfm.offset - self.dlt_tfm.scale

    @property
    def plus_pt(self):
        """The (+1,)^n point after being transformed by the dilatation."""
        return self.dlt_tfm.offset + self.dlt_tfm.scale

    @property
    def min_coords(self):
        """minimum coordinates"""
        return np.minimum(self.minus_pt, self.plus_pt)

    @property
    def max_coords(self):
        """maximum coordinates"""
        return np.maximum(self.minus_pt, self.plus_pt)

    @property
    def center_pt(self):
        """center point"""
        return self.dlt_tfm.offset

    @property
    def size(self):
        """box size"""
        return np.abs(self.dlt_tfm.scale * 2)

    @property
    def signed_volume(self):
        """signed (hyper-)volume"""
        return (self.max_coords - self.min_coords).prod()

    @property
    def volume(self):
        """absolute/unsigned (hyper-)volume"""
        return abs(self.signed_volume)

    # ----- methods -----

    def __init__(self, min_coords, max_coords=None, force_valid=False):
        if isinstance(min_coords, Dlt):
            self.dlt_tfm = min_coords
        else:
            if max_coords is None:
                max_coords = min_coords
                min_coords = np.zeros(dim)
            self.dlt_tfm = Dlt(
                offset=(max_coords + min_coords) / 2,
                scale=(max_coords - min_coords) / 2,
            )

        if force_valid:
            min_coords = self.min_coords
            max_coords = self.max_coords
            self.dlt_tfm = Dlt(
                offset=(max_coords + min_coords) / 2,
                scale=(max_coords - min_coords) / 2,
            )

    def __repr__(self):
        return "Hyperbox({})".format(self.dlt_tfm)

    def is_valid(self):
        return (self.dlt_tfm.scale >= 0).all()

    def validated(self):
        """Returns a validated version of the box."""
        min_coords = self.min_coords
        max_coords = self.max_coords
        return Hyperbox(
            Dlt(offset=(max_coords + min_coords) / 2, scale=max_coords - min_coords)
        )

    def intersect(self, other):
        return Hyperbox(
            np.maximum(self.min_coords, other.min_coords),
            np.minimum(self.max_coords, other.max_coords),
        )

    def box_union(self, other):
        return Hyperbox(
            np.minimum(self.min_coords, other.min_coords),
            np.maximum(self.max_coords, other.max_coords),
        )

    def iou(self, other, epsilon=1e-7):
        return iou_impl(
            self.intersect(other).volume, self.volume, other.volume, eps=epsilon
        )


# ----- joining volumes -----


def join_volume_Hyperbox_and_Hyperbox(obj1, obj2):
    """Joins the volumes of two Hyperboxes of the same dimension.

    Parameters
    ----------
    obj1 : Hyperbox
        the first hyperbox
    obj2 : Hyperbox
        the second hyperbox

    Returns
    -------
    intersection_volume : float
        the volume of the intersection of the two hyperboxes' interior regions
    obj1_only_volume : float
        the volume of the interior of obj1 that does not belong to obj2
    obj2_only_volume : float
        the volume of the interior of obj2 that does not belong to obj1
    union_volume : float
        the volume of the union of the two hyperboxes' interior regions
    """
    if obj1.dim != obj2.dim:
        raise ValueError(
            "Two objects of dimension {} and {} are not in the same space.".format(
                obj1.dim, obj2.dim
            )
        )
    inter = obj1.intersect(obj2)
    inter_volume = inter.volume
    obj1_volume = obj1.volume
    obj2_volume = obj2.volume
    return (
        inter_volume,
        obj1_volume - inter_volume,
        obj2_volume - inter_volume,
        obj1_volume + obj2_volume - inter_volume,
    )


register_join_volume(Hyperbox, Hyperbox, join_volume_Hyperbox_and_Hyperbox)
