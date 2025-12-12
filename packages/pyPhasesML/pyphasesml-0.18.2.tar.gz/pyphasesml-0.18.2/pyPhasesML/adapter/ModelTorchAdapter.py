import gc

import numpy as np
from pyPhasesML.scorer.ScorerTorch import ScorerTorch
import torch
from tqdm import tqdm

from pyPhasesML.adapter.torch.CSVLogger import CSVLogger
from pyPhasesML.adapter.torch.LoadOptimizer import LoadOptimizer
from pyPhasesML.adapter.torch.SystemCheckPoint import SystemCheckPoint
from pyPhasesML.adapter.torch.CheckPoint import CheckPoint

from ..DataSet import DataSet, TrainingSetLoader
from ..ModelAdapter import ModelAdapter


class ModelTorchAdapter(ModelAdapter):
    model: torch.nn.Module
    useGPU = torch.cuda.is_available()

    def __init__(self, options=None) -> None:
        super().__init__(options)
        self.cbs = []
        self.skipValidation = False
        self.metricDefinitions = {}
        self.batchScheduler = None
        self.optimizer = None
        self.debug = False

    def _toTensor(self, x):
        if not torch.is_tensor(x):
            x = torch.tensor(x)
        if self.useGPU:
            x = x.cuda()
        return x

    def prepareX(self, x, validation=False):
        return self._toTensor(x)

    
    def prepareY(self, y, validation=False):
        return self._toTensor(y)

    def prepareDataAdapter(self, datasetOrTuple, validation=False):
        x, y = datasetOrTuple

        dataset = DataSet(x, y)
        return self.prepareData(dataset, validation)

    def registerCB(self, cb):
        self.cbs.append(cb)
        self.cbs.sort(key=lambda x: x.priority)
        cb.trigger("register", self)

    def initAdapter(self, findingLearningRate=False):
        self.batchScheduler = None
        config = self.config

        self.registerCB(LoadOptimizer(config))
        self.registerCB(CSVLogger(config))
        self.registerCB(SystemCheckPoint(config))
        self.registerCB(CheckPoint(config))

    def trigger(self, eventName, *args, **kwargs):
        for cb in self.cbs:
            cb.trigger(eventName, *args, **kwargs)

        super().trigger(eventName, *args, **kwargs)

    def prepareForScore(self, targets, prediction):
        lastDimension = self.config.numClasses if self.oneHotDecoded else 1
        targets = targets.reshape(-1, lastDimension)
        prediction = prediction.reshape(-1, lastDimension)
        return targets, prediction

    def scoreBatch(self, scorer, truth, predictions, processList=None):
        results = scorer.score(truth, predictions, trace=True)

        if processList is not None:
            processList.set_postfix({m: results[m] for m in scorer.metrics})

    def scoreResult(self, scorer):
        results = scorer.scoreAllRecords()
        metrics = {m: results[m] for m in scorer.metrics}
        justPrint = []

        if "confusion" in scorer.results:
            justPrint.append(scorer.results["confusion"])

        return metrics, justPrint

    def getScorer(self):
        scorer = ScorerTorch(self.config.numClasses, trace=True)
        scorer.metrics = self.validationMetrics
        scorer.trace = True
        scorer.ignoreClasses = (
            [self.ignoreClassIndex] if self.ignoreClassIndex is not None else []
        )
        return scorer

    def validate(self, validationData):
        self.trigger("validationStart", self, validationData)
        model = self.model
        model.eval()
        scorer = self.getScorer()

        batchCount = len(validationData)
        processList = tqdm(enumerate(validationData), total=batchCount, disable=(not self.showProgress))
        processList.set_description("Validation")

        for batchIndex, validationBatch in processList:
            x, y = self.prepareDataAdapter(validationBatch, validation=True)

            # Run model
            with torch.no_grad():
                output = model(x)
            batchPredictions = self.mapOutputForPrediction(output)

            if len(self.validationMetrics) > 0:
                y, batchPredictions = self.prepareForScore(y, batchPredictions)

                self.scoreBatch(scorer, y, batchPredictions, processList)

            del batchPredictions
            del x
            del y
            del output
            if self.debug and batchIndex == 2:
                break

        if len(self.validationMetrics) > 0:
            metrics, justPrintMetrics = self.scoreResult(scorer)
            self.trigger("validationEnd", self, metrics, scorer)
        else:
            self.trigger("validationEnd", self, {}, scorer)


    def train(self, dataset: TrainingSetLoader):
        self.bestModelPath = None
        self.finish = False

        self.trigger("trainingStart", self, dataset)

        lossCriterion = self.getLossFunction()
        self.epoch = self.startEpoch

        while self.maxEpochs is None or self.epoch < self.maxEpochs:
            # Put in train mode

            self.model.train(True)
            self.runningStats = {"loss": 0.0}
            batchesPerEpoch = len(dataset.trainingData)
            processList = tqdm(enumerate(dataset.trainingData), total=batchesPerEpoch)
            processList.set_description(f"EPOCH {self.epoch}")

            self.optimizer.zero_grad()
    
            for batchIndex, trainBatch in processList:
                batchFeats, targs = self.prepareDataAdapter(trainBatch)

                # for batchFeat in batchFeats:
                output = self.model(batchFeats)
                output = self.mapOutputForLoss(output)
                loss = lossCriterion(output, targs)
                
                # Scale loss for gradient accumulation
                loss = loss / self.batchSizeAccumulation
                
                ownStats = hasattr(lossCriterion, "stats")

                if ownStats:
                    # processList.set_postfix(ordered_dict=lossCriterion.stats)
                    for stat, value in lossCriterion.stats.items():
                        if stat not in self.runningStats:
                            self.runningStats[stat] = value
                        else:
                            self.runningStats[stat] += value

                # Backpropagation
                loss.backward()

                if (batchIndex + 1) % self.batchSizeAccumulation == 0:
                    self.optimizer.step()
                    self.optimizer.zero_grad()

                # Perform one optimization step
                currentBatchLoss = loss.data.cpu().numpy()
                if np.isnan(currentBatchLoss):
                    self.model(batchFeats)
                    lossCriterion(output, targs)
                    raise Exception("batch loss should be a number")

                if self.batchScheduler is not None:
                    self.batchScheduler.step()

                self.runningStats["loss"] += currentBatchLoss
                self.runningStats["lr"] = self.optimizer.param_groups[0]["lr"]

                self.trigger("batchEnd", self, batchIndex)

                del output
                del targs
                del loss
                currentCount = processList.n + 1
                processList.set_postfix(
                    ordered_dict={
                        n: v / currentCount for n, v in self.runningStats.items()
                    }
                )
                
                if self.debug and batchIndex == 2:
                    break

            # Handle any remaining accumulated gradients at the end of the epoch
            if (batchesPerEpoch) % self.batchSizeAccumulation != 0:
                self.optimizer.step()
                self.optimizer.zero_grad()

            self.runningStats = {
                n: v / batchesPerEpoch for n, v in self.runningStats.items()
            }

            self.epoch += 1

            if not self.skipValidation:
                self.validate(dataset.validationData)

            if self.finish:
                break

        self.trigger("trainingEnd", self)

        self.fullEpochs = self.epoch
        self.trigger("trainEnd", self)
        if self.bestModelPath is not None:
            self.log("load best Model: %s" % self.bestModelPath)
            self.loadState(self.load(self.bestModelPath))
        return self.model

    def getModelPath(self):
        return self.logPath

    def build(self):
        torchSeed = 2
        torch.manual_seed(torchSeed)

        if self.useGPU:
            torch.cuda.manual_seed(torchSeed)
            self.model.cuda()

    def summary(self) -> str:
        pytorch_total_params = sum(
            p.numel() for p in self.model.parameters() if p.requires_grad
        )
        self.log("Total trainable Parameters: %i" % (pytorch_total_params))
        self.parameter = pytorch_total_params

        return str(self.model)

    def cleanUp(self):
        if self.useGPU:
            torch.cuda.empty_cache()

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        return torch.load(
            path,
            map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        )

    def loadState(self, state):
        if isinstance(state, torch.nn.Module):
            state = state.state_dict()
        return self.model.load_state_dict(state)

    def mapOutputForLoss(self, output):
        return output

    def predict(self, input, get_likelihood=False, returnNumpy=True):
        with torch.no_grad():
            if not torch.is_tensor(input):
                input = torch.tensor(input)

            batchSize = input.shape[0]

            if self.useGPU:
                input = input.cuda()

            input = self.prepareX(input)
            model = self.getModelEval()
            out = model(input)

            predictions = self.mapOutputForPrediction(out)

            if self.config.numClasses > 0 and self.oneHotDecoded:
                predictions = predictions.reshape(batchSize, -1, self.config.numClasses)

                if not get_likelihood:
                    predictions = torch.argmax(predictions, dim=2)

            if returnNumpy:
                predictions = predictions.detach().cpu().numpy()

            return predictions
