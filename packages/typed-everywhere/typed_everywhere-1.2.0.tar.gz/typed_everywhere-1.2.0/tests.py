import typeguard
from typed_everywhere import *
import typed_everywhere


x = typed_everywhere.Typed(456)


class A:
    a = Typed(10)


class B:
    def __add__(self, other):
        return B()


class C:
    __slots__ = ["a"]

    def __init__(self):
        self.a = Typed(10)


@Typed
def func2(self):
    print("hello2")
      

class D:
    @typed_method
    def func(self):
        print("hello1")


def test1():
    global b
    print("here")
    b = c = d = Typed(10)
    b += Typed(20)
    print(b)
    print(type(b))


def test2():
    a = A()
    a.a = Typed(5)
    a.a = 30
    print(a.a)
    del a.a
    print(a.a)


def test3():
    a = Typed(B())
    print(a)
    a += 1
    print(a)


@typeguard.typechecked
def test4(a: Typed[list[int]]):
    pass


def test5():
    c = C()
    try:
        c.a = "abc"
    except TypeError:
        pass
    else:
        raise RuntimeError("expected TypeError")


def test6():
    d = D()
    D.func = func2
    d.func()
    try:
        D.func = 10
    except TypeError:
        pass
    else:
        raise RuntimeError("expected TypeError")
    
 
def main():
    print(x)
    test1()
    print()
    test2()
    print()
    test3()
    test4(Typed([1,2,3]))
    print()
    test5()
    print()
    test6()


if typed_everywhere.patch_and_reload_module():
    main()
