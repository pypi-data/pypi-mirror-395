import torch.optim as optim
from pyPhases import classLogger
from pyPhasesML.Model import ModelConfig
from pyPhasesML.adapter.torch.Callback import Callback


class OptimizerNotFound(Exception):
    pass


@classLogger
class LoadOptimizer(Callback):
    def __init__(self, modelConfig: ModelConfig) -> None:
        super().__init__(modelConfig)
        self.optimizerId = modelConfig.optimizerId
        self.lr = modelConfig.learningRate
        self.lr_decay = modelConfig.learningRateDecay

    def onTrainingStart(self, model, dataset):
        if model.optimizer is not None:
            self.log("optimizer already loaded")
            return

        self.log(f"loading optimizer {self.optimizerId}")
        if self.optimizerId == "adams":
            model.optimizer = optim.Adam(model.model.parameters(), lr=self.lr, weight_decay=self.lr_decay)
        elif self.optimizerId == "adamsw":
            model.optimizer = optim.AdamW(model.model.parameters(), lr=self.lr, weight_decay=self.lr_decay)
        elif self.optimizerId == "sgd":
            model.optimizer = optim.SGD(model.model.parameters(), lr=self.lr, weight_decay=self.lr_decay)
        elif self.optimizerId == "nesterov":
            model.optimizer = optim.SGD(model.model.parameters(), lr=self.lr, weight_decay=self.lr_decay, nesterov=True)
        elif self.optimizerId == "nadams":
            model.optimizer = optim.NAdam(model.model.parameters(), lr=self.lr, momentum_decay=self.lr_decay)
        else:
            raise OptimizerNotFound(f"optimizer {self.optimizerId} is currently not supported for pytorch implementation")

    def onTrainingEnd(self, model):
        model.optimizer = None