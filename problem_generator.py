import copy
from typing import List
from modelization import Problem, Storage, Proposal, ResourceValues, Object
import random

# TODO: pour des raison évidente on peut pas finir sa

# nombre de server par objet
SPEAD = 2


def generate_ressources_from_storages(storages: list[Storage]) -> ResourceValues:
    # generate a usage between 0 and 1
    return storages[0].get_resources_current() * (random.randint(0, 50000) / 50000.)


# usage from 0 to 100
def generate_problem(server_count: int, usage: int, proposals_count: int) -> Problem:
    storages: List[Storage] = []
    proposals: List[Proposal] = []
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
        current = copy.copy(limit)

        current._capacity *= usage
        current._read_ops *= usage
        current._capacity *= usage
        current._read_bandwidth *= usage
        current._write_bandwidth *= usage
        current._write_ops *= usage
        storages.append(Storage(False, current, limit))

    print("Generating objects")

    # TODO: multiple storages / object
    for storage in storages:
        total = copy.copy(storage.get_resources_current())

        while total.get_capacity() > 0:
            ressources = storage.get_resources_limits() * (random.randint(30, 60) / 100)
            if(ressources.get_capacity() > total.get_capacity()):
                objects.append(Object([storage], total))
                break
            total -= ressources
            objects.append(Object([storage], ressources))

    print("Generating proposals")

    for _ in range(proposals_count):
        current_object = objects[random.randint(0, len(objects) - 1)]
        new_storages: List[Storage] = []

        while len(new_storages) != SPEAD:
            storage_id = random.randint(0, len(storages) - 1)
            if storages[storage_id] not in new_storages:
                new_storages.append(storages[storage_id])

        values = generate_ressources_from_storages(current_object.get_locations())

        original_object = Object(current_object.get_locations(), values)
        new_object = Object(new_storages, values)

        proposals.append(Proposal(
            original_object, new_object, 2
        ))

    print("Generation done")

    return Problem(storages, objects, proposals)
