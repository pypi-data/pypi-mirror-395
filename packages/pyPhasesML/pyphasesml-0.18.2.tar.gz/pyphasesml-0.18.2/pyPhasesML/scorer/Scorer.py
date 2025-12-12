import itertools
import numpy as np


def confusion_matrix(true, pred, labels=None):
    """Compute confusion matrix from truth and prediction"""
    if labels is None:
        labels = np.unique(np.concatenate([true, pred]))

    assert true.shape == pred.shape

    size = len(labels)
    classes = np.arange(size)
    confmat = np.zeros((size, size))

    for i, j in itertools.product(range(size), range(size)):
        confmat[i, j] = ((true == classes[i]) & (pred == classes[j])).sum()

    return confmat


class Scorer:
    title = "Segmentbasiert"
    cmScaleByClass = 4
    addedMetrics = {}

    def __init__(self, numClasses=2, classNames=None, trace=False, threshold=None) -> None:
        self.metrics = ["kappa", "accuracy"]
        self.ignoreClasses = []
        self.numClasses = numClasses if classNames is None else len(classNames)
        self.classNames = list(range(numClasses)) if classNames is None else classNames
        self.recordResult = {}
        self.recordIndex = 0
        self.trace = trace
        self.possibleValues = None
        self.addEvents = False
        self.mapping = None
        self.threshold = threshold

    def reset(self):
        self.recordResult = {}
        self.recordIndex = 0

    def getMetricDefinition(self, name):
        metricDefinition = {
            # init value, useAsBest, biggerIsBetter
            "AUC": [0.5, False, True],
            "AP": [0.0, True, True],
            "accuracy": [0.0, False, True],
            "acc": [0.0, False, True],
            "kappa": [-1, True, True],
            "f1": [-1, True, True],
            "micro_f1": [-1, True, True],
            "CSI": [0, True, True],
            "meanSquared": [np.inf, True, False],
            "SNR": [np.inf, False, False],
            "confusion": [np.inf, False, False],
            "auroc": [0.0, False, True],
            "auprc": [0.0, True, True],
            "eventCountDiff": [np.inf, False, False],
            "positiveErrorRatio": [np.inf, True, False],
        }

        if name in Scorer.addedMetrics:
            metric = Scorer.addedMetrics[name]
            return [metric["initValue"], metric["useAsBest"], metric["biggerIsBetter"]]

        return metricDefinition[name]

    @staticmethod
    def registerMetric(metricName, metricFunction, combineFunction, biggerIsBetter=True, useAsBest=True, initValue=None):
        Scorer.addedMetrics[metricName] = {
            "score": metricFunction,
            "combine": combineFunction,
            "biggerIsBetter": biggerIsBetter,
            "useAsBest": useAsBest,
            "initValue": initValue if initValue is not None else 0.0 if biggerIsBetter else np.inf,
        }

    def getMetricName(self, metricName):
        return metricName

    def prepareInput(self, inputArray):
        """can be overwritten to tranform tensors to numpy"""
        return inputArray

    def preparePrediction(self, inputArray):
        # for classification task the shape can be (recordcount?, predictions, classCount)
        isOneHotEncode = inputArray.shape[-1] == self.numClasses
        return inputArray.reshape(-1, self.numClasses) if isOneHotEncode else inputArray.reshape(-1, 1)

    def prepareTruth(self, inputArray):
        """flatten and squeeze the truth array"""
        isOneHotEncode = inputArray.shape[-1] == self.numClasses

        if isOneHotEncode:
            maskedIgnored = inputArray.sum(axis=-1) == 0
            inputArray = np.argmax(inputArray, axis=-1)
            inputArray[maskedIgnored] = -1

        return inputArray.reshape(-1)

    def score(self, truth, prediction, recordName=None, trace=True):
        prediction = self.prepareInput(prediction)
        truth = self.prepareInput(truth)
        prediction = self.preparePrediction(prediction)
        truth = self.prepareTruth(truth)

        truthOrg, predictionOrg = truth, prediction
        truth, prediction = self.maskedIgnoredValues(truth, prediction)

        metrics = self.scoreMetrics(truth, prediction)
        if self.trace and trace:
            if recordName is None:
                recordName = self.recordIndex

            self.recordResult[recordName] = self.recordEntry(truthOrg, predictionOrg, self.results, recordName)

            self.recordIndex += 1

        return metrics

    def recordEntry(self, truth, prediction, metrics, recordName=None):
        entry = {
            "truth": truth,
            "prediction": prediction,
        }
        entry.update(metrics)
        return entry

    def combineMetric(self, metricName):
        metricName = self.getMetricName(metricName)

        result = None

        if metricName in self.addedMetrics:
            truth = np.concatenate([self.recordResult[id]["truth"] for id in self.recordResult], axis=0)
            prediction = np.concatenate([self.recordResult[id]["prediction"] for id in self.recordResult], axis=0)
            self.results[metricName] = self.addedMetrics[metricName]["combine"](truth, prediction)
        if metricName in ["kappa", "accuracy"]:  # recalcuate from confusion
            self.combineMetric("confusion")
            self.scoreMetric("kappa", None, None)
        if metricName in ["f1", "micro_f1"]:  # recalcuate from confusion
            self.combineMetric("confusion")
            self.scoreMetric(metricName, None, None)
        elif metricName == "confusion":  # combine all confusion
            result = np.array(
                [self.recordResult[id]["confusion"] for id in self.recordResult if len(self.recordResult[id]["confusion"]) > 0]
            ).sum(axis=0)
        elif metricName in ["auprc", "auroc"]:
            if self.numClasses != 2:
                raise Exception("Metric auprc, auroc only support binary classification at the moment")

            self.results["all_values"] = np.array([self.recordResult[id]["all_values"] for id in self.recordResult]).sum(axis=0)
            self.results["pos_values"] = np.array([self.recordResult[id]["pos_values"] for id in self.recordResult]).sum(axis=0)
            self.results["ign_values"] = np.array([self.recordResult[id]["ign_values"] for id in self.recordResult]).sum(axis=0)

            # Compute the histogram of probabilities
            # given the above
            self.results["neg_values"] = self.results["all_values"] - self.results["pos_values"] - self.results["ign_values"]
            auroc, auprc, _, _, _ = self._auc(self.results["pos_values"], self.results["neg_values"])
            self.results["auprc"] = np.sum(auprc)
            self.results["auroc"] = np.sum(auroc)
        elif metricName in ["eventCountDiff"]: # median/quantiles
            metricList = [self.recordResult[id][metricName] for id in self.recordResult]
            self.results[metricName] = np.median(metricList)
            self.results[f"{metricName}-q1"] = np.quantile(metricList, 0.25)
            self.results[f"{metricName}-q3"] = np.quantile(metricList, 0.75)
        elif metricName in [
            "meanSquared",
            "rootMeanSquared",
            "prd",
            "countTruth",
            "countPred",
            "overlappingCount",
            "positiveErrorRatio",
            "fm",
            "CSI",
            "SNR",
        ]:  # mean over all records
            sum = np.sum([self.recordResult[id][metricName] for id in self.recordResult])
            self.results[metricName] = sum / len(self.recordResult)

        if result is not None:
            self.results[metricName] = result

        return self.results[metricName]

    def combineMetrics(self):
        self.results = {}
        returnMetrics = {}
        for metricName in self.metrics:
            returnMetrics[metricName] = self.combineMetric(metricName)

        return returnMetrics

    def scoreAllRecords(self):
        if self.trace is False:
            raise Exception("The scorer does not keep the scored record, set the scorer.trace to True to keep all the results")
        self.combineMetrics()
        return self.results

    def maskedIgnoredValues(self, truth, prediction):
        """remove all values that are ignored (by ignoreClasses) from the truth and prediction, truth needs to be non one hot encoded"""

        for ignore in self.ignoreClasses:
            keep = truth != ignore

            truth = truth[keep]
            prediction = prediction[keep]

        return truth, prediction

    def scoreMetrics(self, truth, prediction):
        self.results = {}
        returnMetrics = {}
        for metricName in self.metrics:
            returnMetrics[metricName] = self.scoreMetric(metricName, truth, prediction)

        return returnMetrics

    def isHotEncoded(self, y):
        return y.shape[-1] == self.numClasses

    def calculateKappaAccFromConfusion(self, confusion):
        # implementation from sklearn
        n_classes = confusion.shape[0]
        sum0 = np.sum(confusion, axis=0)
        sum1 = np.sum(confusion, axis=1)
        if np.sum(sum0) == 0:
            return 0, 0
        expected = np.outer(sum0, sum1) / np.sum(sum0)

        w_mat = np.ones([n_classes, n_classes], dtype=np.int32)
        w_mat.flat[:: n_classes + 1] = 0

        nonDiag = np.sum(w_mat * confusion)
        if nonDiag == 0:
            k = 1
            acc = 1
        else:
            k = 1 - (nonDiag / np.sum(w_mat * expected))
            acc = 1 - (nonDiag / np.sum(confusion))

        return k, acc

    def getClassLikelyhood(self, prediction):
        max = np.max(prediction, axis=1, keepdims=True)
        if self.isHotEncoded(prediction):
            e_x = np.exp(prediction - max)
            sum = np.sum(e_x, axis=1, keepdims=True)  # returns sum of each row and keeps same dims
            predictionSoftMax = e_x / sum
            classLikelyhood = predictionSoftMax[:, 1]
        else:
            if any(max > 1) or any(max < 0):
                # transform to probability
                max = 1 / (1 + np.exp(-max))
            classLikelyhood = max.reshape(-1)
        return classLikelyhood

    def getClassPrediction(self, prediction):
        likelyhood = self.getClassLikelyhood(prediction)
        binPrediction = np.full(prediction.shape[0], 0)
        binPrediction[likelyhood > self.threshold] = 1
        return binPrediction

    def flattenPrediction(self, prediction, binaryLikelyHood=False, threshold=None):
        if binaryLikelyHood and self.numClasses != 2:
            raise Exception("Selected metric only support binary classification at the moment")
        useThreshold = threshold is not None and self.numClasses <= 2

        if useThreshold:
            return self.getClassPrediction(prediction)

        if self.isHotEncoded(prediction):
            binPrediction = prediction.argmax(-1)
        else:
            threshhold = self.threshold if useThreshold is None else 0.5
            binPrediction = prediction.copy().reshape(-1)
            if self.numClasses > 2:
                binPrediction = np.floor(binPrediction)
                binPrediction[binPrediction == self.numClasses] = self.numClasses - 1
                return np.floor(binPrediction)
            else:
                binPrediction[binPrediction >= threshhold] = 1
                binPrediction[binPrediction < threshhold] = 0
        return binPrediction

    def getMetricScorer(self, metricName, predictionFirst=False):
        def score(truth, prediction):
            if predictionFirst:
                truth, prediction = prediction, truth
            prediction = self.prepareInput(prediction)
            truth = self.prepareInput(truth)
            prediction = self.preparePrediction(prediction)
            truth = self.prepareTruth(truth)
            self.results = {}
            return self.scoreMetric(metricName, truth, prediction)

        score.__name__ = metricName
        return score

    def scoreMetric(self, metricName, truth, prediction):
        metricName = self.getMetricName(metricName)

        if metricName in self.results:
            return self.results[metricName]

        result = None

        if metricName in self.addedMetrics:
            self.results[metricName] = self.addedMetrics[metricName]["score"](truth, prediction)
        elif metricName in ["kappa", "accuracy"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            k, acc = self.calculateKappaAccFromConfusion(confusion)
            self.results["accuracy"] = acc
            self.results["kappa"] = k
        elif metricName in ["f1"]:
            f1s = []
            confusion = self.scoreMetric("confusion", truth, prediction)
            startAt = 1 if self.numClasses == 2 else 0
            for i in range(startAt, self.numClasses):
                # first = truth, second = predicted
                tp = confusion[i][i]
                fp = sum(confusion[i, :]) - tp
                fn = sum(confusion[:, i]) - tp
                f1 = tp / (tp + 0.5 * (fp + fn)) if tp + fp + fn > 0 else 1
                self.results["f1-%i" % i] = f1
                f1s.append(f1)
            self.results["f1"] = np.mean(f1s)
        elif metricName in ["micro_f1"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            startAt = 0  # micro F1 always includes all classes
            # Calculate total TP, FP, FN across all classes
            total_tp = 0
            total_fp = 0
            total_fn = 0
            for i in range(startAt, self.numClasses):
                tp = confusion[i][i]
                fp = sum(confusion[i, :]) - tp
                fn = sum(confusion[:, i]) - tp
                total_tp += tp
                total_fp += fp
                total_fn += fn
            # Calculate micro F1 score
            self.results["micro_f1"] = total_tp / (total_tp + 0.5 * (total_fp + total_fn)) if total_tp + total_fp + total_fn > 0 else 1
        elif metricName == "confusion":
            prediction = self.flattenPrediction(prediction, threshold=self.threshold)
            result = confusion_matrix(
                truth, prediction, labels=range(self.numClasses)
            )  # , labels=range(self.numClasses) # HPC comp
            assert result.sum() == len(truth)
        elif metricName in ["auprc", "auroc"]:
            classLikelyhood = self.getClassLikelyhood(prediction)

            scale = 10**3
            b = scale + 1
            r = (-0.5 / scale, 1.0 + 0.5 / scale)

            self.results["all_values"] = np.histogram(classLikelyhood, bins=b, range=r)[0]

            pred_pos = classLikelyhood[truth > 0]
            self.results["pos_values"] = np.histogram(pred_pos, bins=b, range=r)[0]

            # Compute the histogram of probabilities within unscored regions
            pred_ign = classLikelyhood[truth < 0]
            self.results["ign_values"] = np.histogram(pred_ign, bins=b, range=r)[0]

            # Compute the histogram of probabilities in non-arousal regions,
            # given the above
            self.results["neg_values"] = self.results["all_values"] - self.results["pos_values"] - self.results["ign_values"]
            auroc, auprc, _, _, _ = self._auc(self.results["pos_values"], self.results["neg_values"])
            self.results["auprc"] = np.sum(auprc)
            self.results["auroc"] = np.sum(auroc)
        elif metricName in ["meanSquared", "rootMeanSquared", "prd"]:
            if prediction.shape[1] > 1:
                diag = np.eye(self.numClasses)
                truth = diag[truth]
            else:
                prediction = self.getClassLikelyhood(prediction)
            squared = np.square(truth - prediction)
            meanSquared = squared.mean() if len(truth) > 0 else 0
            if metricName == "meanSquared":  # MS
                self.results[metricName] = meanSquared
            elif metricName == "rootMeanSquared":  # RMS
                self.results[metricName] = np.sqrt(meanSquared)
            elif metricName == "prd":  # Percentage RMS Difference
                self.results[metricName] = 100 * np.sqrt(squared.sum() / (np.square(truth).sum()))
        elif metricName in ["countTruth"]:
            truthCount = np.sum(np.diff(truth) > 0)
            self.results[metricName] = truthCount
        elif metricName in ["countPred"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            predCount = np.sum(np.diff(classPrediction) > 0)
            self.results[metricName] = predCount
        elif metricName in ["eventCountDiff"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            predCount = np.sum(np.diff(classPrediction) > 0)
            truthCount = np.sum(np.diff(truth) > 0)
            self.results[metricName] = int(np.abs(predCount - truthCount))
        elif metricName in ["overlappingCount"]:
            classPrediction = self.flattenPrediction(prediction, threshold=self.threshold)
            overlap = classPrediction + truth
            count = np.diff(overlap == 2).sum() / 2  # only count every up change
            self.results[metricName] = count
        elif metricName in ["positiveErrorRatio"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            tp = confusion[-1][-1]
            tn = confusion[0][0]
            f = np.sum(confusion) - tp - tn
            self.results[metricName] = f / tp if tp > 0 else 0
        elif metricName in ["CSI"]:
            confusion = self.scoreMetric("confusion", truth, prediction)
            tp = confusion[-1][-1]
            tn = confusion[0][0]
            f = np.sum(confusion) - tp - tn
            self.results[metricName] = tp / (tp + f)
        elif metricName == "SNR":  # signal to noise ratio
            axis = 0
            ddof = 0
            a = np.asanyarray(prediction)
            m = a.mean(axis)
            sd = a.std(axis=axis, ddof=ddof)
            self.results[metricName] = np.where(sd == 0, 0, m / sd)
        elif metricName == "fm":  # Fowlkes–Mallows index
            confusion = self.scoreMetric("confusion", truth, prediction)
            (tn, fn), (fp, tp) = confusion

            tp = confusion[-1][-1]
            tn = confusion[0][0]
            ppv = tp / (tp + fp)
            tpr = tp / (tp + fn)

            self.results[metricName] = np.sqrt(ppv * tpr)
        if result is not None:
            self.results[metricName] = result

        return self.results[metricName]

    def _auc(self, pos_values, neg_values):
        # Calculate areas under the ROC and PR curves by iterating
        # over the possible threshold values.

        # At the minimum threshold value, all samples are classified as
        # positive, and thus TPR = 1 and TNR = 0.
        tp = np.sum(pos_values)
        fp = np.sum(neg_values)
        tn = fn = 0
        tpr = 1
        tnr = 0
        if tp == 0 or fp == 0:
            # If either class is empty, scores are undefined.
            return (
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
                float("nan"),
            )
        ppv = float(tp) / (tp + fp)
        auroc = []
        auprc = []
        tpr_arr = []
        fpr_arr = []
        precisions = []

        # As the threshold increases, TP decreases (and FN increases)
        # by pos_values[i], while TN increases (and FP decreases) by
        # neg_values[i].
        for n_pos, n_neg in zip(pos_values, neg_values):
            tp -= n_pos
            fn += n_pos
            fp -= n_neg
            tn += n_neg
            tpr_prev = tpr
            tnr_prev = tnr
            ppv_prev = ppv
            tpr = float(tp) / (tp + fn)  # recall
            tnr = float(tn) / (tn + fp)
            fpr = float(fp) / (fp + tn)

            if tp + fp > 0:
                ppv = float(tp) / (tp + fp)  # precision
            else:
                ppv = ppv_prev

            auroc.append((tpr_prev - tpr) * (tnr + tnr_prev) * 0.5)
            auprc.append((tpr_prev - tpr) * ppv_prev)

            tpr_arr.append(tpr)
            fpr_arr.append(fpr)
            precisions.append(ppv)
        return (auroc, auprc, tpr_arr, fpr_arr, precisions)
