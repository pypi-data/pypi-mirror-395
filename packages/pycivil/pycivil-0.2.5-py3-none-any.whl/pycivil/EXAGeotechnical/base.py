import math
from typing import Tuple

from pycivil.EXAUtils.tables import Table as Table


class PhysicalValue:
    def __init__(self):
        self.__physicalValue = None

    def getPhysicalValue(self):
        return self.__physicalValue


class ModulusYoung(Table):
    tab01 = {
        "source": "Appunti di Lunardi",
        "columns": ("id", "Terreno", "E_{tmin}", "E_{tmax}"),
        "udm": ("", "kg/cm^2", "kg/cm^2"),
        "rows": (
            (1, "Argilla molto molle", 3.50, 21.0),
            (2, "Argilla molle", 17.50, 42.0),
            (3, "Argilla di media consistenza", 42.00, 84.0),
            (4, "Argilla compatta", 70.00, 175.0),
            (5, "Argilla limosa", 280.00, 420.0),
            (6, "Limo sabbioso", 70.00, 210.0),
            (7, "Sabbia sciolta", 105.00, 240.0),
            (8, "Sabbia media", 490.00, 840.0),
            (9, "Sabbia densa e ghiaia", 980.00, 1960.0),
        ),
    }

    def __init__(self):
        Table.__init__(self, ModulusYoung.tab01)


class RatioPoisson(Table):
    tab01 = {
        "source": "Appunti di Lunardi",
        "columns": ("id", "Terreno", "ni_{tmin}", "ni_{tmax}"),
        "udm": ("", "", ""),
        "rows": (
            (1, "Argilla satura", 0.40, 0.50),
            (2, "Argilla non satura", 0.10, 0.30),
            (3, "Argilla limosa", 0.20, 0.30),
            (4, "Limo", 0.30, 0.35),
            (5, "Sabbia densa", 0.20, 0.40),
            (6, "Sabbia grossa", 0.15, 0.15),
            (7, "Sabbia fine", 0.25, 0.25),
            (8, "Roccia", 0.10, 0.40),
        ),
    }

    def __init__(self):
        Table.__init__(self, RatioPoisson.tab01)


class Winkler:
    def __init__(self):
        pass

    def estimateTunnelWallHSprings(self, E, ni, a, surf=""):
        """Stima del modulo di sottofondo per i piedritti (Bussinesque)"""
        if surf == "square":
            # per superficie approssimativamente quadrata
            f = 1
        else:
            # per superficie approssimativamente rettangolare
            f = 2.25

        k = 1 / f * E / ((1 - pow(ni, 2)) * a)
        return k

    def estimateTunnelWallVSprings(self, E, ni, B, surf=""):
        """
        (Bussinesque)
        """
        if surf == "square":
            f = 1
        else:
            f = 2.25

        k = 1 / f * E / ((1 - pow(ni, 2)) * B)
        return k

    def estimateTunnelTopArcSprings(self, E, ni, R):
        """
        (Galerkin)
        """
        k = E / ((1 + ni) * R)
        return k

    def estimateTunnelBotArcSprings(self, E, ni, B, surf=""):
        """
        (Bussinesque)
        """
        if surf == "square":
            f = 1
        else:
            f = 2.25

        k = 1 / f * E / ((1 - pow(ni, 2)) * B)
        return k

    def estimateWinklerOnPileHead(
        self, Es: float, Ep: float, D: float, L: float
    ) -> Tuple[float, float, float, float]:
        """It calculates pile-head stiffnesses according to ANNEX-C of EC1998-5

        It calculates pile-head stiffnesses according to ANNEX-C of EC1998-5
        table C.1 with soil type E=Es (third row in table) for KHH, KMM, KHM.
        Last relation for KVV is calculated with Hooke relationship:
                                      Pl     pi*L*G
                                KVV = --- = -------
                                       w       2
        starting from relationship according to Lancellotta's book "Fondazioni":
                                     2*Pl
                                w = ------
                                    pi*L*G
        Args:
            Es (float): Young modulus for terrain [MPa]
            Ep (float): Young modulus for pile material [MPa]
            D (float): Pile diameter [m]
            L (float): Pile lenght [m]

        Returns:
            Tuple with size 4, with horizontal stiffnesses KHH, flexural KMM,
            cross KHM = KMH, vertical KVV gived by [KHH, KMM, KHM, KVV].
            Dimension are [N/m] for translational springs and [N*m/rad] for
            rotational springs.

        """
        print("Dati i seguenti valori: ")
        print(f"Valore del modulo per pali    Ep: {Ep:.3f} [MPa]")
        print(f"Valore del modulo per terreno Es: {Es:.3f} [MPa]")
        print("Si ottiene:")
        Ep = Ep * 1000
        Es = Es * 1000
        KHH = 1.08 * math.pow(Ep / Es, 0.21) * D * Es
        KMM = 0.16 * math.pow(Ep / Es, 0.75) * math.pow(D, 3) * Es
        KHM = -0.22 * math.pow(Ep / Es, 0.50) * math.pow(D, 2) * Es
        KVV = math.pi * L * Es / 3
        print(f"Valore della rigidezza KHH: {KHH:15.3f} [kN/m]")
        print(f"Valore della rigidezza KMM: {KMM:15.3f} [kNm/rad]")
        print(f"Valore della rigidezza KHM: {KHM:15.3f} [kNm/rad]")
        print(f"Valore della rigidezza KVV: {KVV:15.3f} [kN/m]")
        return KHH, KMM, KHM, KVV


class SoilLayer:
    def __init__(self, name: str = ""):
        """It instantiates a soil layer

        Args:
            name: (str): Layer name for identification [...]
        """
        self.__name = name

        # KN/m3
        self.__gamma_d: float = -1.0
        # deg
        self.__phi_d: float = -1.0
        # MPa
        self.__coe_d: float = -1.0

        self.__gamma_w: float = -1.0
        self.__phi_w: float = -1.0
        self.__coe_w: float = -1.0

        self.__coe_u: float = -1.0

        # MPa
        self.__Et: float = -1.0
        # ...
        self.__nit: float = -1.0

    def getPhiDry(self):
        return self.__phi_d

    def getPhiWet(self):
        return self.__phi_w

    def setPhiDry(self, phi: float):
        self.__phi_d = phi

    def setPhiWet(self, phi: float):
        self.__phi_w = phi

    def setEt(self, Et: float) -> None:
        """Set Young module for terrain

        Args:
            Et (float): set Young module for terrain [MPa]
        """
        self.__Et = Et

    def getEt(self) -> float:
        """Get Young module for terrain

        Returns:
            Et (float): Young module for terrain [MPa]
        """
        return self.__Et

    def setNit(self, Nit):
        self.__nit = Nit

    def getNit(self):
        return self.__nit

    def setDry(self, gamma, phi, coe):
        self.__gamma_d = gamma
        self.__phi_d = phi
        self.__coe_d = coe

    def setWet(self, gamma, phi, coe):
        self.__gamma_w = gamma
        self.__phi_w = phi
        self.__coe_w = coe

    def getGammaDry(self):
        return self.__gamma_d

    def setCu(self, cu):
        self.__coe_u = cu

    def calKa(self):
        return (1 - math.sin(math.radians(self.__phi_d))) / (
            1 + math.sin(math.radians(self.__phi_d))
        )

    def calKp(self):
        return 1 / self.calKa()

    def calKo(self):
        return 1 - math.sin(math.radians(self.__phi_d))

    def calZc_dry(self):
        return (
            2 * self.__coe_d / (self.__gamma_d * 10e-06 * math.sqrt(self.calKa()))
        ) / 1000

    def calZc_wet(self):
        return (2 * self.__coe_u / (self.__gamma_d * 10e-06)) / 1000

    def sigmaV_dry(self, z):
        # Mpa
        return self.__gamma_d * z / 1000

    def sigmaV_wet(self, z):
        # Mpa
        return self.__gamma_w * z / 1000

    def sigmaHa_dry(self, z):
        # Mpa
        if z >= self.calZc_dry():
            return (
                self.calKa() * self.__gamma_d * z / 1000
                - 2 * self.__coe_d * math.sqrt(self.calKa())
            )
        else:
            return 0.0

    def sigmaHo_dry(self, z):
        # Mpa
        if z >= self.calZc_dry():
            return (
                self.calKo() * self.__gamma_d * z / 1000
                - 2 * self.__coe_d * math.sqrt(self.calKo())
            )
        else:
            return 0.0

    def sigmaHa_wet(self, z):
        # Mpa
        if z >= self.calZc_wet():
            return self.__gamma_w * z / 1000 - 2 * self.__coe_u
        else:
            return 0.0

    def __str__(self):
        dispstr = f"Soil Layer name: *{self.__name}*\n"
        if self.__gamma_d != -1 or self.__phi_d != -1 or self.__coe_d != -1:
            dispstr += "Dry:\n"
            dispstr += "========\n"
            if self.__gamma_d != -1:
                txt = "{K:.3f} KN/m3"
                dispstr += " gamma' = " + txt.format(K=self.__gamma_d) + "\n"
            if self.__phi_d != -1:
                txt = "{K:.3f} deg"
                dispstr += "   phi' = " + txt.format(K=self.__phi_d) + "\n"
            if self.__coe_d != -1:
                txt = "{K:.3f} Mpa"
                dispstr += "   coe' = " + txt.format(K=self.__coe_d) + "\n"

        if (
            self.__gamma_w != -1
            or self.__phi_w != -1
            or self.__coe_w != -1
            or self.__coe_u != -1
        ):
            dispstr += "Wet:\n"
            dispstr += "========\n"
            if self.__gamma_w != -1:
                txt = "{K:.3f} KN/m3"
                dispstr += " gamma = " + txt.format(K=self.__gamma_w) + "\n"
            if self.__phi_w != -1:
                txt = "{K:.3f} deg"
                dispstr += "   phi = " + txt.format(K=self.__phi_w) + "\n"
            if self.__coe_w != -1:
                txt = "{K:.3f} Mpa"
                dispstr += "   coe = " + txt.format(K=self.__coe_w) + "\n"
            if self.__coe_u != -1:
                txt = "{K:.3f} Mpa"
                dispstr += " coe_u = " + txt.format(K=self.__coe_u) + "\n"

        if self.__Et != -1:
            txt = "{K:.3f} Mpa"
            dispstr += "   Et   (Young Module) = " + txt.format(K=self.__Et) + "\n"

        if self.__nit != -1:
            txt = "{K:.3f}"
            dispstr += "   Nit (Poisson Ratio) = " + txt.format(K=self.__nit) + "\n"

        return dispstr


class EarthPressure:
    def __init__(self):
        pass

    def coulombResultant(
        self,
        layer: SoilLayer,
        alphaWallAngle: float,
        betaTerrainAngle: float,
        deltaWallTerrainAngle: float,
        wallHeight: float,
    ):
        gamma = layer.getGammaDry()
        phi = math.radians(layer.getPhiDry())
        alpha = math.radians(alphaWallAngle)
        beta = math.radians(betaTerrainAngle)
        delta = math.radians(deltaWallTerrainAngle)

        Kap = math.pow(math.sin(alpha + phi), 2) / (
            math.pow(math.sin(alpha), 2)
            * math.sin(alpha - delta)
            * math.pow(
                1
                + math.sqrt(
                    math.sin(phi + delta)
                    * math.sin(phi - beta)
                    / math.sin(alpha - delta)
                    / math.sin(alpha + beta)
                ),
                2,
            )
        )
        print("Kap =", Kap)
        Sap = 1 / 2 * gamma * math.pow(wallHeight, 2) * Kap
        print("Sap =", Sap)
        return Sap

    def seismicMononobeOkabeResultant(
        self,
        layer: SoilLayer,
        kh: float,
        kv: float,
        alphaWallAngle: float,
        betaTerrainAngle: float,
        deltaWallTerrainAngle: float,
        wallHeight: float,
    ):
        gamma = layer.getGammaDry()
        phi = math.radians(layer.getPhiDry())
        alpha = math.radians(alphaWallAngle)
        beta = math.radians(betaTerrainAngle)
        delta = math.radians(deltaWallTerrainAngle)

        thetap = math.atan(kh / (1 + kv))
        thetam = math.atan(kh / (1 - kv))

        theta = thetap
        if beta <= (phi - theta):
            Kaep = math.pow(math.sin(alpha + phi - theta), 2) / (
                math.cos(theta)
                * math.pow(math.sin(alpha), 2)
                * math.sin(alpha - delta - theta)
                * math.pow(
                    1
                    + math.sqrt(
                        math.sin(phi + delta)
                        * math.sin(phi - beta - theta)
                        / math.sin(alpha - delta - theta)
                        / math.sin(alpha + beta)
                    ),
                    2,
                )
            )
        else:
            Kaep = math.pow(math.sin(alpha + phi - theta), 2) / (
                math.cos(theta)
                * math.pow(math.sin(alpha), 2)
                * math.sin(alpha - delta - theta)
            )

        theta = thetam
        if beta <= (phi - theta):
            Kaem = math.pow(math.sin(alpha + phi - theta), 2) / (
                math.cos(theta)
                * math.pow(math.sin(alpha), 2)
                * math.sin(alpha - delta - theta)
                * math.pow(
                    1
                    + math.sqrt(
                        math.sin(phi + delta)
                        * math.sin(phi - beta - theta)
                        / math.sin(alpha - delta - theta)
                        / math.sin(alpha + beta)
                    ),
                    2,
                )
            )
        else:
            Kaem = math.pow(math.sin(alpha + phi - theta), 2) / (
                math.cos(theta)
                * math.pow(math.sin(alpha), 2)
                * math.sin(alpha - delta - theta)
            )

        SaePos = 1 / 2 * gamma * (1 + kv) * math.pow(wallHeight, 2) * Kaep
        SaeNeg = 1 / 2 * gamma * (1 + kv) * math.pow(wallHeight, 2) * Kaem
        print(f"Spinta con kv positivo = {SaePos} [KN]")
        print(f"Spinta con kv negativo = {SaeNeg} [KN]")
        return [
            SaePos,
            SaeNeg,
        ]
