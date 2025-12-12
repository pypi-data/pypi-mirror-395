from pathlib import Path
import getpass

from uuid import uuid4

from typing import List, Literal

from pycivil.EXAStructural.loads import (
    ForcesOnSection as Force,
    Frequency_Enum as Frequency,
    LimiteState_Enum as LimitState
)

from pycivil.EXAStructural.checkable import CheckableCriteriaEnum as TpCheck
from pycivil.EXAStructural.materials import (
    Concrete, ConcreteModel, ConcreteSteel, SteelModel
)

from pycivil.EXAStructural.sections import (
    SteelDisposerOnLine,
    SteelDisposerStirrup
)

from pycivil.EXAUtils.models import User, Project
from pycivil.EXAStructural.sections import RectangularShape, ShapePositionEnum, ConcreteSectionModel
from pycivil.EXAStructural.codes import Code

from pycivil.EXAStructural.rcrecsolver.srvRcSecCheck import (
    ModelInputRcSecCheck,
    RcSecRectSolver,
    SolverOptions,
    ReportOption
)

from pycivil.EXAUtils.logging import log

class RCRectCalculator:
    def __init__(self, project_name: str, section_name: str):
        self.__idf: List[int] = []
        self.__forces: List[Force] = []
        self.__mat_concrete: Concrete | None = None
        self.__mat_rebars: ConcreteSteel | None = None
        self.__rebars_disposer_on_line: List[SteelDisposerOnLine] = []
        self.__rebars_stirrup_single: SteelDisposerStirrup | None = None
        self.__shape: RectangularShape | None = None
        self.__criteria: List[TpCheck] = \
            [TpCheck.SLE_NM, TpCheck.SLE_F, TpCheck.SLU_T, TpCheck.SLU_NM]
        self.__loads_in_criteria: List[List[int]] = [[],[],[],[]]
        self.__jobPath: Path | None = None
        self.__report_name: str = "RCRectCalculator_Report"
        self.__solver: RcSecRectSolver = RcSecRectSolver()
        self.__solver_exit: bool | None = None
        self.__ll: Literal[0, 1, 2, 3] = 3
        self.__section_descr: str = section_name
        self.__project_brief: str = project_name

    def setDescription(self, descr: str) -> None:
        self.__section_descr = descr

    def setProjectBrief(self, brief: str) -> None:
        self.__project_brief = brief

    def setLogLevel(self, ll: Literal[0, 1, 2, 3]):
        self.__ll = ll
        self.__solver.setLogLevel(ll)

    def setMaterialConcrete(self,
                            code: Literal["NTC2008", "NTC2018", "EC2", "EC2:ITA", "NTC2018:RFI"],
                            code_str: str,
                            environment: Literal["not aggressive", "low-aggressive", "hight-aggressive"],
                            descr: str=""):
        self.__mat_concrete = Concrete()
        self.__mat_concrete.setMatDescr(descr)
        self.__mat_concrete.setByCode(Code(codeStr=code), code_str)
        self.__mat_concrete.setEnvironment(environment)

    def setMaterialRebars(self,
                          code: Literal["NTC2008", "NTC2018", "EC2", "EC2:ITA", "NTC2018:RFI"],
                          code_str: str,
                          environment: Literal["not sensitive", "sensitive"],
                          descr: str=""):
        self.__mat_rebars = ConcreteSteel()
        self.__mat_rebars.setMatDescr(descr)
        self.__mat_rebars.setByCode(Code(codeStr=code), code_str)
        self.__mat_rebars.setSensitivity(environment)

    def addForce(self,
                 N: float, M: float, T: float,
                 limit_state: Literal["ultimate", "serviceability", "accidental"],
                 check_required: List[Literal["SLE-NM", "SLE-F", "SLU-T", "SLU-NM"]],
                 frequency: Literal["quasi-permanent", "characteristic", "frequent", "ND"] = "ND",
                 descr: str=""):
        self.__forces.append(Force(
            Fx=N, My=M, Fz=T,
            descr=descr, id=len(self.__forces),
            limitState=LimitState(limit_state),
            frequency=Frequency(frequency)
        ))
        for tp in check_required:
            self.__loads_in_criteria[self.__criteria.index(TpCheck(tp))].append(len(self.__forces)-1)

    def addRebarsFromTop(self, num: float, diam: float,  dist_from_top: float, dist_rebars: float):
        self.__rebars_disposer_on_line.append(
            SteelDisposerOnLine(
                fromPos=ShapePositionEnum.MT,
                diameter=diam,
                steelInterDistance=dist_rebars,
                distanceFromPos=dist_from_top,
                number=num)
        )

    def addRebarsFromBot(self, num: float, diam: float,  dist_from_bot: float, dist_rebars: float):
        self.__rebars_disposer_on_line.append(
            SteelDisposerOnLine(
                fromPos=ShapePositionEnum.MB,
                diameter=diam,
                steelInterDistance=dist_rebars,
                distanceFromPos=dist_from_bot,
                number=num)
        )

    def setStirrup(self, area: float, step: float, angle):
        self.__rebars_stirrup_single = SteelDisposerStirrup()
        self.__rebars_stirrup_single.area = area
        self.__rebars_stirrup_single.step = step
        self.__rebars_stirrup_single.angle = angle

    def setDimensions(self, w: float, h: float, ids: int=-1, descr: str=""):
        self.__shape = RectangularShape(width=w, height=h, id=ids, descr=descr)

    def setJobPath(self, folder_path: str) -> bool:
        if not Path(folder_path).is_dir():
            log("ERR",f"Folder path {folder_path} is not a dir !!!", self.__ll)
            return False
        if not Path(folder_path).exists():
            log("ERR",f"Folder path {folder_path} doesn't exists !!!", self.__ll)
            return False
        log("INF", f"Job path {folder_path} successfully set", self.__ll)
        self.__jobPath = Path(folder_path)
        self.__solver.setJobPath(str(self.__jobPath))
        return True

    def run(self) -> bool:
        if self.__mat_concrete is None:
            log("ERR",f"Need to set concrete material with setMaterialConcrete() function !!!", self.__ll)
            return False
        concreteModel = ConcreteModel()
        concreteModel.fromMaterial(self.__mat_concrete)

        if self.__mat_rebars is None:
            log("ERR",f"Need to set rebars material with setMaterialRebars() function !!!", self.__ll)
            return False
        steelModel = SteelModel()
        steelModel.fromMaterial(self.__mat_rebars)

        if self.__shape is None:
            log("ERR",f"Need to set dimensions for concrete with setDimensions() function !!!", self.__ll)
            return False

        section = ConcreteSectionModel(
            concreteMat=concreteModel,
            steelMat=steelModel,
            shape=self.__shape,
            descr=self.__section_descr
        )

        if len(self.__rebars_disposer_on_line) == 0:
            if self.__shape is None:
                log("ERR", f"Need to add rebars with addRebarsFromTop or  addRebarsFromBot function !!!")
                return False
        section.disposerOnLine = self.__rebars_disposer_on_line

        if self.__rebars_stirrup_single is None:
            log("ERR",f"Need to add stirrup with setStirrup() function !!!", self.__ll)
            return False
        section.stirrup = self.__rebars_stirrup_single

        if len(self.__forces) == 0:
            log("ERR",f"Need to add forces with addForce() function !!!", self.__ll)
            return False

        section_solver_input = ModelInputRcSecCheck(loads=self.__forces, section=section)
        section_solver_input.criteria = self.__criteria
        section_solver_input.loadsInCriteria = self.__loads_in_criteria

        userName = ""
        try:
            userName = getpass.getuser()
        except KeyError as e:
            log("WRN",f"In this system user doesn't have name !!!", self.__ll)

        section_solver_input.user = User(usr=userName)
        section_solver_input.project = Project(uuid=uuid4(), brief=self.__project_brief)

        self.__solver.setModelInput(section_solver_input)
        self.__solver_exit = self.__solver.run(SolverOptions.STATIC)
        if self.__solver_exit:
            log("INF",f"Solver run with success.", self.__ll)
        else:
            log("ERR", f"Solver run with error !!!", self.__ll)
        return self.__solver_exit

    def buildReport(self) -> bool:
        if self.__solver_exit is None:
            log("ERR",f"You must use run function before build report !!!", self.__ll)
            return False
        if not self.__solver_exit:
            log("ERR",f"Solver exited with error, can't build a report !!!", self.__ll)
            return False
        log("INF",f"Building report ...", self.__ll)
        self.__solver.reportName = self.__report_name
        exit_val = self.__solver.buildReport(opt=ReportOption.REPORT_FROM_RUN)
        if exit_val:
            log("INF", f"done.", self.__ll)
        else:
            log("ERR", f"... error in building report !!!", self.__ll)
        return exit_val



