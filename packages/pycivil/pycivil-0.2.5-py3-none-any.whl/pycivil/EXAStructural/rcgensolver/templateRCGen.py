import math
import os
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, ConfigDict

from pycivil.EXAUtils.EXAExceptions import EXAExceptions as Ex
from pycivil.EXAGeometry.clouds import PointCloud2d, PointCloud2dMdl
from pycivil.EXAGeometry.geometry import Node2d, Point2d
from pycivil.EXAGeometry.shapes import Shape, ShapeCircle, ShapeRect, ShapesEnum
from pycivil.EXAStructural.loads import ForcesOnSection as Forces
from pycivil.EXAStructural.loads import Frequency_Enum as Frequency
from pycivil.EXAStructural.loads import LimiteState_Enum as LimitState
from pycivil.EXAStructural.materials import (
    Concrete,
    ConcreteModel,
    ConcreteSteel,
    SteelModel,
)
from pycivil.EXAStructural.modeler import SectionModeler
from pycivil.EXAStructural.plot import Geometry2DPlot, SectionPlot, SectionPlotView_Enum
from pycivil.EXAStructural.sections import RectangularShape, SectionStates, ShapeEnum as SectionShapeTp, TShape
from pycivil.EXAUtils.logging import log
from pycivil.EXAUtils.solver import Solver

from pycivil.EXAUtils.report import (
    FragmentsBuilder,
    Fragment,
    getTemplatesPath,
    EnumFBSection
)

from pycivil.EXAUtils.latexReportMakers import (
    CodesFB,
    ConcreteFB,
    SteelConcreteFB,
    ForcesOnSectionListFB
)


class Analysis(str, Enum):
    model_config = ConfigDict(use_enum_values=True)
    CHECK_DOMAIN_SLU = "CHECK_DOMAIN_SLU"
    BOUNDING_SLU = "BOUNDING_SLU"
    ELASTIC_SOLVER = "ELASTIC_SOLVER"
    CHECK_ELASTIC = "CHECK_ELASTIC"


class ArtifactType(str, Enum):
    model_config = ConfigDict(use_enum_values=True)
    SECTION_GEOMETRY = "SECTION_GEOMETRY"
    DOMAIN_SLU = "DOMAIN_SLU"
    ELASTIC_STRESS = "ELASTIC_STRESS"
    REPORT_NOT_EDITABLE = "REPORT_NOT_EDITABLE"
    REPORT_EDITABLE = "REPORT_EDITABLE"
    UNKNOWN = "UNKNOWN"


class Artifact(BaseModel):
    tp: ArtifactType = ArtifactType.UNKNOWN
    path: Path | str = Path()
    name: str = "unknown_artifact"
    ext: str = ""
    def file_name(self) -> Path:
        return self.path / Path(self.name).with_suffix("."+self.ext)

class DomainSLUOptions(BaseModel):
    degreeDivision: int = 15
    rationDivision: int = 30
    rebuild: bool = False


class BoundingSLUOptions(BaseModel):
    degreeDivision: int = 15
    rationDivision: int = 30
    rebuild: bool = False


class CheckResults(BaseModel):
    check: bool = False
    safetyFactor: Union[float, Literal["inf"]] = 0.0


class DomainSLUCheck(BaseModel):
    interactionDomain: CheckResults = CheckResults()
    loadId: int


class InteractionPoints2d(BaseModel):
    component: Literal["Fz", "Mx", "My"] = "Fz"
    pointsCloud2d: PointCloud2dMdl = PointCloud2dMdl()


class DomainSLUCheckLog(BaseModel):
    logs: List[str] = field(default_factory=list)
    Nmin: float
    Nmax: float
    Nrd: Union[float, None]
    Ned: float
    Mxrd: Union[float, None]
    Myrd: Union[float, None]
    Mxed: float
    Myed: float
    loadId: int
    check: bool
    domain: InteractionPoints2d = InteractionPoints2d()
    artifacts: List[Artifact] = []

class CheckDomainSLUResults(BaseModel, FragmentsBuilder):
    logs: List[str] = field(default_factory=list[str])
    globalCheck: Optional[CheckResults] = None
    loadIdCheck: Optional[int] = None
    loadsCheck: Dict[int, DomainSLUCheck] = field(
        default_factory=dict[int, DomainSLUCheck]
    )
    loadsCheckLogs: Dict[int, DomainSLUCheckLog] = field(
        default_factory=dict[int, DomainSLUCheckLog]
    )
    artifacts: List[Artifact] = []
    def model_post_init(self, context: Any, /) -> None:
        self._setFragmentOptions({"job_path": Path()})

    def buildFragment(self) -> Fragment:
        f = Fragment(getTemplatesPath())
        place_holders = dict()
        place_holders["check_SLU_MN"] = []
        place_holders["domainUrls"] = []
        artifacts = []
        for key_load, check_loads in self.loadsCheckLogs.items():
            place_holders_check = dict()
            place_holders_check["id"] = key_load
            place_holders_check["Ned"] = f"{check_loads.Ned / 1e3:.1f}"
            place_holders_check["Mxed"] = f"{check_loads.Mxed / 1e6:.1f}"
            place_holders_check["Myed"] = f"{check_loads.Myed / 1e6:.1f}"

            if check_loads.Nrd is None:
                place_holders_check["Nrd"] = f"n.d."
            else:
                place_holders_check["Nrd"] = f"{check_loads.Nrd / 1e3:.1f}"

            if check_loads.Mxrd is None or check_loads.Mxed == 0.0:
                place_holders_check["Mxrd"] = f"n.d."
            else:
                place_holders_check["Mxrd"] = f"{check_loads.Mxrd / 1e6:.1f}"

            if check_loads.Myrd is None or check_loads.Myed == 0.0:
                place_holders_check["Myrd"] = f"n.d."
            else:
                place_holders_check["Myrd"] = f"{check_loads.Myrd / 1e6:.1f}"

            place_holders_check["FS"] = f"{self.loadsCheck[key_load].interactionDomain.safetyFactor :.2f}"
            if self.loadsCheck[key_load].interactionDomain.check:
                place_holders_check["check"] = f"OK"
            else:
                place_holders_check["check"] = f"NOOK"

            for artifact in check_loads.artifacts:
                if artifact.tp == ArtifactType.DOMAIN_SLU:
                    geometryFilePath_encoded_for_latex = str(str(self.getFragmentOptions()["job_path"] / artifact.file_name())).replace('\\', '/')
                    artifacts.append(
                        {
                            "domainUrl": geometryFilePath_encoded_for_latex,
                            "idLoad": key_load,
                            "newLine": False
                        }
                    )

            place_holders["check_SLU_MN"].append(place_holders_check)

        # TABLE for figures
        #
        maxCols = 2
        maxRows = 3
        max_elem_for_figure = maxCols * maxRows
        nb_elem = len(artifacts)
        nb_figs = math.ceil(nb_elem / max_elem_for_figure)

        figures_matrix = []
        elem = []
        fig_index = 0

        if nb_elem == 1:
            figure_width = 0.9
        else:
            figure_width = 0.41

        for a in artifacts:
            elem.append(a)
            if math.ceil(len(elem) / maxCols) == math.floor(len(elem) / maxCols):
                a["newLine"] = True
            if len(elem) == max_elem_for_figure:
                fig_index += 1
                figures_matrix.append({"domainUrls": elem, "figIndex": fig_index})
                elem = []
        if len(elem) < max_elem_for_figure:
            fig_index += 1
            figures_matrix.append({"domainUrls": elem, "figIndex": fig_index})

        place_holders["figures"] = figures_matrix
        place_holders["nbFigs"] = nb_figs
        place_holders["figuresWidth"] = figure_width
        f.add_template("template-ita-rc-gen-slu-nm.tex", place_holders)
        return f


class ElasticSLSCheck(BaseModel):
    elasticCheck: CheckResults = CheckResults()
    loadId: int = -1


class ElasticSolverResult(BaseModel):
    Ned: float = 0.0
    Mxed: float = 0.0
    Myed: float = 0.0
    sigmacMin: float = 0.0
    sigmacMax: float = 0.0
    sigmasMin: float = 0.0
    sigmasMax: float = 0.0
    tensionPlane: Tuple[float, float, float] = [0.0, 0.0, 0.0]
    sigmaci: dict[int, float] = field(default_factory=dict[int, float])
    sigmasi: dict[int, float] = field(default_factory=dict[int, float])
    state: SectionStates = SectionStates.UNKNOWN
    artifacts: List[Artifact] = []
    # maxIt: int = 0
    # tolIt: float = 0.0


class ElasticSolverResults(BaseModel):
    logs: List[str] = field(default_factory=list[str])
    elasticResults: Dict[int, ElasticSolverResult] = field(
        default_factory=dict[int, ElasticSolverResult]
    )


class ElasticSLSCheckLog(BaseModel):
    logs: List[str] = field(default_factory=list)
    sigmacMinQP: Union[float, None] = None
    sigmacQP: Union[float, None] = None
    sigmacMinCH: Union[float, None] = None
    sigmacCH: Union[float, None] = None
    sigmasMaxCH: Union[float, None] = None
    sigmasCH: Union[float, None] = None
    frequency: Frequency = Frequency.FREQUENCY_ND


class ElasticSLSCheckResults(BaseModel):
    logs: List[str] = field(default_factory=list[str])
    globalCheck: Optional[CheckResults] = None
    loadIdCheck: Optional[int] = None
    loadsCheck: dict[int, ElasticSLSCheck] = field(
        default_factory=dict[int, ElasticSLSCheck]
    )
    loadsCheckLogs: dict[int, ElasticSLSCheckLog] = field(
        default_factory=dict[int, ElasticSLSCheckLog]
    )
    artifacts: List[Artifact] = []


class BoundingSLUResults(BaseModel):
    logs: List[str] = field(default_factory=list)
    minForces: Optional[Forces] = None
    maxForces: Optional[Forces] = None


class Results(BaseModel):
    logs: List[str] = field(default_factory=list)
    sectionKey: str = ""
    domainSLU: Optional[CheckDomainSLUResults] = None
    boundingSLU: Optional[BoundingSLUResults] = None
    elasticSolver: Optional[ElasticSolverResults] = None
    elasticCheck: Optional[ElasticSLSCheckResults] = None
    artifacts: List[Artifact] = []


class RCGenSectionsOutput(BaseModel):
    sectionResults: Dict[int, Results] = field(default_factory=dict[int, Results])


class Options(BaseModel):
    domainSLU: Optional[DomainSLUOptions] = DomainSLUOptions()
    boundingSLU: Optional[BoundingSLUOptions] = BoundingSLUOptions()


class Node2dModel(BaseModel):
    id: int = 0
    coords: Tuple[float, float] = [0.0, 0.0]


class Triangle2dModel(BaseModel):
    id: Tuple[int, int, int] = [0, 0, 0]


class MeshedShape(BaseModel):
    vertices: Dict[int, Tuple[float, float]] = {}
    triangles: Dict[int, Tuple[int, int, int]] = {}
    namedVertices: Dict[str, int] = {}


class Rebar(BaseModel):
    idRebar: int = -1
    idVertex: int = -1
    radius: float = 0


class Geom(BaseModel):
    meshedConcrete: MeshedShape = MeshedShape()
    shapedConcrete: Optional[Union[RectangularShape, TShape]] = None
    rebars: Optional[Dict[int, Rebar]] = {}

class MatForSection(BaseModel):
    concrete: Optional[int] = None
    rebars: Optional[int] = None

class RCGenSection(BaseModel, FragmentsBuilder):
    key: str = ""
    geometry: Geom = Geom()
    materials: MatForSection = MatForSection()
    loads: Dict[int, Forces] = {}

    def model_post_init(self, context: Any, /) -> None:
        self._setFragmentOptions({"geometry_file_path": Path()})

    def buildFragment(self) -> Fragment:
        f = Fragment(getTemplatesPath())
        f.add_line(r"\subsection{Geometria}")

        rebars_place_holders = []
        vertices_place_holders = []
        named_vertices_place_holders = []
        triangles_place_holders = []
        place_holders = {
            "vertices": vertices_place_holders,
            "triangles": triangles_place_holders,
            "rebars": rebars_place_holders,
            "geometryFigure": False,
            "geometryUrl": ""
        }

        # Build figure with few tricks for latex
        #
        geometryFilePath = self.getFragmentOptions()["geometry_file_path"]
        if not isinstance(geometryFilePath, Path):
            log("WRN", f"Fragment option *geometry_file_path* isn't Path class", 2)
        if not geometryFilePath.exists():
            log("WRN", f"FIle path {geometryFilePath} doesn't exists !!!", 2)
        else:
            place_holders["geometryFigure"] = True
        # Only for latex also in windows path repr we need to
        # use /
        geometryFilePath_encoded_for_latex = str(geometryFilePath).replace('\\', '/')
        place_holders["geometryUrl"] = geometryFilePath_encoded_for_latex

        # TABLE for rebars
        #
        rebar_vertex_id = []
        for key_r, value_r in self.geometry.rebars.items():
            rebar_vertex_id.append(value_r.idVertex)
            rebars_place_holders.append(
                {
                    "id": key_r,
                    "xPos": f"{self.geometry.meshedConcrete.vertices[value_r.idVertex][0]:.1f}",
                    "yPos": f"{self.geometry.meshedConcrete.vertices[value_r.idVertex][1]:.1f}",
                    "diam": f"{value_r.radius*2:.0f}",
                    "id_v": f"{rebar_vertex_id[-1]:.0f}",
                }
            )

        # TABLE for solid vertices
        #
        for key_v, value_v in self.geometry.meshedConcrete.vertices.items():
            if key_v not in rebar_vertex_id:
                vertices_place_holders.append(
                    {
                        "id": key_v,
                        "xPos": f"{value_v[0]:.1f}",
                        "yPos": f"{value_v[1]:.1f}"
                    }
                )

        # TABLE for named vertices
        #
        if len(self.geometry.meshedConcrete.namedVertices) > 0:
            for key_n, value_n in self.geometry.meshedConcrete.namedVertices.items():
                named_vertices_place_holders.append(
                    {
                        "name": key_n,
                        "xPos": f"{self.geometry.meshedConcrete.vertices[value_n][0]:.1f}",
                        "yPos": f"{self.geometry.meshedConcrete.vertices[value_n][1]:.1f}"
                    }
                )
            place_holders["namedVertices"] = named_vertices_place_holders
        if self.geometry.shapedConcrete is not None:
            if isinstance(self.geometry.shapedConcrete, RectangularShape):
                place_holders["sectionShape"] = "rettangolare"
                place_holders["rectangularShape"] = True
                place_holders["shape_width"] = f"{self.geometry.shapedConcrete.width:.1f}"
                place_holders["shape_height"] = f"{self.geometry.shapedConcrete.height:.1f}"
            elif isinstance(self.geometry.shapedConcrete, TShape):
                log("WRN", f"Shape TShape not implemented !!!", 2)
            else:
                log("WRN", f"Shape unknown !!!", 2)

        # TABLE for triangles
        #
        for key_t, value_t in self.geometry.meshedConcrete.triangles.items():
            triangles_place_holders.append(
                {
                    "id": key_t,
                    "id1": f"{value_t[0]:.0f}",
                    "id2": f"{value_t[1]:.0f}",
                    "id3": f"{value_t[2]:.0f}",
                }
            )
        f.add_template("template-ita-rc-section-gen.tex", place_holders)
        return f


class MatCatalogue(BaseModel):
    concrete: Dict[int, ConcreteModel] = {}
    steel: Dict[int, SteelModel] = {}


class IdsManagement(BaseModel):
    lastSectionId: int = 0
    lastTriangleId: int = 0
    lastNodeId: int = 0
    lastMatId: int = 0
    lastRebarId: int = 0


class CommandType(str, Enum):
    RUN = "RUN"
    PLOT = "PLOT"
    NONE = "NONE"


class CommandArg(BaseModel):
    name: str = ""
    value: Optional[Any] = None


class Command(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    type: CommandType = CommandType.NONE
    args: List[CommandArg] = []


class RCGenSectionsInput(BaseModel):
    matCatalogue: MatCatalogue = MatCatalogue()
    sections: Dict[int, RCGenSection] = {}
    idsMng: IdsManagement = IdsManagement()
    commands: Optional[List[Command]] = None


class RCGenSectionsModeler(Solver):
    def __init__(self):
        super().__init__()
        self._setSolverName("RCGen")

        # Logger level
        self.__ll: Literal[0, 1, 2, 3] = 1

        # Modeler object
        self.__md = SectionModeler()
        self.__md.setLogLevel(self.__ll)

        # Id management
        self.__last_section_id = 0
        self.__last_triangle_id = 0
        self.__last_node_id = 0
        self.__last_mat_id = 0
        self.__last_rebar_id = 0

        # Section model keys to id for modeler
        self.__sectionKeys: Dict[str, int] = {}

        # Options for analysis
        self.__options: Options = Options()

        self.__journalOfCommands: List[Command] = []

        # Results for analisys
        self.__results: RCGenSectionsOutput = RCGenSectionsOutput()

        # Material used overall with id
        self.__concreteMaterial: Dict[int, Concrete] = {}
        self.__rebarsMaterial: Dict[int, ConcreteSteel] = {}

        # Material on sections with id for model and id for material assigned
        self.__matForConcrete: Dict[int, int] = {}
        self.__matForRebars: Dict[int, int] = {}

        # Loads on sections
        self.__forces: Dict[int, Dict[int, Forces]] = {}

        # Elements for shaped section
        self.__shapeDicts: Dict[int, Shape] = {}
        self.__namedVerticesDict: Dict[int, Dict[str, int]] = {}

        self.__trianglesIds: Union[Dict[int, List[int]], None] = None

    @property
    def logLevel(self):
        return self.__ll

    @logLevel.setter
    def logLevel(self, value):
        self.__ll = value
        self.__md.setLogLevel(value)

    def setJobPath(self, path: str | Path) -> bool:
        if isinstance(path, Path):
            path = str(path)
        log("INF", f"Setting job path {path}...", self.__ll)
        if Path(path).is_dir() and Path(path).exists():
            log("INF", f"... path exist, is a dir and will be set.", self.__ll)
            return super().setJobPath(path)
        log("ERR", f"... path doesn't exist or isn't a dir !!!", self.__ll)
        return False

    def _buildSolverFromModelInput(self, model: BaseModel) -> bool:
        log("INF", f"Model validation ...", self.__ll)
        if not isinstance(model,RCGenSectionsInput):
            log("ERR",f"Model must be RCGenSectionsInput class !!!", self.__ll)
            return False
        log("INF", f"... model is RCGenSectionsInput class", self.__ll)

        log("INF", f"Build catalogue for concrete ...", self.__ll)
        for k in model.matCatalogue.concrete.keys():
            self.addConcreteLaw(mat=model.matCatalogue.concrete[k].toMaterial(), idm=k)

        log("INF", f"Build catalogue for rebars ...", self.__ll)
        for k in model.matCatalogue.steel.keys():
            self.addRebarLaw(mat=model.matCatalogue.steel[k].toMaterial(), idm=k)

        # Sections have key and ids unique
        #
        log("INF", f"Build sections ...", self.__ll)
        for idx, key in enumerate(model.sections.keys()):
            log("INF", f"... adding section id={key} key={model.sections[key].key}", self.__ll)
            self.addSectionModel(key=model.sections[key].key, ids=key)
            if model.sections[key].geometry.shapedConcrete is not None:
                log("INF", f"... forming geometry shaped ...", self.__ll)
                if model.sections[key].geometry.shapedConcrete.tp == SectionShapeTp.RECT:
                    log("INF", f"...... rectangular shape ...", self.__ll)
                    w = model.sections[key].geometry.shapedConcrete.width
                    h = model.sections[key].geometry.shapedConcrete.height
                    if self.__shapeDicts is None:
                        self.__shapeDicts = {self.__md.getCurrent(): ShapeRect(w, h)}
                    else:
                        self.__shapeDicts[self.__md.getCurrent()] = ShapeRect(w, h)
                    if self.__namedVerticesDict is None:
                        self.__namedVerticesDict = {
                            self.__md.getCurrent():
                            model.sections[key].geometry.meshedConcrete.namedVertices
                        }
                    else:
                        self.__namedVerticesDict[self.__md.getCurrent()] = \
                            model.sections[key].geometry.meshedConcrete.namedVertices
                else:
                    log("ERR", f"...... shaped unknown. Exit with False !!!", self.__ll)
                    return False
            else:
                log("INF", f"... adding section id={key} key={model.sections[key].key}", self.__ll)
                log("INF", f"... forming geometry with vertex ...", self.__ll)

            log("INF", f"... adding vertices ...", self.__ll)
            vertices = model.sections[key].geometry.meshedConcrete.vertices
            for key_v in vertices.keys():
                self.addNode(Node2d(vertices[key_v][0], vertices[key_v][1], key_v))

            log("INF", f"... adding triangles ...", self.__ll)
            triangles = model.sections[key].geometry.meshedConcrete.triangles
            for key_t in triangles.keys():
                self.addTriangle(triangles[key_t][0], triangles[key_t][1], triangles[key_t][2], key_t)

            log("INF", f"... adding rebars ...", self.__ll)
            for key_r in model.sections[key].geometry.rebars.keys():
                rebar = model.sections[key].geometry.rebars[key_r]
                self.addRebar(idr=rebar.idRebar, idn=rebar.idVertex, diameter=rebar.radius * 2, use_vertex=True)

            log("INF", f"... assign material laws ...", self.__ll)
            self.assignConcreteLawToCurrentModel(model.sections[key].materials.concrete)
            self.assignRebarLawToCurrentModel(model.sections[key].materials.rebars)

            log("INF", f"... adding loads ...", self.__ll)
            self.assignForces(model.sections[key].loads)

        log("INF", f"... assign last ids ...", self.__ll)
        self.__last_section_id = model.idsMng.lastSectionId
        self.__last_triangle_id = model.idsMng.lastTriangleId
        self.__last_node_id = model.idsMng.lastNodeId
        self.__last_mat_id = model.idsMng.lastMatId
        self.__last_rebar_id = model.idsMng.lastRebarId

        log("INF", f"... journal of commands ...", self.__ll)
        self.__journalOfCommands = model.commands
        return True

    def _buildModelInputFromSolver(self) -> BaseModel:
        modelInput = RCGenSectionsInput()
        # ----------------------------------------------------------------------
        #                      I D S   M A N A G E M E N T
        # ----------------------------------------------------------------------
        modelInput.idsMng.lastSectionId = self.__last_section_id
        modelInput.idsMng.lastTriangleId = self.__last_triangle_id
        modelInput.idsMng.lastNodeId = self.__last_node_id
        modelInput.idsMng.lastMatId = self.__last_mat_id
        modelInput.idsMng.lastRebarId = self.__last_rebar_id
        # ----------------------------------------------------------------------
        #               J O U R N A L   O F   C O M M A N D S
        # ----------------------------------------------------------------------
        modelInput.commands = self.__journalOfCommands
        # ----------------------------------------------------------------------
        #              M A T E R I A L S   C A T A L O G U E S
        # ----------------------------------------------------------------------
        # Concrete
        #
        for k in self.__concreteMaterial.keys():
            modelInput.matCatalogue.concrete[k] = ConcreteModel()
            modelInput.matCatalogue.concrete[k].fromMaterial(self.__concreteMaterial[k])

        # Steel
        #
        for k in self.__rebarsMaterial.keys():
            modelInput.matCatalogue.steel[k] = SteelModel()
            modelInput.matCatalogue.steel[k].fromMaterial(self.__rebarsMaterial[k])

        for key_section in self.__sectionKeys.keys():
            id_section = self.__sectionKeys[key_section]
            sectionModel = RCGenSection(key=key_section)
            # ------------------------------------------------------------------
            #                        G E O M E T R Y
            # ------------------------------------------------------------------
            # Shaped section datas
            #
            if self.__shapeDicts is not None:
                if id_section in self.__shapeDicts.keys():
                    shape = self.__shapeDicts[id_section]
                    if isinstance(shape, ShapeRect):
                        sectionModel.geometry.shapedConcrete = RectangularShape(
                            id=shape.getIds(),
                            descr=shape.getDesc(),
                            width=shape.w(),
                            height=shape.h(),
                        )
                        sectionModel.geometry.meshedConcrete.namedVertices = (
                            self.__namedVerticesDict[id_section]
                        )

            # Meshed section datas
            #
            self.__md.setCurrent(id_section)
            for k, v in self.__md.getNodes().items():
                sectionModel.geometry.meshedConcrete.vertices[k] = (v.xn, v.yn)

            for k, v in self.__md.getTrianglesIds().items():
                sectionModel.geometry.meshedConcrete.triangles[k] = (v[0], v[1], v[2])

            # Rebars datas
            #
            for k, v in self.__md.getCircles().items():
                rebar = Rebar()
                rebar.idRebar = k
                rebar.idVertex = v.center.id
                rebar.radius = v.radius
                sectionModel.geometry.rebars[k] = rebar
            # ------------------------------------------------------------------
            #              M A T E R I A L S  F O R  S E C T I O N
            # ------------------------------------------------------------------
            # Steel material
            #
            if id_section in self.__matForRebars.keys():
                sectionModel.materials.rebars = self.__matForRebars[id_section]
            else:
                log(
                    "WRN",
                    f"Steel material not assigned to " f" section id *{id_section}*!!!",
                    self.__ll,
                )
            # Concrete material
            #
            if id_section in self.__matForConcrete.keys():
                sectionModel.materials.concrete = self.__matForConcrete[id_section]
            else:
                log(
                    "WRN",
                    f"Concrete material not assigned to "
                    f" section id *{id_section}*!!!",
                    self.__ll,
                )
            # ------------------------------------------------------------------
            #                           L O A D S
            # ------------------------------------------------------------------
            sectionModel.loads = self.__forces[id_section]
            modelInput.sections[id_section] = sectionModel
        return modelInput

    def __buildNodeId(self):
        self.__last_node_id += 1
        return self.__last_node_id

    def __buildSectionId(self):
        self.__last_section_id += 1
        return self.__last_section_id

    def __buildTriangleId(self):
        self.__last_triangle_id += 1
        return self.__last_triangle_id

    def __buildRebarId(self):
        self.__last_rebar_id += 1
        return self.__last_rebar_id

    def __buildMatId(self):
        self.__last_mat_id += 1
        return self.__last_mat_id

    @property
    def modeler(self) -> SectionModeler:
        return self.__md

    def rotate(self, degree: float, center: Point2d = Point2d(0.0, 0.0)):
        self.__md.rotate(degree, center)
        return

    def options(self) -> Options:
        return self.__options

    def posNode(self, idn: int) -> Point2d:
        return Point2d(self.__md.getNodeX(idn), self.__md.getNodeY(idn))

    def addRebarsGroup(
        self,
        points: List[Point2d],
        shape: ShapeCircle = None,
        diameter: float = None,
        id_nodes: List[int] = None,
        id_rebars: List[int] = None,
    ) -> List[int]:

        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return []

        if diameter is None and shape is None:
            log("ERR", "Not provided diameter or shape !!! Do nothing.", self.__ll)
            return []

        if diameter is not None and shape is None:
            d = diameter

        # shape is not None and diameter is None
        else:
            if shape.getType() != ShapesEnum.SHAPE_CIRC:
                log("ERR", "Shape subclass unknown or not implemented !!!", self.__ll)
                return []
            else:
                d = shape.getRadius() * 2

        log("INF", "Perform adding rebars", self.__ll)

        if id_nodes is not None and id_rebars is not None:
            if len(id_nodes) != len(points) or len(id_rebars) != len(points):
                log(
                    msg=f"Size of id nodes {len(id_nodes)} "
                    f"and id rebar {len(id_rebars)} must be equal to size "
                    f"of points {len(points)}!!!",
                    tp="ERR",
                    level=self.__ll,
                )
                return []

        barIds = []
        for i, c in enumerate(points):
            if id_nodes is None and id_rebars is None:
                idNode = self.__buildNodeId()
                idRebar = self.__buildRebarId()
            elif id_nodes is not None and id_rebars is not None:
                idNode = id_nodes[i]
                idRebar = id_rebars[i]
            else:
                log("ERR", "Wrong args !!!", self.__ll)
                return []

            if not self.__md.addNode(idNode, c.x, c.y):
                log(msg=f"Cannot add node {idNode} !!!", tp="ERR", level=self.__ll)
                return []

            if not self.__md.addCircle(idRebar, idNode, d / 2):
                log(msg=f"Cannot add rebar {idRebar} !!!", tp="ERR", level=self.__ll)
                return []

            barIds.append(idRebar)

        log(
            msg=f"Added group of {len(barIds)} rebars with node {barIds}.",
            tp="INF",
            level=self.__ll,
        )
        return barIds

    def addSectionModel(self, key: str, current: bool = True, ids: int = -1) -> int:

        if key in self.__sectionKeys.keys():
            log("ERR", "The key is yet present !!!", self.__ll)
            return -1

        if ids < 0:
            id_section = self.__buildSectionId()
        else:
            if ids in self.__sectionKeys.values():
                log("ERR", f"The id {ids} is yet present !!!", self.__ll)
                return -1
            else:
                id_section = ids

        self.__md.addSection(id_section, current)
        self.__sectionKeys[key] = id_section
        self.__results.sectionResults[id_section] = Results(sectionKey=key)

        if self.__forces is None:
            self.__forces = {id_section: {}}
        else:
            self.__forces[id_section] = {}

        return id_section

    def setCurrentModel(self, key: str = None, ids: int = None) -> bool:
        if ids is None and key is None:
            log(
                "ERR",
                "Key and ids are None type. Con't make current nothing !!!",
                self.__ll,
            )
            return False

        if ids is not None and key is None:
            if not self.__md.setCurrent(ids):
                log("ERR", f"The id {ids} isn't present !!!", self.__ll)
                return False
            return True

        if ids is None and key is not None:
            if key not in self.__sectionKeys.keys():
                log("ERR", "The key isn't present !!!", self.__ll)
                return False

        if self.__md.getCurrent() != self.__sectionKeys[key]:
            self.__md.setCurrent(self.__sectionKeys[key])

        return True

    def addNode(self, node: Node2d) -> int:
        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return False

        if node.idn >= 0:
            idn = node.idn
        else:
            idn = self.__buildNodeId()

        if self.__md.addNode(idn, node.x, node.y):
            return idn
        else:
            log(
                msg=f"Node with id={idn} cannot be added to model !!!",
                tp="ERR",
                level=self.__ll,
            )
            return -1

    def addTriangle(self, idn_1: int, idn_2: int, idn_3: int, idt: int = -1) -> int:

        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return False

        if idt >= 0:
            id_tria = idt
        else:
            id_tria = self.__buildTriangleId()

        if self.__md.addTriangle(id_tria, idn_1, idn_2, idn_3):
            if self.__trianglesIds is None:
                self.__trianglesIds = {self.__md.getCurrent(): [id_tria]}
            else:
                if self.__md.getCurrent() in self.__trianglesIds.keys():
                    self.__trianglesIds[self.__md.getCurrent()].append(id_tria)
                else:
                    self.__trianglesIds[self.__md.getCurrent()] = [id_tria]
            return id_tria
        else:
            log(
                msg=f"Triangle with id=[{id_tria}] and nodes "
                f"{idn_1} {idn_2} {idn_3} cannot be added to model !!!",
                tp="ERR",
                level=self.__ll,
            )
            return -1

    def addSolid(self, shape: Union[ShapeRect, ShapeCircle]) -> bool:
        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return False

        if shape.getType() == ShapesEnum.SHAPE_RECT:
            if self.__shapeDicts is None:
                self.__shapeDicts = {self.__md.getCurrent(): shape}
            else:
                self.__shapeDicts[self.__md.getCurrent()] = shape
            log("INF", "Perform build rectangular shape", self.__ll)
            idBL = self.__buildNodeId()
            pBL = shape.getShapePoint("BL")
            idBR = self.__buildNodeId()
            pBR = shape.getShapePoint("BR")
            idTR = self.__buildNodeId()
            pTR = shape.getShapePoint("TR")
            idTL = self.__buildNodeId()
            pTL = shape.getShapePoint("TL")
            if self.__namedVerticesDict is None:
                self.__namedVerticesDict = {
                    self.__md.getCurrent(): {
                        "BL": idBL,
                        "BR": idBR,
                        "TR": idTR,
                        "TL": idTL,
                    }
                }
            else:
                self.__namedVerticesDict[self.__md.getCurrent()] = {
                    "BL": idBL,
                    "BR": idBR,
                    "TR": idTR,
                    "TL": idTL,
                }

            self.__md.addNode(idBL, pBL.x, pBL.y)
            self.__md.addNode(idBR, pBR.x, pBR.y)
            self.__md.addNode(idTR, pTR.x, pTR.y)
            self.__md.addNode(idTL, pTL.x, pTL.y)
            idTria1 = self.__buildTriangleId()
            self.__md.addTriangle(idTria1, idBL, idBR, idTR)
            idTria2 = self.__buildTriangleId()
            self.__md.addTriangle(idTria2, idTR, idTL, idBL)

            if self.__trianglesIds is None:
                self.__trianglesIds = {self.__md.getCurrent(): [idTria1, idTria2]}
            else:
                self.__trianglesIds[self.__md.getCurrent()] = [idTria1, idTria2]

            return True

        log("ERR", "Shape subclass unknown or not implemented !!!", self.__ll)
        return False

    def getShapeVertex(self, name: str) -> Node2d:
        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return Node2d()
        isec = self.__md.getCurrent()

        if self.__shapeDicts is None:
            log("ERR", "Shape not assigned with addSolid() !!!", self.__ll)
            return Node2d()

        if self.__namedVerticesDict is None:
            log(
                "ERR",
                "Vertices are None. Luckly shape not assigned with addSolid() !!!",
                self.__ll,
            )
            return Node2d()
        else:
            if name not in self.__namedVerticesDict[isec].keys():
                log("ERR", f"Name {name} not in vertices keys !!!", self.__ll)
                return Node2d()
            else:
                idNode = self.__namedVerticesDict[isec][name]
                point = self.__shapeDicts[isec].getShapePoint(name)
                return Node2d(point.x, point.y, idNode)

    def addRebar(
        self,
        shape: Union[ShapeCircle, None] = None,
        center: Point2d = Point2d(),
        diameter: float = 0,
        idn: int = -1,
        idr: int = -1,
        use_vertex: bool = False
    ) -> int:

        if self.__md.getCurrent() == -1:
            log("ERR", "None model current !!!", self.__ll)
            return -1

        if not use_vertex:
            if shape is not None:
                if shape.getType() != ShapesEnum.SHAPE_CIRC:
                    log("ERR", "Shape subclass unknown or not implemented !!!", self.__ll)
                    return -1
                c = shape.getShapePoint("O")
                r = shape.getRadius()
            else:
                c = center
                r = diameter / 2

            if idn < 0:
                id_node = self.__buildNodeId()
            else:
                id_node = idn

            if not self.__md.addNode(id_node, c.x, c.y):
                log(
                    msg=f"Add single rebar with node {id_node} error !!!",
                    tp="ERR",
                    level=self.__ll,
                )
                return -1
            else:
                log(
                    msg=f"Add single rebar with node {id_node} with success",
                    tp="INF",
                    level=self.__ll,
                )
        else:
            id_node = idn
            r = diameter / 2

        if idr < 0:
            id_rebar = self.__buildRebarId()
        else:
            id_rebar = idr

        if not self.__md.addCircle(id_rebar, id_node, r):
            log(
                msg=f"Add single rebar with circle {id_rebar} error !!!",
                tp="ERR",
                level=self.__ll,
            )
            return -1
        else:
            log(
                msg=f"Add single rebar with circle {id_rebar} with success",
                tp="INF",
                level=self.__ll,
            )

        log(
            msg=f"Add single rebar with node {id_node} and rebar {id_rebar}",
            tp="INF",
            level=self.__ll,
        )

        return id_rebar

    def plot(self, pfx: str = "", onlyWorst: bool = True) -> None:
        outPath = super().outPath()
        log("INF", "Start plot ...", self.__ll)

        # Journal of command
        com = Command(type=CommandType.PLOT)
        com.args.append(CommandArg(name="pfx", value=pfx))
        com.args.append(CommandArg(name="onlyWorst", value=onlyWorst))
        self.__journalOfCommands.append(com)

        if outPath.exists():
            log("INF", f"... path {outPath} exist !!!", self.__ll)
        else:
            log("INF", f"... making path {outPath}", self.__ll)
            os.mkdir(outPath)
            if outPath.exists():
                log("INF", "... path maked successfully", self.__ll)
            else:
                log("ERR", "... something was wrong", self.__ll)
                return

        # Saving current model
        holdCurrentModel = self.__md.getCurrent()

        sp = SectionPlot()
        sp.logLevel = self.__ll
        sp.modeler = self.__md
        # ----------------------------------------------------------------------
        #                          PLOTTING GEOMETRIES
        # ----------------------------------------------------------------------
        # Iterate over model indexes
        #
        sp.setView(SectionPlotView_Enum.SP_VIEW_SOLID_NODES)
        for modelKey in self.__sectionKeys.keys():
            log("INF", f"... plot model with key = *{modelKey}*", self.__ll)
            self.__md.setCurrent(self.__sectionKeys[modelKey])

            # Plotting with tool
            #
            sp.plot()

            art_path = Path(modelKey)
            art_name = f"{pfx}geometry"

            (outPath / art_path).mkdir(exist_ok=True)
            sp.save(fname=outPath / art_path / art_name, dpi=300, transparent=False)
            res = self.__results.sectionResults[self.__sectionKeys[modelKey]]
            artifact = Artifact(
                tp=ArtifactType.SECTION_GEOMETRY,
                path=art_path.as_posix(),
                name=art_name,
                ext="png",
            )
            res.artifacts.append(artifact)

        if len(self.__results.sectionResults) > 0:
            log("INF", "... plot domains ...", self.__ll)
        else:
            log("INF", "... there isn't domains in results", self.__ll)

        for ids in self.__results.sectionResults:
            res = self.__results.sectionResults[ids]
            log("INF", f"... ... plot domain for section {res.sectionKey}", self.__ll)

            # ------------------------------------------------------------------
            #                       PLOTTING DOMAIN SLU
            # -------------------------------------------------------------------
            if res.domainSLU is None:
                log(
                    "WRN",
                    f"... ... ... domain doesn't calculated "
                    f"for section *{res.sectionKey}*",
                    self.__ll,
                )
            else:

                if onlyWorst:
                    keysToPlot = [res.domainSLU.loadIdCheck]
                else:
                    keysToPlot = res.domainSLU.loadsCheckLogs

                for keyLoad in keysToPlot:
                    loadres = res.domainSLU.loadsCheckLogs[keyLoad]
                    pointsCloud = PointCloud2d(loadres.domain.pointsCloud2d)
                    plotter = Geometry2DPlot(1, 1, figsize=(7, 7), sx=1e-6, sy=1e-6)
                    plotter.addPointCloud(pointsCloud)

                    pointArrayMy = [Point2d(loadres.Mxed, loadres.Myed)]
                    col = "red"
                    if loadres.check:
                        col = "green"
                    plotter.addPointArray(pointArrayMy, [col])
                    plotter.showItems(False, False, True)
                    plotter.setTitles(
                        [
                            f"Domain Mx-My [KNm] at N={loadres.Ned * 1e-3:.1f} [KN] - load id: {loadres.loadId}\n"
                            f"Nmin={loadres.Nmin * 1e-3:.1f} - "
                            f"Nmax={loadres.Nmax * 1e-3:.1f}",
                        ]
                    )
                    plotter.setXLabel(
                        [
                            "Mx [KNm]",
                        ]
                    )
                    plotter.setYLabel(
                        [
                            "My [KNm]",
                        ]
                    )
                    plotter.plot()
                    art_path = Path(res.sectionKey) / "domain"
                    art_name = f"{pfx}load_{loadres.loadId}_MxMy"

                    (outPath / art_path).mkdir(exist_ok=True)
                    plotter.save(fname=outPath / art_path / art_name, dpi=300)
                    artifact = Artifact(
                        tp=ArtifactType.DOMAIN_SLU,
                        path=art_path.as_posix(),
                        name=art_name,
                        ext="png",
                    )
                    if onlyWorst:
                        res.domainSLU.artifacts.append(artifact)
                        loadres.artifacts.append(artifact)
                    else:
                        loadres.artifacts.append(artifact)

            # ------------------------------------------------------------------
            #                    PLOTTING ELASTIC RESULTS
            # -------------------------------------------------------------------
            if res.elasticSolver is None:
                log(
                    "WRN",
                    f"... ... ... elastic solution don't calculated "
                    f"for section *{res.sectionKey}*",
                    self.__ll,
                )
            else:

                if onlyWorst and res.elasticCheck is not None:
                    keysToPlot = [res.elasticCheck.loadIdCheck]
                else:
                    keysToPlot = res.elasticSolver.elasticResults

                sp = SectionPlot()
                sp.logLevel = self.__ll
                sp.modeler = self.__md
                sp.setView(SectionPlotView_Enum.SP_VIEW_STRESSES)
                for keyLoad in keysToPlot:
                    loadres = res.elasticSolver.elasticResults[keyLoad]
                    sp.vertexStresses = loadres.sigmaci
                    sp.rebarStresses = loadres.sigmasi
                    self.__md.setCurrent(self.__sectionKeys[res.sectionKey])
                    sp.plot()

                    art_path = Path(res.sectionKey) / "stress"
                    art_name = f"{pfx}load_{keyLoad}_stress"

                    (outPath / art_path).mkdir(exist_ok=True)
                    sp.save(fname=outPath / art_path / art_name, dpi=300)
                    artifact = Artifact(
                        tp=ArtifactType.ELASTIC_STRESS,
                        path=art_path.as_posix(),
                        name=art_name,
                        ext="png",
                    )
                    if onlyWorst and res.elasticCheck is not None:
                        res.elasticCheck.artifacts.append(artifact)
                        loadres.artifacts.append(artifact)
                    else:
                        loadres.artifacts.append(artifact)

        log("INF", "Stop plot ...", self.__ll)

        # Restore held model
        self.__md.setCurrent(holdCurrentModel)

    def addConcreteLaw(
        self,
        mat: Concrete,
        shape: Literal["PARABOLA-RECTANGLE"] = "PARABOLA-RECTANGLE",
        idm: int = -1,
    ) -> int:

        if shape != "PARABOLA-RECTANGLE":
            log("ERR", "Law shape unknown", self.__ll)
            return -1

        if idm < 0:
            id_mat = self.__buildMatId()
        else:
            if idm in self.__concreteMaterial.keys():
                log("ERR", f"Material with id = {idm} exists !!!", self.__ll)
                return -1
            id_mat = idm

        mat.setId(id_mat)
        ret_val = self.__md.addLawParaboleRectangle(
            ids=mat.getId(),
            descr=mat.getMatDescr(),
            fcd=-mat.get_alphacc() * mat.get_fck() / mat.get_gammac(),
            ec2=-mat.get_ec2(),
            ecu=-mat.get_ecu(),
        )
        if not ret_val:
            log("ERR", f"Cannot add concrete law with id" f"{id_mat}", self.__ll)
            return -1

        self.__concreteMaterial[id_mat] = mat
        return id_mat

    def assignConcreteLawToCurrentModel(self, idm: int) -> bool:
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0014", "None model current")

        if idm not in self.__concreteMaterial.keys():
            raise Ex(
                "(templateRCGen)-0015",
                f"Concrete material with id *{idm}* doesn't exist.",
            )

        if self.__md.setTrianglesLawInCurrentModel(idm):
            self.__matForConcrete[self.__md.getCurrent()] = idm
            return True

        return False

    def addRebarLaw(
        self,
        mat: ConcreteSteel,
        shape: Literal["LINEAR-RECTANGLE"] = "LINEAR-RECTANGLE",
        idm: int = -1,
    ) -> int:

        if shape != "LINEAR-RECTANGLE":
            log("ERR", "Law shape unknown", self.__ll)
            return -1

        if idm < 0:
            id_mat = self.__buildMatId()
        else:
            if idm in self.__rebarsMaterial.keys():
                log("ERR", f"Material with id = {idm} exists !!!", self.__ll)
                return -1
            id_mat = idm

        mat.setId(id_mat)

        retVal = self.__md.addLawBilinear(
            ids=mat.getId(),
            descr=mat.getMatDescr(),
            fsd=mat.get_fsy() / mat.get_gammas(),
            Es=mat.get_Es(),
            esu=mat.get_esu(),
        )
        if not retVal:
            log("ERR", "Modeler error with addLawBilinear", self.__ll)
            return -1

        self.__rebarsMaterial[id_mat] = mat
        return id_mat

    def assignRebarLawToCurrentModel(self, idm: int) -> bool:
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0013", "None model current")

        if idm not in self.__rebarsMaterial.keys():
            raise Ex(
                "(templateRCGen)-0016",
                f"Rebars material with id *{idm}* doesn't exist.",
            )

        if self.__md.setCirclesLawInCurrentModel(idm):
            self.__matForRebars[self.__md.getCurrent()] = idm
            return True

        return False

    def calcConcreteArea(self) -> float:
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0009", "None model current")
        return self.__md.calcSolidArea()

    def calcRebarArea(self) -> float:
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0010", "None model current")

        return self.__md.calcPointArea()

    def assignForces(self, forces: Dict[int, Forces] = None) -> None:
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0012", "None model current")

        self.__forces[self.__md.getCurrent()] = forces

    def __checkBeforeRun(self):
        if self.__md.getCurrent() == -1:
            raise Ex("(templateRCGen)-0011", "None model current")

        if self.__md.getCurrent() not in self.__matForConcrete.keys():
            raise Ex(
                "(templateRCGen)-0015", "Concrete not assigned in current section !!!"
            )

        if self.__md.getCurrent() not in self.__matForRebars.keys():
            raise Ex(
                "(templateRCGen)-0016",
                "Rebar material not assigned in current section !!!",
            )

    def __run_check_domain_slu(self, res: Results) -> bool:
        res.domainSLU = CheckDomainSLUResults()
        res.domainSLU.logs += [
            log("INF", "... perform DOMAIN_SLU analysis ...", self.__ll)
        ]

        # I have to remove old results
        res.domainSLU = CheckDomainSLUResults()

        if self.__forces is None:
            res.domainSLU.logs += [log("ERR", "Using assignForces !!!", self.__ll)]
            return False

        # Check forces if null or yet assigned
        if self.__md.getCurrent() not in self.__forces.keys():
            res.domainSLU.logs += [
                log("ERR", "Forces in Domain SLU analysis are nulls !!!", self.__ll)
            ]
            return False

        forces = self.__forces[self.__md.getCurrent()]

        if len(forces) == 0:
            res.domainSLU.logs += [
                log("ERR", "Forces with lenght=0 !!! Stop.", self.__ll)
            ]
            return False

        res.domainSLU.logs += [
            log("INF", "Successfully assigned forces for analysis ...", self.__ll)
        ]

        # Check forces if null
        counterNull = 0
        counterSkipped = 0
        filteredForces: Dict[int, Forces] = {}

        for _k, f in forces.items():
            haveToSkip = False

            if f.isNull():
                counterNull += 1
                haveToSkip = False
            if f.limitState is not LimitState.ULTIMATE:
                counterSkipped += 1
                haveToSkip = True

            if not haveToSkip:
                filteredForces[f.id] = f

        res.domainSLU.globalCheck = CheckResults()
        if len(filteredForces) == 0:
            res.domainSLU.logs += [
                log(
                    "WRN",
                    f"All {len(forces)} forces are null or not SLU !!!",
                    self.__ll,
                )
            ]
            res.domainSLU.globalCheck.check = True
            res.domainSLU.globalCheck.safetyFactor = -1

        res.domainSLU.logs += [
            log(
                "INF",
                f"Nb. {counterNull}/{len(forces)} " f"forces are null !!!",
                self.__ll,
            )
        ]
        res.domainSLU.logs += [
            log(
                "INF",
                f"Nb. {counterSkipped}/{len(forces)} " f"forces are not ULTIMATE !!!",
                self.__ll,
            )
        ]

        checkVector: List[bool] = []
        safetyVector: List[float] = []
        loadsIdVector: List[int] = []
        loadsNOOK: List[int] = []
        loadsOK: List[int] = []

        for _k, force in filteredForces.items():
            check = DomainSLUCheck(loadId=force.id)
            checkLogs = DomainSLUCheckLog(
                Mxrd=0.0,
                Myrd=0.0,
                Nrd=0.0,
                loadId=force.id,
                Mxed=force.Mx,
                Myed=force.My,
                Ned=force.Fz,
                check=False,
                Nmin=0.0,
                Nmax=0.0,
            )
            check.interactionDomain.check = True
            check.interactionDomain.safetyFactor = "inf"
            # oldRef = force.ref
            # force.switchToNamedRef('DOMAIN')
            if force.isNull():
                checkLogs.logs += ["Force null"]
            else:
                degreeDivision = self.__options.domainSLU.degreeDivision
                rationDivision = self.__options.domainSLU.rationDivision
                rebuild = self.__options.domainSLU.rebuild
                if self.__md.buildDomain(degreeDivision, rationDivision, rebuild):
                    checkLogs.logs += ["Domain ok"]
                    res.domainSLU.logs += [
                        log(
                            "INF",
                            f"Domain formed successfully with degree {degreeDivision}, "
                            f"ratio {rationDivision}, rebuild {rebuild}",
                            self.__ll,
                        )
                    ]
                    minN = self.__md.domainBounding()[0]
                    maxN = self.__md.domainBounding()[1]
                    roX = abs(
                        self.__md.domainBounding()[3] - self.__md.domainBounding()[2]
                    )
                    roY = abs(
                        self.__md.domainBounding()[5] - self.__md.domainBounding()[4]
                    )

                    assert minN < 0.0
                    assert maxN > 0.0

                    checkLogs.Nmin = minN
                    checkLogs.Nmax = maxN

                    # Compute about safety factor for N
                    if force.Fz < 0.0:
                        safetyN = minN / force.Fz
                        checkLogs.Nrd = minN
                    elif force.Fz > 0.0:
                        safetyN = maxN / force.Fz
                        checkLogs.Nrd = maxN
                    else:
                        safetyN = "inf"
                        checkLogs.Nrd = None

                    if minN < force.Fz < maxN:
                        checkLogs.logs += ["N is contained in bounding"]
                        intersectionsN = self.__md.intersectAtN(force.Fz)
                        checkLogs.domain.pointsCloud2d = intersectionsN.model()
                        # print(f"Intersection plane at N={force.Fz}")
                        # print(f"for Mx={force.Mx} and My= {force.My} and ro=({roX},{roY})")
                        # intersectionsN = self.__md.intersectAtN(force.Fz, 1e-6, 1e-6)
                        if float(force.Mx) == 0.0 and float(force.My) == 0.0:
                            checkLogs.logs += [
                                "Moments Mx and My are nulls. Banal solution"
                            ]
                            check.interactionDomain.safetyFactor = safetyN
                            if check.interactionDomain.safetyFactor == "inf":
                                check.interactionDomain.check = True
                            else:
                                check.interactionDomain.check = (
                                    check.interactionDomain.safetyFactor > 1.0
                                )
                            checkLogs.Mxrd = None
                            checkLogs.Myrd = None
                            checkLogs.check = check.interactionDomain.check
                        else:
                            (
                                contained,
                                pintersect,
                                intfactor0,
                                pindex,
                            ) = intersectionsN.contains(
                                xp=force.Mx, yp=force.My, ro=(roX, roY)
                            )
                            assert intfactor0 >= 0
                            if safetyN == "inf":
                                check.interactionDomain.safetyFactor = intfactor0
                            else:
                                check.interactionDomain.safetyFactor = min(
                                    intfactor0, safetyN
                                )

                            check.interactionDomain.check = (
                                check.interactionDomain.safetyFactor > 1
                            )
                            checkLogs.Mxrd = intfactor0 * force.Mx
                            checkLogs.Myrd = intfactor0 * force.My
                            checkLogs.check = check.interactionDomain.check
                    else:
                        checkLogs.logs += ["N isn't contained in bounding"]

                else:
                    checkLogs.logs += ["Domain error !!!"]
                    res.domainSLU.logs += [log("ERR", "Domain error !!!", self.__ll)]

            res.domainSLU.loadsCheck[force.id] = check
            res.domainSLU.loadsCheckLogs[force.id] = checkLogs

            checkVector += [check.interactionDomain.check]

            if type(check.interactionDomain.safetyFactor) == float:
                safetyVector += [check.interactionDomain.safetyFactor]
                loadsIdVector += [force.id]
                if not check.interactionDomain.safetyFactor > 1:
                    loadsNOOK += [check.loadId]
                else:
                    loadsOK += [check.loadId]
            else:
                loadsOK += [check.loadId]

            # force.switchToRef(oldRef)

        if len(filteredForces) > 0:
            res.domainSLU.globalCheck.check = False not in checkVector
            if len(safetyVector) > 0:
                min_index = min(range(len(safetyVector)), key=lambda i: safetyVector[i])
                res.domainSLU.globalCheck.safetyFactor = safetyVector[min_index]
                res.domainSLU.loadIdCheck = loadsIdVector[min_index]
            # All forces are null then
            else:
                res.domainSLU.globalCheck.safetyFactor = "inf"

        return True

    def __run_check_elastic_sls(self, res: Results) -> bool:
        res.elasticCheck = ElasticSLSCheckResults()
        res.elasticCheck.logs += [
            log("INF", "... perform ELASTIC CHECK analysis ...", self.__ll)
        ]

        # Need run ELASTIC SOLVER before
        if res.elasticSolver is None:
            res.elasticCheck.logs += [
                log("ERR", "Need ELASTIC RUN before !!! Stop.", self.__ll)
            ]
            return False
        if len(res.elasticSolver.elasticResults) == 0:
            res.elasticCheck.logs += [
                log(
                    "ERR",
                    "Need ELASTIC RUN before with almost one" "load !!! Stop.",
                    self.__ll,
                )
            ]
            return False
        else:
            res.elasticCheck.logs += [
                log(
                    "INF",
                    f"Nb.{len(res.elasticSolver.elasticResults)}"
                    f" loads will be checked !!! Stop.",
                    self.__ll,
                )
            ]

        forces_on_section = self.__forces[self.__md.getCurrent()]

        concrete_mat_used = self.__concreteMaterial[
            self.__matForConcrete.get(self.__md.getCurrent())
        ]
        if concrete_mat_used is None:
            res.elasticCheck.logs += [
                log(
                    "ERR",
                    f"Concrete material don't assigned "
                    f"to section {self.__md.getCurrent()} !!! Stop.",
                    self.__ll,
                )
            ]
            return False
        rebar_mat_used = self.__rebarsMaterial[
            self.__matForRebars.get(self.__md.getCurrent())
        ]
        if rebar_mat_used is None:
            res.elasticCheck.logs += [
                log(
                    "ERR",
                    f"Rebars material don't assigned "
                    f"to section {self.__md.getCurrent()} !!! Stop.",
                    self.__ll,
                )
            ]
            return False

        checkVector: List[bool] = []
        safetyVector: List[float] = []
        loadsIdVector: List[int] = []

        for k in res.elasticSolver.elasticResults.keys():
            force = forces_on_section[k]

            # Load need to be CHARACTERISTIC or QUASI_PERMANENT
            ch = force.frequency == Frequency.CHARACTERISTIC
            qp = force.frequency == Frequency.QUASI_PERMANENT
            if ch or qp:
                res.elasticCheck.loadsCheck[k] = ElasticSLSCheck()
                res.elasticCheck.loadsCheckLogs[k] = ElasticSLSCheckLog()
                res.elasticCheck.loadsCheckLogs[k].frequency = force.frequency
                elastic_result = res.elasticSolver.elasticResults[k]
                check = False
                if ch:
                    sigmac_max = -concrete_mat_used.get_sigmac_max_c()
                    sigmas_max = rebar_mat_used.get_sigmas_max_c()
                    ratio_steel = elastic_result.sigmasMax / sigmas_max
                    ratio_concrete = elastic_result.sigmacMin / sigmac_max
                    res.elasticCheck.loadsCheckLogs[k].sigmacMinCH = sigmac_max
                    res.elasticCheck.loadsCheckLogs[k].sigmasMaxCH = sigmas_max
                    res.elasticCheck.loadsCheckLogs[
                        k
                    ].sigmacCH = elastic_result.sigmacMin
                    res.elasticCheck.loadsCheckLogs[
                        k
                    ].sigmasCH = elastic_result.sigmasMax
                    if max(ratio_steel, ratio_concrete) != 0:
                        safetyFactor = 1 / max(ratio_steel, ratio_concrete)
                    else:
                        safetyFactor = "inf"
                    if safetyFactor >= 1 or safetyFactor == "inf":
                        check = True
                else:
                    sigmac_max = -concrete_mat_used.get_sigmac_max_q()
                    res.elasticCheck.loadsCheckLogs[k].sigmacMinQP = sigmac_max
                    ratio_concrete = elastic_result.sigmacMin / sigmac_max
                    res.elasticCheck.loadsCheckLogs[
                        k
                    ].sigmacQP = elastic_result.sigmacMin
                    if ratio_concrete != 0:
                        safetyFactor = 1 / ratio_concrete
                    else:
                        safetyFactor = "inf"
                    if safetyFactor >= 1 or safetyFactor == "inf":
                        check = True

                res.elasticCheck.loadsCheck[k].loadId = force.id
                res.elasticCheck.loadsCheck[k].elasticCheck.safetyFactor = safetyFactor
                res.elasticCheck.loadsCheck[k].elasticCheck.check = check
                checkVector += [check]
                if type(safetyFactor) is float:
                    safetyVector += [safetyFactor]
                    loadsIdVector += [force.id]

            else:
                res.elasticCheck.logs += [
                    log(
                        "INF",
                        f"Load {k} skipped because not "
                        f"CHARACTERISTIC or QUASI_PERMANENT !!! Skipped.",
                        self.__ll,
                    )
                ]

        if len(res.elasticCheck.loadsCheck) == 0:
            res.elasticCheck.logs += [
                log("ERR", "Forces all skipped !!! Stop.", self.__ll)
            ]
            return False

        min_index = min(range(len(safetyVector)), key=lambda i: safetyVector[i])
        res.elasticCheck.globalCheck = CheckResults()
        res.elasticCheck.globalCheck.safetyFactor = safetyVector[min_index]
        res.elasticCheck.loadIdCheck = loadsIdVector[min_index]

        res.elasticCheck.logs += [
            log("INF", "... ELASTIC CHECK end with success.", self.__ll)
        ]
        return True

    def __run_elastic_solver(self, res: Results) -> bool:
        res.elasticSolver = ElasticSolverResults()
        res.elasticSolver.logs += [
            log("INF", "... perform ELASTIC analysis ...", self.__ll)
        ]

        # Forces assigned to current section
        #
        forces = self.__forces[self.__md.getCurrent()]

        if len(forces) == 0:
            res.elasticSolver.logs += [
                log("ERR", "Forces with lenght=0 !!! Stop.", self.__ll)
            ]
            return False

        # Check forces if null
        counterNull = 0
        counterSkipped = 0
        filteredForces: Dict[int, Forces] = {}

        for _k, f in forces.items():
            haveToSkip = False

            if f.isNull():
                counterNull += 1
                haveToSkip = True
            if f.limitState is not LimitState.SERVICEABILITY:
                counterSkipped += 1
                haveToSkip = True

            if not haveToSkip:
                filteredForces[f.id] = f

        res.elasticSolver.logs += [
            log(
                "INF",
                f"Nb. {counterNull}/{len(forces)} " f"forces are null !!!",
                self.__ll,
            )
        ]
        res.elasticSolver.logs += [
            log(
                "INF",
                f"Nb. {counterSkipped}/{len(forces)} "
                f"forces are not SERVICEABILITY !!!",
                self.__ll,
            )
        ]

        for _k, force in filteredForces.items():
            # oldRef = force.ref
            # force.switchToNamedRef('ELASTIC')
            if not self.__md.elSolve(force=force, uncracked=False):
                res.domainSLU.logs += [
                    log(
                        "WRN",
                        f"... ELASTIC solver error with force id = {force.id}!!! Stop.",
                        self.__ll,
                    )
                ]
                return False
            resElastic = ElasticSolverResult()
            # force.switchToRef(oldRef)
            resElastic.Ned = force.Fz
            resElastic.Myed = force.My
            resElastic.Mxed = force.Mx
            (
                resElastic.sigmacMin,
                resElastic.sigmacMax,
            ) = self.__md.elExtremeStressConcrete()
            (
                resElastic.sigmasMin,
                resElastic.sigmasMax,
            ) = self.__md.elExtremeStressSteel()
            resElastic.state = self.__md.elSectionState()
            resElastic.tensionPlane = self.__md.elTensionPlane()

            # Results for solid nodes
            #
            solidNodes = self.__md.getSolidNodes()
            for v in solidNodes.keys():
                resElastic.sigmaci[v] = self.__md.elStressConcreteNodeId(v)

            # Results for rebars
            #
            rebars = self.__md.getCircles()
            for r in rebars.keys():
                resElastic.sigmasi[r] = self.__md.elStressSteelCircleId(r)

            res.elasticSolver.elasticResults[force.id] = resElastic

        res.elasticSolver.logs += [
            log("INF", "... ELASTIC analysis terminated successfully.", self.__ll)
        ]
        return True

    def __run_bounding_slu(self, res: Results) -> bool:
        # I have to remove old results
        res.boundingSLU = BoundingSLUResults()

        res.boundingSLU.logs += [
            log("INF", "... perform BOUNDING_SLU analysis ...", self.__ll)
        ]
        degreeDivision = self.__options.boundingSLU.degreeDivision
        rationDivision = self.__options.boundingSLU.rationDivision

        retVal = self.__md.buildDomain(
            degreeDivision, rationDivision, self.__options.boundingSLU.rebuild
        )
        if not retVal:
            res.boundingSLU.logs += [
                log("ERR", "... domain built with error ... return", self.__ll)
            ]
            return False

        res.boundingSLU.logs += [
            log("INF", "... domain built successfully ...", self.__ll)
        ]
        bbox = self.__md.domainBounding()

        res.boundingSLU.minForces = Forces(Fz=bbox[0], Mx=bbox[2], My=bbox[4])
        res.boundingSLU.maxForces = Forces(Fz=bbox[1], Mx=bbox[3], My=bbox[5])
        return True

    def run(self, opt: Union[Enum, None] = None, **kwargs) -> bool:

        self.__checkBeforeRun()

        res = self.__results.sectionResults[self.__md.getCurrent()]
        super()._setModelOutput(self.__results)

        res.logs += [
            log(
                "INF",
                f"Start analysis ... for section with id *{self.__md.getCurrent()}*",
                self.__ll,
            )
        ]

        com = Command(type=CommandType.RUN)
        if opt == Analysis.CHECK_DOMAIN_SLU:
            if not self.__run_check_domain_slu(res):
                return False
            arg = CommandArg(name="opt", value=Analysis.CHECK_DOMAIN_SLU)
            com.args.append(arg)

        if opt == Analysis.BOUNDING_SLU:
            if not self.__run_bounding_slu(res):
                return False
            arg = CommandArg(name="opt", value=Analysis.BOUNDING_SLU)
            com.args.append(arg)

        if opt == Analysis.CHECK_ELASTIC:
            if not self.__run_check_elastic_sls(res):
                return False
            arg = CommandArg(name="opt", value=Analysis.CHECK_ELASTIC)
            com.args.append(arg)

        if opt == Analysis.ELASTIC_SOLVER:
            if not self.__run_elastic_solver(res):
                return False
            arg = CommandArg(name="opt", value=Analysis.ELASTIC_SOLVER)
            com.args.append(arg)

        self.__journalOfCommands.append(com)

        res.logs += [log("INF", "End analysis.", self.__ll)]
        return True

    def buildReport(self, opt: Union[Enum, None] = None, **kwargs) -> bool:
        pass

class ReportElastic(FragmentsBuilder):
    def __init__(self, oDataSolver: ElasticSolverResults, oDataChecker: ElasticSLSCheckResults, jobPath: Path):
        super().__init__()
        self.__oDataSolver = oDataSolver
        self.__oDataChecker = oDataChecker
        self._setFragmentOptions({"job_path": jobPath})

    def buildFragment(self) -> Fragment:
        f = Fragment(getTemplatesPath())
        place_holder = dict()
        place_holder["check_SLE_MN"] = []
        artifacts = []
        for key_load in self.__oDataChecker.loadsCheckLogs.keys():
            check_logs = self.__oDataChecker.loadsCheckLogs[key_load]
            solver_res = self.__oDataSolver.elasticResults[key_load]
            check = self.__oDataChecker.loadsCheck[key_load]
            row_check = dict()
            row_check["id"] = key_load
            row_check["Ned"] = f"{solver_res.Ned / 1e3:.1f}"
            row_check["Mxed"] = f"{solver_res.Mxed / 1e6:.1f}"
            row_check["Myed"] = f"{solver_res.Myed / 1e6:.1f}"
            row_check["sigmas"] = f"{solver_res.sigmasMax:.1f}"
            row_check["sigmac"] = f"{solver_res.sigmacMin:.1f}"
            if check_logs.frequency == Frequency.CHARACTERISTIC:
                row_check["sigmaxs"] = f"{check_logs.sigmasMaxCH:.1f}"
                row_check["sigmaxc"] = f"{check_logs.sigmacMinCH:.1f}"
            elif check_logs.frequency == Frequency.QUASI_PERMANENT:
                row_check["sigmaxs"] = ""
                row_check["sigmaxc"] = f"{check_logs.sigmacMinQP:.1f}"
            else:
                row_check["sigmaxs"] = ""
                row_check["sigmaxc"] = ""
            if check.elasticCheck.check:
                row_check["check"] = "OK"
            else:
                row_check["check"] = "NOOK"
            row_check["FS"] = f"{check.elasticCheck.safetyFactor:.2f}"
            place_holder["check_SLE_MN"].append(row_check)

            for artifact in solver_res.artifacts:
                if artifact.tp == ArtifactType.ELASTIC_STRESS:
                    geometryFilePath_encoded_for_latex = str(str(self.getFragmentOptions()["job_path"] / artifact.file_name())).replace('\\', '/')
                    artifacts.append(
                        {
                            "domainUrl": geometryFilePath_encoded_for_latex,
                            "idLoad": key_load,
                            "newLine": False
                        }
                    )

        # TABLE for figures
        #
        maxCols = 2
        maxRows = 3
        max_elem_for_figure = maxCols * maxRows
        nb_elem = len(artifacts)
        nb_figs = math.ceil(nb_elem / max_elem_for_figure)

        figures_matrix = []
        elem = []
        fig_index = 0

        if nb_elem == 1:
            figure_width = 0.90
        else:
            figure_width = 0.41

        for a in artifacts:
            elem.append(a)
            if math.ceil(len(elem) / maxCols) == math.floor(len(elem) / maxCols):
                a["newLine"] = True
            if len(elem) == max_elem_for_figure:
                fig_index += 1
                figures_matrix.append({"domainUrls": elem, "figIndex": fig_index})
                elem = []
        if 0 < len(elem) < max_elem_for_figure:
            fig_index += 1
            figures_matrix.append({"domainUrls": elem, "figIndex": fig_index})

        place_holder["figures"] = figures_matrix
        place_holder["nbFigs"] = nb_figs
        place_holder["figuresWidth"] = figure_width

        f.add_template("template-ita-rc-gen-sle-nm.tex", place_holder)
        return f

class ReportBuilder(FragmentsBuilder):
    def __init__(self, iData: RCGenSectionsInput, oData: RCGenSectionsOutput, jobPath: Path):
        super().__init__()
        self.__iData = iData
        self.__oData = oData
        self.__jobPath = jobPath

    def buildFragment(self) -> Fragment:
        f = Fragment(getTemplatesPath())

        for key_section, section in self.__iData.sections.items():
            title_str = f"{key_section}"
            f.add(line=r"\section{Sezione n." + title_str + r"}")
            oData = self.__oData.sectionResults[key_section]
            #
            # Build GEOMETRY
            #
            for a in oData.artifacts:
                if a.tp == ArtifactType.SECTION_GEOMETRY:
                    section.setFragmentOptions({
                        "geometry_file_path": self.__jobPath / a.file_name()
                    })
            f.add(lines=section.buildFragment().frags())
            f.add_line(r"\subsection{Caratteristiche meccaniche dei materiali}")
            #
            # Build MATERIALS paragraph
            #
            # concrete
            #
            concrete_key = section.materials.concrete
            concrete_model = self.__iData.matCatalogue.concrete[concrete_key]
            concrete_fb = ConcreteFB(getTemplatesPath(), concrete_model.toMaterial())
            concrete_fb.setFragmentOptions(
                {
                    "section_title": "Calcestruzzo",
                    "section_level": EnumFBSection.SEC_SUBSUBSECTION,
                }
            )
            f.add(lines=concrete_fb.buildFragment().frags())
            #
            # steel
            #
            steel_key = section.materials.rebars
            steel_model = self.__iData.matCatalogue.steel[steel_key]
            steel_fb = SteelConcreteFB(getTemplatesPath(), steel_model.toMaterial())
            steel_fb.setFragmentOptions(
                {
                    "section_title": "Acciaio in barre",
                    "section_level": EnumFBSection.SEC_SUBSUBSECTION,
                }
            )
            f.add(lines=steel_fb.buildFragment().frags())
            #
            # Build FORCES paragraph
            #
            forces = []
            for v in section.loads.items():
                forces.append(v[1])
            forces_fb = ForcesOnSectionListFB(getTemplatesPath(), forces)
            forces_fb.setFragmentOptions(
                {
                    "section_title": "Carichi e combinazioni",
                    "section_level": EnumFBSection.SEC_SUBSECTION,
                }
            )
            f.add(lines=forces_fb.buildFragment().frags())
            #
            # Build SLU DOMAIN paragraph
            #
            if self.__oData.sectionResults[key_section].domainSLU is not None:
                self.__oData.sectionResults[key_section].domainSLU.setFragmentOptions({"job_path": self.__jobPath})
                f.add_line(r"\subsection{Verifiche agli SLU}")
                f.add(lines=self.__oData.sectionResults[key_section].domainSLU.buildFragment().frags())
                f.add_line(r"\newpage")

            #
            # Build SLE NM check
            #
            solver = self.__oData.sectionResults[key_section].elasticSolver
            checker = self.__oData.sectionResults[key_section].elasticCheck
            if solver is not None and checker is not None:
                elasticBuilder = ReportElastic(solver, checker, jobPath=self.__jobPath)
                f.add_line(r"\subsection{Verifiche agli SLE}")
                f.add(lines=elasticBuilder.buildFragment().frags())
                f.add_line(r"\newpage")


        #
        # Build CODE Paragraph
        #
        codesFragment = CodesFB(getTemplatesPath())
        for k in self.__iData.matCatalogue.concrete:
            mat_str = self.__iData.matCatalogue.concrete[k].code.value
            codesFragment.appendUniqueCode(code_str=mat_str)

        for k in self.__iData.matCatalogue.steel:
            mat_str = self.__iData.matCatalogue.steel[k].code.value
            codesFragment.appendUniqueCode(code_str=mat_str)

        f.add(lines=codesFragment.buildFragment().frags())
        return f
