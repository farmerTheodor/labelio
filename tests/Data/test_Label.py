import copy

import pytest
from labelio.Data.Label import Label


def createTestLabel(boundingBox=(0, 1, 2, 3), name="test") -> Label:
    label = Label()
    label.Name = name
    label.BoundingBox = boundingBox

    return label


def test_Label_IsOverlapingWith():
    otherBox = (10, 10, 40, 40)
    wellInLabel = createTestLabel((20, 20, 25, 25))
    outsideBottomRightLabel = createTestLabel((20, 20, 45, 45))
    outsideTopLeftLabel = createTestLabel((0, 0, 15, 15))

    assert wellInLabel.IsOverlapingWith(otherBox)
    assert outsideBottomRightLabel.IsOverlapingWith(otherBox)
    assert outsideTopLeftLabel.IsOverlapingWith(otherBox)


def test_Label_IsNotOverlapingWith():
    otherBox = (10, 10, 40, 40)
    wellOutLabel = createTestLabel((1000, 1000, 10000, 1000))

    assert not wellOutLabel.IsOverlapingWith(otherBox)


def tests_Label_OnCrop_AndCroppedBoxIsSmallerThanLabel_AssertThatLabelIsSmallerOrEqualToCroppedBox():
    otherBox = (20, 20, 25, 25)
    label = createTestLabel((10, 10, 40, 40))
    (minX, minY, maxX, maxY) = label.Crop(otherBox)
    assert minX >= otherBox[0]
    assert minY >= otherBox[1]
    assert maxX <= otherBox[2]
    assert maxY <= otherBox[3]


def tests_Label_OnCrop_AndCroppedBoxIsLargerThanLabel_AssertThatLabelIsUnchangedCroppedBox():
    otherBox = (10, 10, 40, 40)
    originalDimensions = (20, 20, 25, 25)
    label = createTestLabel(originalDimensions)
    (minX, minY, maxX, maxY) = label.Crop(otherBox)
    assert minX == originalDimensions[0]
    assert minY == originalDimensions[1]
    assert maxX == originalDimensions[2]
    assert maxY == originalDimensions[3]


def tests_Label_OnCopy_ExpectObjectReferenceToBeDifferent():
    label = createTestLabel()
    copiedLabel = copy.copy(label)
    assert copiedLabel is not label


def tests_Label_OnDeepCopy_ExpectObjectReferenceToBeDifferent():
    label = createTestLabel()
    copiedLabel = copy.deepcopy(label)
    assert copiedLabel is not label
    # The rest of the objects are immutable and are not split in memory until need be
