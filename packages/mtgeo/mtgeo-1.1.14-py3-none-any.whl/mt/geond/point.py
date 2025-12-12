"""The base class to represent a point. 

For efficiency reasons, please try to bunch points into arrays or lists and use appropriate representations instead of using single points implemented here.
"""


import numpy as _np
import mt.base.casting as _bc
from ..geo import GeometricObject


__all__ = ["Point", "castable_ndarray_Point"]


def castable_ndarray_Point(obj, ndim):
    return len(obj.shape) == 1 and obj.shape[0] == ndim


class Point(GeometricObject):
    """A point.

    Parameters
    ----------
    point : iterable
        A list of point coordinates, which is an iterable of D items, where D is the `ndim` of the class.
    check : bool
        Whether or not to check if the shape is valid

    Attributes
    ----------
    point : `numpy.ndarray(shape=(D,))`
        The point in numpy.
    """

    def __init__(self, point, check=True):
        point = point if isinstance(point, _np.ndarray) else _np.array(point)
        if check and not castable_ndarray_Point(point, self.ndim):
            raise ValueError(
                "Point in {}D not in the right length: {}".format(self.ndim, len(point))
            )
        self.point = point
