import os
import xml.etree.ElementTree as ET

from labelio.Data.Label import Label


class PascalVocDataReader:
    def __init__(self, source):
        self._ParsedXml = None
        self.ReadLabelSource(source)

    def ImageName(self) -> str:
        return self._ParsedXml.find("filename").text

    def ImagePath(self) -> str:
        return self._ParsedXml.find("path").text

    def ListOfLabels(self):
        listOfLabels = []
        for xmlLabel in self._ParsedXml.iter("object"):
            objectLabel = self._ConvertXmlToLabelObject(xmlLabel)
            listOfLabels.append(objectLabel)

        return listOfLabels

    def _ConvertXmlToLabelObject(self, xmlLabel) -> Label:
        objectLabel = Label()
        objectLabel.BoundingBox = self._ConvertXmlToBoundBoxObject(xmlLabel)
        objectLabel.Name = xmlLabel.find("name").text
        objectLabel.Pose = xmlLabel.find("pose").text
        objectLabel.Truncated = self._ConvertXmlToInt(xmlLabel, "truncated")
        objectLabel.Difficult = self._ConvertXmlToInt(xmlLabel, "difficult")

        return objectLabel

    def _ConvertXmlToBoundBoxObject(self, xmlLabel):
        xmlBoundBox = xmlLabel.find("bndbox")
        minX = self._ConvertXmlToInt(xmlBoundBox, "xmin")
        minY = self._ConvertXmlToInt(xmlBoundBox, "ymin")
        maxX = self._ConvertXmlToInt(xmlBoundBox, "xmax")
        maxY = self._ConvertXmlToInt(xmlBoundBox, "ymax")
        return (minX, minY, maxX, maxY)

    def _ConvertXmlToInt(self, xmlObject, xmlName) -> int:
        return int(xmlObject.find(xmlName).text)

    def ReadLabelSource(self, source) -> None:
        self._ParsedXml = ET.parse(source).getroot()
