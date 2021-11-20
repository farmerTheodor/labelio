import copy


class Label:
    def __init__(self) -> None:
        self.BoundingBox = None
        self.Name = ""
        self.Pose = "Unspecified"
        self.Truncated = 0
        self.Difficult = 0

    def IsOverlapingWith(self, boundingBox):
        (minXOther, minYOther, maxXOther, maxYOther) = boundingBox  # 1
        (
            minXBoundBox,
            minYBoundBox,
            maxXBoundBox,
            maxYBoundBox,
        ) = self.BoundingBox  # 2
        # checks if either box's min value is greater than the others max if so we can deduce that the box does not intersect
        return not (
            # checks if either box is to the right of each other
            minXOther > maxXBoundBox
            or minXBoundBox > maxXOther
            # checks if either box is to the above of each other
            or minYOther > maxYBoundBox
            or minYBoundBox > maxYOther
        )

    def Crop(self, box):
        (minX, minY, maxX, maxY) = self.BoundingBox
        if minX < box[0]:
            minX = box[0]
        if minY < box[1]:
            minY = box[1]

        if maxX > box[2]:
            maxX = box[2]
        if maxY > box[3]:
            maxY = box[3]

        return (minX, minY, maxX, maxY)

    def __copy__(self):
        labelCopy = Label()
        labelCopy.BoundingBox = copy.copy(self.BoundingBox)
        labelCopy.Name = copy.copy(self.Name)
        labelCopy.Pose = copy.copy(self.Pose)
        labelCopy.Truncated = copy.copy(self.Truncated)
        labelCopy.Difficult = copy.copy(self.Difficult)

        return labelCopy

    def __deepcopy__(self, memo):
        labelCopy = Label()
        labelCopy.BoundingBox = copy.deepcopy(self.BoundingBox, memo)
        labelCopy.Name = copy.deepcopy(self.Name, memo)
        labelCopy.Pose = copy.deepcopy(self.Pose, memo)
        labelCopy.Truncated = copy.deepcopy(self.Truncated, memo)
        labelCopy.Difficult = copy.deepcopy(self.Difficult, memo)

        return labelCopy
