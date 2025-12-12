# Submodules are imported lazily to avoid circular import issues.
# Import specific submodules as needed, e.g.:
#   from catrxneng import utils
#   from catrxneng.utils.time import Time

__all__ = [
    "utils",
    "quantities",
    "species",
    "conf",
    "reactors",
    "plots",
    "simulate",
    "kinetic_models",
    "material",
    "reactions",
]


def __getattr__(name: str):
    """Lazy import of submodules to avoid circular imports."""
    if name in __all__:
        import importlib

        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
