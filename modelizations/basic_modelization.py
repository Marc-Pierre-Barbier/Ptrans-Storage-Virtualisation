from enum import Enum


class ProposalType(Enum):
    UNKNOWN = 0
    ADD = 1
    MOVE = 2
    DELETE = 3


class ResourceValues:
    def __init__(self, capacity: int, read_ops: int, read_bandwidth: int, write_ops: int, write_bandwidth: int) -> None:
        self._capacity = capacity
        self._read_ops = read_ops
        self._read_bandwidth = read_bandwidth
        self._write_ops = write_ops
        self._write_bandwidth = write_bandwidth

    def get_capacity(self) -> int:
        return self._capacity

    def get_read_ops(self) -> int:
        return self._read_ops

    def get_read_bandwidth(self) -> int:
        return self._read_bandwidth

    def get_write_ops(self) -> int:
        return self._write_ops

    def get_write_bandwidth(self) -> int:
        return self._write_bandwidth

    def __str__(self) -> str:
        return "capacity: %.2f\nRops: %.2f\nRband: %.2f\nWops: %.2f\nWband: %.2f" % (self._capacity, self._read_ops, self._read_bandwidth, self._write_ops, self._write_bandwidth)

    def __add__(self, other: 'ResourceValues'):
        return ResourceValues(self._capacity + other._capacity, self._read_ops + other._read_ops, self._read_bandwidth + other._read_bandwidth, self._write_ops + other._write_ops, self._write_bandwidth + other._write_bandwidth)

    def __sub__(self, other: 'ResourceValues'):
        return ResourceValues(self._capacity - other._capacity, self._read_ops - other._read_ops, self._read_bandwidth - other._read_bandwidth, self._write_ops - other._write_ops, self._write_bandwidth - other._write_bandwidth)

    def __mul__(self, other: float):
        return ResourceValues(self._capacity * other, self._read_ops * other, self._capacity * other, self._write_ops * other, self._write_bandwidth * other)

    def __truediv__(self, other: 'ResourceValues'):
        return ResourceValues(self._capacity / other._capacity, self._read_ops / other._read_ops, self._read_bandwidth / other._read_bandwidth, self._write_ops / other._write_ops, self._write_bandwidth / other._write_bandwidth)

    def __gt__(self, other: 'object | ResourceValues') -> bool:
        if isinstance(other, ResourceValues):
            return self._capacity > other._capacity and self._read_bandwidth > other._read_bandwidth and self._read_ops > other._read_ops and self._write_bandwidth > other._write_bandwidth and self._write_ops > other._write_ops
        return False

class Storage:
    def __init__(self, is_working: bool, resources_limits: ResourceValues, resources_current: ResourceValues) -> None:
        self._is_working = is_working
        self._resources_limits = resources_limits
        self._resources_current = resources_current

    def storage_is_working(self) -> bool:
        return self._is_working

    def get_resources_limits(self) -> ResourceValues:
        return self._resources_limits

    def get_resources_current(self) -> ResourceValues:
        return self._resources_current

    def set_is_working(self, working: bool) -> None:
        self._is_working = working

    def set_resources_current(self, resources_current: ResourceValues) -> None:
        self._resources_current = resources_current

    def visualize(self):
        print("Working: " + str(self._is_working))
        print("Usage")
        if self.get_resources_current().get_capacity() > 0:
            print(self.get_resources_limits() / self.get_resources_current() * 100)
        else:
            print(self.get_resources_current())

class Object:
    def __init__(self, locations: list[Storage], resource_values: ResourceValues) -> None:
        self._locations = locations
        self._resource_values = resource_values

    def get_locations(self) -> list[Storage]:
        return self._locations

    def get_resources_values(self) -> ResourceValues:
        return self._resource_values

    def visualize(self):
        print("Present in " + str(len(self._locations)) + "storages")


class Proposal:
    def __init__(self, original_object: Object, proposed_object: Object, proposal_type: ProposalType) -> None:
        self._original_object = original_object
        self._proposed_object = proposed_object
        self._proposal_type = proposal_type

    def get_original_object(self) -> Object:
        return self._original_object

    def get_proposed_object(self) -> Object:
        return self._proposed_object

    def get_proposal_type(self) -> ProposalType:
        return self._proposal_type


class Problem:
    def __init__(self, storages: list[Storage], objects: list[Object], proposals: dict[int, list[Proposal]]) -> None:
        self._storages = storages
        self._objects = objects
        self._proposals = proposals

    def get_storages(self) -> list[Storage]:
        return self._storages

    def get_objects(self) -> list[Object]:
        return self._objects

    def get_proposals(self) -> dict[int, list[Proposal]]:
        return self._proposals

    def visualize(self):
        print("Storages: " + str(len(self._storages)) + " Objects: " + str(len(self._objects)))
        if len(self._storages) > 10 or len(self._objects) > 100:
            raise Exception("The visualisation is too big to make sens")

        print("===== VOLUMES =====")
        for i, vol in enumerate(self._storages):
            print("Volume: " + str(i))
            vol.visualize()
            print("---------")
        print("===================\n")

        print("===== Items =====")
        for i, storage_object in enumerate(self._objects):
            print("Object: " + str(i))
            storage_object.visualize()
            print("---------")
        print("===================\n")
