import importlib

from pyPhases import ConfigNotFoundException
from pyPhases.util.EventBusStatic import EventBusStatic

from .Model import Model, ModelConfig


class ModelManager(EventBusStatic):
    model: Model = None
    modelOptions = None
    beforeBuild = None
    modelPath = None

    @staticmethod
    def getModel(forceReload=False) -> Model:
        if ModelManager.model is None or forceReload:
            if ModelManager.modelOptions is None:
                raise Exception("ModelManager setModel was never called!")
            else:
                ModelManager.loadModelFromOptions()
        return ModelManager.model

    def loadModelFromOptions() -> None:
        options = ModelManager.modelOptions
        modelClass = ModelManager.loadModelByModule(options["modelName"])
        model = modelClass(options["modelConfig"])

        for field, value in options["general"].items():
            setattr(model, field, value)
            
        model.config = ModelConfig()
        for field, value in options["config"].items():
            setattr(model.config, field, value)

        if ModelManager.beforeBuild is not None:
            ModelManager.beforeBuild(model)
    
        model.initAdapter()
        model.init()
        model.define()
        model.build()
        ModelManager.model = model
        ModelManager.trigger("modelLoaded", model)

    def validate(config):
        def checkValueInConfig(config, value, valuePath=None):
            checkDict = config if valuePath is None else config[valuePath]

            if value not in checkDict:
                valuePath = value if valuePath is None else valuePath + "." + value
                raise ConfigNotFoundException("The value '%s' is required in the config" % valuePath)

        checkValueInConfig(config, "modelName")
        checkValueInConfig(config, "classification")
        checkValueInConfig(config, "trainingParameter")
        checkValueInConfig(config, "inputShape")
        checkValueInConfig(config, "classNames", "classification")
        checkValueInConfig(config, "batchSize", "trainingParameter")

        if not isinstance(config["classification"]["classNames"], list):
            raise ConfigNotFoundException("The value 'classification.classNames' is required to be a list of class names")

    @staticmethod
    def loadModel(project) -> None:
        config = project.config
        ModelManager.validate(config)
        ModelManager.modelPath = config["modelPath"]

        trainingParameter = config["trainingParameter"]
        classNames = config["classification"]["classNames"]
        labelNames = config["classification"]["labelNames"]
        classCount = len(classNames)
        ModelManager.modelOptions = {
            "modelName": project.config["modelName"],
            "modelConfig": project.getConfig("model", {}),
            "general": {
                "inputShape": project.config["inputShape"],
                "maxEpochs": project.getConfig("trainingParameter.maxEpochs", None, False),
                "batchSize": trainingParameter["batchSize"],
                "batchSizeAccumulation": trainingParameter["batchSizeAccumulation"] if "batchSizeAccumulation" in trainingParameter else 1,
                "classWeights": project.getConfig("trainingParameter.classWeights", None, False),
                "classNames": classNames,
                "validationEvery": project.getConfig("trainingParameter.validationEvery", None, False),
                "ignoreClassIndex": project.getConfig("ignoreClassIndex", None, False),
                "validationMetrics": project.getConfig("trainingParameter.validationMetrics", ["loss"]),
                "useEventScorer": project.getConfig("trainingParameter.useEventScorer", False),
                "predictionType": project.getConfig("classification.type", "classification"),
                "oneHotDecoded": project.getConfig("oneHotDecoded", False),
                "cycleLR": project.getConfig("trainingParameter.cyclicLearningRate", False),
            },
            "config": {
                # training
                "labelNames": labelNames,
                "numClasses": classCount,
                "optimizerId": project.getConfig("trainingParameter.optimizer", "Adams"),
                "learningRate": project.getConfig("trainingParameter.learningRate", 0.001),
                "learningRateDecay": project.getConfig("trainingParameter.learningRateDecay", None, False),
                "stopAfterNotImproving": project.getConfig("trainingParameter.stopAfterNotImproving", 10),
                "cycleLRDivisor": project.getConfig("trainingParameter.cycleLRDivisor", 4),                
            }
        }

    @staticmethod
    def loadModelByModule(name):
        path = ModelManager.modelPath.replace("/", ".")
        packageSplit = path.split(".")
        package = packageSplit[0]
        path = ".".join(packageSplit[1:])
        path = "." + path if path != "" else ""
        module = importlib.import_module("%s.%s.%s" % (path, name, name), package)
        # module = importlib.import_module(".%s.%s" % (name, name), package=userModels.__package__)
        return getattr(module, name)
