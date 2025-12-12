import numpy as np
from pyPhasesML.datapipes.DataPipe import DataPipe


class RecordMap(DataPipe):
    def __init__(self, dataset: DataPipe, mapping, mappingLengths=None):
        self.dataset = dataset

        if mappingLengths is not None:
            mapping = self.convertMappingToSegments(mapping, mappingLengths)

        self.mapping = mapping
        self.currentIndex = 0

    def convertMappingToSegments(self, recordMapping, segmentLengths):
        segmentLengthsCum = np.cumsum([0] + segmentLengths)
        segments = np.arange(sum(segmentLengths))
        segments = [segments[segmentLengthsCum[recordMapping[i]] : segmentLengthsCum[recordMapping[i] + 1]] for i in range(len(recordMapping))]

        return [item for sublist in segments for item in sublist]

    def __len__(self):
        return len(self.mapping)

    def __getitem__(self, index):
        return self.dataset[self.mapping[index]]
