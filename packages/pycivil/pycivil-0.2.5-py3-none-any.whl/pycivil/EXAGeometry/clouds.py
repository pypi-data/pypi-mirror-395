import copy
import pickle
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union
from warnings import warn

from pydantic import BaseModel

from pycivil.EXAGeometry.geometry import Point2d, Point2dMdl, Seg2d, Vector2d


class PointCloud2dMdl(BaseModel):
    points: Optional[List[Point2dMdl]] = None


class PointCloud2d:
    def __init__(self, *args):

        if len(args) == 0:
            self.__points: List[Point2d] = []
            self.__metaData: List[List[Any]] = []
            self.__signs: List[float] = []

        elif len(args) == 1 and isinstance(args[0], list):
            if len(args[0]) == 0:
                self.__points: List[Point2d] = []
                self.__metaData: List[List[Any]] = []
                self.__signs: List[float] = []
            else:
                self.__points: List[Point2d] = [Point2d()] * len(args[0])
                self.__signs: List[float] = [0.0] * (len(args[0]) - 2)
                if isinstance(args[0][0], list):
                    self.__metaData: List[List[Any]] = [[]] * len(args[0])
                    for idx in range(len(self.__points)):
                        metaLenght = len(args[0][idx])
                        assert metaLenght >= 2

                        assert isinstance(args[0][idx][0], (float, int))
                        assert isinstance(args[0][idx][1], (float, int))
                        self.__points[idx] = Point2d(args[0][idx][0], args[0][idx][1])

                        if metaLenght >= 2:
                            self.__metaData[idx] = args[0][idx][2 : (metaLenght + 1)]

                        if idx >= 2:
                            vecStart = Vector2d(
                                self.__points[idx - 2], self.__points[idx - 1]
                            )
                            vecEnd = Vector2d(
                                self.__points[idx - 1], self.__points[idx]
                            )
                            self.__signs[idx - 2] = vecStart.cross(vecEnd)

                elif isinstance(args[0][0], Point2d):
                    self.__metaData: List[List[Any]] = []
                    for idx in range(len(self.__points)):
                        assert isinstance(args[0][idx], Point2d)
                        self.__points[idx] = args[0][idx]
                        if idx >= 2:
                            vecStart = Vector2d(
                                self.__points[idx - 2], self.__points[idx - 1]
                            )
                            vecEnd = Vector2d(
                                self.__points[idx - 1], self.__points[idx]
                            )
                            self.__signs[idx - 2] = vecStart.cross(vecEnd)
                else:
                    raise ValueError("Only list or Point2d for first arg !!!")

        elif len(args) == 1 and isinstance(args[0], PointCloud2dMdl):
            self.__metaData: List[List[Any]] = []
            self.__signs: List[float] = []
            self.__points: List[Point2d] = []
            if args[0].points is not None:
                for p in args[0].points:
                    self.__points.append(Point2d(x=p.xy[0], y=p.xy[1]))
        else:
            raise ValueError("Only one arg list or PointCloud2dMdl !!!")

        self.__index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__index < len(self.__points):
            item = self.__points[self.__index]
            self.__index += 1
            return item
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.__points[key]

    def __str__(self):
        dispstr = self.__points.__str__()
        return dispstr

    def __len__(self):
        return len(self.__points)

    def isConvex(self) -> bool:
        if len(self.__signs) > 0:
            s = self.__signs[0] > 0
            for i in range(1, len(self.__signs)):
                if (self.__signs[i] > 0) != s:
                    return False
            return True
        print(
            "WARNING: Can't know about convexity because lenght is null !!!. Return False"
        )
        return False

    def __eq__(self, __value) -> bool:
        if len(__value) != len(self):
            return False
        for idx in range(len(__value)):
            if self.__points[idx] != __value[idx]:
                return False
        return True

    def getPoints(self):
        return self.__points

    def getMetaAt(self, idx: int) -> List[Any]:
        return self.__metaData[idx]

    def boundingBox(self) -> Tuple[float, float, float, float]:
        bb = [0.0, 0.0, 0.0, 0.0]
        for p in self.__points:
            if p.x < bb[0]:
                bb[0] = p.x
            if p.x > bb[1]:
                bb[1] = p.x
            if p.y < bb[2]:
                bb[2] = p.y
            if p.y > bb[3]:
                bb[3] = p.y

        return bb[0], bb[1], bb[2], bb[3]

    def contains(
        self,
        xp: float,
        yp: float,
        ro: Tuple[float, float],
        convex: bool = True,
        rayFromCenter=True,
        center: Union[Point2d, None] = None,
    ):

        if center is None:
            center = Point2d(0.0, 0.0)

        if not isinstance(xp, float) and not isinstance(yp, int):
            raise ValueError("Only float or int type for N!!!")

        if not isinstance(xp, float) and not isinstance(yp, int):
            raise ValueError("Only float or int type for M!!!")

        if not convex:
            raise ValueError("Only algorithm for convex shape !!!")

        if len(self.__points) < 3:
            raise ValueError("Containts at least 3 points !!!")

        p = Point2d(xp, yp)

        # ro useful for intersection point. Normally ro is estimed
        # with boudingbox calculated during forming interaction
        # domain.
        rox = ro[0]
        roy = ro[1]

        contained: bool = True
        pintersect: List[Point2d] = []
        pintersectFactor: float = 0.0
        pintersectFactors: List[float] = []
        pindex: List[int] = []  # Index that intersection found

        p1 = self.__points[0]
        p2 = self.__points[0 + 1]
        v2 = Vector2d(p2, p1)
        v1 = Vector2d(p1, p)

        minLenght = v1.norm_roxroy(rox, roy)
        if rayFromCenter:
            normro = False
            seg = Seg2d(p2, p1)
            ray = Seg2d(p, center)
            hasIntersection, pint = seg.intersectAndContaints(ray)
            if hasIntersection:
                pintersect.append(pint)
                pintersectFactors.append(ray.extensionFactor(pint))
                pindex.append(0)
        else:
            normro = True

        minPoint = p1
        cross = v1.cross(v2)
        check_contained = True
        for i, _val in enumerate(self.__points[0 : len(self.__points) - 2], 1):
            p1 = self.__points[i]
            p2 = self.__points[i + 1]
            v2 = Vector2d(p2, p1)
            v1 = Vector2d(p1, p)
            if normro:
                minLenght_i = v1.norm_roxroy(rox, roy)
                if minLenght_i < minLenght:
                    minLenght = minLenght_i
                    minPoint = p1
            elif rayFromCenter:
                # if (p2 != p1):
                seg = Seg2d(p2, p1)
                ray = Seg2d(p, center)
                hasIntersection, pint = seg.intersectAndContaints(ray)
                if hasIntersection:
                    found = False
                    for ii in pintersect:
                        # Relative precision for excluding nearest points for
                        # some case precision issue
                        # We can not use i==pint
                        same_point = ii.isEqualTo(pint, rox, roy, 1e-15)
                        if same_point:
                            found = True
                    if not found:
                        pintersect.append(pint)
                        pintersectFactors.append(ray.extensionFactor(pint))
                        pindex.append(i)
            else:
                minLenght_i = v1.norm()
                if minLenght_i < minLenght:
                    minLenght = minLenght_i
                    minPoint = p1

            cross_new = v1.cross(v2)
            if cross * cross_new < 0 and check_contained:
                contained = False
                check_contained = False
            cross = cross_new

        pindexn = -1
        d1 = 0
        d2 = 0
        d3 = 0

        if normro:
            warn("normro not tested !!!")
            return contained, minLenght, minPoint, None

        if len(pintersect) != 2:
            print(
                f"WARNING: intersection with point P=({xp}, {yp}) are {len(pintersect)} not 2 !!!"
            )
            print(f"         seg P1=({p1.x}, {p1.y})-P2=({p2.x}, {p2.y})")
            for p in pintersect:
                print(p)
            return contained, pintersect, pintersectFactor, [pindexn, d1, d2, d3]

        if pintersectFactors[0] < 0:
            pintersectFactor = pintersectFactors[1]
            pindexn = pindex[1]
            pleft = self.__points[pindex[1]]
            pright = self.__points[pindex[1] + 1]
            d1 = pintersect[1].distance(pleft)
            d2 = pintersect[1].distance(pright)
            d3 = pleft.distance(pright)
            ptemp = copy.deepcopy(pintersect)
            pintersect[0] = ptemp[1]
            pintersect[1] = ptemp[0]
        else:
            pintersectFactor = pintersectFactors[0]
            pindexn = pindex[0]
            pleft = self.__points[pindex[0]]
            pright = self.__points[pindex[0] + 1]
            d1 = pintersect[0].distance(pleft)
            d2 = pintersect[0].distance(pright)
            d3 = pleft.distance(pright)

        if pintersectFactor < 1.0:
            contained = False
        else:
            contained = True

        return contained, pintersect, pintersectFactor, [pindexn, d1, d2, d3]

    def save(self, file: Path):
        toSave = {"points": self.__points, "metaData": self.__metaData}
        with open(file, "bw") as f:
            pickle.dump(toSave, f)

    def open(self, file: Path):
        with open(file, "br") as f:
            toRead = pickle.load(f)
            self.__points = toRead["points"]
            self.__metaData = toRead["metaData"]

    def model(self) -> PointCloud2dMdl:
        points: List[Point2dMdl] = [
            Point2dMdl(x=i, y=i, null=True) for i in range(len(self.__points))
        ]
        for i, p in enumerate(points):
            p.xy = (self.__points[i].x, self.__points[i].y)
        return PointCloud2dMdl(points=points)
