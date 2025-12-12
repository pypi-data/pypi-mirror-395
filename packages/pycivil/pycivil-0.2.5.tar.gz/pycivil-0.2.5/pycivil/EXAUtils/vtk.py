import glob
import json
import os
import uuid
from enum import Enum
from typing import Any, Dict, List, Union

import vtkmodules.all as vtk

# Node3d is point with id
from pycivil.EXAGeometry.geometry import Node3d, Point3d, areaFromTria3D
from pycivil.EXAUtils.logging import log


class FileType(Enum):
    VTM_TYPE = 0
    VTU_TYPE = 1


class Parser:
    def __init__(self) -> None:
        self.__currentFile: int = 0
        self.__files: List[str] = []
        self.__filesSuffix: str = ""
        self.__dataParsed: Any = {}
        self.__hashTable_Blocks: Dict[str, int] = {}
        self.__type: FileType = FileType.VTM_TYPE

    def parse(
        self, files: str = "", type: FileType = FileType.VTM_TYPE, ll: int = 1
    ) -> bool:
        # self.__type = type
        return self.__parse__(files, ll)

    def setFileType(self, type: FileType):
        self.__type = type

    def __parse__(self, files: str = "", ll: int = 1) -> bool:

        if self.__type == FileType.VTM_TYPE:
            self.__filesSuffix = ".vtm"

        elif self.__type == FileType.VTU_TYPE:
            self.__filesSuffix = ".vtu"

        else:
            log(
                "ERR",
                "File type UNKNOWN !!!",
                ll,
            )
            return False

        if os.path.exists(files):
            if os.path.isfile(files):
                self.__files = [files]
            else:
                if os.path.isdir(files):
                    filesList = glob.glob(
                        os.path.join(
                            os.path.expanduser(files), "*" + self.__filesSuffix
                        )
                    )
                    if len(filesList) > 0:
                        self.__files = filesList
                    else:
                        log(
                            "ERR",
                            "None file in path <{}> with suffix <{}> !!!".format(
                                files, self.__filesSuffix
                            ),
                            ll,
                        )
                        return False
                else:
                    log("ERR", "Files arg is not file and dir !!!", ll)
                    return False
        else:
            log("ERR", "Files arg file and dir dont exists !!!", ll)
            return False

        log("INF", "Files charged: \n{}".format("\n".join(self.__files)), ll)
        log("INF", f"Current is *{self.__files[self.__currentFile]}*", ll)

        dataDict: Any = {}
        for f in self.__files:
            dataDict[f] = {"ReaderData": {}}

            log("INF", "*" * len(f), ll)
            log("INF", f, ll)
            log("INF", "*" * len(f), ll)

            if self.__type == FileType.VTM_TYPE:
                reader = vtk.vtkXMLMultiBlockDataReader()  # type: ignore

            if self.__type == FileType.VTU_TYPE:
                reader = vtk.vtkXMLUnstructuredGridReader()  # type: ignore

            reader.SetFileName(f)
            reader.Update()

            log("INF", "**************", ll)
            log("INF", "PARSING READER", ll)
            log("INF", "**************", ll)

            log(
                "INF",
                f"Arrays by cells  number is: {reader.GetNumberOfCellArrays()}",
                ll,
            )
            dataDict[f]["ReaderData"]["CellArrayName"] = []
            for i in range(reader.GetNumberOfCellArrays()):
                dataDict[f]["ReaderData"]["CellArrayName"].append(
                    reader.GetCellArrayName(i)
                )
                log(
                    "INF",
                    f'Array nb.{i} name --> "{reader.GetCellArrayName(i)}"',
                    ll,
                )

            log(
                "INF",
                "Arrays by points number is : {}".format(
                    reader.GetNumberOfPointArrays()
                ),
                ll,
            )
            dataDict[f]["ReaderData"]["PointArrayName"] = []
            for i in range(reader.GetNumberOfPointArrays()):
                dataDict[f]["ReaderData"]["PointArrayName"].append(
                    reader.GetPointArrayName(i)
                )
                log(
                    "INF",
                    f'Array nb.{i} nome --> "{reader.GetPointArrayName(i)}"',
                    ll,
                )

            dataDict[f]["DataSet"] = {}
            log(
                "INF",
                f"Output ports number is: {reader.GetNumberOfOutputPorts()}",
                ll,
            )
            dataSet = reader.GetOutput()

            log("INF", "***************", ll)
            log("INF", "PARSING DATASET", ll)
            log("INF", "***************", ll)
            log(
                "INF",
                f"Cells  number in dataset: {dataSet.GetNumberOfCells()}",
                ll,
            )
            log(
                "INF",
                f"Points number in dataset: {dataSet.GetNumberOfPoints()}",
                ll,
            )
            if self.__type == FileType.VTM_TYPE:
                log(
                    "INF",
                    f"Block number in dataser: {dataSet.GetNumberOfBlocks()}",
                    ll,
                )
                dataDict[f]["DataSet"]["NumberOfBlocks"] = dataSet.GetNumberOfBlocks()

            if self.__type == FileType.VTU_TYPE:
                log(
                    "INF",
                    "The dataset isn't multiblock. Nb of blocks setted to 0.",
                    ll,
                )
                dataDict[f]["DataSet"]["NumberOfBlocks"] = 0

            dataDict[f]["DataSet"]["NumberOfCells"] = dataSet.GetNumberOfCells()
            dataDict[f]["DataSet"]["NumberOfPoints"] = dataSet.GetNumberOfPoints()

            fieldData = dataSet.GetFieldData()
            log(
                "INF",
                "Arrays by fieldData number is : {}".format(
                    fieldData.GetNumberOfArrays()
                ),
                ll,
            )
            dataDict[f]["FieldData"] = {}
            space = " " * 1
            for i in range(fieldData.GetNumberOfArrays()):
                dataDict[f]["FieldData"][fieldData.GetArrayName(i)] = []
                log(
                    "INF",
                    space * 2
                    + 'Arrays fieldData nb.{} name --> "{}"'.format(
                        i, fieldData.GetArrayName(i)
                    ),
                    ll,
                )
                fieldArray = fieldData.GetArray(i)
                log(
                    "INF",
                    space * 4
                    + "Tuples array fieldData {}".format(
                        fieldArray.GetNumberOfTuples()
                    ),
                    ll,
                )
                log(
                    "INF",
                    space * 4
                    + "Components array fieldData {}".format(
                        fieldArray.GetNumberOfComponents()
                    ),
                    ll,
                )
                for t in range(fieldArray.GetNumberOfTuples()):
                    log(
                        "INF",
                        space * 6 + f"Tuple n.{t} value --> {fieldArray.GetTuple(t)}",
                        ll,
                    )

                    dataDict[f]["FieldData"][fieldData.GetArrayName(i)].append({})
                    for c in range(fieldArray.GetNumberOfComponents()):
                        dataDict[f]["FieldData"][fieldData.GetArrayName(i)][t][
                            fieldArray.GetComponentName(c)
                        ] = fieldArray.GetComponent(t, c)
                        log(
                            "INF",
                            space * 8
                            + "Component nb.{} value --> {}".format(
                                c, fieldArray.GetComponent(t, c)
                            ),
                            ll,
                        )

            if self.__type == FileType.VTM_TYPE:
                dataDict[f]["Blocks"] = []
                for b in range(dataSet.GetNumberOfBlocks()):
                    log("INF", space * 2 + f"Add block nb.{b} ", ll)
                    uGrid = dataSet.GetBlock(b)
                    uuidForTable = str(uuid.uuid4())
                    self.__hashTable_Blocks[uuidForTable] = uGrid
                    dataDict[f]["Blocks"].append(uuidForTable)

            if self.__type == FileType.VTU_TYPE:
                log("INF", space * 2 + "Add grid ", ll)
                uGrid = dataSet
                uuidForTable = str(uuid.uuid4())
                self.__hashTable_Blocks[uuidForTable] = uGrid
                dataDict[f]["Grid"] = uuidForTable

        log("INF", json.dumps(dataDict, indent=2), ll)
        self.__dataParsed = dataDict
        return True

    # First occorrence for the key
    def findMultiblockKeyByArrayValue(
        self,
        arrayName: str,
        value: float,
        tuple: int = 0,
        componentName: Union[str, None] = None,
        ll: int = 0,
    ) -> str:
        if len(self.__dataParsed) == 0:
            log("ERR", "Data are not parsed !!!", ll)
            return ""
        for k in self.__dataParsed.keys():
            try:
                v = self.__dataParsed[k]["FieldData"][arrayName][tuple][componentName]
                if v == value:
                    log("INF", f"Value {v} found", ll)
                    return k
            except KeyError:
                log("ERR", "ERROR: fetching key !!!", ll)

        log("INF", f"WARNING: Value {value} not found !!!", ll)
        return ""

    def setCurrentMultiblockByKey(self, key: str, ll: int = 1) -> bool:
        idx = self.__currentFile
        try:
            idx = self.__files.index(key)
        except ValueError:
            log(
                "ERR",
                f"setCurrentMultiblockByKey(): Key <{key}> not found !!!",
                ll,
            )
            return False

        log("INF", f"Current multiblock changed to {key}", ll)
        self.__currentFile = idx
        return True

    def setCurrentFileByIndex(self, idx: int, ll: int = 1) -> bool:
        if idx >= 0 and idx < len(self.__files):
            for i in range(len(self.__files)):
                if f"-{str(idx)}.vtu" in self.__files[i]:
                    self.__currentFile = i
                    log("INF", f"File selected by index*{self.__files[i]}*", ll)
                    return True

            log("ERR", f"Wrong index {idx}. Index not in files ", ll)
            return False

        log("ERR", f"Wrong index {idx}. Index must be in [{0,len(self.__files)}]", ll)
        return False

    def __mesh(self, block: int = 0) -> Any:

        if self.__type == FileType.VTM_TYPE:
            blockId = self.__currentFile
            blockKey = self.__files[blockId]
            uuid = self.__dataParsed[blockKey]["Blocks"][block]
            return self.__hashTable_Blocks[uuid]

        if self.__type == FileType.VTU_TYPE:
            blockKey = self.__files[self.__currentFile]
            uuid = self.__dataParsed[blockKey]["Grid"]
            return self.__hashTable_Blocks[uuid]

        return None

    def getPoints(self, block: int = 0, ll: int = 3) -> List[Node3d]:
        uGrid = self.__mesh(block)
        nodes = []
        for i in range(uGrid.GetNumberOfPoints()):
            point = uGrid.GetPoint(i)
            nodes.append(Node3d(point[0], point[1], point[2], i))
        return nodes

    def getPoint(self, id: int, block: int = 0, ll: int = 3) -> Node3d:
        uGrid = self.__mesh(block)
        if 0 <= id and id <= uGrid.GetNumberOfPoints():
            return Node3d(
                uGrid.GetPoint(id)[0], uGrid.GetPoint(id)[1], uGrid.GetPoint(id)[2], id
            )
        else:
            log("ERR", "Point id out of range", ll)
            return Node3d()

    def getPointValueById(
        self,
        id: int,
        arrayName: str,
        block: int = 0,
        componentIdx: int = 0,
        ll: int = 1,
    ) -> Union[float, None]:
        uGrid = self.__mesh(block)
        # Point data == 0
        # Cell data == 1
        pointData = uGrid.GetAttributes(0)
        array = pointData.GetArray(arrayName)

        if array is None:
            log(
                "ERR",
                f"Array name *{arrayName}* do not exists and return None !!!",
                ll,
            )
            return None

        return array.GetComponent(id, componentIdx)

    def getNearestPoint(self, p: Point3d, block: int = 0, ll: int = 3) -> Node3d:
        pointLocator = vtk.vtkPointLocator()  # type: ignore
        uGrid = self.__mesh(block)
        pointLocator.SetDataSet(uGrid)
        pointId = pointLocator.FindClosestPoint(p.x, p.y, p.z)
        point = uGrid.GetPoint(pointId)
        return Node3d(point[0], point[1], point[2], pointId)

    def getPointsCellNearestPoint(
        self, p: Point3d, block: int = 0, ll: int = 3
    ) -> List[Node3d]:
        cellLocator = vtk.vtkCellLocator()  # type: ignore
        uGrid = self.__mesh(block)
        cellLocator.SetDataSet(uGrid)
        cellLocator.BuildLocator()
        cellId = cellLocator.FindCell([p.x, p.y, p.z])
        if cellId == -1:
            log("INF", "Cell id not found", ll)
            return []

        log("INF", f"Cell id found *{cellId}*", ll)
        cell = uGrid.GetCell(cellId)
        pl = []
        for i in range(cell.GetNumberOfPoints()):
            idPoint = cell.GetPointIds().GetId(i)
            xcoord = cell.GetPoints().GetPoint(i)[0]
            ycoord = cell.GetPoints().GetPoint(i)[1]
            zcoord = cell.GetPoints().GetPoint(i)[2]
            pl.append(Node3d(xcoord, ycoord, zcoord, idPoint))

        for p in pl:
            log("INF", f"--> {p}", ll)
        return pl

    def getPointValueInterpTriaByIds(
        self,
        p: Point3d,
        id0: int,
        id1: int,
        id2: int,
        arrayName: str,
        block: int = 0,
        componentIdx: int = 0,
        ll: int = 3,
    ) -> Union[float, None]:

        P0 = self.getPoint(id0, block, ll)
        V0 = self.getPointValueById(
            id=id0, arrayName=arrayName, block=block, componentIdx=componentIdx
        )
        if V0 is None:
            return None
        P1 = self.getPoint(id1, block, ll)
        V1 = self.getPointValueById(
            id=id1, arrayName=arrayName, block=block, componentIdx=componentIdx
        )
        if V1 is None:
            return None
        P2 = self.getPoint(id2, block, ll)
        V2 = self.getPointValueById(
            id=id2, arrayName=arrayName, block=block, componentIdx=componentIdx
        )
        if V2 is None:
            return None

        a0 = areaFromTria3D(p, P1, P2) / areaFromTria3D(P0, P1, P2)
        a1 = areaFromTria3D(p, P0, P2) / areaFromTria3D(P0, P1, P2)
        a2 = areaFromTria3D(p, P0, P1) / areaFromTria3D(P0, P1, P2)

        return a0 * V0 + a1 * V1 + a2 * V2
