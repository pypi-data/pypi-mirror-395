import math
from typing import Literal, Tuple

from pycivil.EXAUtils.EXAExceptions import EXAExceptions as Ex


def rebarArea(d: float):
    return d * d * math.pi / 4


def rebarNumber(As: float, d: float) -> Tuple[float, float]:
    areaRebar = rebarArea(d)
    # nbRebar = math.ceil(As/areaRebar)
    nbRebar = As / areaRebar

    if As == 0.0:
        return 0.0, 0.0

    return nbRebar, nbRebar * areaRebar / As


def ratioRebarWeight(Vs: float, Vc: float):
    return Vs * 7850 / Vc


def fcm(fck: float) -> float:
    if fck < 0.0:
        raise Ex("0001", "args fck must be > 0", fck)
    _fcm = fck + 8
    return _fcm


def fctm(fck: float):
    if fck < 0.0:
        raise Ex("0002", "args fck must be > 0", fck)
    if fck <= 50:
        _fctm = 0.30 * math.pow(fck, 0.666)
    else:
        _fctm = 2.12 * math.log(1 + fcm(fck) / 10)
    return _fctm


def rcSectionBeamAreaMin(
    fck: float, fyk: float, d: float, crit: Literal["c1", "c2", "c12"] = "c12"
):
    if d < 0.0:
        raise Ex("0003", "args d must be > 0", d)

    Asmin1 = 0.26 * fctm(fck) / fyk * 1000 * d
    Asmin2 = 0.0013 * 1000 * d

    if crit == "c1":
        return Asmin1
    if crit == "c2":
        return Asmin2
    if crit == "c12":
        return max(Asmin1, Asmin2)


def rcSectionBeamShearAreaMin(fck: float, fyk: float, b: float):
    if fck <= 0.0:
        raise Ex("0004", "args b must be > 0", fck)
    if fyk <= 0.0:
        raise Ex("0005", "args b must be > 0", fyk)
    if b <= 0.0:
        raise Ex("0006", "args b must be > 0", b)

    Astmin = 0.08 * b * math.sqrt(fck) / fyk * 1000

    # mm2/m
    return Astmin


def rcSectionPlateShearAreaMin(fck: float, fyk: float):
    return rcSectionBeamShearAreaMin(fck, fyk, 1000)


def rcSectionBeamStirrupStepsMax(d: float, alpha: float = 90) -> float:
    if d <= 0.0:
        raise Ex("0007", "args d must be > 0", d)

    if not 23 <= alpha <= 90:
        raise Ex("0008", "args alpha must be => 23 and <= 90", alpha)

    smax = 0.75 * d * (1 + math.tan(math.radians(90 - alpha)))

    return smax


def rcSectionPlateStirrupStepsMax(d: float, alpha: float = 90) -> float:
    return rcSectionBeamStirrupStepsMax(d, alpha)


def rcSectionBeamShearLegsMax(d: float) -> float:
    """
    Max trasverse dinstance for legs

    Args:
        d:

    Returns:

    """
    if d <= 0.0:
        raise Ex("0009", "args d must be > 0", d)
    return 0.75 * d


def rcSectionPlateShearLegsMax(d: float) -> float:
    if d <= 0.0:
        raise Ex("0010", "args d must be > 0", d)
    return 1.50 * d


def rcSectionPlateStepMax(
    h: float,
    position: Literal["main", "secondary"] = "main",
    kind: Literal["normal", "maxbending"] = "normal",
) -> float:
    if h < 0.0:
        raise Ex("0008", "args h must be > 0", h)

    if position == "main" and kind == "normal":
        return min(3 * h, 400)
    if position == "main" and kind == "maxbending":
        return min(2 * h, 250)
    if position == "secondary" and kind == "normal":
        return min(3.5 * h, 450)
    if position == "secondary" and kind == "maxbending":
        return min(3 * h, 400)
