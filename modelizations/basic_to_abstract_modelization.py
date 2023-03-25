from modelizations.basic_modelization import *
from modelizations.abstract_modelization import *


def basic_to_abstract_problem(basic_problem: Problem) -> ProblemInstance:
    volumes: dict[Storage, Volume] = {}
    items: dict[Object, dict[Volume, Resources]] = {}

    for storage in basic_problem.get_storages():
        limits: list[int] = [
            storage.get_resources_limits().get_capacity(),
            storage.get_resources_limits().get_read_bandwidth(),
            storage.get_resources_limits().get_read_ops(),
            storage.get_resources_limits().get_write_bandwidth(),
            storage.get_resources_limits().get_write_ops()
        ]
        efficiencies: list[int] = []
        resources_used: list[int] = [
            storage.get_resources_current().get_capacity(),
            storage.get_resources_current().get_read_bandwidth(),
            storage.get_resources_current().get_read_ops(),
            storage.get_resources_current().get_write_bandwidth(),
            storage.get_resources_current().get_write_ops()
        ]

        volumes[storage] = (Volume(limits, efficiencies, resources_used))

    for object in basic_problem.get_objects():
        instances: dict[Volume, Resources] = {}

        for location in object.get_locations():
            resources_used: list[int] = [
                object.get_resources_values().get_capacity(),
                object.get_resources_values().get_read_bandwidth(),
                object.get_resources_values().get_read_ops(),
                object.get_resources_values().get_write_bandwidth(),
                object.get_resources_values().get_write_ops()
            ]

            instances[volumes[location]] = Resources(resources_used, [])

        items[object] = instances

    # for now we don't explore proposals

    volume_list: list[Volume] = volumes.values()
    item_list: list[Item] = [Item(instance, []) for instance in items.values()]

    return ProblemInstance(volume_list, item_list)
