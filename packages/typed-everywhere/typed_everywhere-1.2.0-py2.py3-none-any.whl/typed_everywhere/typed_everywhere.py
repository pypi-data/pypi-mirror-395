import typing
import typeguard
import wrapt


class Typed(wrapt.AutoObjectProxy, typing.Generic[typing.TypeVar("T")]):
    class_id = "typed_everywhere.Typed"

    def __object_proxy__(self, wrapped):
        return Typed(wrapped)

    def __init__(self, wrapped):
        super().__init__(wrapped)
        self._self_type = type(wrapped)
        
    def _assign_(self, value, *annotation):
        if hasattr(value, "class_id") and value.class_id == "typed_everywhere.Typed":
            value = value.__wrapped__        
        self.__wrapped__ = value
        if not issubclass(type(value), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value)}")
        return self

    def __iadd__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__
        value = super().__iadd__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __isub__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__isub__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __imul__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__imul__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __itruediv__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__itruediv__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __ifloordiv__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__ifloordiv__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __imod__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__imod__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __ipow__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__ipow__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __ilshift__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__ilshift__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __irshift__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__irshift__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __iand__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__iand__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __ixor__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__ixor__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __ior__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__                        
        value = super().__ior__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value

    def __imatmul__(self, other):
        if hasattr(other, "class_id") and other.class_id == "typed_everywhere.Typed":
            other = other.__wrapped__           
        value = super().__imatmul__(other)
        if not issubclass(type(value.__wrapped__), self._self_type):
            raise TypeError(f"Expected an instance of {self._self_type} but received an instance of {type(value.__wrapped__)}")        
        return value


class Descriptor:
    def __init__(self, value, name):
        self.value = value
        self.name = name
        self.values = {}

    def __get__(self, instance, owner = None):
        if instance is not None:
            if instance in self.values:
                return self.values[instance]
            else:
                return self.value.__get__(instance, owner = owner)
        else:
            outer_self = self
            orig_assign = type(self.value)._assign_
            def _assign_(self, value, *annotation):
                orig_assign(self, value, *annotation)
                type(self)._assign_ = orig_assign
                return owner.__dict__[outer_self.name]
            if type(self.value)._assign_.__code__ != _assign_.__code__:
                type(self.value)._assign_ = _assign_
            return self.value

    def __set__(self, instance, value):
        self.values[instance] = value

    def __delete__(self, instance):
        try:
            del self.values[instance]
        except KeyError:
            raise AttributeError(f"'{type(instance).__name__}' object has no attribute '{self.name}'")


def typed_method(func):
    return Typed(Descriptor(Typed(func), func.__code__.co_name))


def check_typed_value(value, origin_type, args, memo):
    if not issubclass(type(value), Typed):
        raise typeguard.TypeCheckError("is not a Typed instance")
    if not args:
        return
    inner_type = args[0]
    try:
        typeguard.check_type_internal(value.__wrapped__, inner_type, memo)
    except typeguard.TypeCheckError:
        raise typeguard.TypeCheckError(f"doesn't wrap an instance of {inner_type}")


def typed_lookup(origin_type, args, extras):
    if origin_type is Typed:
        return check_typed_value
    return None


typeguard.checker_lookup_functions.append(typed_lookup)
typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS
