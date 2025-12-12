import math
from typing import Dict, List, Tuple

from xstrumodeler.xstrumodeler import (
    VDouble,
    VVDouble,
    XStruCircle,
    XStruModeler,
    XStruNode2D,
    XStruTriangle,
    toPythonDict,
    toPythonList,
)

from pycivil.EXAGeometry.clouds import PointCloud2d
from pycivil.EXAGeometry.geometry import Point2d
from pycivil.EXAGeometry.shapes import ShapesEnum
from pycivil.EXAStructural.loads import ForcesOnSection
from pycivil.EXAStructural.sections import (
    AreaProperties,
    ConcreteSection,
    SectionStates,
)

# Signs for forces on section:

# X from right to left for forces and moments
# Y from top to bottom for forces and moments
# Z clockwise
# compression forces are negatives


class SectionModeler:
    def __init__(self) -> None:
        self.__modeler = XStruModeler()

    def addSection(self, ids: int, setCurrent: bool = True) -> bool:
        return self.__modeler.addSection(ids, setCurrent)

    def importFromRCSection(self, section: ConcreteSection) -> bool:
        shape = section.getStructConcretelItem().getShape()
        if shape.getType() == ShapesEnum.SHAPE_RECT:
            pBL = shape.getShapePoint("BL")
            pBR = shape.getShapePoint("BR")
            pTR = shape.getShapePoint("TR")
            pTL = shape.getShapePoint("TL")

            idBL = self.__modeler.buildIdForNodes()
            self.__modeler.addNode(idBL, pBL.x, pBL.y)

            idBR = self.__modeler.buildIdForNodes()
            self.__modeler.addNode(idBR, pBR.x, pBR.y)

            idTR = self.__modeler.buildIdForNodes()
            self.__modeler.addNode(idTR, pTR.x, pTR.y)

            idTL = self.__modeler.buildIdForNodes()
            self.__modeler.addNode(idTL, pTL.x, pTL.y)

            idTria1 = self.__modeler.buildIdForTriangles()
            self.__modeler.addTriangle(idTria1, idBL, idBR, idTR)

            idTria2 = self.__modeler.buildIdForTriangles()
            self.__modeler.addTriangle(idTria2, idTR, idTL, idBL)
        else:
            return False

        for si in section.getStructSteelItems():
            idn = self.__modeler.buildIdForNodes()
            exn = self.__modeler.addNode(idn, si.getOrigin().x, si.getOrigin().y)
            exc = self.__modeler.addCircle(
                self.__modeler.buildIdForCircles(), idn, si.getShape().getDiameter() / 2
            )
            if not exn or not exc:
                return False

        return True

    def setCurrent(self, ids: int) -> bool:
        return self.__modeler.setCurrent(ids)

    def getCurrent(self) -> int:
        """
        Get current model index

        Returns:
            (int): if model doesn't have current section return -1.
        """
        return self.__modeler.getCurrent()

    def getCurrentType(self) -> str:
        return self.__modeler.getCurrentType()

    def getModelIndices(self) -> List[int]:
        return list(self.__modeler.getModelIndices())

    def sizeOfSectionModels(self) -> int:
        return self.__modeler.sizeOfSectionModels()

    def addNode(
        self,
        ids: int,
        x: float,
        y: float,
    ) -> bool:
        """Add node to current section model

        Add node to current section model. Parameter ids must be unique
        Args:
            ids: unique ids
            x: x-location
            y: y-location

        Returns:
            True if ids is unique and there is a current model
        """
        return self.__modeler.addNode(ids, x, y)

    def nodesSize(self) -> int:
        """Size of nodes for current model

        Returns:
            A positive integer if there is a current model or -1
        """
        return self.__modeler.nodesSize()

    def getNodeX(self, ids: int) -> float:
        return self.__modeler.getNodeX(ids)

    def getNodeY(self, ids: int) -> float:
        return self.__modeler.getNodeY(ids)

    def setNodeX(self, ids: int, x: float) -> float:
        return self.__modeler.setNodeX(ids, x)

    def setNodeY(self, ids: int, y: float) -> float:
        return self.__modeler.setNodeY(ids, y)

    def getNodes(self) -> Dict[int, XStruNode2D]:
        """Method that retrives nodes from current model

        The method retrives nodes in current model.
        If there isn't none model already current gets empy dict.

        Returns:
            Dict[int, XStruNode2D]
        """
        return toPythonDict(self.__modeler.getNodes())

    def getSolidNodes(self) -> Dict[int, XStruNode2D]:
        """Method that retrives solid nodes from current model

        The method retrives solid nodes (nodes connected to solid element as
        triangles) in current model.
        If there isn't none model already current gets empy dict.

        Returns:
            Dict[int, XStruNode2D]
        """
        return toPythonDict(self.__modeler.getSolidNodes())

    def addTriangle(self, ids: int, idn_1: int, idn_2: int, idn_3: int) -> bool:
        return self.__modeler.addTriangle(ids, idn_1, idn_2, idn_3)

    # def getTriangles(self) -> Dict[int, XStruTriangle]:
    #     return toPythonDict(self.__modeler.getTriangles())

    def getTrianglesIds(self) -> Dict[int, Tuple[int, int, int]]:
        d = {}
        pd = toPythonDict(self.__modeler.getTrianglesIds())
        for k in pd:
            d[k] = toPythonList(pd[k])
        return d

    def getTrianglesCoords(
        self,
    ) -> Dict[int, Tuple[float, float, float, float, float, float]]:
        d = {}
        pd = toPythonDict(self.__modeler.getTrianglesCoords())
        for k in pd:
            d[k] = toPythonList(pd[k])
        return d

    def trianglesSize(self) -> int:
        return self.__modeler.trianglesSize()

    def triangleNodesSize(self) -> int:
        return self.__modeler.triangleNodesSize()

    def addCircle(self, ids: int, idn_center: int, radius: float) -> bool:
        return self.__modeler.addCircle(ids, idn_center, radius)

    def addCircleAndNode(
        self, ids: int, idn_center: int, x: float, y: float, radius: float
    ) -> bool:
        self.addNode(idn_center, x, y)
        self.addCircle(ids, idn_center, radius)
        return self.__modeler.addCircle(ids, idn_center, radius)

    def getCircles(self) -> Dict[int, XStruCircle]:
        return toPythonDict(self.__modeler.getCircles())

    def circlesSize(self) -> int:
        return self.__modeler.circlesSize()

    def setCircleRadius(self, ids: int, radius: float) -> bool:
        return self.__modeler.setCircleRadius(ids, radius)

    def addLawParaboleRectangle(
        self, ids: int, descr: str, fcd: float, ec2: float, ecu: float
    ) -> bool:
        return self.__modeler.addLawParaboleRectangle(ids, descr, fcd, ec2, ecu)

    def addLawBilinear(
        self, ids: int, descr: str, fsd: float, Es: float, esu: float
    ) -> bool:
        return self.__modeler.addLawBilinear(ids, descr, fsd, Es, esu)

    def setCirclesLawInAllModels(self, idLaw: int) -> bool:
        return self.__modeler.setCirclesLawInAllModels(idLaw)

    def setTrianglesLawInAllModels(self, idLaw: int) -> bool:
        return self.__modeler.setTrianglesLawInAllModels(idLaw)

    def setCirclesLawInCurrentModel(self, idLaw: int) -> bool:
        return self.__modeler.setCirclesLawInCurrentModel(idLaw)

    def setTrianglesLawInCurrentModel(self, idLaw: int) -> bool:
        return self.__modeler.setTrianglesLawInCurrentModel(idLaw)

    def printInfo(self, before: str = "") -> None:
        return self.__modeler.printInfo(before)

    def instancesOfModels(self) -> int:
        return self.__modeler.instancesOfModels()

    def instancesOfMesh(self) -> int:
        return self.__modeler.instancesOfMesh()

    def instancesOfNode2D(self) -> int:
        return self.__modeler.instancesOfNode2D()

    def instancesOfTriangle(self) -> int:
        return self.__modeler.instancesOfTriangle()

    def instancesOfCircle(self) -> int:
        return self.__modeler.instancesOfCircle()

    def instancesOfEdge2D(self) -> int:
        return self.__modeler.instancesOfEdge2D()

    def instancesOfLawBilinear(self) -> int:
        return self.__modeler.instancesOfLawBilinear()

    def instancesOfLawParabola(self) -> int:
        return self.__modeler.instancesOfLawParabola()

    def instancesOfInteractionPoints(self) -> int:
        return self.__modeler.instancesOfInteractionPoints()

    def instancesOfSectionForces(self) -> int:
        return self.__modeler.instancesOfSectionForces()

    def meshMake(self) -> bool:
        return self.__modeler.meshMake()

    def meshReset(self) -> bool:
        return self.__modeler.meshReset()

    def meshSize(self) -> int:
        return self.__modeler.meshSize()

    def meshesSliceAtYrays(self, rays: List[float]) -> bool:
        drays = VDouble()
        for r in rays:
            drays.append(r)

        return self.__modeler.meshesSliceAtYrays(drays)

    def meshesSliceAtRays(self, rays: List[List[float]]) -> bool:
        drays = VVDouble()
        for r in rays:
            abc = VDouble()
            abc.append(r[0])
            abc.append(r[1])
            abc.append(r[2])
            drays.append(abc)

        return self.__modeler.meshesSliceAtRays(drays)

    def nodesSizeAtMesh(self, idm: int) -> int:
        return self.__modeler.nodesSizeAtMesh(idm)

    def trianglesSizeAtMesh(self, idm: int) -> int:
        return self.__modeler.trianglesSizeAtMesh(idm)

    def circlesSizeAtMesh(self, idm: int) -> int:
        return self.__modeler.circlesSizeAtMesh(idm)

    def getNodesAtMesh(self, idm: int) -> List[XStruNode2D]:
        return self.__modeler.getNodesAtMesh(idm)

    def getTrianglesAtMesh(self, idm: int) -> List[XStruTriangle]:
        return self.__modeler.getTrianglesAtMesh(idm)

    def getTrianglesIdsAtMesh(self, idm: int) -> Dict[int, Tuple[int, int, int]]:
        d = {}
        pd = toPythonDict(self.__modeler.getTrianglesIdsAtMesh(idm))
        for k in pd:
            d[k] = toPythonList(pd[k])
        return d

    def getTrianglesCoordsAtMesh(
        self, idm: int
    ) -> Dict[int, Tuple[float, float, float, float, float, float]]:
        d = {}
        pd = toPythonDict(self.__modeler.getTrianglesCoordsAtMesh(idm))
        for k in pd:
            d[k] = toPythonList(pd[k])
        return d

    def getCirclesAtMesh(self, idm: int) -> List[XStruCircle]:
        return self.__modeler.getCirclesAtMesh(idm)

    def calcSolidArea(
        self,
    ) -> float:
        return self.__modeler.calcSolidArea()

    def calcPointArea(
        self,
    ) -> float:
        return self.__modeler.calcPointArea()

    def calcIdealArea(
        self,
    ) -> float:
        return self.__modeler.calcIdealArea()

    def calcSolidBarycenter(
        self,
    ) -> Point2d:
        xstrunode: XStruNode2D = self.__modeler.calcSolidBarycenter()
        return Point2d(xstrunode.xn, xstrunode.yn)

    def calcIdealBarycenter(
        self,
    ) -> Point2d:
        xstrunode: XStruNode2D = self.__modeler.calcIdealBarycenter()
        return Point2d(xstrunode.xn, xstrunode.yn)

    def calcPointBarycenter(self, area: bool = True) -> Point2d:
        """For section formed also with circle elements gives barycenter point

        For section formed also with circle elements gives barycenter point.
        If area is setted as True, the function calculates barycenter with
        weight from area.

        Args:
            area (bool): If True the barycenter is calculated using element
            areas.

        Returns:
            (Point 2d): Barycenter of points

        """
        xstrunode: XStruNode2D = self.__modeler.calcPointBarycenter(area)
        return Point2d(xstrunode.xn, xstrunode.yn)

    def calcSolidAreaProperties(self) -> AreaProperties:
        prop = self.__modeler.calcSolidAreaProperties()
        return AreaProperties(
            area=prop.area,
            sx=prop.sx,
            ixx=prop.ixx,
            iyy=prop.iyy,
            ixy=prop.ixy,
            ixxx=prop.ixxx,
            ixxy=prop.ixxy,
        )

    def calcPointAreaProperties(self) -> AreaProperties:
        prop = self.__modeler.calcPointAreaProperties()
        return AreaProperties(
            area=prop.area,
            sx=prop.sx,
            ixx=prop.ixx,
            iyy=prop.iyy,
            ixy=prop.ixy,
            ixxx=prop.ixxx,
            ixxy=prop.ixxy,
        )

    def calcIdealAreaProperties(self) -> AreaProperties:
        prop = self.__modeler.calcIdealAreaProperties()
        return AreaProperties(
            area=prop.area,
            sx=prop.sx,
            ixx=prop.ixx,
            iyy=prop.iyy,
            ixy=prop.ixy,
            ixxx=prop.ixxx,
            ixxy=prop.ixxy,
        )

    def setLogLevel(self, ll: int) -> int:
        return self.__modeler.setLogLevel(ll)

    def interactionPoints(self) -> Tuple[List[float], List[float], List[float]]:
        return (
            list(self.__modeler.fzVector()),
            list(self.__modeler.mxVector()),
            list(self.__modeler.myVector()),
        )

    def buildDomain(
        self, degreeDivision: int, ratioDivision: int, rebuild: bool = False
    ) -> bool:
        return self.__modeler.buildDomain(degreeDivision, ratioDivision, rebuild)

    def domainBounding(self) -> Tuple[float, float, float, float, float, float]:
        """

        Returns:
            [Fz_min, Fz_max, Mx_min, Mx_max, My_min, My_max,]

        """
        fzVector = self.__modeler.fzVector()
        mxVector = self.__modeler.mxVector()
        myVector = self.__modeler.myVector()
        return (
            min(fzVector),
            max(fzVector),
            min(mxVector),
            max(mxVector),
            min(myVector),
            max(myVector),
        )

    def intersectAtMy(
        self, my: float, sfx: float = 1.0, sfy: float = 1.0
    ) -> PointCloud2d:
        # Interserct at My means with domain bounding generated by Exagone Z dir
        # because we have in order Fz (X-dir), Mx (Y-dir), My (Z-dir)
        points = list(self.__modeler.intersectAtZDir(my))
        ptsNb = len(points) / 3
        assert math.ceil(ptsNb) == math.floor(ptsNb)
        cloud = []

        # skip first that is barycenter
        for i in range(1, int(ptsNb)):
            cloud.append(Point2d(points[3 * i + 0] * sfx, points[3 * i + 1] * sfy))
        return PointCloud2d(cloud)

    def intersectAtN(
        self, n: float, sfx: float = 1.0, sfy: float = 1.0
    ) -> PointCloud2d:
        # Interserct at N means with domain bounding generated by Exagone Z dir
        # because we have in order Fz (X-dir), Mx (Y-dir), My (Z-dir)
        points = list(self.__modeler.intersectAtXDir(n))
        ptsNb = len(points) / 3
        assert math.ceil(ptsNb) == math.floor(ptsNb)
        cloud = []

        # skip first that is barycenter
        for i in range(1, int(ptsNb)):
            cloud.append(Point2d(points[3 * i + 1] * sfx, points[3 * i + 2] * sfy))
        return PointCloud2d(cloud)

    def intersectAtMx(
        self, mx: float, sfx: float = 1.0, sfy: float = 1.0
    ) -> PointCloud2d:
        # Interserct at N means with domain bounding generated by Exagone Z dir
        # because we have in order Fz (X-dir), Mx (Y-dir), My (Z-dir)
        points = list(self.__modeler.intersectAtYDir(mx))
        ptsNb = len(points) / 3
        assert math.ceil(ptsNb) == math.floor(ptsNb)
        cloud = []

        # skip first that is barycenter
        for i in range(1, int(ptsNb)):
            cloud.append(Point2d(points[3 * i + 0] * sfx, points[3 * i + 2] * sfy))
        return PointCloud2d(cloud)

    def sectionRotate(self, degree: float, x: float = 0, y: float = 0) -> None:
        self.__modeler.sectionRotate(degree, x, y)

    def moveToSolidBarycenter(self) -> bool:
        return self.__modeler.moveToSolidBarycenter()

    def saveGeometry(self) -> bool:
        return self.__modeler.saveGeometry()

    def restoreGeometry(self) -> bool:
        return self.__modeler.restoreGeometry()

    def rotate(self, degree: float, center: Point2d = Point2d(0.0, 0.0)) -> bool:
        return self.__modeler.rotate(degree, center.x, center.y)

    def elSolve(self, force: ForcesOnSection, uncracked: bool = False) -> bool:
        return self.__modeler.elSolve(force.Fz, -force.Mx, +force.My, uncracked)

    def elStressConcreteNodeAt(self, i) -> float:
        return self.__modeler.elStressConcreteNodeAt(i)

    def elStressSteelNodeAt(self, i) -> float:
        return self.__modeler.elStressSteelNodeAt(i)

    def elStressConcreteNodeId(self, i) -> float:
        return self.__modeler.elStressConcreteNodeId(i)

    def elStressSteelCircleId(self, i) -> float:
        return self.__modeler.elStressSteelCircleId(i)

    def elExtremeStressConcrete(self) -> List[float]:
        return list(self.__modeler.elExtremeStressConcrete())

    def elExtremeStressSteel(self) -> List[float]:
        return list(self.__modeler.elExtremeStressSteel())

    def elTensionPlane(self) -> Tuple[float, float, float]:
        plane = self.__modeler.elTensionPlane()
        return plane[0], plane[1], plane[2]

    def elSectionState(self) -> SectionStates:
        if self.__modeler.elIsTotallyCompressed():
            return SectionStates.COMPRESSED
        elif self.__modeler.elIsTotallyStretched():
            return SectionStates.STRETCHED
        elif self.__modeler.elIsPartialized():
            return SectionStates.PARTIALIZED
        return SectionStates.UNKNOWN

    def elIsCalculated(self) -> bool:
        return self.__modeler.elIsCalculated()

    def elCalOptionUncracked(self) -> bool:
        return self.__modeler.elCalOptionUncracked()

    @property
    def nCoeff(self):
        return self.__modeler.nCoeff()

    @nCoeff.setter
    def nCoeff(self, val):
        if not any([isinstance(val, float), isinstance(val, int)]):
            raise ValueError("nCoeff must be a float type !!!")
        else:
            self.__modeler.setNCoeff(val)


if __name__ == "__main__":
    pass
