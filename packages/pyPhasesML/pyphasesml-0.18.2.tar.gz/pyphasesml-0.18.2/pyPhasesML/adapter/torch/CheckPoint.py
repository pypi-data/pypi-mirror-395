from pathlib import Path
import pickle
import timeit

from pyPhases import classLogger

from pyPhasesML.adapter.torch.Callback import Callback
from pyPhasesML.Model import ModelConfig


@classLogger
class CheckPoint(Callback):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__(config)
        self.metricDefinitions = None
        self.notImprovedSince = 0
        self.scorer = None
        if config.scorer is not None:
            from pyPhasesML.scorer.ScorerTorch import ScorerTorch

            self.scorer = ScorerTorch(config.numClasses)

    def onTrainingStart(self, model, dataset):
        self.epochStartTime = timeit.default_timer()
        
        self.metricDefinitions = None
        self.notImprovedSince = 0

    def onValidationStart(self, model, dataset):
        self.epochEndTime = timeit.default_timer()

    def prettyPrintConfusionMatrix(self, confusion_matrix):
        num_rows, num_cols = confusion_matrix.shape
        max_value_length = max(len(str(confusion_matrix.max())), len(str(confusion_matrix.min())))
        separator = "-" * ((max_value_length + 2) * num_cols)

        rows = []
        for i in range(num_rows):
            row_data = [f"{int(confusion_matrix[i, j]):>{max_value_length}}" for j in range(num_cols)]
            rows.append(" | ".join(row_data))

        print(separator)
        print("\n".join(rows))
        print(separator)

    def onValidationEnd(self, model, results, scorer):
        metricsValues = {m: results[m] for m in scorer.metrics}
        metricDiffStrings = []
        metricValuetrings = []
        improved = False
        modelId = "checkpointModel_%i_" % model.epoch

        if self.metricDefinitions is None:
            self.metricDefinitions = {m: scorer.getMetricDefinition(m) for m in metricsValues.keys()}

        globalBestMetric = model.validationMetrics[0]

        metricStrings = []
        for metricName, metricVal in metricsValues.items():
            bestValue, useAsBest, biggerIsBetter = self.metricDefinitions[metricName]
            diff = metricVal - bestValue
            metricStrings.append(f"{metricName}: " + "{:.3f}".format(metricVal) + " [best: {:.3f}]".format(bestValue))
            metricDiffStrings.append(f"{metricName}: " + "{:.3f}".format(diff))
            metricValuetrings.append("{:.3f}".format(metricVal))

            isBigger = metricVal > bestValue

            if (biggerIsBetter and isBigger) or (not biggerIsBetter and not isBigger):
                self.metricDefinitions[metricName][0] = metricVal
                if useAsBest:
                    improved = True
                    if metricName == globalBestMetric:
                        model.bestMetric = max(model.bestMetric, metricsValues[globalBestMetric])

        validationEndTime = timeit.default_timer()

        epochTime = str(self.epochEndTime - self.epochStartTime)
        validationTime = str(validationEndTime - self.epochStartTime)
        self.log(f"Validation-Epoch Number: {str(model.epoch)}  Epoche Time: {epochTime}  Validation Time: {validationTime}")
        if model.useGPU:
            import torch
            self.log(f"Max GPU memory usage: {torch.cuda.max_memory_allocated() / (1024 ** 3):.2f} GB")

        if "confusion" in scorer.results:
            self.prettyPrintConfusionMatrix(scorer.results["confusion"])

        trainingStats = " | ".join([f"{n}:{v}" for n, v in model.runningStats.items()])
        self.log(f"Training Stats: {trainingStats} ")
        self.log(" ".join(metricStrings))

        if improved:
            self.log("Model Improved: " + " ".join(metricDiffStrings))
            path = f"{self.getLogPath()}/{modelId}" + "_".join(metricValuetrings) + ".pkl"
            with open(path, "wb") as f:
                import torch
                torch.save(model.model.state_dict(), f)
            self.notImprovedSince = 0
            model.bestModelPath = path
        else:
            self.notImprovedSince += 1
            self.log("Model not improving since %i epochs" % (self.notImprovedSince))

        if self.config.stopAfterNotImproving > 0 and self.notImprovedSince >= self.config.stopAfterNotImproving:
            model.finish = True

        model.metricDefinitions = self.metricDefinitions

    def getCheckpointFile(self):
        return Path(self.getLogPath(), ".resumeCheckpoint.pt")

    def onCheckpoint(self, model):

        with open(self.getCheckpointFile(), "wb") as f:
            pickle.dump({
                "notImprovedSince": self.notImprovedSince,
                "metricDefinitions": self.metricDefinitions,
                "bestModelPath": model.bestModelPath,
            }, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    def onRestore(self, model):
        if not self.getCheckpointFile().exists():
            return

        with open(self.getCheckpointFile(), "rb") as f:
            state = pickle.load(f)
            self.notImprovedSince = state["notImprovedSince"]
            self.metricDefinitions = state["metricDefinitions"]
            model.metricDefinitions = state["metricDefinitions"]
            model.bestModelPath = state["bestModelPath"]
