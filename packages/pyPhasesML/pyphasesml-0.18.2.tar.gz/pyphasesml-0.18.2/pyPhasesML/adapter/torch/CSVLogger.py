from pyPhases import classLogger
from pyPhasesML.adapter.torch.Callback import Callback

from pyPhases import CSVLogger as Logger


@classLogger
class CSVLogger(Callback):
    def getCsvPath(self):
        return f"{self.config.logPath}/{self.config.csvLogFile}"

    def onTrainingStart(self, model, dataset):
        self.logger = Logger(self.getCsvPath())

    def onValidationEnd(self, model, results, scorer):
        csvRow = {
            "epoch": model.epoch,
        }

        csvRow.update(model.runningStats)
        metricsValues = {m: results[m] for m in scorer.metrics}

        for metricName in metricsValues:
            csvRow[f"val_{metricName}"] = metricsValues[metricName]

        self.logger.addCsvRow(csvRow)
