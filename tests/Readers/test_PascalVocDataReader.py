import os

import pytest
from labelio.Readers.DataReaderBase import DataReaderBase
from labelio.Readers.PascalVocDataReader import PascalVocDataReader
from tests.Resources import TestResourceManager


@pytest.fixture
def PascalVocDataReaderInstance():
    pathToTestXmlDoc = TestResourceManager.GetXmlPath()
    return PascalVocDataReader(pathToTestXmlDoc)


@pytest.fixture
def PascalVocDataReaderFirstLabel(PascalVocDataReaderInstance):
    return PascalVocDataReaderInstance.ListOfLabels()[0]


def test_PascalVocDataReader_isOfTypeDataReaderBase(
    PascalVocDataReaderInstance,
):
    assert issubclass(type(PascalVocDataReaderInstance), DataReaderBase)


def test_withFile_canOpen(PascalVocDataReaderInstance):

    assert PascalVocDataReaderInstance.ListOfLabels() is not None


def test_withFile_readCorrectNumberOfEntries(PascalVocDataReaderInstance):

    assert len(PascalVocDataReaderInstance.ListOfLabels()) == 4


def test_withFile_readFirstLabel_boundingBoxIsCorrect(
    PascalVocDataReaderFirstLabel,
):
    (minX, minY, maxX, maxY) = PascalVocDataReaderFirstLabel.BoundingBox
    assert minX == 0
    assert minY == 0
    assert maxX == 200
    assert maxY == 200


def test_withFile_readPathToImage(PascalVocDataReaderInstance):
    # Path is relative because of privacy reasons
    assert PascalVocDataReaderInstance.ImagePath() == """./tests/Resources/img1.png"""


def test_withFile_readImageName(PascalVocDataReaderInstance):
    assert PascalVocDataReaderInstance.ImageName() == TestResourceManager.GetImgName()


def test_withFile_pathToImageIsValid(PascalVocDataReaderInstance):
    assert os.path.exists(PascalVocDataReaderInstance.ImagePath())
