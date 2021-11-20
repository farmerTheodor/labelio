from typing import Protocol, runtime_checkable


@runtime_checkable
class DataWriterBase(Protocol):
    def SetDetails(self, details) -> None:
        ...

    def SetImage(self, image) -> None:
        ...

    def AddLabel(self, label) -> None:
        ...

    def SetListOfLabels(self, labelList) -> None:
        ...

    def SaveImage(self, imagePath) -> None:
        ...

    def SaveListOfLabels(self, labelPath) -> None:
        ...

    def Save(self, imagePath, labelPath) -> None:
        ...
