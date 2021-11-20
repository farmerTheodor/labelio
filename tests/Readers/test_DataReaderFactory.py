import os

import pytest
from labelio.Readers import DataReaderFactory
from labelio.Readers.PascalVocDataReader import PascalVocDataReader
from tests.Resources import TestResourceManager


@pytest.fixture
def xmlPath():
    return os.path.join(os.path.dirname(__file__), "resourcesDocuments/img1.xml")


def InvokeGetDataReader(src):
    return DataReaderFactory.GetDataReader(src)


def test_DataReaderFactory_IfXmlSourceIsUsed_ReturnPascalVocDataReader():
    xmlPath = TestResourceManager.GetXmlPath()
    assert type(InvokeGetDataReader(xmlPath)) is PascalVocDataReader


def test_DataReaderFactory_IfJsonSourceIsUsed_ReturnNone():
    assert InvokeGetDataReader("img.json") is None
