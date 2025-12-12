import numpy as np

from typing import List
from pyPhasesML.datapipes import RecordMap
from pyPhasesML.datapipes.DataPipe import DataPipe


class MultiSourceMap(DataPipe):
    def __init__(self, dataset: List[RecordMap] = None, seed=2024):
        dataset = dataset or []
        
        self.datapipe = []
        self.length = 0
        self.recordMapIndex = np.empty((0, 2), dtype=int)
        self.seed = seed

        for recordmap in dataset:
            self.addRecordMap(recordmap)



    def addRecordMap(self, recordmap: RecordMap):
        datasetIndex = len(self.datapipe)
        self.datapipe.append(recordmap)
        self.length += len(recordmap)

        recordMapping = np.empty((len(recordmap), 2), dtype=int)
        recordMapping[:, 0] = datasetIndex
        recordMapping[:, 1] = np.arange(0, len(recordmap), dtype=int)

        self.recordMapIndex = np.append(self.recordMapIndex, recordMapping, axis=0)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        datasetIndex, recordIndex = self.recordMapIndex[index]
        return self.datapipe[datasetIndex][recordIndex]
    
    def shuffle(self):
        np.random.seed(self.seed)
        np.random.shuffle(self.recordMapIndex)
