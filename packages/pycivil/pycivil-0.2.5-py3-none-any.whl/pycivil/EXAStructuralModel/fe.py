import math
import os
from enum import Enum
from typing import List, Literal, Dict, Tuple, Set

import gmsh
import numpy as np
from gmsh import model as gmsh_model
from jinja2 import Environment, FileSystemLoader


from pycivil.EXAUtils import logging as log, EXAExceptions as Ex

from pycivil.settings import ServerSettings

thisPath = os.path.dirname(os.path.abspath(__file__))
sp = ServerSettings().midas_templates_path

file_loader = FileSystemLoader(searchpath=sp)
env = Environment(loader=file_loader)
template = env.get_template("template-box.mgt")

# -----------------------------------------------------------------------------
#
#  Gmsh Python extended tutorial 1
#
#  Geometry and mesh data
#
# -----------------------------------------------------------------------------

# The Python API allows to do much more than what can be done in .geo files. These
# additional features are introduced gradually in the extended tutorials,
# starting with 'x1.py'.

# In this first extended tutorial, we start by using the API to access basic
# geometrical and mesh data.


class Dim(Enum):
    DIM_0D = 0
    DIM_1D = 1
    DIM_2D = 2
    DIM_3D = 3


class Elem(Enum):
    ELEM_TRIA = 3
    ELEM_QUAD = 4


class FEModel:
    configData = {
        "LoadCaseType": [
            {"id": "U", "description": "User Defined Load"},
            {"id": "D", "description": "Dead Load"},
            {"id": "L", "description": "Live Load"},
            {"id": "R", "description": "Roof Live Load"},
            {"id": "W", "description": "Wind Load on Structure"},
            {"id": "E", "description": "Earthquake"},
            {"id": "T", "description": "Temperature"},
            {"id": "S", "description": "Snow Load"},
            {"id": "R", "description": "Rain Load"},
            {"id": "IL", "description": "Live Load Impact"},
            {"id": "EP", "description": "Earth Pressure"},
            {"id": "B", "description": "Buoyancy"},
            {"id": "WP", "description": "Ground Water Pressure"},
            {"id": "FP", "description": "Fluid Pressure"},
            {"id": "IP", "description": "Ice Pressure"},
            {"id": "WL", "description": "Wind Load on Live Load"},
            {"id": "BK", "description": "Longitudinal Force from Live Load"},
            {"id": "CF", "description": "Centrifugal Force"},
            {"id": "RS", "description": "Rib Shortening"},
            {"id": "SH", "description": "Shrinkage"},
            {"id": "CR", "description": "Creep"},
            {"id": "PS", "description": "Pre-stressing force"},
            {"id": "ER", "description": "Erection Load"},
            {"id": "CO", "description": "Collision Load"},
            {"id": "CS", "description": "Construction Stage Load"},
            {"id": "BL", "description": "Braking Load"},
            {"id": "STL", "description": "Settlement"},
            {"id": "WPL", "description": "Wave Pressure"},
            {"id": "CL", "description": "Crowd Load"},
            {"id": "TG", "description": "Temperature Gradient"},
            {"id": "SW", "description": "Self Weight"}
        ]
    }
    def __init__(self, descr="", modelName="default"):

        # GMSH init
        gmsh.initialize()

        # Using OCC as BREP for geometry
        self.__cad = gmsh_model.occ

        # Adding model and make current
        gmsh_model.add(modelName)
        gmsh_model.setCurrent(modelName)

        self.__models = [modelName]

        print(gmsh_model.list())

        self.__description = descr
        self.__loadCase = {}
        self.__loads = {}
        self.__loadCombinations: Dict[str, List[float]] = {}
        self.__nodeSupports = {}
        self.__nodeSprings = {}

        # [Load Case][Node Tag][Tp]
        self.__nodeTemperatures: Dict[str, Dict[int, Dict[str, float]]] = {}

        # [Load Case][Frame Tag][Tp]
        self.__frameTemperatures: Dict[str, Dict[int, Dict[str, Tuple[float, float]]]] = {}

        # Values that don't depend on geometry or mesh
        # [Load Case] = value
        self.__initialTemperatures: Dict[str, float] = {}
        self.__inertialAcceleration: Dict[str, Tuple[float, float, float]] = {}

        # Springs evenly distribuited in local direction
        #
        # Dict[id_frame, Tuple[LCDIR1, LCDIR2, ONLYCOMPRESSION]]
        self.__framesSprings: Dict[int, Tuple[float, float, bool]] = {}

        self.__sectionShapes = {
            1: {"type": "RECTANGULAR", "dimensions": [1.0, 0.3], "name": "default"}
        }
        self.__framesShapes = {}

        self.__materialLibrary = {}
        self.__framesMaterial = {}

        self.__logLevel: Literal[0,1,2,3] = 3

        # [group tree name, physical]
        self.__groupTree: Dict[str,str] = {}

        # Link between Frames and phisical Names
        self.__framesPhysicalNames: Dict[int, List[str]] = {}

    def __assignShapesToFrames(self):
        pass

    def __log(self, tp, msg):
        log.log(tp, msg, self.__logLevel)

    @staticmethod
    def show():
        gmsh.fltk.run()

    def addMaterialToLibrary(
            self,
            idMaterial: int,
            modulus: float, # Mpa
            poisson: float, # ...
            name: str,
            density: float = 0.0, # kg/mc
            thermal_expansion: float= 0.0, # 1/C
            conductivity: float = 0.0, # KJ/s/m/C
            specific_heat: float = 0.0, # KJ/kg/C
    ):
        self.__materialLibrary[idMaterial] = {
            "name": name,
            "modulus": modulus,
            "poisson": poisson,
            "density": density,
            "thermal_expansion": thermal_expansion,
            "conductivity": conductivity,
            "specific_heat": specific_heat
        }

    def addSectionShape(self, idShape, name, tp, dim=None):
        if dim is None:
            dim = []

        if idShape in self.__sectionShapes.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0007", "idShape for shape must be unique", idShape
            )

        if not isinstance(idShape, int):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "idShape must be a int", type(idShape)
            )

        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "name must be a str", type(name)
            )

        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "tp must be a str", type(tp)
            )

        if not all(isinstance(n, float) for n in dim):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0009", "dim must be float list", type(dim)
            )
        else:
            np.array(dim, dtype=np.float32)

        tps = ["RECTANGULAR"]

        if tp not in tps:
            raise Ex.EXAExceptions("(EXAStructuralModel)-0004", "tp unknown", type(tp))

        if tp == "RECTANGULAR":

            if len(dim) != 2:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0004",
                    "For *RECTANGULAR* dim must have a two dim array",
                    len(dim),
                )

        self.__sectionShapes[idShape] = {
            "type": "RECTANGULAR",
            "dimensions": dim,
            "name": name,
        }

    def sectionShapes(self):
        return self.__sectionShapes

    def sectionMaterials(self):
        return self.__materialLibrary

    def assignFrameSectionShape(self, tagFrame, idShape):
        if not (isinstance(tagFrame, int) or isinstance(tagFrame, np.uint64)):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "tagFrame must be a int", type(tagFrame)
            )

        if not isinstance(idShape, int):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "idShape must be a int", type(idShape)
            )

        if idShape not in self.__sectionShapes.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "idShape unknown in sectionShapes table",
                idShape,
            )

        self.__framesShapes[tagFrame] = idShape

    def assignFrameMaterial(self, tagFrame, idMaterial):
        if not (isinstance(tagFrame, int) or isinstance(tagFrame, np.uint64)):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "tagFrame must be a int", type(tagFrame)
            )

        if not isinstance(idMaterial, int):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "idMaterial must be a int", type(idMaterial)
            )

        if idMaterial not in self.__materialLibrary.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "idMaterial unknown in materialLibrary table",
                idMaterial,
            )

        self.__framesMaterial[tagFrame] = idMaterial

    # llp:
    # assignFrameWinklerSupport assign a special type of support evenly distribuited to frame.
    # The main difference with addMultiframeSprings is that in last function subgrade modulus
    # will be transformed in nodal springs
    def assignFrameWinklerSupport(self, tagFrame: int, winkler_supports: Tuple[float, float, bool]):
        self.__framesSprings[tagFrame] = winkler_supports

    def getNodeTemperatures(self):
        return self.__nodeTemperatures

    def getFrameTemperatures(self):
        return self.__frameTemperatures

    def getInitialTemperatures(self):
        return self.__initialTemperatures

    def getInertialAcceleration(self):
        return self.__inertialAcceleration

    def setInertialAcceleration(self, loadCase: str, acc: Tuple[float, float, float]):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "loadCase arg must be a string", type(loadCase)
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0019", "loadCase case unknown", loadCase
            )

        if not isinstance(acc, tuple):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "acc must be float tuple", type(acc)
            )

        if len(acc) != 3:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "acc must have len = 3", len(acc)
            )
        self.__inertialAcceleration[loadCase] = acc

    def setInitialTemperature(self, loadCase: str, temp: float):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "First arg must be a string", type(loadCase)
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0019", "Load case unknown", loadCase
            )

        if not isinstance(temp, float):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "temp must be float list", type(temp)
            )

        self.__initialTemperatures[loadCase] = temp

    def assignNodeTemperature(
            self,
            loadCase: str,
            tagNode: int,
            temp: float,
            tpTemp: Literal['fixed', 'reference', 'initial'] = 'fixed',
    ):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "First arg must be a string", type(loadCase)
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0019", "Load case unknown", loadCase
            )

        if tagNode not in self.nodesTags():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0020", "Nodes tag unknown", tagNode
            )

        if not isinstance(temp, float):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "temp must be float list", type(temp)
            )

        if not isinstance(tpTemp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "tpTemp must be str", type(tpTemp)
            )

        if loadCase not in self.__nodeTemperatures:
            self.__nodeTemperatures[loadCase] = {}

        if tagNode not in self.__nodeTemperatures[loadCase]:
            self.__nodeTemperatures[loadCase][tagNode] = {}

        self.__nodeTemperatures[loadCase][tagNode][tpTemp] = temp

    def assignFrameTemperature(
            self,
            loadCase: str,
            tagFrame: int,
            temp: Tuple[float, float],
            tpTemp: Literal['gradient'] = 'gradient',
    ):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "First arg must be a string", type(loadCase)
            )

        if loadCase not in self.__loadCase:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0019", "loadCase unknown", loadCase
            )

        if tagFrame not in self.framesTags():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0013", "tagFrame unknown", tagFrame
            )

        if not isinstance(tpTemp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0014", "tpTemp arg must be a string", type(tpTemp)
            )

        if not  tpTemp in ['gradient']:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0014", f"tpTemp arg not in {['gradient']}", type(tpTemp)
            )

        if not isinstance(temp, tuple):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0014", "temp arg must be a tuple", type(temp)
            )

        if len(temp) != 2:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0014", "temp arg must have len=2", len(temp)
            )

        if loadCase not in self.__frameTemperatures:
            self.__frameTemperatures[loadCase] = {}

        if tagFrame not in self.__frameTemperatures[loadCase]:
            self.__frameTemperatures[loadCase][tagFrame] = {}

        self.__frameTemperatures[loadCase][tagFrame][tpTemp] = temp


    def assignMultiFrameWinklerSupport(self, winkler_supports: Tuple[float, float, bool], tagsMacro=None, tagsFrames=None):
        if tagsMacro is None:
            tagsMacro = []
        if tagsFrames is None:
            tagsFrames = []

        if len(tagsMacro) == 0 and len(tagsFrames) == 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0 and len(tagsFrames) != 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be not null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0:
            framesTags = self.getFramesFromMacroTags()
            for tag in tagsMacro:
                for _i, t in enumerate(framesTags[tag]):
                    self.assignFrameWinklerSupport(t, winkler_supports)
        else:
            for _i, t in enumerate(tagsFrames):
                self.assignFrameWinklerSupport(t, winkler_supports)

    def frameSectionShape(self):
        return self.__framesShapes

    def frameMaterial(self):
        return self.__framesMaterial

    def assignMultiFrameSectionShape(self, idShape, tagsMacro=None, tagsFrames=None):
        if tagsMacro is None:
            tagsMacro = []
        if tagsFrames is None:
            tagsFrames = []

        if len(tagsMacro) == 0 and len(tagsFrames) == 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0 and len(tagsFrames) != 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be not null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0:
            framesTags = self.getFramesFromMacroTags()
            for tag in tagsMacro:
                for _i, t in enumerate(framesTags[tag]):
                    self.assignFrameSectionShape(t, idShape)
        else:
            for _i, t in enumerate(tagsFrames):
                self.assignFrameSectionShape(t, idShape)


    def assignMultiFrameMaterial(self, idMaterial, tagsMacro=None, tagsFrames=None):
        if tagsMacro is None:
            tagsMacro = []
        if tagsFrames is None:
            tagsFrames = []

        if len(tagsMacro) == 0 and len(tagsFrames) == 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0 and len(tagsFrames) != 0:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004",
                "tagsMacro or tagsFrames must be not null",
                len(tagsMacro),
            )

        if len(tagsMacro) != 0:
            framesTags = self.getFramesFromMacroTags()
            for tag in tagsMacro:
                for _i, t in enumerate(framesTags[tag]):
                    self.assignFrameMaterial(t, idMaterial)
        else:
            for _i, t in enumerate(tagsFrames):
                self.assignFrameMaterial(t, idMaterial)


    @staticmethod
    def clear():
        gmsh.clear()
        gmsh.finalize()

    @staticmethod
    def nodesTags():
        nt = []
        entities = gmsh_model.getEntities()
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)
            nt += list(nodeTags)
        return nt


    @staticmethod
    def getFramesFromMacroTags(macroTags: List[int] | None=None) -> Dict[int, List[int]] | List[int]:
        """
        Retrive a list of mesh elements tags starting from macro element tags

        Args:
            macroTags ():

        Returns:
            If macroTags are given return a Dict with keys that are macroTags and values are list of mesh tags. In
            macroTags are None return a list of all mesh tags
        """
        if macroTags is None:
            macroTags = []

        ft = {}
        entities = gmsh_model.getEntities(1)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            ft[tag] = list(elemTags[0])
        if len(macroTags) == 0:
            return ft
        else:
            tags = []
            for i in macroTags:
                tags += ft[i]
            return tags


    def framesSupports(self):
        return self.__framesSprings

    @staticmethod
    def framesConnectivity():
        """
        Return a tag frame dictionary with key = frame tag and list of 2d tuple with node tags

        Returns:

        """
        elementTypes, elementTags, nodeTags = gmsh_model.mesh.getElements(1)
        connectivity = {}
        for i, tag in enumerate(elementTags[0]):
            connectivity[tag] = (nodeTags[0][i*2], nodeTags[0][i*2+1])
        return connectivity

    @staticmethod
    def nodeCoords(nodeTags: int):
        coord, _, _, _ = gmsh_model.mesh.getNode(nodeTags)
        return coord

    @staticmethod
    def framesTags():
        ft = []
        entities = gmsh_model.getEntities(1)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            ft += list(elemTags[0])
        return ft

    @staticmethod
    def getFrameNodesFromMacro(macroTags: List[List[int]] | List[int] | int | None = None, unique: bool = False) -> (
            Dict[int, List[Tuple[int, int]]] | List[Tuple[int, int]] | Set[int]):
        """
        Get nodes related to macro-elements

        Args:
            unique (): if True and MacroTags is given get a set o unique nodes tags. Default is False
            macroTags (): if macroTags is None get a dictionary with {macroTag_i: [node1_el_1, node2_el_1], ... ,
                [node1_el_n, node2_el_n]}. If macroTags is a list of macro elements get a list of nodes as
                [node1_el_1, node2_el_1], ... , [node1_el_n, node2_el_n]

        Returns:
            ():
        """
        if macroTags is None:
            macroTags = []
        else:
            if isinstance(macroTags, list):
                if len(macroTags) == 0:
                    return []
                else:
                    if isinstance(macroTags[0], list):
                        u_lst = []
                        for m in macroTags:
                            u_lst.extend(m)
                        macroTags = u_lst
            else:
                macroTags = [macroTags]

        ft = {}
        entities = gmsh_model.getEntities(1)
        unique_tags = set()
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            nt = []
            for a in elemNodeTags[0].reshape(round(len(elemNodeTags[0]) / 2), 2):
                nt += [list(a)]
            ft[tag] = nt

        if len(macroTags) == 0:
            return ft
        else:
            tags = []
            for i in macroTags:
                tags += ft[i]

            if unique:
                for n in tags:
                    unique_tags.add(n[0])
                    unique_tags.add(n[1])
                return list(unique_tags)

            return tags

    @staticmethod
    def framesNodeTags():
        ft = []
        entities = gmsh_model.getEntities(1)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            # Get the mesh nodes for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            nt = []
            for a in elemNodeTags[0].reshape(round(len(elemNodeTags[0]) / 2), 2):
                nt += [list(a)]
            ft += nt

        return ft

    @staticmethod
    def nodesCoords():
        nc = []
        entities = gmsh_model.getEntities()
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]

            # Get the mesh nodes for the entity (dim, tag):
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)
            nc += nodeCoords.reshape(round(len(nodeCoords) / 3), 3).tolist()
        return nc


    @staticmethod
    def nodesGroups():
        ng = {}
        entities = gmsh_model.getEntities(0)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            ng[tag] = list(gmsh_model.getPhysicalGroupsForEntity(dim, tag))
        return ng


    @staticmethod
    def framesGroups():
        fg = {}
        entities = gmsh_model.getEntities(1)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]
            fg[tag] = list(gmsh_model.getPhysicalGroupsForEntity(dim, tag))
        return fg


    @staticmethod
    def printNodes():
        print("** start Nodes **")
        entities = gmsh_model.getEntities()
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]

            # Get the mesh nodes for the entity (dim, tag):
            nodeTags, nodeCoords, nodeParams = gmsh.model.mesh.getNodes(dim, tag)
            print("nodeTags", nodeTags)
            print("nodeCoords", nodeCoords)
            print("phisicalGroup", gmsh_model.getPhysicalGroupsForEntity(dim, tag))
        print("** end Nodes **")


    @staticmethod
    def printFrames():
        print("** start Frames **")
        entities = gmsh_model.getEntities(1)
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]

            # Get the mesh elements for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            print("elemTypes", elemTypes)
            print("elemTags", elemTags)
            print("elemNodeTags", elemNodeTags)
            print("phisicalGroup", gmsh_model.getPhysicalGroupsForEntity(dim, tag))
        print("** end Frames **")


    @staticmethod
    def printElements():
        entities = gmsh_model.getEntities()
        for e in entities:
            # Dimension and tag of the entity:
            dim = e[0]
            tag = e[1]

            # Get the mesh elements for the entity (dim, tag):
            elemTypes, elemTags, elemNodeTags = gmsh.model.mesh.getElements(dim, tag)
            print("elemTypes", elemTypes)
            print("elemTags", elemTags)
            print("elemNodeTags", elemNodeTags)
            print("phisicalGroup", gmsh_model.getPhysicalGroupsForEntity(dim, tag))

    # llp: load combination list is related to load case. Order is the same. Starting from Python 3.6
    #      dictionaries hold ordee also. Then self.__loads even dict is ordered

    def addLoadCombination(self, keyCombination: str, combination: List[float]):
        self.__loadCombinations[keyCombination] = combination

    def getLoadCombinations(self):
        return self.__loadCombinations

    def addLoadCase(self, idCase, tp="U", descr=""):
        if not isinstance(idCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0002", "First arg must be a string", idCase
            )
        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0003", "Second arg must be a string", tp
            )
        else:
            find = False
            for v in self.configData["LoadCaseType"]:
                if v["id"] == tp:
                    find = True
                    print(
                        "Type *{}* of load case generic *{}*: {} ---> {}".format(
                            idCase, v["id"], v["description"], descr
                        )
                    )
                    break
            if not find:
                raise Ex.EXAExceptions("(EXAStructuralModel)-0005", "Type unknown", tp)

        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0004", "Third arg must be a string", descr
            )

        if idCase in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0006", "Load case must be unique", idCase
            )

        self.__loadCase[idCase] = [tp, descr]

    def getLoadCases(self):
        return self.__loadCase

    def getLoads(self):
        return self.__loads

    def addSelfWeight(self, loadCase, GCS):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0007", "First arg must be a string", loadCase
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0008", "Load case unknown", loadCase
            )

        if not all(isinstance(n, float) for n in GCS):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0009", "GCS must be float list", GCS
            )

        if len(GCS) != 3:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0010", "GCS must have len 3", len(GCS)
            )

        if loadCase not in self.__loads:
            self.__loads[loadCase] = {}

        self.__loads[loadCase]["selfWeight"] = GCS

    def addMultiFrameWinklerSpring(self, tagsMacro, tp, dirSprings, subgradeModulus, Bref):
        # subgradeModulus: modulo di sottofondo alla Winkler
        # Bref: largezza di riferimento per il calcolo della pressione

        if not isinstance(tagsMacro, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0011", "tagsMacro must be a list", type(tagsMacro)
            )

        nodesTags = self.nodesTags()
        nodesCoords = self.nodesCoords()
        framesTags = self.getFramesFromMacroTags()
        frameNodes = self.getFrameNodesFromMacro()

        for tag in tagsMacro:
            # TODO: move this in separate function for subFrames (meshed frames) and add tagsFrames
            #       in function args with two cases
            for i, _t in enumerate(framesTags[tag]):
                n1 = frameNodes[tag][i][0]
                n2 = frameNodes[tag][i][1]
                n1_coords = nodesCoords[nodesTags.index(n1)]
                n2_coords = nodesCoords[nodesTags.index(n2)]

                if "DX" in dirSprings:
                    idxDir1 = 1
                    idxDir2 = 2
                elif "DY" in dirSprings:
                    idxDir1 = 0
                    idxDir2 = 2
                else: # "DZ" in dir:
                    idxDir1 = 0
                    idxDir2 = 0

                tributaryLength = math.sqrt(
                    pow(n2_coords[idxDir1] - n1_coords[idxDir1], 2)
                    + pow(n2_coords[idxDir2] - n1_coords[idxDir2], 2)
                )

                stiffness = tributaryLength * subgradeModulus * Bref

                self.addNodeSpring(n1, tp, dirSprings, stiffness, add=True)
                self.addNodeSpring(n2, tp, dirSprings, stiffness, add=True)

    def addMultiFrameLoadHydro(
            self,
            loadCase: str,
            tagsMacro: List[int],
            dirLoad: Literal['GCX', 'GCY', 'GCZ'],
            gamma: float,
            K: float,
            H0: float,
            p0: float,
            Bref: float,
            local: bool=False,
            coordVariation: Literal['X', 'Y', 'Z'] = 'Z',
            oneSignPositive: bool | None = None,
            constValue: bool = False
    ):
        """
        Add a linear load on macro-element

        Args:
            loadCase (): load case as str
            tagsMacro (): macro-element tag
            dirLoad (): load direction
            gamma (): peso del terreno specifico
            K (): coefficiente di spinta del terreno
            H0 (): distanza dallo zero della copertura del terreno
            p0 (): pressione di partenza ovvero il sovraccarico
            Bref (): largezza di riferimento per il calcolo della pressione
            local (): reference system for pressure direction
            coordVariation (): coordinate in global reference that for variation
            oneSignPositive (): If None function considers positive and negative values, If True function considers
                only positive values and negative values if it is False
        """
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0011",
                "First arg must be a string",
                type(loadCase),
            )

        if not isinstance(tagsMacro, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0011", "tagsMacro must be a list", type(tagsMacro)
            )

        if dirLoad not in ("GCX", "GCY", "GCZ"):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022",
                "Third arg *dir* must be GCX, GCY, GCZ",
                dirLoad,
            )

        nodesTags = self.nodesTags()
        nodesCoords = self.nodesCoords()
        framesTags = self.getFramesFromMacroTags()
        frameNodes = self.getFrameNodesFromMacro()

        if coordVariation == 'X':
            coords_idx = 0
        elif coordVariation == 'Y':
            coords_idx = 1
        else: # coordVariation == 'Z'
            coords_idx = 2

        for tag in tagsMacro:
            # TODO: move this in separate function for subFrames (meshed frames) and add tagsFrames
            #       in function args with two cases
            for i, t in enumerate(framesTags[tag]):
                n1 = frameNodes[tag][i][0]
                n2 = frameNodes[tag][i][1]
                n1_coords = nodesCoords[nodesTags.index(n1)]
                n2_coords = nodesCoords[nodesTags.index(n2)]
                press_1 = ((H0 - n1_coords[coords_idx]) * gamma * K + p0) * Bref
                press_2 = ((H0 - n2_coords[coords_idx]) * gamma * K + p0) * Bref
                rel_dist_from_I_node_I = 0.0
                rel_dist_from_I_node_J = 1.0
                if oneSignPositive is not None and press_1 != 0.0 and press_2 != 0.0 and not constValue:
                    zero_rel_dist_from_I = abs(press_1 * press_2 / (press_2 * (abs(press_1) + abs(press_2))))
                    if oneSignPositive:
                        if press_1 < 0.0 and press_2 < 0.0:
                            press_1 = 0.0
                            press_2 = 0.0
                        elif press_1 * press_2 < 0.0:
                            if press_1 < 0.0:
                                press_1 = 0.0
                                rel_dist_from_I_node_I = 1- zero_rel_dist_from_I
                            else: # press_2 < 0.0:
                                press_2 = 0.0
                                rel_dist_from_I_node_J = zero_rel_dist_from_I
                        pass
                    else: # not oneSignPositive
                        if press_1 > 0.0 and press_2 > 0.0:
                            press_1 = 0.0
                            press_2 = 0.0
                        elif press_1 * press_2 < 0.0:
                            if press_1 > 0.0:
                                press_1 = 0.0
                                rel_dist_from_I_node_I = zero_rel_dist_from_I
                            else: # press_2 < 0.0:
                                press_2 = 0.0
                                rel_dist_from_I_node_J = 1 - zero_rel_dist_from_I
                        pass

                if constValue:
                    press_1 = p0 * Bref
                    press_2 = press_1
                    lenght = math.sqrt((n1_coords[coords_idx]-n2_coords[coords_idx])**2)
                    if n1_coords[coords_idx] >= H0 and n2_coords[coords_idx] >= H0:
                        rel_dist_from_I_node_I = 0.0
                        rel_dist_from_I_node_J = 1.0
                        press_1 = 0.0
                        press_2 = 0.0
                    else:
                        if n1_coords[coords_idx] <= H0 and n2_coords[coords_idx] <= H0:
                            rel_dist_from_I_node_I = 0.0
                            rel_dist_from_I_node_J = 1.0
                        else:
                            zero_rel_dist_from_I = abs(abs(H0) - abs(n1_coords[coords_idx])) / lenght
                            if n1_coords[coords_idx] < H0 <= n2_coords[coords_idx]:
                                rel_dist_from_I_node_I = 0.0
                                rel_dist_from_I_node_J = 1.0 - zero_rel_dist_from_I
                            else:
                                rel_dist_from_I_node_I = zero_rel_dist_from_I
                                rel_dist_from_I_node_J = 1.0


                if dirLoad == "GCX":
                    self.addFrameLoad(
                        loadCase, t, tp="force",
                        GCX1=[rel_dist_from_I_node_I, press_1], GCX2=[rel_dist_from_I_node_J, press_2], local=local
                    )
                elif dirLoad == "GCY":
                    self.addFrameLoad(
                        loadCase, t, tp="force",
                        GCY1=[rel_dist_from_I_node_I, press_1], GCY2=[rel_dist_from_I_node_J, press_2], local=local
                    )
                elif dirLoad == "GCZ":
                    self.addFrameLoad(
                        loadCase, t, tp="force",
                        GCZ1=[rel_dist_from_I_node_I, press_1], GCZ2=[rel_dist_from_I_node_J, press_2], local=local
                    )
                else:
                    raise Ex.EXAExceptions(
                        "(EXAStructuralModel)-0011", "unknown error in dirLoad", type(dirLoad)
                    )

    def addMultiFrameLoad(
            self, loadCase, tagsFrames, tp="force",
            GCX1=None, GCX2=None, GCY1=None, GCY2=None, GCZ1=None, GCZ2=None, local=False
    ):
        if GCX1 is None:
            GCX1 = []
        if GCX2 is None:
            GCX2 = []
        if GCY1 is None:
            GCY1 = []
        if GCY2 is None:
            GCY2 = []
        if GCZ1 is None:
            GCZ1 = []
        if GCZ2 is None:
            GCZ2 = []

        if not isinstance(tagsFrames, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0011",
                "tagsFrames must be a list",
                type(tagsFrames),
            )

        for tag in tagsFrames:
            self.addFrameLoad(loadCase, tag, tp, GCX1, GCX2, GCY1, GCY2, GCZ1, GCZ2, local)

    def addFrameLoad(
            self, loadCase, tagFrame, tp="force",
            GCX1=None, GCX2=None, GCY1=None, GCY2=None, GCZ1=None, GCZ2=None, local=False
    ):
        if GCX1 is None:
            GCX1 = []
        if GCX2 is None:
            GCX2 = []
        if GCY1 is None:
            GCY1 = []
        if GCY2 is None:
            GCY2 = []
        if GCZ1 is None:
            GCZ1 = []
        if GCZ2 is None:
            GCZ2 = []

        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0011",
                "First arg must be a string",
                type(loadCase),
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0012", "Load case unknown", loadCase
            )

        if tagFrame not in self.framesTags():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0013", "Frames tag unknown", tagFrame
            )

        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0014", "Third arg must be a string", type(tp)
            )

        if all(["force" != tp, "moment" != tp]):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0015", "tp option *force* or *moment*", tp
            )

        if not isinstance(GCX1, list) or \
           not isinstance(GCX2, list) or \
           not isinstance(GCY1, list) or \
           not isinstance(GCY2, list) or \
           not isinstance(GCZ1, list) or \
           not isinstance(GCZ2, list) :
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0016", "GCX1 ... GCZ2 arg must be lists", type(tp)
            )

        cond_null_X = all([len(GCX1) == 0, len(GCX2) == 0])
        cond_null_Y = all([len(GCY1) == 0, len(GCY2) == 0])
        cond_null_Z = all([len(GCZ1) == 0, len(GCZ2) == 0])

        if not cond_null_X:
            if len(GCX1) != 2:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0016", "GCX1 must have len 2", len(GCX1)
                )

            if not all(isinstance(n, float) for n in GCX1):
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0017", "GCX1 must be float list", GCX1
                )

            if len(GCX2) != 2 and len(GCX2) != 0:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0018", "GCX2 must have len 2 or 0", GCX2
                )

            if len(GCX2) == 0:
                GCX2 = GCX1[:]
                GCX2[0] = 1.0

        if not cond_null_Y:
            if len(GCY1) != 2:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0019", "GCY1 must have len 2", len(GCY1)
                )

            if not all(isinstance(n, float) for n in GCY1):
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0017", "GCY1 must be float list", GCY1
                )

            if len(GCY2) != 2 and len(GCY2) != 0:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0021", "GCX2 must have len 2 or 0", GCY2
                )

            if len(GCY2) == 0:
                GCY2 = GCY1[:]
                GCY2[0] = 1.0

        if not cond_null_Z:
            if len(GCZ1) != 2:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0022", "GCZ1 must have len 2", len(GCZ1)
                )

            if not all(isinstance(n, float) for n in GCZ1):
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0017", "GCZ1 must be float list", GCZ1
                )

            if len(GCZ1) != 2 and len(GCZ1) != 0:
                raise Ex.EXAExceptions(
                    "(EXAStructuralModel)-0024", "GCX2 must have len 2 or 0", GCZ1
                )

            if len(GCZ2) == 0:
                GCZ2 = GCZ1[:]
                GCZ2[0] = 1.0

        if loadCase not in self.__loads:
            self.__loads[loadCase] = {}

        if "frameLoad" not in self.__loads[loadCase]:
            self.__loads[loadCase]["frameLoad"] = {}

        if tagFrame not in self.__loads[loadCase]["frameLoad"].keys():
            self.__loads[loadCase]["frameLoad"][tagFrame] = {}

        if tp not in self.__loads[loadCase]["frameLoad"][tagFrame].keys():
            self.__loads[loadCase]["frameLoad"][tagFrame][tp] = {}

        sfx = "G"
        if local:
            sfx = "L"

        if not cond_null_X:
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CX1"] = GCX1
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CX2"] = GCX2

        if not cond_null_Y:
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CY1"] = GCY1
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CY2"] = GCY2

        if not cond_null_Z:
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CZ1"] = GCZ1
            self.__loads[loadCase]["frameLoad"][tagFrame][tp][sfx+"CZ2"] = GCZ2

    def addMultiNodeLoad(self, loadCase, tagsNodes, NCS):
        if not isinstance(tagsNodes, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "tagsNodes arg must be a list", tagsNodes
            )

        for tag in tagsNodes:
            self.assignNodeLoad(loadCase, tag, NCS)

    def assignNodeLoad(self, loadCase, tagNode, NCS):
        if not isinstance(loadCase, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "First arg must be a string", loadCase
            )

        if loadCase not in self.__loadCase.keys():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0019", "Load case unknown", loadCase
            )

        if tagNode not in self.nodesTags():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0020", "Nodes tag unknown", tagNode
            )

        if not all(isinstance(n, float) for n in NCS):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "NCS must be float list", NCS
            )

        if len(NCS) != 6:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022", "NCS must have len 6", len(NCS)
            )

        if loadCase not in self.__loads:
            self.__loads[loadCase] = {}

        if "nodeLoad" not in self.__loads[loadCase]:
            self.__loads[loadCase]["nodeLoad"] = {}

        self.__loads[loadCase]["nodeLoad"][tagNode] = {"NCS": NCS}

    def addMultiNodeContraints(self, tagsNodes, dof):
        if not isinstance(tagsNodes, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "tagsNodes arg must be a list", tagsNodes
            )

        for tag in tagsNodes:
            self.addNodeContraints(tag, dof)

    def addNodeContraints(self, tagNode, dof):
        if tagNode not in self.nodesTags():
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0034", "Nodes tag unknown", tagNode
            )

        if not all(isinstance(n, int) for n in dof):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0021", "dof must be int list", dof
            )

        if len(dof) != 6:
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022", "dof must have len 6", len(dof)
            )

        self.__nodeSupports[tagNode] = dof

    def getNodeContraints(self):
        return self.__nodeSupports

    def addMultiNodeSpring(self, tagsNodes, tp, dirSpring, stiffness):
        if not isinstance(tagsNodes, list):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0018", "tagsNodes arg must be a list", tagsNodes
            )

        for tag in tagsNodes:
            self.addNodeSpring(tag, tp, dirSpring, stiffness)

    def addNodeSpring(self, tagNode, tp, dirSpring, stiffness, add=False):
        if not (isinstance(tagNode, int) or isinstance(tagNode, np.uint64)):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022",
                "First arg *tagNode* must be int or numpy.uint64",
                tagNode,
            )

        if not isinstance(tp, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022", "Second arg *tp* must be str", tp
            )

        if tp not in ("LINEAR", "COMP", "TENS"):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022",
                "Second arg *tp* must be LINEAR, COMP or TENS",
                tp,
            )

        if not isinstance(dirSpring, str):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022", "Third arg *dir* must be str", dirSpring
            )

        if dirSpring not in ("DX+", "DX-", "DY+", "DY-", "DZ+", "DZ-"):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022", "Third arg *dir* must be DX+ ... DZ-", dirSpring
            )

        if not isinstance(stiffness, float):
            raise Ex.EXAExceptions(
                "(EXAStructuralModel)-0022",
                "Fourth arg *stiffness* must be float",
                stiffness,
            )

        if tagNode not in self.__nodeSprings.keys():
            self.__nodeSprings[tagNode] = {}

        if tp not in self.__nodeSprings[tagNode].keys():
            self.__nodeSprings[tagNode][tp] = {}

        if dirSpring in self.__nodeSprings[tagNode][tp] and add:
            self.__nodeSprings[tagNode][tp][dirSpring] += stiffness
        else:
            self.__nodeSprings[tagNode][tp][dirSpring] = stiffness

    def getNodeSprings(self):
        return self.__nodeSprings

    @staticmethod
    def getNodesPhysicalName():
        groups = gmsh_model.getPhysicalGroups(0)
        names = []
        for g in groups:
            names.append(gmsh_model.getPhysicalName(g[0], g[1]))
        return names

    @staticmethod
    def getPhisicalNames() -> List[str]:
        """
        Get unique physical names defined.
        If many groups exist with same name returns unique values

        Returns:
            List of unique group names
        """
        groups = gmsh_model.getPhysicalGroups()
        names = []
        for g in groups:
            names.append(gmsh_model.getPhysicalName(g[0], g[1]))
        return list(set(names))

    @staticmethod
    def getFramesPhysicalName():
        groups = gmsh_model.getPhysicalGroups(1)
        names = []
        for g in groups:
            names.append(gmsh_model.getPhysicalName(g[0], g[1]))
        return names

    @staticmethod
    def getNodesByPhysicalName(name):
        groups = gmsh_model.getPhysicalGroups(0)
        for g in groups:
            if name == gmsh_model.getPhysicalName(g[0], g[1]):
                return list(gmsh_model.getEntitiesForPhysicalGroup(g[0], g[1]))
        return []


    @staticmethod
    def getNodesByPhysicalGroup(tagGroup):
        groups = gmsh_model.getPhysicalGroups(0)
        for g in groups:
            if g[1] == tagGroup:
                return list(gmsh_model.getEntitiesForPhysicalGroup(g[0], g[1]))
        return []


    @staticmethod
    def getMacroFramesByPhysicalName(name):
        groups = gmsh_model.getPhysicalGroups(1)
        for g in groups:
            if name == gmsh_model.getPhysicalName(g[0], g[1]):
                return list(gmsh_model.getEntitiesForPhysicalGroup(g[0], g[1]))
        return []


    @staticmethod
    def getFramesByPhysicalGroup(tagGroup):
        groups = gmsh_model.getPhysicalGroups(1)
        for g in groups:
            if g[1] == tagGroup:
                return list(gmsh_model.getEntitiesForPhysicalGroup(g[0], g[1]))
        return []

    def __save_mgt(self, fileName):
        # ----------------
        # *NODE    ; Nodes
        # ; iNO, X, Y, Z
        # ----------------
        nodes = []
        nodesTags = self.nodesTags()
        nodesCoords = self.nodesCoords()
        for i, n in enumerate(nodesTags):
            strFormat = "{id:d},{x:.6f},{y:.6f},{z:.6f}"
            formatted = strFormat.format(
                id=n, x=nodesCoords[i][0], y=nodesCoords[i][1], z=nodesCoords[i][2]
            )
            nodes.append(formatted)

        # ------------------------------------------------------------------------------------
        # *ELEMENT    ; Elements
        # ; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB,                     ; Frame  Element
        # ; iEL, TYPE, iMAT, iPRO, iN1, iN2, ANGLE, iSUB, EXVAL, EXVAL2, bLMT ; Comp/Tens Truss
        # ; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iSUB, iWID , LCAXIS    ; Planar Element
        # ; iEL, TYPE, iMAT, iPRO, iN1, iN2, iN3, iN4, iN5, iN6, iN7, iN8     ; Solid  Element
        # ------------------------------------------------------------------------------------
        frames = []
        framesTags = self.framesTags()
        framesNodeTags = self.framesNodeTags()

        for i, f in enumerate(framesTags):
            if f in self.__framesShapes.keys():
                idShape = self.__framesShapes[f]
            else:
                idShape = 1
            strFormat = "{id:d},BEAM,1,{iPRO:d},{idStart:d},{idEnd:d},0,0"
            formatted = strFormat.format(
                id=f,
                iPRO=idShape,
                idStart=framesNodeTags[i][0],
                idEnd=framesNodeTags[i][1],
            )
            frames.append(formatted)

        # -----------------------------------------------------------------------------------------------------------
        # *SECTION    ; Section
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, [DATA1], [DATA2]                    ; 1st line - DB/USER
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, BLT, D1, ..., D8, iCEL              ; 1st line - VALUE
        # ;       AREA, ASy, ASz, Ixx, Iyy, Izz                                               ; 2nd line
        # ;       CyP, CyM, CzP, CzM, QyB, QzB, PERI_OUT, PERI_IN, Cy, Cz                     ; 3rd line
        # ;       Y1, Y2, Y3, Y4, Z1, Z2, Z3, Z4, Zyy, Zzz                                    ; 4th line
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, ELAST, DEN, POIS, POIC, SF, THERMAL ; 1st line - SRC
        # ;       D1, D2, [SRC]                                                               ; 2nd line
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, 1, DB, NAME1, NAME2, D1, D2         ; 1st line - COMBINED
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE, 2, D11, D12, D13, D14, D15, D21, D22, D23, D24
        # ; iSEC, TYPE, SNAME, [OFFSET2], bSD, bWE, SHAPE, iyVAR, izVAR, STYPE                ; 1st line - TAPERED
        # ;       DB, NAME1, NAME2                                                            ; 2nd line(STYPE=DB)
        # ;       [DIM1], [DIM2]                                                              ; 2nd line(STYPE=USER)
        # ;       D11, D12, D13, D14, D15, D16, D17, D18                                      ; 2nd line(STYPE=VALUE)
        # ;       AREA1, ASy1, ASz1, Ixx1, Iyy1, Izz1                                         ; 3rd line(STYPE=VALUE)
        # ;       CyP1, CyM1, CzP1, CzM1, QyB1, QzB1, PERI_OUT1, PERI_IN1, Cy1, Cz1           ; 4th line(STYPE=VALUE)
        # ;       Y11, Y12, Y13, Y14, Z11, Z12, Z13, Z14, Zyy1, Zyy2                          ; 5th line(STYPE=VALUE)
        # ;       D21, D22, D23, D24, D25, D26, D27, D28                                      ; 6th line(STYPE=VALUE)
        # ;       AREA2, ASy2, ASz2, Ixx2, Iyy2, Izz2                                         ; 7th line(STYPE=VALUE)
        # ;       CyP2, CyM2, CzP2, CzM2, QyB2, QzB2, PERI_OUT2, PERI_IN2, Cy2, Cz2           ; 8th line(STYPE=VALUE)
        # ;       Y21, Y22, Y23, Y24, Z21, Z22, Z23, Z24, Zyy2, Zzz2                          ; 9th line(STYPE=VALUE)
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE                                      ; 1st line - COMPOSITE-B
        # ;       Hw, tw, B1, Bf1, tf1, B2, Bf2, tf2                                          ; 2nd line
        # ;       [SHAPE-NUM], [STIFF-SHAPE], [STIFF-POS] (1~4)                               ; 3rd line
        # ;       SW, GN, CTC, Bc, Tc, Hh, EsEc, DsDc, Ps, Pc, TsTc, bMulti, Elong, Esh       ; 4th line
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE                                      ; 1st line - COMPOSITE-I
        # ;       Hw, tw, B1, tf1, B2, tf2                                                    ; 2nd line
        # ;       [SHAPE-NUM], [STIFF-SHAPE], [STIFF-POS] (1~2)                               ; 3rd line
        # ;       SW, GN, CTC, Bc, Tc, Hh, EsEc, DsDc, Ps, Pc, TsTc, bMulti, Elong, Esh       ; 4th line
        # ; iSEC, TYPE, SNAME, [OFFSET], bSD, bWE, SHAPE                                      ; 1st line - COMPOSITE-TUB
        # ;       Hw, tw, B1, Bf1, tf1, B2, Bf2, tf2, Bf3, tfp                                ; 2nd line
        # ;       [SHAPE-NUM], [STIFF-SHAPE], [STIFF-POS] (1~3)                               ; 3rd line
        # ;       SW, GN, CTC, Bc, Tc, Hh, EsEc, DsDc, Ps, Pc, TsTc, bMulti, Elong, Esh       ; 4th line
        # ; [DATA1] : 1, DB, NAME or 2, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10
        # ; [DATA2] : CCSHAPE or iCEL or iN1, iN2
        # ; [SRC]  : 1, DB, NAME1, NAME2 or 2, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, iN1, iN2
        # ; [DIM1], [DIM2] : D1, D2, D3, D4, D5, D6, D7, D8
        # ; [OFFSET] : OFFSET, iCENT, iREF, iHORZ, HUSER, iVERT, VUSER
        # ; [OFFSET2]: OFFSET, iCENT, iREF, iHORZ, HUSERI, HUSERJ, iVERT, VUSERI, VUSERJ
        # ; [SHAPE-NUM]: SHAPE-NUM, POS, STIFF-NUM1, STIFF-NUM2, STIFF-NUM3, STIFF-NUM4
        # ; [STIFF-SHAPE]: SHAPE-NUM, for(SHAPE-NUM) { NAME, SIZE1~8 }
        # ; [STIFF-POS]: STIFF-NUM, for(STIFF-NUM) { SPACING, iSHAPE, bCALC }
        # -----------------------------------------------------------------------------------------------------------

        sections = []
        for k, v in self.__sectionShapes.items():
            strFormat = "{idShape:>8d},DBUSER,{name:>16s}, CC, 0, 0, 0, 0, 0, 0, YES, NO, SB, 2,{width:>8.3f},{height:>8.3f},0,0,0,0,0,0,0,0"
            formatted = strFormat.format(
                idShape=k,
                name=v["name"],
                width=v["dimensions"][0],
                height=v["dimensions"][1],
            )
            sections.append(formatted)

            # --------------------------------
        # *STLDCASE    ; Static Load Cases
        # ; LCNAME, LCTYPE, DESC
        # --------------------------------
        loadCases = []
        for k in self.__loadCase.keys():
            v = self.__loadCase[k]
            strFormat = "{LCNAME:>8s},{LCTYPE:>3s},{DESC:>40s}"
            formatted = strFormat.format(LCNAME=k, LCTYPE=v[0], DESC=v[1])
            loadCases.append(formatted)

        # --------------------------------------------
        # *CONSTRAINT    ; Supports
        # ; NODE_LIST, CONST(Dx,Dy,Dz,Rx,Ry,Rz), GROUP
        # --------------------------------------------
        nodeContraints = []
        if len(self.__nodeSupports) > 0:
            nodeContraints.append("*CONSTRAINT")
            for k, v in self.__nodeSupports.items():
                strFormat = "{tag:d},{TX:d}{TY:d}{TZ:d}{RX:d}{RY:d}{RZ:d}"
                formatted = strFormat.format(
                    tag=k, TX=v[0], TY=v[1], TZ=v[2], RX=v[3], RY=v[4], RZ=v[5]
                )
                nodeContraints.append(formatted)

        # -----------------------------------------------------------------------------------------------------------------
        # *SPRING    ; Point Spring Supports
        # ; NODE_LIST, Type, F_SDx, F_SDy, F_SDz, F_SRx, F_SRy, F_SRz, SDx, SDy, SDz, SRx, SRy, SRz ...
        # ;                  DAMPING, Cx, Cy, Cz, CRx, CRy, CRz, GROUP, [DATA1]                                ; LINEAR
        # ; NODE_LIST, Type, Direction, Vx, Vy, Vz, Stiffness, GROUP, [DATA1]                                  ; COMP, TENS
        # ; NODE_LIST, Type, Direction, Vx, Vy, Vz, FUNCTION, GROUP, [DATA1]                                   ; MULTI
        # ; [DATA1] EFFAREA, Kx, Ky, Kz
        # -----------------------------------------------------------------------------------------------------------------
        springs = []
        if len(self.__nodeSprings) > 0:
            springs.append("*SPRING")
            for k, v in self.__nodeSprings.items():
                for kk, vv in v.items():
                    if kk == "COMP":
                        Type = "COMP"
                    elif kk == "TENS":
                        Type = "TENS"
                    elif kk == "LINEAR":
                        Type = "LINEAR"
                    else:
                        raise Ex.EXAExceptions(
                            "(EXAStructuralModel)-0026", "key error in Type", kk
                        )
                    for kkk, vvv in vv.items():
                        if kkk == "DX+":
                            Direction = 0
                        elif kkk == "DX-":
                            Direction = 1
                        elif kkk == "DY+":
                            Direction = 2
                        elif kkk == "DY-":
                            Direction = 3
                        elif kkk == "DZ+":
                            Direction = 4
                        elif kkk == "DZ-":
                            Direction = 5
                        else:
                            raise Ex.EXAExceptions(
                                "(EXAStructuralModel)-0026",
                                "key error in Direction",
                                kkk,
                            )
                        strFormat = "{tag:d},{Type:s},{Direction:d},0,0,0,{Stiffness:.6f}, , 0, 0, 0, 0, 0"
                        formatted = strFormat.format(
                            tag=k, Type=Type, Direction=Direction, Stiffness=vvv
                        )
                        springs.append(formatted)
            springs.append("")

        # -----------------
        # *USE-STLD, <name>
        # -----------------
        loadCasesUsed = []
        for k, v in self.__loads.items():
            strFormat = "*USE-STLD, {key:s}"
            formatted = strFormat.format(key=k)
            loadCasesUsed.append(formatted)
            loadCasesUsed.append("")
            for kk, vv in v.items():
                if kk == "frameLoad":
                    loadCasesUsed.append("*BEAMLOAD")
                    # *BEAMLOAD    ; Element Beam Loads
                    # ; ELEM_LIST, CMD, TYPE, DIR, bPROJ, [ECCEN], [VALUE], GROUP
                    # ; ELEM_LIST, CMD, TYPE, TYPE, DIR, VX, VY, VZ, bPROJ, [ECCEN], [VALUE], GROUP
                    # ; [VALUE]       : D1, P1, D2, P2, D3, P3, D4, P4
                    # ; [ECCEN]       : bECCEN, ECCDIR, I-END, J-END, bJ-END
                    # ; [ADDITIONAL]  : bADDITIONAL, ADDITIONAL_I-END, ADDITIONAL_J-END, bADDITIONAL_J-END
                    for kkk, vvv in vv.items():

                        for kkkk, vvvv in vvv.items():
                            if kkkk == "force":
                                tp = "UNILOAD"
                            elif kkkk == "moment":
                                tp = "UNIMOMENT"
                            else:
                                raise Ex.EXAExceptions(
                                    "(EXAStructuralModel)-0026", "key error in tp", kkkk
                                )

                            if "GCX1" in vvvv.keys() and "GCX2" in vvvv.keys():
                                strFormat = "{tag: d}, BEAM   , {tp}, GX, NO , NO, aDir[1], , , , {GCX1D:.6f}, {GCX1P:.6f}, {GCX2D:.6f}, {GCX2P:.6f}, 0, 0, 0, 0, , NO, 0, 0, NO,"
                                formatted = strFormat.format(
                                    tag=kkk,
                                    tp=tp,
                                    GCX1D=vvvv["GCX1"][0],
                                    GCX1P=vvvv["GCX1"][1],
                                    GCX2D=vvvv["GCX2"][0],
                                    GCX2P=vvvv["GCX2"][1],
                                )
                                loadCasesUsed.append(formatted)
                            if "GCY1" in vvvv.keys() and "GCY2" in vvvv.keys():
                                strFormat = "{tag: d}, BEAM   , {tp}, GY, NO , NO, aDir[1], , , , {GCY1D:.6f}, {GCY1P:.6f}, {GCY2D:.6f}, {GCY2P:.6f}, 0, 0, 0, 0, , NO, 0, 0, NO,"
                                formatted = strFormat.format(
                                    tag=kkk,
                                    tp=tp,
                                    GCY1D=vvvv["GCY1"][0],
                                    GCY1P=vvvv["GCY1"][1],
                                    GCY2D=vvvv["GCY2"][0],
                                    GCY2P=vvvv["GCY2"][1],
                                )
                                loadCasesUsed.append(formatted)
                            if "GCZ1" in vvvv.keys() and "GCZ2" in vvvv.keys():
                                strFormat = "{tag: d}, BEAM   , {tp}, GZ, NO , NO, aDir[1], , , , {GCZ1D:.6f}, {GCZ1P:.6f}, {GCZ2D:.6f}, {GCZ2P:.6f}, 0, 0, 0, 0, , NO, 0, 0, NO,"
                                formatted = strFormat.format(
                                    tag=kkk,
                                    tp=tp,
                                    GCZ1D=vvvv["GCZ1"][0],
                                    GCZ1P=vvvv["GCZ1"][1],
                                    GCZ2D=vvvv["GCZ2"][0],
                                    GCZ2P=vvvv["GCZ2"][1],
                                )
                                loadCasesUsed.append(formatted)

                    loadCasesUsed.append("")

                elif kk == "nodeLoad":
                    loadCasesUsed.append("*CONLOAD")
                    # *CONLOAD    ; Nodal Loads
                    # ; NODE_LIST, FX, FY, FZ, MX, MY, MZ, GROUP
                    for kkk, vvv in vv.items():
                        strFormat = "{tag: d}, {FX:.6f}, {FY:.6f}, {FZ:.6f}, {MX:.6f}, {MY:.6f}, {MZ:.6f},"
                        formatted = strFormat.format(
                            tag=kkk,
                            FX=vvv["NCS"][0],
                            FY=vvv["NCS"][1],
                            FZ=vvv["NCS"][2],
                            MX=vvv["NCS"][3],
                            MY=vvv["NCS"][4],
                            MZ=vvv["NCS"][5],
                        )
                        loadCasesUsed.append(formatted)

                    loadCasesUsed.append("")

                elif kk == "selfWeight":
                    loadCasesUsed.append("*SELFWEIGHT")
                    strFormat = "{DIRX: .6f}, {DIRY: .6f}, {DIRZ: .6f},"
                    formatted = strFormat.format(DIRX=vv[0], DIRY=vv[1], DIRZ=vv[2])
                    loadCasesUsed.append(formatted)
                    loadCasesUsed.append("")
                else:
                    raise Ex.EXAExceptions(
                        "(EXAStructuralModel)-0025", "key error in loadCasesUsed", kk
                    )

            loadCasesUsed.append(
                f"; End of data for load case {k} -------------------------"
            )

        output = template.render(
            udm="KN,M, BTU, C",
            nodes=nodes,
            elements=frames,
            loadCases=loadCases,
            loadCasesUsed=loadCasesUsed,
            contraints=nodeContraints,
            springs=springs,
            sections=sections,
        )

        # print(output)

        with open(fileName + ".mgt", "w") as f:
            f.write(output)

    def save(self, fileName, fileType=".msh"):
        print("Write ", fileName + fileType)
        gmsh.option.setNumber("Mesh.SaveAll", 1)
        if fileType == ".msh":
            gmsh.write(fileName + fileType)
            # logGmshFile(fileName + fileType)
        elif fileType == ".med":
            gmsh.write(fileName + fileType)
        elif fileType == ".mgt":
            self.__save_mgt(fileName)
        else:
            self.__log("ERR", f"File type unknoun *{fileType}*. None file saved !!!")

    def getCad(self):
        return self.__cad

    @staticmethod
    def getModeler():
        return gmsh_model

    def addModel(self, name: str) -> bool:
        if len(name) == 0:
            self.__log("ERR", "Arg must be a str not null !!!")
            return False
        else:
            if name in self.__models:
                self.__log("ERR", f"Model *{name}* is present !!!")
                return False
            else:
                gmsh_model.add(name)
                self.__models.append(name)
                self.__log("INF", f"Model *{name}* added !!!")
                return True

    def getModels(self) -> List[str]:
        return self.__models

    def setCurrentModel(self, name: str) -> bool:
        if name not in self.__models:
            self.__log("ERR", f"Model *{name}* not present !!!")
            return False
        else:
            gmsh_model.setCurrent(name)
            return True

    def addNodesToGroup(self, tags, tagGroup, physicalName=""):
        self.__addElementToGroup(tags, tagGroup, Dim.DIM_0D, physicalName)

    @staticmethod
    def __addElementToGroup(
        tags: List[int], tagGroup: int, dim: Dim, physicalName: str = ""
    ):
        gmsh_model.addPhysicalGroup(dim.value, tags, tagGroup)
        if len(physicalName) > 0:
            gmsh_model.setPhysicalName(dim.value, tagGroup, physicalName)

    @staticmethod
    def renumberFramesByNodeCoords(macroTags: List[int], dirRule: Literal['+X', '+Y', '+Z', '-X', '-Y', '-Z']):
        oldFrameTags = FEModel.getFramesFromMacroTags(macroTags)
        oldNodesTags = FEModel.getFrameNodesFromMacro(macroTags)

        idxCoord = ['X', 'Y', 'Z'].index(dirRule[1])
        oldMediumCoord = [0] * len(oldFrameTags)
        assert isinstance(oldNodesTags, list)

        for i, t in enumerate(oldNodesTags):
            oldMediumCoord[i] = (FEModel.nodeCoords(t[0])[idxCoord] + FEModel.nodeCoords(t[0])[idxCoord]) / 2

        oldTagCoords = zip(oldFrameTags, oldMediumCoord)

        rev = False
        if dirRule[0] == '-':
            rev = True

        oldTagCoordsSorted = sorted(oldTagCoords, key=lambda tc: tc[1], reverse=rev)

        newFrameTags = [0] * len(oldTagCoordsSorted)
        for i, t in enumerate(oldTagCoordsSorted):
            newFrameTags[i] = oldTagCoordsSorted[i][0]

        return oldFrameTags, newFrameTags

    @staticmethod
    def renumberArrange(oldMacroTags: List[List[int]], newMacroTags: List[List[int]]):
        compactOldTags = oldMacroTags[0]
        for i in range(len(oldMacroTags)-1):
            compactOldTags.extend(oldMacroTags[i+1])

        compactNewTags = newMacroTags[0]
        for i in range(len(newMacroTags)-1):
            compactNewTags.extend(newMacroTags[i+1])

        gmsh.model.mesh.renumberElements(compactOldTags, compactNewTags)

    def addFramesToGroup(self, tags: List[int], tagGroup: int, physicalName: str = "") -> None:
        """
        At macro element level adds frame to group.

        Args:
            tags ():
            tagGroup ():
            physicalName ():
        """
        self.__addElementToGroup(tags, tagGroup, Dim.DIM_1D, physicalName)
        for t in self.getFramesFromMacroTags(tags):
            if self.__framesPhysicalNames.get(t) is None:
                self.__framesPhysicalNames[t] = [physicalName]
            else:
                self.__framesPhysicalNames[t].append(physicalName)


    def getPhysicalNamesForFrame(self, tag):
        return self.__framesPhysicalNames.get(tag)

    def addNode(self, x, y, z, tag=-1, group=False, tagGroup=-1):
        tag = self.__cad.addPoint(x, y, z, meshSize=0.0, tag=tag)
        self.__cad.synchronize()
        if group:
            gmsh_model.addPhysicalGroup(0, [tag], tag=tagGroup)
            # self.__cad.synchronize()
        return tag

    def addFrame(self, tagStart, tagEnd, tag=-1, group=False, tagGroup=-1, nb=1):
        tag = self.__cad.addLine(tagStart, tagEnd, tag=tag)
        self.__cad.synchronize()

        # mesh frame to have underlying mesh
        mesh = gmsh_model.mesh
        mesh.setTransfiniteCurve(tag, nb + 1)
        mesh.generate(1)

        if group:
            gmsh_model.addPhysicalGroup(1, [tag], tag=tagGroup)
            # self.__cad.synchronize()
        return tag

    def addPlateQuad(
        self,
        tagLine_1: int,
        tagLine_2: int,
        tagLine_3: int,
        tagLine_4: int,
        tag: int = -1,
        group: bool = False,
        tagGroup: int = -1,
        elType: Elem = Elem.ELEM_QUAD,
    ):
        wireId = self.__cad.addCurveLoop([tagLine_1, tagLine_2, tagLine_3, tagLine_4])
        plateId = self.__cad.addPlaneSurface(wireTags=[wireId], tag=tag)
        self.__cad.synchronize()
        mesh = gmsh_model.mesh
        mesh.setTransfiniteSurface(tag=plateId, arrangement="left")
        if elType == Elem.ELEM_QUAD:
            mesh.setRecombine(dim=2, tag=plateId)

        mesh.generate(2)

        if group:
            gmsh_model.addPhysicalGroup(2, [plateId], tag=tagGroup)
        return tag

    def addPlateQuadsToGroup(self, tags, tagGroup, physicalName=""):
        self.__addElementToGroup(tags, tagGroup, Dim.DIM_2D, physicalName)

    def addArc(self, tagStart, tagMid, tagEnd, tag=-1, group=False, tagGroup=-1, nb=10):
        tag = self.__cad.addCircleArc(tagStart, tagMid, tagEnd, tag=tag)
        self.__cad.synchronize()

        # mesh frame to have underlying mesh
        mesh = gmsh_model.mesh
        mesh.setTransfiniteCurve(tag, nb + 1)
        mesh.generate(1)

        if group:
            gmsh_model.addPhysicalGroup(1, [tag], tag=tagGroup)
            # self.__cad.synchronize()
        return tag


    def assignGroupTreeToPhysical(self, treePath: List[str | None], physicalName: str):
        if len(treePath) == 0:
            raise ValueError(f'treePath has len 0 !!!')

        if treePath[0] is None:
            raise ValueError(f'treePath starts with None type !!!')

        if physicalName == "":
            raise ValueError(f'physicalName has len 0 !!!')

        pn = self.getPhisicalNames()
        if not physicalName in pn:
            raise ValueError(f'physicalName given "{physicalName}" not in {pn} !!!')


        # check if None type are compacted at end of list
        hashStr = ""
        isNone = False
        for cols in treePath:
            if isNone:
                if cols is not None:
                    raise ValueError(f'None type within not none type !!!')
            if cols is None:
                isNone = True
            else:
                hashStr += cols + "/"

        self.__groupTree[hashStr] = physicalName

    def getGroupTreeToPhysical(self):
        return self.__groupTree


    def __str__(self):
        s = f"Model Description: {self.__description:s}"
        return s
