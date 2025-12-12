from pyPhasesML import ModelAdapter
import tensorflow as tf
import keras as K
import numpy as np

from ..DataSet import TrainingSet


# K.set_image_data_format("channels_last")


class ModelTf1Adapter(ModelAdapter):
    model = None

    def _metrics(self, metric, validation=False):
        prepend = "val_" if validation else ""
        return prepend + metric["name"]

    def beforeTrain(self, dataset):
        # from tensorflow.keras.models import load_model
        if "loadModelPath" in self.options:
            loadedModel = tf.keras.models.load_model(self.options["loadModelPath"])
            try:
                self.model.set_weights(loadedModel.get_weights())
            except Exception:
                raise Exception
        if hasattr(self, "freeze"):
            layers_freeze = self.freeze
            # len(self.model.layers)
            for layer in self.model.layers[:layers_freeze]:
                layer.trainable = False
        return

    def train(self, dataset: TrainingSet):
        callbacks = []
        mainMetric = self.validationMetrics[0]
        metricStop = self.getMetric(mainMetric)
        metricSave = self.getMetric(mainMetric)

        # tensorboard_callback = K.callbacks.TensorBoard(
        #     log_dir=self.logPath + "/tb",
        #     histogram_freq=1,
        # )
        # callbacks.append(tensorboard_callback)

        if self.config.stopAfterNotImproving is not None:
            earlyStopping_cb = K.callbacks.EarlyStopping(
                monitor=self._metrics(metricStop, True),
                patience=self.config.stopAfterNotImproving,
                verbose=0,
                mode=metricStop["type"],
                # baseline=None,
                # restore_best_weights=True,
            )
            callbacks.append(earlyStopping_cb)

        if self.learningRateDecay is not None:
            lr_decay_cb = K.callbacks.LearningRateScheduler(
                schedule=lambda epoch: self.learningRate * (self.learningRateDecay ** epoch)
            )
            callbacks.append(lr_decay_cb)

        log = K.callbacks.CSVLogger(self.getCsvPath())
        callbacks.append(log)

        checkpoint = K.callbacks.ModelCheckpoint(
            self.logPath + "/weights-{epoch:02d}.h5",
            monitor=self._metrics(metricSave, True),
            mode=metricSave["type"],
            save_best_only=True,
            save_weights_only=True,
            verbose=0,
        )
        callbacks.append(checkpoint)
        classWeight = None if self.classWeights is None else dict(list(zip(range(6), self.classWeights)))

        batchesPerEpoch = len(dataset.trainingData)
        validationBatchesPerEpoch = len(dataset.validationData)
        # train = dataset.trainingData.generator(wrapper=self.prepareData)
        # validationData = dataset.validationData.generator(wrapper=self.prepareData)

        def combine(dataset):
            dataset.continous = False
            recordsX = []
            recordsY = []
            for r in dataset:
                recordsX.append(r.x)
                recordsY.append(r.y)

            recordsX = np.concatenate(recordsX)
            recordsY = np.concatenate(recordsY)

            return recordsX, recordsY

        trainX, trainY = combine(dataset.trainingData)
        valX, valY = combine(dataset.validationData)

        self.cleanCsv()
        self.model.fit(
            [trainX, trainY],
            [trainY, trainX],  # capsnet specific
            validation_data=[[valX, valY], [valY, valX]],  # capsnet specific
            # steps_per_epoch=batchesPerEpoch,
            # validation_steps=validationBatchesPerEpoch,
            class_weight=classWeight,
            batch_size=self.batchSize,
            shuffle=False,
            verbose=1,
            epochs=self.maxEpochs,
            callbacks=callbacks,
        )

        metricHistory = self.model.history.history["val_capsnet_acc"]  # capsnet specific
        self.bestMetric = max(metricHistory)
        self.fullEpochs = len(metricHistory)
        return self.model

    def eval(model, data):
        x_test, y_test = data
        y_pred, x_recon = model.predict(x_test, batch_size=64)
        print("-" * 50)
        print(
            "Test acc:",
            np.sum(np.argmax(y_pred, 1) == np.argmax(y_test, 1)) / y_test.shape[0],
        )
        import matplotlib.pyplot as plt

        plt.figure()
        plt.subplot(211)
        plt.plot(x_recon[16], "b-")
        plt.title("Reconstruction")

        plt.figure()
        plt.subplot(212)
        plt.plot(x_test[16])
        plt.title("Original")

    def build(self):
        optimizer = None
        lossFunction = self.getLossFunction()
        lossWeights = self.getLossWeights()
        metrics = []

        if self.optimizer == "adams":
            optimizer = K.optimizers.Adam(lr=self.learningRate)

        for metric in self.monitorMetrics:
            metrics.append(metric)

        self.model.compile(
            optimizer=optimizer,
            loss=lossFunction,
            loss_weights=lossWeights,
            metrics=metrics,
            # run_eagerly=None,  # for debug purpose!
        )

    def summary(self):
        self.model.summary()
        # total_params = tf.reduce_sum([tf.reduce_prod(v.shape) for v in self.model.trainable_weightstf.trainable_variables()])
        total_params = 2134528

        self.log("Total trainable Parameters: %i" % (total_params))
        self.parameter = int(total_params)

        return self.model.summary()

    def __init__(self, options) -> None:
        super().__init__(options=options)

        # if self.useGPU:
        #     physical_devices = tf.config.experimental.list_physical_devices("GPU")
        #     print("Num GPUs Available: ", len(physical_devices))
        #     if len(physical_devices) > 0:
        #         tf.config.experimental.set_memory_growth(physical_devices[0], True)

    def save(self, path):
        self.model.save_weights(path)

    def load(self, path):
        return self.model.load_weights(path)

    def loadState(self, state):
        return self.model.load_weights(state)

    def predict(self, input, get_likelihood=False, returnNumpy=False):
        batchSize = input.shape[0]

        input = self.prepareX(input)

        if list(input.shape[1:]) != self.inputShape:
            input = input.reshape(-1, self.inputShape[0], self.inputShape[1], self.inputShape[2])
        input_tensor = tf.convert_to_tensor(input)
        output_tensor = self.model(input_tensor)
        out = output_tensor.numpy()
        out = out.reshape(1, out.shape[0] * out.shape[1], out.shape[2])

        predictions = self.mapOutputForPrediction(out)
        predictions = predictions.reshape(batchSize, -1, self.config.numClasses)

        if not get_likelihood:
            predictions = predictions.argmax(axis=2)

        # predict supposed to return Tensors: https://js.tensorflow.org/api/latest/#tf.Sequential.predict
        # but its allready numpy
        # if returnNumpy:
        #     predictions = predictions.numpy()

        return predictions
