from modelizations.basic_modelization import Problem, Proposal


LIMITS: dict[int, tuple[str, float]] = {
    0: ('capacity', 1.0),
    1: ('read_ops', 0.5),
    2: ('read_bandwidth', 0.5),
    3: ('write_ops', 0.5),
    4: ('write_bandwidth', 0.5),
}


class Volume:
    """A basic container class."""

    def __init__(self, id: int, limits: dict[int, int], items: list[int]):
        self._id = id
        self._limits: list[int] = limits
        self._items: list[int] = items

    def get_id(self) -> int:
        return self._id

    def get_limits(self) -> dict[int, int]:
        return self._limits


class Item:
    """A basic object class."""

    def __init__(self, id: int, resources: dict[int, int], volumes: list[int]):
        self._id = id
        self._volumes: list[int] = volumes
        self._resources: dict[int, int] = resources

    def get_id(self) -> int:
        return self._id

    def get_volumes(self) -> list[int]:
        return self._volumes

    def get_resources(self) -> dict[int, int]:
        return self._resources


class ProblemInstance:
    """An instance of the problem can be viewed as an object of this class."""

    def __init__(self, basic_problem: Problem):
        volumes: dict[int, Volume] = {}
        items: dict[int, Item] = {}

        for storage in basic_problem.get_storages().values():
            limits: dict[int, int] = {
                0: storage.get_resources_limits().get_capacity(),
                1: storage.get_resources_limits().get_read_bandwidth(),
                2: storage.get_resources_limits().get_read_ops(),
                3: storage.get_resources_limits().get_write_bandwidth(),
                4: storage.get_resources_limits().get_write_ops()
            }

            volumes[storage.get_id()] = Volume(storage.get_id(), limits, storage.get_objects_ids())

        for object in basic_problem.get_objects().values():
            resources: dict[int, int] = {
                0: object.get_resources_values().get_capacity(),
                1: object.get_resources_values().get_read_bandwidth(),
                2: object.get_resources_values().get_read_ops(),
                3: object.get_resources_values().get_write_bandwidth(),
                4: object.get_resources_values().get_write_ops()
            }

            items[object.get_id()] = Item(object.get_id(), resources, object.get_storages_ids())

        self._volumes: list[Volume] = volumes
        self._items: list[Item] = items
        self._proposals: dict[int, Proposal] = basic_problem.get_proposals()

    def get_volumes(self) -> list[Volume]:
        return self._volumes

    def get_items(self) -> list[Item]:
        return self._items

    def get_proposals(self) -> list[Proposal]:
        return self._proposals
