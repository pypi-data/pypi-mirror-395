import copy
import math
from enum import Enum
from typing import Any, Dict, List, Literal, Tuple, Union

import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle, PathPatch, Polygon
from matplotlib.path import Path
from matplotlib.ticker import FormatStrFormatter

from pycivil.EXAGeometry.clouds import PointCloud2d
from pycivil.EXAGeometry.geometry import Point2d
from pycivil.EXAStructural.modeler import SectionModeler
from pycivil.EXAStructural.sections import ConcreteSection
from pycivil.EXAUtils.logging import log
from adjustText import adjust_text

class SectionPlotView_Enum(str, Enum):
    SP_VIEW_SECTION = "SP_VIEW_SECTION"
    SP_VIEW_SECTION_NOID = "SP_VIEW_SECTION_NOID"
    SP_VIEW_NODES = "SP_VIEW_NODES"
    SP_VIEW_SOLID_NODES = "SP_VIEW_SOLID_NODES"
    SP_HIDE_SOLID_NODES = "SP_HIDE_SOLID_NODES"
    SP_HIDE_NODES = "SP_HIDE_NODES"
    SP_HIDE_REBAR_ID = "SP_HIDE_REBAR_ID"
    SP_VIEW_GRID = "SP_VIEW_GRID"
    SP_HIDE_GRID = "SP_HIDE_GRID"
    SP_VIEW_TRIANGLES = "SP_VIEW_TRIANGLES"
    SP_VIEW_TRIANGLE_NOID = "SP_VIEW_TRIANGLE_NOID"
    SP_VIEW_MESH = "SP_VIEW_MESH"
    SP_VIEW_STRESSES = "SP_VIEW_STRESSES"


class SectionPlot:
    def __init__(self):
        self.__fig = plt.figure()
        self.__ax = self.__fig.add_subplot(1, 1, 1)
        self.__ax.set_aspect("equal", "datalim")

        # Data to plot
        self.__rcRect: Union[None, ConcreteSection] = None
        self.__modeler: Union[None, SectionModeler] = None
        self.__vertexStresses: Union[Dict[int, float], None] = None
        self.__rebarStresses: Union[Dict[int, float], None] = None

        # Aspect controls
        self.__colorEdge: str = "black"
        self.__textSize: float = 8
        self.__colorTriaLines: str = "blue"
        self.__colorTriaFill: str = "green"
        self.__colorNodes: str = "red"
        self.__plotShapeEdges: bool = True
        self.__plotTriaLines: bool = False
        self.__plotTriaFill: bool = True
        self.__plotTriaShrinkFill: bool = False
        self.__plotTriaShrink: bool = False
        self.__plotNodes: bool = False
        self.__plotNodesId: bool = False
        self.__plotSolidNodes: bool = True
        self.__plotSolidNodesId: bool = True
        self.__plotStresses: bool = False
        self.__plotRebar: bool = True
        self.__plotMeshTria: bool = False
        self.__plotRebarId: bool = True
        self.__plotGrid: bool = False

        self.__ll: Literal[0, 1, 2] = 0

    @property
    def logLevel(self):
        return self.__ll

    @logLevel.setter
    def logLevel(self, value):
        self.__ll = value

    @property
    def plotRebar(self):
        return self.__plotRebar

    @plotRebar.setter
    def plotRebar(self, value):
        self.__plotRebar = value

    @property
    def colorNodes(self):
        return self.__colorNodes

    @colorNodes.setter
    def colorNodes(self, value):
        self.__colorNodes = value

    @property
    def ax(self):
        return self.__ax

    @ax.setter
    def ax(self, value):
        self.__ax = value

    @property
    def colorTriaFill(self):
        return self.__colorTriaFill

    @colorTriaFill.setter
    def colorTriaFill(self, value):
        self.__colorTriaFill = value

    @property
    def plotTriaShrinkFill(self):
        return self.__plotTriaShrinkFill

    @plotTriaShrinkFill.setter
    def plotTriaShrinkFill(self, value):
        self.__plotTriaShrinkFill = value

    @property
    def textSize(self):
        return self.__textSize

    @textSize.setter
    def textSize(self, value):
        self.__textSize = value

    @property
    def vertexStresses(self) -> Union[Dict[int, float], None]:
        return self.__vertexStresses

    @vertexStresses.setter
    def vertexStresses(self, value: Union[Dict[int, float], None] = None):
        self.__vertexStresses = value

    @property
    def rebarStresses(self) -> Union[Dict[int, float], None]:
        return self.__rebarStresses

    @rebarStresses.setter
    def rebarStresses(self, value: Union[Dict[int, float], None] = None):
        self.__rebarStresses = value

    @property
    def plotGrid(self):
        return self.__plotGrid

    @plotGrid.setter
    def plotGrid(self, value):
        self.__plotGrid = value

    @property
    def plotSolidNodesId(self):
        return self.__plotSolidNodesId

    @plotSolidNodesId.setter
    def plotSolidNodesId(self, value):
        self.__plotSolidNodesId = value

    @property
    def modeler(self):
        return self.__modeler

    @modeler.setter
    def modeler(self, value: SectionModeler):
        self.__modeler = value

    def __plotScaled(self, xDataScaled, yDataScaled, refLenght):
        # Scale from reference lenght in data space
        dx = xDataScaled
        dy = yDataScaled
        headScale = 0.02
        i1 = 0
        i2 = 1
        self.__ax.arrow(
            dx[i1],
            dy[i1],
            dx[i2] - dx[i1],
            dy[i2] - dy[i1],
            head_width=refLenght * headScale,
            head_length=refLenght * headScale,
            length_includes_head=True,
        )
        i1 = 1
        i2 = 2
        self.__ax.arrow(
            dx[i1],
            dy[i1],
            dx[i2] - dx[i1],
            dy[i2] - dy[i1],
            head_width=refLenght * headScale,
            head_length=refLenght * headScale,
            length_includes_head=True,
        )
        i1 = 2
        i2 = 0
        self.__ax.arrow(
            dx[i1],
            dy[i1],
            dx[i2] - dx[i1],
            dy[i2] - dy[i1],
            head_width=refLenght * headScale,
            head_length=refLenght * headScale,
            length_includes_head=True,
        )

    @staticmethod
    def __genTriaData(coords: Tuple[float, float, float, float, float, float]) -> Any:
        xData = [coords[0], coords[2], coords[4], coords[0]]
        yData = [coords[1], coords[3], coords[5], coords[1]]

        xg = (xData[0] + xData[1] + xData[2]) / 3
        yg = (yData[0] + yData[1] + yData[2]) / 3

        xDataScaled = [
            (xData[0] - xg) * 0.8 + xg,
            (xData[1] - xg) * 0.8 + xg,
            (xData[2] - xg) * 0.8 + xg,
        ]

        yDataScaled = [
            (yData[0] - yg) * 0.8 + yg,
            (yData[1] - yg) * 0.8 + yg,
            (yData[2] - yg) * 0.8 + yg,
        ]

        polyData = [
            [xData[0], yData[0]],
            [xData[1], yData[1]],
            [xData[2], yData[2]],
        ]

        polyDataScaled = [
            [xDataScaled[0], yDataScaled[0]],
            [xDataScaled[1], yDataScaled[1]],
            [xDataScaled[2], yDataScaled[2]],
        ]

        return xData, yData, xDataScaled, yDataScaled, polyData, polyDataScaled

    def __plotModeler(self, modeler: SectionModeler):
        trianglesCoords = modeler.getTrianglesCoords()

        # We need this for operate in data space
        refLenght = math.sqrt(modeler.calcSolidAreaProperties().area)

        ########################################################################
        #                               TRIANGLES                              #
        ########################################################################
        for k in trianglesCoords:
            coords = trianglesCoords[k]
            (
                xData,
                yData,
                xDataScaled,
                yDataScaled,
                polyData,
                polyDataScaled,
            ) = self.__genTriaData(coords)

            ####################################################################
            #                               FILL                               #
            ####################################################################
            if self.__plotTriaFill:
                self.__ax.add_patch(
                    Polygon(polyData, facecolor=self.__colorTriaFill, alpha=0.3)
                )

            ####################################################################
            #                               LINES                              #
            ####################################################################
            if self.__plotTriaLines:
                self.__ax.plot(xData, yData, color=self.__colorTriaLines)

            ####################################################################
            #                       SHRINK LINES AND FILL                      #
            ####################################################################
            if self.__plotTriaShrinkFill:
                self.__ax.add_patch(
                    Polygon(polyDataScaled, facecolor=self.__colorTriaFill, alpha=0.3)
                )

            if self.__plotTriaShrink:
                self.__plotScaled(xDataScaled, yDataScaled, refLenght)

        ########################################################################
        #                               SHAPE                                  #
        ########################################################################
        trianglesIds = modeler.getTrianglesIds()
        if self.__plotShapeEdges:
            segsId = []
            for k in trianglesIds:
                t = trianglesIds[k]
                # Order by id segments
                seg1 = [t[1], t[0]]
                if t[1] > t[0]:
                    seg1 = [t[0], t[1]]
                if seg1 not in segsId:
                    segsId.append(seg1)
                else:
                    segsId.remove(seg1)

                seg2 = [t[2], t[1]]
                if t[2] > t[1]:
                    seg2 = [t[1], t[2]]
                if seg2 not in segsId:
                    segsId.append(seg2)
                else:
                    segsId.remove(seg2)

                seg3 = [t[0], t[2]]
                if t[0] > t[2]:
                    seg3 = [t[2], t[0]]
                if seg3 not in segsId:
                    segsId.append(seg3)
                else:
                    segsId.remove(seg3)

            for ids in segsId:
                self.__ax.plot(
                    [modeler.getNodeX(ids[0]), modeler.getNodeX(ids[1])],
                    [modeler.getNodeY(ids[0]), modeler.getNodeY(ids[1])],
                    color=self.__colorEdge,
                )

        ########################################################################
        #                                NODES                                 #
        ########################################################################
        if self.__plotNodes or self.__plotSolidNodes:
            if self.__plotNodes:
                nodes = modeler.getNodes()
            else:
                nodes = modeler.getSolidNodes()

            for k in nodes:
                node = nodes[k]
                sc = self.__ax.scatter(
                    node.xn,
                    node.yn,
                    marker="o",
                    color=self.__colorNodes,
                    # linewidths = 3.5
                )
                sizeOfAnnotation = math.sqrt(sc.get_sizes()) / 2 + 2

                text_to_put = ""
                if self.__plotStresses and self.__plotSolidNodesId:
                    stress = self.__vertexStresses[node.id]
                    text_to_put = f"{stress:.1f}"
                else:
                    text_to_put = f"{node.id}"

                if self.__plotNodesId or self.__plotSolidNodesId:
                    self.__ax.annotate(
                        text=text_to_put,
                        xy=(node.xn, node.yn),
                        fontsize=self.__textSize,
                        xytext=(sizeOfAnnotation, sizeOfAnnotation),
                        textcoords="offset points",
                        color="red",
                        ha="left",
                        va="center",
                    )

        ########################################################################
        #                                REBAR                                 #
        ########################################################################
        texts = []
        patches = []
        if self.__plotRebar:
            circles = modeler.getCircles()
            for k in circles:
                circle = circles[k]
                x = circle.center.xn
                y = circle.center.yn
                r = circle.radius
                patch = self.__ax.add_patch(Circle((x, y), r))
                self.__ax.add_patch(Circle((x, y), r, fill=False, edgecolor="black"))
                patches.append(patch)

                if self.__plotStresses and self.__plotRebarId:
                    stress = self.__rebarStresses[circle.id]
                    text_to_put = f"{stress:.0f}"
                else:
                    text_to_put = f"{circle.id}"

                if self.__plotRebarId:
                    # text = self.__ax.annotate(
                    #     text=f"{text_to_put}",
                    #     xy=(x + r, y + r),
                    #     fontsize=self.__textSize,
                    #     # xytext = (sizeOfAnnotation, sizeOfAnnotation),
                    #     # textcoords="offset points",
                    #     ha="left",
                    #     va="center",
                    # )
                    text = self.__ax.text(
                        s=f"{text_to_put}",
                        x=x, # + r,
                        y=y, # + r,
                        fontsize=self.__textSize,
                        # xytext = (sizeOfAnnotation, sizeOfAnnotation),
                        # textcoords="offset points",
                        ha="left",
                        va="center",
                    )
                    texts.append(text)
        #self.__fig.canvas.draw()
        adjust_text(
            texts=texts,
            objects=patches,
            ax=self.__ax,
            max_move=100,
            expand=(1.2, 1.2),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=0.3),
            force_static=(2.0,2.0))

        ########################################################################
        #                               MESHES                                 #
        ########################################################################
        if self.__plotMeshTria:
            for i in range(modeler.meshSize()):
                trianglesCoords = modeler.getTrianglesCoordsAtMesh(i)
                for k in trianglesCoords:
                    coords = trianglesCoords[k]
                    (
                        xData_,
                        yData_,
                        xDataScaled_,
                        yDataScaled_,
                        polyData_,
                        polyDataScaled_,
                    ) = self.__genTriaData(coords)
                    self.__plotScaled(xDataScaled_, yDataScaled_, refLenght)
                    self.__ax.plot(xData_, yData_, color=self.__colorTriaLines)

    def setView(self, opt: SectionPlotView_Enum):
        if opt == SectionPlotView_Enum.SP_VIEW_MESH:
            self.__plotShapeEdges: bool = False
            self.__plotTriaLines: bool = False
            self.__plotTriaFill: bool = False
            self.__plotTriaShrinkFill: bool = False
            self.__plotTriaShrink: bool = False
            self.__plotNodes: bool = False
            self.__plotNodesId: bool = False
            self.__plotRebar: bool = False
            self.__plotMeshTria: bool = True
            self.__plotRebarId: bool = False
            self.__plotGrid: bool = False

        if opt == SectionPlotView_Enum.SP_VIEW_SECTION:
            self.__plotShapeEdges = True
            self.__plotTriaLines = False
            self.__plotTriaFill = True
            self.__plotTriaShrinkFill = False
            self.__plotTriaShrink = False
            self.__plotNodes = False
            self.__plotNodesId = False
            self.__plotRebar = True
            self.__plotRebarId = True
            self.__plotStresses = False

        if opt == SectionPlotView_Enum.SP_VIEW_SECTION_NOID:
            self.__plotShapeEdges = True
            self.__plotTriaLines = False
            self.__plotTriaFill = True
            self.__plotTriaShrinkFill = False
            self.__plotTriaShrink = False
            self.__plotNodes = False
            self.__plotNodesId = False
            self.__plotRebar = True
            self.__plotRebarId = False

        if opt == SectionPlotView_Enum.SP_HIDE_REBAR_ID:
            self.__plotRebarId = False

        if opt == SectionPlotView_Enum.SP_VIEW_NODES:
            self.__plotNodes = True
            self.__plotNodesId = True

        if opt == SectionPlotView_Enum.SP_HIDE_NODES:
            self.__plotNodes = False
            self.__plotNodesId = False

        if opt == SectionPlotView_Enum.SP_VIEW_SOLID_NODES:
            self.__plotNodes = False
            self.__plotNodesId = False
            self.__plotSolidNodes = True
            self.__plotSolidNodesId = True
            self.__plotStresses = False

        if opt == SectionPlotView_Enum.SP_VIEW_STRESSES:
            self.__plotNodes = False
            self.__plotNodesId = False
            self.__plotRebarId = True
            self.__plotSolidNodes = True
            self.__plotSolidNodesId = True
            self.__plotStresses = True

        if opt == SectionPlotView_Enum.SP_HIDE_NODES:
            self.__plotNodes = False
            self.__plotNodesId = False
            self.__plotSolidNodes = False
            self.__plotSolidNodesId = False

        if opt == SectionPlotView_Enum.SP_VIEW_GRID:
            self.__plotGrid = True

        if opt == SectionPlotView_Enum.SP_HIDE_GRID:
            self.__plotGrid = False

        if opt == SectionPlotView_Enum.SP_VIEW_TRIANGLES:
            self.__plotShapeEdges = False
            self.__plotTriaLines = True
            self.__plotTriaFill = True
            self.__plotTriaShrinkFill = True
            self.__plotTriaShrink = True
            self.__plotNodes = True
            self.__plotNodesId = True
            self.__plotRebar = False
            self.__plotRebarId = False

        if opt == SectionPlotView_Enum.SP_VIEW_TRIANGLE_NOID:
            self.__plotShapeEdges = False
            self.__plotTriaLines = True
            self.__plotTriaFill = True
            self.__plotTriaShrinkFill = True
            self.__plotTriaShrink = True
            self.__plotNodes = True
            self.__plotNodesId = False
            self.__plotRebar = False
            self.__plotRebarId = False

    def plot(self):
        self.__ax.cla()
        #self.__ax.set_facecolor("white")
        if self.__plotGrid:
            self.__ax.grid(True, "both")
            self.__ax.minorticks_on()
            self.__ax.set_facecolor("#EBEBEB")

        if self.__modeler is not None:
            self.__plotModeler(self.__modeler)
        else:
            log("ERR", "Modeler does not assigned !!!", self.__ll)

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(
        fname,
        *,
        transparent=None,
        dpi="figure",
        format=None,
        metadata=None,
        bbox_inches=None,
        pad_inches=0.1,
        facecolor=None,
        edgecolor=None,
        backend=None,
        **kwargs,
    ):
        plt.savefig(
            fname,
            dpi=dpi,
            format=format,
            metadata=metadata,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            facecolor=facecolor,
            edgecolor=edgecolor,
            backend=backend,
            transparent=transparent,
            **kwargs,
        )


class Geometry2DPlot:
    def __init__(
        self,
        nrows: int = 1,
        ncols: int = 1,
        figsize: Tuple[float, float] = (7, 7),
        sx: float = 1,
        sy: float = 1,
    ):
        self.__fig = plt.figure(figsize=figsize)

        # Adjust layout
        # self.__fig.subplots_adjust(hspace=0.9, wspace=0.9)

        self.__ax: List[Axes] = [
            self.__fig.add_subplot(nrows, ncols, i + 1) for i in range(nrows * ncols)
        ]
        self.__titles: List[str] = ["" for i in range(len(self.__ax))]
        self.__xlabels: List[str] = ["" for i in range(len(self.__ax))]
        self.__ylabels: List[str] = ["" for i in range(len(self.__ax))]

        # Data to plot
        self.__points: List[Point2d] = []
        self.__pointArray: List[List[Point2d]] = []
        self.__pointClouds: List[PointCloud2d] = []

        # Scale Factor
        self.__sx = sx
        self.__sy = sy

        # Aspect controls
        self.__pointSize: float = 30
        self.__textSize: float = 12
        self.__showPointIndex: bool = True
        self.__showPointIndexArray: bool = True
        self.__showLineArray: bool = False
        self.__showArrow: bool = True
        self.__showLine: bool = True
        self.__colorLines: str = "black"
        self.__colorPoints: str = "red"
        self.__colorPointsArray: List[List[str]] = []

    @property
    def pointSize(self):
        return self.__pointSize

    @pointSize.setter
    def pointSize(self, value: float):
        self.__pointSize = value

    @property
    def textSize(self):
        return self.__textSize

    @textSize.setter
    def textSize(self, value: float):
        self.__textSize = value

    def setXLabel(self, xlabel: List[str]):
        self.__xlabels = xlabel

    def setYLabel(self, ylabel: List[str]):
        self.__ylabels = ylabel

    def setTitles(self, titles: List[str]):
        self.__titles = titles

    def showItems(
        self,
        pointIndex: bool = True,
        arrow: bool = True,
        line: bool = True,
        lineArray: bool = False,
        pointIndexArray: bool = True,
    ):
        self.__showPointIndex = pointIndex
        self.__showArrow = arrow
        self.__showLine = line
        self.__showLineArray = lineArray
        self.__showPointIndexArray = pointIndexArray

    def addPoint(self, point: Point2d) -> None:
        self.__points.append(point)

    def addPointArray(self, array: List[Point2d], colorArray: List[str] = []) -> None:
        self.__pointArray.append(array)

        if len(colorArray) == 0:
            self.__colorPointsArray.append(["black" for i in range(len(array))])
            return

        if len(colorArray) == 1:
            self.__colorPointsArray.append([colorArray[0] for i in range(len(array))])
            return

        if len(colorArray) not in [0, 1, len(array)]:
            raise ValueError(
                f"Len of array {len(array)} must be equal to \
                            len of colorArray {len(colorArray)}"
            )
        else:
            self.__colorPointsArray.append(colorArray)
            return

    def addPointCloud(self, cloud: PointCloud2d) -> None:
        self.__pointClouds.append(cloud)

    def __plotFromPointArray(self, points: List[List[Point2d]]):
        if len(self.__ax) != len(points):
            print("ERR: Can't plot many set of points with one axes")

        else:
            for idx, pts in enumerate(points):
                # save options
                showLineOld = self.__showLine
                self.__showLine = self.__showLineArray

                showPointIndexOld = self.__showPointIndex
                self.__showPointIndex = self.__showPointIndexArray

                self.__plotFromPoint2dLst(
                    pts, self.__ax[idx], self.__colorPointsArray[idx]
                )

                # restore options
                self.__showLine = showLineOld
                self.__showPointIndex = showPointIndexOld

    def __plotFromPoint2dLst(
        self, points: List[Point2d], axes: Axes, color: Union[str, List[str]]
    ):
        for i, p in enumerate(points):
            if isinstance(color, str):
                sc = axes.scatter(
                    [p.x * self.__sx],
                    [p.y * self.__sy],
                    color=color,
                    s=self.__pointSize,
                )
            else:
                sc = axes.scatter(
                    [p.x * self.__sx],
                    [p.y * self.__sy],
                    color=color[i],
                    s=self.__pointSize,
                )

            if self.__showPointIndex:
                sizeOfAnnotation = math.sqrt(sc.get_sizes()[0]) / 2 + 2
                axes.annotate(
                    text=f"{i}",
                    xy=(p.x * self.__sx, p.y * self.__sy),
                    xytext=(sizeOfAnnotation, 0),
                    fontsize=self.__textSize,
                    textcoords="offset points",
                    ha="left",
                    va="center",
                )

            if i < len(points) - 1:
                p0 = points[i]
                p1 = points[i + 1]

                if self.__showLine:
                    axes.plot(
                        [p0.x * self.__sx, p1.x * self.__sx],
                        [p0.y * self.__sy, p1.y * self.__sy],
                        color=self.__colorLines,
                    )

                if self.__showArrow:
                    centerOfArrow = [
                        (p0.x * self.__sx + p1.x * self.__sx) / 2,
                        (p0.y * self.__sy + p1.y * self.__sy) / 2,
                    ]
                    direction = [
                        (p1.x * self.__sx - p0.x * self.__sx),
                        (p1.y * self.__sx - p0.y),
                    ]
                    lenght = math.sqrt(
                        math.pow(direction[0], 2) + math.pow(direction[1], 2)
                    )
                    if not lenght == 0:
                        versor = [
                            direction[0] / lenght / 100,
                            direction[1] / lenght / 100,
                        ]
                        axes.annotate(
                            "",
                            xy=(centerOfArrow[0], centerOfArrow[1]),
                            xytext=(
                                centerOfArrow[0] + versor[0],
                                centerOfArrow[1] + versor[1],
                            ),
                            fontsize=self.__textSize * 2,
                            arrowprops={
                                "arrowstyle": "<-",
                            },
                        )
                    else:
                        print(
                            f"Point at coords {p0} duplicate with index {i} and {i + 1}"
                        )

    def __plotFromPointCloudLst(self, points: List[PointCloud2d]):

        if len(self.__titles) == len(self.__ax):
            for i, t in enumerate(self.__titles):
                self.__ax[i].set_title(t)
        else:
            if len(self.__titles) == 1:
                for a in self.__ax:
                    a.set_title(self.__titles[0])
            else:
                print("ERR: Can't set titles because lenght !!!")

        if len(self.__xlabels) == len(self.__ax):
            for i, t in enumerate(self.__xlabels):
                self.__ax[i].set_xlabel(t)
        else:
            if len(self.__xlabels) == 1:
                for a in self.__ax:
                    a.set_xlabel(self.__xlabels[0])
            else:
                print("ERR: Can't set xlabels because lenght !!!")

        if len(self.__ylabels) == len(self.__ax):
            for i, t in enumerate(self.__ylabels):
                self.__ax[i].set_ylabel(t)
        else:
            if len(self.__ylabels) == 1:
                for a in self.__ax:
                    a.set_ylabel(self.__ylabels[0])
            else:
                print("ERR: Can't set ylabels because lenght !!!")

        if len(self.__ax) == 1:
            for p in points:
                self.__plotFromPoint2dLst(
                    p.getPoints(), self.__ax[0], self.__colorPoints
                )

        else:
            if len(self.__ax) != len(points):
                print("ERR: Can't plot many set of points with one axes")

            else:
                for idx, p in enumerate(points):
                    self.__plotFromPoint2dLst(
                        p.getPoints(), self.__ax[idx], self.__colorPoints
                    )

    def plot(self):

        # Points
        self.__plotFromPoint2dLst(self.__points, self.__ax[0], self.__colorPoints)

        # Point cloud
        self.__plotFromPointCloudLst(self.__pointClouds)

        # Point array
        if len(self.__pointArray) > 0:
            self.__plotFromPointArray(self.__pointArray)

        self.__fig.tight_layout(pad=2)

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(
        fname,
        *,
        transparent=None,
        dpi="figure",
        format=None,
        metadata=None,
        bbox_inches=None,
        pad_inches=0.1,
        facecolor="auto",
        edgecolor="auto",
        backend=None,
        **kwargs,
    ):

        plt.savefig(
            fname,
            dpi=dpi,
            format=format,
            metadata=metadata,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            facecolor=facecolor,
            edgecolor=edgecolor,
            backend=backend,
            transparent=transparent,
            **kwargs,
        )


# def interactionDomainBasePlot2d(vertices, fields, xLabel = 'Nz [N]', yLabel = 'Mz [Nmm]', titleAddStr = None,
# tensionPoints = None, scale_Nx = 0.001, scale_Mz = 0.000001):
def interactionDomainBasePlot2d(vertices, fields, **kwargs):
    if "export" in kwargs:
        fileName = kwargs["export"]
    else:
        fileName = None

    if "dpi" in kwargs:
        dpi = kwargs["dpi"]
    else:
        dpi = None

    if "xLabel" in kwargs:
        xLabel = kwargs["xLabel"]
    else:
        xLabel = "Nz [N]"

    if "yLabel" in kwargs:
        yLabel = kwargs["yLabel"]
    else:
        yLabel = "Mz [Nmm]"

    if "titleAddStr" in kwargs:
        titleAddStr = kwargs["titleAddStr"]
    else:
        titleAddStr = None

    if "tensionPoints" in kwargs:
        tensionPoints = kwargs["tensionPoints"]
    else:
        tensionPoints = None

    if "scale_Nx" in kwargs:
        scale_Nx = kwargs["scale_Nx"]
    else:
        scale_Nx = 0.001

    if "scale_Mz" in kwargs:
        scale_Mz = kwargs["scale_Mz"]
    else:
        scale_Mz = 0.000001

    if "lines" in kwargs:
        lines = kwargs["lines"]
    else:
        lines = []

    if "markers" in kwargs:
        markers = kwargs["markers"]
    else:
        markers = True

    if "savingSingleDomains" in kwargs:
        savingSingleDomains = kwargs["savingSingleDomains"]
    else:
        savingSingleDomains = False

    if "hotPoints" in kwargs:
        hotPoints = kwargs["hotPoints"]
    else:
        hotPoints = False

    if "printDomains" in kwargs:
        printDomains = kwargs["printDomains"]
        if printDomains is None:
            printDomains = list(range(0, len(vertices)))
    else:
        printDomains = list(range(0, len(vertices)))

    """
    if "pointsScale" in kwargs:
        pointsScale = kwargs["pointsScale"]
    else:
        pointsScale = 40
    """
    if isinstance(vertices, list) and len(vertices) != 0:
        # Only one diagrammpython
        if isinstance(vertices[0][0], float) and isinstance(vertices[0][1], float):
            verticesList = [vertices]
            fieldsList = [fields]
        else:
            verticesList = vertices
            fieldsList = fields
    else:
        raise ValueError(
            "Vertices must be a list with lenght > 0 !!! Maybe you need build domain."
        )

    fig, ax = plt.subplots()

    if tensionPoints is not None:
        if len(tensionPoints) > 0:
            tp = np.array(tensionPoints, float)
            ax.scatter(
                tp[:, 0] * scale_Nx,
                tp[:, 1] * scale_Mz,
                marker="+",
                s=2000,
                color=[0, 0, 0],
            )

    # plt.autoscale(enable = None)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xticks(rotation="vertical")
    plt.margins(0.0)
    plt.subplots_adjust(bottom=0.25)
    plt.subplots_adjust(left=0.20)

    if len(lines) != 0:
        for ll in lines:
            x1 = ll[0].x * scale_Nx
            y1 = ll[0].y * scale_Mz
            x2 = ll[1].x * scale_Nx
            y2 = ll[1].y * scale_Mz
            plt.plot([x1, x2], [y1, y2], "k-", lw=2)

    strTitle = "Interaction Domain Nx - Mz"
    if titleAddStr is not None:
        plt.subplots_adjust(top=0.87)
        strTitle = strTitle + "\n" + titleAddStr

    ax.set_title(strTitle)
    ax.grid(True)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2e"))
    ax.xaxis.set_major_formatter(FormatStrFormatter("%.2e"))

    # Cloning list only for plot only with deep
    verticesListCopy = copy.deepcopy(verticesList)

    # Removing columns from 2 to n that contains others values
    for _idx, vertices_i in enumerate(verticesListCopy):
        for idy, v in enumerate(vertices_i):
            vertices_i[idy] = [v[0], v[1]]

    for idx, vertices_i in enumerate(verticesListCopy):

        if idx not in printDomains:
            continue

        codes = [Path.MOVETO] + [Path.LINETO] * (len(vertices_i) - 1)

        vertices_i = np.array(vertices_i, float)

        # setting scale
        vertices_i[:, 0] = vertices_i[:, 0] * scale_Nx
        vertices_i[:, 1] = vertices_i[:, 1] * scale_Mz

        # setting color for hot and cold section
        _edgecolor = "black"
        if isinstance(hotPoints, bool):
            if hotPoints is False:
                _edgecolor = "black"
        if isinstance(hotPoints, list):
            if hotPoints[idx] is False:
                _edgecolor = "black"
            else:
                _edgecolor = "red"

        path = Path(vertices_i, codes)
        pathpatch = PathPatch(path, facecolor="None", edgecolor=_edgecolor)

        ax.add_patch(pathpatch)

        if markers:
            x, y = zip(*path.vertices)  # ?

            colorsMap = np.array(
                [
                    [1, 0, 0, 0.5],
                    [0, 1, 0, 0.5],
                    [0, 0, 1, 0.5],
                    [1, 0, 1, 0.5],
                    [1, 0, 0, 1.0],
                    [0, 1, 0, 1.0],
                    [0, 0, 1, 1.0],
                    [1, 0, 1, 1.0],
                ]
            )

            # Displayng Domain Different colors
            scatt_colors = []
            for f in fieldsList[idx]:
                if f == 1.0:
                    scatt_colors.append(0)
                elif f == 2.0:
                    scatt_colors.append(1)
                elif f == 3.0:
                    scatt_colors.append(2)
                elif f == 4.0:
                    scatt_colors.append(3)
                elif f == 11.0:
                    scatt_colors.append(4)
                elif f == 12.0:
                    scatt_colors.append(5)
                elif f == 13.0:
                    scatt_colors.append(6)
                elif f == 14.0:
                    scatt_colors.append(7)
                else:
                    raise ValueError("The value of f is <%1.4f> not mapped!!!" % f)

            # print('Lunghezza x = %f - Lunghezza scatt_colors %f '%(len(x),len(scatt_colors)))
            ax.scatter(x, y, marker="o", s=40, c=colorsMap[scatt_colors])

        if savingSingleDomains:
            ax.autoscale_view()
            if titleAddStr is not None:
                plt.savefig(titleAddStr + "_domain_" + str("%1.0i" % idx) + ".png")

    ax.autoscale_view()

    if fileName is not None:
        if dpi is not None:
            print("save figure to file name -->", fileName)
            plt.style.use("classic")
            plt.savefig(fileName, bbox_inches="tight", dpi=600)
        else:
            raise ValueError("If fileName is not None must provide dpi argument")
    else:
        plt.show()
