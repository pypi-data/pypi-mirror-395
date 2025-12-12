# typed-everywhere
Runtime type checking and not only for function arguments and class variables but even for the ordinary local and global variables!

# Installation
```pip install typed-everywhere```

# How To Use
We have a proxy class:

_class_ typed_everywhere.**Typed**(wrapped)

_class_ @typed_everywhere.**Typed**(wrapped)

This class inherits a variant of [ObjectProxy](https://wrapt.readthedocs.io/en/master/wrappers.html#object-proxy) from wrapt.
Along with all augmented assignment operators, this class also overloads the normal assignment operator (=) thanks to [assign-overload](https://github.com/pyhacks/assign-overload).
_wrapped_ can be any object and the resulting instance of this class will act like _wrapped_ in every way.
If you use this class, you need to call typed_everywhere.**patch_and_reload_module**(). 
You can also access this function from assign_overload module.
You can find documentation about this function in [assign-overload](https://github.com/pyhacks/assign-overload).
Usage example:
```python
import typed_everywhere

def main():
    a = typed_everywhere.Typed(10)
    a = 20 # Ok
    print(a) # prints 20
    a = "abc" # Error

if typed_everywhere.patch_and_reload_module():
    main()
```
One thing to note is if you assign a variable holding a _Typed_ instance to a new variable, new variable takes the value of the _Typed_ instance, not the value of its underlying object.
However, most operators return the underlying object. Example:
```python
import typed_everywhere

def main():
    a = typed_everywhere.Typed(10)
    print(type(a+5)) # prints int
    b = a
    print(type(b)) # prints Typed

if typed_everywhere.patch_and_reload_module():
    main()
```
If you want to access the underlying object, use the ```__wrapped__``` attribute:
```python
import typed_everywhere

def main():
    a = typed_everywhere.Typed(10)
    b = a.__wrapped__
    print(type(b)) # prints int

if typed_everywhere.patch_and_reload_module():
    main()
```

_Typed_ is also compatible with [typeguard](https://typeguard.readthedocs.io/en/latest/). Function argument type enforcement example:
```python
import typeguard
import typed_everywhere

@typeguard.typechecked
def test4(a: typed_everywhere.Typed[int]):
    pass

def main():
    a = typed_everywhere.Typed(10)
    b = typed_everywhere.Typed("abc")
    test4(a) # Ok
    test4(b) # Error

if typed_everywhere.patch_and_reload_module():
    main()
```

@typed_everywhere.**typed_method**(func)

Use this decorator for functions inside a class. Use _@Typed_ for functions defined outside any class.
