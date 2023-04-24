import copy
from modelizations.basic_modelization import Object, Proposal, ProposalType, ResourceValues, Storage, Problem
import numpy as np
import random


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

    def __init__(self, capacity_max: ResourceValues, capacity_min: ResourceValues | int | float, overfilled_max: ResourceValues | int | float, overfilled_min: ResourceValues | int | float, capacity_spread: float, overfilled_spread: float) -> None:
        if isinstance(capacity_min, ResourceValues) and isinstance(overfilled_max, ResourceValues) and isinstance(overfilled_min, ResourceValues):
            self._constructorA(capacity_max, capacity_min, overfilled_max, overfilled_min, capacity_spread, overfilled_spread)
        elif isinstance(capacity_min, int | float) and isinstance(overfilled_max, int | float) and isinstance(overfilled_min, int | float):
            self._constructorB(capacity_max, capacity_min, overfilled_max, overfilled_min, capacity_spread, overfilled_spread)
        else:
            raise Exception('Invalid parameters')

    def _constructorB(self, capacity_max: ResourceValues, capacity_min: int | float, overfilled_max: int | float, overfilled_min: int | float, capacity_spread: float, overfilled_spread: float):
        if capacity_min > 1 or capacity_min < 0:
            raise Exception('Invalid capacity limit')

        if overfilled_max > 1 or overfilled_max < 0 or overfilled_min > 1 or overfilled_min < 0:
            raise Exception('Invalid overfill specifications')

        self.capacity_spread = capacity_spread
        self.overfilled_spread = overfilled_spread
        self.capacity_max = capacity_max
        self.capacity_min = capacity_max * capacity_min
        self.overfilled_max = capacity_max * overfilled_max
        self.overfilled_min = capacity_max * overfilled_min

    def _constructorA(self, capacity_max: ResourceValues, capacity_min: ResourceValues | None, overfilled_max: ResourceValues | None, overfilled_min: ResourceValues | None, capacity_spread: float, overfilled_spread: float):
        self.capacity_spread = capacity_spread
        self.overfilled_spread = overfilled_spread
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

        delta: ResourceValues = self.overfilled_max - self.overfilled_min

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
    capacity = ResourceValues(
        30000000000000,
        50000,
        3400000000,
        50000,
        491300000,
    )
    return Server_generator(capacity, 0.1, 0.95, 0.90, 0.5, 0.1)


def get_hdd_server():
    capacity = ResourceValues(
        120000000000000,
        320,
        400000000,
        320,
        291300000,
    )
    return Server_generator(capacity, 0.1, 0.95, 0.9, 0.5, 0.1)


class ProblemGenerator:
    file_count: int
    server_count: int
    proposal_count: int
    # Generator : weight the weight define the probability of using this generator
    server_repartition: list[tuple[Server_generator, int]]
    file_generator: File_generator

    def __init__(self, file_count: int, server_count: int, proposal_count: int, server_repartition: list[tuple[Server_generator, int]], file_generator: File_generator) -> None:
        self.file_count = file_count
        self.server_count = server_count
        self.server_repartition = server_repartition
        self.file_generator = file_generator
        self.proposal_count = proposal_count

    def generate(self):
        servers: list[Storage] = []
        server_dict: dict[int, Storage] = {}
        files: list[Object] = []
        files_dict: dict[int, Object] = {}
        proposal_dict: dict[int, list[Proposal]] = {}
        proposals: list[Proposal] = []

        # Generating servers
        wheight_total = 0
        for _generator, weight in self.server_repartition:
            wheight_total += weight

        for id in range(self.server_count):
            index = random.randint(1, wheight_total)

            target_generator = self.server_repartition[0][0]
            for server in self.server_repartition:
                index -= server[1]
                if index < 0:
                    target_generator: Server_generator = server[0]
                    break

            capacity, _ = target_generator.generate_server()

            storage = Storage(id, False, [], capacity, ResourceValues(0, 0, 0, 0, 0))
            servers.append(storage)
            server_dict[id] = storage

        # Generating files
        for id in range(self.file_count):
            file_size = self.file_generator.generate_file()
            new_file = Object(id, [], file_size)
            files.append(new_file)
            files_dict[id] = new_file

        # Binding the files and servers
        for file in files:
            available_servers = copy.copy(servers)
            while len(file.get_storages_ids()) < 2:
                if len(available_servers) == 0:
                    raise Exception('No enough server for the numbers and size of the files')

                index = random.randint(1, len(available_servers)) - 1
                if available_servers[index].get_resources_current() + file.get_resources_values() < available_servers[index].get_resources_limits():
                    available_servers[index].add_object(file.get_id())
                    file.get_storages_ids().append(available_servers[index].get_id())
                available_servers.pop(index)

        available_files = copy.copy(files)
        # Generating proposals
        while len(proposals) < self.proposal_count:
            file_index = 0
            try:
                file_index = random.randint(0, len(available_files) - 1)
                current_file = available_files[file_index]
                current_id = current_file.get_id()

                proposed_storages: list[int] = []
                available_servers = copy.copy(servers)

                while len(proposed_storages) < 2:
                    if len(available_servers) == 0:
                        raise Exception('No enough server for the numbers and size of the files')

                    index = random.randint(1, len(available_servers)) - 1
                    if available_servers[index].get_resources_current() + current_file.get_resources_values() < available_servers[index].get_resources_limits():
                        proposed_storages.append(available_servers[index].get_id())
                    available_servers.pop(index)

                if current_id not in proposal_dict:
                    proposal_dict[current_id] = []
                proposal_dict[current_id].append(Proposal(current_id, current_file.get_id(), proposed_storages, ProposalType.MOVE, 0))
            except Exception:
                available_files.pop(file_index)

        return Problem(self.server_count, server_dict, self.file_count, files_dict, proposal_dict)


if __name__ == "__main__":
    file_max = ResourceValues(
        10000000000,
        1000,
        10000000000,
        1000,
        5000000000
    )

    file_generator = File_generator(file_max, 0.1, 0.2, 0.5)

    generator = ProblemGenerator(300, 10000, 100, [tuple([get_ssd_server(), 20]), tuple([get_hdd_server(), 100])], file_generator)
    problem = generator.generate()
    print(problem)
