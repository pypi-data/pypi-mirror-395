
from typing import Any, Iterator


class DataPipe:
    def __init__(self, datapipe: "DataPipe") -> None:
        self.datapipe = datapipe
        self._iterator = None

    def __getitem__(self, index):
        if index == len(self):
            raise StopIteration
        return self.datapipe[index]

    def __len__(self):
        return len(self.datapipe)

    def __iter__(self) -> Iterator[Any]:
        # For nested pipelines, we need to ensure the wrapped datapipe's __iter__ is called
        # This is important for pipelines that need to initialize state in __iter__
        if hasattr(self, 'datapipe') and self.datapipe is not None:
            # Get an iterator from the wrapped datapipe
            datapipe_iter = iter(self.datapipe)
            # We'll use our own __getitem__ method to get items
            # This ensures consistent behavior while still triggering the wrapped datapipe's __iter__
            for i in range(len(self)):
                yield self[i]
        else:
            # Base case: no wrapped datapipe, just yield items directly
            for i in range(len(self)):
                yield self[i]

    def close(self):
        # Propagate close to the wrapped datapipe if it exists
        if hasattr(self, 'datapipe') and self.datapipe is not None:
            self.datapipe.close()