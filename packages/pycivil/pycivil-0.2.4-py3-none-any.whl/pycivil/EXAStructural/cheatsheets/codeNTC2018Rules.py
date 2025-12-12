from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing_extensions import Self

from pycivil.EXAStructural.lawcodes.codeNTC2018 import (
    rcSectionBeamAreaMin,
    rcSectionBeamShearAreaMin,
    rcSectionBeamShearStepsMax,
    rebarArea,
    rebarNumber,
)
from pycivil.EXAStructural.codes import Code
from pycivil.EXAStructural.materials import Concrete, ConcreteSteel
from pycivil.EXAUtils.solver import Solver


class BeamMinimumAreaInput(BaseModel):
    elementDescr: str = "Nome elemento"
    keyCode: str = "NTC2018"
    steelClass: str = "B450C"
    concreteClass: str = "C20/25"
    wEl: float = 300.0
    hEl: float = 600.0
    bt: float = 300.0
    rebarD: float = 12
    cover: float = 40.0
    bMin: float = 300.0
    stirrupD: float = 8
    rebarDComp: float = 12
    nbLegDirX: float = 2

    model_config = ConfigDict(extra="forbid")

    @field_validator("elementDescr", "keyCode", "steelClass", "concreteClass")
    def must_be_string(cls, v: Any) -> Any:
        assert isinstance(v, str)
        return v

    @field_validator(
        "wEl",
        "hEl",
        "bt",
        "rebarD",
        "cover",
        "bMin",
        "stirrupD",
        "rebarDComp",
        "nbLegDirX",
    )
    def greater_than_zero(cls, v: Any) -> Any:
        assert isinstance(v, float)
        assert v > 0
        return v

    @model_validator(mode="after")
    def rebar_in_concrete(self) -> Self:
        if self.hEl - self.rebarD - self.cover < 0:
            raise ValueError("Concrete height")
        return self


class BeamMinimumAreaOutput(BaseModel):
    rebarNumber: int = 0
    stirrupStepMin: float = 0
    stirrupCompStepMin: float = 0


class BeamMinimumAreaLogs(BaseModel):
    clsClass: str = ""
    cls_fck: float = 0
    cls_fctm: float = 0
    steelClass: str = ""
    steel_fyk: float = 0
    heightUtil: float = 0
    areaUtil: float = 0
    minimumRebarAreaCrit1: float = 0
    minimumRebarAreaCrit2: float = 0
    minimumRebarArea: float = 0
    rebarAreaDisposed: float = 0
    minimumRebarAreaForElementLenght: float = 0
    minimumLegsForElementLenght: float = 0
    maxStepCrit1: float = 0
    maxStepCrit2: float = 0
    maxStepCrit3: float = 0
    maxStepCrit4: float = 0


class BeamMinimumArea(BaseModel):
    inputData: BeamMinimumAreaInput = BeamMinimumAreaInput()
    logsData: BeamMinimumAreaLogs = BeamMinimumAreaLogs()
    outputData: BeamMinimumAreaOutput = BeamMinimumAreaOutput()


class ConcreteMaterialInput(BaseModel):
    elementDescr: str = "Nome elemento"
    keyCode: str = "NTC2018"
    concreteClass: str = "C20/25"


class RebarMaterialInput(BaseModel):
    elementDescr: str = "Nome elemento"
    keyCode: str = "NTC2018"
    steelClass: str = "B450C"


class ConcreteMaterialOutput(BaseModel):
    value_Rck: float = 0
    value_fck: float = 0
    value_fcm: float = 0
    value_fctm: float = 0
    value_Ecm: float = 0
    value_gammac: float = 0
    value_fcd: float = 0
    value_alphacc: float = 0
    value_sigmaCar: float = 0
    value_sigmaQp: float = 0


class RebarMaterialOutput(BaseModel):
    value_fyk: float = 0
    value_ftk: float = 0
    value_Es: float = 0
    value_gammas: float = 0
    value_fyd: float = 0
    value_sigmaCar: float = 0


class ConcreteMaterial(BaseModel):
    inputData: ConcreteMaterialInput = ConcreteMaterialInput()
    outputData: ConcreteMaterialOutput = ConcreteMaterialOutput()


class RebarMaterial(BaseModel):
    inputData: RebarMaterialInput = RebarMaterialInput()
    outputData: RebarMaterialOutput = RebarMaterialOutput()


class SolverConcrete(Solver):
    def __init__(self, inputModel: ConcreteMaterialInput):
        if not isinstance(inputModel, ConcreteMaterialInput):
            raise ValueError
        self.__in = inputModel
        super().__init__(modelInput=inputModel)
        self.__out = ConcreteMaterialOutput()
        super()._setModelOutput(model=self.__out)

    def run(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        if opt is None:
            mat = Concrete()
            mat.setByCode(
                codeObj=Code(self.__in.keyCode), catstr=self.__in.concreteClass
            )
            self.__out.value_Rck = mat.get_Rck()
            self.__out.value_fck = mat.get_fck()
            self.__out.value_fcd = mat.cal_fcd()
            self.__out.value_fcm = mat.get_fcm()
            self.__out.value_fctm = mat.get_fctm()
            self.__out.value_Ecm = mat.get_Ecm()
            self.__out.value_gammac = mat.get_gammac()
            self.__out.value_alphacc = mat.get_alphacc()
            self.__out.value_sigmaCar = mat.get_sigmac_max_c()
            self.__out.value_sigmaQp = mat.get_sigmac_max_q()
            return True
        else:
            return False


class SolverSteelRebar(Solver):
    def __init__(self, inputModel: RebarMaterialInput):
        if not isinstance(inputModel, RebarMaterialInput):
            raise ValueError
        self.__in = inputModel
        super().__init__(modelInput=inputModel)
        self.__out = RebarMaterialOutput()
        super()._setModelOutput(model=self.__out)

    def run(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        mat = ConcreteSteel()
        mat.setByCode(codeObj=Code(self.__in.keyCode), catstr=self.__in.steelClass)
        self.__out.value_fyk = mat.get_fsy()
        self.__out.value_Es = mat.get_Es()
        self.__out.value_fyd = mat.cal_fyd()
        self.__out.value_ftk = mat.get_fuk()
        self.__out.value_gammas = mat.get_gammas()
        self.__out.value_sigmaCar = mat.get_sigmas_max_c()
        return True


class SolverBeamMinRebar(Solver):
    def __init__(self, inputModel: BeamMinimumAreaInput):
        if not isinstance(inputModel, BeamMinimumAreaInput):
            raise ValueError
        self.__in = inputModel
        super().__init__(modelInput=inputModel)
        self.__logs = BeamMinimumAreaLogs()
        super()._setModelLogs(model=self.__logs)
        self.__out = BeamMinimumAreaOutput()
        super()._setModelOutput(model=self.__out)

    def run(self, opt: Union[Enum, None] = None, **kwargs) -> bool:

        # Materials
        mat_steel = ConcreteSteel()
        mat_steel.setByCode(
            codeObj=Code(self.__in.keyCode), catstr=self.__in.steelClass
        )
        self.__logs.steelClass = mat_steel.catStr()
        self.__logs.steel_fyk = mat_steel.get_fsy()
        mat_concrete = Concrete()
        mat_concrete.setByCode(
            codeObj=Code(self.__in.keyCode), catstr=self.__in.concreteClass
        )
        self.__logs.clsClass = mat_concrete.catStr()
        self.__logs.cls_fck = mat_concrete.get_fck()
        self.__logs.cls_fctm = mat_concrete.get_fctm()

        # Geometry for main rebar
        self.__logs.heightUtil = self.__in.hEl - self.__in.cover - self.__in.rebarD / 2
        self.__logs.minimumRebarAreaCrit1 = rcSectionBeamAreaMin(
            self.__logs.cls_fck,
            self.__logs.steel_fyk,
            self.__in.bt,
            self.__logs.heightUtil,
            "c1",
        )
        self.__logs.minimumRebarAreaCrit2 = rcSectionBeamAreaMin(
            self.__logs.cls_fck,
            self.__logs.steel_fyk,
            self.__in.bt,
            self.__logs.heightUtil,
            "c2",
        )
        self.__logs.minimumRebarArea = rcSectionBeamAreaMin(
            self.__logs.cls_fck,
            self.__logs.steel_fyk,
            self.__in.bt,
            self.__logs.heightUtil,
        )
        self.__logs.areaUtil = self.__in.bt * self.__logs.heightUtil
        self.__out.rebarNumber = rebarNumber(
            self.__logs.minimumRebarArea, self.__in.rebarD
        )[0]
        self.__logs.rebarAreaDisposed = self.__out.rebarNumber * rebarArea(
            self.__in.rebarD
        )

        # Geometry for stirrups
        self.__logs.minimumRebarAreaForElementLenght = rcSectionBeamShearAreaMin(
            self.__in.bMin
        )
        self.__logs.minimumLegsForElementLenght = rebarNumber(
            self.__logs.minimumRebarAreaForElementLenght, self.__in.stirrupD
        )[0]
        self.__logs.maxStepCrit1 = (
            self.__in.nbLegDirX / self.__logs.minimumLegsForElementLenght * 1000
        )
        (
            self.__logs.maxStepCrit2,
            self.__logs.maxStepCrit3,
            self.__logs.maxStepCrit4,
        ) = rcSectionBeamShearStepsMax(self.__logs.heightUtil, self.__in.rebarDComp)
        self.__out.stirrupStepMin = min(
            [
                self.__logs.maxStepCrit3,
                self.__logs.maxStepCrit1,
                self.__logs.maxStepCrit2,
            ]
        )
        self.__out.stirrupCompStepMin = min(
            [self.__out.stirrupStepMin, self.__logs.maxStepCrit4]
        )
        return True
