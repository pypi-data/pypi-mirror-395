"""
Created on Wed Jan 16 18:02:25 2019

@author: lpaone
"""
from __future__ import annotations

import math
from copy import deepcopy
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel


# Defines points or free vector in 2D space
class Point2d:
    def __init__(
        self,
        x: Union[float, int] = 0.0,
        y: Union[float, int] = 0.0,
        make_null: bool = False,
        coords: Union[Tuple[Union[float, int], Union[float, int]], None] = None,
    ):
        if isinstance(x, (float, int)):
            self.__x = x
            self.__y = y
            self.__isNull: bool = make_null
        else:
            raise ValueError("Point2d init only with float or int !!!")

        if coords is not None:
            self.__x = coords[0]
            self.__y = coords[1]

    def __str__(self):
        return f"Point2d: ({self.__x:.2e},{self.__y:.2e})"

    def __add__(self, other: Point2d) -> Point2d:
        return Point2d(self.__x + other.x, self.__y + other.y)

    def __sub__(self, other: Point2d) -> Point2d:
        return Point2d(self.__x - other.x, self.__y - other.y)

    def __mul__(self, other: Union[float, int]) -> Point2d:
        return Point2d(self.__x * other, self.__y * other)

    def __rmul__(self, other: float) -> Point2d:
        return Point2d(self.__x * other, self.__y * other)

    def __eq__(self, other: Point2d):
        if self.__x == other.x and self.__y == other.y:
            return True
        else:
            return False

    def __repr__(self):
        return str(self)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val: float) -> None:
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val: float) -> None:
        self.__y = val

    def translate(self, dx=0.0, dy=0.0):

        assert type(self.__x) is float or type(self.__x) is int
        assert type(self.__y) is float or type(self.__y) is int

        self.__x = self.__x + dx
        self.__y = self.__y + dy

    def isNull(self) -> bool:
        return self.__isNull

    def isEqualTo(self, other, rox, roy, prec):
        dx = math.sqrt(math.pow(self.__x - other.x, 2) / math.pow(rox, 2))
        dy = math.sqrt(math.pow(self.__y - other.y, 2) / math.pow(roy, 2))
        if dx < prec and dy < prec:
            return True
        else:
            return False

    def distance(self, other):
        return math.sqrt(
            math.pow(self.__x - other.x, 2) + math.pow(self.__y - other.y, 2)
        )

    def midpoint(self, other):
        return Point2d((self.__x + other.x) / 2, (self.__y + other.y) / 2)

    def cross(self, p1, p2):
        x1 = p1.x - self.__x
        y1 = p1.y - self.__y

        x2 = p2.x - self.__x
        y2 = p2.y - self.__y

        return x1 * y2 - x2 * y1

    @staticmethod
    def areaFromTria(p0: Point2d, p1: Point2d, p2: Point2d) -> float:
        assert isinstance(p0.x, (float, int))
        assert isinstance(p0.y, (float, int))
        assert isinstance(p1.x, (float, int))
        assert isinstance(p1.y, (float, int))
        assert isinstance(p2.x, (float, int))
        assert isinstance(p2.y, (float, int))
        return (
            1
            / 2
            * abs(
                p0.x * p1.y * 1
                + p0.y * 1 * p2.x
                + 1 * p1.x * p2.y
                - 1 * p1.y * p2.x
                - p0.y * p1.x * 1
                - p0.x * 1 * p2.y
            )
        )


def boundingBox(p1, p2):
    if not isinstance(p1, Point2d) or not isinstance(p2, Point2d):
        raise Exception("Bounding only for two Point2d !!!")

    assert isinstance(p1.x, (float, int))
    assert isinstance(p1.y, (float, int))
    assert isinstance(p2.x, (float, int))
    assert isinstance(p2.y, (float, int))

    min_x = min(p1.x, p2.x)
    max_x = max(p1.x, p2.x)
    min_y = min(p1.y, p2.y)
    max_y = max(p1.y, p2.y)

    return [min_x, max_x, min_y, max_y]


class Node2d(Point2d):
    def __init__(self, x=0.0, y=0.0, idn=-1):
        Point2d.__init__(self, x, y)
        self.idn = idn

    def __str__(self):
        return f"Node2D: idn = {self.idn:.0f}, x = {self.__x:.3e}, y = {self.__y:.3e}"


# Defines points or free vector in 3D space
class Point3d:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.__x = x
        self.__y = y
        self.__z = z

    def __str__(self):
        return f"Point3D: x = {self.__x:.3e}, y = {self.__y:.3e}, z = {self.__z:.3e}"

    def __add__(self, other) -> Point3d:
        return Point3d(self.__x + other.x, self.__y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3d(self.__x - other.x, self.__y - other.y, self.z - other.z)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val: float) -> None:
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val: float) -> None:
        self.__y = val

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, val: float) -> None:
        self.__z = val

    def tranlate(self, dx=0.0, dy=0.0, dz=0.0):
        self.__x = self.__x + dx
        self.__y = self.__y + dy
        self.z = self.z + dz

    def distanceFrom(self, p: Point3d) -> float:

        if not isinstance(p, Point3d):
            raise Exception("Arg must be a Point3d instance !!!")

        return math.dist([self.__x, self.__y, self.z], [p.x, p.y, p.z])

    # @staticmethod
    # def areaFromTria(p0, p1, p2) -> float:
    # area0 = Point2d.areaFromTria(Point2d(p0.x,p0.y),Point2d(p1.x,p1.y),Point2d(p2.x,p2.y))
    # area1 = Point2d.areaFromTria(Point2d(p0.y,p0.z),Point2d(p1.y,p1.z),Point2d(p2.y,p2.z))
    # area2 = Point2d.areaFromTria(Point2d(p0.x,p0.z),Point2d(p1.x,p1.z),Point2d(p2.x,p2.z))
    # return 1/2 * math.sqrt(area0*area0 + area1*area1 + area2*area2)


def areaFromTria3D(p0: Point3d, p1: Point3d, p2: Point3d) -> float:
    v = Vector3d(p0, p1)
    w = Vector3d(p1, p2)
    return 1 / 2 * math.sqrt(abs(v.scalar(v) * w.scalar(w) - v.scalar(w) * v.scalar(w)))


class Node3d(Point3d):
    def __init__(self, x=0.0, y=0.0, z=0.0, idn=-1):
        Point3d.__init__(self, x, y, z)
        self.idn = idn

    def __str__(self):
        return "Node3D: idn = {:.0f}, x = {:.3e}, y = {:.3e}, z = {:.3e}".format(
            self.idn,
            self.x,
            self.y,
            self.z,
        )

    def __add__(self, other) -> Node3d:
        return Node3d(self.__x + other.x, self.__y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Node3d(self.__x - other.x, self.__y - other.y, self.z - other.z)


class Seg2d:
    def __init__(self, p0: Point2d, p1: Point2d):
        self.__p0 = p0
        self.__p1 = p1

    @property
    def p0(self):
        return self.__p0

    @p0.setter
    def p0(self, val: Point2d) -> None:
        self.__p0 = val

    @property
    def p1(self):
        return self.__p1

    @p1.setter
    def p1(self, val: Point2d) -> None:
        self.__p1 = val

    def len(self) -> float:
        return self.__p0.distance(self.__p1)

    # Find the intersection point by Seg2D in input
    def intersect(self, other: Seg2d) -> Point2d:
        a0 = self.__p1.x - self.__p0.x
        b0 = other.p0.x - other.p1.x
        c0 = other.p0.x - self.__p0.x

        a1 = self.__p1.y - self.__p0.y
        b1 = other.p0.y - other.p1.y
        c1 = other.p0.y - self.__p0.y

        detA = a0 * b1 - a1 * b0
        if detA == 0:
            return Point2d(make_null=True)

        detA_alpha = c0 * b1 - c1 * b0
        alpha = detA_alpha / detA
        return self.__p0 + alpha * (self.__p1 - self.__p0)

    def boundingHasPoint(self, p: Point2d, toll: float = 1e-15):
        bb = boundingBox(self.__p0, self.__p1)
        if (
            p.x < bb[0] - toll
            or p.x > bb[1] + toll
            or p.y < bb[2] - toll
            or p.y > bb[3] + toll
        ):
            return False
        else:
            return True

    # Calculate intersection point from extension of other and self
    def intersectAndContaints(self, other: Seg2d) -> Tuple[bool, Point2d]:
        pint = self.intersect(other)
        m1 = (pint.distance(self.__p0) + pint.distance(self.__p1))/ self.__p0.distance(self.__p1)
        # m2 = (pint.distance(other.p0) + pint.distance(other.p1)) / other.len()
        pint.isNull()
        if abs(m1-1) < 0.0000000001:
            return True, pint
        else:
            return False, pint

        # if not pint.isNull() and self.boundingHasPoint(pint, toll=self.len() / 100000):
        #     return True, pint
        # else:
        #     return False, pint

    # If p is a Point2d calculs factor witch factor * Seg2d = p
    def extensionFactor(self, p):
        vx = self.__p0.x - self.__p1.x
        vy = self.__p0.y - self.__p1.y

        evx = p.x - self.__p1.x
        evy = p.y - self.__p1.y

        f = 1
        if vx != 0.0:
            f = evx / vx
        if vy != 0.0:
            f = evy / vy
        return f

    def __str__(self):
        dispstr = "Point2d i: x = {:.3e}, y = {:.3e} \n".format(
            self.__p0.x,
            self.__p0.y,
        )
        dispstr = dispstr + "Point2d j: x = {:.3e}, y = {:.3e} \n".format(
            self.__p1.x,
            self.__p1.y,
        )
        return dispstr


class Edge2d:
    def __init__(self, *args):
        if len(args) == 2:
            if isinstance(args[0], Node2d) & isinstance(args[1], Node2d) is True:
                self.__node_i = args[0]
                self.__node_j = args[1]
            else:
                raise TypeError("Args must be [Node2D] !!!")
        else:
            raise TypeError("Only two argument !!!")

    def nodeI(self) -> Node2d:
        return self.__node_i

    def nodeJ(self) -> Node2d:
        return self.__node_j

    def __str__(self):
        dispstr = "Node2D i: idn = {:.0f}, x = {:.3e}, y = {:.3e} \n".format(
            self.__node_i.idn,
            self.__node_i.x,
            self.__node_i.y,
        )
        dispstr = dispstr + "Node2D j: idn = {:.0f}, x = {:.3e}, y = {:.3e} \n".format(
            self.__node_j.idn,
            self.__node_j.x,
            self.__node_j.y,
        )
        return dispstr


class Edge3d:
    def __init__(self, *args):
        if len(args) == 2:
            if isinstance(args[0], Node3d) & isinstance(args[1], Node3d) is True:
                self.__node_i = args[0]
                self.__node_j = args[1]
            else:
                raise Exception("Args must be [Node3D] !!!")
        elif len(args) == 0:
            self.__node_i = Node3d()
            self.__node_j = Node3d()
        elif len(args) == 8:
            for i in range(2):
                if isinstance(args[0 + 4 * i], float) is False:
                    raise Exception("Arg n. %e must be float !!!" % (0 + i))
                if isinstance(args[1 + 4 * i], float) is False:
                    raise Exception("Arg n. %e must be float !!!" % (1 + i))
                if isinstance(args[2 + 4 * i], float) is False:
                    raise Exception("Arg n. %e must be float !!!" % (2 + i))
                if isinstance(args[3 + 4 * i], int) is False:
                    raise Exception("Arg n. %e must be int !!!" % (3 + i))
            self.__node_i = Node3d(args[0], args[1], args[2], args[3])
            self.__node_j = Node3d(args[4], args[5], args[6], args[7])
        else:
            raise Exception("Wrong arguments !!!")

    def nodeI(self) -> Node3d:
        return self.__node_i

    def nodeJ(self) -> Node3d:
        return self.__node_j

    def setNodeI(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Node3d) is True:
                self.__node_i = args[0]
            else:
                raise Exception("Arg must be [Node3D] !!!")
        else:
            raise Exception("Only one argument !!!")

    def setNodeJ(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Node3d) is True:
                self.__node_j = args[0]
            else:
                raise Exception("Arg must be [Node3D] !!!")
        else:
            raise Exception("Only one argument !!!")

    def __str__(self):
        dispstr = (
            "Node3D i: idn = {:.0f}, x = {:.3e}, y = {:.3e}, z = {:.3e} \n".format(
                self.__node_i.idn,
                self.__node_i.x,
                self.__node_i.y,
                self.__node_i.z,
            )
        )
        dispstr = (
            dispstr
            + "Node3D j: idn = {:.0f}, x = {:.3e}, y = {:.3e}, z = {:.3e} \n".format(
                self.__node_j.idn,
                self.__node_j.x,
                self.__node_j.y,
                self.__node_j.z,
            )
        )
        return dispstr

    def lenght(self):
        return math.sqrt(
            math.pow(self.__node_j.x - self.__node_i.x, 2)
            + math.pow(self.__node_j.y - self.__node_i.y, 2)
            + math.pow(self.__node_j.z - self.__node_i.z, 2)
        )


class Polyline2d:
    """
    List of Nodes2D
    """

    def __init__(self, *args):
        if len(args) == 0:
            raise TypeError("Only one argument !!!")
        elif len(args) == 1:
            lst = args[0]
            if isinstance(lst, list) is True:
                for i in lst:
                    if isinstance(i, Node2d) is False:
                        raise TypeError("List must be [Node2D] formed !!!")
                self.__node = lst
            else:
                raise TypeError("First arg must be type List !!!")
        elif len(args) > 1:
            raise TypeError("Only one argument !!!")

    def __str__(self):
        dispstr = "Polyline2d: size is %.0f \n" % len(self.__node)
        for n in self.__node:
            dispstr = (
                dispstr
                + "Node2D: idn = {:.0f}, x = {:.3e}, y = {:.3e} \n".format(
                    n.idn,
                    n.x,
                    n.y,
                )
            )
        return dispstr

    def getNodes(self):
        return self.__node

    def size(self) -> int:
        return len(self.__node)

    def setClosed(self):
        self.__node.append(self.__node[0])
        return

    def isClosed(self):
        sz = len(self.__node)
        if self.__node[0] == self.__node[sz - 1]:
            return True
        else:
            return False

    def translate(
        self, pStart: Union[Point2d, None], pEnd: Union[Point2d, None]
    ) -> None:
        if pStart is None:
            pStart = Point2d()
        if pEnd is None:
            pEnd = Point2d()

        v = pEnd - pStart
        for node in self.__node:
            node.translate(v.x, v.y)

    def vertexNb(self):
        return len(self.__node)

    def vertexAt(self, i):
        return len(self.__node[i])


class Polyline3d:
    """
    List of Nodes3D
    """

    def __init__(self, *args):
        if len(args) == 0:
            raise Exception("Only one argument !!!")
        elif len(args) == 1:
            lst = args[0]
            if isinstance(lst, list) is True:
                for i in lst:
                    if isinstance(i, Node3d) is False:
                        raise Exception("List must be [Node3D] formed !!!")
                self.__node = lst
            else:
                raise Exception("First arg must be type List !!!")
        elif len(args) > 1:
            raise Exception("Only one argument !!!")

    def __str__(self):
        dispstr = "Polyline3d: size is %.0f \n" % len(self.__node)
        for n in self.__node:
            dispstr = (
                dispstr
                + "Node3D: idn = {:.0f}, x = {:.3e}, y = {:.3e}, z = {:.3e}\n".format(
                    n.idn,
                    n.x,
                    n.y,
                    n.z,
                )
            )
        return dispstr

    def setClosed(self):
        self.__node.append(self.__node[0])
        return

    def isClosed(self):
        sz = len(self.__node)
        if self.__node[0] == self.__node[sz - 1]:
            return True
        else:
            return False

    def vertexNb(self):
        return len(self.__node)

    def vertexAt(self, i):
        return len(self.__node[i])


# Defines points or free vector in 3D space
class Vector2d:
    def __init__(
        self,
        p0: Point2d = Point2d(make_null=True),
        p1: Point2d = Point2d(make_null=True),
        vx: float = 0.0,
        vy: float = 0.0,
    ):

        if isinstance(p0, Point2d) and isinstance(p1, Point2d):
            if not p0.isNull() and not p1.isNull():
                self.vx = p1.x - p0.x
                self.vy = p1.y - p0.y
                return
        else:
            raise TypeError("p0 and p1 must be Point2d instances")

        self.vx = vx
        self.vy = vy

    def __str__(self):
        return f"Vector2D: vx = {self.vx:.3e}, vy = {self.vy:.3e}"

    def __add__(self, other: Vector2d) -> Vector2d:
        return Vector2d(vx=self.vx + other.vx, vy=self.vy + other.vy)

    def __sub__(self, other: Vector2d):
        return Vector2d(vx=self.vx - other.vx, vy=self.vy - other.vy)

    # def __mul__(self, scale):
    #    return Vector3d(self.vx*scale,self.vy*scale,self.z*scale)

    def __rmul__(self, scale):
        return Vector2d(vx=self.vx * scale, vy=self.vy * scale)

    #       _    _    _            _         _         _
    #     | x    y    z  |   y1*z2*x + z1*x2*y + x1*y2*z +
    #  det| x1   y1   z1 | =       _         _         _
    #     | x2   y2   z2 |  -y2*z1*x - x1*z2*y - x2*y1*z
    #
    def cross(self, other: Vector2d):
        x1 = self.vx
        y1 = self.vy

        x2 = other.vx
        y2 = other.vy

        return x1 * y2 - x2 * y1

    def norm(self):
        return math.sqrt(math.pow(self.vx, 2) + math.pow(self.vy, 2))

    def norm_roxroy(self, rox=1.0, roy=1.0):
        return math.sqrt(math.pow(self.vx / rox, 2) + math.pow(self.vy / roy, 2))

    def normalize(self):
        n = self.norm()
        if n != 0:
            self.vx = self.vx / n
            self.vy = self.vy / n
        else:
            raise Exception("Vector 2D null !!!")
        return self

    def rotate(self, angle: float) -> Vector2d:
        hold_vx = self.vx
        hold_vy = self.vy
        alpha = math.radians(angle)
        self.vx = (math.cos(alpha)) * hold_vx + (-math.sin(alpha)) * hold_vy
        self.vy = (math.cos(alpha)) * hold_vy + (math.sin(alpha)) * hold_vx

        return self


# Defines points or free vector in 3D space
class Vector3d:
    def __init__(self, *args):
        if len(args) == 3:
            for a in args:
                if isinstance(a, float) is False and isinstance(a, int) is False:
                    raise Exception("With len args == 3 only float or int type !!!")

            self.vx = float(args[0])
            self.vy = float(args[1])
            self.vz = float(args[2])

        elif len(args) == 2:
            for a in args:
                if isinstance(a, Point3d) is False:
                    raise Exception("With len args == 2 only Point3d type !!!")

            self.vx = args[1].x - args[0].x
            self.vy = args[1].y - args[0].y
            self.vz = args[1].z - args[0].z

        elif len(args) == 0:
            self.vx = 0.0
            self.vy = 0.0
            self.vz = 0.0

        else:
            raise Exception("Wrong args !!!")

    def __str__(self):
        return f"Vector3D: vx = {self.vx:.3e}, vy = {self.vy:.3e}, vz = {self.vz:.3e}"

    def __add__(self, other: Vector3d) -> Vector3d:
        return Vector3d(self.vx + other.vx, self.vy + other.vy, self.vz + other.vz)

    def __sub__(self, other: Vector3d) -> Vector3d:
        return Vector3d(self.vx - other.vx, self.vy - other.vy, self.vz - other.vz)

    # def __mul__(self, scale):
    #    return Vector3d(self.vx*scale,self.vy*scale,self.z*scale)

    def __rmul__(self, scale):
        return Vector3d(self.vx * scale, self.vy * scale, self.vz * scale)

    #       _    _    _            _         _         _
    #     | x    y    z  |   y1*z2*x + z1*x2*y + x1*y2*z +
    #  det| x1   y1   z1 | =       _         _         _
    #     | x2   y2   z2 |  -y2*z1*x - x1*z2*y - x2*y1*z
    #
    def cross(self, other):
        x1 = self.vx
        y1 = self.vy
        z1 = self.vz
        x2 = other.vx
        y2 = other.vy
        z2 = other.vz
        x3 = y1 * z2 - y2 * z1
        y3 = z1 * x2 - x1 * z2
        z3 = x1 * y2 - x2 * y1
        return Vector3d(x3, y3, z3)

    def norm(self):
        return math.sqrt(
            math.pow(self.vx, 2) + math.pow(self.vy, 2) + math.pow(self.vz, 2)
        )

    def normalize(self):
        n = self.norm()
        if n != 0:
            self.vx = self.vx / n
            self.vy = self.vy / n
            self.vz = self.vz / n
        else:
            raise Exception("Vector 3D null !!!")
        return self

    def scalar(self, other):
        return self.vx * other.vx + self.vy * other.vy + self.vz * other.vz


# Sum vector to point in affine space
def affineSum2d(p: Point2d, v: Vector2d) -> Point2d:
    return Point2d(p.x + v.vx, p.y + v.vy)


# Make a points array with equal space between theme
# Extremes stand for include first and last point
def twoPointsDivide(
    p0: Point2d, p1: Point2d, nb: int, extremes: bool = True
) -> List[Point2d]:
    if nb < 1:
        raise ValueError("nb must be >=1")
    lPoints = []
    if extremes:
        lPoints.append(deepcopy(p0))
    vDir = Vector2d(p0, p1).normalize()
    space = p0.distance(p1) / nb
    for i in range(1, nb):
        lPoints.append(affineSum2d(p0, space * i * vDir))
    if extremes:
        lPoints.append(deepcopy(p1))
    return lPoints


def twoPointsMiddle(p0: Point2d, p1: Point2d) -> Point2d:
    return Point2d((p0.x + p1.x) / 2, (p0.y + p1.y) / 2)


# Copy of points translated with offset
def twoPointsOffset(
    p0: Point2d, p1: Point2d, offset: float = 0.0
) -> Tuple[Point2d, Point2d]:
    nDir = offset * Vector2d(p0, p1).normalize().rotate(90)
    return affineSum2d(p0, nDir), affineSum2d(p1, nDir)


class Point2dMdl(BaseModel):
    xy: Optional[Tuple[float, float]] = None
