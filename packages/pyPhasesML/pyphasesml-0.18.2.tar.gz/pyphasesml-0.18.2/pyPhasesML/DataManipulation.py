import numpy as np
from pyPhases import classLogger


class ManipulationStepMissingException(Exception):
    pass


@classLogger
class DataManipulation:
    """manipulate Data using sequential steps defined in a config"""
    def __init__(self, config, splitName, projectconfig=None) -> None:
        self.manipulationConfig = config
        self.config = projectconfig
        self.splitName = splitName

    def step(self, stepname, X, Y, index=None, **options):
        # check if manipulation step exist
        self.currentIndex = index
        if hasattr(self, stepname):
            # call method
            try:
                return getattr(self, stepname)(X, Y, **options)
            except Exception as e:
                import traceback
                
                # Get the full traceback as a string
                tb_str = traceback.format_exc()
                # Add context about which step failed
                self.logError(type(e)(f"Error in data manipulation step '{stepname}': {str(e)}\nTraceback:\n{tb_str}"))
                raise type(e)(f"Error in data manipulation step '{stepname}': {str(e)}") from e
        else:
            raise ManipulationStepMissingException(f"DataManipulation {stepname} not found")

    def __call__(self, Segment, config=None, index=None):
        X, Y = Segment
        config = config or self.manipulationConfig
        return self.manipulateByConfig(X, Y, config, index)
    
    def addBatchDimension(self, X, Y):
        return X[np.newaxis], Y[np.newaxis]

    def manipulateByConfig(self, X, Y, config, index=None):      
        for c in config:
            X, Y = self.loadFromConfig(c, X, Y, self.splitName, index)
        return X, Y

    def loadFromConfig(self, config, X, Y, splitName, index=None):
        config = config.copy()
        name = config["name"]
        ignoreChannels = config["ignoreChannels"] if "ignoreChannels" in config else None
        del config["name"]

        if "split" in config:
            if config["split"] and splitName != config["split"]:
                return X, Y
            del config["split"]

        # remove ignored channels for manipulation
        if ignoreChannels is not None:
            ignored = X[:, :, ignoreChannels]
            X = np.delete(X, ignoreChannels, axis=2)
            del config["ignoreChannels"]

        X, Y = self.step(name, X, Y, index, **config)

        # add ignored channels back
        if ignoreChannels is not None:
            X = np.insert(X, ignoreChannels, ignored, axis=2)

        return X, Y
