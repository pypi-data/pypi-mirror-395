"""Module that generates Cheat Sheets.

A cheat sheet is a synthetic view of something, of objects with a lots of
properties. In this case, for example PlateMinimumAreaCS show input data,
calculations and output in synthetic manner.

Classes list:

    1. BeamMinimumAreaCS
    2. ConcreteMaterialCS
    3. PlateMinimumAreaCS
    4. RebarMaterialCS
"""

from pathlib import Path

from pycivil.EXAStructural.cheatsheets.codeEC2Rules import PlateMinimumArea
from pycivil.EXAStructural.cheatsheets.codeNTC2018Rules import (
    BeamMinimumArea,
    ConcreteMaterial,
    RebarMaterial,
)
from pycivil.EXAUtils.report import Fragment, FragmentsBuilder


class ConcreteMaterialCS(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, data: ConcreteMaterial) -> None:
        super().__init__()
        self.__latexTemplatePath = latexTemplatePath
        self.__data = data

    def setDataModel(self, data: ConcreteMaterial) -> None:
        self.__data = data

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        placeHolders = {
            "elementDescr": f"{self.__data.inputData.elementDescr:s}",
            "keyCode": f"{self.__data.inputData.keyCode:s}",
            "concreteClass": f"{self.__data.inputData.concreteClass:s}",
            "value_Rck": f"{self.__data.outputData.value_Rck:.1f}",
            "value_fck": f"{self.__data.outputData.value_fck:.1f}",
            "value_fcm": f"{self.__data.outputData.value_fcm:.2f}",
            "value_fctm": f"{self.__data.outputData.value_fctm:.2f}",
            "value_Ecm": f"{self.__data.outputData.value_Ecm:.2f}",
            "value_alphacc": f"{self.__data.outputData.value_alphacc:.2f}",
            "value_gammac": f"{self.__data.outputData.value_gammac:.2f}",
            "value_fcd": f"{self.__data.outputData.value_fcd:.2f}",
            "value_sigmaCar": f"{self.__data.outputData.value_sigmaCar:.2f}",
            "value_sigmaQp": f"{self.__data.outputData.value_sigmaQp:.2f}",
        }
        f.add(
            templateName="sheet-MatConcrete-NTC2018-ita.tex",
            templatePlaceholders=placeHolders,
        )
        self._setFragment(f)
        return f


class RebarMaterialCS(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, data: RebarMaterial) -> None:
        super().__init__()
        self.__latexTemplatePath = latexTemplatePath
        self.__data = data

    def setDataModel(self, data: RebarMaterial) -> None:
        self.__data = data

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        placeHolders = {
            "elementDescr": f"{self.__data.inputData.elementDescr:s}",
            "keyCode": f"{self.__data.inputData.keyCode:s}",
            "steelClass": f"{self.__data.inputData.steelClass:s}",
            "value_fyk": f"{self.__data.outputData.value_fyk:.1f}",
            "value_ftk": f"{self.__data.outputData.value_ftk:.1f}",
            "value_gammas": f"{self.__data.outputData.value_gammas:.2f}",
            "value_Es": f"{self.__data.outputData.value_Es:.2f}",
            "value_fyd": f"{self.__data.outputData.value_fyd:.2f}",
            "value_sigmaCar": f"{self.__data.outputData.value_sigmaCar:.2f}",
        }
        f.add(
            templateName="sheet-MatRebar-NTC2018-ita.tex",
            templatePlaceholders=placeHolders,
        )
        self._setFragment(f)
        return f


class PlateMinimumAreaCS(FragmentsBuilder):
    """The class builds a fragment report starting from PlateMinimumArea class

    The class needs a Reporter class in Report module to build real pdf file.

    Examples:

    ```
    fragBuilder = latexCheatSheets.PlateMinimumAreaCS(
        latexTemplatePath=latexTemplatePath,
        data=data
    )

    frag_title = Fragment()
    frag_title.add(line=r"\section{Area minima delle piastre secondo EC2}")
    frag = fragBuilder.buildFragment()

    reporter = Reporter(latexTemplatePath)
    reporter.buildPDF(ReportDriverEnum.PDFLATEX, ReportTemplateEnum.TEX_ENG_CAL, [frag_title,frag])
    reporter.makePDF(path=str(tmp_path), fileName="TEX_ENG_CAL")
    ```
    """
    def __init__(self, latexTemplatePath: Path, data: PlateMinimumArea) -> None:
        super().__init__()
        self.__latexTemplatePath = latexTemplatePath
        self.__data = data

    def setDataModel(self, data: PlateMinimumArea) -> None:
        self.__data = data

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        placeHolders = {
            "elementDescr": f"{self.__data.inputData.elementDescr:s}",
            "keyCode": f"{self.__data.inputData.keyCode:s}",
            "concreteClass": f"{self.__data.inputData.concreteClass:s}",
            "cls_fck": f"{self.__data.logsData.cls_fck:.2f}",
            "cls_fctm": f"{self.__data.logsData.cls_fctm:.2f}",
            "steelClass": f"{self.__data.inputData.steelClass:s}",
            "steel_fyk": f"{self.__data.logsData.steel_fyk:.2f}",
            "hEl": f"{self.__data.inputData.hEl:.2f}",
            "rebarD": f"{self.__data.inputData.rebarD:.2f}",
            "rebarDSec": f"{self.__data.inputData.rebarDSec:.2f}",
            "cover": f"{self.__data.inputData.cover:.2f}",
            "coverSec": f"{self.__data.inputData.coverSec:.2f}",
            "stirrupD": f"{self.__data.inputData.stirrupD:.2f}",
            "nbLegDirX": f"{self.__data.inputData.nbLegDirX:.2f}",
            "heightUtil": f"{self.__data.logsData.heightUtil:.2f}",
            "areaUtil": f"{self.__data.logsData.areaUtil:.2f}",
            "minimumRebarAreaCrit1": f"{self.__data.logsData.minimumRebarAreaCrit1:.2f}",
            "minimumRebarAreaCrit2": f"{self.__data.logsData.minimumRebarAreaCrit2:.2f}",
            "minimumRebarArea": f"{self.__data.logsData.minimumRebarArea:.2f}",
            "distMaxRebar": f"{self.__data.logsData.distMaxRebar:.2f}",
            "distMaxRebarMaxLoad": f"{self.__data.logsData.distMaxRebarMaxLoad:.2f}",
            "disposedRebarArea": f"{self.__data.logsData.disposedRebarArea:.2f}",
            "disposedRebarNumber": f"{self.__data.logsData.disposedRebarNumber:.2f}",
            "disposedRebarAreaMaxLoad": f"{self.__data.logsData.disposedRebarAreaMaxLoad:.2f}",
            "disposedRebarNumberMaxLoad": f"{self.__data.logsData.disposedRebarNumberMaxLoad:.2f}",
            "heightUtilSec": f"{self.__data.logsData.heightUtilSec:.2f}",
            "areaUtilSec": f"{self.__data.logsData.areaUtilSec:.2f}",
            "minimumRebarAreaCrit1Sec": f"{self.__data.logsData.minimumRebarAreaCrit1Sec:.2f}",
            "minimumRebarAreaCrit2Sec": f"{self.__data.logsData.minimumRebarAreaCrit2Sec:.2f}",
            "minimumRebarAreaSec": f"{self.__data.logsData.minimumRebarAreaSec:.2f}",
            "distMaxRebarSec": f"{self.__data.logsData.distMaxRebarSec:.2f}",
            "distMaxRebarMaxLoadSec": f"{self.__data.logsData.distMaxRebarMaxLoadSec:.2f}",
            "disposedRebarAreaSec": f"{self.__data.logsData.disposedRebarAreaSec:.2f}",
            "disposedRebarNumberSec": f"{self.__data.logsData.disposedRebarNumberSec:.2f}",
            "disposedRebarAreaMaxLoadSec": f"{self.__data.logsData.disposedRebarAreaMaxLoadSec:.2f}",
            "disposedRebarNumberMaxLoadSec": f"{self.__data.logsData.disposedRebarNumberMaxLoadSec:.2f}",
            "minimumRebarAreaForElementLenght": f"{self.__data.logsData.minimumRebarAreaForElementLenght:.2f}",
            "maxStepTrasv": f"{self.__data.logsData.maxStepTrasv:.2f}",
            "legsNumber": f"{self.__data.logsData.legsNumber:.2f}",
            "legsNumberTrasv": f"{self.__data.logsData.legsNumberTrasv:.2f}",
            "maxStepLongCrit1": f"{self.__data.logsData.maxStepLongCrit1:.2f}",
            "maxStepLongCrit2": f"{self.__data.logsData.maxStepLongCrit2:.2f}",
            "maxStep": f"{self.__data.logsData.maxStep:.2f}",
            "rebarAreaForElementLenght": f"{self.__data.logsData.rebarAreaForElementLenght:.2f}",
        }
        f.add(
            templateName="sheet-PlateMinimumArea-EC211-ita.tex",
            templatePlaceholders=placeHolders,
        )
        self._setFragment(f)
        return f


class BeamMinimumAreaCS(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, data: BeamMinimumArea) -> None:
        super().__init__()
        self.__latexTemplatePath = latexTemplatePath
        self.__data = data

    def setDataModel(self, data: BeamMinimumArea) -> None:
        self.__data = data

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        placeHolders = {
            "elementDescr": f"{self.__data.inputData.elementDescr:s}",
            "keyCode": f"{self.__data.inputData.keyCode:s}",
            "concreteClass": f"{self.__data.inputData.concreteClass:s}",
            "cls_fck": f"{self.__data.logsData.cls_fck:.2f}",
            "cls_fctm": f"{self.__data.logsData.cls_fctm:.2f}",
            "steelClass": f"{self.__data.inputData.steelClass:s}",
            "steel_fyk": f"{self.__data.logsData.steel_fyk:.2f}",
            "hEl": f"{self.__data.inputData.hEl:.2f}",
            "wEl": f"{self.__data.inputData.wEl:.2f}",
            "bt": f"{self.__data.inputData.bt:.2f}",
            "rebarD": f"{self.__data.inputData.rebarD:.2f}",
            "cover": f"{self.__data.inputData.cover:.2f}",
            "bMin": f"{self.__data.inputData.bMin:.2f}",
            "rebarDComp": f"{self.__data.inputData.rebarDComp:.2f}",
            "stirrupD": f"{self.__data.inputData.stirrupD:.2f}",
            "nbLegDirX": f"{self.__data.inputData.nbLegDirX:.2f}",
            "heightUtil": f"{self.__data.logsData.heightUtil:.2f}",
            "areaUtil": f"{self.__data.logsData.areaUtil:.2f}",
            "minimumRebarAreaCrit1": f"{self.__data.logsData.minimumRebarAreaCrit1:.2f}",
            "minimumRebarAreaCrit2": f"{self.__data.logsData.minimumRebarAreaCrit2:.2f}",
            "minimumRebarArea": f"{self.__data.logsData.minimumRebarArea:.2f}",
            "rebarAreaDisposed": f"{self.__data.logsData.rebarAreaDisposed:.2f}",
            "rebarNumber": f"{self.__data.outputData.rebarNumber:.2f}",
            "minimumRebarAreaForElementLenght": f"{self.__data.logsData.minimumRebarAreaForElementLenght:.2f}",
            "minimumLegsForElementLenght": f"{self.__data.logsData.minimumLegsForElementLenght:.2f}",
            "maxStepCrit1": f"{self.__data.logsData.maxStepCrit1:.2f}",
            "maxStepCrit2": f"{self.__data.logsData.maxStepCrit2:.2f}",
            "maxStepCrit3": f"{self.__data.logsData.maxStepCrit3:.2f}",
            "maxStepCrit4": f"{self.__data.logsData.maxStepCrit4:.2f}",
            "stirrupStepMin": f"{self.__data.outputData.stirrupStepMin:.2f}",
            "stirrupCompStepMin": f"{self.__data.outputData.stirrupCompStepMin:.2f}",
        }
        f.add(
            templateName="sheet-BeamMinimumArea-NTC2018-ita.tex",
            templatePlaceholders=placeHolders,
        )
        self._setFragment(f)
        return f
