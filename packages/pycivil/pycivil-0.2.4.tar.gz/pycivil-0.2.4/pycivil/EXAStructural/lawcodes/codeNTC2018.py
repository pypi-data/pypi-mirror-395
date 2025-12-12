import math
from enum import Enum
from typing import Literal, Tuple, Union

import numpy as np

from pycivil.EXAUtils import EXAExceptions as ex
from pycivil.EXAUtils.logging import log
from pycivil.EXAUtils.tables import Table


def fcm(fck: float) -> float:
    """Resistenza media a compressione nel calcestruzzo secondo NTC2018 [11.2.10.1]

    Args:
        fck (float): Resistenza cilindrica caratteristica del calcestruzzo

    Raises:
        ex.EXAExceptions: args fck must be float
        ex.EXAExceptions: args fck must be > 0

    Returns:
        float: resistenza media a compressione
    """
    if type(fck) != float and type(fck) != int:
        raise ex.EXAExceptions("(fcm)-0001", "args fck must be float or int", type(fck))

    if fck < 0.0:
        raise ex.EXAExceptions("(fcm)-0002", "args fck must be > 0", fck)

    _fcm = fck + 8

    return _fcm


def fctm(fck: Union[float, int]):
    """Resistenza media a trazione nel calcestruzzo secondo NTC2018 [11.2.10.2]

    Restituisce il valore della resistenza media a trazione nel calcestruzzo
    secondo NTC2018.

    Unità in MPa

    Args:
        fck (float): Resistenza cilindrica caratteristica del calcestruzzo

    Returns:
        fctm (float): resistenza media a trazione
    """
    if type(fck) not in (float, int):
        raise ex.EXAExceptions(
            "(fctm)-0001", "args fck must be float or int", type(fck)
        )

    if fck < 0.0:
        raise ex.EXAExceptions("(fctm)-0002", "args fck must be > 0", fck)

    if fck <= 50:
        _fctm = 0.30 * math.pow(fck, 0.666)
    else:
        _fctm = 2.12 * math.log(1 + fcm(fck) / 10)

    return _fctm


def fcfk(fck: Union[float, int]) -> float:
    """Resistenza caratteristica a trazione per flessione NTC2018 [11.2.10.2]

    Args:
        fck (Union(float,int)): Resistenza cilindrica caratteristica del calcestruzzo

    Raises:
        ex.EXAExceptions: args fck must be float or int
        ex.EXAExceptions: args fck must be > 0

    Returns:
        float: fcfk
    """
    if type(fck) not in (float, int):
        raise ex.EXAExceptions("0001", "args fck must be float or int", type(fck))

    if fck < 0.0:
        raise ex.EXAExceptions("0002", "args fck must be > 0", fck)

    return 0.7 * 1.2 * fctm(fck)


def Ecm(fck):
    """Modulo elastico istantaneo del calcestruzzo secondo NTC2018 [11.2.10.3]

    Per modulo elastico istantaneo del calcestruzzo va assunto quello secante tra
    la tensione nulla e 0,40fcm, determinato sulla base di apposite prove, da
    eseguirsi secondo la norma UNI EN 12390-13:2013.

    Il valore dovrà essere ridotto del 20% in caso di utilizzo di aggregati grossi
    di riciclo nei limiti previsti dalla Tab. 11.2.III. Tale formula non è
    applicabile ai calcestruzzi maturati a vapore.

    Essa non è da considerarsi vincolante nell’interpretazione dei controlli speri-
    mentali delle strutture.

    Unità in MPa

    Args:
        fck (float): Resistenza cilindrica caratteristica del calcestruzzo

    Returns:
        Ecm (float): Modulo elastico istantaneo del calcestruzzo
    """
    if type(fck) != float and type(fck) != int:
        raise ex.EXAExceptions("0001", "args fck must be float or int", type(fck))

    if fck < 0.0:
        raise ex.EXAExceptions("0002", "args fck must be > 0", fck)

    return 22000 * math.pow(fcm(fck) / 10, 0.3)


def rcSectionBeamAreaMax(Ac):
    """Area massima armature tese o compresse nelle travi secondo NTC2018 [4.1.6.11]

    Restituisce il valore dell'area massima di acciaio per una trave secondo
    NTC2018 che può essere disposta individualmente in zona tesa o compressa.

    Il valore è valido al di fuori delle zone di sovrapposizione per le quali è
    tollerabile il superamento.

    Unità in mm^2

    Args:
        Ac (float): Area di calcestruzzo. Ac > 0
    Returns:
        Asmax (float): Armatura minima
    """
    if type(Ac) != float:
        raise ex.EXAExceptions("0001", "args Ac must be float", type(Ac))
    if Ac < 0.0:
        raise ex.EXAExceptions("0002", "args Ac must be > 0", Ac)

    Asmax = 0.04 * Ac

    return Asmax


def rcSectionBeamAreaMin(
    fck: float,
    fyk: float,
    bt: float,
    d: float,
    crit: Literal["c1", "c2", "c12"] = "c12",
):
    """Area minima in zona tesa di armatura nelle travi secondo NTC2018 [4.1.6.11]

    Restituisce il valore dell'area minima di acciaio per una trave secondo
    NTC2018 nella zona tesa.

    Unità in N, mm

    Args:
        crit (Literal["c1","c2","c12"]): Criterio di minimo.
            Nel caso di:
            1. "c1" verrà usato 0.26 * fctm/fyk * bt * d
            2. "c2" verrà usato 0.0013 * bt * d
            3. "c12" verrà usato il massimo tra i due criteri
        d (float): Altezza utile della sezione
        bt (float): rappresenta la larghezza media della zona tesa;
            per una trave a T con piattabanda compressa, nel calcolare il
            valore di b t si considera solo la larghezza dell'anima;
        fyk (float): Snervamento dell'acciaio
        fck (float): Resistenza cilindrica caratteristica del calcestruzzo

    Returns:
        Asmin (float): Armatura minima
    """
    if type(fck) is not float and type(fck) is not int:
        raise ex.EXAExceptions("0001", "args fck must be float or int", type(fck))
    if fck < 0.0:
        raise ex.EXAExceptions("0002", "args fck must be > 0", fck)
    if type(fyk) is not float and type(fyk) is not int:
        raise ex.EXAExceptions("0003", "args fyk must be float or int", type(fyk))
    if fyk < 0.0:
        raise ex.EXAExceptions("0004", "args fyk must be > 0", fyk)
    if type(bt) is not float and type(bt) is not int:
        raise ex.EXAExceptions("0005", "args bt must be float or int", type(bt))
    if bt < 0.0:
        raise ex.EXAExceptions("0006", "args bt must be > 0", bt)
    if type(d) is not float and type(d) is not int:
        raise ex.EXAExceptions("0007", "args d must be float or int", type(d))
    if d < 0.0:
        raise ex.EXAExceptions("0008", "args d must be > 0", d)

    Asmin1 = 0.26 * fctm(fck) / fyk * bt * d
    Asmin2 = 0.0013 * bt * d

    if crit == "c1":
        return Asmin1
    if crit == "c2":
        return Asmin2
    if crit == "c12":
        return max(Asmin1, Asmin2)


def rebarArea(d: float):
    return d * d * math.pi / 4


def rebarNumber(As: float, d: float) -> Tuple[float, float]:
    areaRebar = rebarArea(d)
    nbRebar = math.ceil(As / areaRebar)
    return nbRebar, nbRebar * areaRebar / As


def ratioRebarWeight(Vs: float, Vc: float):
    return Vs * 7850 / Vc


def rcSectionBeamShearAreaMin(b):
    """Area minima staffe al metro nelle travi secondo NTC2018 [4.1.6.11]

    Restituisce il valore dell'area minima delle staffe per una trave secondo
    NTC2018

    Unità in mm

    Args:
        b (float): Larghezza minima dell'anima della trave in mm. b > 0
    Returns:
        Astmin (float): Armatura minima trasversale in mm2 al metro
    """
    if type(b) is not float and type(b) is not int:
        raise ex.EXAExceptions("0001", "args b must be float or int", type(b))
    if b <= 0.0:
        raise ex.EXAExceptions("0002", "args b must be > 0", b)

    Astmin = 1.5 * b

    return Astmin


def rcSectionBeamShearStepMax(d, dlmin):
    """Passo massimo delle staffe in mm nelle travi secondo NTC2018 [4.1.6.11]

    Restituisce il valore passo massimo delle staffe in mm nelle travi secondo
    NTC2018

    Unità in mm

    Args:
        d (float): Altezza utile della trave. d > 0
        dlmin (float): Diametro minimo delle barre longitudinali compresse.
            dlmin > 0
    Returns:
        smax (float): Passo minimo in mm
    """
    if type(d) != float:
        raise ex.EXAExceptions("0001", "args d must be float", type(d))
    if d <= 0.0:
        raise ex.EXAExceptions("0002", "args d must be > 0", d)
    if type(dlmin) != float:
        raise ex.EXAExceptions("0001", "args dlmin must be float", type(dlmin))
    if dlmin <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmin must be > 0", dlmin)

    smax1 = 333.0
    smax2 = 0.8 * d
    # llp: vale solo per le compresse
    smax3 = 15 * dlmin

    smax = min(smax1, smax2, smax3)

    return smax


def rcSectionBeamShearStepsMax(d, dlmin):
    """Passo massimo delle staffe in mm nelle travi secondo NTC2018 [4.1.6.11]

    Restituisce il valore passo massimo delle staffe in mm nelle travi secondo
    NTC2018 come:
        1. minimo assoluto
        2. in rapporto all'altezza utile
        3. per le zone compresse

    Unità in mm

    Args:
        d (float): Altezza utile della trave. d > 0
        dlmin (float): Diametro minimo delle barre longitudinali compresse.
            dlmin > 0
    Returns:
        smax (float): Passo minimo in mm
    """
    if type(d) is not float and type(d) is not int:
        raise ex.EXAExceptions("0001", "args d must be float", type(d))
    if d <= 0.0:
        raise ex.EXAExceptions("0002", "args d must be > 0", d)
    if type(dlmin) is not float and type(dlmin) is not int:
        raise ex.EXAExceptions("0001", "args dlmin must be float", type(dlmin))
    if dlmin <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmin must be > 0", dlmin)

    smax1 = 333.0
    smax2 = 0.8 * d
    # llp: vale solo per le compresse
    smax3 = 15 * dlmin

    return smax1, smax2, smax3


def rcSectionColumnAreaMin(fyk, Ac, Ned=0.0, gammas=1.15):
    """Area minima delle armature longitudinali nei pilastri NTC2018 [4.1.6.1.2]

    Restituisce il valore dell'area minima di acciaio per un pilasto secondo
    NTC2018.

    Unità in N, mm

    Args:
        fyk (float): Resistenza caratteristica dell'accciaio a snervamento > 0 [Mpa]
        Ac (float): Area del calcestruzzo della sezione compressa > 0 [mm^2]
        Ned (float): Sforzo normale di progetto della sezione > 0 [mm^2]
        gammas (float): Resistenza cilindrica caratteristica del calcestruzzo

    Returns:
        Asmin (float): Armatura minima
    """
    if type(fyk) != float:
        raise ex.EXAExceptions("0003", "args fyk must be float", type(fyk))
    if fyk < 0.0:
        raise ex.EXAExceptions("0004", "args fyk must be > 0", fyk)
    if type(Ac) != float:
        raise ex.EXAExceptions("0005", "args Ac must be float", type(Ac))
    if Ac < 0.0:
        raise ex.EXAExceptions("0006", "args Ac must be > 0", Ac)
    if type(Ned) != float:
        raise ex.EXAExceptions("0007", "args Ned must be float", type(Ned))
    if Ned < 0.0:
        raise ex.EXAExceptions("0008", "args Ned must Ned > 0", Ned)
    if type(gammas) != float:
        raise ex.EXAExceptions("0007", "args gammas must be float", type(gammas))
    if gammas < 0.0:
        raise ex.EXAExceptions("0008", "args gammas must gammas > 0", gammas)

    Asmin1 = 0.10 * Ned / (fyk / gammas)
    Asmin2 = 0.003 * Ac

    return max(Asmin1, Asmin2)


def rcSectionColumnAreaMax(Ac):
    """Area massima armature compresse nei pilastri secondo NTC2018 [4.1.6.1.2]

    Restituisce il valore dell'area massima di acciaio per un pilastro secondo
    NTC2018 che può essere disposta individualmente in zona tesa o su tutta l'area compressa.

    Il valore è valido al di fuori delle zone di sovrapposizione per le quali è
    tollerabile il superamento.

    Unità in mm^2

    Args:
        Ac (float): Area di calcestruzzo. Ac > 0
    Returns:
        Asmax (float): Armatura minima
    """
    if type(Ac) != float:
        raise ex.EXAExceptions("0001", "args Ac must be float", type(Ac))
    if Ac < 0.0:
        raise ex.EXAExceptions("0002", "args Ac must be > 0", Ac)

    Asmax = 0.04 * Ac

    return Asmax


def rcSectionColumnShearStepMax(dlmin):
    """Passo massimo delle staffe in mm nelle travi secondo NTC2018 [4.1.6.1.2]

    Restituisce il valore passo massimo delle staffe in mm nei pilastri secondo
    NTC2018

    Unità in mm

    Args:
        dlmin (float): Diametro minimo delle barre longitudinali.
            dlmin > 0
    Returns:
        smax (float): Passo minimo in mm
    """
    if type(dlmin) != float:
        raise ex.EXAExceptions("0001", "args dlmin must be float", type(dlmin))
    if dlmin <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmin must be > 0", dlmin)

    smax1 = 250.0
    smax2 = 12.0 * dlmin

    smax = min(smax1, smax2)

    return smax


def rcSectionColumnShearDstMin(dlmax):
    """Diametro minimo staffe al metro nei pilastri secondo NTC2018 [4.1.6.1.2]

    Restituisce il valore dell'area minima delle staffe per una trave secondo
    NTC2018

    Unità in mm

    Args:
        dlmax (float): Diametro massimo armature longitudinali del pilastro. dlmax > 0
    Returns:
        dstmin (float): diametro minimo delle staffe
    """
    if type(dlmax) != float:
        raise ex.EXAExceptions("0001", "args dlmax must be float", type(dlmax))
    if dlmax <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmax must be > 0", dlmax)

    dmin1 = 6.0
    dmin2 = dlmax / 4.0
    dstmin = max(dmin1, dmin2)

    return dstmin


def rcSectionColumnShearAreaMin(dlmin, dlmax):
    """Area minima staffe al metro nei pilastri secondo NTC2018 [4.1.6.1.2]

    Restituisce il valore dell'area minima delle staffe per una trave secondo
    NTC2018

    Unità in mm

    Args:
        dlmin (float): Diametro minimo armature longitudinali del pilastro. dlmin > 0
        dlmax (float): Diametro massimo armature longitudinali del pilastro. dlmax > 0
    Returns:
        Astmin (float): Armatura minima trasversale al metro
    """
    if type(dlmin) != float:
        raise ex.EXAExceptions("0001", "args dlmin must be float", type(dlmin))
    if dlmin <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmin must be > 0", dlmin)
    if type(dlmax) != float:
        raise ex.EXAExceptions("0001", "args dlmax must be float", type(dlmax))
    if dlmax <= 0.0:
        raise ex.EXAExceptions("0002", "args dlmax must be > 0", dlmax)

    smax = rcSectionColumnShearStepMax(dlmin)
    dmin = rcSectionColumnShearDstMin(dlmax)

    Amin = 3.14 * dmin * dmin / 4.0
    Astmin = 2.0 * Amin / smax * 1000

    return Astmin


def shearCheckWithoutRebar(bw, d, fck, Asl, sigmacp=0.0, gammac=1.50, Ved=None, ll=1):
    """Verifica a taglio per elementi senza armatura specifica secondo NTC2018 [4.1.2.3.5.1]

    Se, sulla base del calcolo, non è richiesta armatura al taglio, è comunque
    necessario disporre un'armatura minima secondo quanto previsto al punto
    [4.1.6.1.1.] E' consentito omettere tale armatura minima in elementi quali
    solai, piastre e membrature a comportamento analogo, purché sia garantita
    una ripartizione trasversale dei carichi.

    Unità in N, mm

    Args:
        bw (float):
            Larghezza resistente a taglio > 0 [mm]. Minima della sezione.
        d (float):
            Altezza utile della sezione [mm].
        fck (float):
            Resistenza caratteristica cilindrica del cls > 0 [MPa]
        Asl (float):
            Armatura longitudinale in zona tesa il cui rapporto geometrico
            Asl/(bw*d )sarà <= 0.02
        sigmacp (:obj:`float`, optional):
            Tensione media di compressione della sezione [MPa] <= 0.2fcd.
            Se sigmacp < 0 lo sforzo è inteso di trazione. Default è 0.0
        gammac (:obj:`float`, optional):
            Coefficiente di sicurezza del calcestruzzo. Default è 1.50
        Ved (:obj:`float`, optional):
            Taglio sollecitante [N]. Default è None
        ll (:obj:`int`, optional):
            Log level. Default è 1

    Returns:
        res (dict): Risultato della verifica
            res['Vrd']   (float):
            res['check'] (float): Verifica se Vrd >= Vrd. 1 se vero 0 se falso
    """
    log("INF", "codeNTC2018-(shearCheckWithoutRebar) start ", ll)

    res = {"Vrd": 0, "check": None}

    if type(bw) != float and type(bw) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args bw must be float or int", type(bw)
        )
    if type(d) != float and type(d) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args d must be float or int", type(d)
        )
    if type(fck) != float and type(fck) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args fck must be float or int", type(fck)
        )
    if type(Asl) != float and type(Asl) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args Asl must be float or int", type(Asl)
        )
    if type(sigmacp) != float and type(sigmacp) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001",
            "args sigmacp must be float or int",
            type(sigmacp),
        )
    if type(gammac) != float and type(gammac) != int:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001",
            "args gammac must be float or int",
            type(gammac),
        )
    if Ved is not None:
        if type(Ved) != float and type(Ved) != int:
            raise ex.EXAExceptions(
                "(shearCheckWithoutRebar)-0001",
                "args Ved must be float or int",
                type(Ved),
            )

    if bw < 0.0:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args bw must be > 0", bw
        )
    if d < 0.0:
        raise ex.EXAExceptions("(shearCheckWithoutRebar)-0001", "args d must be > 0", d)
    if fck < 0.0:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args fck must be > 0", fck
        )
    if Asl < 0.0:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args Asl must be > 0", Asl
        )
    if gammac <= 0.0:
        raise ex.EXAExceptions(
            "(shearCheckWithoutRebar)-0001", "args gammac must be > 0", gammac
        )
    if Ved is not None:
        if Ved < 0.0:
            raise ex.EXAExceptions(
                "(shearCheckWithoutRebar)-0001", "args Ved must be > 0", Ved
            )

    if sigmacp < 0:
        log("INF", "rol > 0.02 taked 0.02")

    k = 1 + math.sqrt(200 / d)
    if k > 2:
        k = 2
        log("INF", "k > 2 taked 2", ll)

    nimin = 0.035 * math.pow(k, 1.5) * math.pow(fck, 0.5)

    rol = Asl / (bw * d)
    if rol > 0.02:
        rol = 0.02
        log("INF", "rol > 0.02 taked 0.02")

    alphacc = 0.85
    fcd = alphacc * fck / gammac
    if sigmacp > 0.2 * fcd:
        sigmacp = 0.2 * fcd
        log("INF", "sigmacp > 0.2 * fcd taked 0.2 * fcd")

    Vrd1 = (
        (0.018 * k * math.pow(100 * rol * fck, 0.333) / gammac + 0.15 * sigmacp)
        * bw
        * d
    )
    Vrd2 = (nimin + 0.15 * sigmacp) * bw * d
    res["Vrd"] = max(Vrd1, Vrd2)

    if Ved is not None:
        if Ved < res["Vrd"]:
            res["check"] = 1
        else:
            res["check"] = 0

    log("INF", "codeNTC2018-(shearCheckWithoutRebar) end ", ll)

    return res


def shearCheckWithRebar(
    bw,
    d,
    fck,
    fyk,
    Asw,
    s,
    alpha=90.0,
    theta=None,
    sigmacp=0.0,
    gammac=1.50,
    gammas=1.15,
    Ved=None,
    ll=1,
) -> dict:
    """Verifica a taglio per elementi con armatura a taglio NTC2018 [4.1.2.3.5.2]

    La resistenza di progetto a taglio Vrd di elementi strutturali dotati di
    specifica armatura a taglio deve essere valutata sulla base di una adeguata
    schematizzazione a traliccio.
    Gli elementi resistenti dell'ideale traliccio sono: le armature trasversali,
    le armature longitudinali, il corrente compresso di calcestruzzo e i puntoni
    d'anima inclinati.

    Unità in N, mm

    Args:
        bw (float):
            Larghezza resistente a taglio > 0 [mm]. Minima della sezione.
        d (float):
            Altezza utile della sezione [mm].
        fck (float):
            Resistenza caratteristica cilindrica del cls > 0 [MPa]
        fyk (float):
            Resistenza caratteristica a snervamento dell'acciaio > 0 [MPa]
        Asw (float):
            Armatura trasversale e taglio disposta ad interasse s [mm^2]
        s (float):
              Passo dell'armatura trasversale [mm]
        alpha (:obj:`float`, optional):
            Angolo delle staffe o ferri longitudinali rispetto all'asse
            della trave [deg]. Default è 90.
        theta (:obj:`float`, optional):
            Angolo dei puntoni di calcestruzzo rispetto all'asse della
            trave [deg]. Default è None.
            Se theta = None allora viene calcolato l'angolo percui la
            resistenza del puntone eguaglia quella dell'acciaio se esiste
            una rottura bilanciata.
            Deve risultare 1 <= theta <= 2.5 [4.1.25] altrimenti viene preso il valore
            più vicino.
        sigmacp (:obj:`float`, optional):
            Tensione media di compressione della sezione [MPa] < fcd.
            Se sigmacp < 0 lo sforzo è inteso di trazione. Default è 0.0
        gammac (:obj:`float`, optional):
            Coefficiente di sicurezza del calcestruzzo. Default è 1.50
        gammas (:obj:`float`, optional):
            Coefficiente di sicurezza dell'acciaio. Default è 1.15
        Ved (:obj:`float`, optional):
            Taglio sollecitante [N]. Default è None
        ll (:obj:`int`, optional):
            Log level. Default è 1

    Returns:
        res (dict): Risultato della verifica
            res['Vrd'] (float):
            res['check'] (float): Verifica se Vrd >= Vrd. 1 se vero 0 se falso
            res['Vrsd'] (float): Resistenza del traliccio in acciaio [N]
            res['Vrcd'] (float): Resistenza del puntone in calcestruzzo [N]
            res['cotgTheta'] (float): Angolo di inclinazione dei puntoni
            res['al'] (float): Misura di traslazione del momento
    """
    log("INF", "codeNTC2018-(shearCheckWithRebar) start ", ll)

    if type(bw) not in (float, int):
        log("ERR", "shearCheckWithRebar(): args bw must be float", ll)
        raise ex.EXAExceptions("0001", "args bw must be float", type(bw))
    if bw < 0.0:
        log("ERR", "shearCheckWithRebar(): args bw must be > 0", ll)
        raise ex.EXAExceptions("0002", "args bw must be > 0", bw)

    if type(d) not in (float, int):
        log("ERR", "shearCheckWithRebar(): args d must be float", ll)
        raise ex.EXAExceptions("0001", "args d must be float", type(d))
    if d < 0.0:
        log("ERR", f"shearCheckWithRebar(): args d={d} must be > 0", ll)
        raise ex.EXAExceptions("0002", "args d must be > 0", d)

    if type(fck) not in (float, int):
        log("ERR", "args fck must be float", ll)
        raise ex.EXAExceptions("0001", "args fck must be float", type(fck))
    if fck < 0.0:
        log("ERR", "args fck must be > 0", ll)
        raise ex.EXAExceptions("0002", "args fck must be > 0", fck)

    if type(fyk) not in (float, int):
        log("ERR", "args fyk must be float", ll)
        raise ex.EXAExceptions("0001", "args fyk must be float", type(fyk))
    if fyk < 0.0:
        log("ERR", "args fyk must be > 0", ll)
        raise ex.EXAExceptions("0002", "args fyk must be > 0", fyk)

    if type(Asw) not in (float, int):
        log("ERR", "0001 - args Asw must be float", ll)
        raise ex.EXAExceptions("0001", "args Asw must be float", type(Asw))
    if Asw < 0.0:
        log("ERR", "0002 - args Asw must be > 0", ll)
        raise ex.EXAExceptions("0002", "args Asw must be > 0", Asw)

    if type(s) not in (float, int):
        log("ERR", "0003 - args s must be float", ll)
        raise ex.EXAExceptions("0003", "args s must be float", type(s))
    if s < 0.0:
        log("ERR", "0004 - args s must be > 0", ll)
        raise ex.EXAExceptions("0004", "args s must be > 0", s)

    if type(alpha) not in (float, int):
        log("ERR", f"args alpha is a {str(type(alpha)):s} must be float", ll)
        raise ex.EXAExceptions("0001", "args alpha must be float", type(alpha))
    if alpha < 45 or alpha > 90:
        log("ERR", f"args alpha must be 45 <= alpha = {alpha:.3f} <= 90", ll)
        raise ex.EXAExceptions("0002", "args alpha must be 45 <= alpha <= 90", s)

    if type(sigmacp) not in (float, int):
        log("ERR", "args sigmacp must be float", ll)
        raise ex.EXAExceptions("0001", "args sigmacp must be float", type(sigmacp))

    if type(gammac) not in (float, int):
        log("ERR", "args gammac must be float", ll)
        raise ex.EXAExceptions("0001", "args gammac must be float", type(gammac))
    if gammac < 0.0:
        log("ERR", "args gammac must be > 0", ll)
        raise ex.EXAExceptions("0002", "args gammac must be > 0", gammac)

    if type(gammas) not in (float, int):
        log("ERR", "args gammas must be float", ll)
        raise ex.EXAExceptions("0001", "args gammas must be float", type(gammas))

    if gammas < 0.0:
        log("ERR", "args gammas must be > 0", ll)
        raise ex.EXAExceptions("0002", "args gammas must be > 0", gammas)

    if Ved is not None:
        if type(Ved) not in (float, int):
            log("ERR", f"args Ved must be float. Ved is {type(Ved)}", ll)
            raise ex.EXAExceptions("0001", "args Ved must be float", type(Ved))
        if Ved < 0.0:
            log("ERR", "args Ved must be > 0", ll)
            raise ex.EXAExceptions("0002", "args Ved must be > 0", Ved)

    res = {
        "check": None,
        "Vrd": 0,
        "Vrsd": 0,
        "Vrcd": 0,
        "alpha": alpha,
        "cotgTheta": 0,
        "sigmacp": sigmacp,
        "al": 0,
        "alphac": 0,
        "err": False,
    }

    path = {"tetha_calculated": False}

    if theta is None:
        path["tetha_calculated"] = True
        cotgTheta = 1.11
    else:
        path["tetha_calculated"] = False
        cotgTheta = 1 / math.tan(math.radians(theta))
        if (cotgTheta < 1.0) or (cotgTheta > 2.5):
            log(
                "WRN",
                "cotgTheta = {:.3f}. It can not be less than 1 or greater then 2.5".format(
                    cotgTheta
                ),
                ll,
            )
            res["err"] = True
            return res

    cotgAlpha = 1 / math.tan(math.radians(alpha))
    alphar = math.radians(alpha)

    fyd = fyk / gammas
    fcd = fck / gammac

    res["path"] = path

    res["fyd"] = fyd
    res["fcd"] = fcd

    if sigmacp < 0:
        alphac = 1
    else:
        if (0 <= sigmacp) and (sigmacp < 0.25 * fcd):
            alphac = 1 + sigmacp / fcd
        elif (0.25 * fcd <= sigmacp) and (sigmacp <= 0.50 * fcd):
            alphac = 1.25
        elif (0.50 * fcd <= sigmacp) and (sigmacp < fcd):
            alphac = 2.5 * (1 - sigmacp / fcd)
        else:
            log(
                "WRN",
                "alphac can not be calulated cause sigmacp = {:.3f} > fcd = {:.3f}".format(
                    sigmacp, fcd
                ),
                ll,
            )
            res["err"] = True
            return res

    res["alphac"] = alphac

    log("INF", f"alphac = {alphac:.3f}", ll)

    # NTC2008 [4.1.2.3.5.2] ni si pone 0.5
    ni = 0.5

    def Vrsd_cotgTheta(x):
        return 0.9 * d * Asw / s * fyd * (cotgAlpha + x) * math.sin(math.radians(alpha))

    def Vrcd_cotgTheta(x):
        return 0.9 * d * bw * alphac * ni * fcd * (cotgAlpha + x) / (1 + math.pow(x, 2))

    res["bw"] = bw
    res["Asw"] = Asw
    res["s"] = s
    res["d"] = d

    if path["tetha_calculated"]:
        A = math.sin(alphar) * (Asw / s) * fyd
        B = bw * alphac * ni * fcd

        AA = A
        BB = A * cotgAlpha
        CC = A - B
        DD = (A - B) * cotgAlpha

        def T(x):
            return AA * pow(x, 3) + BB * pow(x, 2) + CC * pow(x, 1) + DD

        # First derivative of T(x)
        def D1_T(x):
            return 3 * AA * pow(x, 2) + 2 * BB * x + CC

        # D1_T(x) is ever monotone in [1.0,2.5] because vertex in x = -BB/(3*AA) is negative
        # than we are in growing branch of parabola
        if D1_T(1.0) * D1_T(2.5) > 0:
            log("INF", "Function T(x) is monotone ...", ll)
            if T(1.0) * T(2.5) < 0:
                log("INF", "Function T(x) has unique real solution ...", ll)
                path["method"] = "1. NUMPY with unique solution and T(x) monotone"

                # solving AA*x^3 + BB*x^2 + CC*x +DD
                roots = np.roots([AA, BB, CC, DD])
                log(
                    "INF",
                    "roots are x1 = {:.3f} x1 = {:.3f} x1 = {:.3f}".format(
                        roots[0], roots[1], roots[2]
                    ),
                    ll,
                )
                sol = []
                for r in roots:
                    if (1 <= r) and (r <= 2.5) and np.isreal(r):
                        sol.append(r)

                if len(sol) == 1:
                    cotgTheta = np.real(sol[0])
                    Vrd = Vrsd_cotgTheta(cotgTheta)
                    Vrsd = Vrsd_cotgTheta(cotgTheta)
                    Vrcd = Vrcd_cotgTheta(cotgTheta)
                else:
                    raise ex.EXAExceptions("0001", "Solution is not unique !!!", roots)

            else:
                log(
                    "INF",
                    "Function T(x) has not unique real solution but max and min value",
                    ll,
                )
                path[
                    "method"
                ] = "2. DISCRETE solution from 1.0 and 2.5 and T(x) monotone"
                cotgThetaLst = [1.0, 2.5]
                Vrd1 = min(Vrsd_cotgTheta(1.0), Vrcd_cotgTheta(1.0))
                Vrd2 = min(Vrsd_cotgTheta(2.5), Vrcd_cotgTheta(2.5))
                VrdLst = [Vrd1, Vrd2]
                Vrd = max(VrdLst)
                cotgTheta = cotgThetaLst[VrdLst.index(Vrd)]
                Vrsd = Vrsd_cotgTheta(cotgTheta)
                Vrcd = Vrcd_cotgTheta(cotgTheta)
        else:
            log("INF", "Function T(x) is not monotone ...", ll)
            log("INF", "... than we have max inside interval [1.0,2.5] ...", ll)
            path[
                "method"
            ] = "3. DISCRETE solution from 1.0 and 2.5 and T(x) not monotone"
            deltaOf_D1_T = 4 * pow(BB, 2) - 12 * AA * CC
            x1 = (-2 * BB - math.sqrt(deltaOf_D1_T)) / (2 * 3 * AA)
            x2 = (-2 * BB + math.sqrt(deltaOf_D1_T)) / (2 * 3 * AA)
            log(
                "INF",
                "Function D1_T(x) has zero in x1 = {:.3f} and x2 = {:.3f}".format(
                    x1, x2
                ),
                ll,
            )

            # Cause x1 is negative than x1 is outside [1.0,2.5] i use only x2
            if (1.0 <= x2) and (x2 <= 2.5):
                log("INF", f"x2 = {x2:.3f} inside [1.0,2.5] ...", ll)
            else:
                log("INF", f"x2 = {x2:.3f} outside [1.0,2.5] ...", ll)
                x2 = 1.0

            cotgThetaLst = [1.0, x2, 2.5]
            Vrd1 = min(Vrsd_cotgTheta(1.0), Vrcd_cotgTheta(1.0))
            Vrdx2 = min(Vrsd_cotgTheta(x2), Vrcd_cotgTheta(x2))
            Vrd2 = min(Vrsd_cotgTheta(2.5), Vrcd_cotgTheta(2.5))
            log(
                "INF",
                "... Vrd1 = {:.3f} Vrdx2 = {:.3f} Vrd2 = {:.3f}".format(
                    Vrd1, Vrdx2, Vrd2
                ),
                ll,
            )
            VrdLst = [Vrd1, Vrdx2, Vrd2]
            Vrd = max(VrdLst)
            cotgTheta = cotgThetaLst[VrdLst.index(Vrd)]
            Vrsd = Vrsd_cotgTheta(cotgTheta)
            Vrcd = Vrcd_cotgTheta(cotgTheta)

    else:
        Vrsd = Vrsd_cotgTheta(cotgTheta)
        Vrcd = Vrcd_cotgTheta(cotgTheta)
        Vrd = min(Vrsd, Vrcd)

    res["cotgTheta"] = cotgTheta
    res["Vrd"] = Vrd
    res["Vrsd"] = Vrsd
    res["Vrcd"] = Vrcd

    res["Ved"] = Ved
    if Ved is not None:
        if Ved < res["Vrd"]:
            res["check"] = 1
        else:
            res["check"] = 0

    # al is moment translation diagram (NTC 2018 4.1.30)
    res["al"] = 0.9 * d * res["cotgTheta"] / 2

    log("INF", "codeNTC2018-(shearCheckWithRebar) end ", ll)

    return res


class CrackOut:
    def __init__(self):
        self.__wk: float = 0.0
        self.__epsism: Union[None, float] = None
        self.__sigmas_stiffning: Union[None, float] = None
        self.__deltasm: Union[None, float] = None
        self.__deltasm1: Union[None, float] = None
        self.__deltasm2: Union[None, float] = None
        self.__roeff: Union[None, float] = None
        self.__zoneC: Union[None, float] = None
        self.__k2: Union[None, float] = None
        self.__alpham: Union[None, float] = None
        self.__epsi1: Union[None, float] = None
        self.__epsi2: Union[None, float] = None

    @property
    def epsi1(self):
        return self.__epsi1

    @epsi1.setter
    def epsi1(self, value):
        self.__epsi1 = value

    @property
    def epsi2(self):
        return self.__epsi2

    @epsi2.setter
    def epsi2(self, value):
        self.__epsi2 = value

    @property
    def alpham(self):
        return self.__alpham

    @alpham.setter
    def alpham(self, value):
        self.__alpham = value

    @property
    def k2(self):
        return self.__k2

    @k2.setter
    def k2(self, value):
        self.__k2 = value

    @property
    def zoneC(self):
        return self.__zoneC

    @zoneC.setter
    def zoneC(self, value):
        self.__zoneC = value

    @property
    def epsism(self):
        return self.__epsism

    @epsism.setter
    def epsism(self, value):
        self.__epsism = value

    @property
    def sigmas_stiffning(self):
        return self.__sigmas_stiffning

    @sigmas_stiffning.setter
    def sigmas_stiffning(self, value):
        self.__sigmas_stiffning = value

    @property
    def deltasm1(self):
        return self.__deltasm1

    @deltasm1.setter
    def deltasm1(self, value):
        self.__deltasm1 = value

    @property
    def deltasm(self):
        return self.__deltasm

    @deltasm.setter
    def deltasm(self, value):
        self.__deltasm = value

    @property
    def wk(self):
        return self.__wk

    @wk.setter
    def wk(self, value):
        self.__wk = value

    @property
    def deltasm2(self):
        return self.__deltasm2

    @deltasm2.setter
    def deltasm2(self, value):
        self.__deltasm2 = value

    @property
    def roeff(self):
        return self.__roeff

    @roeff.setter
    def roeff(self, value):
        self.__roeff = value

    def __str__(self):
        dispstr = f"__wk                = {self.__wk}\n"
        dispstr += f"__epsism            = {self.__epsism}\n"
        dispstr += f"__sigmas_stiffning  = {self.__sigmas_stiffning}\n"
        dispstr += f"__deltasm           = {self.__deltasm}\n"
        dispstr += f"__deltasm1          = {self.__deltasm1}\n"
        dispstr += f"__deltasm2          = {self.__deltasm2}\n"
        dispstr += f"__roeff             = {self.__roeff}\n"
        dispstr += f"__zoneC             = {self.__zoneC}\n"
        dispstr += f"__k2                = {self.__k2}\n"
        dispstr += f"__alpham            = {self.__alpham}\n"
        dispstr += f"__epsi1             = {self.__epsi1}\n"
        dispstr += f"__epsi2             = {self.__epsi2}\n"
        return dispstr

    def toDict(self) -> dict:
        return {
            "wk": self.__wk,
            "epsism": self.__epsism,
            "sigmas_stiffning": self.__sigmas_stiffning,
            "deltasm": self.__deltasm,
            "deltasm1": self.__deltasm1,
            "deltasm2": self.__deltasm2,
            "roeff": self.__roeff,
            "zoneC": self.__zoneC,
            "k2": self.__k2,
            "alpham": self.__alpham,
            "epsi1": self.__epsi1,
            "epsi2": self.__epsi2,
        }


def crackMeasure(
    epsiBot: float,
    epsiTop: float,
    deq: float,
    As: float,
    rebarsCover: float,
    rebarsDistance: float,
    hcEff: float,
    beff: float,
    hsec: float,
    xi: float,
    fck: float,
    sigmas: float,
    Es: float,
    load: str = "short",
) -> CrackOut:
    """Calcolo diretto ampiezza delle fessure secondo NTC2018 [C4.1.2.2.4.5]

    Unità in N, mm

    Args:
        deq (float): Diametro equivalente delle barre di armatura. Se ad esempio
            nella area efficace sono presenti due diametri d1 e d2 con rispetti
            vamente n1 ed n2 il numero di barre il valore proposto è:

                                    n1 * d1^2 + n2 * d2^2
                            deq = ---------------------
                                    n1 * d1 + n2 * d2

        As (float): Area totale dell'acciaio teso [mm^2]
        rebarsCover (float): Copriferro [mm]
        rebarsDistance (float): Interferro massimo [mm]
        hcEff (float): Altezza efficace [mm]
        beff (float): Larghezza efficace dell'area del tirante convenzionale [mm].
            Il valore è tale che moltiplicato per l'altezza heff fornisce l'area
            efficace del tirante convenzionale.
        hsec (float): Altezza della sezione [mm]
        xi (float): Profondità dell'asse neutro della sezione [mm]. Se x è positivo
            allora la sezione è parzializzata fino a quando x <= hsec. Se negativo
            la sezione è tutta tesa.
        fck (float): Resistenza cilindrica caratteristica a compressione del
            calcestruzzo in [MPa]
        sigmas (float): Tensione di trazione nell'acciaio [MPa]
        Es (float): Modulo di young dell'acciaio [MPa]
        epsiBot (float): Allungamento massimo sezione per sezione tutta tesa
        epsiTop (float): Allungamento minimo sezione per sezione tutta tesa
        load (str, optional): Durata del carico. 'short' o 'long'. Defaults to 'short'.

    Raises:
        ex.EXAExceptions: _description_

    Returns:
        dict: Risultato della misura epsism
            res['wk'] (float): Ampiezza caratteristica delle fessure [mm]
            res['epsism'] (float): Deformazione acciaio tra le fessure
            res['deltasm'] (float): Distanza media tra le fessure [mm]
            res['heff'] (float): Resistenza del puntone in calcestruzzo [N]
            res['roeff'] (float): Rapporto geometrico d'armatura efficace
            res['zoneC'] (float): Lunghezza per la quale è valida deltasm
    """
    res = CrackOut()

    if (epsiBot <= 0) and (epsiTop <= 0):
        res.wk = 0
        return res

    epsi1 = max(epsiBot, epsiTop)
    epsi2 = min(epsiBot, epsiTop) if min(epsiBot, epsiTop) > 0.0 else 0.0

    if load == "short":
        kt = 0.6
    elif load == "long":
        kt = 0.4
    else:
        raise ex.EXAExceptions(
            "0001", 'load parameter must be "short" or "long" !!!', load
        )

    Aceff = beff * hcEff
    roeff = As / Aceff
    alpham = Es / Ecm(fck)

    sigmas_stiffning = kt * fctm(fck) / roeff * (1 + alpham * roeff)
    if sigmas_stiffning >= 0.4 * sigmas:
        sigmas_stiffning = 0.4 * sigmas

    epsism = (sigmas - sigmas_stiffning) / Es

    # Medium distance between crack
    k1 = 0.8
    k2 = (epsi1 + epsi2) / (2 * epsi1)
    k3 = 3.4
    k4 = 0.425

    deltasm1 = (k3 * rebarsCover + k1 * k2 * k4 * deq / roeff) * (1 / 1.7)

    if epsiTop > epsiBot:
        deltasm2 = 0.75 * xi
    else:
        deltasm2 = 0.75 * (hsec - xi)

    zoneC = 5 * (rebarsCover + deq / 2)
    if rebarsDistance >= zoneC:
        deltasm = deltasm2
    else:
        deltasm = deltasm1

    wk = 1.7 * epsism * deltasm

    res.wk = wk
    res.epsism = epsism
    res.sigmas_stiffning = sigmas_stiffning
    res.deltasm = deltasm
    res.deltasm1 = deltasm1
    res.deltasm2 = deltasm2
    res.roeff = roeff
    res.zoneC = zoneC
    res.k2 = k2
    res.alpham = alpham
    res.epsi1 = epsi1
    res.epsi2 = epsi2
    return res


class WindActionZonesEnum(int, Enum):
    ZONE_1 = 1
    ZONE_2 = 2
    ZONE_3 = 3
    ZONE_4 = 4
    ZONE_5 = 5
    ZONE_6 = 6
    ZONE_7 = 7
    ZONE_8 = 8
    ZONE_9 = 9


class WindActionsZones(Table):
    descr_1 = (
        "Valle d'Aosta, Piemonte, Lombardia,"
        "Trentino Alto Adige, Veneto, "
        "Friuli Venezia Giulia "
        "(con l'eccezione della provincia di Trieste)"
    )
    descr_2 = "Emilia Romagna"
    descr_3 = (
        "Toscana, Marche, Umbria, Lazio, Abruzzo, "
        "Molise, Puglia, Campania, Basilicata, Calabria "
        "(esclusa la provincia di Reggio calabria)"
    )
    descr_4 = "Sicilia e provincia di Reggio Calabria"
    descr_5 = (
        "Sardegna (zona a oriente della retta congiungente"
        "Capo Teulada con l'Isola di Maddalena)"
    )
    descr_6 = (
        "Sardegna (zona a occidente della retta congiungente"
        "Capo Teulada con l'Isola di Maddalena)"
    )
    descr_7 = "Liguria"
    descr_8 = "Provincia di Trieste"
    descr_9 = "Isole (con l'eccezione di Sicilia e Sardegna) " "e mare aperto"
    tab01 = {
        "source": "Testo della Norma",
        "columns": ("id", "Zona", "Descrizione", "v_{b,0}", "a_{0}", "k_{a}"),
        "udm": ("", "", "", "m/s", "m", ""),
        "rows": (
            (1, "Zona 1", descr_1, 25, 1000, 0.40),
            (2, "Zona 2", descr_2, 25, 750, 0.45),
            (3, "Zona 3", descr_3, 27, 500, 0.37),
            (4, "Zona 4", descr_4, 28, 500, 0.36),
            (5, "Zona 5", descr_5, 28, 750, 0.40),
            (6, "Zona 6", descr_6, 28, 500, 0.36),
            (7, "Zona 7", descr_7, 28, 1000, 0.54),
            (8, "Zona 8", descr_8, 30, 1500, 0.50),
            (9, "Zona 9", descr_9, 31, 500, 0.32),
        ),
    }

    def __init__(self):
        Table.__init__(self, WindActionsZones.tab01)


class WindActionRoughtnessEnum(int, Enum):
    CLASS_A = 1
    CLASS_B = 2
    CLASS_C = 3
    CLASS_D = 4


class WindActionRoughtness(Table):
    descr_1 = (
        "Area urbana, in cui almeno il 15% della superficie "
        "del terreno sia coperto da edifici la cui altezza"
        "media supera i 15 m"
    )
    descr_2 = "Area urbana (non di classe A), suburbana, industriale o boschiva"
    descr_3 = (
        "Area con ostacoli diffusi (quali alberi, case, muri, recinzioni, ...); "
        "aree con rugosità non riconducibile alle Classi A, B, D."
    )
    descr_4 = (
        "a) Mare e relativa fascia costiera (entro 2 km dalla riva)"
        "b) Lago (con larghezza pari ad almeno 1 km) e relativa fascia costiera "
        "(entro 1 km dalla riva)"
        "c) Area priva di ostacoli o con al più rari ostacoli isolati (aperta "
        "campagna, aeroporti, aree agricole, pascoli, zone paludose o sabbiose, "
        "superfici innevate o ghiacciate, ...)"
    )
    tab01 = {
        "source": "Testo della Norma",
        "columns": ("id", "Classe di rugosità", "Descrizione"),
        "udm": ("", "", ""),
        "rows": (
            (1, "A", descr_1),
            (2, "B", descr_2),
            (3, "C", descr_3),
            (4, "D", descr_4),
        ),
    }

    def __init__(self):
        Table.__init__(self, WindActionRoughtness.tab01)


class WindActionSiteCategoriesEnum(int, Enum):
    CAT_I = 1
    CAT_II = 2
    CAT_III = 3
    CAT_IV = 4
    CAT_V = 5
    CAT_ND = 0


class WindActionSiteCategories(Table):
    tab01 = {
        "source": "Testo della Norma",
        "columns": ("id", "Categoria di esposizione", "k_r", "z_0", "z_min"),
        "udm": ("", "", "m", "m"),
        "rows": (
            (1, "I", 0.17, 0.01, 2),
            (2, "II", 0.19, 0.05, 4),
            (3, "III", 0.20, 0.10, 5),
            (4, "IV", 0.22, 0.30, 8),
            (5, "V", 0.23, 0.70, 12),
        ),
    }

    def __init__(self):
        Table.__init__(self, WindActionSiteCategories.tab01)


def windActionSiteCategorie(
    geoArea: WindActionZonesEnum,
    roughtness: WindActionRoughtnessEnum,
    aslm: float,
    seaDist: float,
) -> WindActionSiteCategoriesEnum:
    """Restituisce la categoria di sito [NTC2018 par. 3.3.1.]

    Args:
        geoArea (WindActionZonesEnum): zona geografica [NTC2018 par. 3.3.1.]
        roughtness (WindActionRoughtnessEnum): rugosità secondo [NTC2018 par. Tab.3.3.III]
        aslm (float): altezza sul livello del mare in m. Solo valori >= 0.
        seaDist (float): distanza dalla costa. Valori negativi
            significa in mare. Positivi nell'entroterra

    Returns:
        WindActionSiteCategoriesEnum: categoria del sito [NTC2018 fig. 3.3.2]
    """
    if aslm < 0:
        raise ex.EXAExceptions("ERR", "aslm must be > 0", aslm)

    c1 = any(
        [
            geoArea == WindActionZonesEnum.ZONE_1,
            geoArea == WindActionZonesEnum.ZONE_2,
            geoArea == WindActionZonesEnum.ZONE_3,
            geoArea == WindActionZonesEnum.ZONE_4,
            geoArea == WindActionZonesEnum.ZONE_5,
        ]
    )

    c2 = geoArea == WindActionZonesEnum.ZONE_6

    c3 = any(
        [geoArea == WindActionZonesEnum.ZONE_7, geoArea == WindActionZonesEnum.ZONE_8]
    )

    c4 = geoArea == WindActionZonesEnum.ZONE_9

    if c1:
        if seaDist <= 0:
            if roughtness != WindActionRoughtnessEnum.CLASS_D:
                raise ex.EXAExceptions(
                    "ERR",
                    "roughtness must be only D with 0 >= seaDist >= -2000",
                    seaDist,
                )

            if seaDist >= -2000:
                return WindActionSiteCategoriesEnum.CAT_I
            else:
                raise ex.EXAExceptions(
                    "ERR", "seaDist value must be >= -2000 m", seaDist
                )
        elif 0 < seaDist and seaDist <= 40000:
            if seaDist <= 10000:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_III
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    if geoArea == WindActionZonesEnum.ZONE_5:
                        return WindActionSiteCategoriesEnum.CAT_III
                    else:
                        return WindActionSiteCategoriesEnum.CAT_II
                else:
                    return WindActionSiteCategoriesEnum.CAT_II

            else:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_III
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_III
                else:
                    return WindActionSiteCategoriesEnum.CAT_II
        else:
            if aslm < 500:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_V
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_III
                else:
                    return WindActionSiteCategoriesEnum.CAT_II
            elif aslm < 750:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_V
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_IV
                else:
                    return WindActionSiteCategoriesEnum.CAT_III
            else:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    if geoArea == WindActionZonesEnum.ZONE_1:
                        return WindActionSiteCategoriesEnum.CAT_IV
                    else:
                        return WindActionSiteCategoriesEnum.CAT_III

    elif c2:
        if seaDist <= 0:
            if roughtness != WindActionRoughtnessEnum.CLASS_D:
                raise ex.EXAExceptions(
                    "ERR",
                    "roughtness must be only D with 0 >= seaDist >= -2000",
                    seaDist,
                )

            if seaDist >= -2000:
                return WindActionSiteCategoriesEnum.CAT_I
            else:
                raise ex.EXAExceptions(
                    "ERR", "seaDist value must be >= -2000 m", seaDist
                )

        elif 0 < seaDist and seaDist <= 40000:
            if seaDist <= 10000:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_III
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_II
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_II
                else:
                    return WindActionSiteCategoriesEnum.CAT_I
            else:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_III
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_III
                else:
                    return WindActionSiteCategoriesEnum.CAT_II
        else:
            if aslm < 500:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_V
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_III
                else:
                    return WindActionSiteCategoriesEnum.CAT_II
            else:
                if roughtness == WindActionRoughtnessEnum.CLASS_A:
                    return WindActionSiteCategoriesEnum.CAT_V
                elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                    return WindActionSiteCategoriesEnum.CAT_IV
                elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                    return WindActionSiteCategoriesEnum.CAT_IV
                else:
                    return WindActionSiteCategoriesEnum.CAT_III

    elif c3:

        if seaDist <= 0:
            if roughtness != WindActionRoughtnessEnum.CLASS_D:
                raise ex.EXAExceptions(
                    "ERR",
                    "roughtness must be only D with 0 >= seaDist >= -2000",
                    seaDist,
                )

            if seaDist > -500:
                return WindActionSiteCategoriesEnum.CAT_I
            elif seaDist >= -2000:
                return WindActionSiteCategoriesEnum.CAT_II
            else:
                raise ex.EXAExceptions(
                    "ERR", "seaDist value must be >= -2000 m", seaDist
                )
        else:
            if roughtness == WindActionRoughtnessEnum.CLASS_A:
                return WindActionSiteCategoriesEnum.CAT_IV
            elif roughtness == WindActionRoughtnessEnum.CLASS_B:
                return WindActionSiteCategoriesEnum.CAT_IV
            elif roughtness == WindActionRoughtnessEnum.CLASS_C:
                return WindActionSiteCategoriesEnum.CAT_III
            else:
                if geoArea == WindActionZonesEnum.ZONE_8:
                    return WindActionSiteCategoriesEnum.CAT_II
                else:
                    return WindActionSiteCategoriesEnum.CAT_III

    elif c4:
        if seaDist <= 0:
            if roughtness != WindActionRoughtnessEnum.CLASS_D:
                raise ex.EXAExceptions(
                    "ERR",
                    "roughtness must be only D with 0 >= seaDist >= -2000",
                    seaDist,
                )
            else:
                return WindActionSiteCategoriesEnum.CAT_I
        else:
            return WindActionSiteCategoriesEnum.CAT_I

    else:
        raise ex.EXAExceptions("ERR", "area unknown !!!")

    return WindActionSiteCategoriesEnum.CAT_ND


class WindActionsExpositionParam(Table):
    tab01 = {
        "source": "Testo della Norma",
        "columns": ("id", "Categoria di esposizione", "K_r", "z_0", "z_{min}"),
        "udm": ("", "", "", "m", "m"),
        "rows": (
            (1, "I", 0.17, 0.01, 2),
            (2, "II", 0.19, 0.05, 4),
            (3, "III", 0.20, 0.10, 5),
            (4, "IV", 0.22, 0.30, 8),
            (5, "V", 0.23, 0.70, 12),
        ),
    }

    def __init__(self):
        Table.__init__(self, WindActionsExpositionParam.tab01)


def windActionsExposition(
    siteCategory: WindActionSiteCategoriesEnum, z: float
) -> float:
    """Restituisce il coefficienti di esposizione [NTC20018 3.3.7.]

    Il valore del coefficiente di topografia è assunto unitario.

    Args:
        siteCategory (WindActionSiteCategoriesEnum): categoria di esposizione del sito
        z (float): altezza della costruzione dal suolo. z > 0 && z < 200

    Raises:
        ex.EXAExceptions: z must be > 0
        ex.EXAExceptions: z must be < 200

    Returns:
        float: coefficiente di esposizione
    """
    if z < 0:
        raise ex.EXAExceptions("ERR", "z must be > 0", z)

    if z > 200:
        raise ex.EXAExceptions("ERR", "z must be < 200", z)

    def ce(Kr: float, z0: float, zmin: float, z: float) -> float:
        ct = 1.0

        if z < zmin:
            z = zmin

        return Kr * Kr * ct * np.log(z / z0) * (7 + ct * np.log(z / z0))

    param = WindActionsExpositionParam()
    Kr = param.valueAt(siteCategory.value)[2]
    z0 = param.valueAt(siteCategory.value)[3]
    zmin = param.valueAt(siteCategory.value)[4]

    return ce(Kr, z0, zmin, z)


def windActionsPressure(
    zone: WindActionZonesEnum,
    roughtness: WindActionRoughtnessEnum,
    aslm: float,
    seaDist: float,
    zRef: float,
    Tr: float = 50,
) -> dict:
    """Calcola la pressione cinetica di picco e tutte le grandezze correlate

    Args:
        zone (WindActionZonesEnum): _description_
        roughtness (WindActionRoughtnessEnum): _description_
        aslm (float): _description_
        seaDist (float): _description_
        zRef (float): è l'altezza di riferimento in metri del filetto fluido
            considerato.
        Tr (float, optional): _description_. Defaults to 50.

    Returns:
        dict: _description_
    """
    res = {}

    zoneTable = WindActionsZones()
    zone_label = zoneTable.valueAt(zone)[1]
    zone_descr = zoneTable.valueAt(zone)[2]
    zone_vb0 = zoneTable.valueAt(zone)[3]
    zone_a0 = zoneTable.valueAt(zone)[4]
    zone_ka = zoneTable.valueAt(zone)[5]

    rougthnessTable = WindActionRoughtness()
    rougthness_label = rougthnessTable.valueAt(roughtness)[1]
    rougthness_descr = rougthnessTable.valueAt(roughtness)[2]

    res["input"] = {
        "zone_label": zone_label,
        "zone_descr": zone_descr,
        "zone_vb0": zone_vb0,
        "zone_a0": zone_a0,
        "zone_ka": zone_ka,
        "rougthness_label": rougthness_label,
        "rougthness_descr": rougthness_descr,
        "aslm": aslm,
        "seaDist": seaDist,
        "zRef": zRef,
        "Tr": Tr,
    }

    # (1) calcolo velocità base di riferimento
    zoneParam = WindActionsZones()
    zoneLabel = zoneParam.valueAt(zone.value)[1]
    zoneDescr = zoneParam.valueAt(zone.value)[2]
    vb0 = zoneParam.valueAt(zone.value)[3]
    a0 = zoneParam.valueAt(zone.value)[4]
    ka = zoneParam.valueAt(zone.value)[5]

    # (1.1) coefficiente di altitudine
    if aslm <= a0:
        ca = 1
    else:
        ca = 1 + ka * (aslm / a0 - 1)

    # (1.2) velocità di riferimento
    vb = vb0 * ca

    # (2) calcolo velocità di riferimento di progetto

    # (2.1) coefficiente del tempo di ritorno
    cr = 0.75 * np.sqrt(1 - 0.2 * np.log(-np.log(1 - 1 / Tr)))

    # (2.2) velocità di riferimento
    vr = vb * cr

    # (3) pressione cinetica di picco

    # (3.1) calcolo coefficiente di esposizione
    siteCategorie = windActionSiteCategorie(zone, roughtness, aslm, seaDist)
    ce = windActionsExposition(siteCategorie, zRef)

    # (3.2) densità dell'aria in kg/mc
    rho = 1.25

    # (3.3) pressione di riferimento
    qr = 0.5 * vr * vr * rho / 1000

    # (3.3) pressione cinetica di picco
    #
    # La pressione cinetica di picco del vento q p è il valore atteso della
    # pressione cinetica massima del vento sull’intervallo di tempo T = 10
    # minuti. Essa dipende dall’altezza z sul suolo, dalla ventosità della
    # zona in esame (paragrafo 3.2.1), dal periodo di ritorno di progetto
    # (paragrafo 3.2.2), dalle caratteristiche locali del sito ove sorge
    # la costruzione e dalla densità dell’aria.
    #
    # Dalla formula le udm sono N/mq ma noi trasformiamo in KN/mq
    qp = qr * ce

    siteCat = WindActionSiteCategories()
    siteCatLabel = siteCat.valueAt(siteCategorie.value)[1]
    k_r = siteCat.valueAt(siteCategorie.value)[2]
    z_0 = siteCat.valueAt(siteCategorie.value)[3]
    z_min = siteCat.valueAt(siteCategorie.value)[4]

    res["output"] = {
        "zone_label": zoneLabel,
        "zone_descr": zoneDescr,
        "zone_vb0": vb0,
        "zone_a0": a0,
        "zone_ka": ka,
        "ca": ca,
        "vb": vb,
        "cr": cr,
        "vr": vr,
        "siteCat_label": siteCatLabel,
        "siteCat_k_r": k_r,
        "siteCat_z_0": z_0,
        "siteCat_z_min": z_min,
        "ce": ce,
        "qr": qr,
        "rho": rho,
        "qp": qp,
    }

    return res


def windActionsForcesOnRect(d_shape: float, h_shape: float, qp: float = 1.0) -> dict:
    """Azione del vento su elementi orizzontali rettangolari [CNR DT207/2008 G.10.3]

    Fornisce l'azione del vento su elementi orizzontali rettangolari secondo la
    direzione X (Y dal basso verso l'alto).

                        ^     |------------------------|
        vento X         |     |                        |
        ------>      h_shape  |                        |
                        |     |                        |
                        v     |------------------------|

                              |<------- d_shape ------>|

    Args:
        d_shape (float): Larghezza del rettangolo
        h_shape (float): Altezza del rettangolo
        qp (float, optional): Pressione cinetica di picco. Defaults to 1.0

    Returns:
        dict:
            'input':
                'd_shape': larghezza elemento
                'h_shape': altezza elemento,
                'qp': pressione cinetica di picco
            'output':
                'delta': rapporto d_shape/h_shape,
                'lref': lunghezza di riferimento,
                'C_fx': coefficiente di forza lungo X,
                'C_fy': coefficiente di forza lungo Y,
                'C_mz': coefficiente di momento lungo Z,
                'f_x': forza lungo X per unità di lunghezza,
                'f_y': forza lungo Y per unità di lunghezza,
                'm_z': coppia lungo Z per unità di lunghezza,
    """
    delta = d_shape / h_shape

    if 0.1 <= delta and delta < 0.2:
        C_fx0 = 2.0

    elif 0.2 <= delta and delta < 0.7:
        C_fx0 = 0.73 * np.log10(delta) + 2.51

    elif 0.7 <= delta and delta < 5.0:
        C_fx0 = -1.64 * np.log10(delta) + 2.15

    elif 5.0 <= delta and delta < 10.0:
        C_fx0 = -0.33 * np.log10(delta) + 1.23

    elif 10.0 <= delta and delta <= 50.0:
        C_fx0 = 0.9

    else:
        raise ex.EXAExceptions("ERR", "must be 0.1 <= d_shape/h_shape <= 50.0", delta)

    C_fy0 = 0.0
    C_mz0 = 0.0

    # A favore di sicurezza poichè compreso tra 0 ed 1 [CNR DT207/2008 G.9.4]
    g_lambda = 1.0

    # Coefficienti di forza
    C_fx = C_fx0 * g_lambda
    C_fy = C_fy0 * g_lambda
    C_mz = C_mz0 * g_lambda

    # Lunghezza di riferimento
    lref = h_shape

    f_x = qp * lref * C_fx
    f_y = qp * lref * C_fy
    m_z = qp * lref * lref * C_mz

    res = {
        "input": {"d_shape": d_shape, "h_shape": h_shape, "qp": qp},
        "output": {
            "delta": delta,
            "lref": lref,
            "C_fx": C_fx,
            "C_fy": C_fy,
            "C_mz": C_mz,
            "f_x": f_x,
            "f_y": f_y,
            "m_z": m_z,
        },
    }

    return res


def windActionsForcesOnBridge(d_bridge: float, h_tot: float, qp: float = 1) -> dict:
    """Azione del vento su impalcati da ponte [CNR DT207/2008 G.11]

    Calcola l'azione del vento su impalcati da ponte secondo la CNR DT207/2008
    al punto G.11.

    Sono applicabili a impalcati da ponte a sezione costante lungo la linea
    d'asse, limitatamente ai tipi riportati in Figura G.54, per ponti a luce
    singola o multipla, purché di lunghezza non superiore a 200 m.

    Si considerano esclusi da questo paragrafo altri tipi di ponti quali i
    ponti ad arco, i ponti sospesi o strallati, i ponti coperti o mobili,
    i ponti con curvature planimetriche significative e i ponti costituiti
    da più impalcati affiancati non riconducibili al semplice schema illustrato
    nel paragrafo G.11.2. Per tutti questi tipi strutturali occorre sviluppare
    specifiche e mirate valutazioni.

    Il calcolo è valido per valori di d/h >=2. Per valori inferiori si fà
    riferimento a windActionsForcesOnRect() per C_fx

    Args:
        d_bridge (float): _description_
        h_tot (float): _description_
        qp (float, optional): _description_. Defaults to 1.

    Returns:
        dict: _description_
    """
    delta = d_bridge / h_tot

    if delta < 2.0:
        resRect = windActionsForcesOnRect(d_bridge, h_tot, qp)
        C_fx = resRect["output"]["C_fx"]
        C_fy = 0.70 + 0.1 * delta

    elif 2 <= delta and delta <= 5.0:
        C_fx = 1.85 / delta - 0.10
        C_fy = 0.70 + 0.1 * delta

    else:
        C_fx = 1.35 / delta
        C_fy = 1.20

    C_mz = 0.20

    # Lunghezza di riferimento
    lref = d_bridge

    f_x = qp * lref * C_fx
    f_y = qp * lref * C_fy
    m_z = qp * lref * lref * C_mz

    res = {
        "input": {"d_bridge": d_bridge, "h_tot": h_tot, "qp": qp},
        "output": {
            "delta": delta,
            "lref": lref,
            "C_fx": C_fx,
            "C_fy": C_fy,
            "C_mz": C_mz,
            "f_x": f_x,
            "f_y": f_y,
            "m_z": m_z,
        },
    }

    return res
