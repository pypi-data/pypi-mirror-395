from dataclasses import astuple, dataclass

import numpy as np


class ValidDataset:
    pass


@dataclass
class DataSet:
    x: np.array
    y: np.array
    numClasses: int = None
    catMatrix = None

    def __len__(self):
        return 2

    @staticmethod
    def fromTuple(data, numClasses=None):
        x, y = data
        return DataSet(x, y, numClasses)

    def asTuple(self):
        return astuple(self)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            raise StopIteration
        raise TypeError("Datset can only be split in x and y, try to get index %i" % (index))


class TrainingSetLoader:
    def __init__(self, trainingData=None, validationData=None):
        self.trainingData: DataSet = trainingData
        self.validationData: DataSet = validationData
