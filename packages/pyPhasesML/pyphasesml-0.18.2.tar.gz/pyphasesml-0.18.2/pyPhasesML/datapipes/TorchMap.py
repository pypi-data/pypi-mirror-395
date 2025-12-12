import torch

from pyPhasesML.datapipes.DataPipe import DataPipe


class TorchMap(DataPipe):
    def __init__(self, datapipe: DataPipe, cuda=False) -> None:
        super().__init__(datapipe)
        self.cuda = cuda

    def __getitem__(self, index):
        x,y = self.datapipe[index]
        x,y = torch.tensor(x), torch.tensor(y)
        if self.cuda:
            x, y = x.cuda(), y.cuda()
        return x, y
