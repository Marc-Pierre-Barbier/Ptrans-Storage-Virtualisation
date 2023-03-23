import copy
from typing import Dict, List
from modelizations.basic_modelization import Problem, ProposalType, Storage, Proposal, ResourceValues, Object
import random

# TODO: pour des raison évidente on peut pas finir sa

# nombre de server par objet
SPEAD = 2


def generate_ressources_from_storages(storages: list[Storage]) -> ResourceValues:
    # generate a usage between 0 and 1
    return storages[0].get_resources_current() * (random.randint(0, 50000) / 50000.)


# usage from 0 to 100
def generate_problem(server_count: int, usage: float, usage_var: float, proposals_count: int) -> Problem:
    storages: List[Storage] = []
    proposals: Dict[int, List[Proposal]] = {}
    objects: List[Object] = []
    usage /= 100.0

    print("Generating servers")

    for _ in range(server_count):
        limit = ResourceValues(
            random.randint(10000, 10000000),
            random.randint(100, 10000),
            random.randint(1, 100),
            random.randint(100, 10000),
            random.randint(1, 100)
        )
        current = ResourceValues(0, 0, 0, 0, 0)

        server_usage = random.randint(int(-usage_var * usage * 10000), int(usage_var * usage * 10000)) / 10000.0 + usage
        server_usage = server_usage if server_usage < 100 and server_usage > 0 else usage

        current._capacity = float(server_usage * limit.get_capacity())
        current._read_ops = float(server_usage * limit.get_read_ops())
        current._read_bandwidth = float(server_usage * limit.get_read_bandwidth())
        current._write_bandwidth = float(server_usage * limit.get_write_bandwidth())
        current._write_ops = float(server_usage * limit.get_write_ops())

        storages.append(Storage(False, limit, current))

    print("Generating objects")

    # TODO: multiple storages / object
    for storage in storages:
        total = copy.copy(storage.get_resources_current())

        while total.get_capacity() > 0:
            ressources = storage.get_resources_current() * (random.randint(50, 100) / 1000.)
            if(ressources.get_capacity() > total.get_capacity()):
                ressources = total

            objects.append(Object([storage], ressources))
            total -= ressources

    print("Generating proposals")

    for _ in range(proposals_count):
        object_index = random.randint(0, len(objects) - 1)
        current_object = objects[object_index]
        new_storages: List[Storage] = []

        while len(new_storages) != SPEAD:
            storage_id = random.randint(0, len(storages) - 1)
            if storages[storage_id] not in new_storages:
                new_storages.append(storages[storage_id])

        new_object = Object(new_storages, current_object.get_resources_values())

        if object_index not in proposals:
            proposals[object_index] = []
        proposals[object_index].append(Proposal(
            current_object, new_object, ProposalType.MOVE
        ))

    print("Generation done")

    return Problem(storages, objects, proposals)
