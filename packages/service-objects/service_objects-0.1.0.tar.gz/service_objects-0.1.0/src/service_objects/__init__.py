def __getattr__(name):
    if name == "AV3":
        from .av3 import AV3
        return AV3
    raise AttributeError(f"module {__name__} has no attribute {name}")

__all__ = ["AV3"]