import logging
from itertools import groupby

import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill

from natsort import natsorted

from read_outputs_folder import read_outputs

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()


def prepare_key(algorithm_aliases, key):
    if key[10] is None:
        return algorithm_aliases[key[1] + "_" + key[9]]
    elif key[1] is None and key[0] == "phy":
        if key[11] is None and key[12] is None:
            if key[4] is not None and key[5] is not None:
                return algorithm_aliases[key[2] + "_" + key[10]]
            else:
                return algorithm_aliases[key[2] + "_" + key[10]]
        else:
            # TODO:KSPWLO
            pass
    elif key[1] is not None and key[0] == "mtr":
        if key[11] is None and key[12] is None:
            if key[4] is not None and key[5] is not None:
                return algorithm_aliases[key[2] + "_" + key[1] + "_" + key[10]]
            elif key[4] is None and key[5] is None:
                return algorithm_aliases[key[2] + "_" + key[1] + "_" + key[10]]


def prepare_value(value):
    value_list = list()
    value_list.append(value.topology_result.topology_name)
    value_list.append(value.topology_result.o1)
    value_list.append(value.topology_result.o2)
    value_list.append(value.topology_result.o3)
    value_list.append(value.topology_result.max_util)
    value_list.append(value.topology_result.average)
    value_list.append(value.topology_result.variance)
    value_list.append(value.topology_result.time)
    return value_list


def group_outputs(algorithm_aliases, outputs_list):
    grouped = groupby(outputs_list, key=lambda x: (
        x.solver, x.mtr, x.algorithm, x.randomization, x.normalization, x.cObjective, x.wAVB, x.wTT, x.wLength, x.wUtil,
        x.method, x.kspwlo_algorithm, x.kspwlo_threshold, x.k, x.ba, x.overload))

    grouped_results = dict()

    for key, group in grouped:
        k_results = dict()
        if logger.isEnabledFor(logging.DEBUG):
            logging.debug(key)

        group_sorted = natsorted(list(group), key=lambda x: x.topology_result.topology_name)

        if logger.isEnabledFor(logging.DEBUG):
            for each_group in group_sorted:
                logging.debug(each_group)

        new_key = prepare_key(algorithm_aliases, key)

        for each_group in group_sorted:
            if new_key not in k_results:
                k_results[new_key] = list()
                k_results[new_key].append(prepare_value(each_group))
            else:
                k_results[new_key].append(prepare_value(each_group))

        if key[13] not in grouped_results:
            grouped_results[key[13]] = list()
            grouped_results[key[13]].append(k_results)
        else:
            grouped_results[key[13]].append(k_results)

    return grouped_results


def sort_grouped_outputs(grouped_outputs):
    first_object = grouped_outputs.pop(None)

    sorted_dict = natsorted(grouped_outputs.items(), key=lambda x: x[0])

    new_dict = dict()
    new_dict[None] = first_object

    for key, value in sorted_dict:
        new_dict[key] = value

    return new_dict


def write_to_excel(wb, algorithm_aliases, sheets, output_list):
    grouped_outputs = group_outputs(algorithm_aliases, output_list)
    sorted_grouped_outputs = sort_grouped_outputs(grouped_outputs)

    for key, value in sorted_grouped_outputs.items():
        sorted_to_algorithm_aliases = sorted(value,
                                             key=lambda d: list(algorithm_aliases.values()).index(list(d.keys())[0]))
        sorted_grouped_outputs[key] = sorted_to_algorithm_aliases

    first_key = list(sorted_grouped_outputs.keys())[1]
    is_first_sheet = True
    for key, value in sorted_grouped_outputs.items():
        for sheet in sheets:
            if sheet == sheets[0]:
                if is_first_sheet:
                    new_sheet = wb.active
                    new_sheet.title = sheet + "=" + first_key
                    is_first_sheet = False
                else:
                    if sheet + "=" + key in wb.sheetnames:
                        new_sheet = wb[sheet + "=" + key]
                    else:
                        new_sheet = wb.create_sheet(title=sheet + "=" + key)

                max_column = new_sheet.max_column

                col = 0
                if max_column == 1:
                    col = 1
                else:
                    col += max_column + 1

                for output_dict in value:
                    for innerkey, innervalue in output_dict.items():
                        row = 1
                        new_sheet.cell(row=row, column=col + 1, value=innerkey)
                        row += 1
                        for result in innervalue:
                            column_number = 0
                            new_sheet.cell(row=row, column=col + column_number, value=result[0])
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[1]))
                            column_number += 1
                            row += 1

                        col += len(innervalue[0][:2])

            elif sheet == sheets[1]:
                if key is not None:
                    if sheet + "=" + key in wb.sheetnames:
                        new_sheet = wb[sheet + "=" + key]
                    else:
                        new_sheet = wb.create_sheet(title=sheet + "=" + key)
                else:
                    new_sheet = wb.create_sheet(title=sheet + "=" + first_key)

                max_column = new_sheet.max_column

                col = 0
                if max_column == 1:
                    col = 1
                else:
                    col += max_column + 1

                for output_dict in value:
                    for innerkey, innervalue in output_dict.items():
                        row = 1
                        new_sheet.cell(row=row, column=col + 1, value=innerkey)
                        row += 1
                        for result in innervalue:
                            column_number = 0
                            new_sheet.cell(row=row, column=col + column_number, value=result[0])
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[2]))
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[3]))
                            column_number += 1
                            row += 1

                        col += len(innervalue[0][2:4]) + 1

            elif sheet == sheets[2]:
                if key is not None:
                    if sheet + "=" + key in wb.sheetnames:
                        new_sheet = wb[sheet + "=" + key]
                    else:
                        new_sheet = wb.create_sheet(title=sheet + "=" + key)
                else:
                    new_sheet = wb.create_sheet(title=sheet + "=" + first_key)

                max_column = new_sheet.max_column

                col = 0
                if max_column == 1:
                    col = 1
                else:
                    col += max_column + 1

                for output_dict in value:
                    for innerkey, innervalue in output_dict.items():
                        row = 1
                        new_sheet.cell(row=row, column=col + 1, value=innerkey)
                        row += 1
                        for result in innervalue:
                            column_number = 0
                            new_sheet.cell(row=row, column=col + column_number, value=result[0])
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[4]))
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[5]))
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[6]))
                            column_number += 1
                            new_sheet.cell(row=row, column=col + column_number, value=float(result[7]))
                            column_number += 1
                            row += 1

                        col += len(innervalue[0][4:8]) + 1

    wb.save("output.xlsx")


def find_min_value_keys(d):
    # Find the minimum value in the dictionary
    min_value = min(d.values())

    # Find all keys that have the minimum value
    min_keys = [k for k, v in d.items() if v == min_value]

    # Create a dictionary with these keys and their values
    min_value_dict = {k: min_value for k in min_keys}

    return min_value_dict


def paint_cells(green_fill, yellow_fill, red_fill, workbook):
    i = 0
    for sheet in workbook.worksheets:
        if "O1-K" in sheet.title:
            j = 2
            for row in sheet.iter_rows(min_row=2):
                if i < 3:
                    topology_name_cell = row[0]

                    ro_cell = row[5]

                    mcdm_pp_cell = row[7]
                    mcdm_yen_cell = row[9]
                    # mcdm_mtr_yen_cell = row[11]
                    lwr_pp_cell = row[11]
                    lwr_yen_cell = row[13]
                    cwr_pp_cell = row[15]
                    cwr_yen_cell = row[17]
                    # lwr_mtr_yen_cell = row[21]
                    # lwr_mtr_pp_cell = row[23]
                    # cwr_mtr_yen_cell = row[25]
                    # cwr_mtr_pp_cell = row[27]
                    # mtr_v1_yen_cell = row[29]

                    ro_cell_value = float(ro_cell.value)

                    cell_value_dict = dict()

                    cell_value_dict[mcdm_pp_cell] = float(mcdm_pp_cell.value)
                    cell_value_dict[mcdm_yen_cell] = float(mcdm_yen_cell.value)
                    # cell_value_dict[mcdm_mtr_yen_cell] = float(mcdm_mtr_yen_cell.value)
                    cell_value_dict[lwr_pp_cell] = float(lwr_pp_cell.value)
                    cell_value_dict[lwr_yen_cell] = float(lwr_yen_cell.value)
                    cell_value_dict[cwr_pp_cell] = float(cwr_pp_cell.value)
                    cell_value_dict[cwr_yen_cell] = float(cwr_yen_cell.value)
                    # cell_value_dict[lwr_mtr_yen_cell] = float(lwr_mtr_yen_cell.value)
                    # cell_value_dict[lwr_mtr_pp_cell] = float(lwr_mtr_pp_cell.value)
                    # cell_value_dict[cwr_mtr_yen_cell] = float(cwr_mtr_yen_cell.value)
                    # cell_value_dict[cwr_mtr_pp_cell] = float(cwr_mtr_pp_cell.value)
                    # cell_value_dict[mtr_v1_yen_cell] = float(mtr_v1_yen_cell.value)

                    if logger.isEnabledFor(logging.DEBUG):
                        logging.debug(f"{sheet.title} {topology_name_cell.value} ro_cell {ro_cell_value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_pp_cell {mcdm_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_yen_cell {mcdm_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_mtr_yen_cell {mcdm_mtr_yen_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_pp_cell {lwr_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_yen_cell {lwr_yen_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_pp_cell {cwr_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_yen_cell {cwr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_yen_cell {lwr_mtr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_pp_cell {lwr_mtr_pp_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_mtr_yen_cell {cwr_mtr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_mtr_pp_cell {cwr_mtr_pp_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} mtr_v1_pp_cell {mtr_v1_yen_cell.value}")

                    min_value_keys_dict = find_min_value_keys(cell_value_dict)

                    for key, value in min_value_keys_dict.items():
                        if value < ro_cell_value:
                            key.fill = green_fill
                        elif value == ro_cell_value:
                            key.fill = yellow_fill
                        else:
                            key.fill = red_fill

                    ip_col = 2
                    if ro_cell_value != 0:
                        sheet.cell(row=1, column=17 + ip_col, value="ip_lwr_pp")
                        ip_lwr_pp = ((ro_cell_value - lwr_pp_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=17 + ip_col, value=float(ip_lwr_pp))

                        ip_col += 1

                        sheet.cell(row=1, column=17 + ip_col, value="ip_lwr_yen")
                        ip_lwr_yen = ((ro_cell_value - lwr_yen_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=17 + ip_col, value=float(ip_lwr_yen))

                        ip_col += 1

                        sheet.cell(row=1, column=17 + ip_col, value="ip_cwr_pp")
                        ip_cwr_pp = ((ro_cell_value - cwr_pp_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=17 + ip_col, value=float(ip_cwr_pp))

                        ip_col += 1

                        sheet.cell(row=1, column=17 + ip_col, value="ip_cwr_yen")
                        ip_cwr_yen = ((ro_cell_value - cwr_yen_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=17 + ip_col, value=float(ip_cwr_yen))

                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=29 + ip_col, value="ip_lwr_mtr_yen")
                        # ip_lwr_mtr_yen = ((ro_cell_value - lwr_mtr_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=29 + ip_col, value=float(ip_lwr_mtr_yen))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=29 + ip_col, value="ip_lwr_mtr_pp")
                        # ip_lwr_mtr_pp = ((ro_cell_value - lwr_mtr_pp_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=29 + ip_col, value=float(ip_lwr_mtr_pp))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=29 + ip_col, value="ip_cwr_mtr_yen")
                        # ip_cwr_mtr_yen = ((ro_cell_value - cwr_mtr_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=29 + ip_col, value=float(ip_cwr_mtr_yen))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=29 + ip_col, value="ip_cwr_mtr_pp")
                        # ip_cwr_mtr_pp = ((ro_cell_value - cwr_mtr_pp_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=29 + ip_col, value=float(ip_cwr_mtr_pp))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=29 + ip_col, value="ip_mtr_v1_yen")
                        # ip_mtr_v1_yen = ((ro_cell_value - mtr_v1_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=29 + ip_col, value=float(ip_mtr_v1_yen))
                        #
                        # ip_col += 1

                    j += 1

                else:
                    topology_name_cell = row[0]

                    ro_cell = row[3]

                    mcdm_pp_cell = row[5]
                    mcdm_yen_cell = row[7]
                    # mcdm_mtr_yen_cell = row[9]
                    lwr_pp_cell = row[9]
                    lwr_yen_cell = row[11]
                    cwr_pp_cell = row[13]
                    cwr_yen_cell = row[15]
                    # lwr_mtr_yen_cell = row[19]
                    # lwr_mtr_pp_cell = row[21]
                    # cwr_mtr_yen_cell = row[23]
                    # cwr_mtr_pp_cell = row[25]
                    # mtr_v1_yen_cell = row[27]

                    ro_cell_value = float(ro_cell.value)

                    cell_value_dict = dict()

                    cell_value_dict[mcdm_pp_cell] = float(mcdm_pp_cell.value)
                    cell_value_dict[mcdm_yen_cell] = float(mcdm_yen_cell.value)
                    # cell_value_dict[mcdm_mtr_yen_cell] = float(mcdm_mtr_yen_cell.value)
                    cell_value_dict[lwr_pp_cell] = float(lwr_pp_cell.value)
                    cell_value_dict[lwr_yen_cell] = float(lwr_yen_cell.value)
                    cell_value_dict[cwr_pp_cell] = float(cwr_pp_cell.value)
                    cell_value_dict[cwr_yen_cell] = float(cwr_yen_cell.value)
                    # cell_value_dict[lwr_mtr_yen_cell] = float(lwr_mtr_yen_cell.value)
                    # cell_value_dict[lwr_mtr_pp_cell] = float(lwr_mtr_pp_cell.value)
                    # cell_value_dict[cwr_mtr_yen_cell] = float(cwr_mtr_yen_cell.value)
                    # cell_value_dict[cwr_mtr_pp_cell] = float(cwr_mtr_pp_cell.value)
                    # cell_value_dict[mtr_v1_yen_cell] = float(mtr_v1_yen_cell.value)

                    if logger.isEnabledFor(logging.DEBUG):
                        logging.debug(f"{sheet.title} {topology_name_cell.value} ro_cell {ro_cell_value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_pp_cell {mcdm_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_yen_cell {mcdm_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_mtr_yen_cell {mcdm_mtr_yen_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_pp_cell {lwr_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_yen_cell {lwr_yen_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_pp_cell {cwr_pp_cell.value}")
                        logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_yen_cell {cwr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_yen_cell {lwr_mtr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_pp_cell {lwr_mtr_pp_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_mtr_yen_cell {cwr_mtr_yen_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_mtr_pp_cell {cwr_mtr_pp_cell.value}")
                        # logging.debug(f"{sheet.title} {topology_name_cell.value} mtr_v1_pp_cell {mtr_v1_yen_cell.value}")

                    min_value_keys_dict = find_min_value_keys(cell_value_dict)

                    for key, value in min_value_keys_dict.items():
                        if value < ro_cell_value:
                            key.fill = green_fill
                        elif value == ro_cell_value:
                            key.fill = yellow_fill
                        else:
                            key.fill = red_fill

                    ip_col = 2
                    if ro_cell_value != 0:
                        sheet.cell(row=1, column=15 + ip_col, value="ip_lwr_pp")
                        ip_lwr_pp = ((ro_cell_value - lwr_pp_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=15 + ip_col, value=float(ip_lwr_pp))

                        ip_col += 1

                        sheet.cell(row=1, column=15 + ip_col, value="ip_lwr_yen")
                        ip_lwr_yen = ((ro_cell_value - lwr_yen_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=15 + ip_col, value=float(ip_lwr_yen))

                        ip_col += 1

                        sheet.cell(row=1, column=15 + ip_col, value="ip_cwr_pp")
                        ip_cwr_pp = ((ro_cell_value - cwr_pp_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=15 + ip_col, value=float(ip_cwr_pp))

                        ip_col += 1

                        sheet.cell(row=1, column=15 + ip_col, value="ip_cwr_yen")
                        ip_cwr_yen = ((ro_cell_value - cwr_yen_cell.value) * 100) / ro_cell_value
                        sheet.cell(row=j, column=15 + ip_col, value=float(ip_cwr_yen))

                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=27 + ip_col, value="ip_lwr_mtr_yen")
                        # ip_lwr_mtr_yen = ((ro_cell_value - lwr_mtr_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=27 + ip_col, value=float(ip_lwr_mtr_yen))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=27 + ip_col, value="ip_lwr_mtr_pp")
                        # ip_lwr_mtr_pp = ((ro_cell_value - lwr_mtr_pp_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=27 + ip_col, value=float(ip_lwr_mtr_pp))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=27 + ip_col, value="ip_cwr_mtr_yen")
                        # ip_cwr_mtr_yen = ((ro_cell_value - cwr_mtr_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=27 + ip_col, value=float(ip_cwr_mtr_yen))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=27 + ip_col, value="ip_cwr_mtr_pp")
                        # ip_cwr_mtr_pp = ((ro_cell_value - cwr_mtr_pp_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=27 + ip_col, value=float(ip_cwr_mtr_pp))
                        #
                        # ip_col += 1
                        #
                        # sheet.cell(row=1, column=27 + ip_col, value="ip_mtr_v1_yen")
                        # ip_mtr_v1_yen = ((ro_cell_value - mtr_v1_yen_cell.value) * 100) / ro_cell_value
                        # sheet.cell(row=j, column=27 + ip_col, value=float(ip_mtr_v1_yen))
                        #
                        # ip_col += 1

                    j += 1

            i += 1

        if "O2-O3-K" in sheet.title:
            for row in sheet.iter_rows(min_row=2):
                pass
                # if i < 3:
                #     topology_name_cell = row[0]
                #
                #     ro_cell = row[8]
                #
                #     mcdm_pp_cell = row[11]
                #     mcdm_yen_cell = row[14]
                #     mcdm_mtr_yen_cell = row[17]
                #     lwr_pp_cell = row[17]
                #     lwr_yen_cell = row[20]
                #     cwr_pp_cell = row[23]
                #     cwr_yen_cell = row[26]
                #     lwr_mtr_yen_cell = row[29]
                #
                #     ro_cell_value = float(ro_cell.value)
                #
                #     cell_value_dict = dict()
                #
                #     cell_value_dict[mcdm_pp_cell] = float(mcdm_pp_cell.value)
                #     cell_value_dict[mcdm_yen_cell] = float(mcdm_yen_cell.value)
                #     cell_value_dict[mcdm_mtr_yen_cell] = float(mcdm_mtr_yen_cell.value)
                #     cell_value_dict[lwr_pp_cell] = float(lwr_pp_cell.value)
                #     cell_value_dict[lwr_yen_cell] = float(lwr_yen_cell.value)
                #     cell_value_dict[cwr_pp_cell] = float(cwr_pp_cell.value)
                #     cell_value_dict[cwr_yen_cell] = float(cwr_yen_cell.value)
                #     cell_value_dict[lwr_mtr_yen_cell] = float(lwr_mtr_yen_cell.value)
                #
                #     if logger.isEnabledFor(logging.DEBUG):
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_cell {ro_cell_value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_pp_cell {mcdm_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_yen_cell {mcdm_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_mtr_yen_cell {mcdm_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_pp_cell {lwr_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_yen_cell {lwr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_pp_cell {cwr_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_yen_cell {cwr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_yen_cell {lwr_mtr_yen_cell.value}")
                #
                #     min_value_keys_dict = find_min_value_keys(cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < ro_cell_value:
                #             key.fill = green_fill
                #         elif value == ro_cell_value:
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
                #
                # else:
                #     topology_name_cell = row[0]
                #
                #     ro_cell = row[5]
                #
                #     mcdm_pp_cell = row[8]
                #     mcdm_yen_cell = row[11]
                #     mcdm_mtr_yen_cell = row[14]
                #     lwr_pp_cell = row[17]
                #     lwr_yen_cell = row[20]
                #     cwr_pp_cell = row[23]
                #     cwr_yen_cell = row[26]
                #     lwr_mtr_yen_cell = row[29]
                #
                #     ro_cell_value = float(ro_cell.value)
                #
                #     cell_value_dict = dict()
                #
                #     cell_value_dict[mcdm_pp_cell] = float(mcdm_pp_cell.value)
                #     cell_value_dict[mcdm_yen_cell] = float(mcdm_yen_cell.value)
                #     cell_value_dict[mcdm_mtr_yen_cell] = float(mcdm_mtr_yen_cell.value)
                #     cell_value_dict[lwr_pp_cell] = float(lwr_pp_cell.value)
                #     cell_value_dict[lwr_yen_cell] = float(lwr_yen_cell.value)
                #     cell_value_dict[cwr_pp_cell] = float(cwr_pp_cell.value)
                #     cell_value_dict[cwr_yen_cell] = float(cwr_yen_cell.value)
                #     cell_value_dict[lwr_mtr_yen_cell] = float(lwr_mtr_yen_cell.value)
                #
                #     if logger.isEnabledFor(logging.DEBUG):
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_cell {ro_cell_value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_pp_cell {mcdm_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_yen_cell {mcdm_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_mtr_yen_cell {mcdm_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_pp_cell {lwr_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_yen_cell {lwr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_pp_cell {cwr_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_yen_cell {cwr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_mtr_yen_cell {lwr_mtr_yen_cell.value}")
                #
                #     min_value_keys_dict = find_min_value_keys(cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < ro_cell_value:
                #             key.fill = green_fill
                #         elif value == ro_cell_value:
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
            i += 1

        if "U-T-K" in sheet.title:
            for row in sheet.iter_rows(min_row=2):
                pass
                # if i < 3:
                #     topology_name_cell = row[0]
                #
                #     ro_max_util_cell = row[7]
                #     ro_time_cell = row[8]
                #
                #     mcdm_max_util_pp_cell = row[10]
                #     mcdm_time_pp_cell = row[11]
                #
                #     mcdm_max_util_yen_cell = row[13]
                #     mcdm_time_yen_cell = row[14]
                #
                #     mcdm_max_util_mtr_yen_cell = row[16]
                #     mcdm_time_mtr_yen_cell = row[17]
                #
                #     lwr_max_util_pp_cell = row[19]
                #     lwr_time_pp_cell = row[20]
                #
                #     lwr_max_util_yen_cell = row[22]
                #     lwr_time_yen_cell = row[23]
                #
                #     cwr_max_util_pp_cell = row[19]
                #     cwr_time_pp_cell = row[20]
                #
                #     cwr_max_util_yen_cell = row[22]
                #     cwr_time_yen_cell = row[23]
                #
                #     lwr_max_util_mtr_yen_cell = row[25]
                #     lwr_time_mtr_yen_cell = row[26]
                #
                #     max_util_cell_value_dict = dict()
                #
                #     max_util_cell_value_dict[mcdm_max_util_pp_cell] = float(mcdm_max_util_pp_cell.value)
                #     max_util_cell_value_dict[mcdm_max_util_yen_cell] = float(mcdm_max_util_yen_cell.value)
                #     max_util_cell_value_dict[mcdm_max_util_mtr_yen_cell] = float(mcdm_max_util_mtr_yen_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_pp_cell] = float(lwr_max_util_pp_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_yen_cell] = float(lwr_max_util_yen_cell.value)
                #     max_util_cell_value_dict[cwr_max_util_pp_cell] = float(cwr_max_util_pp_cell.value)
                #     max_util_cell_value_dict[cwr_max_util_yen_cell] = float(cwr_max_util_yen_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_mtr_yen_cell] = float(lwr_max_util_mtr_yen_cell.value)
                #
                #     min_value_keys_dict = find_min_value_keys(max_util_cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < float(ro_max_util_cell.value):
                #             key.fill = green_fill
                #         elif value == float(ro_max_util_cell.value):
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
                #
                #     time_cell_value_dict = dict()
                #
                #     time_cell_value_dict[mcdm_time_pp_cell] = float(mcdm_time_pp_cell.value)
                #     time_cell_value_dict[mcdm_time_yen_cell] = float(mcdm_time_yen_cell.value)
                #     time_cell_value_dict[mcdm_time_mtr_yen_cell] = float(mcdm_time_mtr_yen_cell.value)
                #     time_cell_value_dict[lwr_time_pp_cell] = float(lwr_time_pp_cell.value)
                #     time_cell_value_dict[lwr_time_yen_cell] = float(lwr_time_yen_cell.value)
                #     time_cell_value_dict[cwr_time_pp_cell] = float(cwr_time_pp_cell.value)
                #     time_cell_value_dict[cwr_time_yen_cell] = float(cwr_time_yen_cell.value)
                #     time_cell_value_dict[lwr_time_mtr_yen_cell] = float(lwr_time_mtr_yen_cell.value)
                #
                #     min_value_keys_dict = find_min_value_keys(time_cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < float(ro_time_cell.value):
                #             key.fill = green_fill
                #         elif value == float(ro_time_cell.value):
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
                #
                #     if logger.isEnabledFor(logging.DEBUG):
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_max_util_cell {ro_max_util_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_time_cell {ro_time_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_pp_cell {mcdm_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_pp_cell {mcdm_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_yen_cell {mcdm_max_util_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_yen_cell {mcdm_time_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_mtr_yen_cell {mcdm_max_util_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_mtr_yen_cell {mcdm_time_mtr_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_pp_cell {lwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_pp_cell {lwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_yen_cell {lwr_max_util_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_yen_cell {lwr_time_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_max_util_pp_cell {cwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_time_pp_cell {cwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_max_util_yen_cell {cwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_time_yen_cell {cwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_mtr_yen_cell {lwr_max_util_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_mtr_yen_cell {lwr_time_mtr_yen_cell.value}")
                #
                # else:
                #     topology_name_cell = row[0]
                #
                #     ro_max_util_cell = row[4]
                #     ro_time_cell = row[5]
                #
                #     mcdm_max_util_pp_cell = row[7]
                #     mcdm_time_pp_cell = row[8]
                #
                #     mcdm_max_util_yen_cell = row[10]
                #     mcdm_time_yen_cell = row[11]
                #
                #     mcdm_max_util_mtr_yen_cell = row[13]
                #     mcdm_time_mtr_yen_cell = row[14]
                #
                #     lwr_max_util_pp_cell = row[16]
                #     lwr_time_pp_cell = row[17]
                #
                #     lwr_max_util_yen_cell = row[19]
                #     lwr_time_yen_cell = row[20]
                #
                #     cwr_max_util_pp_cell = row[16]
                #     cwr_time_pp_cell = row[17]
                #
                #     cwr_max_util_yen_cell = row[19]
                #     cwr_time_yen_cell = row[20]
                #
                #     lwr_max_util_mtr_yen_cell = row[22]
                #     lwr_time_mtr_yen_cell = row[23]
                #
                #     max_util_cell_value_dict = dict()
                #
                #     max_util_cell_value_dict[mcdm_max_util_pp_cell] = float(mcdm_max_util_pp_cell.value)
                #     max_util_cell_value_dict[mcdm_max_util_yen_cell] = float(mcdm_max_util_yen_cell.value)
                #     max_util_cell_value_dict[mcdm_max_util_mtr_yen_cell] = float(mcdm_max_util_mtr_yen_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_pp_cell] = float(lwr_max_util_pp_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_yen_cell] = float(lwr_max_util_yen_cell.value)
                #     max_util_cell_value_dict[cwr_max_util_pp_cell] = float(cwr_max_util_pp_cell.value)
                #     max_util_cell_value_dict[cwr_max_util_yen_cell] = float(cwr_max_util_yen_cell.value)
                #     max_util_cell_value_dict[lwr_max_util_mtr_yen_cell] = float(lwr_max_util_mtr_yen_cell.value)
                #
                #     min_value_keys_dict = find_min_value_keys(max_util_cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < float(ro_max_util_cell.value):
                #             key.fill = green_fill
                #         elif value == float(ro_max_util_cell.value):
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
                #
                #     time_cell_value_dict = dict()
                #
                #     time_cell_value_dict[mcdm_time_pp_cell] = float(mcdm_time_pp_cell.value)
                #     time_cell_value_dict[mcdm_time_yen_cell] = float(mcdm_time_yen_cell.value)
                #     time_cell_value_dict[mcdm_time_mtr_yen_cell] = float(mcdm_time_mtr_yen_cell.value)
                #     time_cell_value_dict[lwr_time_pp_cell] = float(lwr_time_pp_cell.value)
                #     time_cell_value_dict[lwr_time_yen_cell] = float(lwr_time_yen_cell.value)
                #     time_cell_value_dict[cwr_time_pp_cell] = float(cwr_time_pp_cell.value)
                #     time_cell_value_dict[cwr_time_yen_cell] = float(cwr_time_yen_cell.value)
                #     time_cell_value_dict[lwr_time_mtr_yen_cell] = float(lwr_time_mtr_yen_cell.value)
                #
                #     min_value_keys_dict = find_min_value_keys(time_cell_value_dict)
                #
                #     for key, value in min_value_keys_dict.items():
                #         if value < float(ro_time_cell.value):
                #             key.fill = green_fill
                #         elif value == float(ro_time_cell.value):
                #             key.fill = yellow_fill
                #         else:
                #             key.fill = red_fill
                #
                #     if logger.isEnabledFor(logging.DEBUG):
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_max_util_cell {ro_max_util_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} ro_time_cell {ro_time_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_pp_cell {mcdm_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_pp_cell {mcdm_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_yen_cell {mcdm_max_util_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_yen_cell {mcdm_time_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_max_util_mtr_yen_cell {mcdm_max_util_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} mcdm_time_mtr_yen_cell {mcdm_time_mtr_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_pp_cell {lwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_pp_cell {lwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_yen_cell {lwr_max_util_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_yen_cell {lwr_time_yen_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_max_util_pp_cell {cwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_time_pp_cell {cwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_max_util_yen_cell {cwr_max_util_pp_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} cwr_time_yen_cell {cwr_time_pp_cell.value}")
                #
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_max_util_mtr_yen_cell {lwr_max_util_mtr_yen_cell.value}")
                #         logging.debug(f"{sheet.title} {topology_name_cell.value} lwr_time_mtr_yen_cell {lwr_time_mtr_yen_cell.value}")

            i += 1

    workbook.save("outputs_colored.xlsx")


def main():
    green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFFF00", end_color="00FF00", fill_type="solid")
    red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

    wb = openpyxl.Workbook()

    project = "tsncf-for_article"

    algorithm_aliases = dict()

    algorithm_aliases["shortestpath_dijkstra"] = "Dijkstra"
    algorithm_aliases["U_yen"] = "KSPU"
    algorithm_aliases["GRASP_yen"] = "RO"
    algorithm_aliases["WSM_pp"] = "WSM_pp"
    algorithm_aliases["WSM_yen"] = "WSM_yen"
    # algorithm_aliases["CD_v1c_yen"] = "MCDM_mtr_yen"
    algorithm_aliases["GRASPCD_pp"] = "LWR_pp"
    algorithm_aliases["GRASPCD_yen"] = "LWR_yen"
    algorithm_aliases["GRASPRandomCD_pp"] = "CWR_pp"
    algorithm_aliases["GRASPRandomCD_yen"] = "CWR_yen"
    # algorithm_aliases["GRASPCD_v1c_yen"] = "LWR_mtr_yen"
    # algorithm_aliases["GRASPCD_v1c_pp"] = "LWR_mtr_pp"
    # algorithm_aliases["GRASPRandomCD_v1c_yen"] = "CWR_mtr_yen"
    # algorithm_aliases["GRASPRandomCD_v1c_pp"] = "CWR_mtr_pp"
    # algorithm_aliases["GRASP_v1_yen"] = "mtr_v1_yen"

    sheets = ["O1-K", "O2-O3-K", "U-T-K"]
    output_list = read_outputs(logger, project)

    write_to_excel(wb, algorithm_aliases, sheets, output_list)

    # workbook = load_workbook("output.xlsx")
    #
    # paint_cells(green_fill, yellow_fill, red_fill, workbook)


if __name__ == "__main__":
    main()
