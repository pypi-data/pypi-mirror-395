import math
from enum import Enum
from typing import Literal, Union

from pycivil.EXAGeometry.geometry import (
    Edge3d,
    Node2d,
    Node3d,
    Point2d,
    Point3d,
    Polyline2d,
    Vector3d,
)


class Frame:
    def __init__(self, *args):
        if len(args) == 0:
            raise TypeError("Only one argument !!!")
        elif len(args) == 1:
            if isinstance(args[0], Edge3d) is True:
                self.__axis = args[0]
                self.__id = -1
                self.__reference = Point3d()
                self.__shape = None
            else:
                raise TypeError("Arg must be [Edge3D] !!!")
        elif len(args) == 8:
            for i in range(2):
                if isinstance(args[0 + 4 * i], float) is False:
                    raise TypeError("Arg n. %e must be float !!!" % (0 + i))
                if isinstance(args[1 + 4 * i], float) is False:
                    raise TypeError("Arg n. %e must be float !!!" % (1 + i))
                if isinstance(args[2 + 4 * i], float) is False:
                    raise TypeError("Arg n. %e must be float !!!" % (2 + i))
                if isinstance(args[3 + 4 * i], int) is False:
                    raise TypeError("Arg n. %e must be int !!!" % (3 + i))
            self.__axis = Edge3d(
                Node3d(args[0], args[1], args[2], args[3]),
                Node3d(args[4], args[5], args[6], args[7]),
            )
            self.__id = -1
            self.__reference = Point3d()
            self.__shape = None
        else:
            raise TypeError("Wrong arguments !!!")

    def __str__(self):
        dispstr = "Frame Object: \n"
        dispstr = dispstr + "------------- \n"
        dispstr = dispstr + "id: " + str(self.__id) + "\n"
        dispstr = dispstr + "axis--> \n"
        dispstr = dispstr + str(self.__axis)
        dispstr = dispstr + "reference--> \n"
        dispstr = dispstr + str(self.__reference) + "\n"
        if self.__shape is not None:
            dispstr = dispstr + "Shape--> \n"
            dispstr = dispstr + str(self.__shape) + "\n"
        return dispstr

    # Fix y local axis
    def setReference(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Point3d):
                self.__reference = args[0]
            else:
                raise Exception("Arg must be [Point3D] !!!")
        elif len(args) == 3:
            if isinstance(args[0], float) is False:
                raise Exception("Arg nb 1 must be float !!!")
            if isinstance(args[1], float) is False:
                raise Exception("Arg nb 2 must be float !!!")
            if isinstance(args[2], float) is False:
                raise Exception("Arg nb 1 must be float !!!")
            self.__reference = Point3d(args[0], args[1], args[2])
        else:
            raise Exception("Wrong arguments !!!")

    def getXLocalAxis(self):
        return Vector3d(self.__axis.nodeI(), self.__axis.nodeJ()).normalize()

    def getZLocalAxis(self):
        xAxis = self.getXLocalAxis()
        yAxisDir = Vector3d(self.__axis.nodeI(), self.__reference)
        if xAxis.cross(yAxisDir).norm() == 0:
            raise Exception("Null cross product: referenze point bad defined !!!")
        return xAxis.cross(yAxisDir).normalize()

    def getYLocalAxis(self):
        return self.getZLocalAxis().cross(self.getXLocalAxis())

    # Shape
    def setShape(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Shape):
                self.__shape = args[0]
            else:
                raise Exception("Arg must be [Shape] !!!")
        else:
            raise Exception("Wrong arguments !!!")

    def nodeI(self):
        return self.__axis.nodeI()

    def nodeJ(self):
        return self.__axis.nodeJ()

    def lenght(self):
        return self.__axis.lenght()


class ShapesEnum(int, Enum):
    SHAPE_NONE = -1
    SHAPE_POLY = 1
    SHAPE_RECT = 101
    SHAPE_CIRC = 102
    SHAPE_AREA = 103


class Shape:
    def __init__(
        self,
        ids: int = -1,
        typ: ShapesEnum = ShapesEnum.SHAPE_NONE,
        originX: float = 0.0,
        originY: float = 0.0,
    ):
        self.__ids = ids
        self.__type = typ
        self.__o = Point2d(originX, originY)

    def getIds(self):
        return self.__ids

    def getType(self) -> ShapesEnum:
        return self.__type

    def getDesc(self):
        return "generic"

    def setId(self, ids):
        self.__ids = ids

    def setOrigin(self, point: Union[Point2d, None]) -> None:
        if point is None:
            point = Point2d(0.0)

        self.__o.x = point.x
        self.__o.y = point.y

    def getOrigin(self):
        return self.__o

    def getArea(self) -> float:
        raise NotImplementedError("getArea() not implemented for subclass !!!")

    def getDiameter(self):
        return 2 * math.sqrt(self.getArea() / math.pi)

    def getShapePoint(self, idstr: str) -> Point2d:
        if isinstance(idstr, str):
            if idstr == "O":
                return self.getOrigin()
            elif idstr == "G":
                return self.getOrigin()
            else:
                raise Exception("Point str undefined !!!")
        return Point2d()

    def translate(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ) -> None:
        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()

        assert isinstance(pStart.x, (float, int))
        assert isinstance(pStart.y, (float, int))
        assert isinstance(pEnd.x, (float, int))
        assert isinstance(pEnd.y, (float, int))
        self.__o.translate(pEnd.x - pStart.x, pEnd.y - pStart.y)

    def vertexNb(self):
        return 0

    def vertexAt(self, i):
        raise Exception("Vertex for [Shape] objects not defined !!!")

    def vertexMaxInY(self):
        if self.vertexNb() == 0:
            raise Exception("Cannot find in 0 vertices number max in Y !!!")

        val = []
        vertex = []
        for i in range(self.vertexNb()):
            val.append(self.vertexAt(i).y)
            vertex.append(self.vertexAt(i))

        return max(val), vertex[val.index(max(val))]

    def vertexMaxInX(self):
        if self.vertexNb() == 0:
            raise Exception("Cannot find in 0 vertices number max in X !!!")

        val = []
        vertex = []
        for i in range(self.vertexNb()):
            val.append(self.vertexAt(i).x)
            vertex.append(self.vertexAt(i))

        return max(val), vertex[val.index(max(val))]

    def vertexMinInY(self):
        if self.vertexNb() == 0:
            raise Exception("Cannot find in 0 vertices number min in Y !!!")

        val = []
        vertex = []
        for i in range(self.vertexNb()):
            val.append(self.vertexAt(i).y)
            vertex.append(self.vertexAt(i))

        return min(val), vertex[val.index(min(val))]

    def vertexMinInX(self):
        if self.vertexNb() == 0:
            raise Exception("Cannot find in 0 vertices number min in X !!!")

        val = []
        vertex = []
        for i in range(self.vertexNb()):
            val.append(self.vertexAt(i).x)
            vertex.append(self.vertexAt(i))
        return min(val), vertex[val.index(min(val))]

    def __str__(self):
        dispstr = "Shape Object: \n"
        dispstr = dispstr + "--------------- \n"
        dispstr = dispstr + "  id: " + str(self.__ids) + "\n"
        dispstr = dispstr + "type: " + str(self.__type) + " " + self.getDesc() + "\n"
        return dispstr


class ShapePoly(Shape):
    def __init__(self, *args):
        if len(args) == 0:
            raise Exception("Only one or >= 9 argument !!!")
        elif len(args) == 1:
            Shape.__init__(self, -1, ShapesEnum.SHAPE_POLY, 0, 0)
            if isinstance(args[0], Polyline2d) is True:
                self.__polyline = args[0]
            else:
                raise Exception("Arg unknown !!!")
        elif len(args) >= 9:
            Shape.__init__(self, -1, ShapesEnum.SHAPE_POLY, 0, 0)
            # lst = []
            if (len(args) / 3.0 - int(len(args) / 3.0)) != 0:
                raise Exception("Args must be multiple of 3 !!!")
            idx = int(len(args) / 3.0)
            lst = []
            for i in range(idx):
                if isinstance(args[0 + i * 3], float) is False:
                    raise Exception("Args 1*n must be only float !!!")
                if isinstance(args[1 + i * 3], float) is False:
                    raise Exception("Args 2*n must be only float !!!")
                if isinstance(args[2 + i * 3], int) is False:
                    raise Exception("Args 3*n must be only int !!!")
                lst.append(Node2d(args[0 + i * 3], args[1 + i * 3], args[2 + i * 3]))
            self.__polyline = Polyline2d(lst)
        else:
            raise Exception("Wrong arguments !!!")

    def getShapePoint(self, idstr):
        if isinstance(idstr, str):
            if idstr == "O":
                return self.getOrigin()
            elif idstr == "G":
                raise Exception("Not defined barycenter for Poliline2D!!!")
            else:
                raise Exception("Point str undefined !!!")

    def getDesc(self):
        return "polygonar"

    def __str__(self):
        return (
            super().__str__()
            + "\n"
            + "Data embedded-->\n"
            + self.__polyline.__str__()
            + "\n"
        )

    def translate(self, pStart: Point2d, pEnd: Point2d) -> None:

        super().translate(pStart, pEnd)
        self.__polyline.translate(pStart, pEnd)

    def getPolyline2D(self):
        return self.__polyline


class ShapeRect(Shape):
    """Class that instantiate a rectangular shape with width and height

    Class that instantiate a rectangular shape with width and height.
    The origin point from default is in x = 0 y = 0.
    Special points are TL (top left), TR (top right), BL (bottom left),
    BR (bottom right), MB (medium bottom), MT (medium top), O (origin),
    G (geometrical barycenter).

    """

    def __init__(
        self,
        width: float = 0.0,
        height: float = 0.0,
        ids: int = -1,
        xo: float = 0.0,
        yo: float = 0.0,
    ):
        super().__init__(ids, ShapesEnum.SHAPE_RECT, xo, yo)
        self.__w = width
        self.__h = height
        self.__vertexFromMDimensions()

    def __vertexFromMDimensions(self):
        o = self.getOrigin()
        assert type(o.x) is float
        assert type(o.y) is float
        self.__TL = Point2d(o.x - self.__w / 2.0, o.y + self.__h / 2.0)
        self.__TR = Point2d(o.x + self.__w / 2.0, o.y + self.__h / 2.0)
        self.__BL = Point2d(o.x - self.__w / 2.0, o.y - self.__h / 2.0)
        self.__BR = Point2d(o.x + self.__w / 2.0, o.y - self.__h / 2.0)

    def w(self):
        return self.__w

    def h(self):
        return self.__h

    def setDimH(self, h):
        self.__h = h
        self.__vertexFromMDimensions()

    def setDimW(self, w):
        self.__w = w
        self.__vertexFromMDimensions()

    def getArea(self) -> float:
        return self.__w * self.__h

    def getDesc(self):
        return "rectangular"

    def getShapePoint(
        self, idstr: Literal["O", "G", "TL", "TR", "BL", "BR", "MB", "MT"]
    ) -> Point2d:

        if isinstance(idstr, str):
            if idstr == "O":
                return self.getOrigin()
            elif idstr == "G":
                return (self.__TL + self.__BR) * 0.5
            elif idstr == "TL":
                return self.__TL
            elif idstr == "TR":
                return self.__TR
            elif idstr == "BL":
                return self.__BL
            elif idstr == "BR":
                return self.__BR
            elif idstr == "MB":
                return (self.__BL + self.__BR) * 0.5
            elif idstr == "MT":
                return (self.__TL + self.__TR) * 0.5
            else:
                raise ValueError("Point str undefined !!!")
        else:
            raise ValueError("idstr must be a str type !!!")

    def translate(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ) -> None:
        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()

        super().translate(pStart, pEnd)

    def vertexNb(self):
        return 4

    def vertexAt(self, i):
        if i == 0:
            return self.getShapePoint("BL")
        elif i == 1:
            return self.getShapePoint("BR")
        elif i == 2:
            return self.getShapePoint("TL")
        elif i == 3:
            return self.getShapePoint("TR")
        else:
            raise Exception("i out of the bound !!!")

    def __str__(self):
        dispstr = super().__str__()
        dispstr = dispstr + "Data embedded-->\n"
        dispstr = dispstr + "b = " + str(self.__w) + " h = " + str(self.__h) + "\n"
        dispstr = dispstr + "Origin in " + self.getOrigin().__str__() + "\n"
        return dispstr


class ShapeCircle(Shape):
    def __init__(
        self,
        radius: float = 0.0,
        posX: float = 0.0,
        posY: float = 0.0,
        ids: int = -1,
        center: Point2d = Point2d(make_null=True),
    ):
        self.__r: float = radius
        if not center.isNull():
            posX = center.x
            posY = center.y

        super().__init__(ids, ShapesEnum.SHAPE_CIRC, posX, posY)

    def getRadius(self) -> float:
        return self.__r

    def getDesc(self) -> str:
        return "circle"

    def getShapePoint(self, idstr: Literal["O", "G", "C"]) -> Union[Point2d, None]:
        if isinstance(idstr, str):
            if idstr == "O" or idstr == "G" or idstr == "C":
                return Point2d(self.getOrigin().x, self.getOrigin().y)
            else:
                raise Exception("Point str undefined !!!")

    def center(self) -> Point2d:
        return Point2d(self.getOrigin().x, self.getOrigin().y)

    def translate(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ) -> None:

        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()

        return super().translate(pStart, pEnd)

    def __str__(self):
        dispstr = super().__str__()
        dispstr = dispstr + "Data embedded-->\n"
        dispstr = dispstr + "r = " + str(self.__r) + "\n"
        dispstr = dispstr + "Origin in " + self.getOrigin().__str__() + "\n"
        return dispstr


class ShapeArea(Shape):
    def __init__(
        self, area: float = 0.0, ids: int = -1, xo: float = 0.0, yo: float = 0.0
    ):
        Shape.__init__(self, ids, ShapesEnum.SHAPE_AREA, xo, yo)
        self.__area = area

    def setArea(self, a):
        self.__area = a

    def getArea(self) -> float:
        return self.__area

    def getDesc(self):
        return "area"

    def getShapePoint(self, idstr: str) -> Point2d:

        if isinstance(idstr, str):
            if idstr == "O":
                return self.getOrigin()
            elif idstr == "G":
                return self.getOrigin()
            else:
                raise Exception("Point str undefined !!!")

        return Point2d()

    def __str__(self):
        dispstr = super().__str__()
        dispstr = dispstr + "Data embedded-->\n"
        dispstr = dispstr + "area = " + str(self.__area) + "\n"
        dispstr = dispstr + "Origin in " + self.getOrigin().__str__() + "\n"
        return dispstr
