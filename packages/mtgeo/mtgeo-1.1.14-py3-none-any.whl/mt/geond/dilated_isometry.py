import math as _m
from mt import np
import mt.base.casting as _bc
from ..geo.approximation import register_approx
from .affine import Aff


__all__ = ['Dliso', 'approx_Aff_to_Dliso']


class Dliso(Aff):
    '''Dilated isometry = Isometry following a uniform scaling.

    An isometry is a (Euclidean-)metric-preserving transformation. In other words, it is an affine transformation but the linear part is a unitary matrix.

    References
    ----------
    .. [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not true but cheeky MT is trying to advertise his paper!)
    '''

    # ----- base adaptation -----

    @property
    def bias(self):
        return self.__offset
    bias.__doc__ = Aff.bias.__doc__

    @bias.setter
    def bias(self, bias):
        if len(bias.shape) != 1:
            raise ValueError("Bias is not a vector, shape {}.".format(bias.shape))
        self.__offset = bias

    @property
    def bias_dim(self):
        return self.__offset.shape[0]
    bias_dim.__doc__ = Aff.bias_dim.__doc__

    @property
    def weight(self):
        return self.linear
    weight.__doc__ = Aff.weight.__doc__

    @weight.setter
    def weight(self, weight):
        raise TypeError("Weight matrix is read-only.")

    @property
    def weight_shape(self):
        return self.__unitary.shape
    weight_shape.__doc__ = Aff.weight_shape.__doc__

    # ----- data encapsulation -----

    @property
    def offset(self):
        '''The offset/bias part of the dilated isometry.'''
        return self.__offset

    @offset.setter
    def offset(self, offset):
        if len(offset.shape) != 1:
            raise ValueError("Offset is not a vector, shape {}.".format(offset.shape))
        self.__offset = offset

    @property
    def scale(self):
        '''The scale component/scalar of the dilated isometry.'''
        return self.__scale

    @scale.setter
    def scale(self, scale):
        if not scale > 0:
            raise ValueError("Scale is not positive {}.".format(scale))
        self.__scale = scale

    @property
    def unitary(self):
        '''The unitary matrix of the dilated isometry.'''
        return self.__unitary

    @unitary.setter
    def unitary(self, unitary):
        if len(unitary.shape) != 2:
            raise ValueError("Unitary is not a matrix of, shape {} given.".format(unitary.shape))
        self.__unitary = unitary

    # ----- derived properties -----

    @property
    def linear(self):
        '''Returns the linear part of the affine transformation matrix of the dilated isometry.'''
        return self.unitary*self.scale

    # ----- methods -----

    def __init__(self, offset=np.zeros(2), scale=1, unitary=np.identity(2)):
        self.offset = offset
        self.scale = scale
        self.unitary = unitary

    def __repr__(self):
        return "Dliso(offset={}, scale={}, unitary_diagonal={})".format(self.offset, self.scale, self.unitary.diagonal())

    # ----- base adaptation -----

    def multiply(self, other):
        if not isinstance(other, Dliso):
            return super(Dliso, self).multiply(other)
        return Dliso(self << other.offset,
            self.scale*other.scale,
            np.dot(self.unitary, other.unitary)
            )
    multiply.__doc__ = Aff.multiply.__doc__

    def invert(self):
        invScale = 1/self.scale
        invUnitary = np.linalg.inv(self.unitary) # slow, and assuming the unitary matrix is invertible
        return Dliso(np.dot(invUnitary, -self.offset*invScale), invScale, invUnitary)
    invert.__doc__ = Aff.invert.__doc__


# ----- casting -----


def approx_Aff_to_Dliso(obj):
    '''Approximates an Aff instance with a Dliso.'''
    ndom = obj.ndim
    U, S, VT = np.linalg.svd(obj.linear, full_matrices=True)
    if len(S) < ndim or S[ndim-1] == 0:
        return Dliso(offset=obj.bias, scale=0, unitary=np.identity(ndim))
    
    scale = _m.pow(S.prod(), 1/obj.ndim)
    return Dliso(offset=obj.bias, scale=scale, unitary=U@VT)


_bc.register_cast(Dliso, Aff, lambda x: Aff(weight=x.weight, bias=x.offset, check_shapes=False))
register_approx(Aff, Dliso, approx_Aff_to_Dliso)
