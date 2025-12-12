'''A 3D box.'''

from mt import np
from mt.base.casting import *

from ..geo import ThreeD, register_approx, register_join_volume
from ..geond import EPSILON, Hyperbox
from .moments import Moments3d


__all__ = ['Box', 'cast_Hyperbox_to_Box', 'cast_Box_to_Moments3d', 'approx_Moments3d_to_Box']


class Box(ThreeD, Hyperbox):
    '''A 3D box.

    Note we do not care if the box is open or partially closed or closed.'''

    
    # ----- derived properties -----

    
    @property
    def min_x(self):
        '''lowest x-coordinate.'''
        return self.min_coords[0]

    @property
    def min_y(self):
        '''lowest y-coodinate.'''
        return self.min_coords[1]

    @property
    def min_z(self):
        '''lowest z-coodinate.'''
        return self.min_coords[2]

    @property
    def max_x(self):
        '''highest x-coordinate.'''
        return self.max_coords[0]

    @property
    def max_y(self):
        '''highest y-coordinate.'''
        return self.max_coords[1]

    @property
    def max_z(self):
        '''highest z-coordinate.'''
        return self.max_coords[2]

    @property
    def x(self):
        '''left, same as min_x.'''
        return self.min_x

    @property
    def y(self):
        '''top, same as min_y.'''
        return self.min_y

    @property
    def z(self):
        '''top, same as min_z.'''
        return self.min_z

    @property
    def lx(self):
        '''length in x-axis'''
        return self.max_x - self.min_x

    @property
    def ly(self):
        '''length in y-axis'''
        return self.max_y - self.min_y

    @property
    def lz(self):
        '''length in z-axis'''
        return self.max_z - self.min_z

    @property
    def cx(self):
        '''Center x-coordinate.'''
        return (self.min_x + self.max_x)/2

    @property
    def cy(self):
        '''Center y-coordinate.'''
        return (self.min_y + self.max_y)/2

    @property
    def cz(self):
        '''Center z-coordinate.'''
        return (self.min_z + self.max_z)/2

    @property
    def surface_area(self):
        '''Surface area.'''
        l = np.abs(self.max_coords.self.min_coords)
        return (l[0]*l[1]+l[1]*l[2]+l[2]*l[0])*2

    
    # ----- moments -----


    @property
    def moment_x(self):
        '''Returns the integral of x over the box's interior.'''
        return self.signed_volume*self.cx

    @property
    def moment_y(self):
        '''Returns the integral of y over the box's interior.'''
        return self.signed_volume*self.cy

    @property
    def moment_z(self):
        '''Returns the integral of z over the box's interior.'''
        return self.signed_volume*self.cz

    @property
    def moment_xy(self):
        '''Returns the integral of x*y over the box's interior.'''
        return self.moment_x*self.cy

    @property
    def moment_yz(self):
        '''Returns the integral of y*z over the box's interior.'''
        return self.moment_y*self.cz

    @property
    def moment_zx(self):
        '''Returns the integral of z*x over the box's interior.'''
        return self.moment_z*self.cx

    @property
    def moment_xx(self):
        '''Returns the integral of x*x over the box's interior.'''
        return self.signed_volume*(self.min_x*self.min_x+self.min_x*self.max_x+self.max_x*self.max_x)/3

    @property
    def moment_yy(self):
        '''Returns the integral of y*y over the box's interior.'''
        return self.signed_volume*(self.min_y*self.min_y+self.min_y*self.max_y+self.max_y*self.max_y)/3

    @property
    def moment_zz(self):
        '''Returns the integral of z*z over the box's interior.'''
        return self.signed_volume*(self.min_z*self.min_z+self.min_z*self.max_z+self.max_z*self.max_z)/3

    
    # ----- methods -----

    
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z, force_valid=False):
        super(Box, self).__init__(np.array([min_x, min_y, min_z]), np.array([max_x, max_y, max_z]), force_valid = force_valid)

    def __repr__(self):
        return "Box(x={}, y={}, z={}, lx={}, ly={}, lz={})".format(self.x, self.y, self.z, self.lx, self.ly, self.lz)

    def intersect(self, other):
        res = super(Box, self).intersect(other)
        return Box(res.min_coords[0], res.min_coords[1], res.min_coords[2], res.max_coords[0], res.max_coords[1], res.max_coords[2])

    def move(self, offset):
        '''Moves the Box by a given offset vector.'''
        return Box(self.min_x + offset[0], self.min_y + offset[1], self.min_z + offset[2], self.max_x + offset[0], self.max_y + offset[1], self.max_z + offset[2])


# ----- casting -----
        

register_cast(Box, Hyperbox, lambda x: Hyperbox(x.dlt_tfm))
register_castable(Hyperbox, Box, lambda x: x.dim==3)

def cast_Hyperbox_to_Box(x):
    '''Casts a Hyperbox to a Box.'''
    min_coords = x.min_coords
    max_coords = x.max_coords
    return Box(min_coords[0], min_coords[1], min_coords[2], max_coords[0], max_coords[1], max_coords[2])
register_cast(Hyperbox, Box, cast_Hyperbox_to_Box)


def cast_Box_to_Moments3d(obj):
    m0 = obj.signed_volume
    m1 = [obj.moment_x, obj.moment_y]
    mxy = obj.moment_xy
    myz = obj.moment_yz
    mzx = obj.moment_zx
    m2 = [[obj.moment_xx, mxy, mzx], [mxy, obj.moment_yy, myz], [mzx, myz, obj.moment_zz]]
    return Moments3d(m0, m1, m2)
register_cast(Box, Moments3d, cast_Box_to_Moments3d)


# ----- approximation -----


def approx_Moments3d_to_Box(obj):
    '''Approximates a Moments3d instance with a box such that the mean aligns with the box's center, and the covariance matrix of the instance is closest to the moment convariance matrix of the box.'''
    raise NotImplementedError("I don't know if the coefficients are correct. Need to figure out.")
register_approx(Moments3d, Box, approx_Moments3d_to_Box)


# ----- joining volumes -----


def join_volume_Box_and_Box(obj1, obj2):
    '''Joins the volumes of two Boxes.

    Parameters
    ----------
    obj1 : Box
        the first box
    obj2 : Box
        the second box

    Returns
    -------
    intersection_volume : float
        the volume of the intersection of the two boxes' interior regions
    obj1_only_volume : float
        the volume of the interior of obj1 that does not belong to obj2
    obj2_only_volume : float
        the volume of the interior of obj2 that does not belong to obj1
    union_volume : float
        the volume of the union of the two boxes' interior regions
    '''
    inter = obj1.intersect(obj2)
    inter_volume = inter.volume
    obj1_volume = obj1.volume
    obj2_volume = obj2.volume
    return (inter_volume, obj1_volume - inter_volume, obj2_volume - inter_volume, obj1_volume + obj2_volume - inter_volume)
register_join_volume(Box, Box, join_volume_Box_and_Box)
