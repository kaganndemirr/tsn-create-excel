class TopologyResult:
    def __init__(self, topology_name, o1, o2, o3, average_wcd, max_util, average_util, util_variance, time):
        self.topology_name = topology_name
        self.o1 = str(o1)
        self.o2 = str(o2)
        self.o3 = str(o3)
        self.average_wcd = str(average_wcd)
        self.max_util = str(max_util)
        self.average_util = str(average_util)
        self.util_variance = str(util_variance)
        self.time = str(time)

    def __repr__(self):
        return f"{self.topology_name}, {self.o1}, {self.o2}, {self.o3}, {self.average_wcd}, {self.max_util}, {self.average_util}, {self.util_variance}, {self.time}"
