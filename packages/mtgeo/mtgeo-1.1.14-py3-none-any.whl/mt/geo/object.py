'''The base class to represent a geometric object.'''


__all__ = ['GeometricObject', 'TwoD', 'ThreeD']


class GeometricObject(object):
    '''A geometric object which lives in a d-dimensional Euclidean space.

    A GeometricObject is a geometric object which lives in a d-dimensional Euclidean space. It can be a point, a point set, a polygon, a circle, a sphere, a parallelogram, a paralleloid, etc. This class represents the base class, in which the only property available is `ndim`, telling the number of dimensions. The user needs to implement `ndim`, or use some mixin classes like `TwoD` or `ThreeD`.
    '''
    
    # ----- properties -----
    
    @property
    def ndim(self):
        '''Returns the number of dimensions in which the geometric object lives.'''
        raise NotImplementedError


class TwoD(object):
    '''Mixin to assert that the geometric object lives in 2D Euclidean space.'''

    @property
    def ndim(self):
        '''the dimensionality, which is 2'''
        return 2


class ThreeD(object):
    '''Mixin to assert that the geometric object lives in 3D Euclidean space.'''

    @property
    def ndim(self):
        '''the dimensionality, which is 3'''
        return 3
