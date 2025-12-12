import numpy as np

from pyPhasesML.exporter import MemmapRecordExporter


class MemmapRecordSegmentsExporter:
    includesStorage = True
    batchFillProcess = None

    def __init__(
        self, recordExporter: MemmapRecordExporter, segmentLength, paddedSegments=None
    ):
        self.recordExporter = recordExporter
        self.segmentLength = segmentLength
        self.paddedSegments = paddedSegments

        self.CurrentItemIndex = 0

    def __iter__(self):
        self.CurrentItemIndex = 0
        return self

    def __next__(self):
        if self.CurrentItemIndex >= len(self):
            raise StopIteration
        else:
            self.CurrentItemIndex += 1
            return self[self.CurrentItemIndex - 1]

    def _getRecordSegmentIndex(self, segment):
        segmentLength = self.segmentLength
        recordStartInSegments = (
            self.recordExporter.recordLengths_cumulative / segmentLength
        )
        recordIndex = np.searchsorted(recordStartInSegments, segment, side="right") - 1
        segmentIndex = segment - recordStartInSegments[recordIndex]
        return int(recordIndex), int(segmentIndex)

    def __getitem__(self, index):
        memmap = self.recordExporter.getMemMap()

        recIndex, segIndex = self._getRecordSegmentIndex(index)

        start = self.recordExporter.recordLengths_cumulative[recIndex] + int(
            segIndex * self.segmentLength
        )
        end = start + self.segmentLength

        # add padding
        if self.paddedSegments is not None:
            end += (
                self.paddedSegments[0] * self.segmentLength
                + self.paddedSegments[1] * self.segmentLength
            )

        return memmap[0, start:end, :]

    def __len__(self):
        if self.paddedSegments is not None:
            # remove all invalid segments
            paddedSegments = (self.paddedSegments[0] + self.paddedSegments[1]) * len(self.recordExporter.recordLengths)
            return sum(self.recordExporter.recordLengths) // self.segmentLength - paddedSegments

        return sum(self.recordExporter.recordLengths) // self.segmentLength
