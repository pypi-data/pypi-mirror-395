'''Registry to store all the functions to upper-bound and lower-bound a geometric object of type A with an object of type B.'''


__all__ = ['upper_bound', 'upper_boundable', 'register_upper_bound', 'register_upper_boundable', 'lower_bound', 'lower_boundable', 'register_lower_bound', 'register_lower_boundable']


# ----- upper-bound functions -----


# map: (src_type, dst_type) -> upper-bound function
_upper_bound_registry = {}

_upper_boundable_registry = {}
# map: (src_type, dst_type) -> upper-boundable function


def upper_boundable(obj, dst_type):
    '''Checks if an object can be upper-bounded to a target type.

    Parameters
    ----------
    obj : object
        object to upper-bound
    dst_type : type
        type or class to upper-bound to

    Returns
    -------
    bool
        whether or not the object is upper-boundable to `dst_type`

    Raises
    ------
    NotImplementedError
        if the upper-boundable function has not been registered using functions `register_upper_boundable` or `register_upper_bound`
    '''
    key = (type(obj), dst_type)
    if key in _upper_boundable_registry:
        return _upper_boundable_registry[key](obj)
    return key in _upper_bound_registry


def upper_bound(obj, dst_type):
    '''Upper-bounds an object to a target type.

    Parameters
    ----------
    obj : object
        object to upper-bound
    dst_type : type
        type or class to upper-bound to

    Returns
    -------
    object
        the upper-bounded version of `obj`

    Raises
    ------
    NotImplementedError
        if the upper-bound function has not been registered using function `register_upper_bound`
    '''
    key = (type(obj), dst_type)
    if key in _upper_bound_registry:
        return _upper_bound_registry[key](obj)
    raise NotImplementedError("Upper-bound function from type {} to type {} not found.".format(key[0], key[1]))


def register_upper_bound(src_type, dst_type, func):
    '''Registers a function to upper-bound an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to upper-bound from
    dst_type : type
        type or class to upper-bound to
    func : function
        upper-bound function to register
    '''

    key = (src_type, dst_type)
    if key in _upper_bound_registry:
        raise SyntaxError("Upper-bound function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _upper_bound_registry[key] = func


def register_upper_boundable(src_type, dst_type, func):
    '''Registers a function to check if we can upper-bound an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to upper-bound from
    dst_type : type
        type or class to upper-bound to
    func : function
        upper-boundable function to register
    '''

    key = (src_type, dst_type)
    if key in _upper_boundable_registry:
        raise SyntaxError("Upper-boundable function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _upper_boundable_registry[key] = func


# ----- upper-bound functions -----


# map: (src_type, dst_type) -> lower-bound function
_lower_bound_registry = {}

_lower_boundable_registry = {}
# map: (src_type, dst_type) -> lower-boundable function


def lower_boundable(obj, dst_type):
    '''Checks if an object can be lower-bounded to a target type.

    Parameters
    ----------
    obj : object
        object to lower-bound
    dst_type : type
        type or class to lower-bound to

    Returns
    -------
    bool
        whether or not the object is lower-boundable to `dst_type`

    Raises
    ------
    NotImplementedError
        if the lower-boundable function has not been registered using functions `register_lower_boundable` or `register_lower_bound`
    '''
    key = (type(obj), dst_type)
    if key in _lower_boundable_registry:
        return _lower_boundable_registry[key](obj)
    return key in _lower_bound_registry


def lower_bound(obj, dst_type):
    '''Lower-bounds an object to a target type.

    Parameters
    ----------
    obj : object
        object to lower-bound
    dst_type : type
        type or class to lower-bound to

    Returns
    -------
    object
        the lower-bounded version of `obj`

    Raises
    ------
    NotImplementedError
        if the lower-bound function has not been registered using function `register_lower_bound`
    '''
    key = (type(obj), dst_type)
    if key in _lower_bound_registry:
        return _lower_bound_registry[key](obj)
    raise NotImplementedError("Lower-bound function from type {} to type {} not found.".format(key[0], key[1]))


def register_lower_bound(src_type, dst_type, func):
    '''Registers a function to lower-bound an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to lower-bound from
    dst_type : type
        type or class to lower-bound to
    func : function
        lower-bound function to register
    '''

    key = (src_type, dst_type)
    if key in _lower_bound_registry:
        raise SyntaxError("Lower-bound function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _lower_bound_registry[key] = func


def register_lower_boundable(src_type, dst_type, func):
    '''Registers a function to check if we can lower-bound an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to lower-bound from
    dst_type : type
        type or class to lower-bound to
    func : function
        lower-boundable function to register
    '''

    key = (src_type, dst_type)
    if key in _lower_boundable_registry:
        raise SyntaxError("Lower-boundable function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _lower_boundable_registry[key] = func
