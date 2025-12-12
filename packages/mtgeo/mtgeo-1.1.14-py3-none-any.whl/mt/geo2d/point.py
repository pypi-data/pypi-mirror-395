"""The base class to represent a point.

For efficiency reasons, please try to bunch points into arrays or lists and use appropriate
representations instead of using single points implemented here.
"""

from mt import np, glm
import mt.base.casting as _bc
from ..geo import TwoD
from ..geond import Point, castable_ndarray_Point


__all__ = ["Point2d"]


class Point2d(TwoD, Point):
    """A 2D point implemented in glm.

    See :class:`Point` for more details.

    Attributes
    ----------
    point_glm : `glm.vec2`
        The point in glm.
    point : `numpy.ndarray(shape=(2,), dtype=numpy.float32)`
        The numpy view of `point_glm`
    """

    def __init__(self, point):
        self.point = point

    @property
    def point(self):
        return np.array(self.point_glm)

    @point.setter
    def point(self, p):
        self.point_glm = glm.vec2(p)


_bc.register_castable(np.ndarray, Point2d, lambda x: castable_ndarray_Point(x, 2))
_bc.register_cast(np.ndarray, Point2d, lambda x: Point2d(x, check=False))
_bc.register_cast(Point2d, Point, lambda x: Point(x.point, check=False))
_bc.register_cast(Point, Point2d, lambda x: Point2d(x.point, check=False))
_bc.register_castable(Point, Point2d, lambda x: x.ndim == 2)
