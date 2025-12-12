"""
Created on Thu Avr 27 09:28:00 2019

@author: lpaone
"""
import math
from enum import Enum
from typing import Any, List, Literal, Tuple, Union

from pycivil.EXAGeometry.clouds import PointCloud2d
from pycivil.EXAGeometry.geometry import Point2d
from pycivil.EXAGeometry.shapes import ShapeArea, ShapeRect
from pycivil.EXAStructural.codes import Code
from pycivil.EXAStructural.materials import Concrete, ConcreteSteel
from pycivil.EXAStructural.plot import interactionDomainBasePlot2d
from pycivil.EXAStructural.sections import (
    ConcreteSection,
    SectionStates,
    StructSectionItem,
)
from pycivil.EXAUtils import logging as logger


class SectionCrackedStates(str, Enum):
    UNKNOWN = "UNKNOWN"
    COMPRESSED = "COMPRESSED"
    DECOMPRESSED = "DECOMPRESSED"
    CRACKED = "CRACKED"
    CRACKED_TOP = "CRACKED_TOP"
    CRACKED_BOT = "CRACKED_BOT"

    def toStr(self) -> Union[str, None]:
        if self == SectionCrackedStates.UNKNOWN:
            return "unknown"
        if self == SectionCrackedStates.COMPRESSED:
            return "compr."
        if self == SectionCrackedStates.DECOMPRESSED:
            return "decompr."
        if self == SectionCrackedStates.CRACKED:
            return "cracked"
        if self == SectionCrackedStates.CRACKED_TOP:
            return "crack top"
        if self == SectionCrackedStates.CRACKED_BOT:
            return "crack bot"


class CrackParameters:
    def __init__(self):
        self.__epsi = None
        self.__xi = None
        self.__hcEff = None
        self.__steelArea = None
        self.__dgs = None
        self.__deq = None
        self.__sigmasMax = None
        self.__rebarsInterDistance = None
        self.__rebarsCover = None
        self.__rebarsInAeff = None
        self.__crackState = SectionCrackedStates.UNKNOWN

    @property
    def crackState(self):
        return self.__crackState

    @crackState.setter
    def crackState(self, value):
        self.__crackState = value

    def __str__(self):
        dispstr = f"__xi                = {self.__xi}\n"
        dispstr += f"__epsi                = {self.__epsi}\n"
        dispstr += f"__hcEff               = {self.__hcEff}\n"
        dispstr += f"__steelArea           = {self.__steelArea}\n"
        dispstr += f"__dgs                 = {self.__dgs}\n"
        dispstr += f"__deq                 = {self.__deq}\n"
        dispstr += f"__sigmasMax           = {self.__sigmasMax}\n"
        dispstr += f"__rebarsInterDistance = {self.__rebarsInterDistance}\n"
        dispstr += f"__rebarsCover         = {self.__rebarsCover}\n"
        dispstr += f"__crackState          = {self.__crackState}\n"
        return dispstr

    def toDict(self) -> dict:
        return {
            "xi": self.__xi,
            "epsi": self.__epsi,
            "hcEff": self.__hcEff,
            "steelArea": self.__steelArea,
            "dgs": self.__dgs,
            "deq": self.__deq,
            "sigmasMax": self.__sigmasMax,
            "rebarsInterDistance": self.__rebarsInterDistance,
            "rebarsCover": self.__rebarsCover,
            "crackState": self.__crackState,
        }

    @property
    def xi(self):
        return self.__xi

    @xi.setter
    def xi(self, val: float):
        self.__xi = val

    @property
    def rebarsInAeff(self):
        return self.__rebarsInAeff

    @rebarsInAeff.setter
    def rebarsInAeff(self, val: list[StructSectionItem]):
        self.__rebarsInAeff = val

    @property
    def epsi(self):
        return self.__epsi

    @epsi.setter
    def epsi(self, val: float):
        self.__epsi = val

    @property
    def hcEff(self):
        return self.__hcEff

    @hcEff.setter
    def hcEff(self, val: float):
        self.__hcEff = val

    @property
    def steelArea(self):
        return self.__steelArea

    @steelArea.setter
    def steelArea(self, val: float):
        self.__steelArea = val

    @property
    def dgs(self):
        return self.__dgs

    @dgs.setter
    def dgs(self, val: float):
        self.__dgs = val

    @property
    def deq(self):
        return self.__deq

    @deq.setter
    def deq(self, val: float):
        self.__deq = val

    @property
    def sigmasMax(self):
        return self.__sigmasMax

    @sigmasMax.setter
    def sigmasMax(self, val: float):
        self.__sigmasMax = val

    @property
    def rebarDistance(self):
        return self.__rebarsInterDistance

    @rebarDistance.setter
    def rebarDistance(self, val: float):
        self.__rebarsInterDistance = val

    @property
    def coverInMaxSteel(self):
        return self.__rebarsCover

    @coverInMaxSteel.setter
    def coverInMaxSteel(self, val: float):
        self.__rebarsCover = val


class RCTemplRectEC2(ConcreteSection):
    def __init__(self, ids: int = 0, descr: str = ""):

        super().__init__(ids, descr)
        self.__ll: Literal[0, 1, 2, 3] = 1
        # ------------------------
        # Crack measure parameters
        # ------------------------
        self.__crack_bot = CrackParameters()
        self.__crack_top = CrackParameters()
        self.__crack_state = SectionCrackedStates.UNKNOWN

        logger.log(tp="INF", level=1, msg="Setting code default *EC2*")
        code = Code("EC2")
        self.setCode(code)

        logger.log(tp="INF", level=1, msg="Setting concrete default *C32/40*")
        cls_material = Concrete(descr="Concrete EC2 for template")
        cls_material.setByCode(code, "C32/40")
        self.setConcreteMaterial(cls_material)

        logger.log(tp="INF", level=1, msg="Setting steel default *B450C*")
        steel_material = ConcreteSteel(descr="Steel EC2 for template")
        steel_material.setByCode(code, "B450C")
        self.setSteelMaterial(steel_material)

        rect_shape = ShapeRect()
        rectangularSection = StructSectionItem(rect_shape, cls_material)
        self.setStructConcrItem(rectangularSection)

        # New starting from structural section.countSteel()
        self.__tensionPoints2d = []
        self.__currentTensionPoint2dIdx = -1
        self.__domainPoints2d = []  # ultimate domain
        self.__domainPointsHot = []  # ultimate domain
        self.__domainBounding = []  # ultimate domain
        self.__currentDomain2dIdx = -1
        self.__domainFieldsPoints2d = []  # ultimate domain field

        # Param for plot2D interaction domain
        self.__plot2dInteraction_xLabel = "Nz [KN]"
        self.__plot2dInteraction_yLabel = "Mz [KNm]"
        self.__plot2dInteraction_titleAddStr = None
        self.__plot2dInteraction_scale_Nx = 0.001
        self.__plot2dInteraction_scale_Mz = 0.000001

        self.__plot2dInteraction_nbPoints = 100

        # neutral axis
        self.__xi = None

        # Solver sls for NM. Properties.
        #
        # Error on iteration debalancing
        self.__errorOnTorque = None
        self.__errorOnForce = None
        self.__uncracked = False
        self.__sls_state = SectionStates.UNKNOWN

    # xi is value of coordinate along y-axis (from top to bottom directed)
    #
    def xi(self) -> Union[float, None]:
        return self.__xi

    def crackState(self):
        return self.__crack_state

    def crackParam(self) -> Tuple[CrackParameters, CrackParameters]:
        r"""
        It gets crack parameters that will be assigned after launch
        solverCrack() function

        Returns:
            A Tuple[CrackParameters, CrackParameters]. At index 0 will be
             returned bottom crack parameters. At index 1 will be returned
             top crack parameters.
        """
        return self.__crack_bot, self.__crack_top

    def __rebarsInAeff(
        self, rebars: List[StructSectionItem]
    ) -> Tuple[float, float, List[StructSectionItem], float, float]:
        """

        Args:
            rebars (List[StructSectionItem]): list of rebars with stress > 0

        Returns:
            A Tuple that containts
             - heff (float):
             - dsg (float):
             - inAeff (List[StructSectionItem]):
             - As (float)
        """
        if self.__sls_state == SectionStates.UNKNOWN:
            print("WRN: Solver uncracked didn't run yet !!!")
            return 0.0, 0.0, [], 0.0, 0.0

        if self.__crack_state == SectionCrackedStates.UNKNOWN:
            print("WRN: Solver uncracked didn't run yet !!!")
            return 0.0, 0.0, [], 0.0, 0.0

        crackedCondition = [
            SectionCrackedStates.CRACKED_BOT,
            SectionCrackedStates.CRACKED_TOP,
            SectionCrackedStates.CRACKED,
        ]
        if self.__crack_state not in crackedCondition:
            print("WRN: Section not cracked !!!")
            return 0.0, 0.0, [], 0.0, 0.0

        # ------------------------
        # Find barycenter of steel
        # ------------------------
        yiAs: float = 0.0
        AsTot: float = 0.0
        for _i, v in enumerate(rebars):
            yiAs += v.getOrigin().y * v.getArea()
            AsTot += v.getArea()
        ysg = yiAs / AsTot

        # ---------
        # Find heff
        # ---------
        y_inf_limit = 0.0
        y_sup_limit = 0.0
        heff = 0.0
        dsg = 0.0
        xi = 0.0
        if self.__crack_state == SectionCrackedStates.CRACKED_BOT:
            dsg = math.pow(math.pow(self.getVertexConcrAt(3).y - ysg, 2), 1 / 2)
            xi = self.__xi
            heff = min(
                2.5 * (self.getDimH() - dsg),
                (self.getDimH() - xi) / 3,
                self.getDimH() / 2,
            )
            y_inf_limit = self.getVertexConcrAt(0).y
            y_sup_limit = self.getVertexConcrAt(0).y + heff
        if self.__crack_state == SectionCrackedStates.CRACKED_TOP:
            dsg = math.pow(math.pow(self.getVertexConcrAt(0).y - ysg, 2), 1 / 2)
            xi = self.getDimH() - self.__xi
            heff = min(
                2.5 * (self.getDimH() - dsg),
                (self.getDimH() - xi) / 3,
                self.getDimH() / 2,
            )
            y_inf_limit = self.getVertexConcrAt(3).y - heff
            y_sup_limit = self.getVertexConcrAt(3).y
        if self.__crack_state == SectionCrackedStates.CRACKED:
            xi = self.__xi
            if ysg > 0.0:
                dsg = math.pow(math.pow(self.getVertexConcrAt(0).y - ysg, 2), 1 / 2)
                heff = min(2.5 * (self.getDimH() - dsg), self.getDimH() / 2)
                y_inf_limit = self.getVertexConcrAt(3).y - heff
                y_sup_limit = self.getVertexConcrAt(3).y
            else:
                dsg = math.pow(math.pow(self.getVertexConcrAt(3).y - ysg, 2), 1 / 2)
                heff = min(2.5 * (self.getDimH() - dsg), self.getDimH() / 2)
                y_inf_limit = self.getVertexConcrAt(0).y
                y_sup_limit = self.getVertexConcrAt(0).y + heff

        inAeff = []
        As = 0.0

        for _ii, v in enumerate(rebars):
            if y_inf_limit <= v.getOrigin().y <= y_sup_limit:
                inAeff.append(v)
                As += v.getArea()

        return heff, dsg, inAeff, As, xi

    def __rebarEquivalent(self, rebars: List[StructSectionItem]) -> float:
        """

        Args:
            rebars:

        Returns:
            Equivalent diameters (float) of rebars gived.
        """
        diams = []
        diamsNb = []
        for i, _r in enumerate(rebars):
            if self.getSteelDiamAt(i) not in diams:
                diams.append(self.getSteelDiamAt(i))
                diamsNb.append(1)
            else:
                diamsNb[diams.index(self.getSteelDiamAt(i))] += 1

        # Equivalent diameter
        nD = 0
        nD2 = 0
        for i, _d in enumerate(diams):
            nD2 += diamsNb[i] * diams[i] * diams[i]
            nD += diamsNb[i] * diams[i]
        return nD2 / nD

    def __rebarDistances(self, rebars: List[StructSectionItem]) -> Tuple[float, float]:
        """

        Args:
            rebars:

        Returns:
            A Tuple that containts cover (float) and interdistance (float)
        """
        cover = max(self.getDimH(), self.getDimW())
        vertexBL = self.getVertexConcrAt(0)
        vertexTR = self.getVertexConcrAt(3)
        rebarIndex = -1
        for i, r in enumerate(rebars):
            d1 = (r.getOrigin().y - r.getDiameter() / 2) - vertexBL.y
            d2 = vertexTR.y - (r.getOrigin().y + r.getDiameter() / 2)
            d3 = (r.getOrigin().x - r.getDiameter() / 2) - vertexBL.x
            d4 = vertexTR.x - (r.getOrigin().x + r.getDiameter() / 2)
            _cover = min(d1, d2, d3, d4)
            if cover > _cover:
                rebarIndex = i
                cover = _cover
        if rebarIndex == -1:
            print("WRN: Some error occurred in cover measure !!!")
            return 0.0, 0.0

        # Find aligned rebars in x-direction
        #
        yUpper = rebars[rebarIndex].getOrigin().y + rebars[rebarIndex].getDiameter() / 2
        yLower = rebars[rebarIndex].getOrigin().y - rebars[rebarIndex].getDiameter() / 2

        rebarsAligned = []
        rebarsXPos = []
        for r in rebars:
            if yLower <= r.getOrigin().y <= yUpper:
                rebarsAligned.append(r)
                rebarsXPos.append(r.getOrigin().x)

        # With aligning condition above there isn't equal XPos then we can find
        # index among rebars aftr sort() function

        rebarsAligned.sort(key=lambda rebar: rebar.getOrigin().x)

        distance = 0.0
        for i in range(0, len(rebarsAligned) - 1):
            r_left = rebarsAligned[i].getOrigin().x + rebarsAligned[i].getDiameter() / 2
            r_right = (
                rebarsAligned[i + 1].getOrigin().x
                - rebarsAligned[i + 1].getDiameter() / 2
            )
            distance = max(distance, r_right - r_left)

        return cover, distance

    def solverCrack(self, N: float, M: float):

        # First solve section as uncracked
        logger.log(tp="INF", level=self.__ll, msg="Solve uncracked section first ...")
        self.solverSLS_NM(N, M, uncracked=True)

        # Totally compressed
        if max(self.getConcrStress()) <= 0:
            logger.log(
                tp="INF", level=self.__ll, msg="section totally compressed ... quit !!!"
            )
            self.__crack_state = SectionCrackedStates.COMPRESSED
            return

        if max(self.getConcrStress()) <= self.getConcreteMaterial().get_fct_crack():
            logger.log(
                tp="INF", level=self.__ll, msg="section totally decompressed !!!"
            )
            self.__crack_state = SectionCrackedStates.DECOMPRESSED
            return

        condition_bot_cracked = self.getConcrStress()[0] > 0.0
        condition_top_cracked = self.getConcrStress()[2] > 0.0

        # For rebars in tension we need to have real position of neutral axis
        self.solverSLS_NM(N, M, uncracked=False)

        def _assignCracked(
            crackParam: CrackParameters,
            rebars: List[StructSectionItem],
            sigmasMax: float,
        ):
            rebarsInAeff = self.__rebarsInAeff(rebars)
            crackParam.xi = self.__xi
            crackParam.hcEff = rebarsInAeff[0]
            crackParam.steelArea = rebarsInAeff[3]
            crackParam.dgs = rebarsInAeff[1]
            crackParam.deq = self.__rebarEquivalent(rebarsInAeff[2])
            crackParam.sigmasMax = sigmasMax
            crackParam.rebarsInAeff = rebarsInAeff[2]
            (
                crackParam.coverInMaxSteel,
                crackParam.rebarDistance,
            ) = self.__rebarDistances(rebarsInAeff[2])

        # If section is totally stretched we divide section in two zones using
        # half height
        if condition_top_cracked and condition_bot_cracked:
            logger.log(
                tp="INF", level=self.__ll, msg="Top and Bot of section are cracked!!!"
            )
            self.__crack_state = SectionCrackedStates.CRACKED
            rebarsOnTop = []
            rebarsOnBot = []
            sigmasMaxOnTop = 0.0
            sigmasMaxOnBot = 0.0
            for idx, rebar in enumerate(self.getSteelRebar()):
                if rebar.getOrigin().y > self.calBarycenterOfConcrete().y:
                    rebarsOnTop.append(rebar)
                    if self.getSteelStress()[idx] > sigmasMaxOnTop:
                        sigmasMaxOnTop = self.getSteelStress()[idx]
                else:
                    rebarsOnBot.append(rebar)
                    if self.getSteelStress()[idx] > sigmasMaxOnBot:
                        sigmasMaxOnBot = self.getSteelStress()[idx]
            logger.log(tp="INF", level=self.__ll, msg="... solve cracked section ...")
            _assignCracked(self.__crack_top, rebarsOnTop, sigmasMaxOnTop)
            _assignCracked(self.__crack_bot, rebarsOnBot, sigmasMaxOnBot)

        # If section is partialized we divide section in one zone using
        # stretched zone
        if condition_bot_cracked and not condition_top_cracked:
            logger.log(
                tp="INF", level=self.__ll, msg="Bottom of section is cracked !!!"
            )
            self.__crack_state = SectionCrackedStates.CRACKED_BOT
            rebarsOnBot = []
            sigmasMaxOnBot = 0.0
            for idx, rebar in enumerate(self.getSteelRebar()):
                if self.getSteelStress()[idx] > 0.0:
                    rebarsOnBot.append(rebar)
                    if self.getSteelStress()[idx] > sigmasMaxOnBot:
                        sigmasMaxOnBot = self.getSteelStress()[idx]
            logger.log(tp="INF", level=self.__ll, msg="... solve cracked section ...")
            _assignCracked(self.__crack_bot, rebarsOnBot, sigmasMaxOnBot)

        # If section is partialized we divide section in one zone using
        # stretched zone
        if condition_top_cracked and not condition_bot_cracked:
            logger.log(tp="INF", level=self.__ll, msg="Top of section is cracked!!!")
            self.__crack_state = SectionCrackedStates.CRACKED_TOP
            rebarsOnTop = []
            sigmasMaxOnTop = 0.0
            for idx, rebar in enumerate(self.getSteelRebar()):
                if self.getSteelStress()[idx] > 0.0:
                    rebarsOnTop.append(rebar)
                    if self.getSteelStress()[idx] > sigmasMaxOnTop:
                        sigmasMaxOnTop = self.getSteelStress()[idx]
            logger.log(tp="INF", level=self.__ll, msg="... solve cracked section ...")
            _assignCracked(self.__crack_top, rebarsOnTop, sigmasMaxOnTop)

        # Bot deformation retived from BL concrete deformation
        self.__crack_bot.epsi = self.getConcrDeform()[0]
        # Top deformation retived from TL concrete deformation
        self.__crack_top.epsi = self.getConcrDeform()[2]

    def setDimH(self, h: float) -> None:
        r"""
        Set dimension height in [mm] for section rectangular

        Args:
            h (float): height in [mm]
        """
        if isinstance(h, (float, int)):
            self.getStructConcretelItem().getShape().setDimH(h)  # type: ignore
        else:
            raise Exception("Only one float for h!!!")

    def setDimW(self, w):
        r"""
        Set dimension width in [mm] for section rectangular

        Args:
            w (float): width in [mm]
        """
        if isinstance(w, (float, int)):
            self.getStructConcretelItem().getShape().setDimW(w)  # type: ignore
        else:
            raise Exception("Only one float for w !!!")

    def getDimH(self) -> float:
        return self.getStructConcretelItem().getShape().h()  # type: ignore

    def getDimW(self) -> float:
        return self.getStructConcretelItem().getShape().w()  # type: ignore

    def assignSteelAreaWithAlphaWeight(self, areas):
        """
        Assegna area totale d'acciaio distribuendola sulle armature in modo
        che l'area totale corrisponda ad <areas>.
        Non vengono considerati i pesi
        """
        factor = areas / self.calSteelArea()
        self.setSteelAlphaWeight(factor)

    def addSteelArea(
        self,
        posStr: str,
        dist: float = 0.0,
        area: float = 0.0,
        x: float = 0.0,
        y: float = 0.0,
        d: float = 0.0,
        nb: float = 0.0,
        sd: float = 0.0,
        idSteel: int = 0,
    ) -> Union[int, list[int], None]:

        if isinstance(posStr, str) is not True:
            raise Exception("First arg must be a str type !!!")

        shape = self.getStructConcretelItem().getShape()
        if ("MB" == posStr) or ("MT" == posStr):

            if isinstance(dist, float) is not True:
                raise Exception("Second arg must be a float type !!!")

            if isinstance(area, float) is not True:
                raise Exception("Third arg must be a float type !!!")

            assert isinstance(dist, float)
            if posStr == "MB":
                MB = shape.getShapePoint("MB")
                steel_area = ShapeArea(area)
                steel_area.setOrigin(MB + Point2d(0, dist))
                steel_item = StructSectionItem(steel_area, self.getSteelMaterial())
                # self.getStructSteelItems().append(steel_item)
                super().addSteelArea(steel_item)
                return len(super().getStructSteelItems()) - 1

            elif posStr == "MT":
                MT = shape.getShapePoint("MT")
                steel_area = ShapeArea(area)
                steel_area.setOrigin(MT + Point2d(0, -dist))
                steel_item = StructSectionItem(steel_area, self.getSteelMaterial())
                # self.getStructSteelItems().append(steel_item)
                super().addSteelArea(steel_item)
                return len(super().getStructSteelItems()) - 1

        elif "XY" == posStr:
            if not isinstance(area, float):
                raise Exception("area arg must be a float type !!!")
            if not isinstance(x, float):
                raise Exception("x arg must be a float type !!!")
            if not isinstance(y, float):
                raise Exception("y arg must be a float type !!!")

            steel_area = ShapeArea(area)
            steel_area.setOrigin(Point2d(x, y))
            steel_item = StructSectionItem(steel_area, self.getSteelMaterial())
            steel_item.setId(idSteel)
            super().addSteelArea(steel_item)
            return len(super().getStructSteelItems()) - 1

        elif ("LINE-MB" == posStr) or ("LINE-MT" == posStr):
            if not isinstance(dist, (float, int)):
                raise Exception("Second arg must be a float type !!!")
            if not isinstance(d, (float, int)):
                raise Exception("d arg must be a float or int type !!!")
            if not isinstance(nb, int):
                raise Exception("nb arg must be a int type !!!")
            if nb < 2:
                raise Exception(
                    "nb arg must be greater than one !!! Use single method for disposing area."
                )
            if not isinstance(sd, (float, int)):
                raise Exception("sd arg must be a float or int type !!!")

            shape = self.getStructConcretelItem().getShape()

            # P0 is points origin for copies starting from left to right
            if "LINE-MB" == posStr:
                P0 = shape.getShapePoint("MB")
            else:
                P0 = shape.getShapePoint("MT")
                dist = -1 * dist

            indexOfSteel = []
            for i in range(nb):
                steel_area = ShapeArea(math.pi * d * d / 4)
                xCoord = -((nb - 1) * sd) / 2 + sd * i
                steel_area.setOrigin(P0 + Point2d(xCoord, dist))
                steel_item = StructSectionItem(steel_area, self.getSteelMaterial())
                super().addSteelArea(steel_item)
                indexOfSteel.append(len(super().getStructSteelItems()) - 1)
            return indexOfSteel

        else:
            raise Exception("posStr arg unknown type !!!")

    def getSteelAt(self, i):
        return self.getStructSteelItems()[i]

    def getSteelAreaAt(self, i, alphaWeight=False, weights=False):
        return super().getSteelAreaAt(i, alphaWeight, weights)

    def getSteelXAt(self, i):
        return self.getStructSteelItems()[i].getOrigin().x

    def getSteelYAt(self, i):
        return self.getStructSteelItems()[i].getOrigin().y

    def getSteelItemNumber(self):
        return len(self.getStructSteelItems())

    def setMaterials(
        self,
        concreteStr="C20/25",
        steelStr="B450C",
        concreteMaxStress=None,
        steelMaxStress=None,
        homogenization=None,
    ):
        cls_material = Concrete(descr="Concrete EC2 for template")
        cls_material.setByCode(self.getCode(), concreteStr)
        self.setConcreteMaterial(cls_material, concreteMaxStress=concreteMaxStress)

        steel_material = ConcreteSteel(descr="Steel EC2 for template")
        steel_material.setByCode(self.getCode(), steelStr)
        self.setSteelMaterial(steel_material, steelMaxStress=steelMaxStress)

        self.setHomogenization(homogenization)

    def getMaterialConcr(self):
        return super().getConcreteMaterial()

    def getMaterialSteel(self):
        return super().getSteelMaterial()

    def clearTensionPoints(self):
        self.__tensionPoints2d.clear()

    def addTensionPoint2d(self, N: float, M: float):
        if isinstance(N, Point2d):
            self.__tensionPoints2d.append([N.x, N.y])
            return N
        else:
            if not isinstance(N, float) and not isinstance(N, int):
                raise Exception("N must be float or int type!!!")

            if not isinstance(M, float) and not isinstance(M, int):
                raise Exception("M must be float or int type!!!")

            self.__tensionPoints2d.append([N, M])
            return Point2d(N, M)

    def addTensionPoints2d(self, listOfPoints):
        if isinstance(listOfPoints, list):
            for p in listOfPoints:
                self.__tensionPoints2d.append([p.x, p.y])
        else:
            raise Exception("Only list of Point2d!!!")

    def tensionPoints2d(self):
        return self.__tensionPoints2d

    def currentIdxTensionPoint2d(self):
        return self.__currentTensionPoint2dIdx

    def setCurrentIdxTensionPoint2d(self, idx):
        self.__currentTensionPoint2dIdx = idx

    def setLogLevel(self, ll: int):
        self.__ll = ll

    def currentIdxInteractionDomain2d(self):
        return self.__currentDomain2dIdx

    def setCurrentIdxInteractionDomain2d(self, idx):
        if isinstance(idx, int):
            self.__currentDomain2dIdx = idx
        elif isinstance(idx, str) and (idx == "last"):
            self.__currentDomain2dIdx = len(self.__domainPoints2d) - 1
        else:
            raise TypeError("idx must be string or int")

    def interactionDomainBuild2d(self, **kwargs):
        if "nbPoints" in kwargs:
            _nbPoints = kwargs["nbPoints"]
        else:
            _nbPoints = self.__plot2dInteraction_nbPoints

        if "alpha" in kwargs:
            self.setSteelAlphaWeight(kwargs["alpha"])

        if "bounding" in kwargs:
            bounding = kwargs["bounding"]
        else:
            bounding = False

        if "SLS" in kwargs:
            SLS = kwargs["SLS"]
        else:
            SLS = False

        if "negative_compression" in kwargs:
            NC = kwargs["negative_compression"]
        else:
            NC = False

        if "hotPoints" in kwargs:
            hotPoints = kwargs["hotPoints"]
        else:
            hotPoints = False

        NxMz, fields, bound = self.build2dInteractionCompleteDomain(_nbPoints, SLS, NC)

        self.__domainPoints2d.append(NxMz)
        self.__domainPointsHot.append(hotPoints)
        self.__domainFieldsPoints2d.append(fields)
        self.__domainBounding.append(bound)

        if bounding:
            return PointCloud2d(NxMz), bound
        else:
            return PointCloud2d(NxMz)

    def getInteractionDomain(self):
        return self.__domainPoints2d

    def getInteractionField(self):
        return self.__domainFieldsPoints2d

    def getInteractionBounding(self):
        return self.__domainBounding

    def getInteractionDomainDict(self) -> dict:
        domainDict = {"domains": []}
        for idx, _d in enumerate(self.__domainPoints2d):
            domain = {
                "NxMx": self.__domainPoints2d[idx],
                "Fields": self.__domainFieldsPoints2d[idx],
                "Bounding": self.__domainBounding[idx],
            }
            domainDict["domains"].append(domain)

        return domainDict

    def interactionDomainPlot2d(self, **kwargs):
        """Print interaction domain builded with interactionDomainBuild2d()

        Print interaction domain builded with interactionDomainBuild2d()
        Ex:
            sec.interactionDomainPlot2d(xLabel = 'N [KN]', yLabel = 'M [KN*m]', export = filePath + '/' + fileName)

        Args:
            xLabel (str): Add label in x-axis
            yLabel (str): Add label in y-axis
            titleAddStr (str): Big title above figure
            scale_Nx (float): Scale figure in Nx. Default is 0.001 [KN]
            scale_Mz (float): Scale figure in Mx. Default is 0.000001 [KN/m]
            lines (List[Point2D]): Add line series
            markers (bool): Add markers on domain. Default is True
            export (str): file name to export figure.
            savingSingleDomains (List[int]): For multidomain, plot only index assigned to list
        Returns:
            None: Armatura minima
        """
        if "xLabel" in kwargs:
            _xLabel = kwargs["xLabel"]
        else:
            _xLabel = self.__plot2dInteraction_xLabel

        if "yLabel" in kwargs:
            _yLabel = kwargs["yLabel"]
        else:
            _yLabel = self.__plot2dInteraction_yLabel

        if "titleAddStr" in kwargs:
            _titleAddStr = kwargs["titleAddStr"]
        else:
            _titleAddStr = self.getDescr()

        if "scale_Nx" in kwargs:
            _scale_Nx = kwargs["scale_Nx"]
        else:
            _scale_Nx = self.__plot2dInteraction_scale_Nx

        if "scale_Mz" in kwargs:
            _scale_Mz = kwargs["scale_Mz"]
        else:
            _scale_Mz = self.__plot2dInteraction_scale_Mz

        if "lines" in kwargs:
            _lines = kwargs["lines"]
        else:
            _lines = []

        if "markers" in kwargs:
            _markers = kwargs["markers"]
        else:
            _markers = True

        if "export" in kwargs:
            _export = kwargs["export"]
            _dpi = 300
        else:
            _export = None
            _dpi = None

        if "savingSingleDomains" in kwargs:
            _savingSingleDomains = kwargs["savingSingleDomains"]
        else:
            _savingSingleDomains = False

        if "printDomains" in kwargs:
            _printDomains = kwargs["printDomains"]
        else:
            _printDomains = None

        interactionDomainBasePlot2d(
            self.__domainPoints2d,
            self.__domainFieldsPoints2d,
            hotPoints=self.__domainPointsHot,
            xLabel=_xLabel,
            yLabel=_yLabel,
            titleAddStr=_titleAddStr,
            tensionPoints=self.__tensionPoints2d,
            scale_Nx=_scale_Nx,
            scale_Mz=_scale_Mz,
            lines=_lines,
            markers=_markers,
            savingSingleDomains=_savingSingleDomains,
            export=_export,
            dpi=_dpi,
            printDomains=_printDomains,
        )

    def getSection(self) -> ConcreteSection:
        """
        Restituisce la sezione embedded di tipo EXAStructural
        """
        return super()

    def calConcreteArea(self):
        return super().calConcreteArea()

    def calSteelArea(self, alphaWeight=False, weights=False):
        return super().calSteelArea(alphaWeight, weights)

    def calIdealArea(self):
        return super().calProp_Ah()

    def calSteelAreaMin(self, Ned: float = 0.0):
        if len(self.__tensionPoints2d) == 0:
            return super().calSteelAreaMin(Ned)

        if self.currentIdxTensionPoint2d == -1:
            return super().calSteelAreaMin(Ned)

        tp = self.__tensionPoints2d[self.currentIdxTensionPoint2d()]
        return super().calSteelAreaMin(tp[0])

    def calSteelAreaMax(self):
        return super().calSteelAreaMax()

    def alphaPhi(self, Asmin, Asmax, phi):
        """
        Determina il moltiplicatore alpha al variare di phi tale che per phi
        che và da 0 ed 1 l'area và da Amin ad Amax
        """
        As = self.calSteelArea()
        alphaphi = (Asmin / As) * (1 - phi) + (Asmax / As) * phi
        # print("AlplaPhi = %1.6f - As = %2.6f - AsAlphaPhi =%3.6f "%(alphaphi,As,As*alphaphi))
        return alphaphi

    def setElementType(self, elTypeStr):
        super().setElementType(elTypeStr)

    def getElementType(self):
        return super().getElementType()

    @staticmethod
    def __solveAB(
        _N: float, _M: float, _A: float, _Sx: float, _Jx: float
    ) -> Tuple[float, float]:
        AA = (-_N * _Sx - _M * _A) / (-_Sx * _Sx + _Jx * _A)
        BB = (_M * _Sx + _N * _Jx) / (-_Sx * _Sx + _Jx * _A)
        return AA, BB

    @staticmethod
    def __sigma(AABB: Tuple[float, float], ycoord: float) -> float:
        return AABB[0] * ycoord + AABB[1]

    def __properties_cracked(
        self, AABB: Tuple[float, float]
    ) -> Tuple[float, float, float]:

        # ys is position for neutral x-axis
        yn = -AABB[1] / AABB[0]

        topRectBarycenterY = (self.getVertexConcrAt(2).y + yn) / 2
        botRectBarycenterY = (self.getVertexConcrAt(0).y + yn) / 2

        topAc = self.getDimW() * (self.getVertexConcrAt(2).y - yn)
        topScx = topAc * topRectBarycenterY
        topJcx = 1 / 12 * self.getDimW() * pow(
            self.getVertexConcrAt(2).y - yn, 3
        ) + topAc * pow(topRectBarycenterY, 2)

        botAc = self.getDimW() * (yn - self.getVertexConcrAt(0).y)
        botScx = botAc * botRectBarycenterY
        botJcx = 1 / 12 * self.getDimW() * pow(
            yn - self.getVertexConcrAt(0).y, 3
        ) + botAc * pow(botRectBarycenterY, 2)

        if self.__sigma(AABB, topRectBarycenterY) < 0:
            Ac = topAc
            Scx = topScx
            Jcx = topJcx
        else:
            Ac = botAc
            Scx = botScx
            Jcx = botJcx

        n = self.getHomogenization()
        Ah = Ac + n * self.calSteelArea()
        Shx = Scx + n * self.calProp_Ssx()
        Jhx = Jcx + n * self.calProp_Isx()
        return Ah, Shx, Jhx

    def __effortsNM_cracked(self, AABB: Tuple[float, float]) -> Tuple[float, float]:
        prop = self.__properties_cracked(AABB)
        N = prop[1] * AABB[0] + prop[0] * AABB[1]
        M = -prop[2] * AABB[0] - prop[1] * AABB[1]
        return N, M

    def __debalancing(
        self,
        N_sec: float,
        M_sec: float,
        N_ext: float,
        M_ext: float,
    ) -> float:

        if N_ext != 0.0:
            N_toll = abs((N_ext - N_sec) / N_ext)
        else:
            N_toll = max(self.getDimW(), self.getDimH()) / abs(M_sec / N_sec)

        if M_ext != 0.0:
            M_toll = abs((M_ext - M_sec) / M_ext)
        else:
            M_toll = 0.0

        return max(N_toll, M_toll)

    def solverSLS_NM(
        self, N: float, M: float, uncracked: bool = False
    ) -> Tuple[float, float, Any]:
        r"""
        Solver for axial and flexural effort (N and M) in rc-section.
        M positive if positive fiber is in compression and N negative if
        produces compression.
        Normal effort N is applied on barycenter of rectangular section.

        Args:
            N (float): Normal effort negative for compression
            M (float): Flexural effort positive intended if it strech inferior
             fibers
            uncracked (bool): If True section will be intended totally
             responsive in traction and compression

        Returns:
                A tuple containing

                 -  $`\sigma_c`$ max compression on concrete vertices
                 -  $`\sigma_s`$ max traction on steel rebars
                 +  $`x_i`$ (float|Any) measured from top to bottom.

                 None will be returned when N and M are 0. When cases are pure
                 tension or compression math.inf will be returned.
        """
        logger.log(tp="INF", level=1, msg="Perform classical solution for N and M ...")
        # Assign solution method:
        self.__uncracked = uncracked

        # Assign N, M to section
        self.setForces(N, M)

        # Reset stresses and neutral axis
        self.setSteelStress(self.getVertexSteelNb() * [0])
        self.setConcrStress(self.getVertexConcrNb() * [0])
        self.setConcrDeform(self.getVertexConcrNb() * [0])

        self.__xi = None

        # Null efforts
        if N == 0.0 and M == 0.0:
            logger.log(tp="INF", level=1, msg="... efforts are nulls ...")
            logger.log(tp="INF", level=1, msg="... done. Quit !!!")
            return 0.0, 0.0, None

        # Retrive some geometrical dimension and properties
        n = self.getHomogenization()
        H = self.getStructConcretelItem().getShape().h()
        Es = self.getMaterialSteel().get_Es()

        # Ideal area properties
        Ah = self.calIdealArea()
        Shx = self.calProp_Shx()
        Jhx = self.calProp_Ihx()

        AABBh = self.__solveAB(N, M, Ah, Shx, Jhx)

        # ----------------------------------------------------------------------
        #                         UNCRACKED SECTION
        # ----------------------------------------------------------------------
        if self.__uncracked:
            logger.log(
                tp="INF", level=self.__ll, msg="... uncracked chosen section ..."
            )
            for i in range(0, self.getVertexConcrNb()):
                yc = self.getVertexConcrAt(i).y
                self.getConcrStress()[i] = self.__sigma(AABBh, yc)
                self.getConcrDeform()[i] = n * self.getConcrStress()[i] / Es

            for i in range(0, self.getVertexSteelNb()):
                ys = self.getVertexSteelAt(i).y
                self.getSteelStress()[i] = n * self.__sigma(AABBh, ys)

            sigma_c = min(self.getConcrStress())
            sigma_s = max(self.getSteelStress())

            if M == 0.0 and Shx == 0.0:
                xi = math.inf
            else:
                # From sigma = AA*y + BB with sigma = 0:
                #           y = - BB / AA
                # then xi = H/2 - y = H/2 + BB / AA
                xi = H / 2 + AABBh[1] / AABBh[0]

            self.__xi = xi
            logger.log(tp="INF", level=self.__ll, msg="... done. Quit !!!")
            return sigma_c, sigma_s, xi

        # ----------------------------------------------------------------------
        #                           CRACKED SECTION
        # ----------------------------------------------------------------------
        # copy stresses zero
        concreteStresses = self.getConcrStress().copy()
        for i in range(0, self.getVertexConcrNb()):
            yc = self.getVertexConcrAt(i).y
            concreteStresses[i] = self.__sigma(AABBh, yc)
            self.getConcrDeform()[i] = n * concreteStresses[i] / Es

        if max(concreteStresses) <= 0.0:
            logger.log(
                tp="INF", level=self.__ll, msg="... section totally compressed ..."
            )
            self.__sls_state = SectionStates.COMPRESSED
            self.setConcrStress(concreteStresses)

            for i in range(0, self.getVertexSteelNb()):
                ys = self.getVertexSteelAt(i).y
                self.getSteelStress()[i] = n * self.__sigma(AABBh, ys)

            sigma_c = min(self.getConcrStress())
            sigma_s = max(self.getSteelStress())
            if AABBh[0] != 0.0:
                xi = H / 2 + AABBh[1] / AABBh[0]
            else:
                xi = math.inf

            self.__xi = xi
            logger.log(tp="INF", level=self.__ll, msg="... done. Quit !!!")
            return sigma_c, sigma_s, xi

        # Steel area properties
        As = self.calSteelArea()
        Ssx = self.calProp_Ssx()
        Jsx = self.calProp_Isx()
        AABBs = self.__solveAB(N, M, As, Ssx, Jsx)

        for i in range(0, self.getVertexConcrNb()):
            yc = self.getVertexConcrAt(i).y
            concreteStresses[i] = self.__sigma(AABBs, yc)
            self.getConcrDeform()[i] = concreteStresses[i] / Es

        if min(concreteStresses) >= 0.0:
            logger.log(
                tp="INF", level=self.__ll, msg="... section totally stretched ..."
            )
            self.__sls_state = SectionStates.STRETCHED
            for i in range(0, self.getVertexSteelNb()):
                ys = self.getVertexSteelAt(i).y
                self.getSteelStress()[i] = self.__sigma(AABBs, ys)
            sigma_c = min(self.getConcrStress())
            sigma_s = max(self.getSteelStress())
            if AABBs[0] != 0.0:
                xi = H / 2 + AABBs[1] / AABBs[0]
            else:
                xi = math.inf
            logger.log(tp="INF", level=self.__ll, msg="... done. Quit !!!")
            self.__xi = xi
            return sigma_c, sigma_s, xi

        logger.log(tp="INF", level=self.__ll, msg="... cracked section ...")
        self.__sls_state = SectionStates.PARTIALIZED
        maxIt = 15
        toll = 1e-6
        for i in range(0, maxIt):
            Ah, Shx, Jhx = self.__properties_cracked(AABBh)
            AABBh = self.__solveAB(N, M, Ah, Shx, Jhx)
            N_sec, M_sec = self.__effortsNM_cracked(AABBh)
            tollDebal = self.__debalancing(N_sec, M_sec, N, M)
            self.__errorOnForce = tollDebal
            self.__errorOnTorque = tollDebal
            logger.log(tp="INF", level=self.__ll, msg=f"tollDebal -> {tollDebal}")
            logger.log(tp="INF", level=self.__ll, msg=f"iteration for balance -> {i}")
            if tollDebal < toll:
                logger.log(tp="INF", level=self.__ll, msg=f"found balance at i = {i}")
                for ii in range(0, self.getVertexConcrNb()):
                    yc = self.getVertexConcrAt(ii).y
                    self.getConcrDeform()[ii] = n * self.__sigma(AABBh, yc) / Es

                    if self.__sigma(AABBh, yc) > 0.0:
                        self.getConcrStress()[ii] = 0.0
                    else:
                        self.getConcrStress()[ii] = self.__sigma(AABBh, yc)

                for ii in range(0, self.getVertexSteelNb()):
                    ys = self.getVertexSteelAt(ii).y
                    self.getSteelStress()[ii] = n * self.__sigma(AABBh, ys)

                sigma_c = min(self.getConcrStress())
                sigma_s = max(self.getSteelStress())

                if AABBh[0] != 0.0:
                    xi = H / 2 + AABBh[1] / AABBh[0]
                else:
                    xi = math.inf
                logger.log(
                    tp="INF", level=self.__ll, msg="... solution found. Quit !!!"
                )
                self.__xi = xi

                return sigma_c, sigma_s, xi
        logger.log(tp="ERR", level=self.__ll, msg="... solution not found. Quit :-(")
        return 0.0, 0.0, None

    def __str__(self):
        dispstr = "RCTemplRectEC2 Object: \n"
        dispstr = dispstr + "-----------------------  \n"
        dispstr = dispstr + "Tension Points 2d = " + str(self.__tensionPoints2d) + "\n"
        dispstr = dispstr + "-----------------\n"
        dispstr = dispstr + "Section embedded-->\n"
        dispstr = dispstr + "------------------\n"
        dispstr = dispstr + str(ConcreteSection).replace("\n", "\n  | ")
        return dispstr


def RCTemplRectEC2DesignNM(**kwargs):
    if "name" in kwargs:
        name = kwargs["name"]
    else:
        name = "section_01"

    if "elementType" in kwargs:
        elementType = kwargs["elementType"]
    else:
        elementType = "beam"

    if "steel" in kwargs:
        steel = kwargs["steel"]
    else:
        steel = "B450C"

    if "concrete" in kwargs:
        concrete = kwargs["concrete"]
    else:
        concrete = "C32/40"

    if "sectionH" in kwargs:
        sectionH = kwargs["sectionH"]
    else:
        sectionH = 500.0

    if "sectionW" in kwargs:
        sectionW = kwargs["sectionW"]
    else:
        sectionW = 300.0

    if "topRecover" in kwargs:
        topRecover = kwargs["topRecover"]
    else:
        topRecover = 40.0

    if "botRecover" in kwargs:
        botRecover = kwargs["botRecover"]
    else:
        botRecover = 40.0

    if "N" in kwargs:
        N = kwargs["N"]
    else:
        N = +2.50 * 1e3 * 1e3

    if "M" in kwargs:
        M = kwargs["M"]
    else:
        M = +2.93 * 1e2 * 1e6

    if "toll" in kwargs:
        toll = kwargs["toll"]
    else:
        toll = 1e-5

    if "toll_bisec" in kwargs:
        toll_bisec = kwargs["toll_bisec"]
    else:
        toll_bisec = 1e-3

    if "maxIt" in kwargs:
        maxIt = kwargs["maxIt"]
    else:
        maxIt = 100

    if "plot" in kwargs:
        plot = kwargs["plot"]
    else:
        plot = False

    if "alphaTopBot" in kwargs:
        alphaTopBot = kwargs["alphaTopBot"]
    else:
        alphaTopBot = 1.0

    if "factorStart" in kwargs:
        factorStart = kwargs["factorStart"]
    else:
        factorStart = 0

    if "factorEnd" in kwargs:
        factorEnd = kwargs["factorEnd"]
    else:
        factorEnd = 1

    if "points" in kwargs:
        points = kwargs["points"]
    else:
        points = 100

    if "logLevel" in kwargs:
        log = kwargs["logLevel"]
    else:
        log = 0

    if "markersOnDomain" in kwargs:
        markers = kwargs["markersOnDomain"]
    else:
        markers = True

    if "savingSingleDomains" in kwargs:
        savingSingleDomains = kwargs["savingSingleDomains"]
    else:
        savingSingleDomains = False

    if "SLS" in kwargs:
        SLS = kwargs["SLS"]
    else:
        SLS = False

    if "sigmacMax" in kwargs:
        sigmacMax = kwargs["sigmacMax"]
    else:
        sigmacMax = 0.6 * 32

    if "sigmasMax" in kwargs:
        sigmasMax = kwargs["sigmasMax"]
    else:
        sigmasMax = 0.85 * 450

    if "homogeneization" in kwargs:
        homogeneization = kwargs["homogeneization"]
    else:
        homogeneization = 15.0

    if "outSection" in kwargs:
        outSection = kwargs["outSection"]
    else:
        outSection = False

    # Setting new instance of section with
    # id = 1 and name = "First Section"
    section = RCTemplRectEC2(1, name)
    section.setElementType(elementType)

    # Setting dimension
    section.setDimH(sectionH)
    section.setDimW(sectionW)
    # Setting materials
    section.setMaterials(concrete, steel, sigmacMax, sigmasMax, homogeneization)

    if "alphacc" in kwargs:
        section.getMaterialConcr().set_alphacc(kwargs["alphacc"])
    else:
        section.getMaterialConcr().set_alphacc(1.0)

    # Adding Tension point Area
    pt = Point2d(N, M)
    print(f"Tension point = ({N:1.3E},{M:2.3E})")
    section.addTensionPoint2d(N=pt.x, M=pt.y)

    # section can have many tension points then we need choosing the current
    section.setCurrentIdxTensionPoint2d(0)

    AsteelMax = section.calSteelAreaMax()
    AsteelMin = section.calSteelAreaMin()
    AsteelMed = (AsteelMax + AsteelMin) / 2

    # 'MB' means medium bottom area
    # 'MT' means medium top area
    Atot = AsteelMed
    ABot = Atot / (alphaTopBot + 1)
    ATop = alphaTopBot * ABot

    if log == 1:
        print("Steel Area TOP = %1.3f" % ATop)
    if log == 1:
        print("Steel Area BOT = %1.3f" % ABot)

    section.addSteelArea("MB", botRecover, ABot)
    section.addSteelArea("MT", topRecover, ATop)

    # Recalc cause recover now is present
    AsteelMax = section.calSteelAreaMax()
    AsteelMin = section.calSteelAreaMin()

    # Finding area max and min with current tension point
    if log == 2:
        print("Values after tension point")
    if log == 1:
        print("Steel Area max = %1.3f" % section.calSteelAreaMax())
    if log == 1:
        print("Steel Area min = %1.3f" % section.calSteelAreaMin())

    # print(section)
    # Building points set of interaction diagramm with min and max
    areaFactor0 = factorStart  # 0
    minPointsCloud = section.interactionDomainBuild2d(
        nbPoints=points,
        alpha=section.alphaPhi(AsteelMin, AsteelMax, areaFactor0),
        SLS=SLS,
    )

    areaFactor1 = factorEnd  # 1
    maxPointsCloud, bounding = section.interactionDomainBuild2d(
        nbPoints=points,
        alpha=section.alphaPhi(AsteelMin, AsteelMax, areaFactor1),
        bounding=True,
        SLS=SLS,
    )

    if log == 2:
        print("Bounding of MAXIMUM domain")
    if log == 2:
        print(bounding)

    brox = bounding[1] - bounding[0]
    broy = bounding[3] - bounding[2]

    # linesOfMinimalPoints = []

    contained, pintersect, intfactor0, pindex = minPointsCloud.contains(
        pt.x, pt.y, rayFromCenter=True, ro=(brox, broy)
    )

    find = True
    # if contained:
    if intfactor0 > 1.0:
        # raise Exception("Pt - Containted in MIN !!!")
        find = False
        Area = AsteelMin
        section.addTensionPoints2d(pintersect)
        if log == 1:
            print("Pt - Containted in MIN !!!")
        Area = section.alphaPhi(AsteelMin, AsteelMax, areaFactor0) * Atot
        print("Tension point contained by minimal area %f.2" % Area)
    else:
        section.addTensionPoints2d(pintersect)
        if log == 1:
            print("Pt - NOT containted in MIN !!!")
        Area = 0.0

    contained, pintersect, intfactor1, pindex = maxPointsCloud.contains(
        pt.x, pt.y, rayFromCenter=True, ro=(brox, broy)
    )

    # if not contained:
    if intfactor1 < 1.0:
        find = False
        if log == 1:
            print("Pt - NOT containted in MAX !!!")
        if factorEnd == 1:
            Area = AsteelMax
        else:
            Area = factorEnd * AsteelMax
        # raise Exception("Pt - Not containted in MAX !!!")

    pointsCloud = None
    value_estimate = None
    if find:
        Area_n = areaFactor1
        Area_nm1 = areaFactor0

        Fx_n = intfactor1 - 1.0
        Fx_nm1 = intfactor0 - 1.0

        if log == 2:
            print("Step i= 0")
        if log == 2:
            print(f"Fx_n = {Fx_n:1.6e} - Fx_nm1 = {Fx_nm1:1.6e}")
        if log == 2:
            print(f"intfactor1 = {intfactor1:1.6e} - intfactor0 = {intfactor0:1.6e}")

        if log == 1:
            print(
                "Ricerca area tra %1.6e e %2.6e"
                % (factorStart * AsteelMax, factorEnd * AsteelMax)
            )

        bisection = False
        if log == 1:
            print("Secants algorithm ...")
        for i in range(1, maxIt):
            if log == 2:
                print("-----------------------------------------")
            if log == 2:
                print(
                    "Step i= %1.i - Fx_n = %2.6e - Fx_nm1 = %3.6e" % (i, Fx_n, Fx_nm1)
                )
            Area_np1 = Area_n - ((Area_n - Area_nm1) / (Fx_n - Fx_nm1)) * Fx_n
            if log == 2:
                print("Area_np1= %1.6e" % Area_np1)

            # Area = Area_np1*AsteelMax
            Area = section.alphaPhi(AsteelMin, AsteelMax, Area_np1) * Atot
            if log == 2:
                print("Area al passo = %1.6e" % Area)

            # if Area < 0:
            if Area_np1 < 0:
                if log == 1:
                    print("Secants algorithm fails !!!")
                if log == 1:
                    print("... using bisec algorithm ...")
                bisection = True
                break
            Area_nm1 = Area_n
            Area_n = Area_np1

            Area = section.alphaPhi(AsteelMin, AsteelMax, Area_n) * Atot
            # Area = Area_np1*AsteelMax

            Fx_nm1 = Fx_n

            pointsCloud = section.interactionDomainBuild2d(
                nbPoints=points,
                alpha=section.alphaPhi(AsteelMin, AsteelMax, Area_n),
                SLS=SLS,
            )
            contained, pintersect, intfactor, pindex = pointsCloud.contains(
                pt.x, pt.y, rayFromCenter=True, ro=(brox, broy)
            )

            Fx_n = intfactor - 1.0

            if math.sqrt(math.pow(Fx_n, 2)) < toll or i == maxIt:
                if log == 1:
                    print("Iterazioni convergenti al passo n = %1.0i" % i)
                break
        # if True:
        if bisection:
            leftLimit = areaFactor0
            rightLimit = areaFactor1

            # Area_p = mLimit*AsteelMax

            Area_p = 0.0  # section.alphaPhi(AsteelMin,AsteelMax,(leftLimit + rightLimit) / 2)*Atot

            for i in range(1, maxIt):

                mLimit = (leftLimit + rightLimit) / 2.0

                pointsCloud = section.interactionDomainBuild2d(
                    nbPoints=points,
                    alpha=section.alphaPhi(AsteelMin, AsteelMax, mLimit),
                    SLS=SLS,
                )

                contained, pintersect, intfactor, pindex = pointsCloud.contains(
                    pt.x, pt.y, rayFromCenter=True, ro=(brox, broy)
                )

                if log == 2:
                    print(f"intfactor = {intfactor:1.3e} - mLimit = {mLimit:2.3e}")
                if log == 2:
                    print(
                        "Area al passo = %1.6e"
                        % (section.alphaPhi(AsteelMin, AsteelMax, mLimit) * Atot)
                    )

                # if contained:
                if intfactor > 1:
                    # print("contained")
                    rightLimit = mLimit
                    if i == 1:
                        contained_pm1 = True
                    elif i > 1 and contained_pm1 is False:
                        leftLimit = mLimit
                        contained_pm1 = True
                    else:
                        contained_pm1 = True
                else:
                    # print("not contained")
                    leftLimit = mLimit

                    if i == 1:
                        contained_pm1 = False
                    elif i > 1 and contained_pm1 is True:
                        rightLimit = mLimit
                        contained_pm1 = False
                    else:
                        contained_pm1 = False

                # Area_p = mLimit*AsteelMax
                Area_pm1 = Area_p
                Area_p = section.alphaPhi(AsteelMin, AsteelMax, mLimit) * Atot

                if (
                    math.sqrt(math.pow((Area_p - Area_pm1) / Area_p, 2)) < toll_bisec
                ) or i == maxIt:
                    # print(math.sqrt(math.pow((Area_p-Area_pm1)/Area_p,2)))
                    if i < maxIt:
                        if log == 1:
                            print("Iterazioni convergenti al passo n = %1.0i" % i)
                    else:
                        if log == 1:
                            print(
                                "Raggiunto il numero massimo di iterazioni %1.6i !!!"
                                % i
                            )
                    Area = Area_p
                    break

    if plot:
        section.interactionDomainPlot2d(
            markers=markers, savingSingleDomains=savingSingleDomains
        )

    if pointsCloud is not None:
        # Estimating value on base distance from intersection point
        value_estimate = len(pointsCloud[pindex[0]]) * [None]
        for i, _v in enumerate(value_estimate):
            left_factor = pindex[1] / pindex[3]
            right_factor = pindex[2] / pindex[3]
            value_estimate[i] = (
                pointsCloud[pindex[0]][i] * left_factor
                + pointsCloud[pindex[0] + 1][i] * right_factor
            )

    if outSection:
        return Area, value_estimate, section
    else:
        return Area, value_estimate
