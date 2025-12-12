from __future__ import annotations
__all__: list[str] = ['EmptyPrintPolicy', 'FloatTypePolicy', 'IntTypePolicy', 'MinMaxPrintPolicy', 'UnknownTypePolicy']
class EmptyPrintPolicy:
    """
    allows to change how an empty set prints
    """
    def __init__(self, s: str) -> None:
        ...
class FloatTypePolicy:
    """
    internal stored type - float. Additional operations are available
    """
class IntTypePolicy:
    """
    internal stored type - int. Additional operations are available
    """
class MinMaxPrintPolicy:
    """
    allows to change how prints -INF and +INF
    """
    @staticmethod
    def __init__(*args, **kwargs) -> None:
        ...
class UnknownTypePolicy:
    """
    may store any types with required operators
    """
