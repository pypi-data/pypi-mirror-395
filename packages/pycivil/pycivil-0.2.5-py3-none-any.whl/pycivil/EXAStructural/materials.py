import math
from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel

from pycivil.EXAUtils.EXAExceptions import EXAExceptions
from pycivil.EXAStructural.lawcodes.codeEC212 import Aggregates, Moisture, SteelShapingType
from pycivil.EXAStructural.codes import Code, CodeEnum


class Steel_NTC2008_Enum(str, Enum):
    B450A = "B450A"
    B450C = "B450C"


class Steel_NTC2018_Enum(str, Enum):
    B450A = "B450A"
    B450C = "B450C"


class Concrete_NTC2018_Enum(str, Enum):
    C12_15 = "C12/15"
    C16_20 = "C16/20"
    C20_25 = "C20/25"
    C25_30 = "C25/30"
    C28_35 = "C28/35"
    C30_37 = "C30/37"
    C35_45 = "C35/45"
    C40_50 = "C40/50"
    C45_55 = "C45/55"
    C50_60 = "C50/60"
    C55_67 = "C55/67"
    C60_75 = "C60/75"
    C70_85 = "C70/85"
    C80_95 = "C80/95"
    C90_105 = "C90/105"


class Concrete_NTC2008_Enum(str, Enum):
    C12_15 = "C12/15"
    C16_20 = "C16/20"
    C20_25 = "C20/25"
    C25_30 = "C25/30"
    C28_35 = "C28/35"
    C32_40 = "C32/40"
    C35_45 = "C35/45"
    C40_50 = "C40/50"
    C45_55 = "C45/55"
    C50_60 = "C50/60"
    C55_67 = "C55/67"
    C60_75 = "C60/75"
    C70_85 = "C70/85"
    C80_95 = "C80/95"
    C90_105 = "C90/105"


class Environment_Concrete_Enum(str, Enum):
    AGGRESSIVITY_NOT = "not aggressive"
    AGGRESSIVITY_LOW = "low aggressive"
    AGGRESSIVITY_HIGHT = "hight aggressive"
    AGGRESSIVITY_ND = "undefined"


class Environment_Steel_Enum(str, Enum):
    SENSITIVITY_LOW = "not sensitive"
    SENSITIVITY_HIGHT = "sensitive"
    SENSITIVITY_ND = "undefined"


class Material:
    def __init__(self, ids=-1, descr="generic"):
        self.__ids = ids
        self.__descr = descr
        self.__byCode = ""
        self.__catStr = ""

        # Need to know value derived from manual or by code
        self.__setByCode = False

    def setId(self, ids: int) -> None:
        self.__ids = ids

    def getId(self) -> int:
        return self.__ids

    def unsetByCode(self):
        self.__setByCode = False

    def setByCode(self, codeObj: Code, catstr: str = ""):
        if isinstance(codeObj, Code):
            self.__byCode = codeObj.codeStr()
            self.__catStr = catstr
            self.__setByCode = True
        else:
            raise Exception("Only one [Code] argument !!!")

    def isSetByCode(self) -> bool:
        return self.__setByCode

    def codeStr(self) -> str:
        return self.__byCode

    def catStr(self) -> str:
        return self.__catStr

    def getMatDescr(self):
        return self.__descr

    def setMatDescr(self, descr: str):
        self.__descr = descr

    def __str__(self):
        dispstr = "Material Object: \n"
        dispstr = dispstr + "--------------- \n"
        dispstr = dispstr + "  id: " + str(self.__ids) + "\n"
        dispstr = dispstr + "desc: " + str(self.__descr) + "\n"
        dispstr = dispstr + "         code: " + str(self.__byCode) + "\n"
        dispstr = dispstr + "setted byCode: " + str(self.__setByCode) + "\n"
        return dispstr


class Concrete(Material):

    tab_fck = {
        "EC2": {
            "C12/15": 12,
            "C16/20": 16,
            "C20/25": 20,
            "C25/30": 25,
            "C30/37": 30,
            "C32/40": 32,
            "C35/45": 35,
            "C40/50": 40,
            "C45/55": 45,
            "C50/60": 50,
            "C55/67": 55,
            "C60/75": 60,
            "C70/85": 70,
            "C80/95": 80,
            "C90/105": 90,
        },
        "EC2:ITA": {
            "C12/15": 12,
            "C16/20": 16,
            "C20/25": 20,
            "C25/30": 25,
            "C30/37": 30,
            "C32/40": 32,
            "C35/45": 35,
            "C40/50": 40,
            "C45/55": 45,
            "C50/60": 50,
            "C55/67": 55,
            "C60/75": 60,
            "C70/85": 70,
            "C80/95": 80,
            "C90/105": 90,
        },
        "NTC2018": {
            "C12/15": 12,
            "C16/20": 16,
            "C20/25": 20,
            "C25/30": 25,
            "C30/37": 30,
            "C35/45": 35,
            "C40/50": 40,
            "C45/55": 45,
            "C50/60": 50,
            "C55/67": 55,
            "C60/75": 60,
            "C70/85": 70,
            "C80/95": 80,
            "C90/105": 90,
        },
        "NTC2018:RFI": {
            "C12/15": 12,
            "C16/20": 16,
            "C20/25": 20,
            "C25/30": 25,
            "C30/37": 30,
            "C35/45": 35,
            "C40/50": 40,
            "C45/55": 45,
            "C50/60": 50,
            "C55/67": 55,
            "C60/75": 60,
            "C70/85": 70,
            "C80/95": 80,
            "C90/105": 90,
        },
        "NTC2008": {
            "C8/10": 8,
            "C12/15": 12,
            "C16/20": 16,
            "C20/25": 20,
            "C25/30": 25,
            "C28/35": 28,
            "C32/40": 32,
            "C35/45": 35,
            "C40/50": 40,
            "C45/55": 45,
            "C50/60": 50,
            "C55/67": 55,
            "C60/75": 60,
            "C70/85": 70,
            "C80/95": 80,
            "C90/105": 90,
        },
    }

    tab_Rck = {
        "EC2": {
            "C12/15": 15,
            "C16/20": 20,
            "C20/25": 25,
            "C25/30": 30,
            "C30/37": 37,
            "C32/40": 40,
            "C35/45": 45,
            "C40/50": 50,
            "C45/55": 55,
            "C50/60": 60,
            "C55/67": 67,
            "C60/75": 75,
            "C70/85": 85,
            "C80/95": 95,
            "C90/105": 105,
        },
        "EC2:ITA": {
            "C12/15": 15,
            "C16/20": 20,
            "C20/25": 25,
            "C25/30": 30,
            "C30/37": 37,
            "C32/40": 40,
            "C35/45": 45,
            "C40/50": 50,
            "C45/55": 55,
            "C50/60": 60,
            "C55/67": 67,
            "C60/75": 75,
            "C70/85": 85,
            "C80/95": 95,
            "C90/105": 105,
        },
        "NTC2018": {
            "C12/15": 15,
            "C16/20": 20,
            "C20/25": 25,
            "C25/30": 30,
            "C30/37": 37,
            "C35/45": 45,
            "C40/50": 50,
            "C45/55": 55,
            "C50/60": 60,
            "C55/67": 67,
            "C60/75": 75,
            "C70/85": 85,
            "C80/95": 95,
            "C90/105": 105,
        },
        "NTC2018:RFI": {
            "C12/15": 15,
            "C16/20": 20,
            "C20/25": 25,
            "C25/30": 30,
            "C30/37": 37,
            "C35/45": 45,
            "C40/50": 50,
            "C45/55": 55,
            "C50/60": 60,
            "C55/67": 67,
            "C60/75": 75,
            "C70/85": 85,
            "C80/95": 95,
            "C90/105": 105,
        },
        "NTC2008": {
            "C8/10": 10,
            "C12/15": 15,
            "C16/20": 20,
            "C20/25": 25,
            "C25/30": 30,
            "C28/35": 35,
            "C32/40": 40,
            "C35/45": 45,
            "C40/50": 50,
            "C45/55": 55,
            "C50/60": 60,
            "C55/67": 67,
            "C60/75": 75,
            "C70/85": 85,
            "C80/95": 95,
            "C90/105": 105,
        },
    }

    def __init__(self, ids: int = -1, descr: str = "concrete"):

        self.__Rck = 0
        self.__fck = 0
        self.__fctm = 0
        self.__fcm = 0
        self.__ec2 = 0
        self.__ecu = 0
        self.__Ecm = 0
        self.__fct_crack = 0

        # EC2:
        # resistenza effettiva della zona di compressione. Infatti
        # eta*fcd è l'altezza dello stress block
        #
        # NTC2018:
        # coefficiente riduttivo di lunga durata 0.85
        self.__eta = 0

        # EC2:
        # profondità della zona compressa del calcestruzzo nello stress-block
        #
        # NTC2018:
        # come per EC2
        self.__lambda = 0

        # EC2:
        # the coefficient taking account of long term effects on the compressive
        # strength and of unfavourable effects resulting from the way the load
        # is applied.
        #
        # NTC2018:
        # coefficiente riduttivo di lunga durata 0.85
        self.__alphacc = 0
        self.__alphacc_fire = 0

        self.__environnment = "not aggressive"

        self.__gammac = 0
        self.__gammac_fire = 0
        # EC2: limite calceestruzzo combo RARA
        self.__k1 = 0
        # EC2: limite calceestruzzo combo QP
        self.__k2 = 0
        self.__sigmac_max_c = 0
        self.__sigmac_max_q = 0

        # EC212:
        # per il fire design
        self.__aggregates = Aggregates.CALCAREOUS
        self.__moisture = Moisture.v00

        Material.__init__(self, ids, descr)

    def setByCode(self, codeObj: Code, catstr: str = "") -> None:

        if codeObj.codeStr() in self.tab_fck:
            if catstr in self.tab_fck[codeObj.codeStr()]:

                Material.setByCode(self, codeObj, catstr)
                self.__fck = self.tab_fck[codeObj.codeStr()][catstr]
                self.__Rck = self.tab_Rck[codeObj.codeStr()][catstr]

                if (
                    codeObj.codeStr() == "EC2"
                    or codeObj.codeStr() == "EC2:ITA"
                    or codeObj.codeStr() == "NTC2008"
                    or codeObj.codeStr() == "NTC2018"
                    or codeObj.codeStr() == "NTC2018:RFI"
                ):
                    if codeObj.codeStr() == "EC2":
                        self.__alphacc = 1.00
                        self.__alphacc_fire = 1.00
                    else:
                        self.__alphacc = 0.85
                        self.__alphacc_fire = 1.00

                    self.__fcm = self.__fck + 8

                    self.__gammac = 1.5
                    self.__gammac_fire = 1.0

                    if codeObj.codeStr() == "NTC2018:RFI":
                        self.__k1 = 0.55
                        self.__k2 = 0.40
                    else:
                        self.__k1 = 0.6
                        self.__k2 = 0.45

                    self.__sigmac_max_c = self.__k1 * self.__fck
                    self.__sigmac_max_q = self.__k2 * self.__fck

                    # Mega pascal from Giga pascal * 1000
                    self.__Ecm = 22 * pow((self.__fcm / 10), 0.3) * 1000

                    fck_min = 12.0
                    if codeObj.codeStr() == "NTC2008":
                        fck_min = 8.0

                    if fck_min <= self.__fck < 50.0:
                        self.__fctm = 0.3 * (self.__fck ** (2 / 3))
                        self.__ec2 = 0.002
                        self.__ecu = 0.0035
                        self.__lambda = 0.8
                        self.__eta = 1.0

                    elif 50.0 <= self.__fck <= 90.0:
                        self.__fctm = 2.12 * math.log(1 + self.__fcm / 10)
                        self.__ec2 = (2.0 + 0.085 * (self.__fck - 50.0) ** 0.53) / 1000
                        self.__ecu = (
                            2.6 + 35 * (((90.0 - self.__fck) / 100) ** 4)
                        ) / 1000
                        self.__lambda = 0.8 - (self.__fck - 50.0) / 400.0
                        self.__eta = 1.0 + (self.__fck - 50.0) / 200.0

                    else:
                        raise EXAExceptions(
                            "(EXAStructural)-0004",
                            f"fck must be >={fck_min:.3f} and <=90.0",
                            self.__fck,
                        )

                    # Paragraph 4.1.2.2.4 formula [4.1.13] in NTC2018
                    #
                    self.__fct_crack = self.__fctm / 1.2

                else:
                    raise EXAExceptions(
                        "(EXAStructural)-0005", "not implemented", codeObj.codeStr()
                    )
            else:
                raise EXAExceptions("(EXAStructural)-0003", "fck class unknown", catstr)
        else:
            raise EXAExceptions(
                "(EXAStructural)-0002", "codeStr unknown", codeObj.codeStr()
            )

    def set_fck(self, fck):
        self.__fck = fck
        super().unsetByCode()

    def set_Rck(self, Rck):
        self.__Rck = Rck
        super().unsetByCode()

    def set_fctm(self, fctm):
        self.__fctm = fctm
        super().unsetByCode()

    def set_fcm(self, fcm):
        self.__fcm = fcm
        super().unsetByCode()

    def set_ec2(self, ec2):
        self.__ec2 = ec2
        super().unsetByCode()

    def set_ecu(self, ecu):
        self.__ecu = ecu
        super().unsetByCode()

    def set_k1(self, k1):
        self.__k1 = k1
        super().unsetByCode()

    def set_k2(self, k2):
        self.__k2 = k2
        super().unsetByCode()

    def get_k1(self):
        return self.__k1

    def get_k2(self):
        return self.__k2

    def set_lambda(self, lm):
        self.__lambda = lm
        super().unsetByCode()

    def get_fct_crack(self):
        return self.__fct_crack

    def set_fct_crack(self, fct):
        self.__fct_crack = fct
        super().unsetByCode()

    def set_eta(self, eta: float):
        self.__eta = eta
        super().unsetByCode()

    def set_alphacc(self, alphacc: float):
        self.__alphacc = alphacc
        super().unsetByCode()

    def set_alphacc_fire(self, alphacc: float):
        self.__alphacc_fire = alphacc
        super().unsetByCode()

    def set_gammac(self, gammac: float):
        self.__gammac = gammac
        Material.unsetByCode(self)

    def set_gammac_fire(self, gammac_fire):
        self.__gammac_fire = gammac_fire
        Material.unsetByCode(self)

    def get_gammac_fire(self):
        return self.__gammac_fire

    def set_sigmac_max_c(self, sigmac_max_c):
        self.__sigmac_max_c = sigmac_max_c
        Material.unsetByCode(self)

    def set_sigmac_max_q(self, sigmac_max_q):
        self.__sigmac_max_q = sigmac_max_q
        Material.unsetByCode(self)

    def get_fck(self) -> float:
        return self.__fck

    def get_Rck(self) -> float:
        return self.__Rck

    def get_fctm(self) -> float:
        return self.__fctm

    def get_fcm(self) -> float:
        return self.__fcm

    def get_Ecm(self) -> float:
        return self.__Ecm

    def get_ec2(self) -> float:
        return self.__ec2

    def get_ecu(self) -> float:
        return self.__ecu

    def get_lambda(self) -> float:
        return self.__lambda

    def get_eta(self) -> float:
        return self.__eta

    def get_alphacc(self) -> float:
        return self.__alphacc

    def get_alphacc_fire(self) -> float:
        return self.__alphacc_fire

    def getEnvironment(self):
        return self.__environnment

    def getEnvironmentTr(self, lan="IT") -> str:
        if lan == "IT":
            if self.__environnment == "hight-aggressive":
                return "fortemente aggressivo"
            if self.__environnment == "low-aggressive":
                return "aggressivo"
            if self.__environnment == "not aggressive":
                return "non aggressivo"
        return ""

    def cal_fcd(self) -> float:
        return self.__alphacc * self.__fck / self.__gammac

    def isEnvironmentHightAggressive(self):
        return self.__environnment == "hight-aggressive"

    def isEnvironmentAggressive(self):
        return self.__environnment == "low-aggressive"

    def isEnvironmentNotAggressive(self):
        return self.__environnment == "not aggressive"

    def setEnvironmentHightAggressive(self):
        self.__environnment = "hight-aggressive"

    def setEnvironmentAggressive(self):
        self.__environnment = "low-aggressive"

    def setEnvironmentNotAggressive(self):
        self.__environnment = "not aggressive"

    def setEnvironment(
        self, tp: Literal["hight-aggressive", "low-aggressive", "not aggressive"]
    ):
        self.__environnment = tp

    def get_gammac(self) -> float:
        return self.__gammac

    def get_sigmac_max_c(self) -> float:
        return self.__sigmac_max_c

    def cal_sigmac_max_c(self) -> float:
        return self.__k1 * self.__fck

    def cal_sigmac_max_q(self) -> float:
        return self.__k2 * self.__fck

    def get_sigmac_max_q(self) -> float:
        return self.__sigmac_max_q

    def setAggregates(self, aggregates: Aggregates):
        self.__aggregates = aggregates

    def getAggregates(self) -> Aggregates:
        return self.__aggregates

    def setMoisture(self, moisture: Moisture):
        self.__moisture = moisture

    def getMoisture(self) -> Moisture:
        return self.__moisture

    def __str__(self):
        dispstr = super().__str__()
        dispstr = dispstr + "Data embedded-->\n"
        dispstr = dispstr + "        Code = " + str(self.codeStr()) + "\n"
        dispstr = dispstr + "       catStr = " + str(self.catStr()) + "\n"
        dispstr = dispstr + "         fck = " + str(self.__fck) + "\n"
        dispstr = dispstr + "        fctm = " + str(self.__fctm) + "\n"
        dispstr = dispstr + "         fcm = " + str(self.__fcm) + "\n"
        dispstr = dispstr + "         Ecm = " + str(self.__Ecm) + "\n"
        dispstr = dispstr + "         ec2 = " + str(self.__ec2) + "\n"
        dispstr = dispstr + "         ecu = " + str(self.__ecu) + "\n"
        dispstr = dispstr + "         Ecm = " + str(self.__ecu) + "\n"
        dispstr = dispstr + "      lambda = " + str(self.__lambda) + "\n"
        dispstr = dispstr + "         eta = " + str(self.__eta) + "\n"
        dispstr = dispstr + "     alphacc = " + str(self.__alphacc) + "\n"
        dispstr = dispstr + "alphacc fire = " + str(self.__alphacc_fire) + "\n"
        dispstr = dispstr + "      gammac = " + str(self.__gammac) + "\n"
        dispstr = dispstr + " gammac_fire = " + str(self.__gammac_fire) + "\n"
        dispstr = dispstr + "sigmac max c = " + str(self.__sigmac_max_c) + "\n"
        dispstr = dispstr + "sigmac max q = " + str(self.__sigmac_max_q) + "\n"
        dispstr = dispstr + "environnment = " + str(self.__environnment) + "\n"
        return dispstr.replace("\n", "\n  | ")


class ConcreteModel(BaseModel):
    code: CodeEnum = CodeEnum.NTC2018
    mat: Union[
        Concrete_NTC2008_Enum, Concrete_NTC2018_Enum
    ] = Concrete_NTC2008_Enum.C20_25
    descr: str = ""
    bycode: bool = True
    fck: float = -1
    fctm: float = -1
    fcm: float = -1
    ec2: float = -1
    ecu: float = -1
    Ecm: float = -1
    eta: float = -1
    llambda: float = -1
    alphacc: float = -1
    alphacc_fire: float = -1
    gammac: float = -1
    sigmac_max_c: float = -1
    sigmac_max_q: float = -1
    environment: Environment_Concrete_Enum = Environment_Concrete_Enum.AGGRESSIVITY_NOT
    aggregates: Aggregates = Aggregates.CALCAREOUS
    moisture: Moisture = Moisture.v00

    def fromMaterial(self, mat: Material) -> bool:
        if not isinstance(mat, Concrete):
            return False
        self.code = CodeEnum(mat.codeStr())

        if self.code == CodeEnum.NTC2018:
            self.mat = Concrete_NTC2018_Enum(mat.catStr())
        elif self.code == CodeEnum.NTC2008:
            self.mat = Concrete_NTC2008_Enum(mat.catStr())
        else:
            return False

        self.descr = mat.getMatDescr()
        self.bycode = mat.isSetByCode()
        self.fck = mat.get_fck()
        self.fctm = mat.get_fctm()
        self.fcm = mat.get_fcm()
        self.ec2 = mat.get_ec2()
        self.ecu = mat.get_ecu()
        self.Ecm = mat.get_Ecm()
        self.eta = mat.get_eta()
        self.llambda = mat.get_lambda()
        self.alphacc = mat.get_alphacc()
        self.alphacc_fire = mat.get_alphacc_fire()
        self.gammac = mat.get_gammac()
        self.sigmac_max_c = mat.get_sigmac_max_c()
        self.sigmac_max_q = mat.get_sigmac_max_q()
        self.environment = Environment_Concrete_Enum(mat.getEnvironment())
        self.aggregates = mat.getAggregates()
        self.moisture = mat.getMoisture()
        return True

    def toMaterial(self) -> Concrete:
        mat = Concrete(descr=self.descr)
        if self.bycode:
            codeConcrete = Code(self.code.value)
            mat.setByCode(codeConcrete, self.mat.value)
        else:
            mat.set_alphacc(self.alphacc)
            mat.set_alphacc_fire(self.alphacc_fire)
            mat.set_ec2(self.ec2)
            mat.set_ecu(self.ecu)
            mat.set_eta(self.eta)
            mat.set_fcm(self.fcm)
            mat.set_fck(self.fck)
            mat.set_fctm(self.fctm)
            mat.set_lambda(self.llambda)
            mat.set_gammac(self.gammac)
            mat.set_sigmac_max_c(self.sigmac_max_c)
            mat.set_sigmac_max_q(self.sigmac_max_q)

        if (
            self.environment
            == self.environment.AGGRESSIVITY_HIGHT
        ):
            mat.setEnvironmentHightAggressive()
        elif (
            self.environment
            == self.environment.AGGRESSIVITY_LOW
        ):
            mat.setEnvironmentAggressive()
        elif (
            self.environment
            == self.environment.AGGRESSIVITY_NOT
        ):
            mat.setEnvironmentNotAggressive()
        else:
            print("ERR: environment unknown !!!")

        mat.setAggregates(self.aggregates)
        mat.setMoisture(self.moisture)
        return mat

class ConcreteSteel(Material):
    tab_steel = {
        "EC2": {
            "B450A": {
                "fyk": 450,
                "fuk": 450 * 1.05,
                "euk": 0.0025,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.05,
                },
            },
            "B450B": {
                "fyk": 450,
                "fuk": 450 * 1.08,
                "euk": 0.0050,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.08,
                },
            },
            "B450C": {
                "fyk": 450,
                "fuk": 540,
                "euk": 0.0075,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {"geq": 1.15, "leq": 1.35},
            },
        },
        "EC2:ITA": {
            "B450A": {
                "fyk": 450,
                "fuk": 450 * 1.05,
                "euk": 0.0025,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.05,
                },
            },
            "B450B": {
                "fyk": 450,
                "fuk": 450 * 1.08,
                "euk": 0.0050,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.08,
                },
            },
            "B450C": {
                "fyk": 450,
                "fuk": 540,
                "euk": 0.0075,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {"geq": 1.15, "leq": 1.35},
            },
        },
        "NTC2008": {
            "B450A": {
                "fyk": 450,
                "fuk": 450 * 1.05,
                "euk": 0.0025,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.05,
                },
            },
            "B450C": {
                "fyk": 450,
                "fuk": 540,
                "euk": 0.0075,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {"geq": 1.15, "leq": 1.35},
            },
        },
        "NTC2018": {
            "B450A": {
                "fyk": 450,
                "fuk": 450 * 1.05,
                "euk": 0.0025,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.05,
                },
            },
            "B450C": {
                "fyk": 450,
                "fuk": 540,
                "euk": 0.0075,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {"geq": 1.15, "leq": 1.35},
            },
        },
        "NTC2018:RFI": {
            "B450A": {
                "fyk": 450,
                "fuk": 450 * 1.05,
                "euk": 0.0025,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.80,
                "(ft/fy)k": {
                    "geq": 1.05,
                },
            },
            "B450C": {
                "fyk": 450,
                "fuk": 540,
                "euk": 0.0075,
                "Es": 210000,
                "gammas": 1.15,
                "gammas_fire": 1.00,
                "sigmas_max_c_ratio": 0.75,
                "(ft/fy)k": {"geq": 1.15, "leq": 1.35},
            },
        },
    }

    def __init__(self, ids: int = -1, descr: str = "concrete steel"):
        self.__fsy = 0
        self.__Es = 0
        self.__esy = 0
        self.__esu = 0
        self.__fuk = 0
        self.__gammas = 0
        self.__gammas_fire = 0
        self.__shapedType = SteelShapingType.HOT_ROLLED
        self.__sigmas_max_c_ratio = 0
        self.__sigmas_max_c = 0
        self.__sensitivity = "not sensitive"

        Material.__init__(self, ids, descr)

    def setByCode(self, codeObj, catstr=""):
        if codeObj.codeStr() in self.tab_steel:
            if catstr in self.tab_steel[codeObj.codeStr()]:

                Material.setByCode(self, codeObj, catstr)
                self.__fsy = self.tab_steel[codeObj.codeStr()][catstr]["fyk"]
                self.__fuk = self.tab_steel[codeObj.codeStr()][catstr]["fuk"]
                self.__esu = self.tab_steel[codeObj.codeStr()][catstr]["euk"]
                self.__Es = self.tab_steel[codeObj.codeStr()][catstr]["Es"]
                self.__gammas = self.tab_steel[codeObj.codeStr()][catstr]["gammas"]
                self.__gammas_fire = self.tab_steel[codeObj.codeStr()][catstr][
                    "gammas_fire"
                ]
                self.__sigmas_max_c_ratio = self.tab_steel[codeObj.codeStr()][catstr][
                    "sigmas_max_c_ratio"
                ]
                self.__sigmas_max_c = self.__sigmas_max_c_ratio * self.__fsy
                self.__esy = self.__fsy / self.__Es
            else:
                raise EXAExceptions("(EXAStructural)-0007", "steel tag unknown", catstr)
        else:
            raise EXAExceptions(
                "(EXAStructural)-0006", "codeStr unknown", codeObj.codeStr()
            )

    def set_fsy(self, fsy):
        super().unsetByCode()
        self.__fsy = fsy

    def set_fuk(self, fuk):
        super().unsetByCode()
        self.__fuk = fuk

    def get_fuk(self):
        return self.__fuk

    def set_Es(self, Es):
        super().unsetByCode()
        self.__Es = Es

    def set_esy(self, esy):
        super().unsetByCode()
        self.__esy = esy

    def set_esu(self, esu):
        super().unsetByCode()
        self.__esu = esu

    def set_gammas(self, gammas):
        super().unsetByCode()
        self.__gammas = gammas

    def set_gammas_fire(self, gammas_fire):
        super().unsetByCode()
        self.__gammas_fire = gammas_fire

    def get_gammas_fire(self) -> float:
        return self.__gammas_fire

    def set_shapingType(self, tp: SteelShapingType):
        self.__shapedType = tp

    def get_shapingType(self) -> SteelShapingType:
        return self.__shapedType

    def set_sigmas_max_c(self, sigmas_max_c):
        super().unsetByCode()
        self.__sigmas_max_c = sigmas_max_c

    def cal_sigmas_max_c(self):
        return self.__sigmas_max_c_ratio * self.__sigmas_max_c

    def cal_fyd(self):
        return self.__fsy / self.__gammas

    def set_sigmas_max_c_ratio(self, sigmas_max_c_ratio):
        super().unsetByCode()
        self.__sigmas_max_c_ratio = sigmas_max_c_ratio

    def get_sigmas_max_c_ratio(self):
        return self.__sigmas_max_c_ratio

    def get_gammas(self) -> float:
        return self.__gammas

    def get_sigmas_max_c(self) -> float:
        return self.__sigmas_max_c

    def get_fsy(self) -> float:
        return self.__fsy

    def get_Es(self) -> float:
        return self.__Es

    def get_esy(self) -> float:
        return self.__esy

    def get_esu(self) -> float:
        return self.__esu

    def isSteelSensitive(self):
        return self.__sensitivity == "sensitive"

    def setSensitivity(self, tp: Literal["sensitive", "not sensitive"]):
        self.__sensitivity = tp

    def setEnvironmentSensitive(self):
        self.__sensitivity = "sensitive"

    def setEnvironmentNotSensitive(self):
        self.__sensitivity = "not sensitive"

    def getEnvironment(self):
        return self.__sensitivity

    def getEnvironmentTr(self, lan: str = "IT") -> str:
        if lan == "IT":
            if self.__sensitivity == "sensitive":
                return "sensibile"
            if self.__sensitivity == "not sensitive":
                return "poco sensibile"
        return ""

    def __str__(self):
        dispstr = super().__str__()
        dispstr = dispstr + "Data embedded-->\n"
        dispstr = dispstr + "         fsy = " + str(self.__fsy) + "\n"
        dispstr = dispstr + "          Es = " + str(self.__Es) + "\n"
        dispstr = dispstr + "         esy = " + str(self.__esy) + "\n"
        dispstr = dispstr + "         esu = " + str(self.__esu) + "\n"
        dispstr = dispstr + "      gammas = " + str(self.__gammas) + "\n"
        dispstr = dispstr + " gammas_fire = " + str(self.__gammas_fire) + "\n"
        dispstr = dispstr + "sigmas_max_c = " + str(self.__sigmas_max_c) + "\n"
        dispstr = dispstr + " sensitivity = " + str(self.__sensitivity) + "\n"
        return dispstr.replace("\n", "\n  | ")


class SteelModel(BaseModel):
    code: CodeEnum = CodeEnum.NTC2018
    mat: Union[Steel_NTC2008_Enum, Steel_NTC2018_Enum] = Steel_NTC2018_Enum.B450C
    descr: str = ""
    bycode: bool = True
    fsy: float = -1
    Es: float = -1
    esy: float = -1
    esu: float = -1
    gammas: float = -1
    sigmas_max_c: float = -1
    sensitivity: Environment_Steel_Enum = Environment_Steel_Enum.SENSITIVITY_LOW
    formed: SteelShapingType = SteelShapingType.COLD_ROLLED

    def fromMaterial(self, mat: Material) -> bool:
        if not isinstance(mat, ConcreteSteel):
            return False
        self.code = CodeEnum(mat.codeStr())

        if self.code == CodeEnum.NTC2018:
            self.mat = Steel_NTC2018_Enum(mat.catStr())
        elif self.code == CodeEnum.NTC2008:
            self.mat = Steel_NTC2008_Enum(mat.catStr())
        else:
            return False

        self.descr = mat.getMatDescr()
        self.bycode = mat.isSetByCode()
        self.fsy = mat.get_fsy()
        self.Es = mat.get_Es()
        self.esy = mat.get_esy()
        self.esu = mat.get_esu()
        self.gammas = mat.get_gammas()
        self.sigmas_max_c = mat.get_sigmas_max_c()

        self.sensitivity = Environment_Steel_Enum(mat.getEnvironment())
        self.formed = mat.get_shapingType()

        return True

    def toMaterial(self) -> ConcreteSteel:
        mat = ConcreteSteel(descr=self.descr)

        if self.bycode:
            codeSteel = Code(self.code.value)
            mat.setByCode(codeSteel, self.mat.value)
        else:
            mat.set_Es(self.Es)
            mat.set_esu(self.esu)
            mat.set_esy(self.esy)
            mat.set_fsy(self.fsy)
            mat.set_gammas(self.gammas)
            mat.set_sigmas_max_c(self.sigmas_max_c)

        if (
            self.sensitivity
            == self.sensitivity.SENSITIVITY_HIGHT
        ):
            mat.setEnvironmentSensitive()
        elif (
            self.sensitivity
            == self.sensitivity.SENSITIVITY_LOW
        ):
            mat.setEnvironmentNotSensitive()
        else:
            print("ERR: sensitivity unknown !!!")

        mat.set_shapingType(self.formed)
        return mat