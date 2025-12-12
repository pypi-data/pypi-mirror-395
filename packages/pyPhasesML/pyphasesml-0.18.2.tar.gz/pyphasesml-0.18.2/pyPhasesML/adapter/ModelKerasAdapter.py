from ..ModelAdapter import ModelAdapter
from ..scorer.ScorerTF import ScorerTF

import shutil
import tensorflow as tf
import tensorflow.keras as K
import matplotlib.pyplot as plt
import numpy as np
import io

from ..DataSet import TrainingSetLoader


def plot_to_image(figure):
    """Converts the matplotlib plot specified by 'figure' to a PNG image and
    returns it. The supplied figure is closed and inaccessible after this call."""
    # Save the plot to a PNG in memory.
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    # Closing the figure prevents it from being displayed directly inside
    # the notebook.
    plt.close(figure)
    buf.seek(0)
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    image = tf.expand_dims(image, 0)
    return image


class ModelKerasAdapter(ModelAdapter):
    model: K.Model = None

    def _metrics(self, metric, validation=False):
        prepend = "val_" if validation else ""
        return prepend + metric["name"]

    def getMetrics(self):
        scorer = ScorerTF(len(self.classNames[0]))
        metrics = []
        for metric in self.validationMetrics:
            m = scorer.getMetricScorer(metric)
            metrics.append(m)
        return metrics

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

    def generateDataset(self, dataset):
        while True:
            dataiterator = iter(dataset)
            for batch in dataiterator:
                yield self.prepareData(batch)

    def train(self, dataset: TrainingSetLoader):
        callbacks = []
        mainMetric = self._metrics(self.metrics[self.validationMetrics[0]])
        metricStop = self.getMetric(mainMetric)
        metricSave = self.getMetric(mainMetric)

        tbLogDir = self.config.logPath + "/tb"
        shutil.rmtree(tbLogDir, ignore_errors=True)

        # tf.debugging.experimental.enable_dump_debug_info(tbLogDir, tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1)
        tensorboard_callback = K.callbacks.TensorBoard(
            log_dir=tbLogDir,
            histogram_freq=1,
        )
        callbacks.append(tensorboard_callback)

        if self.predictionType == "reconstruction":
            model = self.model
            reconstruction_train = dataset.trainingData.__next__().x
            reconstruction_val = dataset.validationData.__next__().x
            reconstructionExamples = np.concatenate((reconstruction_train[0:5], reconstruction_val[0:5]))
            dataset.trainingData.__iter__()
            dataset.validationData.__iter__()

            file_writer_recon = tf.summary.create_file_writer(tbLogDir + "/recon")

            def log_examples(epoch, logs):
                reconstructions = model.predict(reconstructionExamples)
                for i, recon in enumerate(reconstructions):
                    type = "train" if i < 5 else "validation"
                    fig, ax = plt.subplots(1, figsize=(6, 3), dpi=300)
                    ax.plot(reconstructionExamples[i][:, 0])
                    ax.plot(recon[:, 0])
                    image = plot_to_image(fig)
                    with file_writer_recon.as_default():
                        tf.summary.image(
                            "Example Reconstruction (%s) %i" % (type, i),
                            image,
                            step=epoch,
                        )

            cm_callback = K.callbacks.LambdaCallback(on_epoch_end=log_examples)
            callbacks.append(cm_callback)

        if self.config.stopAfterNotImproving is not None:
            earlyStopping_cb = K.callbacks.EarlyStopping(
                monitor=self._metrics(metricStop, True),
                patience=self.config.stopAfterNotImproving,
                verbose=0,
                mode=metricStop["type"],
                baseline=None,
                restore_best_weights=True,
            )
            callbacks.append(earlyStopping_cb)

        if self.config.learningRateDecay is not None and self.config.learningRateDecay > 0:
            lr_decay_cb = K.callbacks.LearningRateScheduler(
                schedule=lambda epoch: self.config.learningRate * (self.config.learningRateDecay**epoch)
            )
            callbacks.append(lr_decay_cb)

        log = K.callbacks.CSVLogger(self.getCsvPath())
        callbacks.append(log)

        checkpoint = K.callbacks.ModelCheckpoint(
            self.config.logPath + "/weights-{epoch:02d}.weights.h5",
            monitor=self._metrics(metricSave, True),
            mode=metricSave["type"],
            save_best_only=True,
            save_weights_only=True,
            verbose=0,
        )
        callbacks.append(checkpoint)
        classWeight = None if self.classWeights is None else dict(list(zip(range(6), self.classWeights)))

        dataset.trainingData.continous = True
        dataset.validationData.continous = True
        batchesPerEpoch = len(dataset.trainingData)
        validationBatchesPerEpoch = len(dataset.validationData)
        train = self.generateDataset(dataset.trainingData)
        validationData = self.generateDataset(dataset.validationData)

        # self.cleanCsv()

        # debug
        # Model for trainingsdata: self.model(train.__next__()[0])
        # Model for validationdata: self.model(validationData.__next__()[0])
        # Loss (if its not implemented as string!): self.getLossFunction()(train.__next__()[1], self.model(train.__next__()[0]))
        # Test other Loss: tf.keras.losses.BinaryCrossentropy(from_logits=False)(train.__next__()[1], self.model(train.__next__()[0]))
        # Test Test Scorer
        # x, y = train.__next__()
        # ScorerTF(self.config.numClasses).getMetricScorer("kappa")(y, self.model(x))
        self.model.fit(
            x=train,
            validation_data=validationData,
            steps_per_epoch=batchesPerEpoch,
            validation_steps=validationBatchesPerEpoch,
            class_weight=classWeight,
            batch_size=self.batchSize,
            shuffle=False,
            verbose=1,
            epochs=self.maxEpochs,
            callbacks=callbacks,
        )

        metricHistory = self.model.history.history[mainMetric]
        self.bestMetric = max(metricHistory)
        self.fullEpochs = len(metricHistory)
        return self.model

    def build(self):
        optimizer = None
        lossFunction = self.getLossFunction()
        lossWeights = self.getLossWeights()

        if self.config.optimizerId == "adams":
            optimizer = K.optimizers.Adam(learning_rate=self.config.learningRate)
        if self.config.optimizerId == "nadams":
            optimizer = K.optimizers.Nadam(learning_rate=self.config.learningRate)

        self.model.compile(
            optimizer=optimizer,
            loss=lossFunction,
            loss_weights=lossWeights,
            metrics=self.getMetrics(),
            # run_eagerly=None,
            run_eagerly=True,  # for debug purpose! required for scorer ?
        )
        # for metric in self.validationMetrics:
        # m = scorer.getMetricScorer(metric)
        # self.model.addMetric(m, name='activation_mean')
        # if metric == ["acc", "accuracy"]:
        #     metric = "acc"
        # elif metric == "kappa":
        #     metric = tfa.metrics.CohenKappa(num_classes=self.config.numClasses)
        # elif metric == "auprc":
        #     metric = tf.keras.metrics.AUC(name="AUPRC", curve="PR")
        # elif metric == "auroc":
        #     metric = tf.keras.metrics.AUC(name="AUROC", curve="ROC")
        # elif metric == "meanSquared":
        #     metric = tf.keras.metrics.MeanSquaredError(name="meanSquared")
        # self.model.compile(
        #     optimizer="adam",
        #     loss="categorical_crossentropy",
        #     # loss_weights=lossWeights,
        #     metrics=["accuracy"],
        #     run_eagerly=None,  # for debug purpose!
        # )

    def summary(self):
        total_params = tf.reduce_sum([tf.reduce_prod(v.shape) for v in self.model.trainable_weights])
        self.log("Total trainable Parameters: %i" % (total_params))
        self.parameter = int(total_params)

        return self.model.summary()

    def __init__(self, options) -> None:
        super().__init__(options=options)

        if self.useGPU:
            physical_devices = tf.config.experimental.list_physical_devices("GPU")
            print("Num GPUs Available: ", len(physical_devices))
            if len(physical_devices) > 0:
                tf.config.experimental.set_memory_growth(physical_devices[0], True)

    def save(self, path):
        self.model.save_weights(path)

    def load(self, path):
        return self.model.load_weights(path)

    def loadState(self, state):
        return self.model.load_weights(state)

    def predict(self, input, get_likelihood=False, returnNumpy=True):
        batchSize = input.shape[0]

        input = self.prepareX(input)

        if input.ndim == len(self.inputShape):
            input = input.reshape(-1, self.inputShape[0], self.inputShape[1], self.inputShape[2])
        input_tensor = tf.convert_to_tensor(input)
        output_tensor = self.model(input_tensor)
        out = output_tensor.numpy()

        if out.ndim < input.ndim:
            out = out.reshape(1, out.shape[0] * out.shape[1], out.shape[2])

        predictions = self.mapOutputForPrediction(out)
        if self.oneHotDecoded:
            predictions = predictions.reshape(batchSize, -1, self.config.numClasses)

            if not get_likelihood:
                predictions = predictions.argmax(axis=2)

        # predict supposed to return Tensors: https://js.tensorflow.org/api/latest/#tf.Sequential.predict
        # but its allready numpy
        # if returnNumpy:
        #     predictions = predictions.numpy()

        return predictions

    def mapOutputForLoss(self, output, mask):
        return output.reshape(-1)
