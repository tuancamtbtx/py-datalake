from abc import ABC, abstractmethod

class BaseOperator(ABC):
    """Metaclass of BaseOperator."""

    def __init__(self, **args) -> None:
        pass

    def execute(self, **args) -> None:
        pass