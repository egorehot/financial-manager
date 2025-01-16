from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class UseCase(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    def __call__(self, data: InputType) -> OutputType:
        raise NotImplementedError
