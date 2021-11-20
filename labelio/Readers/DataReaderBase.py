from typing import Protocol, runtime_checkable


@runtime_checkable
class DataReaderBase(Protocol):
    def ListOfLabels(self):
        ...

    def ImageName(self) -> str:
        ...

    def ImagePath(self) -> str:
        ...

    def ReadLabelSource(self, source) -> None:
        ...
