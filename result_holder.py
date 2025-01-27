class ResultHolder:
    def __init__(self):
        self.routing = None
        self.mtr_name = None
        self.path_finding_method = None
        self.algorithm = None
        self.lwr = None
        self.k = None
        self.wpm_objective = None
        self.wsm_normalization = None
        self.cwr = None
        self.w_srt = None
        self.w_tt = None
        self.w_length = None
        self.w_util = None
        self.wpm_version = None
        self.wpm_value_type = None
        self.metaheuristic_name = None
        self.evaluator_name = None
        self.topology_result = None

    def __repr__(self):
        return (
            f'{self.routing}, {self.mtr_name}, {self.path_finding_method}, {self.algorithm}, {self.lwr}, {self.k}, {self.wpm_objective}, {self.wsm_normalization}, {self.cwr}, '
            f'{self.w_srt}, {self.w_tt}, {self.w_length}, {self.w_util}, {self.wpm_version}, {self.wpm_value_type}, {self.metaheuristic_name},'
            f'{self.evaluator_name}, {self.topology_result.topology_name}, {self.topology_result.o1},  {self.topology_result.o2},'
            f'{self.topology_result.o3}, {self.topology_result.average_wcd}, {self.topology_result.max_util}, {self.topology_result.average_util}, {self.topology_result.util_variance}, {self.topology_result.time}')
