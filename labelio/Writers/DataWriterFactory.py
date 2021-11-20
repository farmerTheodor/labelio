from labelio.Writers.DataWriterBase import DataWriterBase
from labelio.Writers.PascalVocDataWriter import PascalVocDataWriter


def GetDataWriter(requestedWriter) -> DataWriterBase:
    if "pascal" in requestedWriter.lower():
        return PascalVocDataWriter()

    return None
