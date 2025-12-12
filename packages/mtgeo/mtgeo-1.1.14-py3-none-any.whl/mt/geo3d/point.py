"""The base class to represent a point.

For efficiency reasons, please try to bunch points into arrays or lists and use appropriate
representations instead of using single points implemented here.
"""


from mt import np, glm
import mt.base.casting as _bc
from ..geo import ThreeD
from ..geond import Point, castable_ndarray_Point


__all__ = ["Point3d"]


class Point3d(ThreeD, Point):
    """A 3D point implemented in glm.

    See :class:`Point` for more details.

    Attributes
    ----------
    point_glm : `glm.vec3`
        The point in glm.
    point : `numpy.ndarray(shape=(3,), dtype=numpy.float32)`
        The numpy view of `point_glm`
    """

    def __init__(self, point, check=True):
        self.point = point

    @property
    def point(self):
        return np.array(self.point_glm)

    @point.setter
    def point(self, p):
        self.point_glm = glm.vec3(p)


_bc.register_castable(np.ndarray, Point3d, lambda x: castable_ndarray_Point(x, 3))
_bc.register_cast(np.ndarray, Point3d, lambda x: Point3d(x, check=False))
_bc.register_cast(Point3d, Point, lambda x: Point(x.point, check=False))
_bc.register_cast(Point, Point3d, lambda x: Point3d(x.point, check=False))
_bc.register_castable(Point, Point3d, lambda x: x.ndim == 3)
