from mt import np
from mt.base.deprecated import deprecated_func
from mt.base.casting import cast, register_cast

from ..geo import GeometricObject, approx, register_approx
from .dilated_translation import Dltra
from .hyperbox import Hyperbox

__all__ = ['Hypercube']

class Hypercube(GeometricObject):
    '''Axis-aligned n-dimensional hypercube.

    An axis-aligned n-dimensional hypercube is defined as the set of points of the hypercube [-1,1]^n transformed by a dilated translation.

    Parameters
    ----------
    offset_or_dltra : 1d array or Dltra
        array of coordinate values of the center of the hypercube or the dilated translation itself.
    scale : float
        if the first argument is an offset, this argument specifies the uniform scale

    Attributes
    ----------
    dltra_tfm : Dlt
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
    '''

    # ----- data encapsulation -----

    @property
    def dltra_tfm(self):
        '''the dilatation'''
        return self.__dltra_tfm

    @dltra_tfm.setter
    def dltra_tfm(self, dltra_tfm):
        self.__dltra_tfm = dltra_tfm

    # ----- derived properties -----

    @classmethod
    def ndim(self):
        '''The dimensionality'''
        return self.dim

    @property
    def dim(self):
        '''The dimensionality'''
        return self.dltra_tfm.dim

    @property
    def minus_pt(self):
        '''The (-1,)^n point after being transformed by the dilatation.'''
        return self.dltra_tfm.offset - self.dltra_tfm.scale

    @property
    def plus_pt(self):
        '''The (+1,)^n point after being transformed by the dilatation.'''
        return self.dltra_tfm.offset + self.dltra_tfm.scale

    @property
    def min_coords(self):
        '''minimum coordinates'''
        return self.minus_pt if self.dltra_tfm.scale >= 0 else self.plus_pt

    @property
    def max_coords(self):
        '''maximum coordinates'''
        return self.plus_pt if self.dltra_tfm.scale >= 0 else self.minus_pt

    @property
    def center_pt(self):
        '''center point'''
        return self.dlt_tfm.offset

    @property
    def size(self):
        '''box size'''
        return np.abs(self.dlt_tfm.scale*2)

    # ----- methods -----

    def __init__(self, offset_or_dltra, scale=1):
        if isinstance(min_coords, Dltra):
            self.dltra_tfm = offset_or_dltra
        else:
            self.dltra_tfm = Dltra(offset=offset_or_dltra, scale=scale)

    def __repr__(self):
        return "Hypercube({})".format(self.dltra_tfm)


# ----- casting -----


register_cast(Hypercube, Hyperbox, lambda x: Hyperbox(cast(x.dltra_tfm, Dlt)))


# ----- approximation ------


register_approx(Hyperbox, Hypercube, lambda x: Hypercube(approx(x.dlt_tfm, Dltra)))
