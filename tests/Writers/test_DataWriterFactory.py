from labelio.Writers.DataWriterFactory import GetDataWriter
from labelio.Writers.PascalVocDataWriter import PascalVocDataWriter


def test_DataWriterFactory_GivenPascalVocString_ReturnPascalVocWriterTypeObject():
    writer = GetDataWriter("PascalVoc")
    assert type(writer) is PascalVocDataWriter


def test_DataWriterFactory_GivenUnknownString_ReturnNone():
    writer = GetDataWriter("thisisanunknownstring")
    assert writer is None
