'''Base tools to represent a geometric transformer and the act of transforming geometric objects (transformation).'''


from inspect import getmro

from .object import GeometricObject


__all__ = ['transform', 'transformable', 'register_transform', 'register_transformable', 'Transformer', 'InvertibleTransformer', 'LieTransformer']


# map: (tfm_type, obj_type) -> transform function
_transform_registry = {}

_transformable_registry = {}
# map: (tfm_type, obj_type) -> transformable function


def transformable(tfm, obj):
    '''Checks if an object can be transformed using a transformer.

    Parameters
    ----------
    tfm : Transformer
        a transformer
    obj : object
        object to transform from

    Returns
    -------
    bool
        whether or not the object is transformable using the transformer

    Raises
    ------
    NotImplementedError
        if the transformable function has not been registered using functions `register_transformable` or `register_transform`
    '''
    tfm_type = type(tfm)
    obj_type = type(obj)
    for cur_type in getmro(tfm_type): # go through every base class, in method resolution order
        key = (cur_type, obj_type)
        if key in _transformable_registry:
            return _transformable_registry[key](tfm, obj)
        if key in _transform_registry:
            return True
    return False


def transform(tfm, obj):
    '''Transforms an object using a given transformer.

    Parameters
    ----------
    tfm : GeometricObject
        the transformer. It must contain the Transformer mixin.
    obj : GeometricObject
        object to transform from

    Returns
    -------
    object
        the transformed version of `obj`

    Raises
    ------
    NotImplementedError
        if the approx function has not been registered using function `register_transform`
    '''
    obj_type = type(obj)
    for cur_type in getmro(type(tfm)): # go through every base class, in method resolution order
        key = (cur_type, obj_type)
        if key in _transform_registry:
            return _transform_registry[key](tfm, obj)
    raise NotImplementedError("Transformer {} has no function to transform object {}.".format(tfm, obj))


def register_transform(tfm_type, obj_type, func):
    '''Registers a function to transform an object of a given type using a transformer of a given type.

    Parameters
    ----------
    tfm_type : type
        type or class of the transformer
    obj_type : type
        type or class of the object to transform from
    func : function
        transform function `f(tfm, obj) -> obj` to register
    '''

    key = (tfm_type, obj_type)
    if key in _transform_registry:
        raise SyntaxError("Transform function using transformer type {} applying to object type {} has been registered before.".format(tfm_type, obj_type))
    _transform_registry[key] = func


def register_transformable(tfm_type, obj_type, func):
    '''Registers a function to check if we can transform an object of a given type using a transformer of another given type.

    Parameters
    ----------
    tfm_type : type
        type or class of the transformer
    obj_type : type
        type or class of the object to transform from
    func : function
        transformable function `f(tfm_type, obj) -> bool` to register
    '''

    key = (tfm_type, obj_type)
    if key in _transformable_registry:
        raise SyntaxError("Transformable function using transformer type {} applying to object type {} has been registered before.".format(tfm_type, obj_type))
    _transformable_registry[key] = func



class Transformer(object):
    '''A mixin asserting that this is a class of transformers.

    A transformer is an object capable of transforming geometric objects of certain types into other geometric objects. It is usually parametrised by a transformation matrix. The mixin assumes that the act of transforming an object using the inheriting class is conducted via calling the global `transform` function. The mixin overloads the left shift operator.
    '''
    
    # ----- operators -----
    
    def __lshift__(self, obj):
        '''Transforms an object or raise a ValueError if the object is not transformable by the transformer.'''
        if not transformable(self, obj):
            raise ValueError("Object {} cannot by transformed by transformer type {}".format(obj, type(self)))
        return transform(self, obj)


class InvertibleTransformer(Transformer):
    '''A mixin asserting that this is a class of invertible transformers. 

    The mixin assumes that a function `self.invert()` to return the inverted transformer has been implemented. It further overloads the right shift operator and the inverse operator.
    '''

    # ----- abstract -----
    
    def invert(self):
        '''Inverses the transformer'''
        raise NotImplementedError("You must implement the function {}.invert().".format(type(self)))

    # ----- operators -----
    
    def __rshift__(self, obj):
        '''Inversely transforms an object or raises a ValueError if the object is not transformable by the transformer.'''
        return (~self) << obj

    def __invert__(self):
        '''Returns the inverted transformer, invoking a given function `self.invert()`.'''
        return self.invert()

class LieTransformer(InvertibleTransformer):
    '''A mixin asserting that this is a class of transformers living in a Lie group, supporting the associative multiplication operator and the inversion operator. 

    Beside being an invertible transformer, the mixin additionally assumes that a function `self.multiply(other)` implementing the multiplication operator is available. It further overloads the multiplication, true division and modular operators, and provides a conjugate function.
    '''
    
    # ----- abstract -----
    
    def multiply(self, other):
        '''Multiplies the transformer with another transformer.'''
        raise NotImplementedError("You must implement the function {}.multiply().".format(type(self)))

    # ----- operators -----
    
    def __mul__(self, other):
        '''a*b = Lie operator'''
        return self.multiply(other)

    def __truediv__(self, other):
        '''a/b = a*(~b)'''
        return self*(~other)

    def __mod__(self, other):
        '''a%b = (~a)*b'''
        return (~self)*other

    def conjugate(self, other):
        '''Conjugate: `self.conjugate(other) = self*other*self^{-1}`'''
        return self*(other/self)
