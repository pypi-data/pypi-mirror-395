from pyPhasesML.datapipes.DataPipe import DataPipe


class DatasetXY(DataPipe):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

        if len(X) != len(Y):
            raise ValueError(f"Lengths of X and Y must be the same: {len(X)} != {len(Y)}")

    def __getitem__(self, index):
        return self.X[index], self.Y[index]

    def __len__(self):
        return len(self.Y)
