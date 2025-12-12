"""The base class to represent a list of points."""

from mt import tp, np, glm
import mt.base.casting as bc
from ..geo import TwoD
from ..geond import PointList, castable_ndarray_PointList


__all__ = ["PointList2d"]


class PointList2d(TwoD, PointList):
    """A list of 2D points.

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
        The array of vec2 points
    points : `numpy.ndarray(shape=(N,2))`
        The numpy view of `points_glm`
    """

    def __init__(self, point_list: tp.Union[list, np.ndarray, glm.array]):
        self.points = point_list

    @property
    def points(self):
        p = np.frombuffer(self.points_glm.to_bytes(), dtype=np.float32)
        return p.reshape((len(p) // 2, 2))

    @points.setter
    def points(self, point_list: tp.Union[list, np.ndarray, glm.array]):
        if len(point_list) == 0:
            self.points_glm = glm.array.zeros(0, glm.vec2)
        elif isinstance(point_list, glm.array):
            self.points_glm = point_list
            if not isinstance(self.points_glm[0], glm.vec2):
                self.points_glm = self.points_glm.reinterpret_cast(glm.vec2)
        else:
            self.points_glm = glm.array([glm.vec2(x) for x in point_list])


bc.register_castable(
    np.ndarray, PointList2d, lambda x: castable_ndarray_PointList(x, 2)
)
bc.register_cast(np.ndarray, PointList2d, lambda x: PointList2d(x, check=False))
bc.register_cast(PointList2d, PointList, lambda x: PointList(x.points, check=False))
bc.register_cast(PointList, PointList2d, lambda x: PointList2d(x.points, check=False))
bc.register_castable(PointList, PointList2d, lambda x: x.ndim == 2)
