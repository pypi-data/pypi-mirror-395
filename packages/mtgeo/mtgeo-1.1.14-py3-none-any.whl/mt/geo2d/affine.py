from mt import tp, np, glm
import mt.base.casting as _bc

from ..geo import TwoD, register_transform, register_transformable
from ..geond import Aff
from .moments import Moments2d
from .point_list import PointList2d
from .polygon import Polygon
from .rect import Rect
from .linear import sshr2mat, mat2sshr


__all__ = [
    "Aff2d",
    "transform_Aff2d_on_Moments2d",
    "transform_Aff2d_on_PointList2d",
    "transform_Aff2d_on_ndarray",
    "transform_Aff2d_on_Polygon",
    "swapAxes2d",
    "flipLR2d",
    "flipUD2d",
    "shearX2d",
    "shearY2d",
    "originate2d",
    "rotate2d",
    "translate2d",
    "scale2d",
    "crop2d",
    "crop_rect",
    "uncrop_rect",
    "rect2rect",
    "rect2rect_tf",
]


class Aff2d(TwoD, Aff):
    """Affine transformation in 2D.

    The 2D affine transformation defined here consists of a linear/weight part and an offset/bias
    part.

    Attributes
    ----------
    offset : glm.vec2
        the bias vector
    bias : numpy.ndarray
        the numpy view of `offset`
    linear : glm.mat2
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
        """Obtains an Aff2d instance from a non-singular affine transformation matrix.

        Parameters
        ----------
        mat : a 3x3 array
            a non-singular affine transformation matrix

        Returns
        -------
        Aff2d
            An instance representing the transformation

        Notes
        -----
        For speed reasons, no checking is involved.
        """
        return Aff2d(offset=mat[:2, 2], linear=mat[:2, :2])

    # ----- base adaptation -----

    @property
    def ndim(self):  # reimplementation to enforce constantness
        return 2

    def multiply(self, other):
        if not isinstance(other, Aff2d):
            return super(Aff2d, self).multiply(other)
        return Aff2d(
            offset=self.linear * other.offset + self.offset,
            linear=self.linear * other.linear,
        )

    multiply.__doc__ = Aff.multiply.__doc__

    def invert(self):
        invLinear = glm.inverse(self.linear)
        invOffset = invLinear * (-self.offset)
        return Aff2d(offset=invOffset, linear=invLinear)

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
        return 2

    bias_dim.__doc__ = Aff.bias_dim.__doc__

    @property
    def weight(self):
        return np.frombuffer(self.__linear.to_bytes(), dtype=np.float32).reshape(2, 2).T

    weight.__doc__ = Aff.weight.__doc__

    @weight.setter
    def weight(self, weight):
        raise TypeError("Weight matrix is read-only. Use self.linear instead.")

    @property
    def weight_shape(self):
        return (2, 2)

    weight_shape.__doc__ = Aff.weight_shape.__doc__

    # ----- data encapsulation -----

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, value: tp.Union[np.ndarray, glm.vec2]):
        self.__offset = glm.vec2(value)

    @property
    def linear(self):
        return self.__linear

    @linear.setter
    def linear(self, value: tp.Union[np.ndarray, glm.mat2, glm.vec4]):
        if isinstance(value, glm.vec4):
            value = sshr2mat(value)
        if isinstance(value, np.ndarray):
            self.__linear = glm.mat2(glm.vec2(value[:, 0]), glm.vec2(value[:, 1]))
        else:
            self.__linear = glm.mat2(value)

    # ----- derived properties -----

    @property
    def affine(self):
        return glm.mat3(
            glm.vec3(self.linear[0], 0),
            glm.vec3(self.linear[1], 0),
            glm.vec3(self.offset, 1),
        )

    @property
    def matrix(self):
        return np.array(self.affine)

    @property
    def matrix(self):
        a = np.empty((3, 3))
        a[:2, :2] = self.weight
        a[:2, 2] = self.bias
        a[2, :2] = 0
        a[2, 2] = 1
        return a

    matrix.__doc__ = Aff.matrix.__doc__

    @property
    def det(self):
        return glm.determinant(self.linear)

    det.__doc__ = Aff.det.__doc__

    # ----- methods -----

    def __init__(
        self,
        offset=np.zeros(2),
        linear: tp.Union[np.ndarray, glm.mat2, glm.vec4] = glm.mat2(),
    ):
        self.offset = offset
        self.linear = linear

    def __repr__(self):
        return f"Aff2d(offset={repr(self.offset)}, linear={repr(self.linear)})"


# ----- casting -----


_bc.register_cast(
    Aff2d, Aff, lambda x: Aff(weights=x.weight, bias=x.offset, check_shapes=False)
)
_bc.register_cast(Aff, Aff2d, lambda x: Aff2d(offset=x.bias, linear=x.weight))
_bc.register_castable(Aff, Aff2d, lambda x: x.ndim == 2)


# ----- transform functions -----


def transform_Aff2d_on_Moments2d(aff_tfm, moments):
    """Transform a Moments2d using a 2D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff2d
        2D affine transformation
    moments : Moments2d
        2D moments

    Returns
    -------
    Moments2d
        affined-transformed 2D moments
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
    return Moments2d(new_m0, new_m1, new_m2)


register_transform(Aff2d, Moments2d, transform_Aff2d_on_Moments2d)


def transform_Aff2d_on_ndarray(aff_tfm, point_array):
    """Transform an array of 2D points using a 2D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff
        a 2D affine transformation
    point_array : numpy.ndarray with last dimension having the same length as the dimensionality of the transformation
        an array of 2D points

    Returns
    -------
    numpy.ndarray
        affine-transformed point array
    """
    return point_array @ aff_tfm.weight.T + aff_tfm.bias


register_transform(Aff2d, np.ndarray, transform_Aff2d_on_ndarray)
register_transformable(Aff2d, np.ndarray, lambda x, y: y.shape[-1] == 2)


def transform_Aff2d_on_PointList2d(aff_tfm, point_list):
    """Transform a 2D point list using a 2D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff2d
        a 2D affine transformation
    point_list : PointList2d
        a 2D point list

    Returns
    -------
    PointList2d
        affine-transformed point list
    """
    return PointList2d(point_list.points @ aff_tfm.weight.T + aff_tfm.bias, check=False)


register_transform(Aff2d, PointList2d, transform_Aff2d_on_PointList2d)


def transform_Aff2d_on_Polygon(aff_tfm, poly):
    """Transform a polygon using a 2D affine transformation.

    Parameters
    ----------
    aff_tfm : Aff2d
        a 2D affine transformation
    poly : Polygon
        a 2D polygon

    Returns
    -------
    Polygon
        affine-transformed polygon
    """
    return Polygon(poly.points @ aff_tfm.weight.T + aff_tfm.bias, check=False)


register_transform(Aff2d, Polygon, transform_Aff2d_on_Polygon)


# ----- useful 2D transformations -----


def swapAxes2d():
    """Returns the affine transformation that swaps the x-axis with the y-axis."""
    return Aff2d(linear=glm.mat2([0, 1], [1, 0]))


def flipLR2d(width):
    """Returns a left-right flip for a given width."""
    return Aff2d.from_matrix(np.array([[-1, 0, width], [0, 1, 0]]))


def flipUD2d(height):
    """Returns a up-down flip for a given height."""
    return Aff2d.from_matrix(np.array([[1, 0, 0], [0, -1, height]]))


def shearX2d(h):
    """Returns the shearing along the x-axis."""
    return Aff2d(linear=glm.vec4(1, 1, h, 0))


def shearY2d(h):
    """Returns the shearing along the y-axis."""
    return Aff2d(linear=glm.mat2([1, h], [0, 1]))


def originate2d(tfm, x, y):
    """Tweaks a 2D affine transformation so that it acts as if it originates at (x,y) instead of (0,0)."""
    return Aff2d(offset=np.array((x, y))).conjugate(tfm)


def rotate2d(theta, x, y):
    """Returns the rotation about a reference point (x,y). Theta is in radian."""
    return originate2d(Aff2d(linear=glm.vec4(1, 1, 0, theta)), x, y)


def translate2d(x, y):
    """Returns the translation."""
    return Aff2d(offset=np.array([x, y]))


def scale2d(scale_x=1, scale_y=None):
    """Returns the scaling."""
    if scale_y is None:
        scale_y = scale_x
    return Aff2d(linear=glm.vec4(scale_x, scale_y, 0, 0))


def crop2d(tl, br=None):
    """Transforms an axis-aligned rectangle into [(0,0),(1,1)].

    Parameters
    ----------
    tl : 2d point (x,y)
        coordinates to be mapped to (0,0) if `br` is specified. If `br` is not specified, then the transformation is 2d scaling. In other words, (0,0) is mapped to (0,0) and tl is mapped to (1,1).
    br : 2d point (x,y), optional
        If specified, coordinates to be mapped to (1,1).

    Returns
    -------
    Aff2d
        A transformation that maps points in [(0,0),(1,1)] to the crop given by `tl` and `br`.
    """
    if br is None:
        return scale2d(1.0 / tl[0], 1.0 / tl[1])
    return Aff2d(
        offset=np.array([-tl[0] / (br[0] - tl[0]), -tl[1] / (br[1] - tl[1])]),
        linear=glm.vec4(1.0 / (br[0] - tl[0]), 1.0 / (br[1] - tl[1]), 0, 0),
    )


def crop_rect(r: Rect) -> Aff2d:
    """Transforms an-axis-aligned Rect into [(0,0),(1,1)].

    Parameters
    ----------
    r : Rect
        the input rectangle

    Returns
    -------
    Aff2d
        A transformation that maps points in [(0,0),(1,1)] to the crop given by `tl` and `br`.
    """
    return crop2d((r.min_x, r.min_y), (r.max_x, r.max_y))


def uncrop_rect(tfm: Aff2d) -> Rect:
    """Transforms a 2D affine transformation back to a crop, ignoring shearing and rotation.

    Parameters
    ----------
    tfm : Aff2d
        A 2D affine transformation supposedly transforms a crop to [(0,0),(1,1)]

    Returns
    -------
    Rect
        the recovered rectangle
    """
    tfm = ~tfm  # take the inverse
    x, y = tfm.bias
    linear = mat2sshr(tfm.linear)
    w, h = linear.xy
    return Rect(x, y, x + w, y + h)


def rect2rect(src_rect: Rect, dst_rect: Rect, eps=1e-7) -> Aff2d:
    """Returns an Aff2d that transforms pixels in a source Rect to pixels in a destination Rect.

    The transformation ensures that the source corner pixels match with the destination corner pixels.

    Parameters
    ----------
    src_rect : Rect
        source rectangle
    dst_rect : Rect
        destination rectangle
    eps : float
        epsilon to detect zero source width or height

    Returns
    -------
    Aff2d
        the output transformation
    """
    if abs(src_rect.w) < eps:
        if abs(dst_rect.w) < eps:
            sx = 0.0
        else:
            raise ValueError(
                "Source width is zero {} but destination width is not {}.".format(
                    src_rect.w, dst_rect.w
                )
            )
    else:
        sx = dst_rect.w / src_rect.w
    if abs(src_rect.h) < eps:
        if abs(dst_rect.h) < eps:
            sy = 0.0
        else:
            raise ValueError(
                "Source height is zero {} but destination height is not {}.".format(
                    src_rect.h, dst_rect.h
                )
            )
    else:
        sy = dst_rect.h / src_rect.h
    return (
        translate2d(dst_rect.cx, dst_rect.cy)
        * scale2d(sx, sy)
        / translate2d(src_rect.cx, src_rect.cy)
    )


def rect2rect_tf(src_rects, dst_rects):
    """A tensorflow version of :func:`rect2rect` where inputs and outputs are replaced by tensors.

    ----------
    src_rects : tf.Tensor
        source rectangles of shape `[batch, 4]` where each batch item is `[min_x, min_y, max_x, max_y]`
    dst_rects : tf.Tensor
        destination rectangles of shape `[batch, 4]` where each batch item is
        `[min_x, min_y, max_x, max_y]`

    Returns
    -------
    tfm_array : tf.Tensor
        the output transformations of shape `[batch, 3, 3]` where each item is a 3x3 affine
        transformation matrix mapping source coordinates to destination coordinates
    """
    from mt import tf

    # batch_size = src_rects.shape[0]

    # center points
    src_pts = (src_rects[:, 0:2] + src_rects[:, 2:4]) * 0.5
    dst_pts = (dst_rects[:, 0:2] + dst_rects[:, 2:4]) * 0.5

    # lengths
    src_lens = src_rects[:, 2:4] - src_rects[:, 0:2]
    dst_lens = dst_rects[:, 2:4] - dst_rects[:, 0:2]

    # scales
    scales = tf.math.divide_no_nan(dst_lens, src_lens)

    # translations: src_pts*scales + transalations = dst_pts
    translations = dst_pts - src_pts * scales

    # parts of the returning array of 3x3 matrices
    sx = tf.tensordot(
        scales[:, 0],
        tf.constant(
            [
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        ),
        axes=0,
    )
    sy = tf.tensordot(
        scales[:, 1],
        tf.constant(
            [
                [0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        ),
        axes=0,
    )
    tx = tf.tensordot(
        translations[:, 0],
        tf.constant(
            [
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        ),
        axes=0,
    )
    ty = tf.tensordot(
        translations[:, 1],
        tf.constant(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0],
            ]
        ),
        axes=0,
    )
    ones = tf.expand_dims(
        tf.constant(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        ),
        axis=0,
    )

    # returning
    return sx + sy + tx + ty + ones
