
'''A 2D rotated rectangle.'''

import math

from mt import np
from mt.base.casting import *

from ..geo import GeometricObject, TwoD, register_approx, transform, register_join_volume
from .moments import Moments2d
from .affine import originate2d, rotate2d, scale2d, translate2d
from .rect import Rect
from .polygon import Polygon
from .shapely import HasShapely, join_volume_shapely


__all__ = ['RRect', 'cast_RRect_to_Moments2d', 'approx_Moments2d_to_RRect']


class RRect(HasShapely, TwoD, GeometricObject):
    '''A 2D rotated rectangle.

    An RRect represents a 2D axis-aligned rectangle rotated by an angle. It is parametrised by
    center point, signed width, height and angle. Internally, an affine transformation is computed
    that transforms the unit square '[0,0,1,1]' to the rotated rectangle. Signed width cannot be
    zero and height must be positive. Angle is in radian. Note that we do not care if the rectangle
    is open or partially closed or closed.

    Parameters
    ----------
    signed_width : float
        the signed width, meaning normal width if positive or width with left-right flipping if
        negative
    height : float
        the height
    cx : float
        the x-coordinate of the rectangle's centroid
    cy : float
        the y-coordinate of the rectangle's centroid
    angle : float
        the angle (in radian) at which the rectangle is rotated, the rotation direction is in
        the standard convention, from x-axis to y-axis

    Attributes
    ----------
    width : float
        the actual (positive) width
    center_pt : point
        the rectangle's centroid
    tl : point
        the transform of point (0,0)
    br : point
        the transform of point (1,1)
    tr : point
        the transform of point (0,1)
    bl : point
        the transform of point (1,0)
    tfm : mt.geo2d.Aff2d
        the 2D affine transformation turning unit square [0,0,1,1] into the given rectangle
    corners : numpy.ndarray
        the four corners [tl,tr,bl,br] above
    area : float
        the area
    circumference : float
        the circumference
    sign : {-1,0,1,nan}
        the sign of the rectangle
    signed_area : float
        the signed area

    Notes
    -----

    For more details, see `this page <https://structx.com/Shape_Formulas_033.html>`_. But note that
    we primarily use CV convention for images, top left is (0,0).
    '''

    
    # ----- internal representations -----


    @property
    def shapely(self):
        '''Shapely representation for fast intersection operations.'''
        if not hasattr(self, '_shapely'):
            import shapely.geometry as _sg
            points = self.corners[[0,1,3,2] if self.signed_width >= 0 else [2,3,1,0]]
            self._shapely = _sg.Polygon(points)
            self._shapely = self._shapely.buffer(0.0001) # to clean up any (multi and/or non-simple) polygon into a simple polygon
        return self._shapely


    # ----- derived properties -----


    @property
    def width(self):
        '''The actual (positive) width.'''
        return abs(self.signed_width)
    
    @property
    def tl(self):
        '''The transform of point (0,0).'''
        return self.corners[0]

    @property
    def br(self):
        '''The transform of point (1,1).'''
        return self.corners[3]

    @property
    def tr(self):
        '''The transform of point (1,0).'''
        return self.corners[1]

    @property
    def bl(self):
        '''The transform of point (0,1).'''
        return self.corners[2]

    @property
    def sign(self):
        return np.sign(self.signed_width)

    @property
    def area(self):
        '''Absolute area.'''
        return abs(self.signed_width*self.height)

    @property
    def circumference(self):
        '''Circumference.'''
        return (self.width+self.height)*2


    # ---- interior squares ----


    def left_square(self):
        '''The interior square attaching to the left edge.'''

        if self.width < self.height:
            raise ValueError("The left square does not exist because width is less than height.")

        tl = self.tl
        bl = self.bl
        br = self.br

        v = br - bl
        br2 = bl + v*abs(self.height/self.width)
        cpt = (tl+br2)/2 # new center point

        return RRect(self.sign*self.height, self.height, cx=cpt[0], cy=cpt[1], angle=self.angle)


    def right_square(self):
        '''The interior square attaching to the right edge.'''

        if self.width < self.height:
            raise ValueError("The right square does not exist because width is less than height.")

        tr = self.tr
        br = self.br
        bl = self.bl

        v = bl - br
        bl2 = br + v*abs(self.height/self.width)
        cpt = (bl2+tr)/2 # new center point

        return RRect(self.sign*self.height, self.height, cx=cpt[0], cy=cpt[1], angle=self.angle)

    
    # ----- moments -----


    @property
    def signed_area(self):
        '''Signed area.'''
        return self.signed_width*self.height

    @property
    def moment1(self):
        '''First-order moment.'''
        return self.sign*self.center_pt

    @property
    def moment_x(self):
        '''Returns the integral of x over the rectangle's interior.'''
        return self.moment1[0]

    @property
    def moment_y(self):
        '''Returns the integral of y over the rectangle's interior.'''
        return self.moment1[1]

    @property
    def moment2(self):
        '''Second-order moment.'''
        if not hasattr(self, '_moment2'):
            # 2nd-order central moments if the rectangle were not rotated
            rx = self.signed_width/2
            ry = self.height/2
            r = Rect(-rx, -ry, rx, ry)
            Muu = r.moment_xx
            Muv = r.moment_xy
            Mvv = r.moment_yy

            # Rotate the central moments (a.k.a. moments of inertia):
            #   Original axes: x, y
            #   Rotated axes:  u, v
            #   Dst-to-src change-of-coordinates formulae:
            #     x =  c*u+s*v
            #     y = -s*u+c*v
            #   where c = cos(theta), s = sin(theta). Therefore,
            #     Mxx =  c*c*Muu +     2*c*s*Muv + s*s*Mvv
            #     Mxy = -c*s*Muu + (c*c-s*s)*Muv + c*s*Mvv
            #     Myy =  s*s*Muu +    -2*c*s*Muv + c*c*Mvv
            # Reference: `link <https://calcresource.com/moment-of-inertia-rotation.html>`_
            c = math.cos(self.angle)
            s = math.sin(self.angle)
            cc = c*c
            cs = c*s
            ss = s*s
            Mxx =  cc*Muu +    2*cs*Muv + ss*Mvv
            Mxy = -cs*Muu + (cc-ss)*Muv + cs*Mvv
            Myy =  ss*Muu -    2*cs*Muv + cc*Mvv

            # Shift the origin to where it should be:
            #   Axes from the rectangle center point: x, y
            #   Image axes: p, q
            #   Dst-to-src chang-of-coordinates formulae:
            #     p = x+cx
            #     q = y+cy
            #   Formulae:
            #     Mpp = Mxx + 2*cx*Mx       + cx*cx*M1
            #     Mpq = Mxy + cx*My + cy*Mx + cx*cy*M1
            #     Mqq = Myy + 2*cy*My       + cy*cy*M1
            #   where M1 is the signed area. But because the rectangle is symmetric, Mx = My = 0.
            cx = self.center_pt[0]
            cy = self.center_pt[1]
            M1 = self.signed_area
            Mpp = Mxx + cx*cx*M1
            Mpq = Mxy + cx*cy*M1
            Mqq = Myy + cy*cy*M1

            self._moment2 = np.array([[Mpp, Mpq], [Mpq, Mqq]])
        return self._moment2

    @property
    def moment_xy(self):
        '''Returns the integral of x*y over the rectangle's interior.'''
        return self.moment2[0][1]

    @property
    def moment_xx(self):
        '''Returns the integral of x*x over the rectangle's interior.'''
        return self.moment2[0][0]

    @property
    def moment_yy(self):
        '''Returns the integral of y*y over the rectangle's interior.'''
        return self.moment2[1][1]


    # ----- serialization -----


    def to_json(self):
        '''Returns a list [signed_width, height, cx, cy, angle].'''
        return [self.signed_width, self.height, self.cx, self.cy, self.angle]


    @staticmethod
    def from_json(json_obj):
        '''Creates a RRect from a JSON-like object.

        Parameters
        ----------
        json_obj : list
            list [signed_width, height, cx, cy, angle]

        Returns
        -------
        RRect
            output rotated rectangle
        '''
        return RRect(*json_obj)


    def to_tensor(self):
        '''Returns a tensor [signed_width, height, cx, cy, angle] representing the RRect .'''
        from mt import tf
        return tf.convert_to_tensor(self.to_json())

    
    # ----- methods -----

    
    def __init__(self, signed_width: float, height: float, cx: float = 0., cy: float = 0., angle: float = 0.):
        self.signed_width = signed_width
        self.height = height
        self.center_pt = np.array([cx, cy])
        self.angle = angle

        # compute the transformation
        tfm = translate2d(-0.5, -0.5) # shift the centroid of [0,0,1,1] to the origin
        tfm = scale2d(scale_x=signed_width, scale_y=height)*tfm # scale it along signed_width and height
        tfm = rotate2d(angle, 0., 0.)*tfm # rotate it
        tfm = translate2d(cx, cy)*tfm # now shift the centroid of the rotated rectangle to the target location
        self.tfm = tfm

        # transform the corners
        corners = np.array([[0,0],[1,0],[0,1],[1,1]]) # [tl, tr, bl, br]
        self.corners = transform(self.tfm, corners)


    def __repr__(self):
        return "RRect(signed_width=%r, height=%r, cx=%r, cy=%r, angle=%r)" % (self.signed_width, self.height, self.center_pt[0], self.center_pt[1], self.angle)


# ----- casting -----
        

def cast_RRect_to_Moments2d(obj):
    return Moments2d(obj.signed_area, obj.moment1, obj.moment2)
register_cast(RRect, Moments2d, cast_RRect_to_Moments2d)


# ----- approximation -----


def approx_Moments2d_to_RRect(obj):
    '''Approximates a Moments2d instance with a RRect such that the mean aligns with the RRect's center, and the covariance matrix of the instance is closest to the moment convariance matrix of the RRect.'''
    raise NotImplementedError("MT-TODO: to implement one day")
    #cx, cy = obj.mean
    #cov = obj.cov

    ## w = half signed_width, h = half height
    #size = abs(obj.m0)
    #hw3 = cov[0][0]*size*0.75 # should be >= 0
    #wh3 = cov[1][1]*size*0.75 # should be >= 0
    #wh = np.sqrt(np.sqrt(wh3*hw3))
    #h = np.sqrt(wh3/wh)
    #w = np.sqrt(hw3/wh)
    #return Rect(cx-w, cy-h, cx+w, cy+h)
register_approx(Moments2d, RRect, approx_Moments2d_to_RRect)


# ----- joining volumes -----


register_join_volume(Rect, RRect, join_volume_shapely)
register_join_volume(RRect, Rect, join_volume_shapely)
register_join_volume(Polygon, RRect, join_volume_shapely)
register_join_volume(RRect, Polygon, join_volume_shapely)
register_join_volume(RRect, RRect, join_volume_shapely)
