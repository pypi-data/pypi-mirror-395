import math
from pathlib import Path
from pyPhases import classLogger
from pyPhasesML.Model import ModelConfig
from pyPhasesML.adapter.torch.Callback import Callback


@classLogger
class CyclicLearningrate(Callback):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__(config)
        self.learningRateMax = config.learningRate
        self.learningRateMin = config.learningRate / config.cycleLRDivisor
        self.stepSizeInEpochs = 4

    def onTrainingStart(self, model, dataset):
        import torch.optim as optim
        def cyclical_lr(stepsize, min_lr=3e-4, max_lr=3e-3):
            # Scaler: we can adapt this if we do not want the triangular CLR
            scaler = lambda x: 1.0

            # calculate the LR
            def getLR(it):
                return min_lr + (max_lr - min_lr) * relative(it, stepsize)

            # Additional function to see where on the cycle we are
            def relative(it, stepsize):
                cycle = math.floor(1 + it / (2 * stepsize))
                x = abs(it / stepsize - 2 * cycle + 1)
                return max(0, (1 - x)) * scaler(cycle)

            return getLR

        # setup optimizer and scheduler
        if model.optimizer is None:
            model.optimizer = optim.Adam(model.model.parameters(), lr=1.0)
        step_size = self.stepSizeInEpochs * len(dataset.trainingData)
        clr = cyclical_lr(step_size, min_lr=self.learningRateMin, max_lr=self.learningRateMax)
        model.batchScheduler = optim.lr_scheduler.LambdaLR(model.optimizer, [clr for i in range(len(model.optimizer.param_groups))])

    def onTrainingEnd(self, model):
        model.optimizer = None

    def getResumeBatchOptimizerPath(self):
        return Path(self.getLogPath(), ".resumeBatchScheduler.pt")

    def onCheckpoint(self, model):
        import torch
        torch.save(model.batchScheduler.state_dict(), str(self.getResumeBatchOptimizerPath()))
    
    def onRestore(self, model):
        import torch
        batchSchedulerState = torch.load(str(self.getResumeBatchOptimizerPath()))
        model.batchScheduler.load_state_dict(batchSchedulerState)
