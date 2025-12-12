"""Module with classes for generate reports various formats.

Main class in module is Reporter. Reporter uses actually only LaTex executable
for build reports.

Classes list:

    1. EnumFBSection
    2. Fragment
    3. FragmentsBuilder
    4. getTemplatesPath
    5. ReportDriverEnum
    6. Reporter
    7. ReportProperties
    8. ReportTemplateEnum
"""

import os
import subprocess
from enum import Enum, unique
from importlib.resources import files
from pathlib import Path
from typing import Any, Dict, List, Literal, Union
import shutil

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from pycivil.EXAUtils.EXAExceptions import EXAExceptions
from pycivil.EXAUtils import logging as logger


@unique
class ReportDriverEnum(Enum):
    PDFLATEX = 1

@unique
class ReportTemplateEnum(Enum):
    """This Enum describe the main documents level

    Attributes:
        TEX_ENG_CAL: style for official reports
        TEX_KOMA: styled with KOMA scripts LaTex
        TEX_MAIN: styled with main LaTex
    """
    TEX_ENG_CAL = 1
    TEX_KOMA = 2
    TEX_MAIN = 3


def getTemplatesPath() -> Path:
    """Funtion to get templates latex path.

    Returns:
        A Path object.
    """
    return Path(str(files("pycivil") / "templates" / "latex"))


class Fragment:
    """Class that hold fragments as list of strings for use with Reporter.

    This class is a container for complete a template (ex. LaTex template).
    Template are processed after with Reporter class. Will be generated
    automatically a type of file. For example PDF or MD etc.

    """
    def __init__(self, latexTemplatePath: Path = ""):
        self.__fragment: List[str] = []
        self.__latexTemplatePath: Path = latexTemplatePath

    def add_line(self, line: str) -> None:
        self.__fragment.append(line)

    def add_lines(self, lines: List[str]) -> None:
        for ll in lines:
            if ll is not None:
                self.__fragment.append(ll)

    def add_template(self, name: str, placeholders: Dict[str, Any]) -> None:
        file_loader = FileSystemLoader(searchpath=self.__latexTemplatePath)
        env = Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%-",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=file_loader,
        )
        jtemplate = env.get_template(name)
        logoPath = self.__latexTemplatePath / "logo.png"
        rendered = jtemplate.render(placeholders, logo_path=logoPath.as_posix())
        self.__fragment.append(rendered)

    def add(
        self,
        line: Union[str, None] = None,
        lines: Union[List[str], None] = None,
        templateName: Union[str, None] = None,
        templatePlaceholders: Union[dict, None] = None,
    ) -> int:
        if (
            line is not None
            and templateName is None
            and templatePlaceholders is None
            and lines is None
        ):
            self.add_line(line)
        elif (
            line is None
            and lines is None
            and templateName is not None
            and templatePlaceholders is not None
        ):
            self.add_template(templateName, templatePlaceholders)
        elif (
            line is None
            and lines is not None
            and templateName is None
            and templatePlaceholders is None
        ):
            self.add_lines(lines)
        else:
            raise EXAExceptions("0001", "Wrong args", "")
        return len(self.__fragment)

    def frags(self) -> List[str]:
        return self.__fragment


@unique
class EnumFBSection(Enum):
    SEC_CHAPTER = 1
    SEC_SECTION = 2
    SEC_SUBSECTION = 3
    SEC_SUBSUBSECTION = 4


class FragmentsBuilder:
    def __init__(self):
        self.__fragment: Union[Fragment, None] = None
        self.__fragment_options: dict = {}

    def _setFragment(self, f: Fragment):
        self.__fragment = f

    def getFragmentOptions(self) -> dict:
        return self.__fragment_options

    def _setFragmentOptions(self, options: dict) -> bool:
        self.__fragment_options = options
        return True

    def setFragmentOptions(self, options: dict) -> bool:
        for name_opt, value_opt in options.items():
            if name_opt not in self.__fragment_options.keys():
                raise ValueError(f"{name_opt} is not a valid option")
        self.__fragment_options = options
        return True

    def buildFragment(self) -> Fragment:
        raise NotImplementedError("Need to be implemented")

    def fragment(self) -> Union[Fragment, None]:
        return self.__fragment


class ReportProperties(BaseModel):
    project_brief: str = "Brief"
    module_name: str = "Module Name"
    module_version: str = "Module Version"
    report_designer: str = "Designer user name"
    report_date: str = "18/01/1972"
    report_time: str = "01:30"
    report_token: str = "xxxxxxx"


class Reporter:
    r"""Class that compiles fragments to produce PDF or others.

    This class compiles fragments to produce PDF or others type of files.
    Actually produces PDF using LaTex files by one of LaTeX implementations as
    MikTex (popular implementation for Windows) or TexLive (popular on Linux).

    Typical usage example:

    ```
     reporter = Reporter(latexTemplatePath)
     reporter.linkFragments(ReportDriverEnum.PDFLATEX, ReportTemplateEnum.TEX_ENG_CAL, [frag_title, frag])
     reporter.makePDF(path=str(working_path), fileName="TEX_ENG_CAL")
    ```
    """
    def __init__(self, latexTemplatePath: Path):
        self.__main_file_name: str = ""
        self.__templated: Union[str, None] = ""
        self.__sepForTex: str = "\n"
        self.__opt_makeGlossary: bool = False
        self.__ll: Literal[0, 1, 2, 3] = 3
        self.__latexTemplatePath: Path = latexTemplatePath
        self.__properties: ReportProperties = ReportProperties()

    def setProperties(self, prop: ReportProperties):
        self.__properties = prop

    def compileDocument(
        self,
        path: str = "",
        fileName: str = "report",
        verbose: bool = False,
        deleteIfExists: bool = True,
    ):
        """Build a PDF using driver LATEXPDF

        Write before templated in <path> with name <fileName>.
        Extension are automatically added at the end of file name.

        Args:
            deleteIfExists (bool, optional): if True delete file pdf if exists
            verbose (bool, optional):
            path (str, optional): where intermediate file are crated. Defaults to ''.
            fileName (str, optional): input file name. Defaults to 'report'.
        """
        completeFileName = Path(f"{path}/{fileName}")
        completeFileNameTex = Path(f"{completeFileName}.tex")
        completeFileNamePdf = Path(f"{completeFileName}.pdf")

        # Save tex file
        with open(file=completeFileNameTex, mode="w", encoding="utf-8") as f:
            f.write(self.__templated)  # type: ignore

        if deleteIfExists:
            if os.path.exists(completeFileNamePdf):
                os.remove(completeFileNamePdf)
                logger.log(
                    tp="INF", level=self.__ll, msg=f"removed file {completeFileNamePdf}"
                )
            else:
                logger.log(
                    tp="INF",
                    level=self.__ll,
                    msg=f"file do not exists {completeFileNamePdf}",
                )

        # Compile
        os.chdir(path)
        os.listdir()
        #
        # FIRST RUN PDFLATEX
        #
        print("Setted make glossary:")
        print("... 1/4 run first pdflatex")
        self._run_latex(str(completeFileNameTex), verbose)
        if not self.__opt_makeGlossary:
            print("... 2/4 no run makeglossaries")
        else:
            self._make_glossaries(fileName, path, verbose)

        #
        # SECOND RUN PDFLATEX
        #
        print("... 3/4 run pdflatex for tables width adjust")
        self._run_latex(str(completeFileNameTex), verbose)

        #
        # THIRD RUN PDFLATEX
        #
        print("... 4/4 run pdflatex for tables width adjust")
        if self._run_latex(str(completeFileNameTex), verbose):
            print(f"PDF generated as {completeFileNamePdf}")

    def _make_glossaries(self, fileName, path, verbose):
        #
        # SECOND RUN MAKEGLOSSARIES
        #
        print("... 2/4 run makeglossaries")
        print(f"Current working directory: {os.getcwd()}")
        cwdOld = os.getcwd()
        os.chdir(path)
        print(f"for makeglossaries working directory: {os.getcwd()}")
        self._run_command(["makeglossaries", fileName], verbose)
        os.chdir(cwdOld)

    def _run_latex(self, file_name: str, verbose: bool = False) -> bool:
        logger.log("INF", msg=f"File name pdflatex run is in {file_name}", level=self.__ll)

        return self._run_command(["pdflatex", "--no-shell-escape",file_name], verbose)

    @staticmethod
    def _run_command(args: List[str], verbose: bool = False) -> bool:
        # Check if pdflatex is in PATH

        program_path = shutil.which(args[0])
        if shutil.which(args[0]):
            print(f"{program_path} found in PATH {program_path}")
        else:
            print(f"{program_path} NOT found in PATH - need to install")
        print(args)

        if os.name == "nt":
            x = subprocess.run(
                executable=None,
                args=args,
                text=True,
                shell=True,
                capture_output=not verbose)
        else:
            x = subprocess.run(
                executable=args[0],
                args=args[1:len(args)],
                text=True,
                shell=True,
                capture_output=not verbose)

        if x != 0:
            print("... Exit-code not 0, check result!")
        else:
            print("... Exit-code 0")
        return x == 0

    def linkFragments(
        self,
        template: ReportTemplateEnum,
        driver: ReportDriverEnum = ReportDriverEnum.PDFLATEX,
        fragments: List[Fragment] | None = None,
        builder: Union[FragmentsBuilder, List[FragmentsBuilder]] | None = None,
        glossary: bool = False,
        main_file_name: str = "",
    ) -> bool:
        """Links fragments adding also a main documents.

        Links fragments adding also a main documents. For example in LaTex
        the linking process add

        ```LaTex
            \\documentclass[11pt,a4paper]{article}
            \\usepackage[latin1]{inputenc}
            ...
            \\begin{document}
            ...
            Fragment line 1
            Fragment line 2
            ...
            Fragment line n
            ...
            \\end{document}
        ```

        Args:
            template (ReportTemplateEnum):
             Enum for main document template.
            driver (ReportDriverEnum, Optional):
             Leave default option.
            fragments (List[Fragment], Optional):
             List of rows to put in main document.
            builder (Union[FragmentsBuilder, List[FragmentsBuilder]], Optional):
             List of fragment builder. This is alternative to fragments
             argument. Default is None.
            glossary (bool, optional): Default is False.
            main_file_name (str, optional): Default is "".

        Returns:
            True on success, False otherwise
        """
        self.__opt_makeGlossary = glossary
        self.__main_file_name = main_file_name
        print("buildPDF: start ...")

        if builder is not None:
            if not isinstance(builder, list):
                builders = [builder]
            else:
                builders = builder

            fragments: List[Fragment] = []
            for b in builders:
                fragments.append(b.buildFragment())

        united = []
        for f in fragments:
            if f.frags() is not None:
                united += f.frags()  # type: ignore
            else:
                print("ERR: None fragment")
                print("buildPDF: Quit")
                return False

        if driver != ReportDriverEnum.PDFLATEX:
            print("ERR: driver unknown !!! quit")
            return False

        file_loader = FileSystemLoader(searchpath=self.__latexTemplatePath)
        env = Environment(
            block_start_string="\\BLOCK{",
            block_end_string="}",
            variable_start_string="\\VAR{",
            variable_end_string="}",
            comment_start_string="\\#{",
            comment_end_string="}",
            line_statement_prefix="%-",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=file_loader,
        )

        print("build with pdflatex ...")

        # LaTex substitution strings
        #
        # 1) Changing "_" with "\_" for latex
        project_brief = self.__properties.project_brief.replace("_", r"\_")

        if (
            template == ReportTemplateEnum.TEX_ENG_CAL
            or template == ReportTemplateEnum.TEX_MAIN
        ):
            print("... template TEX_ENG_CAL")
            if template == ReportTemplateEnum.TEX_ENG_CAL:
                jtemplate = env.get_template("template-eng-cal.tex")
            else:
                jtemplate = env.get_template(self.__main_file_name)
            logoPath = self.__latexTemplatePath / "logo.png"
            self.__templated = jtemplate.render(
                place_holder=self.__sepForTex.join(united),
                glossary=self.__opt_makeGlossary,
                logo_path=logoPath.as_posix(),
                project_brief=project_brief,
                module_name=self.__properties.module_name,
                module_version=self.__properties.module_version,
                report_designer=self.__properties.report_designer,
                report_date=self.__properties.report_date,
                report_time=self.__properties.report_time,
                report_token=self.__properties.report_token,
            )

        elif template == ReportTemplateEnum.TEX_KOMA:
            print("... template TEX_KOMA")
            jtemplate = env.get_template("template-koma.tex")
            self.__templated = jtemplate.render(
                glossary=self.__opt_makeGlossary,
                place_holder=self.__sepForTex.join(united),
            )

        else:
            print("ERR: driver unknown !!! quit")
            return False

        return True
