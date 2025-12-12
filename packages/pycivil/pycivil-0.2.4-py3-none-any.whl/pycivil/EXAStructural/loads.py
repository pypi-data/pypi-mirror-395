from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel


class Frequency_Enum(str, Enum):
    QUASI_PERMANENT = "quasi-permanent"
    CHARACTERISTIC = "characteristic"
    FREQUENT = "frequent"
    FREQUENCY_ND = "ND"


class LimiteState_Enum(str, Enum):
    ULTIMATE = "ultimate"
    SERVICEABILITY = "serviceability"
    ACCIDENTAL = "accidental"
    LIMIT_STATE_ND = "ND"


# YHL_ZTD_XCCW default for RECTANGULAR section solver
# XHL_YTD_ZCCW default for general section DOMAIN
# YHL_XDT_ZCCW default for general ELASTIC section solver
class Ref_Enum(str, Enum):
    YHL_ZTD_XCCW = "YHL_ZTD_XCCW"  # default for force
    XHL_YTD_ZCCW = "XHL_YTD_ZCCW"
    YHL_XDT_ZCCW = "YHL_XDT_ZCCW"


class ForcesOnSection(BaseModel):
    Fx: Union[float, int] = 0
    Fy: Union[float, int] = 0
    Fz: Union[float, int] = 0
    Mx: Union[float, int] = 0
    My: Union[float, int] = 0
    Mz: Union[float, int] = 0
    descr: str = ""
    id: int = 0
    frequency: Frequency_Enum = Frequency_Enum.FREQUENCY_ND
    limitState: LimiteState_Enum = LimiteState_Enum.LIMIT_STATE_ND
    ref: Ref_Enum = Ref_Enum.YHL_ZTD_XCCW

    def setLimitState(self, ls: Literal["ultimate", "serviceability", "accidental", "ND"]):
        self.limitState = LimiteState_Enum(ls)

    def setFrequency(self, fr: Literal["quasi-permanent", "characteristic", "frequent", "ND"]):
        self.frequency = Frequency_Enum(fr)

    def switchToNamedRef(
        self, newRef: Literal["DEFAULT", "DOMAIN", "ELASTIC"] = "DEFAULT"
    ):
        if newRef == "DEFAULT":
            self.switchToRef(Ref_Enum.YHL_ZTD_XCCW)
        if newRef == "DOMAIN":
            self.switchToRef(Ref_Enum.XHL_YTD_ZCCW)
        if newRef == "ELASTIC":
            self.switchToRef(Ref_Enum.YHL_XDT_ZCCW)

    def switchToRef(self, newRef: Ref_Enum):
        new_Fx = self.Fx
        new_Fy = self.Fy
        new_Fz = self.Fz
        new_Mx = self.Mx
        new_My = self.My
        new_Mz = self.Mz
        if newRef is Ref_Enum.YHL_ZTD_XCCW:
            if self.ref is Ref_Enum.YHL_ZTD_XCCW:
                pass
            elif self.ref is Ref_Enum.XHL_YTD_ZCCW:
                new_Fy = self.Fx
                new_Fz = self.Fy
                new_Fx = self.Fz
                new_My = self.Mx
                new_Mz = self.My
                new_Mx = self.Mz
            else:  # self.ref is Ref_Enum.YHL_XDT_ZCCW:
                new_Fz = -self.Fx
                new_Fx = self.Fz
                new_Mz = -self.Mx
                new_Mx = self.Mz
        elif newRef is Ref_Enum.XHL_YTD_ZCCW:
            if self.ref is Ref_Enum.YHL_ZTD_XCCW:
                new_Fx = self.Fy
                new_Fy = self.Fz
                new_Fz = self.Fx
                new_Mx = self.My
                new_My = self.Mz
                new_Mz = self.Mx
            elif self.ref is Ref_Enum.XHL_YTD_ZCCW:
                pass
            if self.ref is Ref_Enum.YHL_XDT_ZCCW:
                new_Fx = self.Fy
                new_Fy = self.Fx
                new_Mx = self.My
                new_My = self.Mx
        else:  # newRef is Ref_Enum.YHL_XDT_ZCCW:
            if self.ref is Ref_Enum.YHL_ZTD_XCCW:
                new_Fx = -self.Fz
                new_Fz = self.Fx
            elif self.ref is Ref_Enum.XHL_YTD_ZCCW:
                new_Fy = self.Fx
                new_Fx = -self.Fy
            else:  # self.ref is Ref_Enum.YHL_XDT_ZCCW:
                pass
        self.ref = newRef
        self.Fx = new_Fx
        self.Fy = new_Fy
        self.Fz = new_Fz
        self.Mx = new_Mx
        self.My = new_My
        self.Mz = new_Mz
        return

    def isNull(self) -> bool:
        return all(
            [
                self.Fx == 0,
                self.Fy == 0,
                self.Fz == 0,
                self.Mx == 0,
                self.My == 0,
                self.Mz == 0,
            ]
        )

    def getFrequencyTr(self, lan="IT") -> str:
        if lan == "IT":
            if self.frequency == Frequency_Enum.CHARACTERISTIC:
                return "RAR"
            if self.frequency == Frequency_Enum.FREQUENT:
                return "FRE"
            if self.frequency == Frequency_Enum.QUASI_PERMANENT:
                return "QP"
            if self.frequency == Frequency_Enum.FREQUENCY_ND:
                return " "
        return ""

    def getLimitStateTr(self, lan="IT") -> str:
        if lan == "IT":
            if self.limitState == LimiteState_Enum.ULTIMATE:
                return "SLU"
            if self.limitState == LimiteState_Enum.SERVICEABILITY:
                return "SLE"
            if self.limitState == LimiteState_Enum.ACCIDENTAL:
                return "ACC"
            if self.limitState == LimiteState_Enum.LIMIT_STATE_ND:
                return ""
        return ""
