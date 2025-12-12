
from pyPhasesML.datapipes.DataPipe import DataPipe
from ..DataManipulation import DataManipulation


class Manipulator(DataPipe):
    def __init__(self, datapipe: DataPipe, manipulation: DataManipulation, config = None) -> None:
        self.datapipe = datapipe
        self.manipulation = manipulation
        self.config = config

    def __getitem__(self, index):
        return self.manipulation(self.datapipe[index], self.config, index)

    def __len__(self):
        return len(self.datapipe)

