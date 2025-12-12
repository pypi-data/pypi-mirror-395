from typing import Literal, List, Any, Union, Dict
from pathlib import Path
import pandas as pd
import numpy as np
import math
import time
import json

from numpy.typing import ArrayLike, NDArray

import pyvista as pv
from pyvista import Plotter

import matplotlib.pyplot as plt

from pycivil.EXAUtils.logging import log
from pycivil.EXAStructural.templateRCRect import RCTemplRectEC2
from pycivil.EXAStructural.codes import Code
from pycivil.EXAStructural.loads import Frequency_Enum, LimiteState_Enum, ForcesOnSection as Load
from pycivil.EXAStructural.materials import Concrete, ConcreteSteel
from pycivil.EXAStructuralCheckable.RcsRectangular import RcsRectangular
from pycivil.EXAStructural.checkable import CheckableCriteriaEnum as Crit, Enum

class ResultsType(str, Enum):
    WA = "WA",
    FORCE = "FORCE"

class PostProcessor:
    def __init__(self):

        self.__ll: Literal[0, 1, 2, 3] = 3

        self.__working_path: None | Path = None
        self.__in_rel_path: None | Path = Path("in")
        self.__out_rel_path: None | Path = Path("out")

        self.__fn_nodes: str = "Nodes_Coordinates.txt"
        self.__fn_elements: str = "Elements_Elements.txt"
        self.__fn_model: str = "Model.txt"

        self.__fn_assignments_for_rebar: str = "rebars_assignment.xlsx"
        self.__fn_assignments_for_check: str = "check_assignment.xlsx"

        self.__nodes_df: None | pd.DataFrame = None
        self.__nodes_id: None | np.ndarray = None
        self.__nodes_coords: None | np.ndarray = None

        self.__elements_df: None | pd.DataFrame = None
        self.__elements_2D_id: None | np.ndarray = None
        self.__elements_2D_groups: None | np.ndarray = None
        self.__elements_2D_properties: None | dict = None
        self.__elements_2D_connectivity: None | List[np.ndarray] = None
        self.__elements_2D_type: None | List[np.ndarray] = None

        self.__assignments_for_rebar: None | dict = None
        self.__assignments_for_check: None | dict = None

        self.__model_static_nl_combo: None | List[str] = None
        self.__model_plate_properties: None | dict = None

        self.__plate_results_stream: None | List[Any] = None
        self.__plate_results_log_stream: None | List[dict] = None
        self.__idx_check_nook: None | List[int] = None

        self.__results_parsed: Union[None, NDArray] = None

        self.__filter_on_group: List[str] | None = None

        self.__curr_check_required: Crit = Crit.SLU_NM
        self.__curr_input_results_tp: ResultsType = ResultsType.WA
        self.__curr_input_results_name: str = ""

        # Main results dictionary
        self.__results_checked: Dict[str, Dict[ResultsType, Dict[Crit, List[Any]]]] = dict()

        self.__path_last_figure_plotted: Path | None = None

    def setFilterOnGroups(self, f: List[str] | None):
        self.__filter_on_group = f

    def getFilterOnGroups(self) -> List[str] | None:
        return self.__filter_on_group

    def getResultsChecked(self) -> Dict[str, Dict[ResultsType, Dict[Crit, List[Any]]]]:
        return self.__results_checked

    def getPathLastFigurePlotted(self) -> Path | None:
        return self.__path_last_figure_plotted

    def getPathOutAbsolute(self) -> Path | None:
        return self.__working_path / self.__out_rel_path

    def getPathWorking(self) -> Path | None:
        return self.__working_path


    @staticmethod
    def __parse_model_plate_properties(path: Path) -> None | dict:
        parsed = {}
        read_block = False
        with open(path) as file:
            for item in file:
                if not read_block:
                    if item[0] == '/':
                        if "/ PLATE PROPERTIES" in item:
                            read_block = True
                else:
                    if "PlateShellProp" in item:
                        row_split = item.split()
                        prop_id = int(row_split[1])
                        prop_name = row_split[3]
                        parsed[prop_id] = []
                        parsed[prop_id].append(prop_name)
                    if " MemThick" in item:
                        row_split = item.split()
                        prop_MemThick = float(row_split[1])
                        parsed[prop_id].append(prop_MemThick)
                    if " BendThick" in item:
                        row_split = item.split()
                        prop_BendThick = float(row_split[1])
                        parsed[prop_id].append(prop_BendThick)
                    if item[0] == '/':
                        break
        if len(parsed) == 0:
            return None
        return parsed

    @staticmethod
    def __parse_model_static_nl_combo(path: Path) -> None | List[str]:
        parsed = []
        read_block = False
        with open(path) as file:
            for item in file:
                if not read_block:
                    if item[0] == '/':
                        if "/ NON-LINEAR STATIC SOLVER DATA" in item:
                            read_block = True
                else:
                    if "NonLinearIncrement" in item:
                        row_splitted = item.split()
                        combo_name = str(row_splitted[4].strip('"'))
                        parsed.append(combo_name)
                    if item[0] == '/':
                        break
        return parsed

    @staticmethod
    def __make_file_assignments_for_rebar(
            path: Path,
            groups: np.ndarray,
            ll: Literal[0, 1, 2, 3]
    ) -> bool:
        df_rows_nb = len(np.unique(groups))
        rebar_colum = np.full(df_rows_nb, dtype=object, fill_value="[[nb=, diam=, dist=, from=]]")
        shear_colum = np.full(df_rows_nb, dtype=object, fill_value="[[nb=, diam=, dist=, step=]]")
        rebar_mat_code = np.full(df_rows_nb, dtype=object, fill_value="NTC2008")
        rebar_mat_key = np.full(df_rows_nb, dtype=object, fill_value="B450C")
        rebar_mat_sensitivity = np.full(df_rows_nb, dtype=object, fill_value="not sensitive")
        concrete_mat_code = np.full(df_rows_nb, dtype=object, fill_value="NTC2008")
        concrete_mat_key = np.full(df_rows_nb, dtype=object, fill_value="NTC2008")
        concrete_mat_environment = np.full(df_rows_nb, dtype=object, fill_value="not aggressive")
        thick_reduced = np.full(df_rows_nb, dtype=float, fill_value=0.0)

        combined = np.vstack((
            groups,
            rebar_colum,
            rebar_colum,
            shear_colum,
            rebar_mat_code,
            rebar_mat_key,
            rebar_mat_sensitivity,
            concrete_mat_code,
            concrete_mat_key,
            concrete_mat_environment,
            thick_reduced
        )).transpose()
        rebars_assignments = pd.DataFrame(
            combined,
            columns=[
                "group",
                "lay13_rebar",
                "lay24_rebar",
                "shear_rebar",
                "rebar_code",
                "rebar_key",
                "rebar_sensitivity",
                "concrete_code",
                "concrete_key",
                "concrete_environment",
                "thick_reduced"
            ]
        )
        rebars_assignments.to_excel(path)
        msg = f"File {path.name} ... created !!!"
        log("INF", msg, ll, True)
        return True

    @staticmethod
    def __make_file_assignments_for_check(
            path: Path,
            combo: List[str],
            ll: Literal[0, 1, 2, 3]
    ) -> bool:
        df_rows_nb = len(combo)
        check_colum = np.full(df_rows_nb, dtype=object, fill_value="X")
        no_check_colum = np.full(df_rows_nb, dtype=object, fill_value="")
        combined = np.vstack((
            np.array(combo),
            check_colum,
            check_colum,
            check_colum,
            check_colum,
            no_check_colum,
            no_check_colum,
            no_check_colum,
            no_check_colum,
            no_check_colum,
            no_check_colum
        )).transpose()
        check_assignments = pd.DataFrame(
            combined,
            columns=["combo_name",
                     "CHECK_SLU_NM",
                     "CHECK_SLU_T",
                     "CHECK_SLE_NM",
                     "CHECK_SLE_F",
                     "SLU",
                     "SLV",
                     "SLE_R",
                     "SLE_F",
                     "SLE_QP",
                     "ACC"
                     ]
        )
        check_assignments.to_excel(path)
        msg = f"File {path.name} ... created !!!"
        log("INF", msg, ll, True)
        return True

    @staticmethod
    def __parse_assignment_for_rebar(path: Path, ll: Literal[0, 1, 2, 3]) -> None | dict:
        msg = f"File {path.name} already exists. I'm reading ..."
        log("INF", msg, ll, True)
        columns = (
            "group",
            "lay13_rebar",
            "lay24_rebar",
            "shear_rebar",
            "rebar_code",
            "rebar_key",
            "rebar_sensitivity",
            "concrete_code",
            "concrete_key",
            "concrete_environment",
            "thick_reduced"
        )
        assignments_df = pd.read_excel(path, usecols=columns)
        assignments = dict()
        for r in assignments_df.to_numpy():
            lay13_rebar_assigned = None
            lay24_rebar_assigned = None
            shear_rebar_assigned = None
            try:
                lay13_rebar_assigned = eval(r[1])
            except SyntaxError:
                msg = f"SyntaxError in lay13 rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            except NameError:
                msg = f"NameError in lay13 rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            try:
                lay24_rebar_assigned = eval(r[2])
            except SyntaxError:
                msg = f"SyntaxError in lay24 rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            except NameError:
                msg = f"NameError in lay24 rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            try:
                shear_rebar_assigned = eval(r[3])
            except SyntaxError:
                msg = f"SyntaxError in shear rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            except NameError:
                msg = f"NameError in shear rebar assign at group *{r[0]}* !!!"
                log("ERR", msg, ll, True)
            c1 = lay13_rebar_assigned is not None
            c2 = lay24_rebar_assigned is not None
            c3 = shear_rebar_assigned is not None
            if all([c1, c2, c3]):
                assignments[r[0]] = [
                    lay13_rebar_assigned,
                    lay24_rebar_assigned,
                    shear_rebar_assigned,
                    r[4], r[5], r[6], r[7], r[8], r[9], r[10]
                ]
            else:
                return None

        return assignments

    @staticmethod
    def __parse_assignment_for_check(path: Path, ll: Literal[0, 1, 2, 3]) -> None | dict:
        msg = f"File {path.name} already exists. I'm reading ..."
        log("INF", msg, ll, True)
        columns = (
            "combo_name",
            "CHECK_SLU_NM",
            "CHECK_SLU_T",
            "CHECK_SLE_NM",
            "CHECK_SLE_F",
            "SLU",
            "SLV",
            "SLE_R",
            "SLE_F",
            "SLE_QP",
            "ACC"
        )
        assignments_df = pd.read_excel(path, usecols=columns)
        assignments = {}
        for r in assignments_df.to_numpy():
            SLU_NM = True if r[1] == 'X' else False
            SLU_T = True if r[2] == 'X' else False
            SLE_NM = True if r[3] == 'X' else False
            SLE_F = True if r[4] == 'X' else False
            combo_type = ""
            if r[5] == 'X':
                combo_type = "SLU"
            if r[6] == 'X':
                combo_type = "SLV"
            if r[7] == 'X':
                combo_type = "SLE_R"
            if r[8] == 'X':
                combo_type = "SLE_F"
            if r[9] == 'X':
                combo_type = "SLE_QP"
            if r[10] == 'X':
                combo_type = "ACC"
            assignments[r[0]] = {
                "combo_name": r[0],
                "SLU_NM": SLU_NM,
                "SLU_T": SLU_T,
                "SLE_NM": SLE_NM,
                "SLE_F": SLE_F,
                "combo_type": combo_type
            }
        if len(assignments) == 0:
            assignments = None
        return assignments

    @staticmethod
    def __extract_plate_layer_combo(res: ArrayLike):
        plate_id = int(res[0].split(':')[0].split(' ')[1])
        layer_id = 0
        if len(res[0].split(':')) == 2:
            layer_id = int(res[0].split(':')[1].split(' ')[2])
        combo_id = int(res[1].split(':')[0])
        combo_name = res[1].split(':')[1].split(' ')[1]
        return plate_id, layer_id, combo_id, combo_name

    def __checker_for_plate(
            self,
            plate_id: int,
            layer_id: int,
            combo_id: int,
            combo_name: str,
            plate_thick: float,
            F1: float,
            F2: float,
            rebar_assignment: list,
            check_assignment: dict,
            group_name: str,
            print_nook: bool = True,
            save_fig_nook: bool = False,
            save_fig_ok: bool = False,
            check_required: str = 'SLU_NM',
            ll: Literal[0, 1, 2, 3] = 3
    ) -> dict:
        check_result = dict()
        check_result['global_check'] = True
        code_steel = Code(rebar_assignment[3])
        steel = ConcreteSteel()
        steel.setByCode(code_steel, rebar_assignment[4])
        steel.setSensitivity(rebar_assignment[5])

        code_concrete = Code(rebar_assignment[6])
        concrete = Concrete()
        concrete.setByCode(code_concrete, rebar_assignment[7])
        concrete.setEnvironment(rebar_assignment[8])

        KN = 1000
        KNm = 1000 * 1000
        m = 1000

        section = RCTemplRectEC2(1, f"Template RC Section for plate {plate_id} with thick = {plate_thick*1000:.0f}")
        section.setConcreteMaterial(concrete)
        section.setSteelMaterial(steel)
        section.setDimH(plate_thick * m - rebar_assignment[9])
        section.setDimW(1000)

        err = False
        force = Load()
        Med = 0.0
        Ned = 0.0
        Ted = 0.0
        if check_assignment['combo_type'] == 'SLU' and check_assignment['SLU_NM'] and  check_required == 'SLU_NM':
            Med = F1
            Ned = F2
            if layer_id == 3 or layer_id == 4:
                Med = -Med
            # Normal efforts must be multiplied for 2 cause Wood Armer Moment
            force.id = combo_id
            force.Fx = 2*Ned * KN
            force.My = Med * KNm
            force.descr=f"Layer: {layer_id} Combo: {combo_name}"
            force.limitState = LimiteState_Enum.ULTIMATE
            check_result['SLU_NM'] = dict()
        elif check_assignment['combo_type'] == 'SLU' and check_assignment['SLU_T']  and  check_required == 'SLU_T':
            Ted = float(np.sqrt(F1**2 + F2**2))
            force.id = combo_id
            force.Fz = Ted * KN
            force.descr=f"Combo: {combo_name}"
            force.limitState = LimiteState_Enum.ULTIMATE
            check_result['SLU_T'] = dict()
        elif check_assignment['combo_type'] == 'SLE_R' and check_assignment['SLE_NM']  and  check_required == 'SLE_NM':
            Med = F1
            Ned = F2
            if layer_id == 3 or layer_id == 4:
                Med = -Med
            # Normal efforts must be multiplied for 2 cause Wood Armer Moment
            force.id=combo_id
            force.Fx = 2*Ned * KN
            force.My = Med * KNm
            force.descr=f"Layer: {layer_id} Combo: {combo_name}"
            force.limitState = LimiteState_Enum.SERVICEABILITY
            force.frequency = Frequency_Enum.CHARACTERISTIC
            check_result['SLE_NM'] = dict()
        elif check_assignment['combo_type'] == 'SLE_QP' and check_assignment['SLE_NM']  and  check_required == 'SLE_NM':
            Med = F1
            Ned = F2
            if layer_id == 3 or layer_id == 4:
                Med = -Med
            # Normal efforts must be multiplied for 2 cause Wood Armer Moment
            force.id=combo_id
            force.Fx = 2*Ned * KN
            force.My = Med * KNm
            force.descr=f"Layer: {layer_id} Combo: {combo_name}"
            force.limitState = LimiteState_Enum.SERVICEABILITY
            force.frequency = Frequency_Enum.QUASI_PERMANENT
            check_result['SLE_NM'] = dict()
        elif check_assignment['combo_type'] == 'SLE_F' and check_assignment['SLE_F']  and  check_required == 'SLE_F':
            Med = F1
            Ned = F2
            if layer_id == 3 or layer_id == 4:
                Med = -Med
            # Normal efforts must be multiplied for 2 cause Wood Armer Moment
            force.id=combo_id
            force.Fx = 2*Ned * KN
            force.My = Med * KNm
            force.descr=f"Layer: {layer_id} Combo: {combo_name}"
            force.limitState = LimiteState_Enum.SERVICEABILITY
            force.frequency = Frequency_Enum.FREQUENT
            check_result['SLE_F'] = dict()
        elif check_assignment['combo_type'] == 'SLE_QP' and check_assignment['SLE_F']  and  check_required == 'SLE_F':
            Med = F1
            Ned = F2
            if layer_id == 3 or layer_id == 4:
                Med = -Med
            # Normal efforts must be multiplied for 2 cause Wood Armer Moment
            force.id=combo_id
            force.Fx = 2*Ned * KN
            force.My = Med * KNm
            force.descr=f"Layer: {layer_id} Combo: {combo_name}"
            force.limitState = LimiteState_Enum.SERVICEABILITY
            force.frequency = Frequency_Enum.QUASI_PERMANENT
            check_result['SLE_F'] = dict()
        else:
            err = True
            msg = f"None check for SLU and SLU_NM selection !!!"
            log("WRN", msg, ll, True)

        if not err:

            if layer_id == 1 or layer_id == 3:
                rebars_aligned_arr = rebar_assignment[0]
            elif layer_id == 2 or layer_id == 4:
                rebars_aligned_arr = rebar_assignment[1]
            else:
                rebars_aligned_arr = []

            # We need this because height section util for shear for example
            if layer_id == 0:
                rebars_aligned_arr = rebar_assignment[0] + rebar_assignment[1]

            for r in rebars_aligned_arr:
                if r[3] < 0:
                    section.addSteelArea("LINE-MT", dist=-r[3], d=r[1], nb=r[0], sd=r[2])
                else:
                    section.addSteelArea("LINE-MB", dist=r[3], d=r[1], nb=r[0], sd=r[2])

            checkable = RcsRectangular(section)
            perform_save_fig = False
            if check_required == 'SLU_NM':
                checkable.setMaxPointsForSLUDomain(20)
                res = checkable.check_SLU_NM_NTC2018(force)
                check_result['SLU_NM'] = res
                check_result['safetyFactor'] = res['safetyFactor']['interactionDomain']
                if res['safetyFactor']['interactionDomain'] < 1:
                    check_result['global_check'] = False
                    if print_nook:
                        msg = (f"Safety factor is {res['safetyFactor']['interactionDomain']} for plate "
                               f"{plate_id} layer {layer_id} combo_name {combo_name}")
                        log("ERR", msg, ll, True)
                        msg = f"       : Group Name: {group_name} Thickness is {section.getDimH():.0f}mm"
                        log("WRN", msg, ll, True)
                        msg = f"       : Med = {Med} Ned = {2*Ned} Rebar: {rebars_aligned_arr}"
                        log("WRN", msg, ll, True)
                    if save_fig_nook:
                        perform_save_fig = True
                else:
                    if save_fig_ok:
                        perform_save_fig = True

                if perform_save_fig:
                    gn = group_name.replace('\\', '-')
                    fn = (self.__working_path /
                          self.__out_rel_path /
                          Path(f"group-{gn}-plate-{plate_id}-layer-{layer_id}-combo-{combo_name}.png"))
                    section.interactionDomainPlot2d(
                        xLabel="N [KN]",
                        yLabel="M [KN*m]",
                        export=str(fn)
                    )

            elif check_required == 'SLU_T':
                stirrup_arr = rebar_assignment[2]
                sum_Awi = 0
                sum_si = 0
                for r in stirrup_arr:
                    nb_leg = r[0]
                    diam_leg = r[1]
                    area_leg = diam_leg**2 * np.pi / 4
                    sum_Awi += area_leg * nb_leg
                    sum_si += r[3]
                average_si = sum_si / len(stirrup_arr)
                shear_area = sum_Awi
                section.setStirrupt(area = shear_area, dist = average_si, angle = 90)
                res = checkable.check_SLU_T_NTC2018(force)
                check_result['SLU_T'] = res
                check_result['safetyFactor'] = None
                if res["safetyFactor"] is not None:
                    check_result['safetyFactor'] = res['safetyFactor']['globalCheck']
                    if check_result['safetyFactor'] < 1:
                        check_result['global_check'] = False
                        if print_nook:
                            msg = (f"WARNING: Safety factor is {check_result['safetyFactor']} for plate {plate_id}"
                                   f"layer {layer_id} combo_name {combo_name} ")
                            log("WRN", msg, ll, True)
                            msg = f"       : Group Name: {group_name} Thickness is {section.getDimH():.0f}"
                            log("WRN", msg, ll, True)
                            msg = f"       : Ted = {Ted} Shear Area: {shear_area} Average Step: {average_si}"
                            log("WRN", msg, ll, True)

            elif check_required == 'SLE_NM':
                res = checkable.check_SLE_NM_NTC2018(force)
                check_result['SLE_NM'] = res
                check_result['global_check'] = res["check"]["globalCheck"]
                check_result['safetyFactor'] = None
                # Is None Type when section is totally stretched
                if res["safetyFactor"]["globalCheck"] is not None:
                    check_result['safetyFactor'] = res["safetyFactor"]["globalCheck"]
                    if check_result['safetyFactor'] < 1:
                        if print_nook:
                            msg = (f"WARNING: Safety factor is {check_result['safetyFactor']} for plate {plate_id} "
                                   f"layer {layer_id} combo_name {combo_name} ")
                            log("WRN", msg, ll, True)
                            msg = f"       : Group Name: {group_name} Thickness is {section.getDimH():.0f}"
                            log("WRN", msg, ll, True)
                            msg = f"       : Med = {Med} Ned = {2*Ned} Rebar: {rebars_aligned_arr}"
                            log("WRN", msg, ll, True)

            elif check_required == 'SLE_F':
                res = checkable.check_SLE_F_NTC2018(force)
                check_result['SLE_F'] = res
                check_result['global_check'] = res["check"]["crack"]
                check_result['safetyFactor'] = None
                # Is None Type when section is totally stretched
                if res["safetyFactor"]["crack"] is not None:
                    check_result['safetyFactor'] = res["safetyFactor"]["crack"]
                    if check_result['safetyFactor'] < 1:
                        if print_nook:
                            msg = (f"WARNING: Safety factor is {check_result['safetyFactor']} for plate {plate_id} "
                                   f"layer {layer_id} combo_name {combo_name} ")
                            log("WRN", msg, ll, True)
                            msg = f"       : Group Name: {group_name} Thickness is {section.getDimH():.0f}"
                            log("WRN", msg, ll, True)
                            msg = f"       : Med = {Med} Ned = {2*Ned} Rebar: {rebars_aligned_arr}"
                            log("WRN", msg, ll, True)
        return check_result

    @staticmethod
    def __write_to_excel_with_row_limited(
            file_path: Path,
            rows_per_file: int,
            data: Union[None, NDArray[Any]],
            ll: Literal[0, 1, 2, 3]
    ):
        number_of_files = math.floor((len(data) / rows_per_file)) + 1
        start_index = 0
        end_index = rows_per_file
        columns = ["plate_nb", "layer", "combo_name", "combo_id", "plate_thick", "F1", "F2", "rebar_properties",
                   "check_properties", "group", "check_performed", "safety_factor", "plate_X", "plate_Y", "plate_Z"]
        df = pd.DataFrame(data, columns=columns)
        log("INF", f" ... data shape originale {df.shape}", ll, True)

        for i in range(number_of_files):
            filepart = Path(str(file_path) + str(Path('_file_' + str(i) + '.xlsx')))
            log("INF", f" ... writing file {filepart} {df.shape}", ll, True)

            with pd.ExcelWriter(filepart, engine='openpyxl') as writer:
                df_mod = df.iloc[start_index:end_index]
                log("INF", f" ... data shape chunked {df_mod.shape}", ll, True)
                df_mod.to_excel(writer, index=False, sheet_name='sheet')
                start_index = end_index
                end_index = end_index + rows_per_file
                df_mod.to_excel(writer)

    def export_checks_to_files(self, file_path: Path, write_json=False, export_nook=True, export_xlsx=True):
        path = self.__working_path / self.__out_rel_path / file_path
        stream_in = self.__plate_results_stream
        stream_out = self.__plate_results_log_stream
        nook_indices = self.__idx_check_nook

        # Write json verbose and slow process
        if write_json:
            log("INF", f"I'm writing json ... ", self.__ll, True)
            with open(str(path) + ".json", 'w') as f:
                json.dump(stream_out, f, indent=4)
            log("INF", f"... done", self.__ll, True)



        # Export NOOK results
        #
        if len(nook_indices) > 0:
            log("INF", f"I risultati con check negativo sono {len(nook_indices)}", self.__ll, True)

            plate_results_stream_nook = np.zeros((len(nook_indices), len(stream_in[0])), dtype=object)

            for idx, val in enumerate(nook_indices):
                plate_results_stream_nook[idx] = np.array(stream_in[val], dtype=object)

            if export_nook:
                log("INF", f"I'm writing nook results on excel file ... ", self.__ll, True)
                self.__write_to_excel_with_row_limited(
                    Path(str(path) + "_nook"),
                    50000,
                    plate_results_stream_nook,
                    self.__ll
                )
                log("INF", f"... done", self.__ll, True)

        else:
            log("INF", f"Nook results are zero lenght. Can't export it.", self.__ll, True)

        if export_xlsx:
            log("INF", f"I'm writing results on excel file ... ", self.__ll, True)
            self.__write_to_excel_with_row_limited(
                path,
                50000,
                stream_in,
                self.__ll
            )
            log("INF", f"... done", self.__ll, True)
        else:
            log("INF", f"Required don't export massive excel results files.", self.__ll, True)

    def results_checker(
            self,
            max_row: int | None = None,
            check_required: str = 'SLU_NM',
            save_fig_nook: bool = False,
            save_fig_ok: bool = False
        ) -> bool:
        results = self.__results_parsed
        row_to_check = len(results)
        elements_2D_properties = self.__elements_2D_properties
        check_assignments = self.__assignments_for_check
        rebar_assignments = self.__assignments_for_rebar
        if max_row is None:
            plate_results_stream = [dict()] * row_to_check
            plate_results_log_stream = [dict()] * row_to_check
        else:
            plate_results_stream = [dict()] * min(row_to_check, max_row)
            plate_results_log_stream = [dict()] * min(row_to_check, max_row)

        idx = 0
        msg = f"Number of results for check {row_to_check}"
        log("WRN", msg, self.__ll, True)
        idx_check_nook = []
        start_single = time.time()
        min_safety_factor = 1000000000000000
        max_safety_factor = -1000000000000000

        for res in results:
            plate_id, layer_id, combo_id, combo_name = self.__extract_plate_layer_combo(res)

            # Filter on Elements dataframe
            #
            if self.__filter_on_group is not None:
               if elements_2D_properties.get(plate_id) is None:
                    idx += 1
                    continue

            property_id = elements_2D_properties[plate_id][2]
            group_name = elements_2D_properties[plate_id][1]

            elements_XX = elements_2D_properties[plate_id][5]
            elements_YY = elements_2D_properties[plate_id][6]
            elements_ZZ = elements_2D_properties[plate_id][7]

            try:
                rebar_for_check = rebar_assignments[group_name]
            except KeyError:
                log("ERR", f"Error in {group_name} fetching rebar assignment", self.__ll, True)
                log("ERR", f"Probably you didn't check Show Group Path in Strand7 while exporting.", self.__ll, True)
                return False

            plate_thick = self.__model_plate_properties[property_id][1]
            plate_input_row = (plate_id, layer_id, combo_id, combo_name, plate_thick, res[2], res[3], rebar_for_check,
                               check_assignments[combo_name], group_name)
            output_stream = self.__checker_for_plate(
                *plate_input_row,
                save_fig_nook=save_fig_nook,
                check_required=check_required,
                save_fig_ok=save_fig_ok
            )
            plate_results_log_stream[idx] = output_stream

            plate_results_stream[idx] = plate_input_row + (check_required, output_stream['safetyFactor'], elements_XX,
                                                           elements_YY, elements_ZZ)

            if plate_results_log_stream[idx]['safetyFactor'] is not None:
                if plate_results_log_stream[idx]['safetyFactor'] < min_safety_factor:
                    min_safety_factor = plate_results_log_stream[idx]['safetyFactor']

                if plate_results_log_stream[idx]['safetyFactor'] > max_safety_factor:
                    max_safety_factor = plate_results_log_stream[idx]['safetyFactor']

            # Build index for nook check result
            if not plate_results_log_stream[idx]['global_check']:
                idx_check_nook.append(idx)

            nb_elements_trace = 1000
            if idx / nb_elements_trace == np.floor(idx / nb_elements_trace):
                end_single = time.time()
                elapsed = end_single - start_single
                remaining = (len(results) - idx) * (elapsed / nb_elements_trace)
                msg = (f"Elaborati {idx} di {row_to_check} - {idx / row_to_check * 100:.4f} % in {elapsed:.2f} sec. "
                       f"Restano {remaining:.0f} sec. (min sf: {min_safety_factor:.2f} - max sf: {max_safety_factor:.2f})")
                log("INF", msg, self.__ll, True)
                start_single = time.time()

            idx += 1
            if max_row is not None:
                if idx == max_row:
                    break
        log("INF", f"Minimo fattore di sicurezza è {min_safety_factor}", self.__ll, True)
        log("INF", f"Massimo fattore di sicurezza è {max_safety_factor}", self.__ll, True)

        self.__plate_results_stream = plate_results_stream
        self.__plate_results_log_stream = plate_results_log_stream
        self.__idx_check_nook = idx_check_nook

        if len(plate_results_stream) > 0:
            # TODO: change "_" with "-" and remove <.replace('_','-')> from line below
            self.__curr_check_required = Crit(check_required.replace('_','-'))
            self.__results_checked[self.__curr_input_results_name] = {
                self.__curr_input_results_tp: {
                    self.__curr_check_required: plate_results_stream
                }
            }
        return True

    def getModelPlateProperties(self):
        return self.__model_plate_properties

    def getModelStaticNLCombo(self):
        return self.__model_static_nl_combo

    def getAssignmentsForRebars(self):
        return self.__assignments_for_rebar

    def getAssignmentsForCheck(self):
        return self.__assignments_for_check

    def getPlateResultsStream(self):
        return self.__plate_results_stream

    def getPlateResultsLogStream(self):
        return self.__plate_results_log_stream

    def getCheckNookIndices(self):
        return self.__idx_check_nook

    def getElement2DProperties(self):
        return self.__elements_2D_properties

    def parse(self) -> bool:

        if self.__working_path is None:
            msg = f"Working path is none. Assign it with setWorkingPath() !!!"
            log("ERR", msg, self.__ll, True)
            return False

        if not self.__working_path.exists():
            msg = (f"Working path {self.__working_path} doesn't exists. "
                   f"Assign it with setWorkingPath() !!!")
            log("ERR", msg, self.__ll, True)
            return False

        in_file_path = self.__working_path / self.__in_rel_path
        if not in_file_path.exists():
            msg = (f"Input path {self.__in_rel_path} in working path "
                   f"{self.__working_path} doesn't exists. You have to create it !!!")
            log("ERR", msg, self.__ll, True)
            return False

        out_file_path = self.__working_path / self.__out_rel_path
        if not out_file_path.exists():
            msg = (f"Output path {self.__out_rel_path} in working path "
                   f"{self.__working_path} doesn't exists. You have to create it !!!")
            log("ERR", msg, self.__ll, True)
            return False

        # Parsing of NODES
        #
        nodes_file_path = self.__working_path / self.__in_rel_path / Path(self.__fn_nodes)
        if not nodes_file_path.exists():
            msg = (f"File of nodes {nodes_file_path} doesn't exists. "
                   f"Export it with Strand7 or change path !!!")
            log("ERR", msg, self.__ll, True)
            return False
        self.__nodes_df = pd.read_csv(nodes_file_path, header=[0, 1])
        self.__nodes_id = self.__nodes_df.iloc[:, [0]].to_numpy()
        self.__nodes_coords = self.__nodes_df.iloc[:, [2, 3, 4]].to_numpy()
        msg = f"File of nodes {nodes_file_path} done."
        log("INF", msg, self.__ll, True)

        # Parsing of ELEMENTS
        #
        element_file_path = self.__working_path / self.__in_rel_path / Path(self.__fn_elements)
        if not element_file_path.exists():
            msg = (f"File of elements {element_file_path} doesn't exists. "
                   f"Export it with Strand7 or change path !!!")
            log("ERR", msg, self.__ll, True)
            return False

        self.__elements_df = pd.read_csv(element_file_path, header=[0, 1])
        log("INF", f"Elements read from file {len(self.__elements_df)}", self.__ll, True)
        if self.__filter_on_group is not None:
            mask_on_group = self.__elements_df["Group"].isin(self.__filter_on_group)
            self.__elements_df = self.__elements_df[mask_on_group.values]
            log("INF", f"Elements filtered {len(self.__elements_df)}", self.__ll, True)

        self.__elements_2D_id = self.__elements_df.loc[:, "Plate"].to_numpy()
        self.__elements_2D_groups = self.__elements_df.loc[:, "Group"].to_numpy()

        # Forming arrays for PYVISTA
        #
        elements_2D_connectivity = \
            self.__elements_df.iloc[:, [14, 15, 16, 17, 18, 19, 20, 21, 22]].fillna(0).to_numpy()
        self.__elements_2D_connectivity = []
        self.__elements_2D_type = []
        nb_lines = 0
        nb_triangles = 0
        nb_quad = 0

        for e in elements_2D_connectivity:
            element = [len(np.trim_zeros(e)), *list(np.trim_zeros(e))]
            indexes = [len(np.trim_zeros(e))]

            for i in element[1:len(element)]:
                indexes.append(np.where(self.__nodes_id == i)[0][0])

            self.__elements_2D_connectivity += indexes
            if element[0] == 2:
                self.__elements_2D_type.append(pv.CellType.LINE)
                nb_lines += 1
            if element[0] == 3:
                self.__elements_2D_type.append(pv.CellType.TRIANGLE)
                nb_triangles += 1
            if element[0] == 4:
                self.__elements_2D_type.append(pv.CellType.QUAD)
                nb_quad += 1

        log("INF", f"Parsed {nb_lines} lines | {nb_triangles} triangles | {nb_quad} quads", self.__ll, True)

        # Forming __elements_2D_properties
        #
        elements_property = self.__elements_df.loc[:, "Property"].to_numpy()
        elements_angle = self.__elements_df.loc[:, "Angle"].to_numpy()
        elements_X = self.__elements_df.loc[:, "X"].to_numpy()
        elements_Y = self.__elements_df.loc[:, "Y"].to_numpy()
        elements_Z = self.__elements_df.loc[:, "Z"].to_numpy()
        self.__elements_2D_properties = dict()
        for i, v in np.ndenumerate(self.__elements_2D_id):
            prop_id = int(elements_property[i[0]][0].split(':')[0])
            prop_str = elements_property[i[0]][0].split(':')[1].strip()
            self.__elements_2D_properties[v] = [
                i[0],
                self.__elements_2D_groups[i[0]][0],
                prop_id,
                prop_str,
                elements_angle[i[0]][0],
                elements_X[i[0]][0],
                elements_Y[i[0]][0],
                elements_Z[i[0]][0]
            ]
        # Parsing or creating REBAR ASSIGNMENTS file
        #
        # Build a dataframe for external rebar data formed by:
        #  -------------------------------------------------------------------------------
        # |  group  |  lay1_rebar  |  lay3_rebar | lay2_rebar | lay4_rebar | shear_legs |
        #  -------------------------------------------------------------------------------
        # Example for lay1_rebar:
        # -----------------------
        #              [[4, 20, 100, -50], [8, 26, 80, +50]]
        # means:
        # two rebars lines with 4 rebar d=20mm with distance 100mm between rebars and 50mm
        # from top (- sign) + 8 rebar d=26mm with distance 80mm  between rebars and 50mm
        # from bottom (+ sign)
        #
        # Example for shear_legs
        # -----------------------
        #             [[4, 12, 100, 250], [4, 10, 150, 200]]
        # means:
        # 4 legs diam=12mm with transverse distance 100mm and longitudinal step 250mm
        #
        rebars_file_path = self.__working_path / self.__in_rel_path / Path(self.__fn_assignments_for_rebar)
        if not rebars_file_path.exists():
            msg = (f"File of rebar assignments {rebars_file_path} doesn't exists. "
                   f"Will be created. Check it out and compile it !!!")
            log("INF", msg, self.__ll, True)
            self.__make_file_assignments_for_rebar(
                rebars_file_path,
                np.unique(self.__elements_2D_groups),
                self.__ll
            )
            return False
        else:
            self.__assignments_for_rebar = self.__parse_assignment_for_rebar(
                rebars_file_path,
                self.__ll
            )
            if self.__assignments_for_rebar is None:
                msg = f"... error reading !!! Quit."
                log("ERR", msg, self.__ll, True)
                return False
            msg = f"... read successfully !!!"
            log("INF", msg, self.__ll, True)

        # Parsing MODEL for plate properties
        model_file_path = self.__working_path / self.__in_rel_path / Path(self.__fn_model)
        if not model_file_path.exists():
            msg = (f"Model file {model_file_path} doesn't exists. "
                   f"Export it with Strand7 or change path !!!")
            log("ERR", msg, self.__ll, True)
            self.__model_plate_properties = None
            self.__model_static_nl_combo = None
            return False

        self.__model_plate_properties = self.__parse_model_plate_properties(model_file_path)
        if self.__model_plate_properties is None:
            msg = f"Model file {model_file_path} parsed plate properties with error."
            log("ERR", msg, self.__ll, True)
            return False
        msg = f"Model file {model_file_path} parsed plate properties with success."
        log("INF", msg, self.__ll, True)

        self.__model_static_nl_combo = self.__parse_model_static_nl_combo(model_file_path)
        if len(self.__model_static_nl_combo) == 0:
            msg = f"Model file {model_file_path} parsed plate properties with error."
            log("ERR", msg, self.__ll, True)
            return False
        msg = f"Model file {model_file_path} parsed not linear combinations with success."
        log("INF", msg, self.__ll, True)

        # Parsing or creating CHECK ASSIGNMENTS file
        #
        rebars_check_file_path = self.__working_path / self.__in_rel_path / Path(self.__fn_assignments_for_check)
        if not rebars_check_file_path.exists():
            msg = (f"File of check assignments {rebars_check_file_path} doesn't exists. "
                   f"Will be created. Check it out and compile it !!!")
            log("INF", msg, self.__ll, True)
            self.__make_file_assignments_for_check(
                rebars_check_file_path,
                self.__model_static_nl_combo,
                self.__ll
            )
            return False
        else:
            self.__assignments_for_check = self.__parse_assignment_for_check(
                rebars_check_file_path,
                self.__ll
            )
            if self.__assignments_for_rebar is None:
                msg = f"... error reading !!! Quit."
                log("ERR", msg, self.__ll, True)
                return False
            msg = f"... read successfully !!!"
            log("INF", msg, self.__ll, True)
        return True

    def setWorkingPath(self, working_path: str) -> bool:
        path = Path(working_path)

        if not path.exists():
            msg = (f"Working path {path} doesn't exists. "
                   f"Assign it with setWorkingPath() !!!")
            log("ERR", msg, self.__ll, True)
            return False

        self.__working_path = path
        log("INF", f"Working path <{self.__working_path}> done.", self.__ll, True)
        return True

    def readResults(self, file_name: Path, file_type: Literal["WA","FORCE"], skip_nb_rows: int = 0) -> bool:
        path = self.__working_path / self.__in_rel_path / file_name
        self.__curr_input_results_name = str(file_name)
        if file_type == "WA":
            self.__curr_input_results_tp = ResultsType.WA
            results_parsed = pd.read_csv(path, header=[0], skiprows=[1, 2] + [i for i in range(3, 3 + skip_nb_rows)])
            self.__results_parsed = results_parsed.to_numpy()
        elif file_type == "FORCE":
            self.__curr_input_results_tp = ResultsType.FORCE
            results_parsed = pd.read_csv(path, header=[0], skiprows=[1] + [i for i in range(2, 2 + skip_nb_rows)])
            self.__results_parsed = results_parsed.to_numpy()[:, [0, 1, 5, 6]]
        else:
            log("ERR", f"You have to choose WA or FORCE type", self.__ll, True)
            return False

        log("INF", f"You can check max {len(self.__results_parsed)} results", self.__ll, True)
        return True

    def plot_model(self, off_screen=False) -> Plotter:
        grid = pv.UnstructuredGrid(
            self.__elements_2D_connectivity,
            self.__elements_2D_type,
            self.__nodes_coords
        )
        pl = pv.Plotter(off_screen=off_screen)
        pl.show_axes()
        pl.add_mesh(grid, show_edges=True, line_width=1)
        return pl

    def plot_figure(self, results_fn: str, results_tp: str, check_required: str, skip_less_than: float | None = None) -> plt:
        results_list = self.__results_checked[results_fn][ResultsType(results_tp)][Crit(check_required.replace('_','-'))]
        results_arr = np.zeros((len(results_list),2))
        results_arr_skipped = np.zeros((len(results_list), 2))
        skipped = False
        nb_skipped = 0
        for i, r in enumerate(results_list):
            if type(r[12]) is np.float64:
                if skip_less_than is not None:
                    if r[11] <= skip_less_than:
                        skipped = True
                        nb_skipped += 1
                        results_arr_skipped[i] = [r[11], r[12]]
                    else:
                        results_arr[i] = [r[11],r[12]]
                else:
                    results_arr[i] = [r[11], r[12]]
            else:
                skipped = True
                nb_skipped += 1
                results_arr_skipped[i] = [r[11],r[12]]

        if skipped:
            log("WRN", f"Nb. {nb_skipped} results was skipped from {len(results_arr)}!!!", self.__ll, True)

        # results_arr = np.array(results_list)
        idx_col_sf = 0
        idx_col_xx = 1

        results_arr_no_zero = results_arr[results_arr[:,idx_col_sf] != 0]

        plt.figure()
        # plt.subplot(211)
        plt.xlabel('Progressive lenght [m]')
        plt.ylabel('Safety Factor (< 1 means check ok)')
        plt.title(f"File name: '{results_fn}' \n File type: '{results_tp}' - Check Required: '{check_required}'")
        plt.plot(results_arr_no_zero[:,idx_col_xx], results_arr_no_zero[:,idx_col_sf]**(-1), 'bo')
        path_where_save = self.__working_path / self.__out_rel_path
        fn_without_suffix = str(path_where_save / Path(results_fn).stem) + f"-{results_tp}" + f"-{check_required}"
        self.__path_last_figure_plotted = Path(fn_without_suffix).with_suffix(".png")
        plt.savefig(self.__path_last_figure_plotted)
        log("INF", f"Plotting figure {fn_without_suffix} ... ", self.__ll, True)
        plt.savefig(fn_without_suffix, dpi = 300)
        log("INF", f"... plotted.", self.__ll, True)
        return plt



