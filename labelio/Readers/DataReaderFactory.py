from labelio.Readers.DataReaderBase import DataReaderBase
from labelio.Readers.PascalVocDataReader import PascalVocDataReader


def GetDataReader(source) -> DataReaderBase:
    if ".xml" in source:
        return PascalVocDataReader(source)

    return None
