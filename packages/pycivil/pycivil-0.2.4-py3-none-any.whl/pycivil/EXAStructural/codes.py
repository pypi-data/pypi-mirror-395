from enum import Enum
from typing import List

from pydantic import BaseModel


class CodeEnum(str, Enum):
    NTC2008 = "NTC2008"
    NTC2018 = "NTC2018"
    EC2 = "EC2"
    EC2ITA = "EC2:ITA"
    NTC2018RFI = "NTC2018:RFI"


class CodeInfo(BaseModel):
    """Code information."""

    code: str
    description: str
    author: str
    year: int
    country: str

    def __str__(self):
        """Verbose representation of the code."""
        return (
            f"Code Object: \n"
            f"------------ \n"
            f"    id: {str(self.code)}\n"
            f" descr: {self.description}\n"
        )

    @classmethod
    def from_code(cls, code: str) -> "CodeInfo":
        """
        Returns the code info for the given code

        Args:
            code: Code key

        Returns:
            Code information

        Raises:
            ValueError: on unknown code
        """
        try:
            return KNOWN_CODES[code]
        except KeyError as err:
            raise ValueError(f"Unknown code: {code}") from err


KNOWN_CODES: dict[str, CodeInfo] = {
    "EC2": CodeInfo(
        code="EC2",
        description="Eurocode 2: Design of concrete structures - 2005 Edition",
        author="C.E.N.",
        year=2005,
        country="ITA",
    ),
    "EC2:ITA": CodeInfo(
        code="EC2:ITA",
        description="Eurocodice 2: Progettazione delle strutture in calcestruzzo - 2005 Edition",
        author="U.N.I.",
        year=2005,
        country="ITA",
    ),
    "EC2-1-1:2005:ITA": CodeInfo(
        code="EC2-1-1:2005:ITA",
        description="Eurocode 2 Parte 1-1: Progettazione delle strutture in calcestruzzo – Regole generali e regole "
        "per gli edifici – Edizione del 2005",
        author="U.N.I.",
        year=2005,
        country="ITA",
    ),
    "NTC2008": CodeInfo(
        code="NTC2008",
        description="Norme tecniche per le costruzioni di cui al DM 14 gennaio 2008",
        author="M.I.T.",
        year=2008,
        country="ITA",
    ),
    "NTC2018": CodeInfo(
        code="NTC2018",
        description="Norme tecniche per le costruzioni di cui al DM 17 gennaio 2018",
        author="M.I.T.",
        year=2018,
        country="ITA",
    ),
    "CIRC2008": CodeInfo(
        code="CIRC2008",
        description='Circolare 2 febbraio 2009, n. 617 - Istruzioni per l\'applicazione delle "Nuove norme tecniche per le costruzioni" di cui al D.M. 14 gennaio 2008',
        author="C.S.LL.PP.",
        year=2009,
        country="ITA",
    ),
    "CIRC2018": CodeInfo(
        code="CIRC2018",
        description='Circolare 21 gennaio 2019, n. 2 - Istruzioni per l\'applicazione dell\' "Aggiornamento delle Norme tecniche per le costruzioni" di cui al D.M. 17 gennaio 2018',
        author="C.S.LL.PP.",
        year=2019,
        country="ITA",
    ),
}


class Code:
    """Class to select technical standards

    Class to build code. The code is a selector for technical standars in
    construction. E.g. EC2, NTC2008, NTC2018

    Args:
        codeStr (str): Key to select code

    """

    tabKeys = (
        "EC2",
        "EC2:ITA",
        "NTC2008",
        "NTC2018",
        "CIRC2008",
        "CIRC2018",
        "NTC2018:RFI",
    )
    tabIndices = (0, 1, 2, 3, 4, 5, 6)
    tabDescriptions = (
        "Eurocode 2: Design of concrete structures - 2005 Edition",
        "Eurocode 2: modificato con DAN 20 luglio 2007",
        "Norme tecniche per le costruzioni di cui al DM 14 gennaio 2008",
        "Norme tecniche per le costruzioni di cui al DM 17 gennaio 2018",
        "Circolare esplicativa di cui al DM 14 gennaio 2008",
        "Circolare esplicativa di cui al DM 17 gennaio 2018",
        "Norme tecniche per le costruzioni di cui al DM 17 gennaio 2018 modificate da RFI",
    )

    def __init__(self, codeStr: str = "EC2"):
        self.__i = -1
        if isinstance(codeStr, str):
            if codeStr in self.tabKeys:
                self.__byCode = codeStr
            else:
                raise ValueError(f"Code string {codeStr} not in tabKeys !!!")
        else:
            raise ValueError("Only one str argument !!!")

    def __len__(self):
        return len(self.tabKeys)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__i < self.__len__() - 1:
            self.__i += 1
            return self.tabKeys[self.__i]
        else:
            raise StopIteration()

    def setCodeStr(self, codeStr):
        if isinstance(codeStr, str):
            if codeStr in self.tabKeys:
                self.__byCode = codeStr
            else:
                print("WRN: str not in list !!!")
                self.__byCode = ""
        else:
            raise Exception("Only one str argument !!!")

    def codeStr(self):
        return self.__byCode

    def codeDescr(self, i=-1):
        if i == -1:
            if self.__byCode != "":
                return self.tabDescriptions[self.tabKeys.index(self.__byCode)]
            else:
                return ""
        if i >= 0 and i < len(self.tabKeys):
            return self.tabDescriptions[i]
        else:
            return ""

    def __str__(self):
        dispstr = "Code Object: \n"
        dispstr = dispstr + "--------------- \n"
        dispstr = dispstr + "    id: " + str(self.__byCode) + "\n"
        if self.__byCode in self.tabKeys:
            dispstr = (
                dispstr
                + " descr: "
                + str(self.tabDescriptions[self.tabKeys.index(self.__byCode)])
                + "\n"
            )
        else:
            dispstr = dispstr + " descr: " + "\n"
        return dispstr


class Codes:
    """
    Class to build list of Code.
    """

    def __init__(self, codes: List[Code] = []) -> None:
        if codes is None:
            codes = []
        self.__codes = codes

    def __str__(self):
        dispstr = ""
        for c in self.__codes:
            dispstr += c.__str__()

        return dispstr

    def appendUniqueCode(self, code: Code | None = None, code_str = "") -> bool:
        if code is not None:
            for c in self.__codes:
                if c.codeStr() == code.codeStr():
                    return False
            self.__codes.append(code)
            return True
        if code_str != "":
            for c in self.__codes:
                if c.codeStr() == code_str:
                    return False
            self.__codes.append(Code(code_str))
            return True
        return False

    def getCodes(self) -> List[Code]:
        return self.__codes

    def len(self) -> int:
        return len(self.__codes)
