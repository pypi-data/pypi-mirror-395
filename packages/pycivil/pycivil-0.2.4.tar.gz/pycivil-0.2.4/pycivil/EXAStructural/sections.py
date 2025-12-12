"""
Created on Wed Jan 16 18:02:25 2019

@author: lpaone
"""
import math
from dataclasses import field
from enum import Enum
from typing import Any, List, Optional, Tuple, Union

import numpy as np
from pydantic import BaseModel

import pycivil.EXAStructural.lawcodes.codeEC212 as fireCode
import pycivil.EXAStructural.codes as codes
import pycivil.EXAStructural.materials as materials
from pycivil.EXAGeometry.geometry import Point2d
from pycivil.EXAGeometry.shapes import Shape, ShapeArea, ShapeRect
from pycivil.EXAStructural.materials import ConcreteModel, SteelModel


class ShapeEnum(str, Enum):
    RECT = "rectangular"
    T_SHAPE = "T-shape"
    I_SHAPE = "I-shape"
    POLYGONAL = "polygon"


class ShapeModel(BaseModel):
    tp: Optional[ShapeEnum] = None
    id: int = 0
    descr: str = ""
    selected: List[int] = field(default_factory=list)


class RectangularShape(ShapeModel):
    tp: ShapeEnum = ShapeEnum.RECT
    width: float
    height: float

class TShape(ShapeModel):
    tp: ShapeEnum = ShapeEnum.T_SHAPE
    width: float
    height: float
    slab_width: float
    slab_height: float
    web_position: float

class RebarDisposerEnum(str, Enum):
    SINGLE = "single"
    LINE = "line"
    STIRRUP = "stirrup"
    STIRRUP_Y = "stirrup_single_leg_y"


class ShapePositionEnum(str, Enum):
    MT = "MT"
    MB = "MB"


class SteelDisposerSingle(BaseModel):
    id: int = -1
    tp: RebarDisposerEnum = RebarDisposerEnum.SINGLE
    area: float
    xpos: float
    ypos: float


class SteelDisposerOnLine(BaseModel):
    tp: RebarDisposerEnum = RebarDisposerEnum.LINE
    fromPos: ShapePositionEnum = ShapePositionEnum.MB
    diameter: float = 20
    steelInterDistance: float = 20
    distanceFromPos: float = 20
    number: float | int = 4


class SteelDisposerStirrup(BaseModel):
    tp: RebarDisposerEnum = RebarDisposerEnum.STIRRUP
    area: Optional[float] = None
    step: Optional[float] = None
    angle: Optional[float] = None


class SteelDisposerStirrupSingleLeg(BaseModel):
    id: int = -1
    tp: RebarDisposerEnum = RebarDisposerEnum.STIRRUP_Y
    diameter: float = 8
    angle: float = 0
    slope: float = 90
    centerX: float = 0
    centerY: float = 0
    length: float = 0
    step: float = 0


class AreaProperties(BaseModel):
    area: float = 0
    sx: float = 0
    sy: float = 0
    ixx: float = 0
    iyy: float = 0
    ixy: float = 0
    ixxx: float = 0
    ixxy: float = 0


class SectionStates(str, Enum):
    UNKNOWN = "UNKNOWN"
    COMPRESSED = "COMPRESSED"
    STRETCHED = "STRETCHED"
    PARTIALIZED = "PARTIALIZED"


class StructSectionItem:
    def __init__(
        self,
        shape: Union[Shape, None],
        material: Union[materials.Material, None] = None,
        ids: int = -1,
    ):
        if shape is None:
            shape = Shape()
        if material is None:
            material = materials.Material()

        self.__id = ids
        self.shape = shape
        self.material = material

    def setId(self, ids: Union[int, None]) -> None:
        self.__id = ids

    def getId(self) -> Union[int, None]:
        return self.__id

    def getShape(self):
        return self.shape

    def getOrigin(self):
        return self.shape.getOrigin()

    def setOriginX(self, x):
        p = self.shape.getOrigin()
        p.x = x
        self.shape.setOrigin(p)

    def setOriginY(self, y):
        p = self.shape.getOrigin()
        p.y = y
        self.shape.setOrigin(p)

    def getArea(self) -> float:
        return self.shape.getArea()

    def getDiameter(self) -> float:
        return self.shape.getDiameter()

    def getMaterial(self):
        return self.material

    def __str__(self):
        dispstr = "StructSectionItem Object: \n"
        dispstr = dispstr + "--------------------  \n"
        dispstr = dispstr + "Shape embedded-->\n"
        dispstr = dispstr + self.shape.__str__().replace("\n", "\n  | ")
        dispstr = dispstr + "Material embedded-->\n"
        dispstr = dispstr + self.material.__str__().replace("\n", "\n  | ")
        return dispstr


class ConcreteSection:
    """Class that instantiate a general concrete section

    Reference for geometry is:

                     ----------------
                     |              |
                     |              |
                     |    Y ^       |
                     |      |       |
                     |      |   X   |
                     |      O--->   |
                     |              |
                     |              |
                     |              |
                     ----------------

     for forces and moments (N compression negative)

                     ----------------
                     |              |
                     |              |
                     |      --.     |
                     |  My     \\    |
                     |  <<--O   ;   |
                     |      |  /    |
                     |     <--'     |
                     |  N = Fx < 0  |
                     |              |
                     ----------------


    """

    def __init__(self, ids: int = 0, descr: str = ""):

        self.__ids: int = ids
        self.__descr: str = descr

        # StructuralItemContainer
        self.__concreteItem: Union[StructSectionItem, None] = None
        self.__steelItems: list[StructSectionItem] = []
        self.__steelItemsWeights = []  # Weight to apply alpha for design
        self.__steelItemsAlphaWeight = 1.0  # Alpha designer factor
        self.__steelItemsTemperatures: List[float] = []  # Temperature for steel
        self.__steelItems_kappa_s: List[float] = []  # Temperature for steel

        # Coding by
        self.__code = codes.Code("EC2")
        self.__elementType = "beam"

        # Concrete material set
        cls_material = materials.Concrete(descr="EC2-C20/25 [default]")
        cls_material.setByCode(self.__code, "C20/25")
        self.__concreteMaterial = cls_material
        # Steel material set
        steel_material = materials.ConcreteSteel(descr="EC2-B450C [default]")
        steel_material.setByCode(self.__code, "B450C")
        self.__steelMaterial = steel_material

        self.__homogenization = 15.0

        # Material only for section
        self.__steelMaxStress = 0.85 * 450
        self.__steel_safetyFactorForULS = 1.15
        self.__concreteMaxStress = 0.65 * 20
        self.__cls_safetyFactorForULS = 1.50

        self.__useSectionMaterials = True

        # SLS stress and forces
        self.__steelStress: List[float] = []
        self.__concrStress: List[float] = []
        self.__concrDeform: List[float] = []
        self.__N = None
        self.__Mx = None
        self.__My = None

        # Steel for stippupts
        self.__steelStirruptArea = None
        self.__steelStirruptDist = None
        self.__steelStirruptAngle = None

    def setForces(self, N=None, Mx=None, My=None, M=None):
        if N is not None:
            self.__N = N
        if Mx is not None:
            self.__Mx = Mx
        if My is not None:
            self.__My = My
        if M is not None:
            self.__Mx = M

    def getForceN(self):
        return self.__N

    def getForceM(self):
        return self.__Mx

    def setCode(self, c):
        if isinstance(c, codes.Code):
            self.__code = c
        else:
            raise Exception("Argument must have [Code] object !!!")

    def setElementType(self, elTypeStr):
        if isinstance(elTypeStr, str):
            self.__elementType = elTypeStr
        else:
            raise Exception("Argument must be str type !!!")

    def setStructConcrItem(self, strusecitem: StructSectionItem):
        if isinstance(strusecitem, StructSectionItem):
            if isinstance(strusecitem.getShape(), Shape) and isinstance(
                strusecitem.getMaterial(), materials.Concrete
            ):
                self.__concreteItem = strusecitem
            else:
                raise Exception(
                    "Argument must have [Shape] and [Concrete] as material assigned !!!"
                )
        else:
            raise Exception("Argument must be [structSectionItem] !!!")

    def setStructSteelItems(self, strusecitems: List[StructSectionItem]):
        if isinstance(strusecitems, list):
            for item in strusecitems:
                if not isinstance(item, StructSectionItem):
                    raise Exception("Only list of [structSectionItem] !!!")
                if not (
                    isinstance(item.getShape(), Shape)
                    and isinstance(item.getMaterial(), materials.ConcreteSteel)
                ):
                    raise Exception(
                        "List item must have [Shape] and [Steel] as material assigned !!!"
                    )
            self.__steelItems = strusecitems
            self.__steelItemsWeights = len(strusecitems) * [1.0]
        else:
            raise Exception("Argument must be list of [structSectionItem] !!!")

    def setSteelWeights(self, weights):
        if not isinstance(weights, list):
            raise Exception("Only list for weights !!!")
        for i in weights:
            if not isinstance(i, float):
                raise Exception("Only float for weights list !!!")
        if not len(weights) == len(self.__steelItems):
            raise Exception(
                "Weights lenght must be %1.0i same of steel items !!!"
                % len(self.__steelItems)
            )
        self.__steelItemsWeights = weights  # finally

    def setSteelTemperatures(self, temperatures: List[float]):
        if len(temperatures) != len(self.__steelItems):
            raise Exception("Temperatures must have same lenght of steel items !!!")
        self.__steelItemsTemperatures = temperatures
        return True

    def setSteelAlphaWeight(self, weight):
        if isinstance(weight, float):
            self.__steelItemsAlphaWeight = weight
        else:
            raise Exception("Only float type for weight !!!")

    def getSteelFireFactors(self) -> List[float]:
        return self.__steelItems_kappa_s

    def getSteelTemperatures(self) -> List[float]:
        return self.__steelItemsTemperatures

    def getSteelStress(self) -> List[float]:
        return self.__steelStress

    def setSteelStress(self, s: List[float]):
        self.__steelStress = s

    def getConcrStress(self) -> List[float]:
        return self.__concrStress

    def setConcrStress(self, s: List[float]):
        self.__concrStress = s

    def getConcrDeform(self) -> List[float]:
        return self.__concrDeform

    def setConcrDeform(self, s: List[float]):
        self.__concrDeform = s

    def getDescr(self):
        return self.__descr

    def getId(self):
        return self.__ids

    def getElementType(self):
        return self.__elementType

    def getSteelRebar(self) -> list[StructSectionItem]:
        return self.__steelItems

    def getSteelAreaAt(self, i, alphaWeight=False, weights=False):
        if alphaWeight:
            used_alphaWeight = self.__steelItemsAlphaWeight
        else:
            used_alphaWeight = 1.0

        if weights:
            used_weights = self.__steelItemsWeights[i]
        else:
            used_weights = 1.0

        return self.__steelItems[i].getArea() * used_alphaWeight * used_weights

    def getSteelDiamAt(self, i) -> float:
        # return round(2 * math.sqrt(self.__steelItems[i].getArea() / math.pi))
        return 2 * math.sqrt(self.__steelItems[i].getArea() / math.pi)

    def mirrorXaxis(self):
        for s in self.__steelItems:
            origin = s.getShape().getOrigin()
            origin.y = -origin.y

    def calProp_As(self, alphaWeight=False, weights=False):
        return self.calSteelArea(alphaWeight, weights)

    def calProp_Ac(self):
        return self.calConcreteArea()

    def calProp_Ah(self, alphaWeight=False, weights=False):
        return (
            self.__homogenization * self.calSteelArea(alphaWeight, weights)
            + self.calProp_Ac()
        )

    def calProp_Ssx(self, alphaWeight=False, weights=False):
        if weights:
            using_weights = self.__steelItemsWeights
        else:
            using_weights = len(self.__steelItemsWeights) * [1]

        if alphaWeight:
            using_alphaWeight = self.__steelItemsAlphaWeight
        else:
            using_alphaWeight = 1.0

        Sx = 0.0
        for i, s in enumerate(self.__steelItems):
            Sx = (
                Sx
                + s.getShape().getArea()
                * using_weights[i]
                * using_alphaWeight
                * s.getShape().getShapePoint("G").y
            )

        return Sx

    def calProp_Ssy(self, alphaWeight=False, weights=False):
        if weights:
            using_weights = self.__steelItemsWeights
        else:
            using_weights = len(self.__steelItemsWeights) * [1]

        if alphaWeight:
            using_alphaWeight = self.__steelItemsAlphaWeight
        else:
            using_alphaWeight = 1.0

        Sy = 0.0
        for i, s in enumerate(self.__steelItems):
            Sy = (
                Sy
                + s.getShape().getArea()
                * using_weights[i]
                * using_alphaWeight
                * s.getShape().getShapePoint("G").x
            )

        return Sy

    def calProp_Scx(self):
        Scx = (
            self.__concreteItem.getShape().getShapePoint("O").y
            * self.__concreteItem.getShape().getArea()
        )
        return Scx

    def calProp_Scy(self):
        Scy = (
            self.__concreteItem.getShape().getShapePoint("O").x
            * self.__concreteItem.getShape().getArea()
        )
        return Scy

    def calProp_Shx(self, alphaWeight=False, weights=False):
        return (
            self.calProp_Scx()
            + self.calProp_Ssx(alphaWeight, weights) * self.__homogenization
        )

    def calProp_Shy(self, alphaWeight=False, weights=False):
        return (
            self.calProp_Scy()
            + self.calProp_Ssy(alphaWeight, weights) * self.__homogenization
        )

    def calBarycenterOfSteel(self, alphaWeight=False, weights=False):
        xg = self.calProp_Ssy(alphaWeight, weights) / self.calProp_As(
            alphaWeight, weights
        )
        yg = self.calProp_Ssx(alphaWeight, weights) / self.calProp_As(
            alphaWeight, weights
        )
        return Point2d(xg, yg)

    def calBarycenterOfConcrete(self) -> Point2d:
        return self.__concreteItem.getShape().getShapePoint("G")

    def calBarycenter(self, alphaWeight=False, weights=False):

        steelg = self.calBarycenterOfSteel(alphaWeight, weights)
        steelArea = self.calSteelArea(alphaWeight, weights)
        concrg = self.calBarycenterOfConcrete()
        concrArea = self.calConcreteArea()

        xg = (steelg.x * steelArea * self.__homogenization + concrg.x * concrArea) / (
            steelArea * self.__homogenization + concrArea
        )
        yg = (steelg.y * steelArea * self.__homogenization + concrg.y * concrArea) / (
            steelArea * self.__homogenization + concrArea
        )

        return Point2d(xg, yg)

    def calProp_Isx(self, alphaWeight=False, weights=False, yg: float = 0.0):
        if weights:
            using_weights = self.__steelItemsWeights
        else:
            using_weights = len(self.__steelItemsWeights) * [1]

        if alphaWeight:
            using_alphaWeight = self.__steelItemsAlphaWeight
        else:
            using_alphaWeight = 1.0

        Isx = 0.0
        for i, s in enumerate(self.__steelItems):
            area = s.getShape().getArea() * using_weights[i] * using_alphaWeight
            y = s.getShape().getShapePoint("G").y
            Isx = Isx + area * (y - yg) * (y - yg)
        return Isx

    def calProp_Icx(self, yg: float = 0.0):
        B = self.__concreteItem.getShape().w()  # type: ignore
        H = self.__concreteItem.getShape().h()  # type: ignore
        return 1 / 12 * B * H * H * H + B * H * yg**2

    def calProp_Ihx(
        self, alphaWeight: bool = False, weights: bool = False, barycenter: bool = False
    ) -> float:
        """
        Function calculates moment of inertia along x-axis where x-axis is horizontal axis that
        goes through xhg-axis. This axis is the barycenter axis of homogeneized section
        Args:
            barycenter: if True prop will be calculated on barycentric axis
            alphaWeight: moltiplication factor for all rebars
            weights: TODO

        Returns:
            float: barycenter axis of homogeneized section
        """
        if barycenter:
            yg = self.calBarycenter().y
        else:
            yg = 0.0

        return self.__homogenization * self.calProp_Isx(
            alphaWeight, weights, yg
        ) + self.calProp_Icx(yg)

    def calProp_Isy(self, alphaWeight=False, weights=False):
        if weights:
            using_weights = self.__steelItemsWeights
        else:
            using_weights = len(self.__steelItemsWeights) * [1]

        if alphaWeight:
            using_alphaWeight = self.__steelItemsAlphaWeight
        else:
            using_alphaWeight = 1.0

        Isy = 0.0
        for i, s in enumerate(self.__steelItems):
            area = s.getShape().getArea() * using_weights[i] * using_alphaWeight
            x = s.getShape().getShapePoint("G").x
            Isy = Isy + area * x * x
        return Isy

    def calProp_Icy(self):
        B = self.__concreteItem.getShape().w()  # type: ignore
        H = self.__concreteItem.getShape().h()  # type: ignore
        return 1 / 12 * H * B * B * B

    def calProp_Ihy(self, alphaWeight=False, weights=False):
        return (
            self.__homogenization * self.calProp_Isy(alphaWeight, weights)
            + self.calProp_Icy()
        )

    def getCode(self):
        return self.__code

    def calConcreteArea(self):
        return self.__concreteItem.getShape().getArea()

    def calSteelArea(self, alphaWeight=False, weights=False):
        if weights:
            using_weights = self.__steelItemsWeights
        else:
            using_weights = len(self.__steelItemsWeights) * [1]

        if alphaWeight:
            using_alphaWeight = self.__steelItemsAlphaWeight
        else:
            using_alphaWeight = 1.0

        area = 0.0
        for i, s in enumerate(self.__steelItems):
            area = area + s.getShape().getArea() * using_weights[i] * using_alphaWeight
        return area

    def calSteelAreaMin(self, Ned=0.0):
        if self.getCode().codeStr() == "EC2":
            if self.__elementType == "beam":
                fctm = self.__concreteMaterial.get_fctm()
                fyk = self.__steelMaterial.get_fsy()
                b = self.__concreteItem.getShape().w()  # type: ignore

                if len(self.__steelItems) != 0:
                    d = self.__concreteItem.getShape().h() - self.getSteelBotRecover()  # type: ignore
                else:
                    d = self.__concreteItem.getShape().h()  # type: ignore

                asmin = max([0.26 * fctm / fyk, 0.0013 * b * d])
            elif self.__elementType == "column":
                fyd = self.__steelMaterial.get_fsy() / self.__steel_safetyFactorForULS
                Ac = self.__concreteItem.getShape().getArea()
                asmin = max([0.10 * Ned / fyd, 0.002 * Ac])
            else:
                raise Exception("Element type unknown !!!")
        else:
            raise Exception("Actually only for EC2 code !!!")
        return asmin

    def calSteelAreaMax(self):
        if self.getCode().codeStr() == "EC2":
            asmax = 0.04 * self.__concreteItem.getShape().getArea()
        else:
            raise Exception("Actually only for EC2 code !!!")
        return asmax

    def addSteelArea(self, item, weight=1.0) -> Union[int, None]:
        if not isinstance(item, StructSectionItem):
            raise Exception("Only list of [structSectionItem] !!!")
        if not (
            isinstance(item.getShape(), Shape)
            and isinstance(item.getMaterial(), materials.ConcreteSteel)
        ):
            raise Exception(
                "List item must have [Shape] and [Steel] as material assigned !!!"
            )
        self.__steelItems.append(item)
        self.__steelItemsWeights.append(weight)
        return len(self.__steelItems) - 1

    def translateSteelItems(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ):
        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()

        for s in self.__steelItems:
            s.getShape().translate(pStart, pEnd)

    def translateConcreteItem(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ):
        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()
        self.__concreteItem.getShape().translate(pStart, pEnd)

    def getSteelWeights(self):
        return self.__steelItemsWeights

    def getSteelAlphaWeight(self):
        return self.__steelItemsAlphaWeight

    def getStructConcretelItem(self):
        return self.__concreteItem

    def getStructSteelItems(self):
        return self.__steelItems

    def findLowSteelItem(self):
        vals = []
        for item in self.__steelItems:
            vals.append(item.getShape().getOrigin().y)

        # Steel not present
        if len(vals) == 0:
            return StructSectionItem(ShapeArea(0.0))
        else:
            return self.__steelItems[vals.index(min(vals))]

    def findHitSteelItem(self):
        vals = []
        for item in self.__steelItems:
            vals.append(item.getShape().getOrigin().y)

        if len(vals) == 0:
            return StructSectionItem(ShapeArea(0.0))
        else:
            return self.__steelItems[vals.index(max(vals))]

    def getConcrVertexMaxInY(self):
        return self.__concreteItem.getShape().vertexMaxInY()[1]

    def getSteelTopRecover(self) -> float:
        top = self.__concreteItem.getShape().vertexMaxInY()[1]
        bot = self.findHitSteelItem().getShape().getOrigin()
        return (top - bot).y

    def getSteelBotRecover(self) -> float:
        bot = self.__concreteItem.getShape().vertexMinInY()[1]
        top = self.findLowSteelItem().getShape().getOrigin()
        return (top - bot).y

    def getSteelMaterial(self):
        return self.__steelMaterial

    def setConcreteMaterial(self, mat, concreteMaxStress=None):
        if isinstance(mat, materials.Concrete):
            self.__concreteMaterial = mat
        else:
            raise Exception("You need get in Concrete naterial object !!!")
        if concreteMaxStress is not None:
            if isinstance(concreteMaxStress, float):
                self.__concreteMaxStress = concreteMaxStress
            else:
                raise Exception("Concrete max stress must be float type !!!")

    def getConcreteMaterial(self):
        return self.__concreteMaterial

    def setSteelMaterial(self, mat, steelMaxStress=None):
        if isinstance(mat, materials.ConcreteSteel):
            self.__steelMaterial = mat
        else:
            raise Exception("You need get in ConcreteSteel naterial object !!!")
        if steelMaxStress is not None:
            if isinstance(steelMaxStress, float):
                self.__steelMaxStress = steelMaxStress
            else:
                raise Exception("Steel max stress must be float type !!!")

    def getSteelMaxStress(self) -> float:
        return self.__steelMaxStress

    def getSteelSafetyFactorForULS(self) -> float:
        return self.__steel_safetyFactorForULS

    def getConcreteMaxStress(self) -> float:
        return self.__concreteMaxStress

    def getClsSafetyFactorForULS(self) -> float:
        return self.__cls_safetyFactorForULS

    def getUseSectionMaterials(self) -> bool:
        return self.__useSectionMaterials

    def getHomogenization(self):
        return self.__homogenization

    def setHomogenization(self, n):
        if n is not None:
            if isinstance(n, float):
                self.__homogenization = n
            else:
                raise Exception("Homogeneization must be float type !!!")

    def getN(self) -> Union[float, None]:
        return self.__N

    def getMx(self) -> Union[float, None]:
        return self.__Mx

    def getMy(self) -> Union[float, None]:
        return self.__My

    def build2dInteractionCompleteDomain(
        self, nbPoints=100, SLS=False, negative_compression=False
    ) -> Any:

        if not SLS:
            NxMz_section, Fields, Bounding = self.build2dInteractionDomain(
                nbPoints, negative_compression
            )
        else:
            NxMz_section, Fields, Bounding = self.build2dInteractionDomainSLS(
                nbPoints, negative_compression
            )

        # TODO: this need to be fixed for barycenter not (0,0)
        for si in self.__steelItems:
            si.setOriginY(-si.getOrigin().y)

        if not SLS:
            (
                NxMz_section_flipped,
                Fields_flipped,
                Bounding_flipped,
            ) = self.build2dInteractionDomain(nbPoints, negative_compression)
        else:
            (
                NxMz_section_flipped,
                Fields_flipped,
                Bounding_flipped,
            ) = self.build2dInteractionDomainSLS(nbPoints, negative_compression)

        for nm in NxMz_section_flipped:
            nm[1] = -nm[1]

        # Adjust bounding for flipped values
        M_min = -Bounding_flipped[3]
        M_max = -Bounding_flipped[2]

        Bounding_flipped[2] = M_min
        Bounding_flipped[3] = M_max

        N_min = min(Bounding[0], Bounding_flipped[0])
        N_max = max(Bounding[1], Bounding_flipped[1])
        M_min = min(Bounding[2], Bounding_flipped[2])
        M_max = max(Bounding[3], Bounding_flipped[3])

        for si in self.__steelItems:
            si.setOriginY(-si.getOrigin().y)

        NxMz_section_flipped.reverse()
        Fields_flipped.reverse()
        return (
            NxMz_section + NxMz_section_flipped[1:],
            Fields + Fields_flipped[1:],
            [N_min, N_max, M_min, M_max],
        )

    def getH(self) -> float:
        return (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )

    def getHs(self) -> float:
        return (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().getShapePoint("G").y
        )

    def getHi(self):
        return (
            self.__concreteItem.getShape().getShapePoint("G").y
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )

    def getVertexConcrAt(self, i: int) -> Point2d:
        return self.__concreteItem.getShape().vertexAt(i)

    def getVertexConcrNb(self):
        return self.__concreteItem.getShape().vertexNb()

    def getVertexSteelAt(self, i):
        return self.__steelItems[i].getShape().getOrigin()

    def getVertexSteelNb(self):
        return len(self.__steelItems)

    def build2dInteractionDomain(self, nbPoints=100, negative_compression=True):

        if not (self.__code.codeStr() == "EC2"):
            raise Exception("Implemented now only for EC2 code !!!")

        if not self.__useSectionMaterials:
            raise Exception("Implemented now only for same material on steel !!!")

        if not isinstance(self.__concreteItem.getShape(), ShapeRect):
            raise Exception("Implemented now only for rectangular section shape !!!")

        H = (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )
        c = self.getSteelBotRecover()
        Hs = (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().getShapePoint("G").y
        )
        Hi = (
            self.__concreteItem.getShape().getShapePoint("G").y
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )
        Hc = (H / self.__concreteMaterial.get_ecu()) * self.__concreteMaterial.get_ec2()

        # spazio lagrangiano con il seguente significato:
        # e1: limite acciaio di massima deformazione
        # e2: limite di sezione con calcestruzzo a rottura ed acciaio a rottura (deformazioni)
        # e3: limite di sezione con calcestruzzo decompresso
        # e4: limite di sezione con calcestruzzo tutto compresso
        e1 = self.__steelMaterial.get_esu()
        e2 = e1 + self.__concreteMaterial.get_ecu()
        ecs = e2 / (H - c) * c
        e3 = e2 + ecs + self.__steelMaterial.get_esu()
        e4 = e3 + self.__concreteMaterial.get_ec2()

        # print("H = %1.6f - c = %2.6f - e1 = %3.6f - e2 = %4.6f - e3 = %5.6f - e4 = %6.6f - ecs = %7.6f"%(H,c,e1,e2,e3,e4,ecs))
        # print("Hs = %1.6f - Hi = %2.6f"%(Hs,Hi))

        B = self.__concreteItem.getShape().w()  # type: ignore

        # Convenzioni: sforzi normali positivi se di compressione
        #              flessione positiva prodotta da sforzi normali positivi lato +y
        def sigmas(e: float, temp: float = 20.0):

            fsy = self.__steelMaterial.get_fsy()
            esu = self.__steelMaterial.get_esu()

            # gammas in case of fire
            if temp <= 20.0:
                gamma_s = self.__steelMaterial.get_gammas()
            else:
                gamma_s = self.__steelMaterial.get_gammas_fire()

            #
            # reduction resistence factor in case of fire
            #
            kappa_s = 1.0
            if temp > 20.0:
                if self.__code.codeStr() in [
                    "EC2",
                    "EC2:ITA",
                    "NTC2008",
                    "NTC2018",
                    "CIRC2008",
                    "CIRC2018",
                ]:
                    if e < -0.02:
                        if (
                            self.__steelMaterial.get_shapingType()
                            == fireCode.SteelShapingType.COLD_ROLLED
                        ):
                            kappa_s = fireCode.kappa_s(
                                temp, fireCode.SteelShapingType.COLD_ROLLED
                            )
                        elif (
                            self.__steelMaterial.get_shapingType()
                            == fireCode.SteelShapingType.HOT_ROLLED
                        ):
                            kappa_s = fireCode.kappa_s(
                                temp, fireCode.SteelShapingType.HOT_ROLLED
                            )
                    else:
                        kappa_s = fireCode.kappa_s(
                            temp, stress=fireCode.StressType.COMPRESSION
                        )
                else:
                    raise Exception(
                        f"Code {self.__code.codeStr()} has not hot options !!!"
                    )

            fsd = kappa_s * fsy / gamma_s

            Es = self.__steelMaterial.get_Es()
            esd = fsd / Es

            if e >= -esd and e <= +esd:
                sigma = -Es * e
                field = "e"
            elif e < -esd and e >= -esu:
                sigma = +fsd
                field = "y"
            elif e > esd and e <= esu:
                sigma = -fsd
                field = "y"
            else:
                raise Exception("sigmas(%1.6e) deformation value error !!!" % e)

            return sigma, field, kappa_s

        def es(s, y, e1, e2, e3, e4, H, c, Hs, Hi, Hc) -> Tuple[float, float]:

            if s >= 0.0 and s < e1:
                # print("CAMPO 1")
                es = +self.__steelMaterial.get_esu() - (s / (H - c)) * (y + Hi - c)
                return es, 1.0
            elif s >= e1 and s < e2:
                # print("CAMPO 2")
                es = +self.__steelMaterial.get_esu() - (s / (H - c)) * (y + Hi - c)
                return es, 2.0
            elif s >= e2 and s < e3:
                # print("CAMPO 3")
                s1 = e3 - s + self.__concreteMaterial.get_ecu()
                es = ((s1) / H) * (Hs - y) - self.__concreteMaterial.get_ecu()
                return es, 3.0
            elif s >= e3 and s <= e4:
                # print("CAMPO 4")
                es = -(
                    ((e4 - s) / Hc) * (y + Hi - Hc) + self.__concreteMaterial.get_ec2()
                )
                return es, 4.0
            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

        def xis(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc):
            if s >= 0.0 and s < e1:
                if s == 0.0:
                    xi = -float("Inf")
                else:
                    xi = -(((H - c) / s) * (self.__steelMaterial.get_esu() - s))
            elif s >= e1 and s < e2:
                xi = -((H - c) / s) * (self.__steelMaterial.get_esu() - s)
            elif s >= e2 and s < e3:
                s1 = e3 - s + self.__concreteMaterial.get_ecu()
                xi = (self.__concreteMaterial.get_ecu() / s1) * H
            elif s >= e3 and s <= e4:
                if s == e4:
                    xi = +float("Inf")
                else:
                    xi = ((s - e3) / (e4 - s)) * Hc + H
            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

            return xi

        def Ncs(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc, hotSection: bool = False):
            lamda = self.__concreteMaterial.get_lambda()
            eta = self.__concreteMaterial.get_eta()

            xi = xis(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc)

            if hotSection:
                gammac = self.__concreteMaterial.get_gammac_fire()
                alphacc = self.__concreteMaterial.get_alphacc_fire()
            else:
                gammac = self.__concreteMaterial.get_gammac()
                alphacc = self.__concreteMaterial.get_alphacc()

            if s >= 0.0 and s < e1:
                Ncs = 0.0
                ycs = 0.0
                return Ncs, ycs

            elif s >= e1 and s < e2:
                Ncs = (
                    lamda
                    * eta
                    * (self.__concreteMaterial.get_fck() * alphacc / gammac)
                    * xi
                )
                ycs = Hs - lamda * xi / 2
                return Ncs, ycs

            elif s >= e2 and s < e3:
                Ncs = (
                    lamda
                    * eta
                    * (self.__concreteMaterial.get_fck() * alphacc / gammac)
                    * xi
                )
                ycs = Hs - lamda * xi / 2
                return Ncs, ycs

            elif s >= e3 and s <= e4:
                if lamda * xi <= H:
                    Ncs = (
                        (self.__concreteMaterial.get_fck() * eta * alphacc / gammac)
                        * lamda
                        * xi
                    )
                    ycs = Hs - lamda * xi / 2
                else:
                    Ncs = (
                        self.__concreteMaterial.get_fck() * eta * alphacc / gammac
                    ) * H
                    ycs = Hs - H / 2
                return Ncs, ycs

            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

        linearSpace = np.linspace(0, e4, nbPoints)

        NxMz_section = []
        ArrayField = []

        N_min = 0.0
        N_max = 0.0
        M_min = 0.0
        M_max = 0.0

        if True is negative_compression:
            nc = -1.0
        else:
            nc = 1.0

        ybottom = self.findLowSteelItem().getOrigin().y
        field = -1.0
        hotSection = len(self.__steelItemsTemperatures) > 0
        self.__steelItems_kappa_s = [1.0] * len(self.__steelItemsTemperatures)
        for i_s in linearSpace:
            N_steel = 0.0
            M_steel = 0.0
            steel_yelding = True
            for idx, si in enumerate(self.__steelItems):
                y_steel = si.getOrigin().y
                Ai = si.getArea()
                e, field = es(i_s, y_steel, e1, e2, e3, e4, H, c, Hs, Hi, Hc)
                if hotSection:
                    steelValues = sigmas(e, self.__steelItemsTemperatures[idx])
                    N_steel_si = (
                        steelValues[0]
                        * Ai
                        * self.__steelItemsWeights[idx]
                        * self.__steelItemsAlphaWeight
                        * nc
                    )
                    self.__steelItems_kappa_s[idx] = steelValues[2]
                else:
                    N_steel_si = (
                        sigmas(e)[0]
                        * Ai
                        * self.__steelItemsWeights[idx]
                        * self.__steelItemsAlphaWeight
                        * nc
                    )

                if (sigmas(e)[1] == "e") and (ybottom == y_steel) and steel_yelding:
                    steel_yelding = False

                N_steel = N_steel + N_steel_si
                M_steel_si = N_steel_si * y_steel * nc
                M_steel = M_steel + M_steel_si

            if len(self.__steelItemsTemperatures) > 0:
                N_concrete = (
                    Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc, True)[0] * B * nc
                )
                y_concrete = Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc, True)[1]
            else:
                N_concrete = (
                    Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc, False)[0] * B * nc
                )
                y_concrete = Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc, False)[1]

            M_concrete = N_concrete * y_concrete * nc

            N_tot = N_concrete + N_steel
            M_tot = M_concrete + M_steel

            if N_tot < N_min:
                N_min = N_tot
            if N_tot > N_max:
                N_max = N_tot
            if M_tot < M_min:
                M_min = M_tot
            if M_tot > M_max:
                M_max = M_tot

            # remove duplicates
            if len(NxMz_section) >= 1:
                if (
                    NxMz_section[len(NxMz_section) - 1][0] != N_tot
                    and NxMz_section[len(NxMz_section) - 1][1] != M_tot
                ):
                    NxMz_section.append([N_tot, M_tot])
                    # ArrayField.append(field)
                    if not steel_yelding:
                        ArrayField.append(field + 10)
                    else:
                        ArrayField.append(field)
            else:
                NxMz_section.append([N_tot, M_tot])
                # ArrayField.append(field)
                if not steel_yelding:
                    ArrayField.append(field + 10)
                else:
                    ArrayField.append(field)

        return NxMz_section, ArrayField, [N_min, N_max, M_min, M_max]

    def build2dInteractionDomainSLS(self, nbPoints=100, negative_compression=False):

        if not (self.__code.codeStr() == "EC2"):
            raise Exception("Implemented now only for EC2 code !!!")

        if not self.__useSectionMaterials:
            raise Exception("Implemented now only for same material on steel !!!")

        if not isinstance(self.__concreteItem.getShape(), ShapeRect):
            raise Exception("Implemented now only for rectangular section shape !!!")

        es_max = self.__steelMaterial.get_sigmas_max_c() / self.__steelMaterial.get_Es()
        ec_max = (
            self.__concreteMaterial.get_sigmac_max_c()
            / self.__steelMaterial.get_Es()
            * self.__homogenization
        )

        H = (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )
        c = self.getSteelBotRecover()

        e1 = es_max
        e2 = ec_max + es_max
        ecs = (es_max + ec_max) / (H - c) * c
        e3 = ecs + 2 * es_max + ec_max
        e4 = ecs + 2 * (ec_max + es_max)

        Hs = (
            self.__concreteItem.getShape().vertexMaxInY()[0]
            - self.__concreteItem.getShape().getShapePoint("G").y
        )
        Hi = (
            self.__concreteItem.getShape().getShapePoint("G").y
            - self.__concreteItem.getShape().vertexMinInY()[0]
        )
        Hc = (H / self.__concreteMaterial.get_ecu()) * self.__concreteMaterial.get_ec2()

        B = self.__concreteItem.getShape().w()  # type: ignore

        # Convenzioni: sforzi normali positivi se di compressione
        #              flessione positiva prodotta da sforzi normali positivi lato +y
        def sigmas(e):

            Es = self.__steelMaterial.get_Es()
            sigma = +Es * e
            return sigma, "e"

        def es(s, y, e1, e2, e3, e4, H, c, Hs, Hi, Hc):
            di = Hi - c
            d = H - c
            if s >= 0.0 and s < e1:
                # print("CAMPO 1")
                es = es_max - (y + di) * s / d
                return -es, 1.0
            elif s >= e1 and s < e2:
                # print("CAMPO 2")
                es = +es_max - (y + di) * s / d
                return -es, 2.0
            elif s >= e2 and s < e3:
                # print("CAMPO 3")
                s1 = e4 - s
                es = +ec_max - s1 / H * (Hs - y)
                return es, 3.0
            elif s >= e3 and s <= e4:
                # print("CAMPO 4")
                s1 = e4 - s
                es = ec_max - s1 / H * (Hs - y)
                return es, 4.0
            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

        def xis(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc):

            d = H - c
            s1 = e4 - s
            if s >= 0.0 and s < e1:
                if s == 0.0:
                    xi = -float("Inf")
                else:
                    xi = -d * (es_max / s - 1)
            elif s >= e1 and s < e2:
                xi = (s - es_max) / s * d
            elif s >= e2 and s < e3:
                xi = H / s1 * ec_max
            elif s >= e3 and s <= e4:
                if s == e4:  # print("CAMPO 4")self.__concreteMaterial.get_ecu()
                    xi = +float("Inf")
                else:
                    xi = H / s1 * ec_max
            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

            # print("xi = %1.3f"%xi)
            return xi

        def Ncs(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc):

            Es = self.__steelMaterial.get_Es()
            xi = xis(s, e1, e2, e3, e4, H, c, Hs, Hi, Hc)
            n = self.__homogenization
            s1 = e4 - s

            if s >= 0.0 and s < e1:
                Ncs = 0.0
                ycs = 0.0
                return Ncs, ycs

            elif s >= e1 and s < e2:
                Ncs = xi / 2 * Es / n * (s - es_max)
                ycs = Hs - xi / 3
                return Ncs, ycs

            elif s >= e2 and s < e3:
                Ncs = xi / 2 * self.__concreteMaterial.get_sigmac_max_c()
                ycs = Hs - xi / 3
                return Ncs, ycs

            elif s >= e3 and s <= e4:
                Ncs = (
                    (2 * self.__concreteMaterial.get_sigmac_max_c() - s1 * Es / n)
                    * H
                    / 2
                )
                ycs = H * (3 * ec_max - s1) / (3 * (2 * ec_max - s1)) - Hi

                return Ncs, ycs
            else:
                raise Exception(
                    "The value of s is <%1.4f> out of range [%2.6f,%3.6f]!!!"
                    % (s, 0, e4)
                )

        linearSpace = np.linspace(0, e4, nbPoints)

        NxMz_section = []
        ArrayField = []

        N_min = 0.0
        N_max = 0.0
        M_min = 0.0
        M_max = 0.0

        ybottom = self.findLowSteelItem().getOrigin().y

        if True is negative_compression:
            nc = -1.0
        else:
            nc = 1.0

        for i_s in linearSpace:
            N_steel = 0.0
            M_steel = 0.0
            steel_yelding = True
            field = -1.0
            for idx, si in enumerate(self.__steelItems):
                y_steel = si.getOrigin().y
                Ai = si.getArea()
                e, field = es(i_s, y_steel, e1, e2, e3, e4, H, c, Hs, Hi, Hc)
                N_steel_si = (
                    sigmas(e)[0]
                    * Ai
                    * self.__steelItemsWeights[idx]
                    * self.__steelItemsAlphaWeight
                    * nc
                )

                if (sigmas(e)[1] == "e") and (ybottom == y_steel) and steel_yelding:
                    steel_yelding = False

                N_steel = (N_steel + N_steel_si) * nc
                M_steel_si = N_steel_si * y_steel * nc
                M_steel = M_steel + M_steel_si

            N_concrete = Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc)[0] * B * nc
            y_concrete = Ncs(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc)[1]

            # Additional parameter for benchmark
            sigma_concrete = (
                -es(i_s, Hs, e1, e2, e3, e4, H, c, Hs, Hi, Hc)[0]
                * self.__steelMaterial.get_Es()
                / self.__homogenization
            )
            y_steel_miny = self.findLowSteelItem().getShape().getOrigin().y
            sigma_steel = (
                -es(i_s, y_steel_miny, e1, e2, e3, e4, H, c, Hs, Hi, Hc)[0]
                * self.__steelMaterial.get_Es()
            )
            xi = xis(i_s, e1, e2, e3, e4, H, c, Hs, Hi, Hc)

            M_concrete = N_concrete * y_concrete * nc

            N_tot = N_concrete + N_steel
            M_tot = M_concrete + M_steel

            if N_tot < N_min:
                N_min = N_tot
            if N_tot > N_max:
                N_max = N_tot
            if M_tot < M_min:
                M_min = M_tot
            if M_tot > M_max:
                M_max = M_tot

            # remove duplicates
            if len(NxMz_section) >= 1:
                if (
                    NxMz_section[len(NxMz_section) - 1][0] != N_tot
                    and NxMz_section[len(NxMz_section) - 1][1] != M_tot
                ):
                    NxMz_section.append(
                        [
                            N_tot,
                            M_tot,
                            N_concrete,
                            M_concrete,
                            y_concrete,
                            sigma_concrete,
                            sigma_steel,
                            xi,
                        ]
                    )
                    # ArrayField.append(field)
                    if not steel_yelding:
                        ArrayField.append(field + 10)
                    else:
                        ArrayField.append(field)
            else:
                NxMz_section.append(
                    [
                        N_tot,
                        M_tot,
                        N_concrete,
                        M_concrete,
                        y_concrete,
                        sigma_concrete,
                        sigma_steel,
                        xi,
                    ]
                )
                # ArrayField.append(field)
                if not steel_yelding:
                    ArrayField.append(field + 10)
                else:
                    ArrayField.append(field)

        return NxMz_section, ArrayField, [N_min, N_max, M_min, M_max]

    def setStirrupt(
        self,
        area: Union[float, int, None] = None,
        dist: Union[float, int, None] = None,
        angle: Union[float, int, None] = None,
    ):

        # def setStirrupt(self, area = None, dist = None, angle = None):
        if area is not None:
            self.__steelStirruptArea = area
        if dist is not None:
            self.__steelStirruptDist = dist
        if angle is not None:
            self.__steelStirruptAngle = angle

    def getStirruptArea(self) -> Union[float, int, None]:
        return self.__steelStirruptArea

    def getStirruptAngle(self) -> Union[float, int, None]:
        return self.__steelStirruptAngle

    def getStirruptDistance(self) -> Union[float, int, None]:
        return self.__steelStirruptDist

    def __str__(self):
        dispstr = "ConcreteSection Object: \n"
        dispstr = dispstr + "-----------------------  \n"
        dispstr = dispstr + "  Ids = " + str(self.__ids) + "\n"
        dispstr = dispstr + "Descr = " + str(self.__descr) + "\n"
        dispstr = (
            dispstr
            + "Steel safety factor for    ULS = "
            + str(self.__steel_safetyFactorForULS)
            + "\n"
        )
        dispstr = (
            dispstr
            + "Concrete safety factor for ULS = "
            + str(self.__cls_safetyFactorForULS)
            + "\n"
        )
        dispstr = (
            dispstr
            + "Concrete Max Stress for    ELS = "
            + str(self.__concreteMaterial.get_sigmac_max_c())
            + "\n"
        )
        dispstr = (
            dispstr
            + "Steel Max Stress for       ELS = "
            + str(self.__steelMaterial.get_sigmas_max_c())
            + "\n"
        )
        dispstr = (
            dispstr
            + "Homogeneization for        ELS = "
            + str(self.__homogenization)
            + "\n"
        )
        dispstr = dispstr + "---------------------\n"
        dispstr = dispstr + "Materials embedded-->\n"
        dispstr = dispstr + "---------------------\n"
        dispstr = dispstr + str(self.__concreteMaterial).replace("\n", "\n  | ")
        dispstr = dispstr + str(self.__steelMaterial).replace("\n", "\n  | ")
        dispstr = dispstr + "-----------------\n"
        dispstr = dispstr + "Items embedded-->\n"
        dispstr = dispstr + "-----------------\n"
        if self.__concreteItem is not None:
            dispstr = dispstr + str(self.__concreteItem).replace("\n", "\n  | ")
        else:
            dispstr = dispstr + "Steel without concrete :-)\n"

        if self.__steelItems is not None:
            for i in self.__steelItems:
                dispstr = dispstr + str(i).replace("\n", "\n  | ")
        else:
            dispstr = dispstr + "Without steel :-)"
        return dispstr


class ConcreteSectionModel(BaseModel):
    descr: str = ""
    id: int = -1
    shape: RectangularShape
    concreteMat: ConcreteModel
    steelMat: SteelModel
    disposerOnLine: Optional[List[SteelDisposerOnLine]] = None
    disposerSingle: Optional[List[SteelDisposerSingle]] = None
    stirrup: Optional[SteelDisposerStirrup] = None
    stirrupSingleLeg: Optional[List[SteelDisposerStirrupSingleLeg]] = None
