"""
Created on Wed Jan 19 16:09:00 2021

@author: lpaone
"""

import math

from pycivil.EXAUtils import EXAExceptions as ex
from pycivil.EXAGeotechnical import base as geot
from pycivil.EXAStructuralModel import fe as struModel


class CircularTubeShape01:
    def __init__(self, descr, B, H, Tw, Tt, Tb):
        """
        Costruisce uno scatolare circolare delle dimensioni di seguito descritte

        Args:
             B (float): larghezza misurata sulla linea d'asse dei piedritti
             H (float): altezza totale della struttura tra la chiave di calotta e la
                        base dei piedritti
            Tw (float): spessore dei piedritti
            Tt (float): spessore del semicerchio di calotta
            Tb (float): spessore della fondazione

        Returns:
            None:
        """
        self.__descr = descr
        self.__B = B
        self.__H = H
        self.__Tw = Tw
        self.__Tt = Tt
        self.__Tb = Tb

        self.__Kwh = 0
        self.__Kwv = 0
        self.__Ktv = 0
        self.__Kbv = 0

        self.__soilTopLayer = None
        self.__soilBotLayer = None

        self.__topCoverSoil = 0
        self.__paverThickness = 0
        self.__paverGamma = 0

        self.__model = None

        self.__ag_Normalized = None
        self.__betas = None

    def setTopCover(self, c):
        if isinstance(c, float):
            if c >= 0.0:
                self.__topCoverSoil = c
            else:
                raise ex.EXAExceptions(
                    "(EXAParametric)-0004", "cover must be greater than zero", c
                )
        else:
            raise ex.EXAExceptions(
                "(EXAParametric)-0003", "argument must be a float", type(c)
            )

    def getTopCover(self):
        return self.__topCoverSoil

    def setPaverThickness(self, t, gamma):
        # t: spessore in millimetri
        # gamma: peso specifico in KN/mc
        #
        if isinstance(t, float):
            if t >= 0.0 and gamma >= 0.0:
                self.__paverThickness = t
                self.__paverGamma = gamma
            else:
                raise ex.EXAExceptions(
                    "(EXAParametric)-0004",
                    "paver thikness must be greater than zero",
                    t,
                )
        else:
            raise ex.EXAExceptions(
                "(EXAParametric)-0003", "argument must be a float", type(t)
            )

    def getPaverThickness(self):
        return self.__paverThickness

    def assignSeismicAction(self, agn, betas):
        self.__ag_Normalized = agn
        self.__betas = betas

    def model(self):
        return self.__model

    def assignTopLayer(self, soilLayer):
        if isinstance(soilLayer, geot.SoilLayer):
            self.__soilTopLayer = soilLayer
        else:
            raise ex.EXAExceptions(
                "(EXAParametric)-0001", "argument must be a soilLayer", type(soilLayer)
            )

    def assignBotLayer(self, soilLayer):
        if isinstance(soilLayer, geot.SoilLayer):
            self.__soilBotLayer = soilLayer
        else:
            raise ex.EXAExceptions(
                "(EXAParametric)-0002", "argument must be a soilLayer", type(soilLayer)
            )

    def springs(self, Ew=-1, niw=-1, Et=-1, nit=-1, Eb=-1, nib=-1):
        estimator = geot.Winkler()

        if all([Ew != -1, niw != -1, Et != -1, nit != -1, Eb != -1, nib != -1]):
            self.__Kwh = estimator.estimateTunnelWallHSprings(
                Ew, niw, (self.__H - self.__B / 2)
            )
            self.__Kwv = estimator.estimateTunnelWallVSprings(Eb, nib, self.__Tw)
            self.__Ktv = estimator.estimateTunnelBotArcSprings(Eb, nib, self.__B)
            self.__Kbv = estimator.estimateTunnelBotArcSprings(Eb, nib, self.__B)
        else:
            self.__Kwh = estimator.estimateTunnelWallHSprings(
                self.__soilTopLayer.getEt(),
                self.__soilTopLayer.getNit(),
                (self.__H - self.__B / 2),
            )
            self.__Kwv = estimator.estimateTunnelWallVSprings(
                self.__soilBotLayer.getEt(), self.__soilBotLayer.getNit(), self.__Tw
            )
            self.__Ktv = estimator.estimateTunnelBotArcSprings(
                self.__soilBotLayer.getEt(), self.__soilBotLayer.getNit(), self.__B
            )
            self.__Kbv = estimator.estimateTunnelBotArcSprings(
                self.__soilBotLayer.getEt(), self.__soilBotLayer.getNit(), self.__B
            )

    def buildFEModel(self):

        self.__model = struModel.FEModel(self.__descr + " - Modello FE")

        _M = 1 / 1000
        _KNM3 = 1000000

        B = self.__B * _M
        print("B", B)
        H = self.__H * _M
        print("H", H)
        Hw = H - B / 2
        print("Hw", Hw)

        self.__model.addNode(0, 0, 0, 1)
        self.__model.addNode(0, 0, Hw, 2)
        self.__model.addNode(B / 2, 0, H, 3)
        self.__model.addNode(B, 0, Hw, 4)
        self.__model.addNode(B, 0, 0, 5)
        self.__model.addNode(B / 2, 0, Hw, 6)

        self.__model.addFrame(1, 2, 1, nb=15)
        self.__model.addFrame(4, 5, 2, nb=15)
        self.__model.addArc(2, 6, 3, tag=3, nb=10)
        self.__model.addArc(3, 6, 4, tag=4, nb=10)
        self.__model.addFrame(1, 5, 5, nb=15)

        self.__model.addNodesToGroup([1], 1, "A")
        self.__model.addNodesToGroup([2], 2, "B")
        self.__model.addNodesToGroup([3], 3, "C")
        self.__model.addNodesToGroup([4], 4, "D")
        self.__model.addNodesToGroup([5], 5, "E")
        self.__model.addNodesToGroup([6], 6, "CENTER")
        self.__model.addNodesToGroup([1, 2, 3, 4, 5], 7, "vertici")

        self.__model.addFramesToGroup([1, 2, 5], 100, "travi")
        self.__model.addFramesToGroup([3, 4], 200, "arco")
        self.__model.addFramesToGroup([3], 40, "arco-SX")
        self.__model.addFramesToGroup([4], 50, "arco-DX")
        self.__model.addFramesToGroup([1], 10, "ritto-SX")
        self.__model.addFramesToGroup([2], 20, "ritto-DX")
        self.__model.addFramesToGroup([5], 30, "fondazione")

        self.__model.addSectionShape(
            2, "top section", "RECTANGULAR", [self.__Tt * _M, 1.0]
        )
        self.__model.addSectionShape(
            3, "bottom section", "RECTANGULAR", [self.__Tb * _M, 1.0]
        )
        self.__model.addSectionShape(
            4, "wall section", "RECTANGULAR", [self.__Tw * _M, 1.0]
        )

        self.__model.assignMultiFrameSectionShape(
            4, tagsMacro=self.__model.getMacroFramesByPhysicalName("ritto-SX")
        )
        self.__model.assignMultiFrameSectionShape(
            4, tagsMacro=self.__model.getMacroFramesByPhysicalName("ritto-DX")
        )
        self.__model.assignMultiFrameSectionShape(
            2, tagsMacro=self.__model.getMacroFramesByPhysicalName("arco-SX")
        )
        self.__model.assignMultiFrameSectionShape(
            2, tagsMacro=self.__model.getMacroFramesByPhysicalName("arco-DX")
        )
        self.__model.assignMultiFrameSectionShape(
            3, tagsMacro=self.__model.getMacroFramesByPhysicalName("fondazione")
        )

        self.__model.addLoadCase(idCase="SW", tp="R", descr="peso proprio strutture")
        self.__model.addLoadCase(idCase="DL", tp="D", descr="sovraccarichi permanenti")
        self.__model.addLoadCase(
            idCase="TL", tp="L", descr="sovraccarichi variabili da traffico (q1k)"
        )
        self.__model.addLoadCase(
            idCase="TLC", tp="L", descr="sovraccarichi variabili da traffico (Q1K)"
        )
        self.__model.addLoadCase(idCase="EPL", tp="EP", descr="pressione del terreno")
        self.__model.addLoadCase(
            idCase="CL", tp="ER", descr="carico in corso di costruzione"
        )
        self.__model.addLoadCase(idCase="E(-X)", tp="E", descr="sisma statico direzione -X")
        self.__model.addLoadCase(idCase="E(+X)", tp="E", descr="sisma statico direzione +X")
        self.__model.addLoadCase(idCase="E(-Z)", tp="E", descr="sisma statico direzione -Z")

        arcoSX = self.__model.getFramesFromMacroTags(
            macroTags=self.__model.getMacroFramesByPhysicalName("arco-SX")
        )
        arcoDX = self.__model.getFramesFromMacroTags(
            macroTags=self.__model.getMacroFramesByPhysicalName("arco-DX")
        )
        rittoSX = self.__model.getFramesFromMacroTags(
            macroTags=self.__model.getMacroFramesByPhysicalName("ritto-SX")
        )
        rittoDX = self.__model.getFramesFromMacroTags(
            macroTags=self.__model.getMacroFramesByPhysicalName("ritto-DX")
        )
        self.__model.getFramesFromMacroTags(
            macroTags=self.__model.getMacroFramesByPhysicalName("fondazione")
        )

        arcoSX_macro = self.__model.getMacroFramesByPhysicalName("arco-SX")
        arcoDX_macro = self.__model.getMacroFramesByPhysicalName("arco-DX")
        rittoSX_macro = self.__model.getMacroFramesByPhysicalName("ritto-SX")
        rittoDX_macro = self.__model.getMacroFramesByPhysicalName("ritto-DX")
        fondazione_macro = self.__model.getMacroFramesByPhysicalName("fondazione")

        # -----------------------------
        # ASSEGNAZIONE del peso proprio
        # -----------------------------
        self.__model.addSelfWeight(loadCase="SW", GCS=[0.0, 0.0, -1.0])

        # -----------------------------------------------------
        # ASSEGNAZIONE DEI CARICHI PERMANENTI DA PAVIMENTAZIONE
        # -----------------------------------------------------
        qPav = self.__paverGamma * (self.__paverThickness * _M)
        print("qPav = ", qPav)

        # calolo coefficiente di spinta attiva del topLayer
        K_topLayer = self.__soilTopLayer.calKa()
        print("Ka = ", K_topLayer)

        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=arcoSX,
            tp="force",
            GCZ1=[0.0, -qPav],
            GCZ2=[1.0, -qPav],
        )
        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=arcoDX,
            tp="force",
            GCZ1=[0.0, -qPav],
            GCZ2=[1.0, -qPav],
        )

        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=arcoSX,
            tp="force",
            GCX1=[0.0, +qPav * K_topLayer],
            GCX2=[1.0, +qPav * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=arcoDX,
            tp="force",
            GCX1=[0.0, -qPav * K_topLayer],
            GCX2=[1.0, -qPav * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=rittoSX,
            tp="force",
            GCX1=[0.0, +qPav * K_topLayer],
            GCX2=[1.0, +qPav * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="DL",
            tagsFrames=rittoDX,
            tp="force",
            GCX1=[0.0, -qPav * K_topLayer],
            GCX2=[1.0, -qPav * K_topLayer],
        )

        # ------------------------------------------------
        # ASSEGNAZIONE DEI CARICHI IN CORSO DI COSTRUZIONE
        # ------------------------------------------------
        qCos = 20.0
        print("qCos = ", qCos)

        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=arcoSX,
            tp="force",
            GCZ1=[0.0, -qCos],
            GCZ2=[1.0, -qCos],
        )
        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=arcoDX,
            tp="force",
            GCZ1=[0.0, -qCos],
            GCZ2=[1.0, -qCos],
        )

        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=arcoSX,
            tp="force",
            GCX1=[0.0, +qCos * K_topLayer],
            GCX2=[1.0, +qCos * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=arcoDX,
            tp="force",
            GCX1=[0.0, -qCos * K_topLayer],
            GCX2=[1.0, -qCos * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=rittoSX,
            tp="force",
            GCX1=[0.0, +qCos * K_topLayer],
            GCX2=[1.0, +qCos * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="CL",
            tagsFrames=rittoDX,
            tp="force",
            GCX1=[0.0, -qCos * K_topLayer],
            GCX2=[1.0, -qCos * K_topLayer],
        )

        # ------------------------------------------------
        # ASSEGNAZIONE DEI CARICHI DA TRAFFICO DISTRIBUITI
        # ------------------------------------------------
        # Stesa uniforme su corsia di 3m DM2018 in KN/mq
        qTrafUnif = 9
        print("qTrafEff = ", qTrafUnif)
        wCorsia = 3
        print("wCorsia = ", wCorsia)

        alpha_diff_pav = math.radians(45)
        alpha_diff_ter = math.radians(30)
        alpha_diff_sol = math.radians(45)

        wEffective = (
            wCorsia
            + 2
            * (
                math.tan(alpha_diff_pav) * self.__paverThickness
                + math.tan(alpha_diff_ter) * self.__topCoverSoil
                + math.tan(alpha_diff_sol) * self.__Tt
            )
            * _M
        )
        print("wEffective = ", wEffective)
        qTrafEff = qTrafUnif * wCorsia / wEffective
        print("qTrafEff = ", qTrafEff)

        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=arcoSX,
            tp="force",
            GCZ1=[0.0, -qTrafEff],
            GCZ2=[1.0, -qTrafEff],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=arcoDX,
            tp="force",
            GCZ1=[0.0, -qTrafEff],
            GCZ2=[1.0, -qTrafEff],
        )

        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=arcoSX,
            tp="force",
            GCX1=[0.0, +qTrafEff * K_topLayer],
            GCX2=[1.0, +qTrafEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=arcoDX,
            tp="force",
            GCX1=[0.0, -qTrafEff * K_topLayer],
            GCX2=[1.0, -qTrafEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=rittoSX,
            tp="force",
            GCX1=[0.0, +qTrafEff * K_topLayer],
            GCX2=[1.0, +qTrafEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TL",
            tagsFrames=rittoDX,
            tp="force",
            GCX1=[0.0, -qTrafEff * K_topLayer],
            GCX2=[1.0, -qTrafEff * K_topLayer],
        )

        # -------------------------------------------
        # ASSEGNAZIONE DEI CARICHI DA TRAFFICO TANDEM
        # -------------------------------------------
        # Stesa uniforme su corsia di 3m DM2018 in KN/mq
        qTrafTandem = 600
        print("qTrafTandem = ", qTrafTandem)
        wImpronta = 1.6
        hImpronta = 2.4
        print("wImpronta = ", wImpronta)
        print("hImpronta = ", hImpronta)

        wImprontaEff = (
            wImpronta
            + 2
            * (
                math.tan(alpha_diff_pav) * self.__paverThickness
                + math.tan(alpha_diff_ter) * self.__topCoverSoil
                + math.tan(alpha_diff_sol) * self.__Tt
            )
            * _M
        )
        hImprontaEff = (
            hImpronta
            + 2
            * (
                math.tan(alpha_diff_pav) * self.__paverThickness
                + math.tan(alpha_diff_ter) * self.__topCoverSoil
                + math.tan(alpha_diff_sol) * self.__Tt
            )
            * _M
        )
        print("wImprontaEff = ", wImprontaEff)
        print("hImprontaEff = ", hImprontaEff)
        qTandemEff = qTrafTandem / (wImprontaEff * hImprontaEff)
        print("qTandemEff = ", qTandemEff)

        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=arcoSX,
            tp="force",
            GCZ1=[0.0, -qTandemEff],
            GCZ2=[1.0, -qTandemEff],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=arcoDX,
            tp="force",
            GCZ1=[0.0, -qTandemEff],
            GCZ2=[1.0, -qTandemEff],
        )

        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=arcoSX,
            tp="force",
            GCX1=[0.0, +qTandemEff * K_topLayer],
            GCX2=[1.0, +qTandemEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=arcoDX,
            tp="force",
            GCX1=[0.0, -qTandemEff * K_topLayer],
            GCX2=[1.0, -qTandemEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=rittoSX,
            tp="force",
            GCX1=[0.0, +qTandemEff * K_topLayer],
            GCX2=[1.0, +qTandemEff * K_topLayer],
        )
        self.__model.addMultiFrameLoad(
            loadCase="TLC",
            tagsFrames=rittoDX,
            tp="force",
            GCX1=[0.0, -qTandemEff * K_topLayer],
            GCX2=[1.0, -qTandemEff * K_topLayer],
        )

        # ------------------------------------------------------
        # ASSEGNAZIONE DELLA PRESSIONE DEL TERRENO SUL MANUFATTO
        # ------------------------------------------------------
        gamma_topLayer = self.__soilTopLayer.getGammaDry()
        print("gamma = ", gamma_topLayer)
        Zc_topLayer = self.__soilTopLayer.calZc_dry()
        print("Zc_topLayer = ", Zc_topLayer)

        if self.__topCoverSoil <= (self.__H + self.__B):
            print("INF: Caso di poca ricopertura")
            qEp = self.__topCoverSoil * _M * gamma_topLayer
            H0 = (self.__H * _M) - (Zc_topLayer * _M) + (self.__topCoverSoil * _M)
            p0 = 0.0
        else:
            print("INF: Caso di grande ricopertura")
            qEp = (self.__H + self.__B) * _M * gamma_topLayer
            H0 = (self.__H + self.__B + self.__H) * _M
            p0 = 0.0  # (self.__H + self.__B) * _M * gamma_topLayer

        print("qEp = ", qEp)
        print("H0 = ", H0)
        print("p0 = ", p0)

        self.__model.addMultiFrameLoad(
            "EPL", tagsFrames=arcoSX, tp="force", GCZ1=[0.0, -qEp], GCZ2=[1.0, -qEp]
        )
        self.__model.addMultiFrameLoad(
            "EPL", tagsFrames=arcoDX, tp="force", GCZ1=[0.0, -qEp], GCZ2=[1.0, -qEp]
        )

        self.__model.addMultiFrameLoadHydro(
            "EPL",
            tagsMacro=arcoSX_macro,
            dirLoad="GCX",
            gamma=gamma_topLayer,
            K=+K_topLayer,
            H0=H0,
            p0=p0,
            Bref=1.0,
        )
        self.__model.addMultiFrameLoadHydro(
            "EPL",
            tagsMacro=rittoSX_macro,
            dirLoad="GCX",
            gamma=gamma_topLayer,
            K=+K_topLayer,
            H0=H0,
            p0=p0,
            Bref=1.0,
        )

        self.__model.addMultiFrameLoadHydro(
            "EPL",
            tagsMacro=arcoDX_macro,
            dirLoad="GCX",
            gamma=gamma_topLayer,
            K=-K_topLayer,
            H0=H0,
            p0=-p0,
            Bref=1.0,
        )
        self.__model.addMultiFrameLoadHydro(
            "EPL",
            tagsMacro=rittoDX_macro,
            dirLoad="GCX",
            gamma=gamma_topLayer,
            K=-K_topLayer,
            H0=H0,
            p0=-p0,
            Bref=1.0,
        )

        # ----------------------
        # ASSEGNAZIONE DEL SISMA
        # ----------------------
        kh = self.__ag_Normalized * self.__betas
        kv = 0.5 * kh
        qEh = kh * gamma_topLayer * self.__H * _M
        print("qEh = ", qEh)

        if self.__topCoverSoil <= (self.__H + self.__B):
            qEv = kv * gamma_topLayer * self.__topCoverSoil * _M
        else:
            qEv = kv * gamma_topLayer * (self.__H + self.__B) * _M
        print("qEv = ", qEv)

        self.__model.addMultiFrameLoad(
            "E(-X)",
            tagsFrames=rittoDX,
            tp="force",
            GCX1=[0.0, -qEh - qEv],
            GCX2=[1.0, -qEh - qEv],
        )
        self.__model.addMultiFrameLoad(
            "E(-X)",
            tagsFrames=arcoDX,
            tp="force",
            GCX1=[0.0, -qEh - qEv],
            GCX2=[1.0, -qEh - qEv],
        )

        self.__model.addMultiFrameLoad(
            "E(+X)",
            tagsFrames=rittoSX,
            tp="force",
            GCX1=[0.0, +qEh + qEv],
            GCX2=[1.0, +qEh + qEv],
        )
        self.__model.addMultiFrameLoad(
            "E(+X)",
            tagsFrames=arcoSX,
            tp="force",
            GCX1=[0.0, +qEh + qEv],
            GCX2=[1.0, +qEh + qEv],
        )

        self.__model.addMultiFrameLoad(
            "E(-Z)", tagsFrames=arcoSX, tp="force", GCZ1=[0.0, -qEv], GCZ2=[1.0, -qEv]
        )
        self.__model.addMultiFrameLoad(
            "E(-Z)", tagsFrames=arcoDX, tp="force", GCZ1=[0.0, -qEv], GCZ2=[1.0, -qEv]
        )

        # -----------------------------------------------------
        # ASSEGNAZIONE DEI VINCOLI ELASTICI SOLO A COMPRESSIONE
        # -----------------------------------------------------
        self.__model.addMultiFrameWinklerSpring(
            rittoSX_macro, "COMP", "DX-", subgradeModulus=self.__Kwh * _KNM3, Bref=1
        )
        self.__model.addMultiFrameWinklerSpring(
            rittoDX_macro, "COMP", "DX+", subgradeModulus=self.__Kwh * _KNM3, Bref=1
        )
        self.__model.addMultiFrameWinklerSpring(
            arcoSX_macro, "COMP", "DZ+", subgradeModulus=self.__Ktv * _KNM3, Bref=1
        )
        self.__model.addMultiFrameWinklerSpring(
            arcoDX_macro, "COMP", "DZ+", subgradeModulus=self.__Ktv * _KNM3, Bref=1
        )
        self.__model.addMultiFrameWinklerSpring(
            fondazione_macro, "COMP", "DZ-", subgradeModulus=self.__Kbv * _KNM3, Bref=1
        )

    def exportFEModel(self, filename, ext):
        self.__model.save(filename, ext)

    def __str__(self):
        dispstr = ""
        dispstr = dispstr + "  B = " + str(self.__B) + "\n"
        dispstr = dispstr + "  H = " + str(self.__H) + "\n"
        dispstr = dispstr + " Tw = " + str(self.__Tw) + "\n"
        dispstr = dispstr + " Tt = " + str(self.__Tt) + "\n"
        dispstr = dispstr + " Tb = " + str(self.__Tb) + "\n"
        txt = "{K:.8f} N/mm3"
        dispstr = dispstr + " Kwh = " + txt.format(K=self.__Kwh) + "\n"
        dispstr = dispstr + " Kwv = " + txt.format(K=self.__Kwv) + "\n"
        dispstr = dispstr + " Ktv = " + txt.format(K=self.__Ktv) + "\n"
        dispstr = dispstr + " Kbv = " + txt.format(K=self.__Kbv) + "\n"
        return dispstr
