import os


def GetTestResourceFolderName():
    return os.path.basename(GetTestResourceFolderPath())


def GetTestResourceFolderPath():
    return os.path.dirname(__file__)


def GetXmlPath():
    return os.path.join(GetTestResourceFolderPath(), "img1.xml")


def GetImgName():
    return "img1.png"


def GetImgFolderName():
    return "images"


def GetImgPath():
    return os.path.join(GetTestResourceFolderPath(), GetImgName())


def GetOutputFolderPath():
    return os.path.join(GetTestResourceFolderPath(), "output")


def GetImageOutputFolderPath():
    return os.path.join(GetOutputFolderPath(), GetImgFolderName())


def GetLabelOutputFolderPath():
    return os.path.join(GetOutputFolderPath(), "labels")


def DeleteTestFiles():
    imageOutputPath = GetImageOutputFolderPath()
    for file in os.listdir(imageOutputPath):
        if not file.endswith(".png"):
            continue
        os.remove(os.path.join(imageOutputPath, file))

    labelOutputPath = GetLabelOutputFolderPath()
    for file in os.listdir(labelOutputPath):
        if not file.endswith(".xml"):
            continue
        os.remove(os.path.join(labelOutputPath, file))
