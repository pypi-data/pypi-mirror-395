'''Registry to store all the approximations functions to approximate a geometric object from type A to type B.'''


__all__ = ['approx', 'approximable', 'register_approx', 'register_approximable']


# map: (src_type, dst_type) -> approx function
_approx_registry = {}

_approximable_registry = {}
# map: (src_type, dst_type) -> approximable function


def approximable(obj, dst_type):
    '''Checks if an object can be approximated to a target type.

    Parameters
    ----------
    obj : object
        object to approximate
    dst_type : type
        type or class to approx to

    Returns
    -------
    bool
        whether or not the object is approximable to `dst_type`

    Raises
    ------
    NotImplementedError
        if the approximable function has not been registered using functions `register_approximable` or `register_approx`
    '''
    key = (type(obj), dst_type)
    if key in _approximable_registry:
        return _approximable_registry[key](obj)
    return key in _approx_registry


def approx(obj, dst_type):
    '''Approximates an object to a target type.

    Parameters
    ----------
    obj : object
        object to approximate
    dst_type : type
        type or class to approx to

    Returns
    -------
    object
        the approx version of `obj`

    Raises
    ------
    NotImplementedError
        if the approx function has not been registered using function `register_approx`
    '''
    key = (type(obj), dst_type)
    if key in _approx_registry:
        return _approx_registry[key](obj)
    raise NotImplementedError("Approximate function from type {} to type {} not found.".format(key[0], key[1]))


def register_approx(src_type, dst_type, func):
    '''Registers a function to approximate an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to approximate from
    dst_type : type
        type or class to approximate to
    func : function
        approx function to register
    '''

    key = (src_type, dst_type)
    if key in _approx_registry:
        raise SyntaxError("Approximate function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _approx_registry[key] = func


def register_approximable(src_type, dst_type, func):
    '''Registers a function to check if we can approximate an object from type A to type B.

    Parameters
    ----------
    src_type : type
        type or class to approximate from
    dst_type : type
        type or class to approximate to
    func : function
        approximable function to register
    '''

    key = (src_type, dst_type)
    if key in _approximable_registry:
        raise SyntaxError("Approximable function from type {} to type {} has been registered before.".format(src_type, dst_type))
    _approximable_registry[key] = func
