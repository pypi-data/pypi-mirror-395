"""Module supporting the 2x2 linear transformation."""

from mt import glm

__all__ = [
    "mat2sshr",
    "mat2sshr_tf",
    "sshr2mat",
    "sshr2mat_tf",
    "make_affine",
]


# ----- sshr representation of a 2x2 matrix -----


# Redundant vector (sx,sy,h,r,cr,sr).
# Matrix 2x2 parametrised as [a0,a1,a2,a3].


def sshr2mat(sshr: glm.vec4) -> glm.mat2:
    """Converts an sshr tuple into a mat2 transformation matrices.

    An sshr tuple (sx,sy,h,r) represents the scale2d(sx,sy) shear2d(h) rotate2d(r) transformation.

    Formula::

        cr = cos(r)
        sr = sin(r)
        a0 = sx*(h*sr + cr)
        a1 = sx*(h*cr - sr)
        a2 = sy*sr
        a3 = sy*cr
        m  = [[a0, a1], [a2, a3]]  # row-major

    Parameters
    ----------
    sshr : glm.vec4
        the input sshr tuple

    Returns
    -------
    glm.mat2
        the output 2d transformation matrix

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not really, cheeky MT is trying to advertise his paper!)
    """

    sx, sy, h, r = sshr

    cr = glm.cos(r)
    sr = glm.sin(r)
    a0 = sx * (h * sr + cr)
    a1 = sx * (h * cr - sr)
    a2 = sy * sr
    a3 = sy * cr

    return glm.mat2(glm.vec2(a0, a2), glm.vec2(a1, a3))


def sshr2mat_tf(tensor):
    """Converts an array of sshr tuples into an array of 2x2 transformation matrices.

    An sshr tuple (sx,sy,h,r) represents the scale2d(sx,sy) shear2d(h) rotate2d(r) transformation.

    Formula::

        cr = cos(r)
        sr = sin(r)
        a0 = sx*(h*sr + cr)
        a1 = sx*(h*cr - sr)
        a2 = sy*sr
        a3 = sy*cr
        m  = [[a0, a1], [a2, a3]]

    Parameters
    ----------
    tensor : tensorflow.Tensor
        a tensor of shape (batch, 4) containing sshr tuples

    Returns
    -------
    tensorflow.Tensor
        a tensor of shape (batch, 2, 2) containing 2d row-major transformation matrices

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not really, cheeky MT is trying to advertise his paper!)
    """

    from mt import tf

    sx = tensor[:, 0]
    sy = tensor[:, 1]
    h = tensor[:, 2]
    r = tensor[:, 3]

    cr = tf.math.cos(r)
    sr = tf.math.sin(r)
    a0 = sx * (h * sr + cr)
    a1 = sx * (h * cr - sr)
    a2 = sy * sr
    a3 = sy * cr

    m0 = tf.stack([a0, a1], axis=1)
    m1 = tf.stack([a2, a3], axis=1)
    m = tf.stack([m0, m1], axis=1)

    return m


def mat2sshr(m: glm.mat2) -> glm.vec4:
    """Converts a 2d transformation matrix into an sshr tuple.

    An sshr tuple (sx,sy,h,r) represents the scale2d(sx,sy) shear2d(h) rotate2d(r) transformation.

    Formula::

        [[a0, a1], [a2, a3]] = m  # row-major
        sy = hypot(a2,a3)
        r = atan2(a2,a3)
        sx = det(A)/sy
        h = (a0*a2 + a1*a3)/(sx*r)


    Parameters
    ----------
    m : glm.mat2
        the input 2d transformation matrix

    Returns
    -------
    sshr : glm.vec4
        the output sshr tuple

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not really, cheeky MT is trying to advertise his paper!)
    """

    a0 = m[0, 0]
    a1 = m[1, 0]
    a2 = m[0, 1]
    a3 = m[1, 1]

    sy = glm.length(glm.vec2(a2, a3))
    if sy == 0:  # degenerate case, assume r = 0
        r = 0
        sx = a0
        h = 0 if a0 == 0 else a1 / a0
    else:
        r = glm.atan2(a2, a3)
        sx = glm.determinant(m) / sy
        if sx == 0:  # degenerate case, assume h = 0
            h = 0
        elif glm.abs(a2) < glm.abs(a3):  # use a1
            h = (a1 * sy / sx + a2) / a3
        else:  # use a0
            h = (a0 * sy / sx - a3) / a2

    return glm.vec4(sx, sy, h, r)


def mat2sshr_tf(tensor):
    """Converts an array of 2x2 transformation matrices into an array of sshr tuples.

    An sshr tuple (sx,sy,h,r) represents the scale2d(sx,sy) shear2d(h) rotate2d(r) transformation.

    Formula::

        [[a0, a1], [a2, a3]] = m
        sy = hypot(a2,a3)
        r = atan2(a2,a3)
        sx = det(A)/sy
        h = (a0*a2 + a1*a3)/(sx*r)


    Parameters
    ----------
    tensor : tensorflow.Tensor
        a tensor of shape (batch, 2, 2) containing 2d row-major transformation matrices

    Returns
    -------
    tensorflow.Tensor
        a tensor of shape (batch, 4) containing sshr tuples

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not really, cheeky MT is trying to advertise his paper!)
    """

    from mt import tf

    a0 = tensor[:, 0, 0]
    a1 = tensor[:, 0, 1]
    a2 = tensor[:, 1, 0]
    a3 = tensor[:, 1, 1]

    sy = tf.experimental.numpy.hypot(a2, a3)
    r = tf.math.atan2(a2, a3)
    sx = tf.math.divide_no_nan(a0 * a3 - a1 * a2, sy)
    h = tf.math.divide_no_nan(a0 * a2 + a1 * a3, sx * r)

    return tf.stack([sx, sy, h, r], axis=1)


def make_affine(mat2d_tensor, ofs2d_tensor):
    """Makes an array of 2d affine transformation matrices (in 3x3 with `[0,0,1]` as the 3rd row).

    Parameters
    ----------
    mat2d_tensor : tensorflow.Tensor
        a tensor of shape (batch, 2, 2) containing 2d row-major transformation matrices
    ofs2d_tensor : tensorflow.Tensor
        a tensor of shape (batch, 2) containing 2d translations

    Returns
    -------
    tensorflow.Tensor
        a tensor of shape (batch, 3, 3) containing 2d affine transformation matrices with the
        linear and translation parts defined in the input tensors
    """

    from mt import tf

    zero_tensor = tf.zeros_like(mat2d_tensor[:, :1, :])
    col12 = tf.concat([mat2d_tensor, zero_tensor], axis=1)
    one_tensor = tf.ones_like(ofs2d_tensor[:, :1])
    col3 = tf.concat([ofs2d_tensor, one_tensor], axis=1)
    tensor = tf.concat([col12, tf.expand_dims(col3, axis=-1)], axis=2)
    return tensor
