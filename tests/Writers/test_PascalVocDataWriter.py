import os

import pytest
from labelio.Data.Label import Label
from labelio.Writers.PascalVocDataWriter import PascalVocDataWriter
from PIL import Image
from tests.Resources import TestResourceManager


@pytest.fixture
def ImageInstance():
    return Image.open(TestResourceManager.GetImgPath())


@pytest.fixture
def PascalVocDataWriterInstance(ImageInstance) -> PascalVocDataWriter:
    pascalVocDataWriter = PascalVocDataWriter()
    pascalVocDataWriter.SetImage(ImageInstance)
    label = CreateLabel()
    pascalVocDataWriter.AddLabel(label)
    details = {"DatabaseSource": "TestSource", "Segmented": 10}
    pascalVocDataWriter.SetDetails(details)
    yield pascalVocDataWriter
    TestResourceManager.DeleteTestFiles()


def CreateLabel(name="test", boundingBox=(0, 0, 1, 1)):
    label = Label()
    label.Name = name
    label.BoundingBox = boundingBox
    label.Pose = "TestPose"
    label.Truncated = 4
    label.Difficult = 20
    return label


@pytest.fixture
def PascalVocDataWriterWithTwoLabels(
    PascalVocDataWriterInstance,
) -> PascalVocDataWriter:
    labelSet = []
    labelSet.append(CreateLabel("1", (0, 0, 5, 5)))
    labelSet.append(CreateLabel("2", (5, 5, 10, 10)))
    PascalVocDataWriterInstance.SetListOfLabels(labelSet)
    yield (PascalVocDataWriterInstance, labelSet)
    TestResourceManager.DeleteTestFiles()


@pytest.fixture
def ImagePath():
    return os.path.join(TestResourceManager.GetImageOutputFolderPath(), "testImage.png")


@pytest.fixture
def LabelPath():
    return os.path.join(TestResourceManager.GetLabelOutputFolderPath(), "testLabel.xml")


def test_PascalVocDataWriter_SaveFile_AssertFilesInSpecifiedPaths(
    PascalVocDataWriterInstance, ImagePath, LabelPath
):
    PascalVocDataWriterInstance.Save(ImagePath, LabelPath)
    assert os.path.exists(ImagePath)
    assert os.path.exists(LabelPath)


def test_PascalVocDataWriter_SaveImage_AssertImageInSpecifiedPath(
    PascalVocDataWriterInstance,
    ImagePath,
):
    PascalVocDataWriterInstance.SaveImage(ImagePath)
    assert os.path.exists(ImagePath)


def test_PascalVocDataWriter_SaveImageWithEmptyPath_AssertValueError(
    PascalVocDataWriterInstance,
):
    with pytest.raises(ValueError):
        PascalVocDataWriterInstance.SaveImage("")


def test_PascalVocDataWriter_SaveLabel_AssertLabelInSpecifiedPath(
    PascalVocDataWriterInstance,
    LabelPath,
):
    PascalVocDataWriterInstance.SaveListOfLabels(LabelPath)
    assert os.path.exists(LabelPath)


def test_PascalVocDataWriter_SaveLabelWithEmptyPath_AssertValueError(
    PascalVocDataWriterInstance,
):
    with pytest.raises(ValueError):
        PascalVocDataWriterInstance.SaveListOfLabels("")


def test_PascalVocDataWriter_SetDetails_AssertSetsClassSpecificDetails(
    PascalVocDataWriterInstance,
):
    details = {"DatabaseSource": "newSource", "Segmented": 20}
    PascalVocDataWriterInstance.SetDetails(details)
    assert PascalVocDataWriterInstance.DatabaseSource == details["DatabaseSource"]
    assert PascalVocDataWriterInstance.Segmented == details["Segmented"]


def test_PascalVocDataWriter_SetListOfLabels_SetsListOfLabelsVariable(
    PascalVocDataWriterInstance,
):
    listOfLabels = [CreateLabel()]
    PascalVocDataWriterInstance.SetListOfLabels(listOfLabels)
    assert PascalVocDataWriterInstance.ListOfLabels == listOfLabels


def test_PascalVocDataWriter_AssertLabelXml_HasCorrectFields(
    PascalVocDataWriterInstance,
):
    label = CreateLabel()
    labelXml = PascalVocDataWriterInstance.GenerateXmlForLabel(label)

    AssertNameOfElement("object", labelXml)
    AssertNumImmediateChildrenInElement(5, labelXml)
    AssertStringInElementIsEqual(label.Name, labelXml, "name")
    AssertStringInElementIsEqual(label.Pose, labelXml, "pose")
    AssertIntInElementIsEqual(label.Truncated, labelXml, "truncated")
    AssertIntInElementIsEqual(label.Difficult, labelXml, "difficult")
    AssertElementExistsInImmediateChildren("bndbox", labelXml)


def test_PascalVocDataWriter_AssertSizeXml_HasCorrectFields(
    PascalVocDataWriterInstance,
    ImageInstance,
):
    sizeXml = PascalVocDataWriterInstance.GenerateXmlForSize()

    AssertNameOfElement("size", sizeXml)
    AssertNumImmediateChildrenInElement(3, sizeXml)
    AssertIntInElementIsEqual(ImageInstance.width, sizeXml, "width")
    AssertIntInElementIsEqual(ImageInstance.height, sizeXml, "height")
    assert len(ImageInstance.getbands()) == int(sizeXml.findtext("depth"))


def test_PascalVocDataWriter_AssertBoundingBoxXml_HasCorrectFields(
    PascalVocDataWriterInstance,
):
    xMin = 0
    yMin = 1
    xMax = 2
    yMax = 3
    boundingBox = (xMin, yMin, xMax, yMax)
    boundingXml = PascalVocDataWriterInstance.GenerateXmlForBoundingBox(boundingBox)

    AssertNameOfElement("bndbox", boundingXml)
    AssertNumImmediateChildrenInElement(4, boundingXml)
    AssertIntInElementIsEqual(xMin, boundingXml, "xmin")
    AssertIntInElementIsEqual(yMin, boundingXml, "ymin")
    AssertIntInElementIsEqual(xMax, boundingXml, "xmax")
    AssertIntInElementIsEqual(yMax, boundingXml, "ymax")


def test_PascalVocDataWriter_AssertRootXml_HasCorrectFields(
    PascalVocDataWriterInstance,
):
    segmented = PascalVocDataWriterInstance.Segmented
    databaseSource = PascalVocDataWriterInstance.DatabaseSource
    folder = TestResourceManager.GetTestResourceFolderName()
    filename = TestResourceManager.GetImgName()
    path = TestResourceManager.GetImgPath()

    rootXml = PascalVocDataWriterInstance.GenXml()

    AssertNameOfElement("annotation", rootXml)
    AssertNumImmediateChildrenInElement(7, rootXml)
    AssertStringInElementIsEqual(folder, rootXml, "folder")
    AssertStringInElementIsEqual(filename, rootXml, "filename")
    AssertStringInElementIsEqual(path, rootXml, "path")
    AssertIntInElementIsEqual(segmented, rootXml, "segmented")
    AssertElementExistsInImmediateChildren("source", rootXml)
    AssertStringInElementIsEqual(databaseSource, rootXml.find("source"), "database")
    AssertElementExistsInImmediateChildren("size", rootXml)
    AssertElementExistsInImmediateChildren("object", rootXml)


def AssertNameOfElement(value, element):
    assert element.tag == value


def AssertNumImmediateChildrenInElement(value, element):
    assert len(list(element)) == value


def AssertStringInElementIsEqual(value, element, xmlValue):
    assert value == element.findtext(xmlValue)


def AssertIntInElementIsEqual(value, element, xmlValue):
    assert value == int(element.findtext(xmlValue))


def AssertElementExistsInImmediateChildren(value, element):
    assert element.find(value) is not None
