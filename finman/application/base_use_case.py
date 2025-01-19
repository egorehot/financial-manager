from abc import ABC, abstractmethod
from typing import Generic, TypeVar


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class UseCase(ABC, Generic[InputType, OutputType]):
    @abstractmethod
    async def __call__(self, data: InputType) -> OutputType:
        raise NotImplementedError
