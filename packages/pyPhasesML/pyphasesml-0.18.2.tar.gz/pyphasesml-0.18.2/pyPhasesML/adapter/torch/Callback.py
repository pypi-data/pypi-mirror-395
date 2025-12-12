from pyPhasesML.Model import ModelConfig


class Callback:
    def __init__(self, config: ModelConfig, priority=100) -> None:
        self.config = config
        self.priority = priority        
        self.event_handlers = {
            "trainingStart": self.onTrainingStart,
            "trainingEnd": self.onTrainingEnd,
            "validationStart": self.onValidationStart,
            "validationEnd": self.onValidationEnd,
            "batchEnd": self.onBatchEnd,
            "shutdown": self.onShutdown,
            "checkpoint": self.onCheckpoint,
            "restore": self.onRestore,
            "register": self.onRegister,
        }

    def getLogPath(self):
        return f"{self.config.logPath}/"

    def trigger(self, event, *args, **kwargs):
        handler = self.event_handlers.get(event)
        if handler:
            return handler(*args, **kwargs)

    def onTrainingStart(self, model, dataset):
        pass

    def onTrainingEnd(self, model):
        pass

    def onValidationStart(self, model, validationData):
        pass

    def onValidationEnd(self, model, results, scorer):
        pass

    def onBatchEnd(self, model, batchIndex):
        pass
    
    def onShutdown(self, model):
        pass
    
    def onCheckpoint(self, model):
        pass

    def onRestore(self, model):
        pass
    
    def onRegister(self, model):
        pass
