from queue import Queue, Empty
from threading import Thread
import time

from pyPhasesML.datapipes.DataPipe import DataPipe
from pyPhases import classLogger


@classLogger
class PreloadPipe(DataPipe):
    def __init__(self, datapipe: DataPipe, preloadCount=1):
        super().__init__(datapipe)
        self.queue = Queue(maxsize=preloadCount)
        self.done = False
        self.thread = None

    def start(self):
        # Stop any existing thread
        self.stop()

        # Reset state
        self.done = False

        # Clear the queue
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except Empty:
                break

        # Start a new thread
        self.thread = Thread(target=self._preload)
        self.thread.daemon = True  # don't wait for thread to finish
        self.thread.start()

    def stop(self):
        # Stop the thread if it's running
        if self.thread and self.thread.is_alive():
            self.done = True
            # Wait a short time for the thread to finish
            self.thread.join(timeout=0.1)
            self.thread = None

    def _preload(self):
        try:
            # Explicitly get an iterator from the datapipe to ensure its __iter__ method is called
            datapipe_iter = iter(self.datapipe)
            for d in datapipe_iter:
                if self.done:  # Check if we should stop
                    break
                self.queue.put(d, block=True)
        finally:
            self.done = True

    def __iter__(self):
        self.start()
        return self

    def __next__(self):
        # Check if we're done and the queue is empty
        if (self.done and self.queue.empty()) or len(self) == 0:
            raise StopIteration

        # Get the next item from the queue
        return self.queue.get(block=True)

    def close(self):
        self.stop()
        # Make sure to close the wrapped datapipe
        super().close()