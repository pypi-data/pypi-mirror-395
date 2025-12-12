import importlib
import os
from pathlib import Path

from pyPhases.Data import DataNotFound
from pyPhases.exporter.DataExporter import DataExporter
from pyPhases.util.Logger import Logger

from ..Model import Model

if importlib.util.find_spec("tensorflow"):

    if importlib.util.find_spec("torch"):
        print(
            "\033[31;1;4m%s\033[0m"
            % "Tensorflow and PyTorch are installed in the same enviroment, only one model (Tensorflow) can be handled"
        )

    if importlib.util.find_spec("tensorflow.keras"):
        import tensorflow
        from tensorflow.keras import models
        from tensorflow.python.keras.engine.functional import Functional

    elif importlib.util.find_spec("keras"):
        from keras import models

        Functional = False

    class ModelExporter(DataExporter):
        includesStorage = True

        def initialOptions(self):

            return {"basePath": "data/"}

        def getPath(self, dataId):
            return self.getOption("basePath") + dataId

        def checkType(self, expectedType):
            funcCheck = issubclass(expectedType, Functional) if Functional is not None else False
            return issubclass(expectedType, models.Sequential) or issubclass(expectedType, tensorflow.keras.Model) or issubclass(expectedType, Model) or funcCheck

        def read(self, dataId, options={}):
            path = self.getPath(dataId)
            if not Path("%s.index" % path).exists():
                raise DataNotFound()
            return path

        def write(self, dataId, model, options={}):
            model.save_weights(self.getPath(dataId))

elif importlib.util.find_spec("torch"):
    
    class ModelExporter(DataExporter):
        includesStorage = True

        def initialOptions(self):

            return {"basePath": "data/"}

        def getPath(self, dataId):
            return self.getOption("basePath") + dataId

        def checkType(self, expectedType):
            import torch

            return issubclass(expectedType, torch.nn.Module) or issubclass(expectedType, Model)

        def read(self, dataId, options={}):
            import torch
            
            try:
                deviceName = "cuda" if torch.cuda.is_available() else "cpu"
                return torch.load(self.getPath(dataId), map_location=torch.device(deviceName))
            except FileNotFoundError:
                raise DataNotFound()

        def write(self, dataId, model, options={}):
            import torch
            
            torch.save(model.state_dict(), self.getPath(dataId))

else:
    # ability to ignore missing model exporter for testing purposes
    if os.environ.get("PYPHASESML_IGNORE_MISSING_MODEL_EXPORTER", 0) == 1:
        raise Exception("No supported ModelExporter located (Supported: pytorch/tensorflow)")
    else:

        class ModelExporter(DataExporter):
            includesStorage = True

            def checkType(self, expectedType):
                return False

            def read(self, path, data, options={}):
                raise Exception("ModelExporter is only as stub, please install tensorflow or pytorch to use the ModelExporter")

            def write(self, path, data, model, options={}):
                raise Exception("ModelExporter is only as stub, please install tensorflow or pytorch to use the ModelExporter")
