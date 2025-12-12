from enum import Enum
from pathlib import Path
from typing import Union

from pydantic import BaseModel


# Example of use for solver is swowed below:
# 1. Build a solver:
#           solver = RcSecRectSolver()
# 2. Add a model input for calculations
#           solver.setModelInput(iData)
# 3. Setting a job path for artifacts or similar
#           solver.setJobPath(str(job_path))
# 4. Running a specific task:
#           solver.run(SolverOptions.STATIC)
# 5.
# oData = solver.getModelOutput()
#
class Solver:
    def __init__(self, modelInput: Union[BaseModel, None] = None):
        self.__modelInput: Union[BaseModel, None] = modelInput
        self.__modelLogs: Union[BaseModel, None] = None
        self.__modelOutput: Union[BaseModel, None] = None
        self.__modelResources: Union[BaseModel, None] = None
        self.__jobPath: str | Path = ""
        self.__modelInputFile: str = ""
        self.__modelOutputFile: str = ""
        self.__reportName: str = "report"
        self.__solverName: str = "Solver"

    def _setSolverName(self, name):
        self.__solverName = name

    def solverName(self) -> str:
        return self.__solverName

    def outPath(self) -> Path:
        return Path(self.__jobPath) / Path(self.__solverName)

    @property
    def reportName(self):
        return self.__reportName

    @reportName.setter
    def reportName(self, value):
        self.__reportName = value

    @property
    def modelOutputFile(self):
        return self.__modelOutputFile

    @modelOutputFile.setter
    def modelOutputFile(self, value):
        self.__modelOutputFile = value

    @property
    def modelInputFile(self):
        return self.__modelInputFile

    @modelInputFile.setter
    def modelInputFile(self, value):
        self.__modelInputFile = value

    def _setModelOutput(self, model: BaseModel) -> bool:
        self.__modelOutput = model
        return True

    def _setModelLogs(self, model: BaseModel) -> bool:
        self.__modelLogs = model
        return True

    def setModelInput(self, model: BaseModel) -> bool:
        ext = self._buildSolverFromModelInput(model)
        if ext:
            self.__modelInput = model
        return ext

    def _setModelResources(self, model: BaseModel) -> bool:
        self.__modelResources = model
        return True

    def setJobPath(self, path: str | Path) -> bool:
        self.__jobPath = path
        return True

    def getJobPath(self):
        return self.__jobPath

    def getModelOutput(self, **kwargs) -> Union[BaseModel, None]:
        return self.__modelOutput

    def getModelLogs(self, **kwargs) -> Union[BaseModel, None]:
        return self.__modelLogs

    def getModelInput(self, **kwargs):
        return self.__modelInput

    def getModelResources(self, **kwargs):
        return self.__modelResources

    # Pure Virtual Methods
    #
    def run(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        raise NotImplementedError("Need to be implemented")

    def buildReport(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        raise NotImplementedError("Need to be implemented")

    def buildResources(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        raise NotImplementedError("Need to be implemented")

    def exportModelInput(self) -> BaseModel:
        return self._buildModelInputFromSolver()

    def _buildModelInputFromSolver(self) -> BaseModel:
        raise NotImplementedError("Need to be implemented")

    def _buildSolverFromModelInput(self, model: BaseModel) -> bool:
        raise NotImplementedError("Need to be implemented")
