import os
import re

import constants
from result_holder import ResultHolder
from topology_result import TopologyResult


def get_max_util(line):
    match = re.search(r'Max Loaded Link Utilization: (\d+\.\d+)', line)

    if match:
        utilization_value = float(match.group(1))
        formatted_value = "{:.2f}".format(utilization_value)
        return formatted_value


def get_average_wcd(line):
    match = re.search(r'Average WCD: (\d+\.\d+)', line)

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

    average_wcd = get_average_wcd(lines[2])

    max_util = get_max_util(lines[3])
    average_util = get_average(lines[3])
    variance_util = get_variance(lines[3])

    time = get_time(lines[4])

    topology_result = TopologyResult(topology_name, o1, o2, o3, average_wcd, max_util, average_util, variance_util,
                                     time)

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


def read_output(project):
    outputs_list = []

    routing_path = os.path.join(os.path.expanduser("~"), project, "outputs")
    routing_list = os.listdir(routing_path)

    for routing in routing_list:
        if routing == constants.PHY:
            path_finding_method_path = os.path.join(routing_path, routing)
            path_finding_method_list = os.listdir(path_finding_method_path)
            for path_finding_method in path_finding_method_list:
                if path_finding_method == constants.SHORTEST_PATH:
                    algorithm_path = os.path.join(path_finding_method_path, path_finding_method)
                    algorithm_list = os.listdir(algorithm_path)
                    for algorithm in algorithm_list:
                        result_path = os.path.join(algorithm_path, algorithm)
                        result_list = create_result(result_path)
                        for result in result_list:
                            result_holder = ResultHolder()
                            result_holder.routing = routing
                            result_holder.mtr_name = None
                            result_holder.path_finding_method = path_finding_method
                            result_holder.algorithm = algorithm
                            result_holder.lwr = None
                            result_holder.k = None
                            result_holder.mcdm_objective = None
                            result_holder.cwr = None
                            result_holder.w_srt = None
                            result_holder.w_tt = None
                            result_holder.w_length = None
                            result_holder.w_util = None
                            result_holder.wpm_version = None
                            result_holder.wpm_value_type = None
                            result_holder.metaheuristic_name = None
                            result_holder.evaluator_name = "avbLatencyMathTSNCF"
                            result_holder.topology_result = result
                            outputs_list.append(result_holder)

                else:
                    algorithm_path = os.path.join(path_finding_method_path, path_finding_method)
                    algorithm_list = os.listdir(algorithm_path)
                    for algorithm in algorithm_list:
                        # TODO: Not Final
                        if "WPM" in algorithm and "LWR" not in algorithm and "CWR" not in algorithm:
                            k_path = os.path.join(algorithm_path, algorithm)
                            k_list = os.listdir(k_path)
                            for k in k_list:
                                mcdm_objective_path = os.path.join(k_path, k)
                                mcdm_objective_list = os.listdir(mcdm_objective_path)
                                for mcdm_objective in mcdm_objective_list:
                                    w_srt_path = os.path.join(mcdm_objective_path, mcdm_objective)
                                    w_srt_list = os.listdir(w_srt_path)
                                    for w_srt in w_srt_list:
                                        w_tt_path = os.path.join(w_srt_path, w_srt)
                                        w_tt_list = os.listdir(w_tt_path)
                                        for w_tt in w_tt_list:
                                            w_length_path = os.path.join(w_tt_path, w_tt)
                                            w_length_list = os.listdir(w_length_path)
                                            for w_length in w_length_list:
                                                w_util_path = os.path.join(w_length_path, w_length)
                                                w_util_list = os.listdir(w_util_path)
                                                for w_util in w_util_list:
                                                    wpm_version_path = os.path.join(w_util_path, w_util)
                                                    wpm_version_list = os.listdir(wpm_version_path)
                                                    for wpm_version in wpm_version_list:
                                                        if wpm_version == "v1":
                                                            result_path = os.path.join(wpm_version_path,
                                                                                       wpm_version)
                                                            result_list = create_result(result_path)
                                                            for result in result_list:
                                                                result_holder = ResultHolder()
                                                                result_holder.routing = routing
                                                                result_holder.mtr_name = None
                                                                result_holder.path_finding_method = path_finding_method
                                                                result_holder.algorithm = algorithm
                                                                result_holder.lwr = None
                                                                result_holder.k = k
                                                                result_holder.mcdm_objective = mcdm_objective
                                                                result_holder.cwr = None
                                                                result_holder.w_srt = w_srt
                                                                result_holder.w_tt = w_tt
                                                                result_holder.w_length = w_length
                                                                result_holder.w_util = w_util
                                                                result_holder.wpm_version = wpm_version
                                                                result_holder.wpm_value_type = None
                                                                result_holder.metaheuristic_name = None
                                                                result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                                result_holder.topology_result = result
                                                                outputs_list.append(result_holder)
                                                        elif wpm_version == "v2":
                                                            wpm_value_type_path = os.path.join(wpm_version_path,
                                                                                               wpm_version)
                                                            wpm_value_type_list = os.listdir(wpm_value_type_path)
                                                            for wpm_value_type in wpm_value_type_list:
                                                                result_path = os.path.join(wpm_value_type_path,
                                                                                           wpm_value_type)
                                                                result_list = create_result(result_path)
                                                                for result in result_list:
                                                                    result_holder = ResultHolder()
                                                                    result_holder.routing = routing
                                                                    result_holder.mtr_name = None
                                                                    result_holder.path_finding_method = path_finding_method
                                                                    result_holder.algorithm = algorithm
                                                                    result_holder.lwr = None
                                                                    result_holder.k = k
                                                                    result_holder.mcdm_objective = mcdm_objective
                                                                    result_holder.cwr = None
                                                                    result_holder.w_srt = w_srt
                                                                    result_holder.w_tt = w_tt
                                                                    result_holder.w_length = w_length
                                                                    result_holder.w_util = w_util
                                                                    result_holder.wpm_version = wpm_version
                                                                    result_holder.wpm_value_type = wpm_value_type
                                                                    result_holder.metaheuristic_name = None
                                                                    result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                                    result_holder.topology_result = result
                                                                    outputs_list.append(result_holder)
                        elif "WPM" in algorithm and "LWR" in algorithm and "CWR" not in algorithm:
                            lwr_path = os.path.join(algorithm_path, algorithm)
                            lwr_list = os.listdir(lwr_path)
                            for lwr in lwr_list:
                                k_path = os.path.join(lwr_path, lwr)
                                k_list = os.listdir(k_path)
                                for k in k_list:
                                    mcdm_objective_path = os.path.join(k_path,
                                                                       k)
                                    mcdm_objective_list = os.listdir(
                                        mcdm_objective_path)
                                    for mcdm_objective in mcdm_objective_list:
                                        w_srt_path = os.path.join(
                                            mcdm_objective_path, mcdm_objective)
                                        w_srt_list = os.listdir(w_srt_path)
                                        for w_srt in w_srt_list:
                                            w_tt_path = os.path.join(w_srt_path,
                                                                     w_srt)
                                            w_tt_list = os.listdir(w_tt_path)
                                            for w_tt in w_tt_list:
                                                w_length_path = os.path.join(
                                                    w_tt_path, w_tt)
                                                w_length_list = os.listdir(
                                                    w_length_path)
                                                for w_length in w_length_list:
                                                    w_util_path = os.path.join(
                                                        w_length_path, w_length)
                                                    w_util_list = os.listdir(
                                                        w_util_path)
                                                    for w_util in w_util_list:
                                                        wpm_version_path = os.path.join(
                                                            w_util_path, w_util)
                                                        wpm_version_list = os.listdir(
                                                            wpm_version_path)
                                                        for wpm_version in wpm_version_list:
                                                            if wpm_version == "v1":
                                                                result_path = os.path.join(
                                                                    wpm_version_path,
                                                                    wpm_version)
                                                                result_list = create_result(
                                                                    result_path)
                                                                for result in result_list:
                                                                    result_holder = ResultHolder()
                                                                    result_holder.routing = routing
                                                                    result_holder.mtr_name = None
                                                                    result_holder.path_finding_method = path_finding_method
                                                                    result_holder.algorithm = algorithm
                                                                    result_holder.lwr = lwr
                                                                    result_holder.k = k
                                                                    result_holder.mcdm_objective = mcdm_objective
                                                                    result_holder.cwr = None
                                                                    result_holder.w_srt = w_srt
                                                                    result_holder.w_tt = w_tt
                                                                    result_holder.w_length = w_length
                                                                    result_holder.w_util = w_util
                                                                    result_holder.wpm_version = wpm_version
                                                                    result_holder.wpm_value_type = None
                                                                    result_holder.metaheuristic_name = "GRASP"
                                                                    result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                                    result_holder.topology_result = result
                                                                    outputs_list.append(
                                                                        result_holder)
                                                            elif wpm_version == "v2":
                                                                wpm_value_type_path = os.path.join(
                                                                    wpm_version_path,
                                                                    wpm_version)
                                                                wpm_value_type_list = os.listdir(
                                                                    wpm_value_type_path)
                                                                for wpm_value_type in wpm_value_type_list:
                                                                    result_path = os.path.join(
                                                                        wpm_value_type_path,
                                                                        wpm_value_type)
                                                                    result_list = create_result(
                                                                        result_path)
                                                                    for result in result_list:
                                                                        result_holder = ResultHolder()
                                                                        result_holder.routing = routing
                                                                        result_holder.mtr_name = None
                                                                        result_holder.path_finding_method = path_finding_method
                                                                        result_holder.algorithm = algorithm
                                                                        result_holder.lwr = lwr
                                                                        result_holder.k = k
                                                                        result_holder.mcdm_objective = mcdm_objective
                                                                        result_holder.cwr = None
                                                                        result_holder.w_srt = w_srt
                                                                        result_holder.w_tt = w_tt
                                                                        result_holder.w_length = w_length
                                                                        result_holder.w_util = w_util
                                                                        result_holder.wpm_version = wpm_version
                                                                        result_holder.wpm_value_type = wpm_value_type
                                                                        result_holder.metaheuristic_name = "GRASP"
                                                                        result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                                        result_holder.topology_result = result
                                                                        outputs_list.append(
                                                                            result_holder)
                        elif "WPM" in algorithm and "LWR" not in algorithm and "CWR" in algorithm:
                            k_path = os.path.join(algorithm_path, algorithm)
                            k_list = os.listdir(k_path)
                            for k in k_list:
                                mcdm_objective_path = os.path.join(k_path, k)
                                mcdm_objective_list = os.listdir(mcdm_objective_path)
                                for mcdm_objective in mcdm_objective_list:
                                    cwr_path = os.path.join(mcdm_objective_path, mcdm_objective)
                                    cwr_list = os.listdir(cwr_path)
                                    for cwr in cwr_list:
                                        wpm_version_path = os.path.join(cwr_path, cwr)
                                        wpm_version_list = os.listdir(wpm_version_path)
                                        for wpm_version in wpm_version_list:
                                            if wpm_version == "v1":
                                                result_path = os.path.join(wpm_version_path, wpm_version)
                                                result_list = create_result(result_path)
                                                for result in result_list:
                                                    result_holder = ResultHolder()
                                                    result_holder.routing = routing
                                                    result_holder.mtr_name = None
                                                    result_holder.path_finding_method = path_finding_method
                                                    result_holder.algorithm = algorithm
                                                    result_holder.lwr = None
                                                    result_holder.k = k
                                                    result_holder.mcdm_objective = mcdm_objective
                                                    result_holder.cwr = cwr
                                                    result_holder.w_srt = None
                                                    result_holder.w_tt = None
                                                    result_holder.w_length = None
                                                    result_holder.w_util = None
                                                    result_holder.wpm_version = wpm_version
                                                    result_holder.wpm_value_type = None
                                                    result_holder.metaheuristic_name = "GRASP"
                                                    result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                    result_holder.topology_result = result
                                                    outputs_list.append(result_holder)
                                            elif wpm_version == "v2":
                                                wpm_value_type_path = os.path.join(wpm_version_path, wpm_version)
                                                wpm_value_type_list = os.listdir(wpm_value_type_path)
                                                for wpm_value_type in wpm_value_type_list:
                                                    result_path = os.path.join(wpm_value_type_path, wpm_value_type)
                                                    result_list = create_result(result_path)
                                                    for result in result_list:
                                                        result_holder = ResultHolder()
                                                        result_holder.routing = routing
                                                        result_holder.mtr_name = None
                                                        result_holder.path_finding_method = path_finding_method
                                                        result_holder.algorithm = algorithm
                                                        result_holder.lwr = None
                                                        result_holder.k = k
                                                        result_holder.mcdm_objective = mcdm_objective
                                                        result_holder.cwr = cwr
                                                        result_holder.w_srt = None
                                                        result_holder.w_tt = None
                                                        result_holder.w_length = None
                                                        result_holder.w_util = None
                                                        result_holder.wpm_version = wpm_version
                                                        result_holder.wpm_value_type = wpm_value_type
                                                        result_holder.metaheuristic_name = "GRASP"
                                                        result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                                        result_holder.topology_result = result
                                                        outputs_list.append(result_holder)
                        # elif "WPM" in algorithm and "LWR" in algorithm and "CWR" in algorithm:
                        #     lwr_path = os.path.join(algorithm_path, algorithm)
                        #     lwr_list = os.listdir(lwr_path)
                        #     for lwr in lwr_list:
                        #         k_path = os.path.join(lwr_path, lwr)
                        #         k_list = os.listdir(k_path)
                        #         for k in k_list:
                        #             mcdm_objective_path = os.path.join(k_path, k)
                        #             mcdm_objective_list = os.listdir(mcdm_objective_path)
                        #             for mcdm_objective in mcdm_objective_list:
                        #                 cwr_path = os.path.join(mcdm_objective_path, mcdm_objective)
                        #                 cwr_list = os.listdir(cwr_path)
                        #                 for cwr in cwr_list:
                        #                     wpm_version_path = os.path.join(cwr_path, cwr)
                        #                     wpm_version_list = os.listdir(wpm_version_path)
                        #                     for wpm_version in wpm_version_list:
                        #                         if wpm_version == "v1":
                        #                             result_path = os.path.join(wpm_version_path,
                        #                                                        wpm_version)
                        #                             result_list = create_result(result_path)
                        #                             for result in result_list:
                        #                                 result_holder = ResultHolder()
                        #                                 result_holder.routing = routing
                        #                                 result_holder.mtr_name = None
                        #                                 result_holder.path_finding_method = path_finding_method
                        #                                 result_holder.algorithm = algorithm
                        #                                 result_holder.lwr = lwr
                        #                                 result_holder.k = k
                        #                                 result_holder.mcdm_objective = mcdm_objective
                        #                                 result_holder.cwr = cwr
                        #                                 result_holder.w_srt = w_srt
                        #                                 result_holder.w_tt = w_tt
                        #                                 result_holder.w_length = w_length
                        #                                 result_holder.w_util = w_util
                        #                                 result_holder.wpm_version = wpm_version
                        #                                 result_holder.wpm_value_type = None
                        #                                 result_holder.metaheuristic_name = "GRASP"
                        #                                 result_holder.evaluator_name = "avbLatencyMathTSNCF"
                        #                                 result_holder.topology_result = result
                        #                                 outputs_list.append(result_holder)
                        #                         elif wpm_version == "v2":
                        #                             wpm_value_type_path = os.path.join(wpm_version_path,
                        #                                                                wpm_version)
                        #                             wpm_value_type_list = os.listdir(
                        #                                 wpm_value_type_path)
                        #                             for wpm_value_type in wpm_value_type_list:
                        #                                 result_path = os.path.join(wpm_value_type_path,
                        #                                                            wpm_value_type)
                        #                                 result_list = create_result(result_path)
                        #                                 for result in result_list:
                        #                                     result_holder = ResultHolder()
                        #                                     result_holder.routing = routing
                        #                                     result_holder.mtr_name = None
                        #                                     result_holder.path_finding_method = path_finding_method
                        #                                     result_holder.algorithm = algorithm
                        #                                     result_holder.lwr = lwr
                        #                                     result_holder.k = k
                        #                                     result_holder.mcdm_objective = mcdm_objective
                        #                                     result_holder.cwr = cwr
                        #                                     result_holder.w_srt = w_srt
                        #                                     result_holder.w_tt = w_tt
                        #                                     result_holder.w_length = w_length
                        #                                     result_holder.w_util = w_util
                        #                                     result_holder.wpm_version = wpm_version
                        #                                     result_holder.wpm_value_type = wpm_value_type
                        #                                     result_holder.metaheuristic_name = "GRASP"
                        #                                     result_holder.evaluator_name = "avbLatencyMathTSNCF"
                        #                                     result_holder.topology_result = result
                        #                                     outputs_list.append(result_holder)

                        elif "WSM" in algorithm and "LWR" not in algorithm and "CWR" not in algorithm:
                            unicast_candidate_sorting_method_path = os.path.join(algorithm_path, algorithm)
                            unicast_candidate_sorting_method_list = os.listdir(unicast_candidate_sorting_method_path)
                            for unicast_candidate_sorting_method in unicast_candidate_sorting_method_list:
                                k_path = os.path.join(unicast_candidate_sorting_method_path,
                                                      unicast_candidate_sorting_method)
                                k_list = os.listdir(k_path)
                                for k in k_list:
                                    mcdm_objective_path = os.path.join(k_path, k)
                                    mcdm_objective_list = os.listdir(mcdm_objective_path)
                                    for mcdm_objective in mcdm_objective_list:
                                        if mcdm_objective == constants.SRT_TT_LENGTH:
                                            wsm_normalization_path = os.path.join(mcdm_objective_path,
                                                                                  mcdm_objective)
                                            wsm_normalization_list = os.listdir(wsm_normalization_path)
                                            for wsm_normalization in wsm_normalization_list:
                                                w_srt_path = os.path.join(wsm_normalization_path, wsm_normalization)
                                                w_srt_list = os.listdir(w_srt_path)
                                                for w_srt in w_srt_list:
                                                    w_tt_path = os.path.join(w_srt_path, w_srt)
                                                    w_tt_list = os.listdir(w_tt_path)
                                                    for w_tt in w_tt_list:
                                                        w_length_path = os.path.join(w_tt_path, w_tt)
                                                        w_length_list = os.listdir(w_length_path)
                                                        for w_length in w_length_list:
                                                            evaluator_name_path = os.path.join(
                                                                w_length_path,
                                                                w_length)
                                                            evaluator_name_list = os.listdir(
                                                                evaluator_name_path)
                                                            for evaluator_name in evaluator_name_list:
                                                                result_path = os.path.join(evaluator_name_path,
                                                                                           evaluator_name)
                                                                result_list = create_result(result_path)
                                                                for result in result_list:
                                                                    result_holder = ResultHolder()
                                                                    result_holder.routing = routing
                                                                    result_holder.path_finding_method = path_finding_method
                                                                    result_holder.algorithm = algorithm
                                                                    result_holder.k = k
                                                                    result_holder.mcdm_objective = mcdm_objective
                                                                    result_holder.wsm_normalization = wsm_normalization
                                                                    result_holder.w_srt = w_srt
                                                                    result_holder.w_tt = w_tt
                                                                    result_holder.w_length = w_length
                                                                    result_holder.evaluator_name = evaluator_name
                                                                    result_holder.topology_result = result
                                                                    outputs_list.append(result_holder)
                        elif "WSM" in algorithm and "LWR" in algorithm and "CWR" not in algorithm:
                            unicast_candidate_sorting_method_path = os.path.join(
                                algorithm_path, algorithm)
                            unicast_candidate_sorting_method_list = os.listdir(
                                unicast_candidate_sorting_method_path)
                            for unicast_candidate_sorting_method in unicast_candidate_sorting_method_list:
                                lwr_path = os.path.join(
                                    unicast_candidate_sorting_method_path,
                                    unicast_candidate_sorting_method)
                                lwr_list = os.listdir(lwr_path)
                                for lwr in lwr_list:
                                    k_path = os.path.join(lwr_path, lwr)
                                    k_list = os.listdir(k_path)
                                    for k in k_list:
                                        mcdm_objective_path = os.path.join(
                                            k_path, k)
                                        mcdm_objective_list = os.listdir(
                                            mcdm_objective_path)
                                        for mcdm_objective in mcdm_objective_list:
                                            if mcdm_objective == constants.SRT_TT_LENGTH:
                                                wsm_normalization_path = os.path.join(
                                                    mcdm_objective_path,
                                                    mcdm_objective)
                                                wsm_normalization_list = os.listdir(
                                                    wsm_normalization_path)
                                                for wsm_normalization in wsm_normalization_list:
                                                    w_srt_path = os.path.join(
                                                        wsm_normalization_path,
                                                        wsm_normalization)
                                                    w_srt_list = os.listdir(
                                                        w_srt_path)
                                                    for w_srt in w_srt_list:
                                                        w_tt_path = os.path.join(
                                                            w_srt_path, w_srt)
                                                        w_tt_list = os.listdir(
                                                            w_tt_path)
                                                        for w_tt in w_tt_list:
                                                            w_length_path = os.path.join(
                                                                w_tt_path, w_tt)
                                                            w_length_list = os.listdir(
                                                                w_length_path)
                                                            for w_length in w_length_list:
                                                                metaheuristic_name_path = os.path.join(
                                                                    w_length_path,
                                                                    w_length)
                                                                metaheuristic_name_list = os.listdir(
                                                                    metaheuristic_name_path)
                                                                for metaheuristic_name in metaheuristic_name_list:
                                                                    evaluator_name_path = os.path.join(
                                                                        metaheuristic_name_path,
                                                                        metaheuristic_name)
                                                                    evaluator_name_list = os.listdir(
                                                                        evaluator_name_path)
                                                                    for evaluator_name in evaluator_name_list:
                                                                        result_path = os.path.join(
                                                                            evaluator_name_path,
                                                                            evaluator_name)
                                                                        result_list = create_result(
                                                                            result_path)
                                                                        for result in result_list:
                                                                            result_holder = ResultHolder()
                                                                            result_holder.routing = routing
                                                                            result_holder.path_finding_method = path_finding_method
                                                                            result_holder.algorithm = algorithm
                                                                            result_holder.lwr = lwr
                                                                            result_holder.k = k
                                                                            result_holder.mcdm_objective = mcdm_objective
                                                                            result_holder.wsm_normalization = wsm_normalization
                                                                            result_holder.w_srt = w_srt
                                                                            result_holder.w_tt = w_tt
                                                                            result_holder.w_length = w_length
                                                                            result_holder.metaheuristic_name = metaheuristic_name
                                                                            result_holder.evaluator_name = evaluator_name
                                                                            result_holder.topology_result = result
                                                                            outputs_list.append(
                                                                                result_holder)
                        elif "WSM" in algorithm and "LWR" not in algorithm and "CWR" in algorithm:
                            unicast_candidate_sorting_method_path = os.path.join(algorithm_path, algorithm)
                            unicast_candidate_sorting_method_list = os.listdir(unicast_candidate_sorting_method_path)
                            for unicast_candidate_sorting_method in unicast_candidate_sorting_method_list:
                                k_path = os.path.join(unicast_candidate_sorting_method_path,
                                                      unicast_candidate_sorting_method)
                                k_list = os.listdir(k_path)
                                for k in k_list:
                                    mcdm_objective_path = os.path.join(k_path, k)
                                    mcdm_objective_list = os.listdir(mcdm_objective_path)
                                    for mcdm_objective in mcdm_objective_list:
                                        wsm_normalization_path = os.path.join(mcdm_objective_path, mcdm_objective)
                                        wsm_normalization_list = os.listdir(wsm_normalization_path)
                                        for wsm_normalization in wsm_normalization_list:
                                            cwr_path = os.path.join(wsm_normalization_path, wsm_normalization)
                                            cwr_list = os.listdir(cwr_path)
                                            for cwr in cwr_list:
                                                metaheuristic_name_path = os.path.join(cwr_path, cwr)
                                                metaheuristic_name_list = os.listdir(metaheuristic_name_path)
                                                for metaheuristic_name in metaheuristic_name_list:
                                                    evaluator_name_path = os.path.join(metaheuristic_name_path,
                                                                                       metaheuristic_name)
                                                    evaluator_name_list = os.listdir(evaluator_name_path)
                                                    for evaluator_name in evaluator_name_list:

                                                        result_path = os.path.join(evaluator_name_path, evaluator_name)
                                                        result_list = create_result(result_path)
                                                        for result in result_list:
                                                            result_holder = ResultHolder()
                                                            result_holder.routing = routing
                                                            result_holder.path_finding_method = path_finding_method
                                                            result_holder.algorithm = algorithm
                                                            result_holder.k = k
                                                            result_holder.mcdm_objective = mcdm_objective
                                                            result_holder.wsm_normalization = wsm_normalization
                                                            result_holder.cwr = cwr
                                                            result_holder.metaheuristic_name = metaheuristic_name
                                                            result_holder.evaluator_name = evaluator_name
                                                            result_holder.topology_result = result
                                                            outputs_list.append(result_holder)
                        # elif "WSM" in algorithm and "LWR" in algorithm and "CWR" in algorithm:
                        #     lwr_path = os.path.join(algorithm_path, algorithm)
                        #     lwr_list = os.listdir(lwr_path)
                        #     for lwr in lwr_list:
                        #         k_path = os.path.join(lwr_path, lwr)
                        #         k_list = os.listdir(k_path)
                        #         for k in k_list:
                        #             mcdm_objective_path = os.path.join(k_path, k)
                        #             mcdm_objective_list = os.listdir(mcdm_objective_path)
                        #             for mcdm_objective in mcdm_objective_list:
                        #                 cwr_path = os.path.join(mcdm_objective_path, mcdm_objective)
                        #                 cwr_list = os.listdir(cwr_path)
                        #                 for cwr in cwr_list:
                        #                     wpm_version_path = os.path.join(cwr_path, cwr)
                        #                     wpm_version_list = os.listdir(wpm_version_path)
                        #                     for wpm_version in wpm_version_list:
                        #                         if wpm_version == "v1":
                        #                             result_path = os.path.join(wpm_version_path,
                        #                                                        wpm_version)
                        #                             result_list = create_result(result_path)
                        #                             for result in result_list:
                        #                                 result_holder = ResultHolder()
                        #                                 result_holder.routing = routing
                        #                                 result_holder.mtr_name = None
                        #                                 result_holder.path_finding_method = path_finding_method
                        #                                 result_holder.algorithm = algorithm
                        #                                 result_holder.lwr = lwr
                        #                                 result_holder.k = k
                        #                                 result_holder.mcdm_objective = mcdm_objective
                        #                                 result_holder.cwr = cwr
                        #                                 result_holder.w_srt = w_srt
                        #                                 result_holder.w_tt = w_tt
                        #                                 result_holder.w_length = w_length
                        #                                 result_holder.w_util = w_util
                        #                                 result_holder.wpm_version = wpm_version
                        #                                 result_holder.wpm_value_type = None
                        #                                 result_holder.metaheuristic_name = "GRASP"
                        #                                 result_holder.evaluator_name = "avbLatencyMathTSNCF"
                        #                                 result_holder.topology_result = result
                        #                                 outputs_list.append(result_holder)
                        #                         elif wpm_version == "v2":
                        #                             wpm_value_type_path = os.path.join(wpm_version_path,
                        #                                                                wpm_version)
                        #                             wpm_value_type_list = os.listdir(
                        #                                 wpm_value_type_path)
                        #                             for wpm_value_type in wpm_value_type_list:
                        #                                 result_path = os.path.join(wpm_value_type_path,
                        #                                                            wpm_value_type)
                        #                                 result_list = create_result(result_path)
                        #                                 for result in result_list:
                        #                                     result_holder = ResultHolder()
                        #                                     result_holder.routing = routing
                        #                                     result_holder.mtr_name = None
                        #                                     result_holder.path_finding_method = path_finding_method
                        #                                     result_holder.algorithm = algorithm
                        #                                     result_holder.lwr = lwr
                        #                                     result_holder.k = k
                        #                                     result_holder.mcdm_objective = mcdm_objective
                        #                                     result_holder.cwr = cwr
                        #                                     result_holder.w_srt = w_srt
                        #                                     result_holder.w_tt = w_tt
                        #                                     result_holder.w_length = w_length
                        #                                     result_holder.w_util = w_util
                        #                                     result_holder.wpm_version = wpm_version
                        #                                     result_holder.wpm_value_type = wpm_value_type
                        #                                     result_holder.metaheuristic_name = "GRASP"
                        #                                     result_holder.evaluator_name = "avbLatencyMathTSNCF"
                        #                                     result_holder.topology_result = result
                        #                                     outputs_list.append(result_holder)

                        elif "U" in algorithm:
                            k_path = os.path.join(algorithm_path, algorithm)
                            k_list = os.listdir(k_path)
                            for k in k_list:
                                result_path = os.path.join(k_path, k)
                                result_list = create_result(result_path)
                                for result in result_list:
                                    result_holder = ResultHolder()
                                    result_holder.routing = routing
                                    result_holder.mtr_name = None
                                    result_holder.path_finding_method = path_finding_method
                                    result_holder.algorithm = algorithm
                                    result_holder.lwr = None
                                    result_holder.k = k
                                    result_holder.mcdm_objective = None
                                    result_holder.cwr = None
                                    result_holder.w_srt = None
                                    result_holder.w_tt = None
                                    result_holder.w_length = None
                                    result_holder.w_util = None
                                    result_holder.wpm_version = None
                                    result_holder.wpm_value_type = None
                                    result_holder.metaheuristic_name = None
                                    result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                    result_holder.topology_result = result
                                    outputs_list.append(result_holder)
                        else:
                            k_path = os.path.join(algorithm_path, algorithm)
                            k_list = os.listdir(k_path)
                            for k in k_list:
                                result_path = os.path.join(k_path, k)
                                result_list = create_result(result_path)
                                for result in result_list:
                                    result_holder = ResultHolder()
                                    result_holder.routing = routing
                                    result_holder.mtr_name = None
                                    result_holder.path_finding_method = path_finding_method
                                    result_holder.algorithm = algorithm
                                    result_holder.lwr = None
                                    result_holder.k = k
                                    result_holder.mcdm_objective = None
                                    result_holder.cwr = None
                                    result_holder.w_srt = None
                                    result_holder.w_tt = None
                                    result_holder.w_length = None
                                    result_holder.w_util = None
                                    result_holder.wpm_version = None
                                    result_holder.wpm_value_type = None
                                    result_holder.metaheuristic_name = "GRASP"
                                    result_holder.evaluator_name = "avbLatencyMathTSNCF"
                                    result_holder.topology_result = result
                                    outputs_list.append(result_holder)

    return outputs_list
