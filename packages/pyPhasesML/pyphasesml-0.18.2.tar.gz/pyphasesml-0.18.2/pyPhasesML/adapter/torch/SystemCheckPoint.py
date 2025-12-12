from pathlib import Path
import pickle
import signal

from pyPhases import classLogger
from pyPhasesML.Model import ModelConfig
from pyPhasesML.adapter.torch.Callback import Callback


@classLogger
class SystemCheckPoint(Callback):
    def __init__(self, config: ModelConfig, preventShutdown=False) -> None:
        super().__init__(config)
        if preventShutdown:
            signal.signal(signal.SIGTERM, self.shutdown)
        self.shutdownRequest = False
        self.priority = 1000

    def shutdown(self, signum, frame):
        self.shutdownRequest = True
        self.logError("Shutdown requested received, waiting for the next checkpoint")

    def createCheckpoint(self, model):
        import torch
        self.log("Saving checkpoint")
        torch.save(model.model.state_dict(), str(self.getResumeModelPath()))
        torch.save(model.optimizer.state_dict(), str(self.getResumeOptimizerPath()))

        with open(self.getResumeAdapterPath(), "wb") as f:
            pickle.dump({"epoch": model.epoch, "bestMetric": model.bestMetric}, f, protocol=pickle.HIGHEST_PROTOCOL)

        model.trigger("checkpoint", model)

    def restoreCheckpoint(self, model):
        import torch
        self.logSuccess("Restore training")
        modelState = torch.load(str(self.getResumeModelPath()))
        model.loadState(modelState)
        optimizerState = torch.load(str(self.getResumeOptimizerPath()))
        model.optimizer.load_state_dict(optimizerState)

        with open(self.getResumeAdapterPath(), "rb") as f:
            adapterState = pickle.load(f)

        model.startEpoch = adapterState["epoch"]
        model.bestMetric = adapterState["bestMetric"]

        # delete all resume files
        model.trigger("restore", model)

    def getResumeModelPath(self):
        return Path(self.getLogPath(), ".resumeModel.pt")

    def getResumeOptimizerPath(self):
        return Path(self.getLogPath(), ".resumeOptimizer.pt")

    def getResumeAdapterPath(self):
        return Path(self.getLogPath(), ".resumeAdapter.pcl")

    def onTrainingStart(self, model, dataset):
        if self.getResumeModelPath().exists():
            self.restoreCheckpoint(model)

    def onValidationEnd(self, model, results, scorer):
        self.createCheckpoint(model)

        # If a checkpoint is reached and shutdown signal received, exit gracefully
        if self.shutdownRequest:
            self.logSuccess("Shutdown after checkpoint")
            model.trigger("shutdown", model)
            self.log("Shutdown")
            exit()
