# -*- coding: utf-8 -*-
__all__ = ["extractor", "loaders", "stats", "tensor"]


def __getattr__(name):
    if name in __all__:
        import importlib

        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__():
    return __all__
