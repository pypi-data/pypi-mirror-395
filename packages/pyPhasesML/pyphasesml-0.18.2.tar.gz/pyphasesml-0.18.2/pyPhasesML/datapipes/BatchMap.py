import numpy as np
from pyPhasesML.datapipes.DataPipe import DataPipe


class BatchMap(DataPipe):
    def __init__(
        self,
        datapipe: DataPipe,
        batchSize=1,
        onlyFullBatches=True,
        toXY=True,
    ) -> None:
        super().__init__(datapipe)
        self.batchSize = batchSize
        self.onlyFullBatches = onlyFullBatches
        self.toXY = toXY

    def __getitem__(self, index):
        start_idx = index * self.batchSize
        end_idx = (index + 1) * self.batchSize
        batchX, batchY = [], []

        for i in range(start_idx, min(end_idx, len(self.datapipe))):
            X, Y = self.datapipe[i]
            batchX.append(X)
            batchY.append(Y)

        return batchX, batchY if self.toXY else zip(batchX, batchY)

    def __len__(self):
        if self.onlyFullBatches:
            return len(self.datapipe) // self.batchSize
        else:
            return (len(self.datapipe) + self.batchSize - 1) // self.batchSize
