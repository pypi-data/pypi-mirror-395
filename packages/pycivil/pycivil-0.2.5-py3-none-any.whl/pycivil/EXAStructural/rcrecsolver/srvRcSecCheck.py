import json
import os
from dataclasses import field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union, Literal, Any
from uuid import UUID
from importlib.metadata import version

from pydantic import BaseModel, ConfigDict, Field

import pycivil
from pycivil.EXAUtils.models import Project

from pycivil.settings import ServerSettings

from pycivil.EXAStructural.checkable import Checker, CheckableCriteriaEnum
from pycivil.EXAStructural.lawcodes.codeEC212 import RMinutes, FireCurve
from pycivil.EXAStructural.codes import Code, CodeEnum
from pycivil.EXAStructural.loads import ForcesOnSection
from pycivil.EXAStructural.materials import Concrete, ConcreteSteel
from pycivil.EXAStructural.sections import ShapeEnum, ConcreteSectionModel
from pycivil.EXAStructural.templateRCRect import RCTemplRectEC2, SectionCrackedStates
from pycivil.EXAStructural.templateRCRectFire import RCRectEC2FireDesign
from pycivil.EXAStructuralCheckable.RcsRectangular import RcsRectangular, ThermalMapResults, ThermalMapSolverIn, \
    CrackSeverity
from pycivil.EXAUtils.latexReportMakers import (
    CodesFB,
    ConcreteFB,
    ConcreteSectionFB,
    SteelConcreteFB,
)
from pycivil.EXAUtils.latexReportMakers import ForcesOnSectionListFB as Loads
from pycivil.EXAUtils.logging import log
from pycivil.EXAUtils.report import (
    EnumFBSection,
    Fragment,
    FragmentsBuilder,
    Reporter,
    ReportProperties,
    ReportTemplateEnum,
)
from pycivil.EXAUtils.solver import Solver

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class FireDesignRTime(BaseModel):
    rtime: List[str] = list(RMinutes)


class FireDesignCurve(BaseModel):
    curve: List[str] = list(FireCurve)


class Rows(BaseModel):
    value: List[str]


class Columns(BaseModel):
    value: List[List[str]]


class Table2D(BaseModel):
    rows: Optional[Rows] = None
    columns: Optional[Columns] = None


class CodeSteelRebarSelector(Table2D):
    strCodeDefault: str = "EC2:ITA"
    strCodeKeyDefault: str = "B450C"

class CodeConcreteSelector(Table2D):
    strCodeDefault: str = "EC2:ITA"
    strCodeKeyDefault: str = "C25/30"

class SolverExit(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


class CheckableResults(BaseModel):
    code: Optional[CodeEnum] = None
    loadIndex: int = -1
    loadId: Optional[int] = None
    checkLog: dict = field(default_factory=dict)
    check: Optional[dict] = None
    safetyFactor: Optional[dict] = None

class CheckableNameEnum(str, Enum):
    RCRECT = "RcsRectangular"
    model_config = ConfigDict(extra="forbid")

class ResultsForCriteria(BaseModel):
    criteria: Optional[CheckableCriteriaEnum]
    results: List[CheckableResults] = field(default_factory=list)
    media: Optional[dict] = None
    criteriaLogs: Optional[ThermalMapResults] = None
    model_config = ConfigDict(extra="forbid")

class Checkable(BaseModel):
    name: CheckableNameEnum = CheckableNameEnum.RCRECT
    code: CodeEnum = CodeEnum.NTC2018
    resultsForCriteria: List[ResultsForCriteria] = field(default_factory=list)

class ModelInputRcSecCheck(BaseModel):
    project: Optional[pycivil.EXAUtils.models.Project] = None
    user: Optional[pycivil.EXAUtils.models.User] = None
    code: CodeEnum = CodeEnum.NTC2018
    loads: List[ForcesOnSection]
    section: ConcreteSectionModel
    criteria: List[CheckableCriteriaEnum] = field(default_factory=list)
    loadsInCriteria: List[List[int]] = field(default_factory=list)

    def buildLoads(self) -> Loads:

        # Build loads
        nbl = 0
        _loads = Loads(ServerSettings().latex_templates_path)

        assert self.loads is not None

        for ld in self.loads:
            nbl += 1
            loadToAppend = ForcesOnSection(
                Fx=ld.Fx,
                Fy=ld.Fy,
                Fz=ld.Fz,
                Mx=ld.Mx,
                My=ld.My,
                Mz=ld.Mz,
                descr=ld.descr,
                id=ld.id,
            )

            # Setting frequency
            assert ld.frequency is not None
            loadToAppend.frequency = ld.frequency

            # Setting limit states
            assert ld.limitState is not None
            loadToAppend.limitState = ld.limitState

            _loads.forces().append(loadToAppend)

        print(f"INF: {nbl:.0f} loads added")
        return _loads

    def buildRcsRectangular(self) -> Union[RCTemplRectEC2, None]:
        ids = -1
        descr = ""
        if self.section.id is not None:
            ids = self.section.id
        if self.section.descr is not None:
            descr = self.section.descr

        sectionBuilt = RCTemplRectEC2(ids, descr)

        print("INF: forming concrete material")

        assert self.section.concreteMat is not None
        concrete = Concrete(descr=self.section.concreteMat.descr)
        if self.section.concreteMat.bycode:
            assert self.section.concreteMat.code is not None
            codeConcrete = Code(self.section.concreteMat.code.value)
            assert self.section.concreteMat.mat is not None
            assert isinstance(self.section.concreteMat.mat.value, str)
            concrete.setByCode(codeConcrete, self.section.concreteMat.mat.value)
        else:
            concrete.set_alphacc(self.section.concreteMat.alphacc)
            concrete.set_alphacc_fire(self.section.concreteMat.alphacc_fire)
            concrete.set_ec2(self.section.concreteMat.ec2)
            concrete.set_ecu(self.section.concreteMat.ecu)
            concrete.set_eta(self.section.concreteMat.eta)
            concrete.set_fcm(self.section.concreteMat.fcm)
            concrete.set_fck(self.section.concreteMat.fck)
            concrete.set_fctm(self.section.concreteMat.fctm)
            concrete.set_lambda(self.section.concreteMat.llambda)
            concrete.set_gammac(self.section.concreteMat.gammac)
            concrete.set_sigmac_max_c(self.section.concreteMat.sigmac_max_c)
            concrete.set_sigmac_max_q(self.section.concreteMat.sigmac_max_q)

        assert self.section.concreteMat.environment is not None
        if (
            self.section.concreteMat.environment
            == self.section.concreteMat.environment.AGGRESSIVITY_HIGHT
        ):
            concrete.setEnvironmentHightAggressive()
        elif (
            self.section.concreteMat.environment
            == self.section.concreteMat.environment.AGGRESSIVITY_LOW
        ):
            concrete.setEnvironmentAggressive()
        elif (
            self.section.concreteMat.environment
            == self.section.concreteMat.environment.AGGRESSIVITY_NOT
        ):
            concrete.setEnvironmentNotAggressive()
        else:
            print("ERR: environment unknown !!!")
            return None

        assert self.section.concreteMat.aggregates is not None
        concrete.setAggregates(self.section.concreteMat.aggregates)

        assert self.section.concreteMat.moisture is not None
        concrete.setMoisture(self.section.concreteMat.moisture)

        assert self.section.steelMat is not None
        print("INF: forming steel material")
        steel = ConcreteSteel(descr=self.section.steelMat.descr)
        if self.section.steelMat.bycode:
            assert self.section.steelMat.code is not None
            codeSteel = Code(self.section.steelMat.code.value)
            assert isinstance(self.section.steelMat.mat.value, str)
            steel.setByCode(codeSteel, self.section.steelMat.mat.value)
        else:
            steel.set_Es(self.section.steelMat.Es)
            steel.set_esu(self.section.steelMat.esu)
            steel.set_esy(self.section.steelMat.esy)
            steel.set_fsy(self.section.steelMat.fsy)
            steel.set_gammas(self.section.steelMat.gammas)
            steel.set_sigmas_max_c(self.section.steelMat.sigmas_max_c)

        assert self.section.steelMat.sensitivity is not None
        if (
            self.section.steelMat.sensitivity
            == self.section.steelMat.sensitivity.SENSITIVITY_HIGHT
        ):
            steel.setEnvironmentSensitive()
        elif (
            self.section.steelMat.sensitivity
            == self.section.steelMat.sensitivity.SENSITIVITY_LOW
        ):
            steel.setEnvironmentNotSensitive()
        else:
            print("ERR: sensitivity unknown !!!")
            return None

        assert self.section.steelMat.formed is not None
        steel.set_shapingType(self.section.steelMat.formed)

        sectionBuilt.setConcreteMaterial(concrete)
        sectionBuilt.setSteelMaterial(steel)

        if self.section.shape.tp == ShapeEnum.RECT:
            print("INF: ... shape rectangular")
            sectionBuilt.setDimH(self.section.shape.height)
            sectionBuilt.setDimW(self.section.shape.width)
        else:
            print("ERR: ... shape unknown !!!")
            return None

        if self.section.disposerOnLine is not None:
            print("INF: ... steel disposed on line")
            for disposer in self.section.disposerOnLine:
                sectionBuilt.addSteelArea(
                    posStr="LINE-" + disposer.fromPos.value,
                    dist=disposer.distanceFromPos,
                    d=disposer.diameter,
                    nb=disposer.number,
                    sd=disposer.steelInterDistance,
                )

        if self.section.disposerSingle is not None:
            print("INF: ... steel disposed single")
            for disposer in self.section.disposerSingle:
                sectionBuilt.addSteelArea(
                    posStr="XY",
                    area=disposer.area,
                    x=disposer.xpos,
                    y=disposer.ypos,
                    idSteel=disposer.id,
                )

        if self.section.stirrup is not None:
            print("INF: ... stirrupt disposed")
            sectionBuilt.setStirrupt(
                area=self.section.stirrup.area,
                angle=self.section.stirrup.angle,
                dist=self.section.stirrup.step,
            )

        return sectionBuilt

class ReportOption(str, Enum):
    REPORT_FROM_RUN = "report_from_run"


class SolverOut(BaseModel):
    exit: SolverExit = SolverExit.SUCCESS
    results: Checkable = Field(default_factory=Checkable)
    log: List[str] = field(default_factory=list)
    media: List[str] = field(default_factory=list)

class ModelOutputRcSecCheck(SolverOut, FragmentsBuilder):
    def setFragmentOptions(self, options: dict) -> bool:
        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(ServerSettings().latex_templates_path)
        placeHolders = {}
        if self.results is not None:
            for crit in self.results.resultsForCriteria:
                ###############################################################
                # # #                   REPORT FOR SLU NM                 # # #
                ###############################################################
                #
                if crit.criteria == CheckableCriteriaEnum.SLU_NM:
                    print("crit.criteria == models.CheckableCriteriaEnum.SLU_NM")
                    f.add(line=r"\newpage")
                    f.add(line=r"\section{Verifica SLU a pressoflessione retta}")
                    placeHolders["check_SLU_MN"] = []
                    if crit.results is not None:
                        for res in crit.results:
                            resPlaceHolders: dict[str, int | None | str] = {"id": res.loadId}
                            if res.checkLog is not None:
                                checkLog_SLU_NM = CheckLog_SLU_NM(**res.checkLog)
                                resPlaceHolders["Ned"] = (
                                    f"{checkLog_SLU_NM.Ned / 1000:.1f}"
                                    if checkLog_SLU_NM.Ned is not None
                                    else " "
                                )
                                resPlaceHolders["Med"] = (
                                    f"{checkLog_SLU_NM.Med / 1000000:.1f}"
                                    if checkLog_SLU_NM.Med is not None
                                    else " "
                                )
                                resPlaceHolders["Ner"] = (
                                    f"{checkLog_SLU_NM.Ner / 1000:.1f}"
                                    if checkLog_SLU_NM.Ner is not None
                                    else " "
                                )
                                resPlaceHolders["Mer"] = (
                                    f"{checkLog_SLU_NM.Mer / 1000000:.1f}"
                                    if checkLog_SLU_NM.Mer is not None
                                    else " "
                                )

                            if res.safetyFactor is not None:

                                safetyFactor_SLU_NM = SafetyFactor_SLU_NM(
                                    **res.safetyFactor
                                )

                                resPlaceHolders["FS"] = (
                                    "{:.2f}".format(
                                        safetyFactor_SLU_NM.interactionDomain
                                    )
                                    if safetyFactor_SLU_NM.interactionDomain is not None
                                    else " "
                                )

                            if res.check is not None:
                                check_SLU_NM = Check_SLU_NM(**res.check)
                                if check_SLU_NM.interactionDomain is not None:
                                    resPlaceHolders["check"] = (
                                        "OK"
                                        if check_SLU_NM.interactionDomain
                                        else "NOOK"
                                    )
                                else:
                                    resPlaceHolders["check"] = " "

                            placeHolders["check_SLU_MN"].append(resPlaceHolders)

                    if crit.media is not None:
                        if "check_SLU_NM_NTC2018_image_url" in crit.media.keys():
                            domainUrl = crit.media[
                                "check_SLU_NM_NTC2018_image_url"
                            ]
                            # Only for latex also in windows path repr we need to
                            # use /
                            domainUrl = str(domainUrl).replace('\\','/')
                            placeHolders["domainUrl"] = domainUrl
                            if Path(placeHolders["domainUrl"]).exists():
                                placeHolders["domain"] = True
                            else:
                                placeHolders["domain"] = False
                        else:
                            placeHolders["domain"] = False
                    else:
                        placeHolders["domain"] = False

                    f.add(
                        templateName="template-ita-rc-rec-slu-nm.tex",
                        templatePlaceholders=placeHolders,
                    )

                ###############################################################
                # # #                REPORT FOR SLU NM FIRE               # # #
                ###############################################################
                #
                if crit.criteria == CheckableCriteriaEnum.SLU_NM_FIRE:
                    print("crit.criteria == models.CheckableCriteriaEnum.SLU_NM_FIRE")
                    f.add(line=r"\newpage")
                    f.add(
                        line=r"\section{Verifica SLU a pressoflessione retta sotto incendio}"
                    )
                    placeHolders["check_SLU_MN"] = []
                    if crit.results is not None:
                        assert isinstance(crit.criteriaLogs, ThermalMapResults)

                        placeHolders["width"] = "{:.2f}".format(
                            crit.criteriaLogs.reductedShape.width
                        )
                        placeHolders["height"] = "{:.2f}".format(
                            crit.criteriaLogs.reductedShape.height
                        )
                        placeHolders["curve"] = crit.criteriaLogs.fireDesignCurve.name
                        placeHolders["time"] = crit.criteriaLogs.fireDesignRTime.value

                        for res in crit.results:
                            resPlaceHolders = {"id": res.loadId}
                            if res.checkLog is not None:
                                checkLog_SLU_NM_FIRE = CheckLog_SLU_NM_FIRE(
                                    **res.checkLog
                                )
                                resPlaceHolders["Ned"] = (
                                    f"{checkLog_SLU_NM_FIRE.Ned / 1000:.1f}"
                                    if checkLog_SLU_NM_FIRE.Ned is not None
                                    else " "
                                )
                                resPlaceHolders["Med"] = (
                                    f"{checkLog_SLU_NM_FIRE.Med / 1000000:.1f}"
                                    if checkLog_SLU_NM_FIRE.Med is not None
                                    else " "
                                )
                                if (
                                    checkLog_SLU_NM_FIRE.Ner_Hot is not None
                                    and checkLog_SLU_NM_FIRE.Ner_Cold
                                ):
                                    resPlaceHolders["Ner"] = "{:.1f}".format(
                                        min(
                                            checkLog_SLU_NM_FIRE.Ner_Hot,
                                            checkLog_SLU_NM_FIRE.Ner_Cold,
                                        )
                                        / 1000
                                    )
                                else:
                                    resPlaceHolders["Ner"] = " "
                                if (
                                    checkLog_SLU_NM_FIRE.Mer_Hot is not None
                                    and checkLog_SLU_NM_FIRE.Mer_Cold
                                ):
                                    resPlaceHolders["Mer"] = "{:.1f}".format(
                                        min(
                                            checkLog_SLU_NM_FIRE.Mer_Hot,
                                            checkLog_SLU_NM_FIRE.Mer_Cold,
                                        )
                                        / 1000000
                                    )

                            if res.safetyFactor is not None:

                                safetyFactor_SLU_NM_FIRE = (
                                    SafetyFactor_SLU_NM_FIRE(**res.safetyFactor)
                                )

                                resPlaceHolders["FS"] = (
                                    "{:.2f}".format(
                                        safetyFactor_SLU_NM_FIRE.interactionDomain
                                    )
                                    if safetyFactor_SLU_NM_FIRE.interactionDomain
                                    is not None
                                    else " "
                                )

                            if res.check is not None:
                                check_SLU_NM_FIRE = Check_SLU_NM_FIRE(
                                    **res.check
                                )
                                if check_SLU_NM_FIRE.interactionDomain is not None:
                                    resPlaceHolders["check"] = (
                                        "OK"
                                        if check_SLU_NM_FIRE.interactionDomain
                                        else "NOOK"
                                    )
                                else:
                                    resPlaceHolders["check"] = " "

                            placeHolders["check_SLU_MN"].append(resPlaceHolders)

                    if crit.media is not None:
                        Media_SLU_NM_FIRE(**crit.media)
                        placeHolders["domain"] = True
                        placeHolders["domainUrl"] = crit.media[
                            "check_SLU_NM_FIRE_NTC2018_image_url"
                        ]
                    else:
                        placeHolders["domain"] = False

                    f.add(
                        templateName="template-ita-rc-slu-nm-fire.tex",
                        templatePlaceholders=placeHolders,
                    )

                ###############################################################
                # # #                   REPORT FOR SLE NM                 # # #
                ###############################################################
                elif crit.criteria == CheckableCriteriaEnum.SLE_NM:
                    print("crit.criteria == models.CheckableCriteriaEnum.SLE_NM")
                    f.add(line=r"\newpage")
                    f.add(line=r"\section{Verifica SLE a pressoflessione retta}")
                    placeHolders["check_SLE_MN"] = []
                    if crit.results is not None:
                        for res in crit.results:
                            resPlaceHolders = {"id": res.loadId}
                            if res.checkLog is not None:
                                checkLog_SLE_NM = CheckLog_SLE_NM(**res.checkLog)
                                resPlaceHolders["Ned"] = (
                                    f"{checkLog_SLE_NM.Ned / 1000:.1f}"
                                    if checkLog_SLE_NM.Ned is not None
                                    else " "
                                )
                                resPlaceHolders["Med"] = (
                                    f"{checkLog_SLE_NM.Med / 1000000:.1f}"
                                    if checkLog_SLE_NM.Med is not None
                                    else " "
                                )
                                resPlaceHolders["sigmac"] = (
                                    f"{checkLog_SLE_NM.sigmac:.1f}"
                                    if checkLog_SLE_NM.sigmac is not None
                                    else " "
                                )
                                resPlaceHolders["sigmas"] = (
                                    f"{checkLog_SLE_NM.sigmas:.1f}"
                                    if checkLog_SLE_NM.sigmas is not None
                                    else " "
                                )
                                resPlaceHolders["sigmxc"] = (
                                    f"{checkLog_SLE_NM.sigmxc:.1f}"
                                    if checkLog_SLE_NM.sigmxc is not None
                                    else " "
                                )
                                resPlaceHolders["sigmxs"] = (
                                    f"{checkLog_SLE_NM.sigmxs:.1f}"
                                    if checkLog_SLE_NM.sigmxs is not None
                                    else " "
                                )
                                resPlaceHolders["xi"] = (
                                    f"{checkLog_SLE_NM.xi:.1f}"
                                    if checkLog_SLE_NM.xi is not None
                                    else " "
                                )

                            if res.safetyFactor is not None:

                                safetyFactor_SLE_NM = SafetyFactor_SLE_NM(
                                    **res.safetyFactor
                                )

                                resPlaceHolders["FS"] = (
                                    f"{safetyFactor_SLE_NM.globalCheck:.2f}"
                                    if safetyFactor_SLE_NM.globalCheck is not None
                                    else " "
                                )

                            if res.check is not None:
                                check_SLE_NM = Check_SLE_NM(**res.check)
                                if check_SLE_NM.globalCheck is not None:
                                    resPlaceHolders["check"] = (
                                        "OK" if check_SLE_NM.globalCheck else "NOOK"
                                    )
                                else:
                                    resPlaceHolders["check"] = " "

                            placeHolders["check_SLE_MN"].append(resPlaceHolders)

                    f.add(
                        templateName="template-ita-rc-rec-sle-nm.tex",
                        templatePlaceholders=placeHolders,
                    )

                ###############################################################
                # # #                   REPORT FOR SLU T                  # # #
                ###############################################################
                elif crit.criteria == CheckableCriteriaEnum.SLU_T:
                    print("crit.criteria == models.CheckableCriteriaEnum.SLU_T")
                    f.add(line=r"\newpage")
                    f.add(line=r"\section{Verifica SLU a taglio}")
                    placeHolders["check_SLU_T"] = []
                    if crit.results is not None:
                        for res in crit.results:
                            resPlaceHolders = {"id": res.loadId}
                            if res.checkLog is not None:
                                checkLog_SLU_T = CheckLog_SLU_T(**res.checkLog)
                                resPlaceHolders["Ted"] = (
                                    f"{checkLog_SLU_T.Ved / 1000:.1f}"
                                    if checkLog_SLU_T.Ved is not None
                                    else " "
                                )
                                resPlaceHolders["Trd"] = (
                                    f"{checkLog_SLU_T.Vrd / 1000:.1f}"
                                    if checkLog_SLU_T.Vrd is not None
                                    else " "
                                )
                                resPlaceHolders["Trcd"] = (
                                    f"{checkLog_SLU_T.Vrcd / 1000:.1f}"
                                    if checkLog_SLU_T.Vrcd is not None
                                    else " "
                                )
                                resPlaceHolders["Trsd"] = (
                                    f"{checkLog_SLU_T.Vrsd / 1000:.1f}"
                                    if checkLog_SLU_T.Vrsd is not None
                                    else " "
                                )
                                resPlaceHolders["cotgtheta"] = (
                                    f"{checkLog_SLU_T.cotgTheta:.1f}"
                                    if checkLog_SLU_T.cotgTheta is not None
                                    else " "
                                )
                                resPlaceHolders["Asw"] = (
                                    f"{checkLog_SLU_T.Asw:.0f}"
                                    if checkLog_SLU_T.Asw is not None
                                    else " "
                                )
                                resPlaceHolders["step"] = (
                                    f"{checkLog_SLU_T.s:.0f}"
                                    if checkLog_SLU_T.s is not None
                                    else " "
                                )
                                resPlaceHolders["sigmacp"] = (
                                    f"{checkLog_SLU_T.sigmacp:.1f}"
                                    if checkLog_SLU_T.sigmacp is not None
                                    else " "
                                )

                            if res.safetyFactor is not None:
                                safetyFactor_SLU_T = SafetyFactor_SLU_T(
                                    **res.safetyFactor
                                )
                                resPlaceHolders["FS"] = (
                                    f"{safetyFactor_SLU_T.globalCheck:.2f}"
                                    if safetyFactor_SLU_T.globalCheck is not None
                                    else " "
                                )

                            if res.check is not None:
                                check_SLU_T = Check_SLU_T(**res.check)
                                if check_SLU_T.globalCheck is not None:
                                    resPlaceHolders["check"] = (
                                        "OK" if check_SLU_T.globalCheck else "NOOK"
                                    )
                                else:
                                    resPlaceHolders["check"] = " "

                            placeHolders["check_SLU_T"].append(resPlaceHolders)

                    f.add(
                        templateName="template-ita-rc-slu-t.tex",
                        templatePlaceholders=placeHolders,
                    )

                ###############################################################
                # # #                   REPORT FOR SLE F                  # # #
                ###############################################################
                if crit.criteria == CheckableCriteriaEnum.SLE_F:
                    print("crit.criteria == models.CheckableCriteriaEnum.SLE_F")
                    f.add(line=r"\newpage")
                    f.add(line=r"\section{Verifica SLE a fessurazione}")
                    placeHolders["check_SLE_F"] = []
                    if crit.results is not None:
                        for res in crit.results:
                            resPlaceHolders = {"id": res.loadId}
                            if res.checkLog is not None:
                                checkLog_SLE_F = CheckLog_SLE_F(**res.checkLog)
                                if checkLog_SLE_F.solverNMUncracked is not None:
                                    resPlaceHolders["Ned"] = (
                                        "{:.1f}".format(
                                            checkLog_SLE_F.solverNMUncracked.Ned / 1000
                                        )
                                        if checkLog_SLE_F.solverNMUncracked.Ned is not None
                                        else " "
                                    )
                                    resPlaceHolders["Med"] = (
                                        "{:.1f}".format(
                                            checkLog_SLE_F.solverNMUncracked.Med / 1000000
                                        )
                                        if checkLog_SLE_F.solverNMUncracked.Med is not None
                                        else " "
                                    )
                                    resPlaceHolders["sigmac"] = (
                                        "{:.2f}".format(
                                            checkLog_SLE_F.solverNMUncracked.sigmac_max_u
                                        )
                                        if checkLog_SLE_F.solverNMUncracked.sigmac_max_u
                                        is not None
                                        else " "
                                    )
                                if checkLog_SLE_F.solverCRACKMeasures is not None:
                                    resPlaceHolders["wk"] = (
                                        "{:.3f}".format(
                                            checkLog_SLE_F.solverCRACKMeasures.wk
                                        )
                                        if checkLog_SLE_F.solverCRACKMeasures.wk is not None
                                        else " "
                                    )
                                    resPlaceHolders["sigmasStiff"] = (
                                        "{:.1f}".format(
                                            checkLog_SLE_F.solverCRACKMeasures.sigmas_stiffning
                                        )
                                        if checkLog_SLE_F.solverCRACKMeasures.sigmas_stiffning
                                        is not None
                                        else " "
                                    )
                                    resPlaceHolders["deltasm"] = (
                                        "{:.1f}".format(
                                            checkLog_SLE_F.solverCRACKMeasures.deltasm
                                        )
                                        if checkLog_SLE_F.solverCRACKMeasures.deltasm
                                        is not None
                                        else " "
                                    )
                                    resPlaceHolders["epsism"] = (
                                        "{:.2e}".format(
                                            checkLog_SLE_F.solverCRACKMeasures.epsism
                                        )
                                        if checkLog_SLE_F.solverCRACKMeasures.epsism
                                        is not None
                                        else " "
                                    )
                                    resPlaceHolders["roeff"] = (
                                        "{:.2e}".format(
                                            checkLog_SLE_F.solverCRACKMeasures.roeff
                                        )
                                        if checkLog_SLE_F.solverCRACKMeasures.roeff
                                        is not None
                                        else " "
                                    )
                                if checkLog_SLE_F.solverCRACKLimit is not None:
                                    resPlaceHolders["wkMax"] = (
                                        f"{checkLog_SLE_F.solverCRACKLimit.wk:.3f}"
                                        if checkLog_SLE_F.solverCRACKLimit.wk is not None
                                        else " "
                                    )
                                    resPlaceHolders["fctcrack"] = (
                                        "{:.2f}".format(
                                            checkLog_SLE_F.solverCRACKLimit.fctcrack
                                        )
                                        if checkLog_SLE_F.solverCRACKLimit.fctcrack
                                        is not None
                                        else " "
                                    )
                                if checkLog_SLE_F.solverCRACKParam is not None:
                                    resPlaceHolders["sigmas"] = (
                                        "{:.1f}".format(
                                            checkLog_SLE_F.solverCRACKParam.sigmasMax
                                        )
                                        if checkLog_SLE_F.solverCRACKParam.sigmasMax
                                        is not None
                                        else " "
                                    )
                                    resPlaceHolders["xi"] = (
                                        f"{checkLog_SLE_F.solverCRACKParam.xi:.1f}"
                                        if checkLog_SLE_F.solverCRACKParam.xi is not None
                                        else " "
                                    )
                                    resPlaceHolders[
                                        "state"
                                    ] = checkLog_SLE_F.solverCRACKParam.crackState.toStr()

                            if res.safetyFactor is not None:

                                safetyFactor = SafetyFactor_SLE_F(
                                    **res.safetyFactor
                                )

                                resPlaceHolders["FS"] = (
                                    f"{safetyFactor.crack:.2f}"
                                    if safetyFactor.crack is not None
                                    else " "
                                )

                            if res.check is not None:
                                check = Check_SLE_F(**res.check)
                                if check.crack is not None:
                                    resPlaceHolders["check"] = (
                                        "OK" if check.crack else "NOOK"
                                    )
                                    resPlaceHolders["severity"] = check.severity.toStr()
                                else:
                                    resPlaceHolders["check"] = " "

                            placeHolders["check_SLE_F"].append(resPlaceHolders)

                    f.add(
                        templateName="template-ita-rc-sle-f.tex",
                        templatePlaceholders=placeHolders,
                    )

        return f


class ReportBuilder(FragmentsBuilder):
    def __init__(self, iData: ModelInputRcSecCheck, oData: ModelOutputRcSecCheck):
        super().__init__()
        self.__iData = iData
        self.__oData = oData

    def setFragmentOptions(self, options: dict) -> bool:
        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(ServerSettings().latex_templates_path)

        codesFragment = CodesFB(ServerSettings().latex_templates_path)

        if self.__iData.code is not None:
            codesFragment.appendUniqueCode(Code(self.__iData.code.value))
        if (
            self.__iData.section.concreteMat is not None
            and self.__iData.section.concreteMat.code is not None
        ):
            print(self.__iData.section.concreteMat.code.value)
            codesFragment.appendUniqueCode(
                Code(self.__iData.section.concreteMat.code.value)
            )
        if (
            self.__iData.section.steelMat is not None
            and self.__iData.section.steelMat.code is not None
        ):
            codesFragment.appendUniqueCode(
                Code(self.__iData.section.steelMat.code.value)
            )

        if codesFragment.len() != 0:
            f.add(lines=codesFragment.buildFragment().frags())

        rcsSection = self.__iData.buildRcsRectangular()
        section_description = rcsSection.getDescr()
        if section_description != "":
            section_title = "Geometria della sezione (" + section_description + ")"
        else:
            section_title = "Geometria della sezione"

        if rcsSection is not None:

            sectionFB = ConcreteSectionFB(
                ServerSettings().latex_templates_path, rcsSection
            )
            sectionFB.setFragmentOptions(
                {
                    "section_title": section_title,
                    "section_level": EnumFBSection.SEC_SECTION,
                }
            )

            sectionFrag = sectionFB.buildFragment()
            if sectionFrag is not None:
                lines = sectionFrag.frags()
                if lines is not None:
                    f.add(lines=lines)

            f.add(line=r"\section{Caratteristiche meccaniche dei materiali}")

            concreteFB = ConcreteFB(
                ServerSettings().latex_templates_path, rcsSection.getConcreteMaterial()
            )
            concreteFB.setFragmentOptions(
                {
                    "section_title": "Calcestruzzo",
                    "section_level": EnumFBSection.SEC_SUBSECTION,
                }
            )
            if concreteFB.buildFragment().frags():
                f.add(lines=concreteFB.buildFragment().frags())

            steelFB = SteelConcreteFB(
                ServerSettings().latex_templates_path, rcsSection.getSteelMaterial()
            )
            steelFB.setFragmentOptions(
                {
                    "section_title": "Acciaio",
                    "section_level": EnumFBSection.SEC_SUBSECTION,
                }
            )
            if steelFB.buildFragment().frags():
                f.add(lines=steelFB.buildFragment().frags())

            loadsFB = self.__iData.buildLoads()
            loadsFB.setFragmentOptions(
                {
                    "section_title": "Carichi e combinazioni",
                    "section_level": EnumFBSection.SEC_SECTION,
                }
            )
            loadsFrag = loadsFB.buildFragment()
            if sectionFrag.frags():
                f.add(lines=loadsFrag.frags())

            results_Frag = self.__oData.buildFragment()
            if results_Frag.frags():
                f.add(lines=results_Frag.frags())

        else:
            log("ERR", "section null. Exit", 1)

        return f


class ModelResourcesRcSecCheck(BaseModel):
    materialConcreteCatalogue: Optional[CodeConcreteSelector] = None
    materialSteelRebarCatalogue: Optional[
        Union[CodeSteelRebarSelector, None]
    ] = None
    fireDesignCurve: FireDesignCurve = FireDesignCurve()
    fireDesignRTime: FireDesignRTime = FireDesignRTime()


class SolverOptions(str, Enum):
    STATIC = "static"
    THERMAL = "thermal"


class RcSecRectSolver(Solver):
    def __init__(self):
        super().__init__()
        self.__ll: Literal[0, 1, 2, 3] = 1

    def setLogLevel(self, ll: Literal[0, 1, 2, 3]):
        self.__ll = ll

    @staticmethod
    def __runThermalMap(
        iData: ThermalMapSolverIn,
        jobPath: str = "",
        jobToken: str = "",
        test: bool = False,
    ) -> SolverOut:
        oData = SolverOut()
        oData.log.append("**** srvRcSecCheck thermal mapping start ****")
        section = RCTemplRectEC2()
        section.setDimH(iData.shape.height)
        section.setDimW(iData.shape.width)
        sectionFd = RCRectEC2FireDesign(
            coldSection=section,
            logLevel=3,
            jobToken=jobToken,
            codeAsterLauncher=ServerSettings().codeaster_launcher,
            codeAsterTemplatePath=ServerSettings().codeaster_templates_path,
            codeAsterContainerName=ServerSettings().codeaster_container,
        )

        if sectionFd.setWorkingPath(jobPath):
            oData.log.append("INF: Working path successfully.")
        else:
            oData.log.append("ERR: Working path error. Quit")
            oData.exit = SolverExit.ERROR
            return oData

        if sectionFd.buildMesh():
            oData.log.append("INF: Mesh successfully created.")
        else:
            oData.log.append("ERR: Mesh error.")
            oData.exit = SolverExit.ERROR
            return oData

        if iData.shape.selected is not None:
            if 4 in iData.shape.selected or 6 in iData.shape.selected:
                sectionFd.setEsposedLeft()
                sectionFd.setEsposedRight()
            if 5 in iData.shape.selected:
                sectionFd.setEsposedTop()
            if 7 in iData.shape.selected:
                sectionFd.setEsposedBottom()

        if iData.concrete.moisture is not None:
            sectionFd.setMoisture(iData.concrete.moisture)
            oData.log.append(f"INF: moisture {iData.concrete.moisture}")
        else:
            oData.log.append("INF: moisture None. Use default.")

        if iData.fireDesignCurve is not None:
            sectionFd.setFireCurve(iData.fireDesignCurve)
            oData.log.append(f"INF: fire curve {iData.fireDesignCurve}")
        else:
            oData.log.append("INF: fire curve None. Use default.")

        if iData.fireDesignRTime is not None:
            sectionFd.setTime(iData.fireDesignRTime)
            oData.log.append(f"INF: time {iData.fireDesignRTime}")
        else:
            oData.log.append("INF: time is None. Use default.")

        if sectionFd.buildThermalMap(test=test):
            oData.log.append("INF: thermal map successfully maked.")
        else:
            oData.log.append("ERR: thermal map error.")
            oData.exit = SolverExit.ERROR
            return oData

        # TODO: Choose if we want removing artifacts
        #
        # sectionFd.deleteArtifacts()

        # TODO: Export images with local container
        #
        if sectionFd.exportThermalImgs():
            oData.log.append("INF: export imgs.")
        else:
            oData.log.append("ERR: export imgs..")
            oData.exit = SolverExit.ERROR
            return oData

        return oData

    def __runStatic(
        self, iData: ModelInputRcSecCheck, jobPath: str = ""
    ) -> ModelOutputRcSecCheck:

        oData = ModelOutputRcSecCheck()
        oData.log.append("**** srvRcSecCheck start ****")

        # Build section
        oData.log.append("INF: section forming ...")
        section = iData.buildRcsRectangular()

        if section is not None:
            oData.log.append("INF: ... formed")
        else:
            oData.log.append("ERR: ... an error occurred")

        # Build hot section
        hotSection = RCRectEC2FireDesign(
            coldSection=section,
            workingPath=self.getJobPath(),
            codeAsterLauncher=ServerSettings().codeaster_launcher,
            codeAsterTemplatePath=ServerSettings().codeaster_templates_path,
            codeAsterContainerName=ServerSettings().codeaster_container,
        )

        assert iData.section.concreteMat is not None
        assert iData.section.concreteMat.moisture is not None
        hotSection.setMoisture(iData.section.concreteMat.moisture)

        thermalInFileName = os.path.join(
            self.getJobPath(), "RCRectangularThermalIn.json"
        )
        if os.path.exists(thermalInFileName):
            try:
                oData.log.append("INF: read thermal map solver input file ...")
                with open(thermalInFileName) as jsonFile:
                    jsonObject = json.load(jsonFile)
                    jsonFile.close()
            except OSError:
                oData.log.append("ERR: ... reading thermal map solver input file. Quit")
                oData.exit = SolverExit.ERROR
                return oData

            oData.log.append("INF: thermal map read ...")
            mapSolverInFromFile = ThermalMapSolverIn(**jsonObject)

            hotSection.setTime(mapSolverInFromFile.fireDesignRTime)
            hotSection.setFireCurve(mapSolverInFromFile.fireDesignCurve)

            oData.log.append(f"INF: time = {hotSection.getTime()}...")
        else:
            oData.log.append("INF: thermal map solver input file does not exists ...")

        # Build loads
        listOfLoads = iData.buildLoads()
        nbl = len(listOfLoads.forces())

        oData.log.append(f"INF: {nbl:.0f} loads added")

        if section is not None:

            # Build check and checkable
            checkable = RcsRectangular(section, hotSection)
            print()
            if jobPath == "":
                checkable.setOption_SLU_NM_save(False)
            else:
                checkable.setOption_SLU_NM_save(
                    True, filePath=jobPath, fileName="domain.png"
                )

            checker = Checker()
            checker.setCheckable(checkable)

            listOfCriteria = []
            assert iData.criteria is not None
            for c in iData.criteria:
                listOfCriteria.append(c.value)

            oData.log.append("INF: criteria added")

            assert iData.loadsInCriteria is not None
            listOfLoadsInCriteria = iData.loadsInCriteria
            oData.log.append("INF: loads in criteria added")

            assert iData.code is not None
            code = Code(iData.code.value)
            oData.log.append("INF: checking code added")

            oData.log.append("INF: perform check ...")
            checker.check(
                listOfCriteria, listOfLoads.forces(), code, listOfLoadsInCriteria
            )
            oData.results = Checkable(**checker.getResults())
            oData.log.append("INF: ... end")
        else:
            oData.log.append("ERR: ... can" "t form checker and checkable !!!")

        oData.log.append("**** srvRcSecCheck end ****")
        return oData

    @staticmethod
    def __buildReport(
            jobPath: str = "",
            inFn: str = "",
            outFn: str = "",
            reportName: str = "report"
    ) -> bool:

        if inFn == "" and outFn == "":
            inFn = jobPath + "/RCRectangularIn.json"
            outFn = jobPath + "/RCRectangularOut.json"
        else:
            inFn = str(Path(jobPath) /  Path(inFn))
            outFn = str(Path(jobPath) /  Path(outFn))

        try:
            with open(inFn) as jsonFile:
                jsonObjectIn = json.load(jsonFile)
                jsonFile.close()
        except OSError as e:
            print(f"ERR: open file {inFn} with error {str(e):s}")
            return False
        else:
            print(f"INF: file {inFn} RCRectangularIn open")

        try:
            with open(outFn) as jsonFile:
                jsonObjectOut = json.load(jsonFile)
                jsonFile.close()
        except OSError as e:
            print(f"ERR: open file {outFn} with error {str(e):s}")
            return False
        else:
            print(f"INF: file {outFn} open")

        iData = ModelInputRcSecCheck(**jsonObjectIn)
        oData = ModelOutputRcSecCheck(**jsonObjectOut)

        rb = ReportBuilder(iData, oData)

        f = rb.buildFragment()

        reporter = Reporter(ServerSettings().latex_templates_path)

        prop = ReportProperties()
        if iData.project is not None:
            if iData.project.brief is not None:
                prop.project_brief = iData.project.brief
            if iData.project.uuid is not None:
                prop.report_token = str(iData.project.uuid)[0:8]

        if iData.user is not None:
            if iData.user.usr is not None:
                prop.report_designer = iData.user.usr

        prop.module_name = "RCRectangular"
        prop.module_version = version("pycivil")
        prop.report_date = f"{datetime.now():%d-%m-%Y}"
        prop.report_time = f"{datetime.now():%H:%M:%S}"

        reporter.setProperties(prop)

        if reporter.linkFragments(
            template=ReportTemplateEnum.TEX_ENG_CAL,
            fragments=[f],
        ):
            print("Make PDF after build")
            reporter.compileDocument(path=jobPath, fileName=reportName)
        else:
            print("Error building PDF. Can not make PDF. QUit.")

        return True

    @staticmethod
    def __buildResources() -> ModelResourcesRcSecCheck:

        extracted = (
            (key, list(value.keys())) for key, value in Concrete.tab_fck.items()
        )
        concrete_rows, concrete_cols = zip(*extracted)

        extracted = (
            (key, list(value.keys())) for key, value in ConcreteSteel.tab_steel.items()
        )
        rebar_rows, rebar_cols = zip(*extracted)

        return ModelResourcesRcSecCheck(
            materialConcreteCatalogue=CodeConcreteSelector(
                rows=Rows(value=concrete_rows),
                columns=Columns(value=concrete_cols),
            ),
            materialSteelRebarCatalogue=CodeSteelRebarSelector(
                rows=Rows(value=rebar_rows),
                columns=Columns(value=rebar_cols),
            ),
        )

    def run(self, opt: Enum = None, **kwargs) -> bool:
        jobToken = ""
        if "jobToken" in kwargs.keys():
            if type(kwargs["jobToken"]) == str:
                jobToken = kwargs["jobToken"]
            else:
                log("ERR", "jobToken must be a string", self.__ll)

        test = False
        if "test" in kwargs.keys():
            if type(kwargs["test"]) == bool:
                test = kwargs["test"]
            else:
                log("ERR", "test must be a boolean", self.__ll)

        if not isinstance(opt, SolverOptions):
            log("ERR", "Options unknown class", self.__ll)
            return False

        idata = self.getModelInput()
        if opt == SolverOptions.STATIC:

            if not isinstance(idata, ModelInputRcSecCheck):
                log("ERR", "Model input unknown class not ModelInput_RcSecCheck", self.__ll)
                return False

            oData = self.__runStatic(idata, self.getJobPath())

        elif opt == SolverOptions.THERMAL:

            if not isinstance(idata, ThermalMapSolverIn):
                log("ERR", "Model input unknown class not ThermalMapSolverIn", self.__ll)
                return False

            oData = self.__runThermalMap(idata, self.getJobPath(), jobToken, test)
            if oData.exit == SolverExit.ERROR:
                log("ERR", "I can't build thermal map for unknown error", self.__ll)
                return False
        else:
            log("ERR", "Only THERMAL and STATIC options", self.__ll)
            return False

        self._setModelOutput(oData)
        return True

    def buildReport(self, opt: Union[Enum, None] = None, **kwargs) -> bool:

        if opt is None and len(kwargs) == 0:
            log("INF", "Building report from files ...", self.__ll)

        if type(opt) == ReportOption and opt == ReportOption.REPORT_FROM_RUN:
            log("INF", "Building report from last run ...", self.__ll)

            in_fn = Path("RCRectangularIn.json")
            model_in_file = Path(self.getJobPath()) / in_fn
            self.modelInputFile = str(model_in_file)
            model_in_file.write_text(json.dumps(self.getModelInput().model_dump(), indent=4, cls=UUIDEncoder))

            out_fn = Path("RCRectangularOut.json")
            model_out_file = Path(self.getJobPath()) / out_fn
            self.modelOutputFile =  str(model_out_file)
            model_out_file.write_text(json.dumps(self.getModelOutput().model_dump(), indent=4, cls=UUIDEncoder))

        ret_val = self.__buildReport(
            jobPath=self.getJobPath(),
            inFn=self.modelInputFile,
            outFn=self.modelOutputFile,
            reportName=self.reportName,
        )
        return ret_val

    def buildResources(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        resources = self.__buildResources()
        self._setModelResources(resources)
        return True

    def _buildSolverFromModelInput(self, model: BaseModel) -> bool:
        return True


class Check_SLU_NM(BaseModel):
    interactionDomain: Optional[bool] = None


class Check_SLU_NM_FIRE(BaseModel):
    interactionDomain: Optional[bool] = None
    interactionDomain_Cold: Optional[bool] = None
    interactionDomain_Hot: Optional[bool] = None


class Check_SLE_NM(BaseModel):
    globalCheck: Optional[bool] = None
    concrete: Optional[bool] = None
    steel: Optional[bool] = None


class Check_SLE_F(BaseModel):
    crack: Optional[float] = None
    severity: Optional[CrackSeverity] = None


class Check_SLU_T(BaseModel):
    globalCheck: Optional[bool] = None


class CheckLog_SLU_NM(BaseModel):
    Med: Optional[float] = None
    Mer: Optional[float] = None
    Ned: Optional[float] = None
    Ner: Optional[float] = None
    msg: str = ""
    model_config = ConfigDict(extra="forbid")


class CheckLog_SLU_NM_FIRE(BaseModel):
    Wred: Optional[float] = None
    Hred: Optional[float] = None
    Ned: Optional[float] = None
    Med: Optional[float] = None
    Ner_Cold: Optional[float] = None
    Mer_Cold: Optional[float] = None
    Ner_Hot: Optional[float] = None
    Mer_Hot: Optional[float] = None
    model_config = ConfigDict(extra="forbid")


class CheckLog_SLU_T(BaseModel):
    Ved: Optional[float] = None
    Vrd: Optional[float] = None
    Vrsd: Optional[float] = None
    Vrcd: Optional[float] = None
    cotgTheta: Optional[float] = None
    sigmacp: Optional[float] = None
    alpha: Optional[float] = None
    al: Optional[float] = None
    alphac: Optional[float] = None
    err: Optional[bool] = None
    path: Optional[dict] = None
    fyd: Optional[float] = None
    fcd: Optional[float] = None
    bw: Optional[float] = None
    Asw: Optional[float] = None
    s: Optional[float] = None
    d: Optional[float] = None
    check: Optional[int] = None
    model_config = ConfigDict(extra="forbid")


class CheckLog_SLE_NM(BaseModel):
    msg: List[str] = field(default_factory=list)
    Ned: Optional[float] = None
    Med: Optional[float] = None
    sigmac: Optional[float] = None
    sigmas: Optional[float] = None
    sigmxc: Optional[float] = None
    sigmxs: Optional[float] = None
    xi: Optional[float] = None
    sigmaci: Optional[List[float]] = None
    sigmasi: Optional[List[float]] = None
    model_config = ConfigDict(extra="forbid")


class SLE_F_NMCracked(BaseModel):
    Ned: Optional[float]
    Med: Optional[float]
    sigmac: Optional[float]
    sigmas: Optional[float]
    xi: Optional[float]
    model_config = ConfigDict(extra="forbid")


class SLE_F_NMUncracked(BaseModel):
    Ned: Optional[float]
    Med: Optional[float]
    sigmac_u: Optional[float]
    sigmas_u: Optional[float]
    xi_u: Optional[float]
    sigmac_max_u: Optional[float]
    model_config = ConfigDict(extra="forbid")


class SLE_F_CRACKParam(BaseModel):
    xi: Optional[float]
    epsi: Optional[float]
    hcEff: Optional[float]
    steelArea: Optional[float]
    dgs: Optional[float]
    deq: Optional[float]
    sigmasMax: Optional[float]
    rebarsInterDistance: Optional[float]
    rebarsCover: Optional[float]
    crackState: Optional[SectionCrackedStates]
    model_config = ConfigDict(extra="forbid")


class SLE_F_CRACKMeasures(BaseModel):
    wk: Optional[float]
    epsism: Optional[float]
    sigmas_stiffning: Optional[float]
    deltasm: Optional[float]
    deltasm1: Optional[float]
    deltasm2: Optional[float]
    roeff: Optional[float]
    zoneC: Optional[float]
    k2: Optional[float]
    alpham: Optional[float]
    epsi1: Optional[float]
    epsi2: Optional[float]
    model_config = ConfigDict(extra="forbid")


class SLE_F_CRACKLimit(BaseModel):
    wk: Optional[float]
    fctcrack: Optional[float]
    sigmac: Optional[float]
    model_config = ConfigDict(extra="forbid")


class CheckLog_SLE_F(BaseModel):
    solverNMCracked: Optional[SLE_F_NMCracked] = None
    solverNMUncracked: Optional[SLE_F_NMUncracked] = None
    solverCRACKParam: Optional[SLE_F_CRACKParam] = None
    solverCRACKMeasures: Optional[SLE_F_CRACKMeasures] = None
    solverCRACKLimit: Optional[SLE_F_CRACKLimit] = None
    msg: str = ""


class SafetyFactor_SLU_NM(BaseModel):
    interactionDomain: Optional[float] = None


class SafetyFactor_SLU_NM_FIRE(BaseModel):
    interactionDomain: Optional[float] = None
    interactionDomain_Cold: Optional[float] = None
    interactionDomain_Hot: Optional[float] = None


class SafetyFactor_SLE_NM(BaseModel):
    globalCheck: Optional[float] = None
    concrete: Optional[float] = None
    steel: Optional[float] = None


class SafetyFactor_SLE_F(BaseModel):
    crack: Optional[float] = None


class SafetyFactor_SLU_T(BaseModel):
    globalCheck: Optional[float] = None

class Media_SLU_NM_FIRE(BaseModel):
    check_SLU_NM_FIRE_NTC2018_image_url: Optional[str] = None



