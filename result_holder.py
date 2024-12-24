class ResultHolder:
    def __init__(self):
        self.solver = None
        self.mtr = None
        self.algorithm = None
        self.randomization = None
        self.normalization = None
        self.cObjective = None
        self.wAVB = None
        self.wTT = None
        self.wLength = None
        self.wUtil = None
        self.method = None
        self.kspwlo_algorithm = None
        self.kspwlo_threshold = None
        self.k = None
        self.ba = None
        self.overload = None
        self.topology_result = None

    def __str__(self):
        return (
            f'{self.solver}, {self.mtr}, {self.algorithm}, {self.randomization}, {self.normalization}, {self.cObjective}, {self.wAVB}, {self.wTT}, {self.wLength}, {self.wUtil}, {self.method}, {self.kspwlo_algorithm}, {self.kspwlo_threshold}, {self.k}, '
            f'{self.ba}, {self.overload}, {self.topology_result.topology_name}, '
            f'{self.topology_result.o1},  {self.topology_result.o2},  {self.topology_result.o3},  {self.topology_result.max_util},  {self.topology_result.time}')

    def get_solver(self):
        return self.solver

    def set_solver(self, solver):
        self.solver = solver

    def get_mtr(self):
        return self.mtr

    def set_mtr(self, mtr):
        self.mtr = mtr

    def get_algorithm(self):
        return self.algorithm

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def get_randomization(self):
        return self.randomization

    def set_randomization(self, randomization):
        self.randomization = randomization

    def get_normalization(self):
        return self.normalization

    def set_normalization(self, normalization):
        self.normalization = normalization

    def get_cObjective(self):
        return self.cObjective

    def set_cObjective(self, cObjective):
        self.cObjective = cObjective

    def get_wAVB(self):
        return self.wAVB

    def set_wAVB(self, wAVB):
        self.wAVB = wAVB

    def get_wTT(self):
        return self.wTT

    def set_wTT(self, wTT):
        self.wTT = wTT

    def get_wLength(self):
        return self.wLength

    def set_wLength(self, wLength):
        self.wLength = wLength

    def get_wUtil(self):
        return self.wUtil

    def set_wUtil(self, wUtil):
        self.wUtil = wUtil

    def get_method(self):
        return self.method

    def set_method(self, method):
        self.method = method

    def get_kspwlo_algorithm(self):
        return self.kspwlo_algorithm

    def set_kspwlo_algorithm(self, kspwlo_algorithm):
        self.kspwlo_algorithm = kspwlo_algorithm

    def get_kspwlo_threshold(self):
        return self.kspwlo_threshold

    def set_kspwlo_threshold(self, kspwlo_threshold):
        self.kspwlo_threshold = kspwlo_threshold

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_ba(self):
        return self.ba

    def set_ba(self, ba):
        self.ba = ba

    def get_overload(self):
        return self.overload

    def set_overload(self, overload):
        self.overload = overload

    def get_topology_result(self):
        return self.topology_result

    def set_topology_result(self, topology_result):
        self.topology_result = topology_result





