import sys
import types


def module_callable(func):
    module_name = func.__module__
    module = sys.modules[module_name]

    class CallableModule(types.ModuleType):
        def __call__(self, *args, **kwargs):
            return func(*args, **kwargs)

    module.__class__ = CallableModule
    return func


@module_callable
def __call__(func):
    return module_callable(func)
