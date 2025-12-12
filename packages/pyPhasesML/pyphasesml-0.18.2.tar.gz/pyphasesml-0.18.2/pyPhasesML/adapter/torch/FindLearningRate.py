import math

from pyPhases import classLogger
from pyPhasesML.Model import ModelConfig
from pyPhasesML.adapter.torch.Callback import Callback
from pyPhases import CSVLogger as Logger


@classLogger
class FindLearningRate(Callback):
    def __init__(self, config: ModelConfig, minLR, maxLR, iterations=3) -> None:
        super().__init__(config)
        self.smoothing = 0.05
        self.csvPath = self.getLogPath() + "/rangetest.csv"
        self.minLR = minLR
        self.maxLR = maxLR
        self.iterations = iterations
        self.logger = Logger(self.csvPath)

    def onTrainingStart(self, model, dataset):
        import torch
        model.maxEpochs = self.iterations
        start_lr = self.minLR
        end_lr = self.maxLR

        def cyclical_lr(x):
            return math.exp(x * math.log(end_lr / start_lr) / (model.maxEpochs * len(dataset.trainingData)))
        
        for param_group in model.optimizer.param_groups:
            param_group['lr'] = start_lr

        model.batchScheduler = torch.optim.lr_scheduler.LambdaLR(model.optimizer, cyclical_lr)
        model.skipValidation = True


    def onBatchEnd(self, model, batchIndex):
        lr_step = model.optimizer.state_dict()["param_groups"][0]["lr"]

        # smooth the loss
        loss = model.runningStats["loss"] / (batchIndex + 1)
        if batchIndex == 0 and model.epoch == 0:
            loss_smooth = loss
        else:
            loss_smooth = self.smoothing * loss + (1 - self.smoothing) * self.lastLoss
        
        self.lastLoss = loss_smooth        
        self.logger.addCsvRow({
            "step": lr_step,
            "loss": loss,
            "loss_smooth": loss_smooth,
        })

