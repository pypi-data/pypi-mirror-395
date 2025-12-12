from mt import np
import mt.base.casting as _bc

from .affine import Aff
from .dilated_isometry import Dliso


__all__ = ['Iso']


class Iso(Dliso):
    '''Isometry = orthogonal transformation followed by translation.

    An isometry is a (Euclidean-)metric-preserving transformation. In other words, it is an affine transformation but the linear part is a unitary matrix.

    References:
        [1] Pham et al, Distances and Means of Direct Similarities, IJCV, 2015. (not true but cheeky MT is trying to advertise his paper!)
    '''

    # ----- base adaptation -----

    @property
    def scale(self):
        return 1
    scale.__doc__ = Dliso.scale.__doc__

    @scale.setter
    def scale(self, scale):
        raise TypeError("Scale value is read-only.")

    @property
    def linear(self):
        '''Returns the linear part of the affine transformation matrix of the isometry.'''
        return self.unitary

    # ----- methods -----

    def __init__(self, offset=np.zeros(2), unitary=np.identity(2)):
        self.offset = offset
        self.unitary = unitary

    def __repr__(self):
        return "Iso(offset={}, unitary_diagonal={})".format(self.offset, self.unitary.diagonal())

    # ----- base adaptation -----

    def multiply(self, other):
        if not isinstance(other, Iso):
            return super(Iso, self).__mul__(other)
        return Iso(offset=self << other.offset, unitary=np.dot(self.unitary, other.unitary))
    multiply.__doc__ = Dliso.multiply.__doc__

    def invert(self):
        invUnitary = np.linalg.inv(self.unitary) # slow, and assuming the unitary matrix is invertible
        return Iso(offset=np.dot(invUnitary, -self.offset), unitary=invUnitary)
    invert.__doc__ = Dliso.invert.__doc__


# ----- casting -----


_bc.register_cast(Iso, Dliso, lambda x: Dliso(offset=x.offset, unitary=x.unitary))
_bc.register_cast(Iso, Aff, lambda x: Aff(bias=x.offset, weight=x.weight))
