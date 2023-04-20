from modelizations.basic_modelization import ResourceValues
import numpy as np


class File_generator:
    capacity_max: ResourceValues
    capacity_min: ResourceValues
    average: ResourceValues
    spread: float

    def __init__(self, capacity_max: ResourceValues, capacity_min: ResourceValues | float, average: ResourceValues | float, spread: float) -> None:
        if isinstance(capacity_min, ResourceValues) and isinstance(average, ResourceValues):
            self._constructorA(capacity_max, capacity_min, average, spread)
        elif isinstance(capacity_min, int | float) and isinstance(average, int | float):
            self._constructorB(capacity_max, capacity_min, average, spread)
        else:
            raise Exception('Invalid parameters')

    def _constructorA(self, capacity_max: ResourceValues, capacity_min: ResourceValues, average: ResourceValues, spread: float):
        self.capacity_max = capacity_max
        self.capacity_min = capacity_min
        self.average = average
        self.spread = spread

    def _constructorB(self, capacity_max: ResourceValues, capacity_min: float, average: float, spread: float):
        self.capacity_max = capacity_max
        self.capacity_min = capacity_max * capacity_min
        self.average = capacity_max * average
        self.spread = spread

    def generate_file(self):
        delta = self.capacity_max - self.capacity_min

        return ResourceValues(
            int(abs(np.random.normal(loc=delta.get_capacity(), scale=self.spread * self.capacity_min.get_capacity()))) + self.capacity_min.get_capacity(),
            int(abs(np.random.normal(loc=delta.get_read_bandwidth(), scale=self.spread * self.capacity_min.get_read_bandwidth()))) + self.capacity_min.get_read_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_read_ops(), scale=self.spread * self.capacity_min.get_read_ops()))) + self.capacity_min.get_read_ops(),
            int(abs(np.random.normal(loc=delta.get_write_bandwidth(), scale=self.spread * self.capacity_min.get_write_bandwidth()))) + self.capacity_min.get_write_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_write_ops(), scale=self.spread * self.capacity_min.get_write_ops()))) + self.capacity_min.get_write_ops()
        )


class Server_generator:
    # a which point we define if a storage is overfilled
    overfilled_max: ResourceValues
    overfilled_min: ResourceValues
    overfilled_spread: float

    # actual capacity range
    capacity_max: ResourceValues
    capacity_min: ResourceValues
    capacity_spread: float

    def __init__(self, capacity_max: ResourceValues, capacity_min: ResourceValues | int | float, overfilled: ResourceValues | int | float, overfilled_acuracy: ResourceValues | int | float) -> None:
        if isinstance(capacity_min, ResourceValues) and isinstance(overfilled, ResourceValues) and isinstance(overfilled_acuracy, ResourceValues):
            self._constructorA(capacity_max, capacity_min, overfilled, overfilled_acuracy)
        elif isinstance(capacity_min, int | float) and isinstance(overfilled, int | float) and isinstance(overfilled_acuracy, int | float):
            self._constructorB(capacity_max, capacity_min, overfilled, overfilled_acuracy)
        else:
            raise Exception('Invalid parameters')

    def _constructorB(self, capacity_max: ResourceValues, capacity_min: int | float, overfilled: int | float, overfilled_acuracy: int | float):
        if capacity_min > 1 or capacity_min < 0:
            raise Exception('Invalid capacity limit')

        if overfilled > 1 or overfilled < 0 or overfilled_acuracy > 1 or overfilled_acuracy < 0:
            raise Exception('Invalid overfill specifications')

        self.capacity_max = capacity_max
        self.capacity_min = capacity_max * capacity_min
        self.overfilled_max = capacity_max * (overfilled + overfilled_acuracy)
        self.overfilled_min = capacity_max * (overfilled - overfilled_acuracy)

    def _constructorA(self, capacity_max: ResourceValues, capacity_min: ResourceValues | None, overfilled_max: ResourceValues | None, overfilled_min: ResourceValues | None):
        self.capacity_max = capacity_max
        self.capacity_min = capacity_min if capacity_min is not None else capacity_max
        self.overfilled_max = overfilled_max if overfilled_max is not None else capacity_max
        self.overfilled_min = overfilled_min if overfilled_min is not None else capacity_max

    def generate_server(self) -> tuple[ResourceValues, ResourceValues]:
        delta = self.capacity_max - self.capacity_min

        capacity = ResourceValues(
            int(abs(np.random.normal(loc=delta.get_capacity(), scale=self.capacity_spread * self.capacity_min.get_capacity()))) + self.capacity_min.get_capacity(),
            int(abs(np.random.normal(loc=delta.get_read_bandwidth(), scale=self.capacity_spread * self.capacity_min.get_read_bandwidth()))) + self.capacity_min.get_read_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_read_ops(), scale=self.capacity_spread * self.capacity_min.get_read_ops()))) + self.capacity_min.get_read_ops(),
            int(abs(np.random.normal(loc=delta.get_write_bandwidth(), scale=self.capacity_spread * self.capacity_min.get_write_bandwidth()))) + self.capacity_min.get_write_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_write_ops(), scale=self.capacity_spread * self.capacity_min.get_write_ops()))) + self.capacity_min.get_write_ops()
        )

        delta: ResourceValues = self.overfilled_max - self.overfilled_max

        overfilled = ResourceValues(
            int(abs(np.random.normal(loc=delta.get_capacity(), scale=self.overfilled_spread * self.overfilled_min.get_capacity()))) + self.overfilled_min.get_capacity(),
            int(abs(np.random.normal(loc=delta.get_read_bandwidth(), scale=self.overfilled_spread * self.overfilled_min.get_read_bandwidth()))) + self.overfilled_min.get_read_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_read_ops(), scale=self.overfilled_spread * self.overfilled_min.get_read_ops()))) + self.overfilled_min.get_read_ops(),
            int(abs(np.random.normal(loc=delta.get_write_bandwidth(), scale=self.overfilled_spread * self.overfilled_min.get_write_bandwidth()))) + self.overfilled_min.get_write_bandwidth(),
            int(abs(np.random.normal(loc=delta.get_write_ops(), scale=self.overfilled_spread * self.overfilled_min.get_write_ops()))) + self.overfilled_min.get_write_ops()
        )

        return tuple([capacity, overfilled])


# Server archetypes presets
# i just assumed that all servers are single drive for the sake of simplicity
# it can be modified by using max *= (count)
def get_ssd_server():
    # Benchmark of my Corsair MP400:
    max = ResourceValues(
        30000000000000,
        50000,
        3400000000,
        50000,
        491300000,
    )
    return Server_generator(max, 0.1, max, max)


def get_hdd_server():
    max = ResourceValues(
        120000000000000,
        320,
        400000000,
        320,
        291300000,
    )
    return Server_generator(max, 0.1, max, max)


class Problem_generator:
    file_count: int
    server_count: int
    # Generator : weight the weight define the probability of using this generator
    server_repartition: dict[Server_generator, float]
    file_generator: File_generator

    def __init__(self, file_count: int, server_count: int, server_repartition: dict[float, Server_generator], file_generator: File_generator) -> None:
        self.file_count = file_count
        self.server_count = server_count
        self.server_repartition = server_repartition
        self.file_generator = file_generator

    def generate(self):
        pass
