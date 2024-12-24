class TopologyResult:
    def __init__(self, topology_name, o1, o2, o3, max_util, average, variance, time):
        self.topology_name = topology_name
        self.o1 = str(o1)
        self.o2 = str(o2)
        self.o3 = str(o3)
        self.max_util = str(max_util)
        self.average = str(average)
        self.variance = str(variance)
        self.time = str(time)