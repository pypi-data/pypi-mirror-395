import torch
from .Scorer import Scorer


class ScorerTorch(Scorer):
    def beforeLoss(self, x, y):
        return torch.from_numpy(x), torch.from_numpy(y)

    def prepareInput(self, inputArray):
        if isinstance(inputArray, torch.Tensor):
            inputArray = inputArray.detach().cpu().numpy()
        return inputArray
