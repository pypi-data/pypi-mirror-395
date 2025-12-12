from pathlib import Path
import shutil

import numpy as np

from pyPhases.Data import DataNotFound
from pyPhases.exporter.DataExporter import DataExporter


class MemmapRecordExporter(DataExporter):
    includesStorage = True
    batchFillProcess = None

    def __init__(self, options=None):
        super().__init__(options)
        self.currentArrayShapes = {}
        self.segmentLength = None
        self.recordLengths = None
        self.recordLengths_cumulative = None

    def initialOptions(self):
        return {
            "basePath": "./data",
            "dtype": "float32",
        }

    def getShapeFilePath(self, dataId, tmp=False):
        add = "-tmp" if tmp else ""
        return self.getPath(dataId) + add + "-shape.npy"

    def saveShape(self, dataId, lengths, saveShape, tmp=False):
        shape = np.array((lengths, saveShape), dtype="object")
        np.save(self.getShapeFilePath(dataId, tmp=tmp), shape)
        self.log("saved %s: Shape %s (%i records)" % (dataId, str(saveShape), len(lengths)))

    def finishShape(self, dataId):
        self.saveShape(dataId, *self.currentArrayShapes[dataId], tmp=False)
        del self.currentArrayShapes[dataId]
        tmpPath = Path(self.getShapeFilePath(dataId, tmp=True))
        if tmpPath.is_file():
            tmpPath.unlink()

    def finishStream(self, dataId, options=None):
        options = options or {}
        if dataId in self.currentArrayShapes:
            self.finishShape(dataId)
        path = self.getPath(dataId)
        return shutil.move(f"{path}-tmp", path)

    def saveFromArrayList(self, dataId, arrayList):
        """fills the array from a list of 2-dimensional arrays"""
        array = np.concatenate(arrayList)
        array = np.expand_dims(array, 0)
        memmap = self.stream(dataId, {"dtype": self.getOption("dtype"), "mode": "w+", "shape": array.shape})
        memmap[:, :, :] = array
        memmap.flush()
        del memmap

        lengths = [r.shape[0] for r in arrayList]
        self.currentArrayShapes[dataId] = lengths, array.shape
        self.finishStream(dataId)
        
    def loadTmp(self, dataId):
        shapePath = self.getShapeFilePath(dataId, tmp=True)
        if not Path(shapePath).exists():
            raise Exception(f"Shape file not found: {shapePath}")
        self.currentArrayShapes[dataId] = np.load(shapePath, allow_pickle=True)
        self.currentArrayShapes[dataId][0] = list(self.currentArrayShapes[dataId][0])

    def saveAndAppendArray(self, dataId, arrayList):
        """appends an array to the existing file or creates a new one"""

        array = np.concatenate(arrayList)
        array = np.expand_dims(array, 0)

        memmap = None
        if dataId not in self.currentArrayShapes:
            self.currentArrayShapes[dataId] = [[], np.array((1, 0, array.shape[2]))]
            memmap = self.stream(dataId, {"dtype": self.getOption("dtype"), "mode": "w+", "shape": array.shape})

        shape = self.currentArrayShapes[dataId][1].astype(np.int64)
        if array.shape[2] != shape[2]:
            raise Exception("The number of channels has to be constant, but was %s and is now %s" % (shape[2], array.shape[2]))

        lengths = shape[1]

        shape[1] += np.array(array.shape[1])

        if memmap is None:
            memmap = self.stream(
                dataId,
                {
                    "dtype": self.getOption("dtype"),
                    "mode": "readwrite",
                    "shape": tuple(shape.tolist()),
                },
            )
        memmap[:, lengths:, :] = array
        memmap.flush()
        del memmap

        self.currentArrayShapes[dataId][0] = np.append(self.currentArrayShapes[dataId][0], [r.shape[0] for r in arrayList])
        self.currentArrayShapes[dataId][1] = shape
        self.saveShape(dataId, *self.currentArrayShapes[dataId], tmp=True)

    def checkType(self, type):
        return type == np.memmap

    def getPath(self, dataId):
        return self.getOption("basePath") + "/" + dataId

    def stream(self, dataId, options):
        return np.memmap(self.getPath(dataId + "-tmp"), **options)

    def exists(self, dataId):
        return Path(self.getPath(dataId)).is_file()
    
    def existsTmp(self, dataId):
        return Path(self.getPath(dataId + "-tmp")).is_file()

    def read(self, dataId, options):
        for f, k in self.options.items():
            options.setdefault(f, k)

        if not self.exists(dataId):
            raise DataNotFound("Data with id %s nof found" % dataId)

        shapePath = self.getShapeFilePath(dataId)
        if not Path(shapePath).exists():
            raise Exception("Shape file not found: %s" % shapePath)

        # Clear any existing memmap cache when loading new data
        self.clearMemmapCache()

        # load complete shape, and record lengths
        lengths, shape = np.load(shapePath, allow_pickle=True)
        self.recordLengths = lengths
        self.recordLengths_cumulative = np.cumsum([0] + lengths)
        self.fileShape = tuple(shape)
        self.type = options["dtype"]
        self.CurrentItemIndex = 0

        self.filePath = self.getPath(dataId)

        return self

    def get(self, dataId=None, options=None):
        if options == None:
            return self
        
        return self.read(dataId, options)

    def __iter__(self):
        self.CurrentItemIndex = 0
        self.clearMemmapCache()
        return self

    def __next__(self):
        if self.CurrentItemIndex >= len(self):
            raise StopIteration
        else:
            self.CurrentItemIndex += 1
            return self[self.CurrentItemIndex - 1]

    def getMemMap(self):
        if not hasattr(self, '_memmap_cache') or self._memmap_cache is None:
            self._memmap_cache = np.memmap(self.filePath, dtype=self.type, mode="r", shape=self.fileShape)
        return self._memmap_cache

    def clearMemmapCache(self):
        if hasattr(self, '_memmap_cache') and self._memmap_cache is not None:
            del self._memmap_cache
        self._memmap_cache = None

    def close(self):
        self.clearMemmapCache()

    def __getitem__(self, index):
        memmap = self.getMemMap()
        
        start = sum(self.recordLengths[:index])
        end = start + self.recordLengths[index]
        return memmap[0, start:end, :]

    def __len__(self):
        return len(self.recordLengths)