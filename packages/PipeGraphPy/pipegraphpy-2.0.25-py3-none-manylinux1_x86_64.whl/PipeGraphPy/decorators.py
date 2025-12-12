#!/usr/bin/env python
# -*- coding: utf-8 -*-


class _Missing(object):
    def __repr__(self):
        return "no value"

    def __reduce__(self):
        return "_missing"

_missing = _Missing()

class cached_property(property):
    """将函数转换为惰性属性的装饰器。包装的函数在第一次使用结果时被调用，
       然后在下次访问该值时使用该计算缓存的结果:

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42
    """

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
