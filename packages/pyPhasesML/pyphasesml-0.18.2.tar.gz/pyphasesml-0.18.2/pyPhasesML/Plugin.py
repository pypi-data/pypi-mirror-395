from pyPhases import PluginAdapter, Project

from pyPhasesML.ModelManager import ModelManager

from .exporter.ModelExporter import ModelExporter


class Plugin(PluginAdapter):
    def __init__(self, project: Project, options=None):
        super().__init__(project, options)
        self.project.systemExporter["ModelExporter"] = "pyPhasesML"
        self.project.systemExporter["MemmapRecordExporter"] = "pyPhasesML"
        
    def initPlugin(self):
        # reload the model everytime the config changed
        def updateModel(changedValue):
            ModelManager.loadModel(self.project)
            self.project.trigger('modelLoaded', ModelManager.model)

        self.project.on("configChanged", updateModel)
        options = {}
        if self.project.getConfig("data-path", False):
            options["basePath"] = self.project.getConfig("data-path")

        self.project.registerExporter(ModelExporter(), priority=200)
