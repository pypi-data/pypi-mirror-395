from dataclasses import field
from enum import Enum
from typing import List, Literal, Tuple, Union, Optional

import numpy as np
from pydantic import BaseModel

from pycivil.EXAUtils.EXAExceptions import EXAExceptions as ex
from pycivil.EXAGeometry.clouds import PointCloud2d
from pycivil.EXAStructural.lawcodes import codeEC212 as fireCode
from pycivil.EXAStructural.checkable import Checkable
from pycivil.EXAStructural.lawcodes.codeEC212 import RMinutes, FireCurve
from pycivil.EXAStructural.lawcodes.codeNTC2018 import (
    CrackOut,
    crackMeasure,
    shearCheckWithRebar,
)
from pycivil.EXAStructural.codes import Code
from pycivil.EXAStructural.loads import (
    ForcesOnSection,
    Frequency_Enum,
    LimiteState_Enum,
)
from pycivil.EXAStructural.materials import ConcreteModel
from pycivil.EXAStructural.sections import (
    RectangularShape,
    SteelDisposerSingle,
)
from pycivil.EXAStructural.templateRCRect import (
    CrackParameters,
    RCTemplRectEC2,
    SectionCrackedStates,
)
from pycivil.EXAStructural.templateRCRectFire import RCRectEC2FireDesign
from pycivil.EXAUtils.logging import log


class CrackSeverity(str, Enum):
    A1FR = "A_1_FR"
    A1QP = "A_1_QP"
    A2FR = "A_2_FR"
    A2QP = "A_2_QP"
    B1FR = "B_1_FR"
    B1QP = "B_1_QP"
    B2FR = "B_2_FR"
    B2QP = "B_2_QP"
    C1FR = "C_1_FR"
    C1QP = "C_1_QP"
    C2FR = "C_2_FR"
    C2QP = "C_2_QP"
    ND = "ND"

    def toStr(self) -> str:
        if self == CrackSeverity.A1FR:
            return "A1FR"
        if self == CrackSeverity.A1QP:
            return "A1QP"
        if self == CrackSeverity.A2FR:
            return "A2FR"
        if self == CrackSeverity.A2QP:
            return "A2QP"
        if self == CrackSeverity.B1FR:
            return "B1FR"
        if self == CrackSeverity.B1QP:
            return "B1QP"
        if self == CrackSeverity.B2FR:
            return "B2FR"
        if self == CrackSeverity.B2QP:
            return "B2QP"
        if self == CrackSeverity.C1FR:
            return "C1FR"
        if self == CrackSeverity.C1QP:
            return "C1QP"
        if self == CrackSeverity.C2FR:
            return "C2FR"
        if self == CrackSeverity.C2QP:
            return "C2QP"
        if self == CrackSeverity.ND:
            return "ND"
        return ""


class RcsRectangular(Checkable):
    def __init__(
        self, obj: RCTemplRectEC2, hotSection: Union[RCRectEC2FireDesign, None] = None
    ):
        Checkable.__init__(self)

        if not isinstance(obj, RCTemplRectEC2):
            raise TypeError("obj must be a RCTemplRectEC2 class")

        Checkable._setCriteria(
            self, ["SLE-NM", "SLE-F", "SLU-NM", "SLU-T", "SLU-NM-FIRE"]
        )
        Checkable._setCheckableObj(self, obj)
        self.__obj = obj

        self.__hotSection = hotSection

        self.__ll: Literal[0, 1, 2, 3] = 2

        self.__check_SLU_NM_NTC2018_opt_image_save = True
        self.__check_SLU_NM_NTC2018_opt_image_fileName = "domain.png"
        self.__check_SLU_NM_NTC2018_opt_image_filePath = ""

        self.__domain_SLU_pt_nb = 100

    def setOption_SLU_NM_save(
        self, export: bool = True, filePath: str = "", fileName: str = "domain.png"
    ):
        self.__check_SLU_NM_NTC2018_opt_image_save = export
        self.__check_SLU_NM_NTC2018_opt_image_fileName = fileName
        self.__check_SLU_NM_NTC2018_opt_image_filePath = filePath

    def setLogLevel(self, ll: int) -> None:
        self.__ll = ll

    def setMaxPointsForSLUDomain(self, nb: int):
        self.__domain_SLU_pt_nb = nb

    def check(
        self,
        criteria: Union[List[str], None],
        loads: Union[List[ForcesOnSection], None],
        law: Union[Code, None],
        loadsSelector: Union[List[List[int]], None],
    ) -> dict:

        if criteria is None:
            criteria = []
        if loads is None:
            loads = []
        if law is None:
            law = Code()
        if loadsSelector is None:
            loadsSelector = []

        self._validateCriteria(criteria)
        self._setLoads(loads)
        self._setCode(law)
        self._setLoadsSelector(loadsSelector)

        if len(self._criteriaForCheck()) != len(loadsSelector):
            raise ex(
                "001",
                "Selectors must have same lenght of Criteria",
                type(len(loadsSelector)),
            )

        self._getResults()["name"] = "RcsRectangular"
        self._getResults()["code"] = law.codeStr()
        resultsArray = []
        self._getResults()["resultsForCriteria"] = resultsArray
        for ic, crit in enumerate(self._criteriaForCheck()):
            if len(loadsSelector[ic]) != len(set(loadsSelector[ic])):
                log("WRN", f"Some load for {crit} is duplicated", self.__ll)
            if law.codeStr() == "NTC2018":
                results = []
                media = {}
                if crit == "SLE-NM":
                    for _il, lval in enumerate(loadsSelector[ic]):
                        # TODO: Change in log
                        # print(loads[lval].getDescr())
                        if len(loads) -1 < lval:
                            raise ex(
                                "003",
                                f"Size of loads {len(loads)} is less than index {lval}",
                                lval,
                            )
                        __res = self.__check_SLE_NM_NTC2018(loads[lval])
                        __res["loadIndex"] = lval
                        __res["loadId"] = loads[lval].id
                        results.append(__res)

                elif crit == "SLE-F":
                    for _il, lval in enumerate(loadsSelector[ic]):
                        # TODO: Change in log
                        # print(loads[lval].getDescr())
                        if len(loads) -1 < lval:
                            raise ex(
                                "003",
                                f"Size of loads {len(loads)} is less than index {lval}",
                                lval,
                            )
                        __res = self.__check_SLE_F_NTC2018(loads[lval])
                        __res["loadIndex"] = lval
                        __res["loadId"] = loads[lval].id
                        results.append(__res)

                elif crit == "SLU-T":
                    for _il, lval in enumerate(loadsSelector[ic]):
                        # TODO: Change in log
                        # print(loads[lval].getDescr())
                        if len(loads) -1 < lval:
                            raise ex(
                                "003",
                                f"Size of loads {len(loads)} is less than index {lval}",
                                lval,
                            )
                        __res = self.__check_SLU_T_NTC2018(loads[lval])
                        __res["loadIndex"] = lval
                        __res["loadId"] = loads[lval].id
                        results.append(__res)

                elif crit == "SLU-NM":
                    for _il, lval in enumerate(loadsSelector[ic]):
                        # TODO: Change in log
                        # print(loads[lval].getDescr())
                        if len(loads) -1 < lval:
                            raise ex(
                                "003",
                                f"Size of loads {len(loads)} is less than index {lval}",
                                lval,
                            )
                        __res = self.__check_SLU_NM_NTC2018(loads[lval])
                        __res["loadIndex"] = lval
                        __res["loadId"] = loads[lval].id
                        results.append(__res)

                    # Salve interaction domain and tension points in media
                    if self.__check_SLU_NM_NTC2018_opt_image_save:
                        fileName = self.__check_SLU_NM_NTC2018_opt_image_fileName
                        filePath = self.__check_SLU_NM_NTC2018_opt_image_filePath
                        self.__obj.interactionDomainPlot2d(
                            xLabel="N [KN]",
                            yLabel="M [KN*m]",
                            export=filePath + "/" + fileName,
                        )
                        media["check_SLU_NM_NTC2018_image_url"] = (
                            filePath + "/" + fileName
                        )
                else:
                    pass

                if crit in ["SLE-NM", "SLE-F", "SLU-T", "SLU-NM"]:
                    if len(media) > 0:
                        resultsArray.append(
                            {"criteria": crit, "results": results, "media": media}
                        )
                    else:
                        resultsArray.append({"criteria": crit, "results": results})

        for ic, crit in enumerate(self._criteriaForCheck()):
            if law.codeStr() == "NTC2018":
                results = []
                media = {}
                thermalMapResults = None
                if crit == "SLU-NM-FIRE":

                    if len(self.__obj.getInteractionDomain()) == 1:
                        # Build Cold Domain
                        #
                        self.__obj.getConcreteMaterial().set_alphacc(1.0)
                        self.__obj.getConcreteMaterial().set_gammac(1.0)
                        self.__obj.getSteelMaterial().set_gammas(1.0)
                        self.__obj.interactionDomainBuild2d(
                            nbPoints=100,
                            SLS=False,
                            bounding=True,
                            negative_compression=True,
                        )
                        # Build Hot Domain
                        #
                        assert self.__hotSection is not None
                        self.__hotSection.parse()
                        self.__hotSection.buildHotSection()
                        # self.__hotSection.deleteArtifacts()

                        rectShape = RectangularShape(
                            height=self.__obj.getDimH(), width=self.__obj.getDimW()
                        )
                        rebars = []
                        for r in self.__obj.getSteelRebar():
                            rebars.append(
                                SteelDisposerSingle(
                                    id=r.getId(),
                                    area=r.getArea(),
                                    xpos=r.getOrigin().x,
                                    ypos=r.getOrigin().y,
                                )
                            )

                        temps = self.__obj.getSteelTemperatures()

                        fireDesigneCurve = self.__hotSection.getCurve()

                        if self.__hotSection.getTime() == 30:
                            fireDesigneTime = RMinutes.R30
                        elif self.__hotSection.getTime() == 60:
                            fireDesigneTime = RMinutes.R60
                        elif self.__hotSection.getTime() == 60:
                            fireDesigneTime = RMinutes.R90
                        elif self.__hotSection.getTime() == 90:
                            fireDesigneTime = RMinutes.R90
                        elif self.__hotSection.getTime() == 120:
                            fireDesigneTime = RMinutes.R120
                        elif self.__hotSection.getTime() == 150:
                            fireDesigneTime = RMinutes.R150
                        elif self.__hotSection.getTime() == 180:
                            fireDesigneTime = RMinutes.R180
                        else:
                            fireDesigneTime = RMinutes.RXXX

                        thermalMapResults = ThermalMapResults(
                            reductedShape=rectShape,
                            rebars=rebars,
                            rebarsTemperature=temps,
                            fireDesignCurve=fireDesigneCurve,
                            fireDesignRTime=fireDesigneTime,
                        )

                        self.__obj.interactionDomainBuild2d(
                            nbPoints=100,
                            hotPoints=True,
                            SLS=False,
                            bounding=True,
                            negative_compression=True,
                        )
                        self.__obj.clearTensionPoints()

                    for _il, lval in enumerate(loadsSelector[ic]):
                        # TODO: Change in log
                        # print(loads[lval].getDescr())
                        __res = self.__check_SLU_NM_FIRE_NTC2018(loads[lval])
                        __res["loadIndex"] = lval
                        __res["loadId"] = loads[lval].id
                        results.append(__res)

                    # Salve interaction hot domain and tension points in media
                    #
                    if self.__check_SLU_NM_NTC2018_opt_image_save:
                        fileName = (
                            "hot_" + self.__check_SLU_NM_NTC2018_opt_image_fileName
                        )
                        filePath = self.__check_SLU_NM_NTC2018_opt_image_filePath
                        self.__obj.interactionDomainPlot2d(
                            xLabel="N [KN]",
                            yLabel="M [KN*m]",
                            export=filePath + "/" + fileName,
                            printDomains=[1, 2],
                        )
                        media["check_SLU_NM_FIRE_NTC2018_image_url"] = (
                            filePath + "/" + fileName
                        )

                else:
                    pass

                if crit in ["SLU-NM-FIRE"]:
                    if len(media) > 0:
                        resultsArray.append(
                            {
                                "criteria": crit,
                                "results": results,
                                "criteriaLogs": thermalMapResults,
                                "media": media,
                            }
                        )
                    else:
                        resultsArray.append(
                            {
                                "criteria": crit,
                                "results": results,
                                "criteriaLogs": thermalMapResults,
                            }
                        )

        return self.getResults()

    ###########################
    # Law code NTC2018 checkers
    ###########################
    #
    def __check_SLE_NM_NTC2018(self, load: ForcesOnSection) -> dict:
        [sigmac, sigmas, xi] = self.__obj.solverSLS_NM(load.Fx, load.My)
        if sigmac >= 0:
            sigmac = 0.0
        res = {
            "loadIndex": None,
            "loadId": None,
            "checkLog": {
                "Ned": load.Fx,
                "Med": load.My,
                "sigmac": sigmac,
                "sigmas": sigmas,
                "sigmxc": None,
                "sigmxs": None,
                "xi": xi,
                "msg": [],
                "sigmaci": self.__obj.getConcrStress(),
                "sigmasi": self.__obj.getSteelStress(),
            },
            "check": {"concrete": None, "steel": None, "globalCheck": None},
            "safetyFactor": {"concrete": None, "steel": None, "globalCheck": None},
        }
        if isinstance(load, ForcesOnSection):
            if (
                load.frequency == Frequency_Enum.CHARACTERISTIC
                or load.frequency == Frequency_Enum.QUASI_PERMANENT
            ) and load.limitState == LimiteState_Enum.SERVICEABILITY:
                # Concrete check
                if sigmac >= 0:
                    res["check"]["concrete"] = True
                    res["safetyFactor"]["concrete"] = None
                    res["checkLog"]["msg"].append("totally tension in section")
                else:
                    if load.frequency == Frequency_Enum.CHARACTERISTIC:
                        designStrenght = (
                            self.__obj.getConcreteMaterial().get_sigmac_max_c()
                        )
                    else:
                        designStrenght = (
                            self.__obj.getConcreteMaterial().get_sigmac_max_q()
                        )

                    res["checkLog"]["sigmxc"] = -designStrenght

                    designLoad = -sigmac
                    res["safetyFactor"]["concrete"] = designStrenght / designLoad

                    if res["safetyFactor"]["concrete"] > 1.0:
                        res["check"]["concrete"] = True
                    else:
                        res["check"]["concrete"] = False

                # Steel check
                if load.frequency == Frequency_Enum.CHARACTERISTIC:
                    if sigmas <= 0:
                        res["check"]["steel"] = True
                        res["safetyFactor"]["steel"] = None
                        res["checkLog"]["msg"].append(
                            "steel compressed in section totally compressed"
                        )
                    else:
                        designStrenght = (
                            self.__obj.getSteelMaterial().get_sigmas_max_c()
                        )
                        designLoad = abs(sigmas)
                        res["safetyFactor"]["steel"] = designStrenght / designLoad
                        if res["safetyFactor"]["steel"] > 1.0:
                            res["check"]["steel"] = True
                        else:
                            res["check"]["steel"] = False
                        res["checkLog"]["sigmxs"] = designStrenght

                else:
                    res["check"]["steel"] = True
                    res["safetyFactor"]["steel"] = None
                    res["checkLog"]["msg"].append(
                        "load frequency not characteristic. Check steel not defined"
                    )

                res["check"]["globalCheck"] = (
                    res["check"]["steel"] and res["check"]["concrete"]
                )

                if (
                    res["safetyFactor"]["steel"] is None
                    and res["safetyFactor"]["concrete"] is not None
                ):
                    res["safetyFactor"]["steel"] = None
                    res["safetyFactor"]["globalCheck"] = res["safetyFactor"]["concrete"]
                elif (
                    res["safetyFactor"]["steel"] is not None
                    and res["safetyFactor"]["concrete"] is None
                ):
                    res["safetyFactor"]["globalCheck"] = res["safetyFactor"]["steel"]
                    res["safetyFactor"]["concrete"] = None
                elif (
                    res["safetyFactor"]["steel"] is None
                    and res["safetyFactor"]["concrete"] is None
                ):
                    res["safetyFactor"]["globalCheck"] = None
                    res["safetyFactor"]["concrete"] = None
                    res["safetyFactor"]["steel"] = None
                else:
                    res["safetyFactor"]["globalCheck"] = min(
                        res["safetyFactor"]["steel"], res["safetyFactor"]["concrete"]
                    )

            else:
                log(
                    "ERR",
                    "Load must be characteristic or quasi-permanent and serviceability. Quit",
                    1,
                )
                res["checkLog"]["msg"].append(
                    "load not quasi-permanent or characteristic or serviceability"
                )
                res["check"] = None
                res["safetyFactor"] = None

        return res

    def __check_SLU_T_NTC2018(self, load: ForcesOnSection) -> dict:
        res = {
            "loadIndex": None,
            "loadId": None,
            "checkLog": None,
            "check": None,
            "safetyFactor": None,
        }
        if isinstance(load, ForcesOnSection):
            if load.limitState == LimiteState_Enum.ULTIMATE:
                section = self.__obj
                bw = section.getDimW()
                d = min(
                    section.getDimH() - section.getSteelTopRecover(),
                    section.getDimH() - section.getSteelBotRecover(),
                )
                fck = section.getConcreteMaterial().get_fck()
                fyk = section.getSteelMaterial().get_fsy()
                Asw = section.getStirruptArea()
                s = section.getStirruptDistance()
                alpha = section.getStirruptAngle()

                # Medium compression stress
                section.solverSLS_NM(load.Fx, load.My)
                if (
                    section.getConcrStress()[0] <= 0
                    and section.getConcrStress()[3] <= 0
                ):

                    sigmacp = load.Fx / section.getStructConcretelItem().getArea()
                else:
                    sigmacp = 0.0

                gammac = section.getConcreteMaterial().get_gammac()
                gammas = section.getSteelMaterial().get_gammas()
                Ved = load.Fz
                theta = None
                try:
                    checklog = shearCheckWithRebar(
                        bw,
                        d,
                        fck,
                        fyk,
                        Asw,
                        s,
                        alpha,
                        theta,
                        sigmacp,
                        gammac,
                        gammas,
                        Ved,
                        ll=1,
                    )
                    res = {
                        "loadIndex": None,
                        "loadId": load.id,
                        "checkLog": checklog,
                        "check": {
                            "globalCheck": True if checklog["check"] == 1 else False
                        },
                        "safetyFactor": {"globalCheck": checklog["Vrd"] / Ved},
                    }
                except ex:
                    log("ERR", "unknown error on shearCheckWithRebar()", 1)
                    return res
            else:
                res = {
                    "loadIndex": None,
                    "loadId": None,
                    "checkLog": None,
                    "check": None,
                    "safetyFactor": None,
                }
        return res

    def __check_SLE_F_NTC2018(self, load: ForcesOnSection) -> dict:
        res = {
            "loadIndex": -1,
            "loadId": -1,
            "checkLog": {},
            "check": {"crack": False, "severity": "ND"},
            "safetyFactor": {},
        }
        if isinstance(load, ForcesOnSection):
            if not load.limitState == LimiteState_Enum.SERVICEABILITY:
                res["checkLog"]["msg"] = "load not serviceability limit state"
                log("ERR", "Load must be frequent or quasi-permanent. Quit", 1)
                return res

            if (
                not load.frequency == Frequency_Enum.FREQUENT
                and not load.frequency == Frequency_Enum.QUASI_PERMANENT
            ):
                res["checkLog"]["msg"] = "load not frequent or quasi-permanent"
                log("ERR", "Load must be frequent or quasi-permanent. Quit", 1)
                return res

        section = self.__obj
        concrete = section.getConcreteMaterial()
        steel = section.getSteelMaterial()

        res["checkLog"] = {}
        # res['checkLog']['Environnment']={
        #     'Concrete': concrete.getEnvironment(),
        #     'Steel': steel.getEnvironment(),
        # }

        # 1. Preliminary need to solve NM for cracked hypotesis
        [sigmac, sigmas, xi] = section.solverSLS_NM(load.Fx, load.My)
        res["checkLog"]["solverNMCracked"] = {
            "Ned": load.Fx,
            "Med": load.My,
            "sigmac": sigmac,
            "sigmas": sigmas,
            "xi": xi,
        }

        # 2. Calculate geometrical and tension parameters
        #
        section.solverCrack(N=load.Fx, M=load.My)
        cp = section.crackParam()
        fck = float(section.getMaterialConcr().get_fck())
        Es = float(section.getMaterialSteel().get_Es())

        def _crackMeasure(param: Tuple[CrackParameters, CrackParameters], idx: int):
            return crackMeasure(
                epsiBot=param[0].epsi,
                epsiTop=param[1].epsi,
                deq=param[idx].deq,
                As=param[idx].steelArea,
                rebarsCover=param[idx].coverInMaxSteel,
                rebarsDistance=param[idx].rebarDistance,
                hcEff=param[idx].hcEff,
                beff=section.getDimW(),
                hsec=section.getDimH(),
                xi=section.xi(),
                fck=fck,
                sigmas=param[idx].sigmasMax,
                Es=Es,
                load="long",
            )

        if section.crackState() == SectionCrackedStates.CRACKED_BOT:
            _cm = _crackMeasure(cp, 0)
            _cp = cp[0]
        elif section.crackState() == SectionCrackedStates.CRACKED_TOP:
            _cm = _crackMeasure(cp, 1)
            _cp = cp[1]
        elif section.crackState() == SectionCrackedStates.CRACKED:
            cmBot = _crackMeasure(cp, 0)
            cmTop = _crackMeasure(cp, 1)
            if cmBot.wk > cmTop.wk:
                _cm = cmBot
                _cp = cp[0]
            else:
                _cm = cmTop
                _cp = cp[1]
        else:
            _cm = CrackOut()
            _cp = CrackParameters()
        _cp.crackState = section.crackState()
        res["checkLog"]["solverCRACKParam"] = _cp.toDict()
        res["checkLog"]["solverCRACKMeasures"] = _cm.toDict()

        # 3. Solve NM for uncracked hypotesis
        [sigmac_u, sigmas_u, xi_u] = section.solverSLS_NM(load.Fx, load.My, True)
        sigmac_max_u = max(section.getConcrStress())
        res["checkLog"]["solverNMUncracked"] = {
            "Ned": load.Fx,
            "Med": load.My,
            "sigmac_u": sigmac_u,
            "sigmas_u": sigmas_u,
            "xi_u": xi_u,
            "sigmac_max_u": sigmac_max_u,
        }

        case_1 = concrete.isEnvironmentNotAggressive() and not steel.isSteelSensitive()
        case_2 = concrete.isEnvironmentNotAggressive() and steel.isSteelSensitive()
        case_3 = concrete.isEnvironmentAggressive() and not steel.isSteelSensitive()
        case_4 = concrete.isEnvironmentAggressive() and steel.isSteelSensitive()
        case_5 = (
            concrete.isEnvironmentHightAggressive() and not steel.isSteelSensitive()
        )
        case_6 = concrete.isEnvironmentHightAggressive() and steel.isSteelSensitive()

        wkMax = 0
        fct_crack = concrete.get_fct_crack()
        res["checkLog"]["solverCRACKLimit"] = {}
        res["checkLog"]["solverCRACKLimit"]["fctcrack"] = fct_crack
        res["checkLog"]["solverCRACKLimit"]["wk"] = 0.0
        res["checkLog"]["solverCRACKLimit"]["sigmac"] = 0.0

        if case_1:
            log("INF", "CASE (1)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if load.frequency == Frequency_Enum.FREQUENT:
                    res["check"]["severity"] = "A_1_FR"
                    wkMax = 0.4
                elif load.frequency == Frequency_Enum.QUASI_PERMANENT:
                    res["check"]["severity"] = "A_1_QP"
                    wkMax = 0.3

            res["checkLog"]["solverCRACKLimit"]["wk"] = wkMax

            if _cm.wk <= wkMax:
                res["check"]["crack"] = True
            else:
                res["check"]["crack"] = False

            res["safetyFactor"] = (
                {"crack": wkMax / _cm.wk} if _cm.wk != 0 else {"crack": None}
            )

            return res

        elif case_2:
            log("INF", "CASE (2)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if load.frequency == Frequency_Enum.FREQUENT:
                    res["check"]["severity"] = "A_2_FR"
                    wkMax = 0.3
                elif load.frequency == Frequency_Enum.QUASI_PERMANENT:
                    res["check"]["severity"] = "A_2_QP"
                    wkMax = 0.2
                else:
                    wkMax = None

            res["checkLog"]["solverCRACKLimit"]["wk"] = wkMax

            if _cm.wk <= wkMax:
                res["check"]["crack"] = True
            else:
                res["check"]["crack"] = False
            res["safetyFactor"] = (
                {"crack": wkMax / _cm.wk} if _cm.wk != 0 else {"crack": None}
            )

            return res

        elif case_3:
            log("INF", "CASE (3)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if load.frequency == Frequency_Enum.FREQUENT:
                    res["check"]["severity"] = "B_1_FR"
                    wkMax = 0.3
                elif load.frequency == Frequency_Enum.QUASI_PERMANENT:
                    res["check"]["severity"] = "B_1_QP"
                    wkMax = 0.2
                else:
                    wkMax = None

            res["checkLog"]["solverCRACKLimit"]["wk"] = wkMax

            if _cm.wk <= wkMax:
                res["check"]["crack"] = True
            else:
                res["check"]["crack"] = False
            res["safetyFactor"] = (
                {"crack": wkMax / _cm.wk} if _cm.wk != 0 else {"crack": None}
            )

            return res

        elif case_4:
            log("INF", "CASE (4)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if load.frequency == Frequency_Enum.FREQUENT:

                    wkMax = 0.2
                    res["checkLog"]["solverCRACKLimit"]["wk"] = wkMax
                    res["check"]["severity"] = "B_2_FR"

                    if _cm.wk <= wkMax:
                        res["check"]["crack"] = True
                    else:
                        res["check"]["crack"] = False

                    res["safetyFactor"] = (
                        {"crack": wkMax / _cm.wk} if _cm.wk != 0 else {"crack": None}
                    )
                    return res

                elif load.frequency == Frequency_Enum.QUASI_PERMANENT:
                    res["checkLog"]["solverCRACKLimit"]["sigmac"] = 0.0
                    res["check"]["severity"] = "B_2_QP"
                    if sigmac_max_u > 0.0:
                        res["check"]["crack"] = False
                        res["safetyFactor"] = {"crack": 0.0}
                    else:
                        res["check"]["crack"] = True
                        res["safetyFactor"] = {"crack": 1.0}
                    return res

        elif case_5:
            log("INF", "CASE (5)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if (
                    load.frequency == Frequency_Enum.FREQUENT
                    or load.frequency == Frequency_Enum.QUASI_PERMANENT
                ):
                    wkMax = 0.2
                    res["checkLog"]["solverCRACKLimit"]["wk"] = wkMax
                    if _cm.wk <= wkMax:
                        res["check"]["crack"] = True
                    else:
                        res["check"]["crack"] = False

                    res["safetyFactor"] = (
                        {"crack": wkMax / _cm.wk} if _cm.wk != 0 else {"crack": None}
                    )
                    if load.frequency == Frequency_Enum.FREQUENT:
                        res["check"]["severity"] = "C_1_FR"
                    else:
                        res["check"]["severity"] = "C_1_QP"
                    return res

        elif case_6:
            log("INF", "CASE (6)", self.__ll)
            if isinstance(load, ForcesOnSection):
                if load.frequency == Frequency_Enum.FREQUENT:
                    res["check"]["severity"] = "C_2_FR"
                    res["checkLog"]["solverCRACKLimit"]["sigmac"] = fct_crack
                    if sigmac_max_u > fct_crack:
                        res["check"]["crack"] = False
                    else:
                        res["check"]["crack"] = True

                    res["safetyFactor"] = (
                        {"crack": fct_crack / sigmac_max_u}
                        if sigmac_max_u != 0
                        else {"crack": None}
                    )
                    return res

                elif load.frequency == Frequency_Enum.QUASI_PERMANENT:
                    res["checkLog"]["solverCRACKLimit"]["sigmac"] = 0.0
                    res["check"]["severity"] = "C_2_QP"
                    if sigmac_max_u > 0.0:
                        res["check"]["crack"] = False
                    else:
                        res["check"]["crack"] = True
                    res["safetyFactor"] = {"crack": 0.0}
                    return res
        else:
            raise ex("0001", "Wrong choose !!!")
        return res

    def __check_SLU_NM_NTC2018(self, load: ForcesOnSection) -> dict:
        res = {
            "loadIndex": -1,
            "loadId": load.id,
            "checkLog": {},
            "check": {},
            "safetyFactor": {},
        }

        if isinstance(load, ForcesOnSection):
            if load.limitState is not LimiteState_Enum.ULTIMATE:
                res["checkLog"] = {"msg": "load must be in ultimate limit state"}
                log("ERR", "Load must be in ultimate limit state. Quit", 1)
                return res

        section = self.__obj

        if len(section.getInteractionDomain()) == 0:
            section.interactionDomainBuild2d(
                nbPoints=self.__domain_SLU_pt_nb,
                SLS=False,
                bounding=True,
                negative_compression=True,
            )

        brox = (
            section.getInteractionBounding()[0][1]
            - section.getInteractionBounding()[0][0]
        )
        broy = (
            section.getInteractionBounding()[0][3]
            - section.getInteractionBounding()[0][2]
        )

        Ned = load.Fx
        Med = load.My

        section.addTensionPoint2d(float(Ned), float(Med))

        pointsCloud = PointCloud2d(section.getInteractionDomain()[0])

        contained, pintersect, intfactor, pindex = pointsCloud.contains(
            Ned, Med, rayFromCenter=True, ro=(brox, broy)
        )

        # TODO: custom encoder fastAPI
        # Need conver to native python cause fastAPI
        #
        if isinstance(intfactor, np.float64):
            intfactor = intfactor.item()

        res["checkLog"] = {
            "Ned": Ned,
            "Med": Med,
            "Ner": intfactor * Ned,
            "Mer": intfactor * Med,
        }
        res["check"] = {"interactionDomain": contained}
        res["safetyFactor"] = {"interactionDomain": intfactor}

        return res

    def __check_SLU_NM_FIRE_NTC2018(self, load: ForcesOnSection) -> dict:
        res = {
            "loadIndex": -1,
            "loadId": -1,
            "checkLog": {},
            "check": {},
            "safetyFactor": {},
        }

        if isinstance(load, ForcesOnSection):

            if not load.limitState == LimiteState_Enum.ACCIDENTAL:
                res["checkLog"] = {"msg": "load must be in accidental limit state"}
                log("ERR", "Load must be in accidental limit state. Quit", 1)
                return res

            if len(self.__obj.getInteractionDomain()) != 3:
                res["checkLog"] = {"msg": "First must build static interaction domain"}
                log("ERR", "First must build static interaction domain. Quit", 1)
                return res

        idxCold = 1
        brox = (
            self.__obj.getInteractionBounding()[idxCold][1]
            - self.__obj.getInteractionBounding()[idxCold][0]
        )
        broy = (
            self.__obj.getInteractionBounding()[idxCold][3]
            - self.__obj.getInteractionBounding()[idxCold][2]
        )
        Ned = load.Fx
        Med = load.My

        self.__obj.addTensionPoint2d(Ned, Med)
        res["checkLog"]["Wred"] = (
            self.__hotSection.getDeltas()[0] + self.__hotSection.getDeltas()[1]
        )
        res["checkLog"]["Hred"] = (
            self.__hotSection.getDeltas()[2] + self.__hotSection.getDeltas()[3]
        )
        if Ned != 0.0 or Med != 0.0:
            pointsCloud = PointCloud2d(self.__obj.getInteractionDomain()[idxCold])
            contained, pintersect, intfactor, pindex = pointsCloud.contains(
                Ned, Med, rayFromCenter=True, ro=(brox, broy)
            )

            res["checkLog"]["Ned"] = Ned
            res["checkLog"]["Med"] = Med
            res["checkLog"]["Ner_Cold"] = intfactor * Ned
            res["checkLog"]["Mer_Cold"] = intfactor * Med
            res["check"]["interactionDomain_Cold"] = contained
            res["safetyFactor"]["interactionDomain_Cold"] = intfactor

            idxHot = 2
            brox = (
                self.__obj.getInteractionBounding()[idxHot][1]
                - self.__obj.getInteractionBounding()[idxHot][0]
            )
            broy = (
                self.__obj.getInteractionBounding()[idxHot][3]
                - self.__obj.getInteractionBounding()[idxHot][2]
            )

            self.__obj.addTensionPoint2d(Ned, Med)
            pointsCloud = PointCloud2d(self.__obj.getInteractionDomain()[idxHot])
            contained, pintersect, intfactor, pindex = pointsCloud.contains(
                Ned, Med, rayFromCenter=True, ro=(brox, broy)
            )

            res["checkLog"]["Ner_Hot"] = intfactor * Ned
            res["checkLog"]["Mer_Hot"] = intfactor * Med
            res["check"]["interactionDomain_Hot"] = contained
            res["safetyFactor"]["interactionDomain_Hot"] = intfactor

            res["check"]["interactionDomain"] = (
                res["check"]["interactionDomain_Cold"]
                and res["check"]["interactionDomain_Hot"]
            )
            res["safetyFactor"]["interactionDomain"] = min(
                res["safetyFactor"]["interactionDomain_Cold"],
                res["safetyFactor"]["interactionDomain_Hot"],
            )
        else:
            res["checkLog"]["Ned"] = 0.0
            res["checkLog"]["Med"] = 0.0
            res["checkLog"]["Ner_Cold"] = 0.0
            res["checkLog"]["Mer_Cold"] = 0.0
            res["check"]["interactionDomain_Cold"] = True
            res["safetyFactor"]["interactionDomain_Cold"] = 1.0

            res["checkLog"]["Ner_Hot"] = 0.0
            res["checkLog"]["Mer_Hot"] = 0.0
            res["check"]["interactionDomain_Hot"] = True
            res["safetyFactor"]["interactionDomain_Hot"] = 1.0

            res["check"]["interactionDomain"] = True
            res["safetyFactor"]["interactionDomain"] = True
        return res

    def check_SLE_NM_NTC2018(self, load: ForcesOnSection) -> dict:
        return self.__check_SLE_NM_NTC2018(load)

    def check_SLU_T_NTC2018(self, load: ForcesOnSection) -> dict:
        return self.__check_SLU_T_NTC2018(load)

    def check_SLE_F_NTC2018(self, load: ForcesOnSection) -> dict:
        return self.__check_SLE_F_NTC2018(load)

    def check_SLU_NM_NTC2018(self, load: ForcesOnSection) -> dict:
        return self.__check_SLU_NM_NTC2018(load)


class ThermalMapResults(BaseModel):
    reductedShape: RectangularShape
    rebars: Optional[List[SteelDisposerSingle]] = None
    rebarsTemperature: List[float] = field(default_factory=list)
    fireDesignCurve: fireCode.FireCurve
    fireDesignRTime: fireCode.RMinutes


class ThermalMapSolverIn(BaseModel):
    shape: RectangularShape
    concrete: ConcreteModel
    fireDesignCurve: FireCurve
    fireDesignRTime: RMinutes
