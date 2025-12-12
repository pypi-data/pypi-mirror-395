import numpy as np
from pyPhasesML.datapipes.DataPipe import DataPipe
from pyPhases import classLogger


@classLogger
class MemoryCache(DataPipe):
    """
    A data pipe that loads all data into memory at initialization.
    This is useful for memmapped data that you want to fully load into RAM for faster access.
    """
    def __init__(self, datapipe: DataPipe) -> None:
        super().__init__(datapipe)
        self.log("Loading all data into memory...")
        self.cached_data = [self.datapipe[i] for i in range(len(self.datapipe))]
        self.log(f"Loaded {len(self.cached_data)} items into memory")

    def __getitem__(self, index):
        return self.cached_data[index]
