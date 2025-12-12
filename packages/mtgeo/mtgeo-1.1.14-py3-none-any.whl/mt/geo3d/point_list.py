"""The base class to represent a list of points."""

from mt import tp, np, glm
import mt.base.casting as bc
from ..geo import ThreeD
from ..geond import PointList, castable_ndarray_PointList


__all__ = ["PointList3d"]


class PointList3d(ThreeD, PointList):
    """A list of 3D points.

    See :class:`PointList` for more details.

    Parameters
    ----------
    point_list : list or numpy.ndarray or glm.array
        A list of points, each of which is an iterable of D items, where D is the `ndim` of the
        class.
    check : bool
        Whether or not to check if the shape is valid

    Attributes
    ----------
    points_glm : glm.array
        The array of vec3 points
    points : `numpy.ndarray(shape=(N,3))`
        The numpy view of `points_glm`
    """

    def __init__(self, point_list: tp.Union[list, np.ndarray, glm.array]):
        self.points = point_list

    @property
    def points(self):
        p = np.frombuffer(self.points_glm.to_bytes(), dtype=np.float32)
        return p.reshape((len(p) // 3, 3))

    @points.setter
    def points(self, point_list: tp.Union[list, np.ndarray, glm.array]):
        if len(point_list) == 0:
            self.points_glm = glm.array.zeros(0, glm.vec3)
        elif isinstance(point_list, glm.array):
            self.points_glm = point_list
            if not isinstance(self.points_glm[0], glm.vec3):
                self.points_glm = self.points_glm.reinterpret_cast(glm.vec3)
        else:
            self.points_glm = glm.array([glm.vec3(x) for x in point_list])


bc.register_castable(
    np.ndarray, PointList3d, lambda x: castable_ndarray_PointList(x, 3)
)
bc.register_cast(np.ndarray, PointList3d, lambda x: PointList3d(x, check=False))
bc.register_cast(PointList3d, PointList, lambda x: PointList(x.points, check=False))
bc.register_cast(PointList, PointList3d, lambda x: PointList3d(x.points, check=False))
bc.register_castable(PointList, PointList3d, lambda x: x.ndim == 3)
