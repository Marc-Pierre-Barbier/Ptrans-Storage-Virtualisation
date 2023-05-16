import copy
import functools
from modelizations.basic_modelization import Object, Proposal, ProposalType, ResourceValues, Storage, Problem
import numpy as np
import random
from modelizations.parser import store_problem

from validator import check_problem

B = 1
KB = 1024 * B
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB

MAX_TRY = 1000000


class FileGenerator:
    """The file Generator is a class that defines how files should be generated"""
    capacity_max: ResourceValues
    capacity_min: ResourceValues
    average: ResourceValues
    spread: float

    def __init__(self, capacity_max: ResourceValues, capacity_min: ResourceValues | float, average: ResourceValues | float, spread: float) -> None:
        # polymorphism on the constructor can take multiplier of the max value instead of having to manually put everything
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
        # used to calculate the scale argument
        delta = self.capacity_max - self.capacity_min

        return ResourceValues(
            int(abs(np.random.normal(loc=self.average.get_capacity(), scale=self.spread * delta.get_capacity()))),
            int(abs(np.random.normal(loc=self.average.get_read_bandwidth(), scale=self.spread * delta.get_read_bandwidth()))),
            int(abs(np.random.normal(loc=self.average.get_read_ops(), scale=self.spread * delta.get_read_ops()))),
            int(abs(np.random.normal(loc=self.average.get_write_bandwidth(), scale=self.spread * delta.get_write_bandwidth()))),
            int(abs(np.random.normal(loc=self.average.get_write_ops(), scale=self.spread * delta.get_write_ops())))
        )


class ServerGenerator:
    # actual capacity range
    capacity_max: ResourceValues
    capacity_min: ResourceValues
    capacity_spread: float
    average: ResourceValues

    def __init__(self, capacity_max: ResourceValues, capacity_min: ResourceValues | int | float, average: ResourceValues | int | float, capacity_spread: float) -> None:
        # polymorphism on the constructor can take multiplier of the max value instead of having to manually put everything
        if isinstance(capacity_min, ResourceValues) and isinstance(average, ResourceValues):
            self._constructorA(capacity_max, capacity_min, average, capacity_spread)
        elif isinstance(capacity_min, int | float) and isinstance(average, int | float):
            self._constructorB(capacity_max, capacity_min, average, capacity_spread)
        else:
            raise Exception('Invalid parameters')

    def _constructorB(self, capacity_max: ResourceValues, capacity_min: int | float, average: int | float, capacity_spread: float):
        if capacity_min > 1 or capacity_min < 0:
            raise Exception('Invalid capacity limit')

        self.capacity_spread = capacity_spread
        self.capacity_max = capacity_max
        self.capacity_min = capacity_max * capacity_min
        self.average = capacity_max * average

    def _constructorA(self, capacity_max: ResourceValues, capacity_min: ResourceValues, average: ResourceValues, capacity_spread: float):
        self.capacity_spread = capacity_spread
        self.capacity_max = capacity_max
        self.capacity_min = capacity_min
        self.average = average

    def generate_server(self) -> ResourceValues:
        # used to calculate the scale argument
        delta = self.capacity_max - self.capacity_min

        capacity = ResourceValues(
            int(abs(np.random.normal(loc=self.average.get_capacity(), scale=self.capacity_spread * delta.get_capacity()))),
            int(abs(np.random.normal(loc=self.average.get_read_ops(), scale=self.capacity_spread * delta.get_read_ops()))),
            int(abs(np.random.normal(loc=self.average.get_read_bandwidth(), scale=self.capacity_spread * delta.get_read_bandwidth()))),
            int(abs(np.random.normal(loc=self.average.get_write_ops(), scale=self.capacity_spread * delta.get_write_ops()))),
            int(abs(np.random.normal(loc=self.average.get_write_bandwidth(), scale=self.capacity_spread * delta.get_write_bandwidth())))
        )

        return capacity


# Server archetypes presets
# i just assumed that all servers are single drive for the sake of simplicity
# it can be modified by using max *= (count)
def get_ssd_server():
    # Benchmark of my Corsair MP400:
    max = ResourceValues(
        4 * TB,
        90000,
        3 * GB,
        80000,
        2 * GB,
    )

    avg = ResourceValues(
        1 * TB,
        50000,
        1 * GB,
        40000,
        1 * GB,
    )

    return ServerGenerator(max, max * 0.3, avg, 0.5)


def get_hdd_server():
    max = ResourceValues(
        12 * TB,
        320,
        500 * MB,
        320,
        400 * MB,
    )

    min = copy.copy(max)
    min._capacity = min._capacity * 0.1

    avg = copy.copy(max)
    avg._capacity = avg._capacity * 0.25

    return ServerGenerator(max, min, avg, 0.5)


class ProblemGenerator:
    file_count: int
    proposal_count: int
    server_per_file: int
    # Generator : weight the weight define the probability of using this generator
    server_distribution: list[tuple[ServerGenerator, int]]
    file_generator: FileGenerator

    def __init__(self, file_count: int, proposal_count: int, server_distribution: list[tuple[ServerGenerator, int]], file_generator: FileGenerator, server_per_file: int = 2) -> None:
        self.file_count = file_count
        self.server_distribution = server_distribution
        self.file_generator = file_generator
        self.proposal_count = proposal_count
        self.server_per_file = server_per_file

    def generate(self):
        servers: list[Storage] = []
        server_dict: dict[int, Storage] = {}
        files: list[Object] = []
        files_dict: dict[int, Object] = {}
        proposal_dict: dict[int, Proposal] = {}
        proposals: list[Proposal] = []

        # Generating servers
        storage_id = 0
        for generator, weight in self.server_distribution:
            for _ in range(weight):
                capacity = generator.generate_server()
                storage = Storage(storage_id, [], capacity, ResourceValues(0, 0, 0, 0, 0))
                servers.append(storage)
                server_dict[storage_id] = storage
                storage_id += 1

        # Generating files
        for id in range(self.file_count):
            file_size = self.file_generator.generate_file()
            new_file = Object(id, [], file_size)
            files.append(new_file)
            files_dict[id] = new_file

        # Binding the files and servers
        # Files are bound to two different servers
        for file in files:
            # servers for which we aren't bound yet and might be able to be bound
            available_servers = copy.copy(servers)
            while len(file.get_storages_ids()) < self.server_per_file:
                if len(available_servers) == 0:
                    raise Exception('No enough server for the numbers and size of the files')

                # choose a random server
                index = random.randint(1, len(available_servers)) - 1
                server = available_servers.pop(index)
                if server.get_resources_current().get_capacity() + file.get_resources_values().get_capacity() < server.get_resources_limits().get_capacity():
                    server.add_object_id(file.get_id())
                    server.set_resources_current(server.get_resources_current() + file.get_resources_values())
                    file.get_storages_ids().append(server.get_id())
                    file.get_storages_ids().sort()

        # Generating proposals
        # we select a random file an see if it can fit anywhere else, if it can we store the proposal and try again.
        # if it can't we remove the file from the vailable files
        available_files = copy.copy(files)
        previous_proposals_len = 0
        try_count = 0
        while len(proposals) < self.proposal_count:
            if try_count == MAX_TRY:
                print("Could not generate the requested amount of proposals, continuing")
                break

            if previous_proposals_len == len(proposals):
                try_count += 1
            else:
                try_count = 0

            previous_proposals_len = len(proposals)

            file_index = 0
            try:
                file_index = random.randint(0, len(available_files) - 1)
                current_file = available_files[file_index]

                proposed_storages: list[int] = []
                available_servers = copy.copy(servers)

                while len(proposed_storages) < self.server_per_file:
                    if len(available_servers) == 0:
                        raise Exception('No enough server for the numbers and size of the files')

                    index = random.randint(0, len(available_servers) - 1)
                    if available_servers[index].get_resources_current().get_capacity() + current_file.get_resources_values().get_capacity() < available_servers[index].get_resources_limits().get_capacity():
                        proposed_storages.append(available_servers[index].get_id())
                    available_servers.pop(index)

                proposed_storages.sort()

                def reduce_target(acc: list[Proposal], e: Proposal) -> list[Proposal]:
                    if e.get_object_id() == current_file.get_id() and e.get_proposed_storages() == proposed_storages and e.get_proposal_type() == ProposalType.MOVE:
                        acc.append(e)
                    return acc

                if len(functools.reduce(lambda acc, e: reduce_target(acc, e), proposals, [])) == 0 and current_file.get_storages_ids() != proposed_storages:  # type: ignore
                    # not already defined
                    proposal = Proposal(len(proposals), current_file, proposed_storages, ProposalType.MOVE, 0)
                    proposal_dict[proposal.get_id()] = proposal
                    proposals.append(proposal)

            except Exception:
                if len(available_files) > 0:
                    available_files.pop(file_index)

        server_count = functools.reduce(lambda acc, e: e[1] + acc, self.server_distribution, 0)

        prob = Problem(server_count, server_dict, self.file_count, files_dict, proposal_dict)
        check_problem(prob)
        return prob


if __name__ == "__main__":
    file_max = ResourceValues(
        10 * GB,  # 10Gb
        100,
        10,
        10,
        50
    ) * 0.5
    file_generator = FileGenerator(file_max, 0.01, 0.05, 0.5)
    generator = ProblemGenerator(1000, 40000, [(get_ssd_server(), 1), (get_hdd_server(), 2)], file_generator)
    problem = generator.generate()

    store_problem("1k_items_3s", problem)
