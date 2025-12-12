import math
from enum import Enum

from pycivil.EXAUtils.math import Fun, piecewiseFun


class RMinutes(str, Enum):
    R30 = "R30"
    R60 = "R60"
    R90 = "R90"
    R120 = "R120"
    R150 = "R150"
    R180 = "R180"
    RXXX = "RXXX"


class Moisture(str, Enum):
    v00 = "0.00 %"
    v15 = "1.50 %"
    v30 = "3.00 %"


class Aggregates(str, Enum):
    CALCAREOUS = "calcareous"
    SILICEOUS = "siliceous"


def concreteElongation(theta: float, aggregates: Aggregates) -> float:
    if aggregates == Aggregates.SILICEOUS:
        if 20 <= theta < 700:
            return -1.8e-04 + 9.0e-06 * theta + 2.3e-11 * theta * theta * theta
        elif 700 <= theta <= 1200:
            return 14.0e-03
        else:
            print("Theta greater than 1200 min or less than 20 !!!")
            return 0.0

    elif aggregates == Aggregates.CALCAREOUS:
        if 20 <= theta < 805:
            return -1.2e-04 + 6.0e-06 * theta + 1.4e-11 * theta * theta * theta
        elif 805 <= theta <= 1200:
            return 12.0e-03
        else:
            print("Theta greater than 1200 min or less than 20 !!!")
            return 0.0
    else:
        print("Aggregates unknown !!!")
        return 0.0


def capacity(theta: float, moisture: Moisture) -> float:
    if moisture == Moisture.v00:
        cPeak = 900
    elif moisture == Moisture.v15:
        cPeak = 1470
    elif moisture == Moisture.v30:
        cPeak = 2020
    else:
        print("Moisture unknown !!!")
        return 0.0

    if 20 <= theta and theta <= 100:
        return 900
    elif 100 <= theta and theta <= 115:
        return cPeak
    elif 115 <= theta and theta <= 200:
        return cPeak - (theta - 115) / 85 * (cPeak - 1000)
    elif 200 <= theta and theta <= 400:
        return 1000 + (theta - 200) / 2
    elif 400 <= theta and theta <= 1200:
        return 1100
    else:
        return 0.0


def ro(teta: float, ro20: float = 2300) -> float:
    if 20 <= teta <= 115:
        return ro20
    elif 115 <= teta <= 200:
        return ro20 * (1 - 0.02 * (teta - 115) / 85)
    elif 200 <= teta <= 400:
        return ro20 * (0.98 - 0.03 * (teta - 200) / 200)
    elif 400 <= teta <= 1200:
        return ro20 * (0.95 - 0.07 * (teta - 400) / 800)
    else:
        print("ERR: out of the range !!!")
        return 0.0


def capacityVolumic(
    theta: float, moisture: Moisture = Moisture.v00, ro20: float = 2300
) -> float:
    return ro(theta, ro20) * capacity(theta, moisture)


class LimitCurve(str, Enum):
    INF = "inf"
    SUP = "sup"


def cond(theta: float, limit: LimitCurve) -> float:
    if limit == LimitCurve.INF:
        A = 1.36
        B = 0.136
        C = 0.0057
    elif limit == LimitCurve.SUP:
        A = 2.00
        B = 0.2451
        C = 0.0107
    else:
        print("Limit curve unknown !!!")
        return 0.0

    return A - B * theta / 100 + C * (theta / 100) ** 2


class FireCurve(str, Enum):
    ISO834 = "ISO834"
    HC = "HC"
    HCM = "HCM"
    RWS = "RWS"


def tempByTime(t: float, curve: FireCurve) -> float:
    if curve == FireCurve.ISO834:
        return 20 + 345 * math.log10(8 * t + 1)
    elif curve == FireCurve.HC:
        return 20 + 1080 * (
            1 - 0.325 * math.exp(-0.167 * t) - 0.675 * math.exp(-2.5 * t)
        )
    elif curve == FireCurve.HCM:
        return 20 + 1280 * (
            1 - 0.325 * math.exp(-0.167 * t) - 0.675 * math.exp(-2.5 * t)
        )
    elif curve == FireCurve.RWS:
        if 0.0 <= t and t <= 3.0:
            return 290 * t + 20
        elif 3.0 <= t and t <= 5.0:
            return 125 * t + 515
        elif 5.0 <= t and t <= 10.0:
            return 12 * t + 1080
        elif 10.0 <= t and t <= 30.0:
            return 5 * t + 1150
        elif 30.0 <= t and t <= 60.0:
            return 5 / 3 * t + 1250
        elif 60.0 <= t and t <= 90.0:
            return -5 / 3 * t + 1450
        elif 90.0 <= t and t <= 120.0:
            return -10 / 3 * t + 1600
        elif 120.0 <= t and t <= 180.0:
            return 1200
        else:
            print("Time greater than 180 min !!!")
            return 0.0
    else:
        print("Fire curve unknown !!!")
        return 0.0


class SteelShapingType(str, Enum):
    HOT_ROLLED = "hot rolled"
    COLD_ROLLED = "cold rolled"


class StressType(Enum):
    TENSION = "tension"
    COMPRESSION = "compression"


def kappa_s(
    teta: float,
    shaping: SteelShapingType = SteelShapingType.HOT_ROLLED,
    stress: StressType = StressType.TENSION,
) -> float:

    if stress == StressType.COMPRESSION:
        if 20 <= teta and teta < 100:
            return 1.0
        elif 100 <= teta and teta < 400:
            return 0.7 - 0.3 * (teta - 400) / 300
        elif 400 <= teta and teta < 500:
            return 0.57 - 0.13 * (teta - 500) / 100
        elif 500 <= teta and teta < 700:
            return 0.10 - 0.47 * (teta - 700) / 200
        elif 700 <= teta and teta <= 1200:
            return 0.10 * (1200 - teta) / 500
        else:
            print("ERR: out of the range !!!")
        return 0.0
    else:
        if shaping == SteelShapingType.HOT_ROLLED:
            if 20 <= teta and teta < 400:
                return 1.0
            elif 400 <= teta and teta < 500:
                return -2.20e-03 * teta + 1.88
            elif 500 <= teta and teta < 600:
                return -3.10e-03 * teta + 2.33
            elif 600 <= teta and teta < 700:
                return -2.40e-03 * teta + 1.91
            elif 700 <= teta and teta < 800:
                return -1.20e-03 * teta + 1.07
            elif 800 <= teta and teta < 900:
                return -5.00e-04 * teta + 0.51
            elif 900 <= teta and teta <= 1200:
                return -2.00e-04 * teta + 0.24
            else:
                print("ERR: out of the range !!!")
            return 0.0

        elif shaping == SteelShapingType.COLD_ROLLED:
            if 20 <= teta and teta < 300:
                return 1.0
            elif 300 <= teta and teta < 400:
                return -6.00e-04 * teta + 1.18
            elif 400 <= teta and teta < 600:
                return -2.70e-03 * teta + 2.02
            elif 600 <= teta and teta < 700:
                return -2.80e-03 * teta + 2.08
            elif 700 <= teta and teta < 800:
                return -1.00e-04 * teta + 0.19
            elif 800 <= teta and teta < 1000:
                return -3.00e-04 * teta + 0.35
            elif 1000 <= teta and teta < 1100:
                return -2.00e-04 * teta + 0.25
            elif 1100 <= teta and teta <= 1200:
                return -3.00e-04 * teta + 0.36
            else:
                print("ERR: out of the range !!!")

            return 0.0

        else:
            print("ERR: SteelShapingType unknown !!!")

    return 0.0


class fck_theta_div_fck(piecewiseFun):
    def __init__(self, aggregates: Aggregates = Aggregates.SILICEOUS):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if aggregates == Aggregates.SILICEOUS:
            val = [
                1.0,
                1.0,
                0.95,
                0.85,
                0.75,
                0.60,
                0.45,
                0.30,
                0.15,
                0.08,
                0.04,
                0.01,
                0.00,
            ]
        else:
            val = [
                1.0,
                1.0,
                0.97,
                0.91,
                0.85,
                0.74,
                0.60,
                0.43,
                0.27,
                0.15,
                0.06,
                0.02,
                0.00,
            ]

        piecewiseFun.__init__(self, theta, val)


class ec1_theta(piecewiseFun):
    def __init__(self, aggregates: Aggregates = Aggregates.SILICEOUS):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if aggregates == Aggregates.SILICEOUS:
            val = [
                0.0025,
                0.0040,
                0.0055,
                0.0070,
                0.0100,
                0.0150,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
            ]
        else:
            val = [
                0.0025,
                0.0040,
                0.0055,
                0.0070,
                0.0100,
                0.0150,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
                0.025,
            ]
        piecewiseFun.__init__(self, theta, val)


class ecu1_theta(piecewiseFun):
    def __init__(self, aggregates: Aggregates = Aggregates.SILICEOUS):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if aggregates == Aggregates.SILICEOUS:
            val = [
                0.0200,
                0.0225,
                0.0250,
                0.0275,
                0.0300,
                0.0325,
                0.0350,
                0.0375,
                0.0400,
                0.0425,
                0.0450,
                0.0475,
                0.0500,
            ]
        else:
            val = [
                0.0200,
                0.0225,
                0.0250,
                0.0275,
                0.0300,
                0.0325,
                0.0350,
                0.0375,
                0.0400,
                0.0425,
                0.0450,
                0.0475,
                0.0500,
            ]
        piecewiseFun.__init__(self, theta, val)


class fc_theta_epsi(Fun):
    def __init__(
        self,
        fck: float,
        aggregates: Aggregates = Aggregates.SILICEOUS,
        theta: float = 20,
    ):
        super().__init__()
        self.__theta = theta
        self.__aggregates = aggregates
        self.__fck = fck

    @property
    def theta(self):
        return self.__theta

    @theta.setter
    def theta(self, val: float) -> None:
        if 20 <= val <= 1200:
            self.__theta = val
        else:
            raise ValueError("val must be in the field [20,1200]")

    @theta.deleter
    def theta(self):
        del self.__theta

    def eval(self, x: float) -> float:

        fc = fck_theta_div_fck(self.__aggregates).eval(self.__theta) * self.__fck
        ec1 = ec1_theta(self.__aggregates).eval(self.__theta)
        ecu1 = ecu1_theta(self.__aggregates).eval(self.__theta)

        if x >= 0 and x < ec1:
            return 3 * fc * x / (ec1 * (2 + (x / (ec1)) * (x / (ec1)) * (x / (ec1))))
        elif x >= ec1 and x < ecu1:
            return fc * (ecu1 - x) / (ecu1 - ec1)
        else:
            return 0.0


class fsy_theta_div_fyk(piecewiseFun):
    def __init__(self, formed: SteelShapingType = SteelShapingType.HOT_ROLLED):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if formed == SteelShapingType.HOT_ROLLED:
            val = [
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                0.78,
                0.47,
                0.23,
                0.11,
                0.06,
                0.04,
                0.02,
                0.00,
            ]
        else:
            val = [
                1.0,
                1.0,
                1.0,
                1.0,
                0.94,
                0.67,
                0.40,
                0.12,
                0.11,
                0.08,
                0.05,
                0.03,
                0.00,
            ]

        piecewiseFun.__init__(self, theta, val)


class fsp_theta_div_fyk(piecewiseFun):
    def __init__(self, formed: SteelShapingType = SteelShapingType.HOT_ROLLED):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if formed == SteelShapingType.HOT_ROLLED:
            val = [
                1.0,
                1.0,
                0.81,
                0.61,
                0.42,
                0.36,
                0.18,
                0.07,
                0.05,
                0.04,
                0.02,
                0.01,
                0.00,
            ]
        else:
            val = [
                1.0,
                0.96,
                0.92,
                0.81,
                0.63,
                0.44,
                0.26,
                0.08,
                0.06,
                0.05,
                0.03,
                0.02,
                0.00,
            ]

        piecewiseFun.__init__(self, theta, val)


class Es_theta_div_Es(piecewiseFun):
    def __init__(self, formed: SteelShapingType = SteelShapingType.HOT_ROLLED):
        theta = [
            20.0,
            100.0,
            200.0,
            300.0,
            400.0,
            500.0,
            600.0,
            700.0,
            800.0,
            900.0,
            1000.0,
            1100.0,
            1200.0,
        ]
        if formed == SteelShapingType.HOT_ROLLED:
            val = [
                1.00,
                1.00,
                0.90,
                0.80,
                0.70,
                0.60,
                0.31,
                0.13,
                0.09,
                0.07,
                0.04,
                0.02,
                0.00,
            ]
        else:
            val = [
                1.00,
                1.00,
                0.87,
                0.72,
                0.56,
                0.40,
                0.24,
                0.08,
                0.06,
                0.05,
                0.03,
                0.02,
                0.00,
            ]

        piecewiseFun.__init__(self, theta, val)


class fs_theta_epsi(Fun):
    def __init__(
        self,
        fyk: float,
        Es: float,
        formed: SteelShapingType = SteelShapingType.HOT_ROLLED,
        theta: float = 20,
    ):
        super().__init__()
        self.__theta = theta
        self.__formed = formed
        self.__fyk = fyk
        self.__Es = Es

    @property
    def theta(self):
        return self.__theta

    @theta.setter
    def theta(self, val: float) -> None:
        if 20 <= val <= 1200:
            self.__theta = val
        else:
            raise ValueError("val must be in the field [20,1200]")

    @theta.deleter
    def theta(self):
        del self.__theta

    def eval(self, x: float) -> float:

        Es_theta = Es_theta_div_Es(self.__formed).eval(self.__theta) * self.__Es
        fsy_theta = fsy_theta_div_fyk(self.__formed).eval(self.__theta) * self.__fyk
        fsp_theta = fsp_theta_div_fyk(self.__formed).eval(self.__theta) * self.__fyk

        esp_theta = fsp_theta / Es_theta
        esy_theta = 0.02
        est_theta = 0.15
        esu_theta = 0.20

        c = ((fsy_theta - fsp_theta) ** 2) / (
            (esy_theta - esp_theta) * Es_theta - 2 * (fsy_theta - fsp_theta)
        )
        a = math.sqrt((esy_theta - esp_theta) * (esy_theta - esp_theta + c / Es_theta))
        b = math.sqrt(c * (esy_theta - esp_theta) * Es_theta + c**2)

        if 0 <= x < esp_theta:
            return x * Es_theta
        elif esp_theta <= x < esy_theta:
            return fsp_theta - c + (b / a) * math.sqrt(a**2 - (esy_theta - x) ** 2)
        elif esy_theta <= x < est_theta:
            return fsy_theta
        elif est_theta <= x < esu_theta:
            return fsy_theta * (1 - (x - est_theta) / (esu_theta - est_theta))
        else:
            return 0.0
