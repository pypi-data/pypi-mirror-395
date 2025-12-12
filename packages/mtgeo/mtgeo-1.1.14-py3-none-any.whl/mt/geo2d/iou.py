'''Intersection over Union. In the current primitive form, it is treated as a separate module.'''


from ..geond.iou import iou_impl


__all__ = ['iou']


def iou(geo2d_obj1, geo2d_obj2):
    '''Computes the Intersection-over-Union ratio of two (sets of non-overlapping) 2D geometry objects. Right now we only accept Rect and Polygon.

    Parameters
    ----------
    geo2d_obj1 : Rect or Polygon or list of non-overlapping geometric objects of these types
        the first 2D geometry object
    geo2d_obj2 : Rect or Polygon or list of non-overlapping geometric objects of these types
        the second 2D geometry object

    Returns
    -------
    float
        the IoU ratio of the two objects, regardless of whether they are sepcified in clockwise or counter-clockwise order
    '''
    # make sure each object is a list
    inputs = [obj if isinstance(obj, list) else [obj] for obj in [geo2d_obj1, geo2d_obj2]]

    # compute moments
    sum_left = 0
    sum_right = 0
    sum_inner = 0
    for obj1 in inputs[0]:
        for obj2 in inputs[1]:
            sum_left += obj1.shapely.area
            sum_right += obj2.shapely.area
            sum_inner += obj1.shapely.intersection(obj2.shapely).area

    # result
    return iou_impl(sum_inner, sum_left, sum_right)
