import math
import numpy as np
from pyPhases import classLogger


class NotUniqueException(Exception):
    pass


class NotCompleteException(Exception):
    pass

class SplitsMisconfiguredException(Exception):
    pass


@classLogger
class DataversionManager:
    def __init__(self, groupedRecords, splits=None, seed=None) -> None:
        splits = {} if splits is None else splits

        self.splits = self.normalizeSlicesDict(splits)
        self.seed = seed
        self.removedRecords = {}
        self.splitHasSubs = []

        self.remainingSplit = None

        # shuffle the records
        groups = list(groupedRecords.keys())
        self.unShuffledgroupedRecords = groupedRecords
        if seed is not None:
            np.random.seed(seed)
            np.random.shuffle(groups)
            groupedRecords = {g: groupedRecords[g] for g in groups}

        self.groupedRecords = groupedRecords

    def normalizeSlices(self, slices):
        slices = slices if isinstance(slices, list) else [slices]
        splitSlices = []

        for splitSlice in slices:
            splitSlice = (
                slice(*[int(index) for index in splitSlice.split(":")])
                if isinstance(splitSlice, str)
                else splitSlice
            )
            splitSlices.append(splitSlice)
        return splitSlices

    def normalizeSlicesDict(self, slices):
        return {k: self.normalizeSlices(v) for k, v in slices.items()}

    def addSplitBySlices(self, name, slices):
        self.splits[name] = self.normalizeSlices(slices)

    def addSplitsByFold(
        self,
        mainSplit: str,
        foldSplit: str,
        recordSlice: slice | str,
        foldCount: int,
        currentFold: int,
    ):
        if currentFold >= foldCount:
            raise SplitsMisconfiguredException(
                "Fold %i is higher than fold count %i" % (currentFold, foldCount)
            )

        subSlice, mainSlice = self.getSplitsByPercentage(
            recordSlice, subLength=1 / foldCount, subPosition=currentFold
        )

        self.addSplitBySlices(foldSplit, subSlice)
        self.addSplitBySlices(mainSplit, mainSlice)

    def getSplitsByPercentage(
        self, recordSlice: slice | str, subLength, subPosition=0, ceil=True
    ):
        recordSlice = self.normalizeSlices(recordSlice)[0]
        recordSliceLength = recordSlice.stop - recordSlice.start
        subLength = (
            math.ceil(subLength * recordSliceLength)
            if ceil
            else math.floor(subLength * recordSliceLength)
        )
        subSlice = slice(
            recordSlice.start + int(subLength * subPosition),
            recordSlice.start + int(subLength * (subPosition + 1)),
        )

        if subPosition == 0:
            mainSlice = slice(subSlice.stop, recordSlice.stop)
        else:
            mainSlice = [
                slice(recordSlice.start, subSlice.start),
                slice(subSlice.stop, recordSlice.stop),
            ]

        return subSlice, mainSlice

    def getRemainingSplit(self):
        if len(self.splits) == 0:
            return slice(0, len(self.groupedRecords))
        elif len(self.splits) == 1:
            curSplit = list(self.splits.values())[0]
            if isinstance(curSplit, list):
                if len(curSplit) > 1:
                    raise SplitsMisconfiguredException(
                        "Getting the remaining split only works one slice per split"
                    ) 
                curSplit = curSplit[0]
            if curSplit.start == 0:
                return slice(curSplit.stop, len(self.groupedRecords))
            elif curSplit.stop == len(self.groupedRecords):
                return slice(0, curSplit.start)
            else:
                raise SplitsMisconfiguredException(
                    "Current split is not at the beginning or end of the dataset"
                )
        else:
            raise SplitsMisconfiguredException(
                "Remaining splits can only be used if there is only one split."
            )

    def addSplitByRemaining(self, name: str, percentage: float, ceil=True):
        remainingSplit = (
            self.getRemainingSplit()
            if self.remainingSplit is None
            else self.remainingSplit
        )
        recordCount = remainingSplit.stop - remainingSplit.start
        length = (
            math.ceil(recordCount * percentage)
            if ceil
            else math.floor(recordCount * percentage)
        )
        split = slice(remainingSplit.start, remainingSplit.start + length)

        self.remainingSplit = slice(split.stop, remainingSplit.stop)

        self.addSplitBySlices(name, split)

    def groupDatasetBySplit(
        self, datasetName, splits, groupedRecords, removedRecords=None
    ):
        split = splits[datasetName]
        # check if split is a list of recordids
        if isinstance(split, dict):
            mainSplit = split["mainsplit"]
            mainRecordIds = self.getRecordsForSplit(mainSplit)
            recordIds = [mainRecordIds[i] for i in split["indexes"]]
        else:
            splits = self.normalizeSlicesDict(splits)
            slicesForDataset = (
                splits[datasetName]
                if isinstance(splits[datasetName], list)
                else self.normalizeSlices(splits[datasetName])
            )
            # get record ids for splits and flatten
            groupIds = [
                recordId
                for s in slicesForDataset
                for recordId in list(groupedRecords.keys())[s]
            ]
            recordIds = [
                record for group in groupIds for record in groupedRecords[group]
            ]

        if bool(removedRecords):
            recordIds = [
                record
                for index, record in enumerate(recordIds)
                if index not in removedRecords
            ]

        return recordIds

    def groupDatasetsBySplit(self, datasetNames, splits, groupedRecords):
        recordSlices = {}
        for datasetName in datasetNames:
            recordSlices[datasetName] = self.groupDatasetBySplit(
                datasetName, splits, groupedRecords
            )

        return recordSlices

    def getRecordsForSplit(self, datasetName):
        removedRecords = self.removedRecords.get(datasetName, None)
        return self.groupDatasetBySplit(
            datasetName, self.splits, self.groupedRecords, removedRecords
        )

    def getRecordIndexesForSplit(self, datasetName):
        removedRecords = self.removedRecords.get(datasetName, None)
        recordIds = self.groupDatasetBySplit(
            datasetName, self.splits, self.groupedRecords, removedRecords
        )
        flattenAllRecords = [r for elem in self.groupedRecords.values() for r in elem]
        return [flattenAllRecords.index(r) for r in recordIds]

    def validatDatasetVersion(self, raiseException=True):
        allDBRecordIds = self.groupedRecords
        # remove splits keys that have subsplits
        splits = {k: v for k, v in self.splits.items() if k not in self.splitHasSubs}
        datasetNames = list(splits.keys())

        recordSlices = self.groupDatasetsBySplit(datasetNames, splits, allDBRecordIds)

        flattenAllRecords = [r for elem in allDBRecordIds.values() for r in elem]
        flattenUsedRecords = [r for elem in recordSlices.values() for r in elem]

        # check if all records are unique and present in the dataset splits
        complete = len(flattenAllRecords) == len(flattenUsedRecords)
        unique = len(flattenUsedRecords) == len(set(flattenUsedRecords))
        if not unique:
            error = "There are duplicate records in the dataset splits "
            self.logError(error)
            if raiseException:
                raise NotUniqueException(error)

        if not complete:
            error = (
                "Not all records are used (%i records are missing), overall %s groups"
                % (
                    len(flattenAllRecords) - len(flattenUsedRecords),
                    len(allDBRecordIds.keys()),
                )
            )
            self.logError(error)

            if raiseException:
                raise NotCompleteException(error)

        if complete and unique:
            self.logSuccess("All records are unique and present in the dataset splits")

    def removeRecordIndexesFromSplit(self, datasetName, recordIndexes):
        self.removedRecords[datasetName] = recordIndexes

    def addVirtualSplitByMainSplitIndexes(self, mainsplit, datasetName, recordIndexes):
        self.splitHasSubs.append(mainsplit)
        self.splits[datasetName] = {
            "mainsplit": mainsplit,
            "indexes": list(recordIndexes),
        }

    def getAllRecordIds(self):
        flattenIds = [
            r
            for subgroup in self.unShuffledgroupedRecords.values()
            for r in subgroup
        ]
        return flattenIds