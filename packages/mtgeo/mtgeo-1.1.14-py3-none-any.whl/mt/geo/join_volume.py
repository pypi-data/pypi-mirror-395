'''Registry to store all the functions to join the interior volumes of two geometric objects in the same space.'''


__all__ = ['join_volume', 'register_join_volume']


# map: (type1, type2) -> join_volume function
_join_volume_registry = {}


def join_volume(obj1, obj2):
    '''Joins the interior volumes of two geometric objects in the same space.

    Parameters
    ----------
    obj1 : object
        first object to join
    obj2 : object
        second object to join

    Returns
    -------
    intersection_volume : float
        the volume of the intersection of the two objects' interior regions
    obj1_only_volume : float
        the volume of the interior of obj1 that does not belong to obj2
    obj2_only_volume : float
        the volume of the interior of obj2 that does not belong to obj1
    union_volume : float
        the volume of the union of the two objects' interior regions

    Raises
    ------
    NotImplementedError
        if the join_volume function has not been registered using function `register_join_volume`
    '''
    key = (type(obj1), type(obj2))
    if key in _join_volume_registry:
        return _join_volume_registry[key](obj1, obj2)
    raise NotImplementedError("Join_volume function between type {} and type {} not found.".format(key[0], key[1]))


def register_join_volume(type1, type2, func):
    '''Registers a function to join_volume an object of type A and object of type B.

    Parameters
    ----------
    type1 : type
        type or class of the first object to join_volume
    type2 : type
        type or class of the second object to join_volume
    func : function
        join_volume function to register
    '''

    key = (type1, type2)
    if key in _join_volume_registry:
        raise SyntaxError("Join_Volumeimate function from type {} to type {} has been registered before.".format(type1, type2))
    _join_volume_registry[key] = func
