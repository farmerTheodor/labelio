import os
from xml.etree.ElementTree import Element, ElementTree, SubElement

from PIL import Image


class PascalVocDataWriter:
    def __init__(self):
        self.DatabaseSource = "Unknown"
        self.Segmented = 0
        self.ListOfLabels = []
        self.Image = None

    def SetDetails(self, details) -> None:
        self.DatabaseSource = details["DatabaseSource"]
        self.Segmented = details["Segmented"]

    def SetImage(self, image: Image):
        self.Image = image

    def AddLabel(self, label):
        self.ListOfLabels.append(label)

    def SetListOfLabels(self, labelList):
        self.ListOfLabels = labelList

    def SaveImage(self, imagePath):
        if not imagePath.strip():
            raise ValueError("empty image path")

        self.Image.save(imagePath)
        self.Image.filename = imagePath

    def SaveListOfLabels(self, labelPath):
        if not labelPath.strip():
            raise ValueError("empty label path")

        tree = ElementTree(self.GenXml())
        with open(labelPath, "wb") as xmlFP:
            tree.write(xmlFP)

    def Save(self, imagePath, labelPath):
        self.SaveImage(imagePath)
        self.SaveListOfLabels(labelPath)

    def GenXml(self) -> Element:
        if self.Image is None:
            raise ValueError("Data writer Image value set to None")

        top = Element("annotation")
        path = self.Image.filename
        # strips the file name off of the path returns the first folder
        folder = os.path.basename(os.path.dirname(path))
        self.GenerateTextXmlAndAttach("folder", folder, top)
        filename = os.path.basename(path)
        self.GenerateTextXmlAndAttach("filename", filename, top)
        self.GenerateTextXmlAndAttach("path", path, top)

        source = SubElement(top, "source")
        self.GenerateTextXmlAndAttach("database", self.DatabaseSource, source)

        sizeXml = self.GenerateXmlForSize()
        self.AttachElementToParent(sizeXml, top)

        self.GenerateTextXmlAndAttach("segmented", self.Segmented, top)

        for label in self.ListOfLabels:
            labelXml = self.GenerateXmlForLabel(label)
            self.AttachElementToParent(labelXml, top)

        return top

    def GenerateXmlForSize(self):
        sizeXML = Element("size")
        depth = len(self.Image.getbands())

        self.GenerateTextXmlAndAttach("width", self.Image.width, sizeXML)
        self.GenerateTextXmlAndAttach("height", self.Image.height, sizeXML)
        self.GenerateTextXmlAndAttach("depth", depth, sizeXML)
        return sizeXML

    def GenerateXmlForLabel(self, label) -> Element:
        labelXml = Element("object")

        self.GenerateTextXmlAndAttach("name", label.Name, labelXml)
        self.GenerateTextXmlAndAttach("pose", label.Pose, labelXml)
        self.GenerateTextXmlAndAttach("truncated", label.Truncated, labelXml)
        self.GenerateTextXmlAndAttach("difficult", label.Difficult, labelXml)

        boundingBoxXml = self.GenerateXmlForBoundingBox(label.BoundingBox)
        self.AttachElementToParent(boundingBoxXml, labelXml)

        return labelXml

    def GenerateXmlForBoundingBox(self, boundingBox):
        boundingBoxXml = Element("bndbox")
        (
            xmin,
            ymin,
            xmax,
            ymax,
        ) = boundingBox
        self.GenerateTextXmlAndAttach("xmin", xmin, boundingBoxXml)
        self.GenerateTextXmlAndAttach("ymin", ymin, boundingBoxXml)
        self.GenerateTextXmlAndAttach("xmax", xmax, boundingBoxXml)
        self.GenerateTextXmlAndAttach("ymax", ymax, boundingBoxXml)

        return boundingBoxXml

    def GenerateTextXmlAndAttach(self, name, value, parentElement: Element):
        element = SubElement(parentElement, name)
        if value is not str:
            value = str(value)
        element.text = value

    def AttachElementToParent(self, subElement, parentElement):
        parentElement.append(subElement)
