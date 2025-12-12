import os
import shutil
from pathlib import Path
from typing import List, Literal, Union
from uuid import uuid4

import gmsh
import numpy as np
from jinja2 import Environment, FileSystemLoader

import pycivil.EXAUtils.vtk as vtk
from pycivil.EXAGeometry.geometry import Point2d, Point3d
from pycivil.EXAStructural.lawcodes.codeEC212 import FireCurve, LimitCurve, Moisture, RMinutes
from pycivil.EXAStructural.templateRCRect import RCTemplRectEC2
from pycivil.EXAUtils import logging as logger
from code_aster_whale.tools.code_aster import AsterLauncher, ExportType, LauncherType


class RCRectEC2FireDesign:
    def __init__(
        self,
        coldSection: Union[RCTemplRectEC2, None] = None,
        workingPath: str = "",
        logLevel: Literal[0, 1, 2, 3] = 1,
        jobToken: str = "",
        codeAsterLauncher: str = "CONTAINER",
        codeAsterTemplatePath: Path = Path(__file__).parent.parent.parent
        / "res"
        / "codeaster",
        codeAsterContainerName: str = "",
        paraviewTemplatesPath: str = "",
    ):
        self.__codeAsterLauncher = codeAsterLauncher
        self.__codeAsterContainerName = codeAsterContainerName
        self.__codeAsterTemplatePath = codeAsterTemplatePath
        self.__paraviewTemplatesPath = paraviewTemplatesPath
        self.__section = coldSection
        self.__logLevel = logLevel
        self.__workingPath = os.getcwd()
        self.__fileName_mesh = "thermal-rect"
        self.__ext_mesh = "med"
        self.__ext_mesh_aster = "mmed"
        self.__aster_job_uuid = str(uuid4())
        self.__meshNumberInX = 15
        self.__meshNumberInY = 30
        logger.log(
            "INF",
            f"Aster job   uuid --> *{self.__aster_job_uuid}*",
            self.__logLevel,
        )
        self.__aster_rep_uuid = str(uuid4())
        logger.log(
            "INF",
            f"Aster rep   uuid --> *{self.__aster_rep_uuid}*",
            self.__logLevel,
        )
        self.__aster_study_uuid = str(uuid4())
        logger.log(
            "INF",
            f"Aster study uuid --> *{self.__aster_rep_uuid}*",
            self.__logLevel,
        )
        self.__aster_study_name = "thermal-rect"
        logger.log(
            "INF",
            f"Aster study name --> *{self.__aster_study_name}*",
            self.__logLevel,
        )
        self.__fire_moisture_curve = Moisture.v00
        self.__fire_limite_curve = LimitCurve.INF
        self.__fire_curve = FireCurve.RWS
        self.__parser = vtk.Parser()
        if self.__codeAsterLauncher == "LOCAL":
            logger.log("INF", "Run Aster as *LOCAL*", self.__logLevel)
            self.__launcher = AsterLauncher(
                launcherType=LauncherType.SINGULARITY,
                exportType=ExportType.VTK_TIME_SERIES,
                containerName=self.__codeAsterContainerName,
                paraviewTemplatesPath=self.__paraviewTemplatesPath,
            )
            self.__parser.setFileType(vtk.FileType.VTM_TYPE)

        elif self.__codeAsterLauncher == "CONTAINER":
            logger.log("INF", "Run Aster as *CONTAINER*", self.__logLevel)
            self.__launcher = AsterLauncher(
                launcherType=LauncherType.CONTAINER,
                exportType=ExportType.VTK_FROM_MEDCOUPLING,
                jobToken=jobToken,
                appName="RCRectangular",
                containerName=self.__codeAsterContainerName,
                paraviewTemplatesPath=self.__paraviewTemplatesPath,
            )
            self.__parser.setFileType(vtk.FileType.VTU_TYPE)
        else:
            logger.log(
                "ERR",
                f"Aster settings unknown --> *{self.__codeAsterLauncher}*",
                self.__logLevel,
            )

        logger.log(
            "INF",
            f"Aster settings --> *{self.__codeAsterLauncher}*",
            self.__logLevel,
        )

        self.__exposedTop = False
        self.__exposedBottom = True
        self.__exposedLeft = False
        self.__exposedRight = False
        self.__time = 180
        self.__reductionLeft = 0.0
        self.__reductionRight = 0.0
        self.__reductionTop = 0.0
        self.__reductionBottom = 0.0

        if workingPath != "":
            if os.path.exists(os.path.expanduser(workingPath)):
                self.__workingPath = workingPath
            else:
                self.__workingPath = os.getcwd()
                logger.log(
                    "ERR",
                    "Working path {} do not exists !!! Make cwd {}".format(
                        workingPath, os.getcwd()
                    ),
                    self.__logLevel,
                )

        # Trash file and dir
        self.__fileNameToTrash = []
        self.__dirsNameToTrash = []

    def __fileFullPathComm(self) -> str:
        return os.path.join(self.__workingPath, self.__aster_study_name + ".comm")

    def __fileFullPathExport(self) -> str:
        return os.path.join(self.__workingPath, self.__aster_study_name + ".export")

    def __fileFullPathRmed(self) -> str:
        return os.path.join(self.__workingPath, self.__aster_study_name + ".rmed")

    def __fileFullPathMmed(self) -> str:
        return os.path.join(
            self.__workingPath, self.__fileName_mesh + "." + self.__ext_mesh_aster
        )

    def getFileNameToTrash(self):
        return self.__fileNameToTrash + self.__launcher.getArtifactsFileName()

    def getDirsNameToTrash(self):
        return self.__dirsNameToTrash + self.__launcher.getArtifactsDirName()

    def setLogLevel(self, ll: int) -> bool:
        if 0 <= ll <= 3:
            self.__logLevel = ll
            return True
        else:
            logger.log("ERR", "Log level must be between 0 and 3 !!!")
            return False

    def setMoisture(self, moisture: Moisture):
        self.__fire_moisture_curve = moisture

    def setFireCurve(self, curve: FireCurve):
        self.__fire_curve = curve

    def setEsposedTop(self, exposed=True):
        self.__exposedTop = exposed

    def setEsposedBottom(self, exposed=True):
        self.__exposedBottom = exposed

    def setEsposedLeft(self, exposed=True):
        self.__exposedLeft = exposed

    def setEsposedRight(self, exposed=True):
        self.__exposedRight = exposed

    def setSection(self, coldSection: RCTemplRectEC2):
        self.__section = coldSection

    def getSection(self) -> Union[RCTemplRectEC2, None]:
        return self.__section

    def setTime(self, t: RMinutes = RMinutes.R180):
        self.__time = int(t.name[1 : len(t.name)])

    def getTime(self):
        return self.__time

    def getCurve(self):
        return self.__fire_curve

    def setWorkingPath(self, workingPath: str, purge: bool = False) -> bool:
        if os.path.exists(os.path.expanduser(workingPath)):
            self.__workingPath = os.path.expanduser(workingPath)
            logger.log(
                "INF",
                f"Working path *{self.__workingPath}* setted.",
                self.__logLevel,
            )
            if purge:
                listFiles = os.listdir(self.__workingPath)
                for baseName in listFiles:
                    completeName = os.path.join(self.__workingPath, baseName)
                    if os.path.isfile(completeName):
                        try:
                            os.remove(completeName)
                            logger.log(
                                "WRN",
                                f"Removed file --> {completeName}",
                                self.__logLevel,
                            )
                        except (FileNotFoundError, OSError):
                            logger.log(
                                "ERR",
                                f"Removing file --> {completeName}",
                                self.__logLevel,
                            )
                    elif os.path.isdir(os.path.join(self.__workingPath, baseName)):
                        try:
                            shutil.rmtree(completeName)
                            logger.log(
                                "WRN",
                                f"Removed dir --> {completeName}",
                                self.__logLevel,
                            )
                        except OSError:
                            logger.log(
                                "ERR",
                                f"Removing dir --> {completeName}",
                                self.__logLevel,
                            )
                        pass
                    else:
                        pass

            return True
        else:
            logger.log("ERR", "Working path {} do not exists !!!", self.__logLevel)
            return False

    def getWorkingPath(self) -> str:
        return self.__workingPath

    def buildMesh(self, ll: Literal[0, 1, 2, 3] = 3) -> bool:
        fileNameForMed = os.path.join(
            self.__workingPath, self.__fileName_mesh + "." + self.__ext_mesh
        )
        fileNameForCodeAster = self.__fileFullPathMmed()

        if os.path.exists(fileNameForCodeAster):
            logger.log("WRN", "Mesh yet exists. !!! overwrite", ll)
            # return True

        if self.__section is None:
            logger.log("ERR", "Section is None. My be use setSection() !!! quit", ll)
            return False

        height = self.__section.getDimH()
        width = self.__section.getDimW()

        # GMSH need to be initialized
        #
        gmsh.initialize()

        gmsh.model.add("EXAStruTemplate")
        gmsh.model.set_current("EXAStruTemplate")

        # Points

        p_BL = gmsh.model.occ.addPoint(
            x=-width / 2 / 1000, y=-height / 2 / 1000, z=0, meshSize=0.0, tag=1
        )
        p_BR = gmsh.model.occ.addPoint(
            x=+width / 2 / 1000, y=-height / 2 / 1000, z=0, meshSize=0.0, tag=2
        )
        p_TR = gmsh.model.occ.addPoint(
            x=+width / 2 / 1000, y=+height / 2 / 1000, z=0, meshSize=0.0, tag=3
        )
        p_TL = gmsh.model.occ.addPoint(
            x=-width / 2 / 1000, y=+height / 2 / 1000, z=0, meshSize=0.0, tag=4
        )

        # Lines
        l_BOTTOM = gmsh.model.occ.addLine(p_BL, p_BR, tag=11)
        l_RIGHT = gmsh.model.occ.addLine(p_BR, p_TR, tag=12)
        l_TOP = gmsh.model.occ.addLine(p_TR, p_TL, tag=13)
        l_LEFT = gmsh.model.occ.addLine(p_TL, p_BL, tag=14)

        # Surface
        wireId = gmsh.model.occ.addCurveLoop([l_BOTTOM, l_RIGHT, l_TOP, l_LEFT], tag=1)
        s_RECT = gmsh.model.occ.addPlaneSurface(wireTags=[wireId], tag=1)

        # GMSH need syncronize geometrycal entities with model
        #
        gmsh.model.occ.synchronize()

        # Points physical group
        p_TL_pg = gmsh.model.addPhysicalGroup(0, [p_TL])
        p_TR_pg = gmsh.model.addPhysicalGroup(0, [p_TR])
        p_BL_pg = gmsh.model.addPhysicalGroup(0, [p_BL])
        p_BR_pg = gmsh.model.addPhysicalGroup(0, [p_BR])
        gmsh.model.setPhysicalName(0, p_TL_pg, "TL")
        gmsh.model.setPhysicalName(0, p_TR_pg, "TR")
        gmsh.model.setPhysicalName(0, p_BL_pg, "BL")
        gmsh.model.setPhysicalName(0, p_BR_pg, "BR")

        # Lines physical group
        l_LEFT_pg = gmsh.model.addPhysicalGroup(1, [l_LEFT])
        l_RIGHT_pg = gmsh.model.addPhysicalGroup(1, [l_RIGHT])
        l_TOP_pg = gmsh.model.addPhysicalGroup(1, [l_TOP])
        l_BOTTOM_pg = gmsh.model.addPhysicalGroup(1, [l_BOTTOM])
        gmsh.model.setPhysicalName(1, l_LEFT_pg, "LEFT")
        gmsh.model.setPhysicalName(1, l_RIGHT_pg, "RIGHT")
        gmsh.model.setPhysicalName(1, l_TOP_pg, "TOP")
        gmsh.model.setPhysicalName(1, l_BOTTOM_pg, "BOTTOM")

        # Surface physical group
        s_RECT_pg = gmsh.model.addPhysicalGroup(2, [s_RECT])
        gmsh.model.setPhysicalName(2, s_RECT_pg, "RECT")

        mesher = gmsh.model.mesh()
        mesher.setTransfiniteCurve(l_LEFT, self.__meshNumberInY + 1)
        mesher.setTransfiniteCurve(l_RIGHT, self.__meshNumberInY + 1)
        mesher.setTransfiniteCurve(l_TOP, self.__meshNumberInX + 1)
        mesher.setTransfiniteCurve(l_BOTTOM, self.__meshNumberInX + 1)
        mesher.setTransfiniteSurface(tag=1, arrangement="left", cornerTags=[1, 2, 3, 4])

        # Comment this only for generate triangular meshes
        # mesher.setRecombine(dim = 2, tag = 1)

        mesher.generate(2)

        gmsh.write(fileNameForMed)
        # GMSH need to be initialized
        #
        gmsh.finalize()

        if os.path.exists(fileNameForCodeAster):
            logger.log(
                "INF",
                f"Mesh file *{fileNameForCodeAster}* already exist ... will be removed.",
                self.__logLevel,
            )
            os.remove(fileNameForCodeAster)

        os.rename(fileNameForMed, fileNameForCodeAster)
        if os.path.exists(fileNameForCodeAster):
            logger.log(
                "INF",
                f"Mesh file *{fileNameForCodeAster}* created.",
                self.__logLevel,
            )
            self.__fileNameToTrash.append(fileNameForCodeAster)
            return True
        else:
            logger.log(
                "ERR",
                f"Can not create mesh file *{fileNameForCodeAster}*.",
                self.__logLevel,
            )
            return False

    def buildThermalMap(self, test=False) -> bool:
        os.path.dirname(os.path.abspath(__file__))

        file_loader = FileSystemLoader(searchpath=self.__codeAsterTemplatePath)
        env = Environment(loader=file_loader)

        templateName = "template-thermal-rect.export"
        jtemplate = env.get_template(templateName)
        placeHolders_export = {
            "job_uuid": self.__aster_job_uuid,
            "rep_uuid": self.__aster_rep_uuid,
            "study_uuid": self.__aster_study_uuid,
            "study_name": self.__aster_study_name,
        }
        rendered = jtemplate.render(placeHolders_export)

        fileNameExport = self.__fileFullPathExport()
        if os.path.exists(fileNameExport):
            # logger.log('WRN','Code aster export yet exist !!! do nothing',self.__logLevel)
            logger.log(
                "WRN", "Code aster export yet exist !!! Overwrite", self.__logLevel
            )

        try:
            with open(fileNameExport, "w") as f:
                f.write(rendered)  # type: ignore
        except OSError:
            logger.log("ERR", f"Writing file *{fileNameExport}*.", self.__logLevel)
            return False
        else:
            logger.log(
                "INF",
                f"File for aster EXPORT *{fileNameExport}* created.",
                self.__logLevel,
            )
            self.__fileNameToTrash.append(fileNameExport)

        templateName = "template-thermal-rect.comm"
        jtemplate = env.get_template(templateName)
        boundary_list = (
            self.__exposedBottom * "'BOTTOM',"
            + self.__exposedTop * "'TOP',"
            + self.__exposedLeft * "'LEFT',"
            + self.__exposedRight * "'RIGHT',"
        )

        fire_curve = "FIRERWS"
        if self.__fire_curve == FireCurve.RWS:
            fire_curve = "FIRERWS"
        elif self.__fire_curve == FireCurve.ISO834:
            fire_curve = "FIREISO"
        elif self.__fire_curve == FireCurve.HC:
            fire_curve = "FIREHC"
        elif self.__fire_curve == FireCurve.HCM:
            fire_curve = "FIREHCM"
        else:
            logger.log("ERR", "Fire Curve option unknown", self.__logLevel)

        capacity_curve = "Cv00"
        if self.__fire_moisture_curve == Moisture.v00:
            capacity_curve = "Cv00"
        elif self.__fire_moisture_curve == Moisture.v15:
            capacity_curve = "Cv15"
        elif self.__fire_moisture_curve == Moisture.v30:
            capacity_curve = "Cv30"
        else:
            logger.log("ERR", "Moisture Curve option unknown", self.__logLevel)

        placeHolders_command = {
            "capacity_curve": capacity_curve,
            "fire_curve": fire_curve,
            "conduttivity": "CONDMIN",
            "boundary_list": boundary_list,
        }
        rendered = jtemplate.render(placeHolders_command)

        fileNameComm = self.__fileFullPathComm()
        if os.path.exists(fileNameComm):
            logger.log(
                "WRN", "Code aster comm yet exists !!! Overwrite", self.__logLevel
            )

        try:
            with open(fileNameComm, "w") as f:
                f.write(rendered)  # type: ignore
        except OSError:
            logger.log("ERR", f"Writing file *{fileNameComm}*.", self.__logLevel)
            return False
        else:
            logger.log(
                "INF",
                f"File for aster COMM *{fileNameComm}* created.",
                self.__logLevel,
            )
            self.__fileNameToTrash.append(fileNameComm)

        fileNameRmed = self.__fileFullPathRmed()
        if os.path.exists(fileNameRmed):
            logger.log("WRN", "Code aster yet launched !!! Overwrite", self.__logLevel)

        # Run Code Aster
        #
        rc = self.__launcher.launch(
            fileNameExport, test, fileNameComm, self.__fileFullPathMmed()
        )
        if rc != 0:
            logger.log("ERR", "Code aster failed !!! quit", self.__logLevel)
            return False

        # LOCAL means that we have SINGULARITY container and export will be made
        # by PARAVIS and related plugin for medfile
        #
        if self.__codeAsterLauncher == "LOCAL":

            # Export VTK multiblock file with vtm extension
            #
            if os.path.exists(os.path.join(self.__workingPath, "vtm")):
                logger.log("WRN", "VTK files yet crated !!! Overwrite", self.__logLevel)

            dataArray = ["FamilyIdNode", "resther0TEMP", "FamilyIdCell", "NumIdCell"]
            rc = self.__launcher.exportFromMEDFile(
                fileNameRmed,
                "vtm",
                pointDataArr=dataArray,
                cellDataArr=dataArray,
                timeStep=1,
            )
            if rc != 0:
                logger.log(
                    "ERR", "Export to VTK multiblock failed !!! quit", self.__logLevel
                )
                return False

        # CONTAINER means that we have a container and export will be made
        # by this container and related plugin for medfile
        #
        elif self.__codeAsterLauncher == "CONTAINER":

            # Exporting with option timeStep = -1 means that will be exported
            # complete time series
            rc = self.__launcher.exportFromMEDFile(
                fileNameRmed, pointDataArr=["resther0TEMP"], test=test
            )

            if rc != 0:
                logger.log(
                    "ERR", "Export VTK from MED failed !!! quit", self.__logLevel
                )
                return False

        return True

    def exportThermalImgs(self) -> bool:

        if self.__codeAsterLauncher == "LOCAL":
            # Export images with pvbatch from thermal analysis
            #
            rc = self.__launcher.exportImgsFromVtm(
                self.__workingPath, "vtm", self.__workingPath
            )
            if rc != 0:
                logger.log(
                    "ERR", "Export images from VTK failed !!! quit", self.__logLevel
                )
                return False
            return True
        else:
            logger.log(
                "INF",
                "Exporting thermal images from VTK only in LOCAL mode !!! quit",
                self.__logLevel,
            )
            return True

    def parse(self) -> bool:
        if self.__codeAsterLauncher == "LOCAL":
            if not self.__parser.parse(
                files=os.path.join(self.__workingPath, "vtm"), ll=self.__logLevel
            ):
                logger.log("ERR", "Parsing VTM failed !!! quit", self.__logLevel)
                return False
            else:
                logger.log("INF", "Parsing VTM done.", self.__logLevel)
                return True

        if self.__codeAsterLauncher == "CONTAINER":
            if not self.__parser.parse(
                files=os.path.join(self.__workingPath, "vtu"), ll=self.__logLevel
            ):
                logger.log("ERR", "Parsing VTU failed !!! quit", self.__logLevel)
                return False
            else:
                logger.log("INF", "Parsing VTU done.", self.__logLevel)
                return True

        logger.log("ERR", "Setting launcher wrong !!! quit", self.__logLevel)
        return False

    def getParser(self):
        return self.__parser

    def deleteArtifacts(self):
        # print(self.__fileNameToTrash)
        for f in self.__fileNameToTrash:
            try:
                os.remove(f)
                logger.log("WRN", f"Removed file --> {f}", self.__logLevel)
            except OSError:
                logger.log("ERR", f"Removing file --> {f}", self.__logLevel)
        # print(self.__dirsNameToTrash)
        for d in self.__dirsNameToTrash:
            try:
                shutil.rmtree(d)
                logger.log("WRN", f"Removed dir --> {d}", self.__logLevel)
            except OSError:
                logger.log("ERR", f"Removing dir --> {d}", self.__logLevel)
        self.__fileNameToTrash = []
        self.__dirsNameToTrash = []
        # self.__launcher.deleteArtifacts()

    def buildHotSection(self) -> bool:
        if self.__section is not None:
            # Mesh in [m] but section in [mm]. Need a conversion
            H = self.__section.getDimH() / 1000
            W = self.__section.getDimW() / 1000
        else:
            logger.log("ERR", "Need to use setSection() !!! Quit.", self.__logLevel)
            return False

        if self.__codeAsterLauncher == "LOCAL":

            # Setting actual time value
            #
            logger.log(
                "INF",
                f"Find block with time value {self.__time * 60} ...",
                self.__logLevel,
            )
            k = self.__parser.findMultiblockKeyByArrayValue(
                arrayName="TimeValue", value=self.__time * 60, ll=self.__logLevel
            )
            logger.log("INF", f"... key found {k}.", self.__logLevel)
            self.__parser.setCurrentMultiblockByKey(key=k, ll=self.__logLevel)

        elif self.__codeAsterLauncher == "CONTAINER":

            # Setting index by time step
            #
            timeIndex = int(self.__time / 10)
            logger.log(
                "INF", f"Find block with time index {timeIndex} ...", self.__logLevel
            )
            self.__parser.setCurrentFileByIndex(timeIndex)

        else:
            logger.log(
                "ERR",
                f"Code aster environnment {self.__codeAsterLauncher} wrong",
                self.__logLevel,
            )
            return False

        # Build temperature value in dir. Y
        #
        dirY_y = np.linspace(0, H, self.__meshNumberInY)
        dirY_x = np.zeros(len(dirY_y))
        dirY_v = np.zeros(len(dirY_y))
        for i in range(len(dirY_x)):
            testPoint = Point3d(dirY_x[i], dirY_y[i] - H / 2, 0)
            pointsFound = self.__parser.getPointsCellNearestPoint(
                p=testPoint, ll=self.__logLevel
            )
            dirY_v[i] = self.__parser.getPointValueInterpTriaByIds(
                p=testPoint,
                id0=pointsFound[0].idn,
                id1=pointsFound[1].idn,
                id2=pointsFound[2].idn,
                arrayName="resther0TEMP",
                ll=self.__logLevel,
            )
            logger.log(
                "INF",
                f"---> Dir.Y Temp in point is {dirY_v[i]:.1f}",
                self.__logLevel,
            )

        # Build temperature value in dir. X
        #
        dirX_x = np.linspace(0, W, self.__meshNumberInX)
        dirX_y = np.zeros(len(dirX_x))
        dirX_v = np.zeros(len(dirX_x))
        for i in range(len(dirX_x)):
            testPoint = Point3d(dirX_x[i] - W / 2, dirX_y[i], 0)
            pointsFound = self.__parser.getPointsCellNearestPoint(
                p=testPoint, ll=self.__logLevel
            )
            dirX_v[i] = self.__parser.getPointValueInterpTriaByIds(
                p=testPoint,
                id0=pointsFound[0].idn,
                id1=pointsFound[1].idn,
                id2=pointsFound[2].idn,
                arrayName="resther0TEMP",
                ll=self.__logLevel,
            )
            logger.log(
                "INF",
                f"---> Dir.X Temp in point is {dirX_v[i]:.1f}",
                self.__logLevel,
            )

        zerosDirY, zerosDirY_sgn = self.__findZeros(dirY_y, dirY_v - 500)
        zerosDirX, zerosDirX_sgn = self.__findZeros(dirX_x, dirX_v - 500)

        assert len(zerosDirY) == len(zerosDirY_sgn)

        deltaBot = 0.0
        deltaTop = 0.0
        if len(zerosDirY) in [0, 1, 2]:
            for i in range(len(zerosDirY)):
                if zerosDirY_sgn[i] == -1:
                    deltaBot = zerosDirY[i] * 1000
                elif zerosDirY_sgn[i] == +1:
                    deltaTop = (H - zerosDirY[i]) * 1000
                else:
                    pass
        else:
            logger.log("ERR", "zerosDirY not in [0,1,2] !!! Quit.", self.__logLevel)
            return False

        logger.log(
            "INF",
            f"deltaBot = {deltaBot:.1f} -- deltaTop = {deltaTop:.1f}",
            self.__logLevel,
        )

        deltaLeft = 0.0
        deltaRight = 0.0
        if len(zerosDirX) in [0, 1, 2]:
            for i in range(len(zerosDirX)):
                if zerosDirX_sgn[i] == -1:
                    deltaLeft = zerosDirX[i] * 1000
                elif zerosDirX_sgn[i] == +1:
                    deltaRight = (W - zerosDirX[i]) * 1000
                else:
                    pass
        else:
            logger.log("ERR", "zerosDirX not in [0,1,2] !!! Quit.", self.__logLevel)
            return False

        self.__reductionLeft = deltaLeft
        self.__reductionRight = deltaRight
        self.__reductionTop = deltaTop
        self.__reductionBottom = deltaBot

        logger.log(
            "INF",
            f"deltaLeft = {deltaLeft:.1f} -- deltaRight = {deltaRight:.1f}",
            self.__logLevel,
        )
        logger.log(
            "INF",
            f"deltaTop  = {deltaTop:.1f} --   deltaBot = {deltaBot:.1f}",
            self.__logLevel,
        )

        #
        # Translate concrete part of section after reduction shape
        #
        self.__section.setDimH(self.__section.getDimH() - deltaTop - deltaBot)
        self.__section.setDimW(self.__section.getDimW() - deltaLeft - deltaRight)

        pTL = self.__section.getStructConcretelItem().getShape().getShapePoint("TL")
        pBR = self.__section.getStructConcretelItem().getShape().getShapePoint("BR")

        deltaG_x = ((pBR.x - deltaRight) + (pTL.x + deltaLeft)) / 2
        deltaG_y = ((pTL.y - deltaTop) + (pBR.y + deltaBot)) / 2
        logger.log(
            "INF",
            f"deltaG_x = {deltaG_x:.1f}mm -- deltaG_y = {deltaG_y:.1f}mm",
            self.__logLevel,
        )

        #
        # Assign steel temperature
        #
        if len(self.__section.getSteelRebar()) > 0:
            steelRebarTemperatures = len(self.__section.getSteelRebar()) * [0.0]
            for idx, bar in enumerate(self.__section.getSteelRebar()):
                centerOfBar = bar.getShape().getOrigin()
                #
                # Retrive value in point by interp on cellPoints
                #
                logger.log(
                    "INF",
                    f"Retrive temp by interp on cell points at {centerOfBar}",
                    self.__logLevel,
                )
                testPoint = Point3d(centerOfBar.x / 1000, centerOfBar.y / 1000, 0)

                pointsFound = self.__parser.getPointsCellNearestPoint(
                    p=testPoint, ll=self.__logLevel
                )

                value = self.__parser.getPointValueInterpTriaByIds(
                    p=testPoint,
                    id0=pointsFound[0].idn,
                    id1=pointsFound[1].idn,
                    id2=pointsFound[2].idn,
                    arrayName="resther0TEMP",
                    ll=self.__logLevel,
                )

                if value is not None:
                    logger.log(
                        "INF",
                        f"---> Temp in point is {value:.1f}",
                        self.__logLevel,
                    )
                    steelRebarTemperatures[idx] = value
                else:
                    logger.log(
                        "ERR", "---> Temp in point is None. Quit", self.__logLevel
                    )
                    return False

            self.__section.setSteelTemperatures(steelRebarTemperatures)

            #
            # Translate steel part of section after reduction shape
            # cause center of gravity changed with section reducted
            #
            self.__section.translateSteelItems(Point2d(), Point2d(deltaG_x, deltaG_y))

        else:
            logger.log("INF", "No rebar. Quit.", self.__logLevel)
            return False
        return True

    def __findZeros(self, x: np.ndarray, y: np.ndarray) -> List[List[float]]:
        zeros_val = []
        # Decreasing or increasing funtion
        #
        # decreasing = -1
        # creasing = +1
        # constant = 0
        local_sig = []
        if len(x) != len(y):
            logger.log(
                "ERR",
                "len(x) = {} must be the same of len(y) = {} !!! quit".format(
                    len(x), len(x)
                ),
                self.__logLevel,
            )
            return zeros_val

        for i in range(len(x) - 1):
            if y[i] * y[i + 1] == 0.0:
                if y[i] == 0.0:
                    zeros_val.append(x[i])
                    if y[i + 1] > y[i]:
                        local_sig.append(+1)
                    elif y[i + 1] < y[i]:
                        local_sig.append(-1)
                    else:
                        local_sig.append(0)
            else:
                if y[i] * y[i + 1] < 0.0:
                    zeros_val.append(
                        x[i] + abs(y[i] * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))
                    )
                    if y[i + 1] > y[i]:
                        local_sig.append(+1)
                    elif y[i + 1] < y[i]:
                        local_sig.append(-1)
                    else:
                        local_sig.append(0)

        return [zeros_val, local_sig]

    def getDeltas(self) -> List[float]:
        return [
            self.__reductionLeft,
            self.__reductionRight,
            self.__reductionTop,
            self.__reductionBottom,
        ]
