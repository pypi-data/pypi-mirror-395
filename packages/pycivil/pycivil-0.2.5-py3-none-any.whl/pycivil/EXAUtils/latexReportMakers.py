from pathlib import Path
from typing import List, Union, cast

from pycivil.EXAUtils.EXAExceptions import EXAExceptions
from pycivil.EXAGeometry.shapes import ShapeArea, ShapeRect, ShapesEnum
from pycivil.EXAStructural.codes import KNOWN_CODES, Code, Codes
from pycivil.EXAStructural.loads import ForcesOnSection
from pycivil.EXAStructural.materials import Concrete, ConcreteSteel
from pycivil.EXAStructural.templateRCRect import RCTemplRectEC2
from pycivil.EXAUtils.report import EnumFBSection, Fragment, FragmentsBuilder


def texSpecChars(val: Union[str, None]) -> Union[str, None]:
    replaced = ""
    if val is not None:
        replaced = val.replace("_", "\\_")
    return replaced


class ForcesOnSectionListFB(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, forces: List[ForcesOnSection] | None = None):
        super().__init__()
        if forces is None:
            forces = []
        self.__forces = forces
        self.__opt_section_enabled = True
        self.__opt_section_title = "Forces on section lists with NTC2018"
        self.__opt_section_level = EnumFBSection.SEC_SUBSECTION
        self.__latexTemplatePath = latexTemplatePath

    def forces(self) -> List[ForcesOnSection]:
        return self.__forces

    def setFragmentOptions(self, options: dict) -> bool:
        if "section_enabled" in options:
            self.__opt_section_enabled = options["section_enabled"]

        if "section_title" in options:
            self.__opt_section_title = options["section_title"]

        if "section_level" in options:
            self.__opt_section_level = options["section_level"]

        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        if self.__opt_section_enabled:
            if self.__opt_section_level == EnumFBSection.SEC_CHAPTER:
                f.add(r"\chapter{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SECTION:
                f.add(r"\section{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSECTION:
                f.add(r"\subsection{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSUBSECTION:
                f.add(r"\subsubsection{" + self.__opt_section_title + "}")
            else:
                raise EXAExceptions(
                    "0001", "level number unknown", self.__opt_section_level
                )

        forces = []
        placeHolders = {"forces": forces}
        for fs in self.__forces:

            fd = {"id": f"{fs.id:.0f}"}

            comp = fs.Fx
            if isinstance(comp, (float, int)):
                fd["Fx"] = f"{comp / 1000:.1f}"
            else:
                fd["Fx"] = ""

            comp = fs.Fy
            if isinstance(comp, (float, int)):
                fd["Fy"] = f"{comp / 1000:.1f}"
            else:
                fd["Fy"] = ""

            comp = fs.Fz
            if isinstance(comp, (float, int)):
                fd["Fz"] = f"{comp / 1000:.1f}"
            else:
                fd["Fz"] = ""

            comp = fs.Mx
            if isinstance(comp, (float, int)):
                fd["Mx"] = f"{comp / 1000000:.1f}"
            else:
                fd["Mx"] = ""

            comp = fs.My
            if isinstance(comp, (float, int)):
                fd["My"] = f"{comp / 1000000:.1f}"
            else:
                fd["My"] = ""

            comp = fs.Mz
            if isinstance(comp, (float, int)):
                fd["Mz"] = f"{comp / 1000000:.1f}"
            else:
                fd["Mz"] = ""

            if fs.descr is not None:
                print(texSpecChars(fs.descr))
                fd["descr"] = f"{texSpecChars(fs.descr):s}"
            else:
                fd["descr"] = ""
            # fd["descr"] = f"{fs.descr:s}"
            fd["limitState"] = f"{fs.getLimitStateTr():s}"
            fd["frequency"] = f"{fs.getFrequencyTr():s}"
            forces.append(fd)

        f.add(
            templateName="template-ita-loads-NTC2018.tex",
            templatePlaceholders=placeHolders,
        )

        self._setFragment(f)
        return f


class CodesFB(Codes, FragmentsBuilder):
    def __init__(
        self, latexTemplatePath: Path, codes: Union[List[Code], None] = None
    ) -> None:

        if codes is None:
            codes = []

        Codes.__init__(self, codes)
        self.__opt_nameList = "Normative utilizzate"
        self.__opt_environment = True
        self.__opt_section = True
        self.__opt_subsection = False
        self.__latexTemplatePath = latexTemplatePath

    def setOptionNameList(self, name: str = "Normative utilizzate") -> None:
        self.__opt_nameList = name

    def setOptionSection(self) -> None:
        self.__opt_section = True
        self.__opt_subsection = False

    def setOptionSubSection(self) -> None:
        self.__opt_section = False
        self.__opt_subsection = True

    def setOptionEnvironnment(self, enabled: bool = True) -> None:
        self.__opt_environment = enabled

    def setFragmentOptions(self, options: dict) -> bool:
        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)

        if self.__opt_environment:
            if self.__opt_section:
                f.add(
                    r"\renewcommand{\bibsection}{\section{" + self.__opt_nameList + "}}"
                )
            elif self.__opt_subsection:
                f.add(
                    r"\renewcommand{\bibsection}{\subsection{"
                    + self.__opt_nameList
                    + "}}"
                )

            f.add(r"\begin{thebibliography}{99}")

        for c in self.getCodes():
            try:
                dfc = KNOWN_CODES[c.codeStr()]
            except KeyError:
                print("skipped")
                continue
            f.add(r"\bibitem{" + dfc.code + "}")
            f.add(
                r"\emph{"
                + dfc.description
                + "}"
                + r", \mbox{"
                + dfc.author
                + "}, "
                + str(dfc.year)
            )

        if self.__opt_environment:
            f.add(r"\end{thebibliography}")

        self._setFragment(f)
        return f


class ConcreteFB(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, concrete: Concrete):
        super().__init__()
        self.__concrete = concrete
        self.__opt_section_enabled = True
        self.__opt_section_title = "Concrete material"
        self.__opt_section_level = EnumFBSection.SEC_SUBSECTION
        self.__opt_glossary = False
        self.__latexTemplatePath = latexTemplatePath

    def setFragmentOptions(self, options: dict) -> bool:
        if "section_enabled" in options:
            self.__opt_section_enabled = options["section_enabled"]

        if "section_title" in options:
            self.__opt_section_title = options["section_title"]

        if "section_level" in options:
            self.__opt_section_level = options["section_level"]

        if "glossary" in options:
            self.__opt_glossary = options["glossary"]

        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        if self.__opt_section_enabled:
            if self.__opt_section_level == EnumFBSection.SEC_CHAPTER:
                f.add(r"\chapter{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SECTION:
                f.add(r"\section{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSECTION:
                f.add(r"\subsection{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSUBSECTION:
                f.add(r"\subsubsection{" + self.__opt_section_title + "}")
            else:
                raise EXAExceptions(
                    "0001", "level number unknown", self.__opt_section_level
                )

        placeHolders = {
            "classe": f"{self.__concrete.catStr():s}",
            "norma": f"{self.__concrete.codeStr():s}",
            "environnment": "{:s}".format(self.__concrete.getEnvironmentTr("IT")),
            "fck": "{:.1f} {:s}".format(self.__concrete.get_fck(), r"\text{ MPa}"),
            "fcm": "{:.1f} {:s}".format(self.__concrete.get_fcm(), r"\text{ MPa}"),
            "fctm": "{:.1f} {:s}".format(self.__concrete.get_fctm(), r"\text{ MPa}"),
            "Ecm": "{:.1f} {:s}".format(self.__concrete.get_Ecm(), r"\text{ MPa}"),
            "gammac": f"{self.__concrete.get_gammac():.2f}",
            "sigmac_max_c": "{:.1f} {:s}".format(
                self.__concrete.get_sigmac_max_c(), r"\text{ MPa}"
            ),
            "sigmac_max_q": "{:.1f} {:s}".format(
                self.__concrete.get_sigmac_max_q(), r"\text{ MPa}"
            ),
            "ecu": f"{self.__concrete.get_ecu():.4f}",
            "ec2": f"{self.__concrete.get_ec2():.4f}",
            "lambda": f"{self.__concrete.get_lambda():.2f}",
            "eta": f"{self.__concrete.get_eta():.2f}",
            "alphacc": f"{self.__concrete.get_alphacc():.2f}",
            "alphacc_fire": f"{self.__concrete.get_alphacc_fire():.2f}",
            "byCode": self.__concrete.isSetByCode(),
            "glossary": self.__opt_glossary,
        }

        f.add(
            templateName="template-ita-material-concrete.tex",
            templatePlaceholders=placeHolders,
        )

        self._setFragment(f)
        return f


class SteelConcreteFB(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, steel: ConcreteSteel):
        super().__init__()
        self.__steel = steel
        self.__opt_section_enabled = True
        self.__opt_section_title = "Steel for rebar material"
        self.__opt_section_level = EnumFBSection.SEC_SUBSECTION
        self.__latexTemplatePath = latexTemplatePath

    def setFragmentOptions(self, options: dict) -> bool:
        if "section_enabled" in options:
            self.__opt_section_enabled = options["section_enabled"]

        if "section_title" in options:
            self.__opt_section_title = options["section_title"]

        if "section_level" in options:
            self.__opt_section_level = options["section_level"]

        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        if self.__opt_section_enabled:
            if self.__opt_section_level == EnumFBSection.SEC_CHAPTER:
                f.add(r"\chapter{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SECTION:
                f.add(r"\section{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSECTION:
                f.add(r"\subsection{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSUBSECTION:
                f.add(r"\subsubsection{" + self.__opt_section_title + "}")
            else:
                raise EXAExceptions(
                    "0001", "level number unknown", self.__opt_section_level
                )

        placeHolders = {
            "classe": f"{self.__steel.catStr():s}",
            "norma": f"{self.__steel.codeStr():s}",
            "sensitivity": "{:s}".format(self.__steel.getEnvironmentTr("IT")),
            "fsy": "{:.0f} {:s}".format(self.__steel.get_fsy(), r"\text{ MPa}"),
            "Es": "{:.0f} {:s}".format(self.__steel.get_Es(), r"\text{ MPa}"),
            "gammas": f"{self.__steel.get_gammas():.2f}",
            "sigmas_max_c": "{:.1f} {:s}".format(
                self.__steel.get_sigmas_max_c(), r"\text{ MPa}"
            ),
            "esu": f"{self.__steel.get_esu():.4f}",
            "esy": f"{self.__steel.get_esy():.4f}",
            "byCode": self.__steel.isSetByCode(),
        }

        f.add(
            templateName="template-ita-material-rebar.tex",
            templatePlaceholders=placeHolders,
        )

        self._setFragment(f)
        return f


class ConcreteSectionFB(FragmentsBuilder):
    def __init__(self, latexTemplatePath: Path, rcs: RCTemplRectEC2):
        super().__init__()
        self.__rcs = rcs
        self.__opt_section_enabled = True
        self.__opt_section_title = "Reinforced concrete section"
        self.__opt_section_level = EnumFBSection.SEC_SUBSECTION
        self.__opt_glossary = False
        self.__latexTemplatePath = latexTemplatePath

    def getOptSectionEnabled(self) -> bool:
        return self.__opt_section_enabled

    def getOptSectionTitle(self) -> str:
        return self.__opt_section_title

    def getOptSectionLevel(self):
        return self.__opt_section_level

    def getOptGlossary(self) -> bool:
        return self.__opt_glossary

    def setFragmentOptions(self, options: dict) -> bool:
        if "section_enabled" in options:
            self.__opt_section_enabled = options["section_enabled"]

        if "section_title" in options:
            self.__opt_section_title = options["section_title"]

        if "section_level" in options:
            self.__opt_section_level = options["section_level"]

        if "glossary" in options:
            self.__opt_glossary = options["glossary"]

        return True

    def buildFragment(self) -> Fragment:
        f = Fragment(self.__latexTemplatePath)
        if self.__opt_section_enabled:
            if self.__opt_section_level == EnumFBSection.SEC_CHAPTER:
                f.add(r"\chapter{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SECTION:
                f.add(r"\section{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSECTION:
                f.add(r"\subsection{" + self.__opt_section_title + "}")
            elif self.__opt_section_level == EnumFBSection.SEC_SUBSUBSECTION:
                f.add(r"\subsubsection{" + self.__opt_section_title + "}")
            else:
                raise EXAExceptions(
                    "0001", "level number unknown", self.__opt_section_level
                )

        placeHolders = {}
        #
        # RECTANGULAR SHAPE
        #
        if (
            self.__rcs.getStructConcretelItem().getShape().getType()
            == ShapesEnum.SHAPE_RECT
        ):
            placeHolders["shape"] = "RECT"
            #
            rectShape = cast(ShapeRect, self.__rcs.getStructConcretelItem().getShape())
            placeHolders["width"] = rectShape.w()
            placeHolders["height"] = rectShape.h()
            dimRef = max(rectShape.w(), rectShape.h())

            # Below value is centimeters
            figureRayDimension = 8
            dimLineDistance = 0.6

            scaleFigure = figureRayDimension / dimRef
            placeHolders["scale"] = scaleFigure
            placeHolders["dimDist"] = dimLineDistance / scaleFigure

            #
            placeHolders["xTL"] = rectShape.getShapePoint("TL").x
            placeHolders["xTR"] = rectShape.getShapePoint("TR").x
            placeHolders["xBL"] = rectShape.getShapePoint("BL").x
            placeHolders["xBR"] = rectShape.getShapePoint("BR").x
            placeHolders["yTL"] = rectShape.getShapePoint("TL").y
            placeHolders["yTR"] = rectShape.getShapePoint("TR").y
            placeHolders["yBL"] = rectShape.getShapePoint("BL").y
            placeHolders["yBR"] = rectShape.getShapePoint("BR").y
            #
        else:
            raise EXAExceptions("0001", "Section Unknown")

        # steelShape = typing.cast(eg.ShapeRect,self.getStructSteelItems().getShape())
        steels = []

        for idx, i in enumerate(self.__rcs.getStructSteelItems()):
            steel = {}
            areaShape = cast(ShapeArea, i.getShape())
            steel["id"] = i.getId()
            steel["xPos"] = "{:.1f}".format(areaShape.getShapePoint("O").x)
            steel["yPos"] = "{:.1f}".format(areaShape.getShapePoint("O").y)
            steel["diam"] = f"{self.__rcs.getSteelDiamAt(idx):.0f}"
            steel["area"] = f"{self.__rcs.getSteelAreaAt(idx):.1f}"
            steels.append(steel)

        placeHolders["rebars"] = steels

        f.add(
            templateName="template-ita-rc-section-rec.tex",
            templatePlaceholders=placeHolders,
        )
        self._setFragment(f)
        return f
