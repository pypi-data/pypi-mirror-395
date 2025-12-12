import random
from pyPhasesML.datapipes.DataPipe import DataPipe


class ShuffleMap(DataPipe):
    def __init__(self, datapipe, seed=None) -> None:
        super().__init__(datapipe)
        self.seed = seed
        self.indices = list(range(len(datapipe)))
        self._shuffle_indices()

    def _shuffle_indices(self):
        """Shuffle the indices using the stored seed if available."""
        # If a seed is provided, use it to ensure reproducible shuffling
        if self.seed is not None:
            random_state = random.getstate()  # Save current random state
            random.seed(self.seed)
            random.shuffle(self.indices)
            random.setstate(random_state)  # Restore random state
        else:
            random.shuffle(self.indices)

    def __getitem__(self, index):
        original_index = self.indices[index]
        return self.datapipe[original_index]

    def __iter__(self):
        # Reshuffle the indices on each iteration
        self._shuffle_indices()
        # Call the parent's __iter__ to ensure proper iteration through nested pipelines
        return super().__iter__()
