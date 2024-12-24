import os
import re
import logging

from natsort import natsorted

from result_holder import ResultHolder
from topology_and_result_holder import TopologyResult


def get_max_util(line):
    match = re.search(r'Max Loaded Link Utilization: (\d+\.\d+)', line)

    if match:
        utilization_value = float(match.group(1))
        formatted_value = "{:.2f}".format(utilization_value)
        return formatted_value


def get_average(line):
    match = re.search(r'Average Link Utilization: (\d+\.\d+)', line)

    if match:
        utilization_value = float(match.group(1))
        formatted_value = "{:.3f}".format(utilization_value)
        return formatted_value


def get_variance(line):
    match = re.search(r'Variance: (\d+\.\d+)', line)

    if match:
        utilization_value = float(match.group(1))
        formatted_value = "{:.3f}".format(utilization_value)
        return formatted_value


def get_time(line):
    match = re.search(r'{\d+\.\d+=(\d+\.\d+)', line)

    if match:
        extracted_value = float(match.group(1))
        formatted_value = "{:.2f}".format(extracted_value)
        return formatted_value


def parse_result_line(lines):
    topology_name = lines[0].strip()

    values = ["{:.2f}".format(float(line.split('=')[-1].strip().replace(',', ''))) for line in lines[1].split(',')]

    o1 = values[1:][0]
    o2 = values[1:][1]
    o3 = values[1:][2]

    max_util = get_max_util(lines[3])
    average = get_average(lines[3])
    variance = get_variance(lines[3])

    time = get_time(lines[4])

    topology_result = TopologyResult(topology_name, o1, o2, o3, max_util, average, variance, time)

    return topology_result


def create_result(result_file_path):
    topology_result_list = list()

    with open(os.path.join(result_file_path, "Results.txt"), 'r') as result_file:
        lines = result_file.readlines()

        for i in range(0, len(lines), 5):
            topology_lines = lines[i:i + 5]
            topology_result = parse_result_line(topology_lines)

            topology_result_list.append(topology_result)

    return topology_result_list


def read_outputs(logger, project):
    outputs_list = list()

    solvers_path = os.path.join(os.path.expanduser("~"), project, "outputs")
    solvers = os.listdir(solvers_path)

    for solver in solvers:
        if solver == "phy":
            algorithm_path = os.path.join(solvers_path, solver)
            algorithms = os.listdir(algorithm_path)
            for algorithm in algorithms:
                if "C" == algorithm or "CD" == algorithm or "CDST" == algorithm or "CDSTV2" == algorithm:
                    normalization_path = os.path.join(algorithm_path, algorithm)
                    normalizations = os.listdir(normalization_path)

                    for normalization in normalizations:
                        c_objective_path = os.path.join(normalization_path, normalization)
                        c_objectives = os.listdir(c_objective_path)

                        for c_objective in c_objectives:
                            w_avb_path = os.path.join(c_objective_path, c_objective)
                            w_avbs = os.listdir(w_avb_path)

                            for w_avb in w_avbs:
                                w_tt_path = os.path.join(w_avb_path, w_avb)
                                w_tts = os.listdir(w_tt_path)

                                for w_tt in w_tts:
                                    w_length_path = os.path.join(w_tt_path, w_tt)
                                    w_lengths = os.listdir(w_length_path)

                                    for w_length in w_lengths:
                                        w_util_path = os.path.join(w_length_path, w_length)
                                        w_utils = os.listdir(w_util_path)

                                        for w_util in w_utils:
                                            method_path = os.path.join(w_util_path, w_util)
                                            methods = os.listdir(method_path)

                                            for method in methods:
                                                if "kspwlo" not in method:
                                                    k_path = os.path.join(method_path, method)
                                                    ks = natsorted(os.listdir(k_path))

                                                    for k in ks:
                                                        ba_path = os.path.join(k_path, k)

                                                        try:
                                                            bas = os.listdir(ba_path)
                                                        except:
                                                            continue

                                                        for ba in bas:
                                                            overload_or_topology_path = os.path.join(ba_path, ba)
                                                            overload_or_topology = os.listdir(overload_or_topology_path)

                                                            if "overload" in overload_or_topology:
                                                                overload = "overload"

                                                                result_file_path = os.path.join(
                                                                    overload_or_topology_path,
                                                                    overload)

                                                                topology_result_list = create_result(
                                                                    result_file_path)

                                                                for topology_result in topology_result_list:

                                                                    rh = ResultHolder()
                                                                    rh.set_solver(solver)
                                                                    rh.set_mtr(None)
                                                                    rh.set_algorithm(algorithm)
                                                                    rh.set_randomization(None)
                                                                    rh.set_normalization(normalization)
                                                                    rh.set_cObjective(c_objective)
                                                                    rh.set_wAVB(w_avb)
                                                                    rh.set_wTT(w_tt)
                                                                    rh.set_wLength(w_length)
                                                                    rh.set_wUtil(w_util)
                                                                    rh.set_method(method)
                                                                    rh.set_kspwlo_algorithm(None)
                                                                    rh.set_kspwlo_threshold(None)
                                                                    rh.set_k(k)
                                                                    rh.set_ba(ba)
                                                                    rh.set_overload(overload)
                                                                    rh.set_topology_result(topology_result)
                                                                    outputs_list.append(rh)

                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                        logging.debug(rh.__str__())

                                                            else:
                                                                topology_result_list = create_result(
                                                                    overload_or_topology_path)

                                                                for topology_result in topology_result_list:

                                                                    rh = ResultHolder()
                                                                    rh.set_solver(solver)
                                                                    rh.set_mtr(None)
                                                                    rh.set_algorithm(algorithm)
                                                                    rh.set_randomization(None)
                                                                    rh.set_normalization(normalization)
                                                                    rh.set_cObjective(c_objective)
                                                                    rh.set_wAVB(w_avb)
                                                                    rh.set_wTT(w_tt)
                                                                    rh.set_wLength(w_length)
                                                                    rh.set_wUtil(w_util)
                                                                    rh.set_method(method)
                                                                    rh.set_kspwlo_algorithm(None)
                                                                    rh.set_kspwlo_threshold(None)
                                                                    rh.set_k(k)
                                                                    rh.set_ba(ba)
                                                                    rh.set_overload(None)
                                                                    rh.set_topology_result(
                                                                        topology_result)
                                                                    outputs_list.append(rh)

                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                        logging.debug(rh.__str__())

                                                else:
                                                    kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                                                    kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                                    for kspwlo_algorithm in kspwlo_algorithms:
                                                        threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                                      kspwlo_algorithm)
                                                        thresholds = os.listdir(threshold_path)

                                                        for threshold in thresholds:
                                                            k_path = os.path.join(method_path, method)
                                                            ks = natsorted(os.listdir(k_path))

                                                            for k in ks:
                                                                ba_path = os.path.join(k_path, k)

                                                                try:
                                                                    bas = os.listdir(ba_path)
                                                                except:
                                                                    continue

                                                                for ba in bas:
                                                                    overload_or_topology_path = os.path.join(
                                                                        ba_path,
                                                                        ba)
                                                                    overload_or_topology = os.listdir(
                                                                        overload_or_topology_path)

                                                                    if "overload" in overload_or_topology:
                                                                        overload = "overload"

                                                                        result_file_path = os.path.join(
                                                                            overload_or_topology_path, overload)

                                                                        topology_result_list = create_result(
                                                                            result_file_path)

                                                                        for topology_result in topology_result_list:

                                                                            rh = ResultHolder()
                                                                            rh.set_solver(solver)
                                                                            rh.set_mtr(None)
                                                                            rh.set_algorithm(algorithm)
                                                                            rh.set_randomization(None)
                                                                            rh.set_normalization(normalization)
                                                                            rh.set_cObjective(c_objective)
                                                                            rh.set_wAVB(w_avb)
                                                                            rh.set_wTT(w_tt)
                                                                            rh.set_wLength(w_length)
                                                                            rh.set_wUtil(w_util)
                                                                            rh.set_method(method)
                                                                            rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                            rh.set_kspwlo_threshold(threshold)
                                                                            rh.set_k(k)
                                                                            rh.set_ba(ba)
                                                                            rh.set_overload(overload)
                                                                            rh.set_topology_result(
                                                                                topology_result)
                                                                            outputs_list.append(rh)

                                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                                logging.debug(rh.__str__())

                                                                    else:
                                                                        topology_result_list = create_result(
                                                                            overload_or_topology_path)

                                                                        for topology_result in topology_result_list:

                                                                            rh = ResultHolder()
                                                                            rh.set_solver(solver)
                                                                            rh.set_mtr(None)
                                                                            rh.set_algorithm(algorithm)
                                                                            rh.set_randomization(None)
                                                                            rh.set_normalization(normalization)
                                                                            rh.set_cObjective(c_objective)
                                                                            rh.set_wAVB(w_avb)
                                                                            rh.set_wTT(w_tt)
                                                                            rh.set_wLength(w_length)
                                                                            rh.set_wUtil(w_util)
                                                                            rh.set_method(method)
                                                                            rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                            rh.set_kspwlo_threshold(threshold)
                                                                            rh.set_k(k)
                                                                            rh.set_ba(ba)
                                                                            rh.set_overload(None)
                                                                            rh.set_topology_result(
                                                                                topology_result)
                                                                            outputs_list.append(rh)

                                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                                logging.debug(rh.__str__())
                elif "C" in algorithm or "CD" in algorithm or "CDST" in algorithm or "CDSTV2" in algorithm:
                    if "Random" not in algorithm:
                        randomization_path = os.path.join(algorithm_path, algorithm)
                        randomizations = os.listdir(randomization_path)

                        for randomization in randomizations:
                            normalization_path = os.path.join(randomization_path, randomization)
                            normalizations = os.listdir(normalization_path)

                            for normalization in normalizations:
                                c_objective_path = os.path.join(normalization_path, normalization)
                                c_objectives = os.listdir(c_objective_path)

                                for c_objective in c_objectives:
                                    w_avb_path = os.path.join(c_objective_path, c_objective)
                                    w_avbs = os.listdir(w_avb_path)

                                    for w_avb in w_avbs:
                                        w_tt_path = os.path.join(w_avb_path, w_avb)
                                        w_tts = os.listdir(w_tt_path)

                                        for w_tt in w_tts:
                                            w_length_path = os.path.join(w_tt_path, w_tt)
                                            w_lengths = os.listdir(w_length_path)

                                            for w_length in w_lengths:
                                                w_util_path = os.path.join(w_length_path, w_length)
                                                w_utils = os.listdir(w_util_path)

                                                for w_util in w_utils:
                                                    method_path = os.path.join(w_util_path, w_util)
                                                    methods = os.listdir(method_path)

                                                    for method in methods:
                                                        if "kspwlo" not in method:
                                                            k_path = os.path.join(method_path, method)
                                                            ks = natsorted(os.listdir(k_path))

                                                            for k in ks:
                                                                ba_path = os.path.join(k_path, k)

                                                                try:
                                                                    bas = os.listdir(ba_path)
                                                                except:
                                                                    continue

                                                                for ba in bas:
                                                                    overload_or_topology_path = os.path.join(ba_path, ba)
                                                                    overload_or_topology = os.listdir(overload_or_topology_path)

                                                                    if "overload" in overload_or_topology:
                                                                        overload = "overload"

                                                                        result_file_path = os.path.join(
                                                                            overload_or_topology_path,
                                                                            overload)

                                                                        topology_result_list = create_result(
                                                                            result_file_path)

                                                                        for topology_result in topology_result_list:

                                                                            rh = ResultHolder()
                                                                            rh.set_solver(solver)
                                                                            rh.set_mtr(None)
                                                                            rh.set_algorithm(algorithm)
                                                                            rh.set_randomization(randomization)
                                                                            rh.set_normalization(normalization)
                                                                            rh.set_cObjective(c_objective)
                                                                            rh.set_wAVB(w_avb)
                                                                            rh.set_wTT(w_tt)
                                                                            rh.set_wLength(w_length)
                                                                            rh.set_wUtil(w_util)
                                                                            rh.set_method(method)
                                                                            rh.set_kspwlo_algorithm(None)
                                                                            rh.set_kspwlo_threshold(None)
                                                                            rh.set_k(k)
                                                                            rh.set_ba(ba)
                                                                            rh.set_overload(overload)
                                                                            rh.set_topology_result(topology_result)
                                                                            outputs_list.append(rh)

                                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                                logging.debug(rh.__str__())

                                                                    else:
                                                                        topology_result_list = create_result(
                                                                            overload_or_topology_path)

                                                                        for topology_result in topology_result_list:

                                                                            rh = ResultHolder()
                                                                            rh.set_solver(solver)
                                                                            rh.set_mtr(None)
                                                                            rh.set_algorithm(algorithm)
                                                                            rh.set_randomization(randomization)
                                                                            rh.set_normalization(normalization)
                                                                            rh.set_cObjective(c_objective)
                                                                            rh.set_wAVB(w_avb)
                                                                            rh.set_wTT(w_tt)
                                                                            rh.set_wLength(w_length)
                                                                            rh.set_wUtil(w_util)
                                                                            rh.set_method(method)
                                                                            rh.set_kspwlo_algorithm(None)
                                                                            rh.set_kspwlo_threshold(None)
                                                                            rh.set_k(k)
                                                                            rh.set_ba(ba)
                                                                            rh.set_overload(None)
                                                                            rh.set_topology_result(
                                                                                topology_result)
                                                                            outputs_list.append(rh)

                                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                                logging.debug(rh.__str__())

                                                        else:
                                                            kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                                                            kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                                            for kspwlo_algorithm in kspwlo_algorithms:
                                                                threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                                              kspwlo_algorithm)
                                                                thresholds = os.listdir(threshold_path)

                                                                for threshold in thresholds:
                                                                    k_path = os.path.join(method_path, method)
                                                                    ks = natsorted(os.listdir(k_path))

                                                                    for k in ks:
                                                                        ba_path = os.path.join(k_path, k)

                                                                        try:
                                                                            bas = os.listdir(ba_path)
                                                                        except:
                                                                            continue

                                                                        for ba in bas:
                                                                            overload_or_topology_path = os.path.join(
                                                                                ba_path,
                                                                                ba)
                                                                            overload_or_topology = os.listdir(
                                                                                overload_or_topology_path)

                                                                            if "overload" in overload_or_topology:
                                                                                overload = "overload"

                                                                                result_file_path = os.path.join(
                                                                                    overload_or_topology_path, overload)

                                                                                topology_result_list = create_result(
                                                                                    result_file_path)

                                                                                for topology_result in topology_result_list:

                                                                                    rh = ResultHolder()
                                                                                    rh.set_solver(solver)
                                                                                    rh.set_mtr(None)
                                                                                    rh.set_algorithm(algorithm)
                                                                                    rh.set_randomization(randomization)
                                                                                    rh.set_normalization(normalization)
                                                                                    rh.set_cObjective(c_objective)
                                                                                    rh.set_wAVB(w_avb)
                                                                                    rh.set_wTT(w_tt)
                                                                                    rh.set_wLength(w_length)
                                                                                    rh.set_wUtil(w_util)
                                                                                    rh.set_method(method)
                                                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                                    rh.set_kspwlo_threshold(threshold)
                                                                                    rh.set_k(k)
                                                                                    rh.set_ba(ba)
                                                                                    rh.set_overload(overload)
                                                                                    rh.set_topology_result(
                                                                                        topology_result)
                                                                                    outputs_list.append(rh)

                                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                                        logging.debug(rh.__str__())

                                                                            else:
                                                                                topology_result_list = create_result(
                                                                                    overload_or_topology_path)

                                                                                for topology_result in topology_result_list:

                                                                                    rh = ResultHolder()
                                                                                    rh.set_solver(solver)
                                                                                    rh.set_mtr(None)
                                                                                    rh.set_algorithm(algorithm)
                                                                                    rh.set_randomization(randomization)
                                                                                    rh.set_normalization(normalization)
                                                                                    rh.set_cObjective(c_objective)
                                                                                    rh.set_wAVB(w_avb)
                                                                                    rh.set_wTT(w_tt)
                                                                                    rh.set_wLength(w_length)
                                                                                    rh.set_wUtil(w_util)
                                                                                    rh.set_method(method)
                                                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                                    rh.set_kspwlo_threshold(threshold)
                                                                                    rh.set_k(k)
                                                                                    rh.set_ba(ba)
                                                                                    rh.set_overload(None)
                                                                                    rh.set_topology_result(
                                                                                        topology_result)
                                                                                    outputs_list.append(rh)

                                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                                        logging.debug(rh.__str__())
                    else:
                        randomization_path = os.path.join(algorithm_path, algorithm)
                        randomizations = os.listdir(randomization_path)

                        for randomization in randomizations:
                            normalization_path = os.path.join(randomization_path, randomization)
                            normalizations = os.listdir(normalization_path)

                            for normalization in normalizations:
                                c_objective_path = os.path.join(normalization_path, normalization)
                                c_objectives = os.listdir(c_objective_path)

                                for c_objective in c_objectives:
                                    method_path = os.path.join(c_objective_path, c_objective)
                                    methods = os.listdir(method_path)

                                    for method in methods:
                                        if "kspwlo" not in method:
                                            k_path = os.path.join(method_path, method)
                                            ks = natsorted(os.listdir(k_path))

                                            for k in ks:
                                                ba_path = os.path.join(k_path, k)

                                                try:
                                                    bas = os.listdir(ba_path)
                                                except:
                                                    continue

                                                for ba in bas:
                                                    overload_or_topology_path = os.path.join(ba_path, ba)
                                                    overload_or_topology = os.listdir(
                                                        overload_or_topology_path)

                                                    if "overload" in overload_or_topology:
                                                        overload = "overload"

                                                        result_file_path = os.path.join(
                                                            overload_or_topology_path,
                                                            overload)

                                                        topology_result_list = create_result(result_file_path)

                                                        for topology_result in topology_result_list:

                                                            rh = ResultHolder()
                                                            rh.set_solver(solver)
                                                            rh.set_mtr(None)
                                                            rh.set_algorithm(algorithm)
                                                            rh.set_randomization(randomization)
                                                            rh.set_normalization(normalization)
                                                            rh.set_cObjective(c_objective)
                                                            rh.set_wAVB(None)
                                                            rh.set_wTT(None)
                                                            rh.set_wLength(None)
                                                            rh.set_wUtil(None)
                                                            rh.set_method(method)
                                                            rh.set_kspwlo_algorithm(None)
                                                            rh.set_kspwlo_threshold(None)
                                                            rh.set_k(k)
                                                            rh.set_ba(ba)
                                                            rh.set_overload(overload)
                                                            rh.set_topology_result(topology_result)
                                                            outputs_list.append(rh)

                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                logging.debug(rh.__str__())

                                                    else:
                                                        topology_result_list = create_result(overload_or_topology_path)

                                                        for topology_result in topology_result_list:

                                                            rh = ResultHolder()
                                                            rh.set_solver(solver)
                                                            rh.set_mtr(None)
                                                            rh.set_algorithm(algorithm)
                                                            rh.set_randomization(randomization)
                                                            rh.set_normalization(normalization)
                                                            rh.set_cObjective(c_objective)
                                                            rh.set_wAVB(None)
                                                            rh.set_wTT(None)
                                                            rh.set_wLength(None)
                                                            rh.set_wUtil(None)
                                                            rh.set_method(method)
                                                            rh.set_kspwlo_algorithm(None)
                                                            rh.set_kspwlo_threshold(None)
                                                            rh.set_k(k)
                                                            rh.set_ba(ba)
                                                            rh.set_overload(None)
                                                            rh.set_topology_result(topology_result)
                                                            outputs_list.append(rh)

                                                            if logger.isEnabledFor(logging.DEBUG):
                                                                logging.debug(rh.__str__())
                                        else:
                                            kspwlo_algorithm_path = os.path.join(algorithm_path,
                                                                                 algorithm)
                                            kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                            for kspwlo_algorithm in kspwlo_algorithms:
                                                threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                              kspwlo_algorithm)
                                                thresholds = os.listdir(threshold_path)

                                                for threshold in thresholds:
                                                    k_path = os.path.join(method_path, method)
                                                    ks = natsorted(os.listdir(k_path))

                                                    for k in ks:
                                                        ba_path = os.path.join(k_path, k)

                                                        try:
                                                            bas = os.listdir(ba_path)
                                                        except:
                                                            continue

                                                        for ba in bas:
                                                            overload_or_topology_path = os.path.join(
                                                                ba_path,
                                                                ba)
                                                            overload_or_topology = os.listdir(
                                                                overload_or_topology_path)

                                                            if "overload" in overload_or_topology:
                                                                overload = "overload"

                                                                result_file_path = os.path.join(
                                                                    overload_or_topology_path, overload)

                                                                topology_result_list = create_result(result_file_path)

                                                                for topology_result in topology_result_list:

                                                                    rh = ResultHolder()
                                                                    rh.set_solver(solver)
                                                                    rh.set_mtr(None)
                                                                    rh.set_algorithm(algorithm)
                                                                    rh.set_randomization(randomization)
                                                                    rh.set_normalization(normalization)
                                                                    rh.set_cObjective(c_objective)
                                                                    rh.set_wAVB(None)
                                                                    rh.set_wTT(None)
                                                                    rh.set_wLength(None)
                                                                    rh.set_wUtil(None)
                                                                    rh.set_method(method)
                                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                    rh.set_kspwlo_threshold(threshold)
                                                                    rh.set_k(k)
                                                                    rh.set_ba(ba)
                                                                    rh.set_overload(overload)
                                                                    rh.set_topology_result(topology_result)
                                                                    outputs_list.append(rh)

                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                        logging.debug(rh.__str__())

                                                            else:
                                                                topology_result_list = create_result(overload_or_topology_path)

                                                                for topology_result in topology_result_list:

                                                                    rh = ResultHolder()
                                                                    rh.set_solver(solver)
                                                                    rh.set_mtr(None)
                                                                    rh.set_algorithm(algorithm)
                                                                    rh.set_randomization(randomization)
                                                                    rh.set_normalization(normalization)
                                                                    rh.set_cObjective(c_objective)
                                                                    rh.set_wAVB(None)
                                                                    rh.set_wTT(None)
                                                                    rh.set_wLength(None)
                                                                    rh.set_wUtil(None)
                                                                    rh.set_method(method)
                                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                    rh.set_kspwlo_threshold(threshold)
                                                                    rh.set_k(k)
                                                                    rh.set_ba(ba)
                                                                    rh.set_overload(None)
                                                                    rh.set_topology_result(topology_result)
                                                                    outputs_list.append(rh)

                                                                    if logger.isEnabledFor(logging.DEBUG):
                                                                        logging.debug(rh.__str__())
                elif "shortestpath" == algorithm:
                    method_path = os.path.join(algorithm_path, algorithm)
                    methods = os.listdir(method_path)

                    for method in methods:
                        ba_path = os.path.join(method_path, method)
                        bas = os.listdir(ba_path)

                        for ba in bas:
                            overload_or_topology_path = os.path.join(ba_path, ba)
                            overload_or_topology = os.listdir(overload_or_topology_path)

                            if "overload" in overload_or_topology:
                                overload = "overload"

                                result_file_path = os.path.join(overload_or_topology_path, overload)

                                topology_result_list = create_result(result_file_path)

                                for topology_result in topology_result_list:

                                    rh = ResultHolder()
                                    rh.set_solver(solver)
                                    rh.set_mtr(None)
                                    rh.set_algorithm(algorithm)
                                    rh.set_randomization(None)
                                    rh.set_normalization(None)
                                    rh.set_cObjective(None)
                                    rh.set_wAVB(None)
                                    rh.set_wTT(None)
                                    rh.set_wLength(None)
                                    rh.set_wUtil(None)
                                    rh.set_method(method)
                                    rh.set_kspwlo_algorithm(None)
                                    rh.set_kspwlo_threshold(None)
                                    rh.set_k(None)
                                    rh.set_ba(ba)
                                    rh.set_overload(overload)
                                    rh.set_topology_result(topology_result)
                                    outputs_list.append(rh)

                                    if logger.isEnabledFor(logging.DEBUG):
                                        logging.debug(rh.__str__())

                            else:

                                topology_result_list = create_result(overload_or_topology_path)

                                for topology_result in topology_result_list:

                                    rh = ResultHolder()
                                    rh.set_solver(solver)
                                    rh.set_mtr(None)
                                    rh.set_algorithm(algorithm)
                                    rh.set_randomization(None)
                                    rh.set_normalization(None)
                                    rh.set_cObjective(None)
                                    rh.set_wAVB(None)
                                    rh.set_wTT(None)
                                    rh.set_wLength(None)
                                    rh.set_wUtil(None)
                                    rh.set_method(method)
                                    rh.set_kspwlo_algorithm(None)
                                    rh.set_kspwlo_threshold(None)
                                    rh.set_k(None)
                                    rh.set_ba(ba)
                                    rh.set_overload(None)
                                    rh.set_topology_result(topology_result)
                                    outputs_list.append(rh)

                                    if logger.isEnabledFor(logging.DEBUG):
                                        logging.debug(rh.__str__()) 
                else:
                    method_path = os.path.join(algorithm_path, algorithm)
                    methods = os.listdir(method_path)
                    for method in methods:
                        if "kspwlo" not in method:
                            k_or_ba_path = os.path.join(method_path, method)
                            k_or_bas = os.listdir(k_or_ba_path)

                            try:
                                k_path = os.path.join(method_path, method)
                                ks = natsorted(os.listdir(k_path))

                                for k in ks:
                                    ba_path = os.path.join(k_path, k)

                                    try:
                                        bas = os.listdir(ba_path)
                                    except:
                                        continue

                                    for ba in bas:
                                        overload_or_topology_path = os.path.join(ba_path, ba)
                                        overload_or_topology = os.listdir(overload_or_topology_path)

                                        if "overload" in overload_or_topology:
                                            overload = "overload"

                                            result_file_path = os.path.join(overload_or_topology_path, overload)

                                            topology_result_list = create_result(
                                                result_file_path)

                                            for topology_result in topology_result_list:

                                                rh = ResultHolder()
                                                rh.set_solver(solver)
                                                rh.set_mtr(None)
                                                rh.set_algorithm(algorithm)
                                                rh.set_randomization(None)
                                                rh.set_normalization(None)
                                                rh.set_cObjective(None)
                                                rh.set_wAVB(None)
                                                rh.set_wTT(None)
                                                rh.set_wLength(None)
                                                rh.set_wUtil(None)
                                                rh.set_method(method)
                                                rh.set_kspwlo_algorithm(None)
                                                rh.set_kspwlo_threshold(None)
                                                rh.set_k(k)
                                                rh.set_ba(ba)
                                                rh.set_overload(overload)
                                                rh.set_topology_result(topology_result)
                                                outputs_list.append(rh)

                                                if logger.isEnabledFor(logging.DEBUG):
                                                    logging.debug(rh.__str__())

                                        else:
                                            topology_result_list = create_result(
                                                overload_or_topology_path)

                                            for topology_result in topology_result_list:

                                                rh = ResultHolder()
                                                rh.set_solver(solver)
                                                rh.set_mtr(None)
                                                rh.set_algorithm(algorithm)
                                                rh.set_randomization(None)
                                                rh.set_normalization(None)
                                                rh.set_cObjective(None)
                                                rh.set_wAVB(None)
                                                rh.set_wTT(None)
                                                rh.set_wLength(None)
                                                rh.set_wUtil(None)
                                                rh.set_method(method)
                                                rh.set_kspwlo_algorithm(None)
                                                rh.set_kspwlo_threshold(None)
                                                rh.set_k(k)
                                                rh.set_ba(ba)
                                                rh.set_overload(None)
                                                rh.set_topology_result(topology_result)
                                                outputs_list.append(rh)

                                                if logger.isEnabledFor(logging.DEBUG):
                                                    logging.debug(rh.__str__())

                            except ValueError:
                                for ba in k_or_bas:
                                    overload_or_topology_path = os.path.join(k_or_ba_path, ba)
                                    overload_or_topology = os.listdir(overload_or_topology_path)

                                    if "overload" in overload_or_topology:
                                        overload = "overload"

                                        result_file_path = os.path.join(overload_or_topology_path, overload)

                                        topology_result_list = create_result(
                                            result_file_path)

                                        for topology_result in topology_result_list:

                                            rh = ResultHolder()
                                            rh.set_solver(solver)
                                            rh.set_mtr(None)
                                            rh.set_algorithm(algorithm)
                                            rh.set_randomization(None)
                                            rh.set_normalization(None)
                                            rh.set_cObjective(None)
                                            rh.set_wAVB(None)
                                            rh.set_wTT(None)
                                            rh.set_wLength(None)
                                            rh.set_wUtil(None)
                                            rh.set_method(method)
                                            rh.set_kspwlo_algorithm(None)
                                            rh.set_kspwlo_threshold(None)
                                            rh.set_k(None)
                                            rh.set_ba(ba)
                                            rh.set_overload(overload)
                                            rh.set_topology_result(topology_result)
                                            outputs_list.append(rh)

                                            if logger.isEnabledFor(logging.DEBUG):
                                                logging.debug(rh.__str__())

                                    else:
                                        topology_result_list = create_result(
                                            overload_or_topology_path)

                                        for topology_result in topology_result_list:

                                            rh = ResultHolder()
                                            rh.set_solver(solver)
                                            rh.set_mtr(None)
                                            rh.set_algorithm(algorithm)
                                            rh.set_randomization(None)
                                            rh.set_normalization(None)
                                            rh.set_cObjective(None)
                                            rh.set_wAVB(None)
                                            rh.set_wTT(None)
                                            rh.set_wLength(None)
                                            rh.set_wUtil(None)
                                            rh.set_method(method)
                                            rh.set_kspwlo_algorithm(None)
                                            rh.set_kspwlo_threshold(None)
                                            rh.set_k(None)
                                            rh.set_ba(ba)
                                            rh.set_overload(None)
                                            rh.set_topology_result(topology_result)
                                            outputs_list.append(rh)

                                            if logger.isEnabledFor(logging.DEBUG):
                                                logging.debug(rh.__str__())

                        else:
                            kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                            kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                            for kspwlo_algorithm in kspwlo_algorithms:
                                threshold_path = os.path.join(kspwlo_algorithm_path, kspwlo_algorithm)
                                thresholds = os.listdir(threshold_path)

                                for threshold in thresholds:
                                    k_path = os.path.join(method_path, method)
                                    ks = natsorted(os.listdir(k_path))

                                    for k in ks:
                                        ba_path = os.path.join(k_path, k)

                                        try:
                                            bas = os.listdir(ba_path)
                                        except ValueError:
                                            continue

                                        for ba in bas:
                                            overload_or_topology_path = os.path.join(ba_path, ba)
                                            overload_or_topology = os.listdir(overload_or_topology_path)

                                            if "overload" in overload_or_topology:
                                                overload = "overload"

                                                result_file_path = os.path.join(overload_or_topology_path, overload)

                                                topology_result_list = create_result(
                                                    result_file_path)

                                                for topology_result in topology_result_list:

                                                    rh = ResultHolder()
                                                    rh.set_solver(solver)
                                                    rh.set_mtr(None)
                                                    rh.set_algorithm(algorithm)
                                                    rh.set_randomization(None)
                                                    rh.set_normalization(None)
                                                    rh.set_cObjective(None)
                                                    rh.set_wAVB(None)
                                                    rh.set_wTT(None)
                                                    rh.set_wLength(None)
                                                    rh.set_wUtil(None)
                                                    rh.set_method(method)
                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                    rh.set_kspwlo_threshold(threshold)
                                                    rh.set_k(k)
                                                    rh.set_ba(ba)
                                                    rh.set_overload(overload)
                                                    rh.set_topology_result(topology_result)
                                                    outputs_list.append(rh)

                                                    if logger.isEnabledFor(logging.DEBUG):
                                                        logging.debug(rh.__str__())

                                            else:
                                                topology_result_list = create_result(
                                                    overload_or_topology_path)

                                                for topology_result in topology_result_list:

                                                    rh = ResultHolder()
                                                    rh.set_solver(solver)
                                                    rh.set_mtr(None)
                                                    rh.set_algorithm(algorithm)
                                                    rh.set_randomization(None)
                                                    rh.set_normalization(None)
                                                    rh.set_cObjective(None)
                                                    rh.set_wAVB(None)
                                                    rh.set_wTT(None)
                                                    rh.set_wLength(None)
                                                    rh.set_wUtil(None)
                                                    rh.set_method(method)
                                                    rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                    rh.set_kspwlo_threshold(threshold)
                                                    rh.set_k(k)
                                                    rh.set_ba(ba)
                                                    rh.set_overload(None)
                                                    rh.set_topology_result(topology_result)
                                                    outputs_list.append(rh)

                                                    if logger.isEnabledFor(logging.DEBUG):
                                                        logging.debug(rh.__str__())
        elif solver == "mtr":
            mtr_name_path = os.path.join(solvers_path, solver)
            mtr_names = os.listdir(mtr_name_path)
            for mtr_name in mtr_names:
                algorithm_path = os.path.join(mtr_name_path, mtr_name)
                algorithms = os.listdir(algorithm_path)
                for algorithm in algorithms:
                    if "C" == algorithm or "CD" == algorithm or "CDST" == algorithm or "CDSTV2" == algorithm:
                        normalization_path = os.path.join(algorithm_path, algorithm)
                        normalizations = os.listdir(normalization_path)

                        for normalization in normalizations:
                            c_objective_path = os.path.join(normalization_path, normalization)
                            c_objectives = os.listdir(c_objective_path)

                            for c_objective in c_objectives:
                                w_avb_path = os.path.join(c_objective_path, c_objective)
                                w_avbs = os.listdir(w_avb_path)

                                for w_avb in w_avbs:
                                    w_tt_path = os.path.join(w_avb_path, w_avb)
                                    w_tts = os.listdir(w_tt_path)

                                    for w_tt in w_tts:
                                        w_length_path = os.path.join(w_tt_path, w_tt)
                                        w_lengths = os.listdir(w_length_path)

                                        for w_length in w_lengths:
                                            w_util_path = os.path.join(w_length_path, w_length)
                                            w_utils = os.listdir(w_util_path)

                                            for w_util in w_utils:
                                                method_path = os.path.join(w_util_path, w_util)
                                                methods = os.listdir(method_path)

                                                for method in methods:
                                                    if "kspwlo" not in method:
                                                        k_path = os.path.join(method_path, method)
                                                        ks = natsorted(os.listdir(k_path))

                                                        for k in ks:
                                                            ba_path = os.path.join(k_path, k)

                                                            try:
                                                                bas = os.listdir(ba_path)
                                                            except:
                                                                continue

                                                            for ba in bas:
                                                                overload_or_topology_path = os.path.join(ba_path, ba)
                                                                overload_or_topology = os.listdir(overload_or_topology_path)

                                                                if "overload" in overload_or_topology:
                                                                    overload = "overload"

                                                                    result_file_path = os.path.join(
                                                                        overload_or_topology_path,
                                                                        overload)

                                                                    topology_result_list = create_result(
                                                                        result_file_path)

                                                                    for topology_result in topology_result_list:

                                                                        rh = ResultHolder()
                                                                        rh.set_solver(solver)
                                                                        rh.set_mtr(mtr_name)
                                                                        rh.set_algorithm(algorithm)
                                                                        rh.set_randomization(None)
                                                                        rh.set_normalization(normalization)
                                                                        rh.set_cObjective(c_objective)
                                                                        rh.set_wAVB(w_avb)
                                                                        rh.set_wTT(w_tt)
                                                                        rh.set_wLength(w_length)
                                                                        rh.set_wUtil(w_util)
                                                                        rh.set_method(method)
                                                                        rh.set_kspwlo_algorithm(None)
                                                                        rh.set_kspwlo_threshold(None)
                                                                        rh.set_k(k)
                                                                        rh.set_ba(ba)
                                                                        rh.set_overload(overload)
                                                                        rh.set_topology_result(topology_result)
                                                                        outputs_list.append(rh)

                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                            logging.debug(rh.__str__())

                                                                else:
                                                                    topology_result_list = create_result(
                                                                        overload_or_topology_path)

                                                                    for topology_result in topology_result_list:

                                                                        rh = ResultHolder()
                                                                        rh.set_solver(solver)
                                                                        rh.set_mtr(mtr_name)
                                                                        rh.set_algorithm(algorithm)
                                                                        rh.set_randomization(None)
                                                                        rh.set_normalization(normalization)
                                                                        rh.set_cObjective(c_objective)
                                                                        rh.set_wAVB(w_avb)
                                                                        rh.set_wTT(w_tt)
                                                                        rh.set_wLength(w_length)
                                                                        rh.set_wUtil(w_util)
                                                                        rh.set_method(method)
                                                                        rh.set_kspwlo_algorithm(None)
                                                                        rh.set_kspwlo_threshold(None)
                                                                        rh.set_k(k)
                                                                        rh.set_ba(ba)
                                                                        rh.set_overload(None)
                                                                        rh.set_topology_result(
                                                                            topology_result)
                                                                        outputs_list.append(rh)

                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                            logging.debug(rh.__str__())

                                                    else:
                                                        kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                                                        kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                                        for kspwlo_algorithm in kspwlo_algorithms:
                                                            threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                                          kspwlo_algorithm)
                                                            thresholds = os.listdir(threshold_path)

                                                            for threshold in thresholds:
                                                                k_path = os.path.join(method_path, method)
                                                                ks = natsorted(os.listdir(k_path))

                                                                for k in ks:
                                                                    ba_path = os.path.join(k_path, k)

                                                                    try:
                                                                        bas = os.listdir(ba_path)
                                                                    except:
                                                                        continue

                                                                    for ba in bas:
                                                                        overload_or_topology_path = os.path.join(
                                                                            ba_path,
                                                                            ba)
                                                                        overload_or_topology = os.listdir(
                                                                            overload_or_topology_path)

                                                                        if "overload" in overload_or_topology:
                                                                            overload = "overload"

                                                                            result_file_path = os.path.join(
                                                                                overload_or_topology_path, overload)

                                                                            topology_result_list = create_result(
                                                                                result_file_path)

                                                                            for topology_result in topology_result_list:

                                                                                rh = ResultHolder()
                                                                                rh.set_solver(solver)
                                                                                rh.set_mtr(mtr_name)
                                                                                rh.set_algorithm(algorithm)
                                                                                rh.set_randomization(None)
                                                                                rh.set_normalization(normalization)
                                                                                rh.set_cObjective(c_objective)
                                                                                rh.set_wAVB(w_avb)
                                                                                rh.set_wTT(w_tt)
                                                                                rh.set_wLength(w_length)
                                                                                rh.set_wUtil(w_util)
                                                                                rh.set_method(method)
                                                                                rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                                rh.set_kspwlo_threshold(threshold)
                                                                                rh.set_k(k)
                                                                                rh.set_ba(ba)
                                                                                rh.set_overload(overload)
                                                                                rh.set_topology_result(
                                                                                    topology_result)
                                                                                outputs_list.append(rh)

                                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                                    logging.debug(rh.__str__())

                                                                        else:
                                                                            topology_result_list = create_result(
                                                                                overload_or_topology_path)

                                                                            for topology_result in topology_result_list:

                                                                                rh = ResultHolder()
                                                                                rh.set_solver(solver)
                                                                                rh.set_mtr(mtr_name)
                                                                                rh.set_algorithm(algorithm)
                                                                                rh.set_randomization(None)
                                                                                rh.set_normalization(normalization)
                                                                                rh.set_cObjective(c_objective)
                                                                                rh.set_wAVB(w_avb)
                                                                                rh.set_wTT(w_tt)
                                                                                rh.set_wLength(w_length)
                                                                                rh.set_wUtil(w_util)
                                                                                rh.set_method(method)
                                                                                rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                                rh.set_kspwlo_threshold(threshold)
                                                                                rh.set_k(k)
                                                                                rh.set_ba(ba)
                                                                                rh.set_overload(None)
                                                                                rh.set_topology_result(
                                                                                    topology_result)
                                                                                outputs_list.append(rh)

                                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                                    logging.debug(rh.__str__())
                    elif "C" in algorithm or "CD" in algorithm or "CDST" in algorithm or "CDSTV2" in algorithm:
                        if "Random" not in algorithm:
                            randomization_path = os.path.join(algorithm_path, algorithm)
                            randomizations = os.listdir(randomization_path)

                            for randomization in randomizations:
                                normalization_path = os.path.join(randomization_path, randomization)
                                normalizations = os.listdir(normalization_path)

                                for normalization in normalizations:
                                    c_objective_path = os.path.join(normalization_path, normalization)
                                    c_objectives = os.listdir(c_objective_path)

                                    for c_objective in c_objectives:
                                        w_avb_path = os.path.join(c_objective_path, c_objective)
                                        w_avbs = os.listdir(w_avb_path)

                                        for w_avb in w_avbs:
                                            w_tt_path = os.path.join(w_avb_path, w_avb)
                                            w_tts = os.listdir(w_tt_path)

                                            for w_tt in w_tts:
                                                w_length_path = os.path.join(w_tt_path, w_tt)
                                                w_lengths = os.listdir(w_length_path)

                                                for w_length in w_lengths:
                                                    w_util_path = os.path.join(w_length_path, w_length)
                                                    w_utils = os.listdir(w_util_path)

                                                    for w_util in w_utils:
                                                        method_path = os.path.join(w_util_path, w_util)
                                                        methods = os.listdir(method_path)

                                                        for method in methods:
                                                            if "kspwlo" not in method:
                                                                k_path = os.path.join(method_path, method)
                                                                ks = natsorted(os.listdir(k_path))

                                                                for k in ks:
                                                                    ba_path = os.path.join(k_path, k)

                                                                    try:
                                                                        bas = os.listdir(ba_path)
                                                                    except:
                                                                        continue

                                                                    for ba in bas:
                                                                        overload_or_topology_path = os.path.join(ba_path, ba)
                                                                        overload_or_topology = os.listdir(
                                                                            overload_or_topology_path)

                                                                        if "overload" in overload_or_topology:
                                                                            overload = "overload"

                                                                            result_file_path = os.path.join(
                                                                                overload_or_topology_path,
                                                                                overload)

                                                                            topology_result_list = create_result(
                                                                                result_file_path)

                                                                            for topology_result in topology_result_list:

                                                                                rh = ResultHolder()
                                                                                rh.set_solver(solver)
                                                                                rh.set_mtr(mtr_name)
                                                                                rh.set_algorithm(algorithm)
                                                                                rh.set_randomization(randomization)
                                                                                rh.set_normalization(normalization)
                                                                                rh.set_cObjective(c_objective)
                                                                                rh.set_wAVB(w_avb)
                                                                                rh.set_wTT(w_tt)
                                                                                rh.set_wLength(w_length)
                                                                                rh.set_wUtil(w_util)
                                                                                rh.set_method(method)
                                                                                rh.set_kspwlo_algorithm(None)
                                                                                rh.set_kspwlo_threshold(None)
                                                                                rh.set_k(k)
                                                                                rh.set_ba(ba)
                                                                                rh.set_overload(overload)
                                                                                rh.set_topology_result(topology_result)
                                                                                outputs_list.append(rh)

                                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                                    logging.debug(rh.__str__())

                                                                        else:
                                                                            topology_result_list = create_result(
                                                                                overload_or_topology_path)

                                                                            for topology_result in topology_result_list:

                                                                                rh = ResultHolder()
                                                                                rh.set_solver(solver)
                                                                                rh.set_mtr(mtr_name)
                                                                                rh.set_algorithm(algorithm)
                                                                                rh.set_randomization(randomization)
                                                                                rh.set_normalization(normalization)
                                                                                rh.set_cObjective(c_objective)
                                                                                rh.set_wAVB(w_avb)
                                                                                rh.set_wTT(w_tt)
                                                                                rh.set_wLength(w_length)
                                                                                rh.set_wUtil(w_util)
                                                                                rh.set_method(method)
                                                                                rh.set_kspwlo_algorithm(None)
                                                                                rh.set_kspwlo_threshold(None)
                                                                                rh.set_k(k)
                                                                                rh.set_ba(ba)
                                                                                rh.set_overload(None)
                                                                                rh.set_topology_result(
                                                                                    topology_result)
                                                                                outputs_list.append(rh)

                                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                                    logging.debug(rh.__str__())

                                                            else:
                                                                kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                                                                kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                                                for kspwlo_algorithm in kspwlo_algorithms:
                                                                    threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                                                  kspwlo_algorithm)
                                                                    thresholds = os.listdir(threshold_path)

                                                                    for threshold in thresholds:
                                                                        k_path = os.path.join(method_path, method)
                                                                        ks = natsorted(os.listdir(k_path))

                                                                        for k in ks:
                                                                            ba_path = os.path.join(k_path, k)

                                                                            try:
                                                                                bas = os.listdir(ba_path)
                                                                            except:
                                                                                continue

                                                                            for ba in bas:
                                                                                overload_or_topology_path = os.path.join(
                                                                                    ba_path,
                                                                                    ba)
                                                                                overload_or_topology = os.listdir(
                                                                                    overload_or_topology_path)

                                                                                if "overload" in overload_or_topology:
                                                                                    overload = "overload"

                                                                                    result_file_path = os.path.join(
                                                                                        overload_or_topology_path, overload)

                                                                                    topology_result_list = create_result(
                                                                                        result_file_path)

                                                                                    for topology_result in topology_result_list:

                                                                                        rh = ResultHolder()
                                                                                        rh.set_solver(solver)
                                                                                        rh.set_mtr(mtr_name)
                                                                                        rh.set_algorithm(algorithm)
                                                                                        rh.set_randomization(randomization)
                                                                                        rh.set_normalization(normalization)
                                                                                        rh.set_cObjective(c_objective)
                                                                                        rh.set_wAVB(w_avb)
                                                                                        rh.set_wTT(w_tt)
                                                                                        rh.set_wLength(w_length)
                                                                                        rh.set_wUtil(w_util)
                                                                                        rh.set_method(method)
                                                                                        rh.set_kspwlo_algorithm(
                                                                                            kspwlo_algorithm)
                                                                                        rh.set_kspwlo_threshold(threshold)
                                                                                        rh.set_k(k)
                                                                                        rh.set_ba(ba)
                                                                                        rh.set_overload(overload)
                                                                                        rh.set_topology_result(
                                                                                            topology_result)
                                                                                        outputs_list.append(rh)

                                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                                            logging.debug(rh.__str__())

                                                                                else:
                                                                                    topology_result_list = create_result(
                                                                                        overload_or_topology_path)

                                                                                    for topology_result in topology_result_list:

                                                                                        rh = ResultHolder()
                                                                                        rh.set_solver(solver)
                                                                                        rh.set_mtr(mtr_name)
                                                                                        rh.set_algorithm(algorithm)
                                                                                        rh.set_randomization(randomization)
                                                                                        rh.set_normalization(normalization)
                                                                                        rh.set_cObjective(c_objective)
                                                                                        rh.set_wAVB(w_avb)
                                                                                        rh.set_wTT(w_tt)
                                                                                        rh.set_wLength(w_length)
                                                                                        rh.set_wUtil(w_util)
                                                                                        rh.set_method(method)
                                                                                        rh.set_kspwlo_algorithm(
                                                                                            kspwlo_algorithm)
                                                                                        rh.set_kspwlo_threshold(threshold)
                                                                                        rh.set_k(k)
                                                                                        rh.set_ba(ba)
                                                                                        rh.set_overload(None)
                                                                                        rh.set_topology_result(
                                                                                            topology_result)
                                                                                        outputs_list.append(rh)

                                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                                            logging.debug(rh.__str__())
                        else:
                            randomization_path = os.path.join(algorithm_path, algorithm)
                            randomizations = os.listdir(randomization_path)

                            for randomization in randomizations:
                                normalization_path = os.path.join(randomization_path, randomization)
                                normalizations = os.listdir(normalization_path)

                                for normalization in normalizations:
                                    c_objective_path = os.path.join(normalization_path, normalization)
                                    c_objectives = os.listdir(c_objective_path)

                                    for c_objective in c_objectives:
                                        method_path = os.path.join(c_objective_path, c_objective)
                                        methods = os.listdir(method_path)

                                        for method in methods:
                                            if "kspwlo" not in method:
                                                k_path = os.path.join(method_path, method)
                                                ks = natsorted(os.listdir(k_path))

                                                for k in ks:
                                                    ba_path = os.path.join(k_path, k)

                                                    try:
                                                        bas = os.listdir(ba_path)
                                                    except:
                                                        continue

                                                    for ba in bas:
                                                        overload_or_topology_path = os.path.join(ba_path, ba)
                                                        overload_or_topology = os.listdir(
                                                            overload_or_topology_path)

                                                        if "overload" in overload_or_topology:
                                                            overload = "overload"

                                                            result_file_path = os.path.join(
                                                                overload_or_topology_path,
                                                                overload)

                                                            topology_result_list = create_result(result_file_path)

                                                            for topology_result in topology_result_list:

                                                                rh = ResultHolder()
                                                                rh.set_solver(solver)
                                                                rh.set_mtr(mtr_name)
                                                                rh.set_algorithm(algorithm)
                                                                rh.set_randomization(randomization)
                                                                rh.set_normalization(normalization)
                                                                rh.set_cObjective(c_objective)
                                                                rh.set_wAVB(None)
                                                                rh.set_wTT(None)
                                                                rh.set_wLength(None)
                                                                rh.set_wUtil(None)
                                                                rh.set_method(method)
                                                                rh.set_kspwlo_algorithm(None)
                                                                rh.set_kspwlo_threshold(None)
                                                                rh.set_k(k)
                                                                rh.set_ba(ba)
                                                                rh.set_overload(overload)
                                                                rh.set_topology_result(topology_result)
                                                                outputs_list.append(rh)

                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                    logging.debug(rh.__str__())

                                                        else:
                                                            topology_result_list = create_result(overload_or_topology_path)

                                                            for topology_result in topology_result_list:

                                                                rh = ResultHolder()
                                                                rh.set_solver(solver)
                                                                rh.set_mtr(mtr_name)
                                                                rh.set_algorithm(algorithm)
                                                                rh.set_randomization(randomization)
                                                                rh.set_normalization(normalization)
                                                                rh.set_cObjective(c_objective)
                                                                rh.set_wAVB(None)
                                                                rh.set_wTT(None)
                                                                rh.set_wLength(None)
                                                                rh.set_wUtil(None)
                                                                rh.set_method(method)
                                                                rh.set_kspwlo_algorithm(None)
                                                                rh.set_kspwlo_threshold(None)
                                                                rh.set_k(k)
                                                                rh.set_ba(ba)
                                                                rh.set_overload(None)
                                                                rh.set_topology_result(topology_result)
                                                                outputs_list.append(rh)

                                                                if logger.isEnabledFor(logging.DEBUG):
                                                                    logging.debug(rh.__str__())
                                            else:
                                                kspwlo_algorithm_path = os.path.join(algorithm_path,
                                                                                     algorithm)
                                                kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                                for kspwlo_algorithm in kspwlo_algorithms:
                                                    threshold_path = os.path.join(kspwlo_algorithm_path,
                                                                                  kspwlo_algorithm)
                                                    thresholds = os.listdir(threshold_path)

                                                    for threshold in thresholds:
                                                        k_path = os.path.join(method_path, method)
                                                        ks = natsorted(os.listdir(k_path))

                                                        for k in ks:
                                                            ba_path = os.path.join(k_path, k)

                                                            try:
                                                                bas = os.listdir(ba_path)
                                                            except:
                                                                continue

                                                            for ba in bas:
                                                                overload_or_topology_path = os.path.join(
                                                                    ba_path,
                                                                    ba)
                                                                overload_or_topology = os.listdir(
                                                                    overload_or_topology_path)

                                                                if "overload" in overload_or_topology:
                                                                    overload = "overload"

                                                                    result_file_path = os.path.join(
                                                                        overload_or_topology_path, overload)

                                                                    topology_result_list = create_result(result_file_path)

                                                                    for topology_result in topology_result_list:

                                                                        rh = ResultHolder()
                                                                        rh.set_solver(solver)
                                                                        rh.set_mtr(mtr_name)
                                                                        rh.set_algorithm(algorithm)
                                                                        rh.set_randomization(randomization)
                                                                        rh.set_normalization(normalization)
                                                                        rh.set_cObjective(c_objective)
                                                                        rh.set_wAVB(None)
                                                                        rh.set_wTT(None)
                                                                        rh.set_wLength(None)
                                                                        rh.set_wUtil(None)
                                                                        rh.set_method(method)
                                                                        rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                        rh.set_kspwlo_threshold(threshold)
                                                                        rh.set_k(k)
                                                                        rh.set_ba(ba)
                                                                        rh.set_overload(overload)
                                                                        rh.set_topology_result(topology_result)
                                                                        outputs_list.append(rh)

                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                            logging.debug(rh.__str__())

                                                                else:
                                                                    topology_result_list = create_result(
                                                                        overload_or_topology_path)

                                                                    for topology_result in topology_result_list:

                                                                        rh = ResultHolder()
                                                                        rh.set_solver(solver)
                                                                        rh.set_mtr(mtr_name)
                                                                        rh.set_algorithm(algorithm)
                                                                        rh.set_randomization(randomization)
                                                                        rh.set_normalization(normalization)
                                                                        rh.set_cObjective(c_objective)
                                                                        rh.set_wAVB(None)
                                                                        rh.set_wTT(None)
                                                                        rh.set_wLength(None)
                                                                        rh.set_wUtil(None)
                                                                        rh.set_method(method)
                                                                        rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                                        rh.set_kspwlo_threshold(threshold)
                                                                        rh.set_k(k)
                                                                        rh.set_ba(ba)
                                                                        rh.set_overload(None)
                                                                        rh.set_topology_result(topology_result)
                                                                        outputs_list.append(rh)

                                                                        if logger.isEnabledFor(logging.DEBUG):
                                                                            logging.debug(rh.__str__())
                    else:
                        method_path = os.path.join(algorithm_path, algorithm)
                        methods = os.listdir(method_path)
                        for method in methods:
                            if "kspwlo" not in method:
                                k_or_ba_path = os.path.join(method_path, method)
                                k_or_bas = os.listdir(k_or_ba_path)

                                try:
                                    k_path = os.path.join(method_path, method)
                                    ks = natsorted(os.listdir(k_path))

                                    for k in ks:
                                        ba_path = os.path.join(k_path, k)

                                        try:
                                            bas = os.listdir(ba_path)
                                        except:
                                            continue

                                        for ba in bas:
                                            overload_or_topology_path = os.path.join(ba_path, ba)
                                            overload_or_topology = os.listdir(overload_or_topology_path)

                                            if "overload" in overload_or_topology:
                                                overload = "overload"

                                                result_file_path = os.path.join(overload_or_topology_path, overload)

                                                topology_result_list = create_result(
                                                    result_file_path)

                                                for topology_result in topology_result_list:

                                                    rh = ResultHolder()
                                                    rh.set_solver(solver)
                                                    rh.set_mtr(mtr_name)
                                                    rh.set_algorithm(algorithm)
                                                    rh.set_randomization(None)
                                                    rh.set_normalization(None)
                                                    rh.set_cObjective(None)
                                                    rh.set_wAVB(None)
                                                    rh.set_wTT(None)
                                                    rh.set_wLength(None)
                                                    rh.set_wUtil(None)
                                                    rh.set_method(method)
                                                    rh.set_kspwlo_algorithm(None)
                                                    rh.set_kspwlo_threshold(None)
                                                    rh.set_k(k)
                                                    rh.set_ba(ba)
                                                    rh.set_overload(overload)
                                                    rh.set_topology_result(topology_result)
                                                    outputs_list.append(rh)

                                                    if logger.isEnabledFor(logging.DEBUG):
                                                        logging.debug(rh.__str__())

                                            else:
                                                topology_result_list = create_result(
                                                    overload_or_topology_path)

                                                for topology_result in topology_result_list:

                                                    rh = ResultHolder()
                                                    rh.set_solver(solver)
                                                    rh.set_mtr(mtr_name)
                                                    rh.set_algorithm(algorithm)
                                                    rh.set_randomization(None)
                                                    rh.set_normalization(None)
                                                    rh.set_cObjective(None)
                                                    rh.set_wAVB(None)
                                                    rh.set_wTT(None)
                                                    rh.set_wLength(None)
                                                    rh.set_wUtil(None)
                                                    rh.set_method(method)
                                                    rh.set_kspwlo_algorithm(None)
                                                    rh.set_kspwlo_threshold(None)
                                                    rh.set_k(k)
                                                    rh.set_ba(ba)
                                                    rh.set_overload(None)
                                                    rh.set_topology_result(topology_result)
                                                    outputs_list.append(rh)

                                                    if logger.isEnabledFor(logging.DEBUG):
                                                        logging.debug(rh.__str__())

                                except ValueError:
                                    for ba in k_or_bas:
                                        overload_or_topology_path = os.path.join(k_or_ba_path, ba)
                                        overload_or_topology = os.listdir(overload_or_topology_path)

                                        if "overload" in overload_or_topology:
                                            overload = "overload"

                                            result_file_path = os.path.join(overload_or_topology_path, overload)

                                            topology_result_list = create_result(
                                                result_file_path)

                                            for topology_result in topology_result_list:

                                                rh = ResultHolder()
                                                rh.set_solver(solver)
                                                rh.set_mtr(mtr_name)
                                                rh.set_algorithm(algorithm)
                                                rh.set_randomization(None)
                                                rh.set_normalization(None)
                                                rh.set_cObjective(None)
                                                rh.set_wAVB(None)
                                                rh.set_wTT(None)
                                                rh.set_wLength(None)
                                                rh.set_wUtil(None)
                                                rh.set_method(method)
                                                rh.set_kspwlo_algorithm(None)
                                                rh.set_kspwlo_threshold(None)
                                                rh.set_k(None)
                                                rh.set_ba(ba)
                                                rh.set_overload(overload)
                                                rh.set_topology_result(topology_result)
                                                outputs_list.append(rh)

                                                if logger.isEnabledFor(logging.DEBUG):
                                                    logging.debug(rh.__str__())

                                        else:
                                            topology_result_list = create_result(
                                                overload_or_topology_path)

                                            for topology_result in topology_result_list:

                                                rh = ResultHolder()
                                                rh.set_solver(solver)
                                                rh.set_mtr(mtr_name)
                                                rh.set_algorithm(algorithm)
                                                rh.set_randomization(None)
                                                rh.set_normalization(None)
                                                rh.set_cObjective(None)
                                                rh.set_wAVB(None)
                                                rh.set_wTT(None)
                                                rh.set_wLength(None)
                                                rh.set_wUtil(None)
                                                rh.set_method(method)
                                                rh.set_kspwlo_algorithm(None)
                                                rh.set_kspwlo_threshold(None)
                                                rh.set_k(None)
                                                rh.set_ba(ba)
                                                rh.set_overload(None)
                                                rh.set_topology_result(topology_result)
                                                outputs_list.append(rh)

                                                if logger.isEnabledFor(logging.DEBUG):
                                                    logging.debug(rh.__str__())

                            else:
                                kspwlo_algorithm_path = os.path.join(algorithm_path, algorithm)
                                kspwlo_algorithms = os.listdir(kspwlo_algorithm_path)

                                for kspwlo_algorithm in kspwlo_algorithms:
                                    threshold_path = os.path.join(kspwlo_algorithm_path, kspwlo_algorithm)
                                    thresholds = os.listdir(threshold_path)

                                    for threshold in thresholds:
                                        k_path = os.path.join(method_path, method)
                                        ks = natsorted(os.listdir(k_path))

                                        for k in ks:
                                            ba_path = os.path.join(k_path, k)

                                            try:
                                                bas = os.listdir(ba_path)
                                            except ValueError:
                                                continue

                                            for ba in bas:
                                                overload_or_topology_path = os.path.join(ba_path, ba)
                                                overload_or_topology = os.listdir(overload_or_topology_path)

                                                if "overload" in overload_or_topology:
                                                    overload = "overload"

                                                    result_file_path = os.path.join(overload_or_topology_path, overload)

                                                    topology_result_list = create_result(
                                                        result_file_path)

                                                    for topology_result in topology_result_list:

                                                        rh = ResultHolder()
                                                        rh.set_solver(solver)
                                                        rh.set_mtr(mtr_name)
                                                        rh.set_algorithm(algorithm)
                                                        rh.set_randomization(None)
                                                        rh.set_normalization(None)
                                                        rh.set_cObjective(None)
                                                        rh.set_wAVB(None)
                                                        rh.set_wTT(None)
                                                        rh.set_wLength(None)
                                                        rh.set_wUtil(None)
                                                        rh.set_method(method)
                                                        rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                        rh.set_kspwlo_threshold(threshold)
                                                        rh.set_k(k)
                                                        rh.set_ba(ba)
                                                        rh.set_overload(overload)
                                                        rh.set_topology_result(topology_result)
                                                        outputs_list.append(rh)

                                                        if logger.isEnabledFor(logging.DEBUG):
                                                            logging.debug(rh.__str__())

                                                else:
                                                    topology_result_list = create_result(
                                                        overload_or_topology_path)

                                                    for topology_result in topology_result_list:

                                                        rh = ResultHolder()
                                                        rh.set_solver(solver)
                                                        rh.set_mtr(mtr_name)
                                                        rh.set_algorithm(algorithm)
                                                        rh.set_randomization(None)
                                                        rh.set_normalization(None)
                                                        rh.set_cObjective(None)
                                                        rh.set_wAVB(None)
                                                        rh.set_wTT(None)
                                                        rh.set_wLength(None)
                                                        rh.set_wUtil(None)
                                                        rh.set_method(method)
                                                        rh.set_kspwlo_algorithm(kspwlo_algorithm)
                                                        rh.set_kspwlo_threshold(threshold)
                                                        rh.set_k(k)
                                                        rh.set_ba(ba)
                                                        rh.set_overload(None)
                                                        rh.set_topology_result(topology_result)
                                                        outputs_list.append(rh)

                                                        if logger.isEnabledFor(logging.DEBUG):
                                                            logging.debug(rh.__str__())

    return outputs_list


def outputs_dont_have_k(logger, project):
    outputs_list = list()

    solvers_path = os.path.join(os.path.expanduser("~"), project, "outputs")
    solvers = os.listdir(solvers_path)

    for solver in solvers:
        if solver == "phy":
            algorithm_path = os.path.join(solvers_path, solver)
            algorithms = os.listdir(algorithm_path)

            for algorithm in algorithms:
                if "shortestpath" == algorithm:
                    method_path = os.path.join(algorithm_path, algorithm)
                    methods = os.listdir(method_path)

                    for method in methods:
                        ba_path = os.path.join(method_path, method)
                        bas = os.listdir(ba_path)

                        for ba in bas:
                            overload_or_topology_path = os.path.join(ba_path, ba)
                            overload_or_topology = os.listdir(overload_or_topology_path)

                            if "overload" in overload_or_topology:
                                overload = "overload"

                                result_file_path = os.path.join(overload_or_topology_path, overload)

                                topology_result_list = create_result(result_file_path)

                                for topology_result in topology_result_list:

                                    rh = ResultHolder()
                                    rh.set_solver(solver)
                                    rh.set_mtr(None)
                                    rh.set_algorithm(algorithm)
                                    rh.set_randomization(None)
                                    rh.set_normalization(None)
                                    rh.set_cObjective(None)
                                    rh.set_wAVB(None)
                                    rh.set_wTT(None)
                                    rh.set_wLength(None)
                                    rh.set_wUtil(None)
                                    rh.set_method(method)
                                    rh.set_kspwlo_algorithm(None)
                                    rh.set_kspwlo_threshold(None)
                                    rh.set_k(None)
                                    rh.set_ba(ba)
                                    rh.set_overload(overload)
                                    rh.set_topology_result(topology_result)
                                    outputs_list.append(rh)

                                    if logger.isEnabledFor(logging.DEBUG):
                                        logging.debug(rh.__str__())

                            else:

                                topology_result_list = create_result(overload_or_topology_path)

                                for topology_result in topology_result_list:

                                    rh = ResultHolder()
                                    rh.set_solver(solver)
                                    rh.set_mtr(None)
                                    rh.set_algorithm(algorithm)
                                    rh.set_randomization(None)
                                    rh.set_normalization(None)
                                    rh.set_cObjective(None)
                                    rh.set_wAVB(None)
                                    rh.set_wTT(None)
                                    rh.set_wLength(None)
                                    rh.set_wUtil(None)
                                    rh.set_method(method)
                                    rh.set_kspwlo_algorithm(None)
                                    rh.set_kspwlo_threshold(None)
                                    rh.set_k(None)
                                    rh.set_ba(ba)
                                    rh.set_overload(None)
                                    rh.set_topology_result(topology_result)
                                    outputs_list.append(rh)

                                    if logger.isEnabledFor(logging.DEBUG):
                                        logging.debug(rh.__str__())

    return outputs_list
