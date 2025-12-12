import tensorflow as tf

from .Scorer import Scorer


class ScorerTF(Scorer):
    def prepareInput(self, inputArray):
        if tf.is_tensor(inputArray):
            inputArray = inputArray.numpy()
            
        return inputArray