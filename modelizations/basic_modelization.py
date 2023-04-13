from enum import Enum
import sys
import numpy as np
import pandas as pd
import datetime as dt

np.set_printoptions(threshold=sys.maxsize)

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
        return 'Capacity: %.2f\nRead Ops: %.2f\nRead Bandwidth: %.2f\nWrite Ops: %.2f\nWrite Bandwidth: %.2f\n' % (self._capacity, self._read_ops, self._read_bandwidth, self._write_ops, self._write_bandwidth)

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
    def __init__(self, id: int, is_working: bool, objects_id: list[int], resources_limits: ResourceValues, resources_current: ResourceValues) -> None:
        self._id = id
        self._is_working = is_working
        self._resources_limits = resources_limits
        self._resources_current = resources_current
        self._objects_id = objects_id

    def get_id(self) -> int:
        return self._id

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

    def add_object(self, object_id: int) -> None:
        self._objects_id.append(object_id)

    def get_objects_id(self) -> list[int]:
        return self._objects_id

    def get_full_resources_str(self) -> str:
        resources_current: ResourceValues = self.get_resources_current()
        resources_limits: ResourceValues = self.get_resources_limits()
        resources_percentage: ResourceValues = resources_current / resources_limits * 100

        return 'Capacity: %.2f / %.2f (%.2f)\nRead Ops: %.2f / %.2f (%.2f)\nRead Bandwidth: %.2f / %.2f (%.2f)\nWrite Ops: %.2f / %.2f (%.2f)\nWrite Bandwidth: %.2f / %.2f (%.2f)\n' % (
            resources_current.get_capacity(),
            resources_limits.get_capacity(),
            resources_percentage.get_capacity(),
            resources_current.get_read_ops(),
            resources_limits.get_read_ops(),
            resources_percentage.get_read_ops(),
            resources_current.get_read_bandwidth(),
            resources_limits.get_read_bandwidth(),
            resources_percentage.get_read_bandwidth(),
            resources_current.get_write_ops(),
            resources_limits.get_write_ops(),
            resources_percentage.get_write_ops(),
            resources_current.get_write_bandwidth(),
            resources_limits.get_write_bandwidth(),
            resources_percentage.get_write_bandwidth()
        )


class Object:
    def __init__(self, id: int, storages_id: list[int], resource_values: ResourceValues) -> None:
        self._id = id
        self._storages_id = storages_id
        self._resource_values = resource_values

    def get_id(self) -> int:
        return self._id

    def get_storages_id(self) -> list[int]:
        return self._storages_id

    def get_resources_values(self) -> ResourceValues:
        return self._resource_values


class Proposal:
    def __init__(self, original_object: Object, proposed_object: Object, proposal_type: ProposalType, priority: float) -> None:
        self._original_object = original_object
        self._proposed_object = proposed_object
        self._proposal_type = proposal_type
        self._priority = priority

    def get_original_object(self) -> Object:
        return self._original_object

    def get_proposed_object(self) -> Object:
        return self._proposed_object

    def get_proposal_type(self) -> ProposalType:
        return self._proposal_type

    def get_priority(self) -> float:
        return self._priority


class Problem:
    def __init__(self, storage_max_id: int, storages: dict[int, Storage], object_max_id: int, objects: dict[int, Object], proposals: dict[int, list[Proposal]]) -> None:
        self._storage_max_id = storage_max_id
        self._storages = storages
        self._object_max_id = object_max_id
        self._objects = objects
        self._proposals = proposals

    def get_storage_max_id(self) -> int:
        return self._storage_max_id

    def get_storages(self) -> dict[int, Storage]:
        return self._storages

    def get_object_max_id(self) -> int:
        return self._object_max_id

    def get_objects(self) -> dict[int, Object]:
        return self._objects

    def get_storage_list(self) -> list[Storage]:
        return self._storages.values()

    def get_object_list(self) -> list[Object]:
        return self._objects.values()

    def get_proposals(self) -> dict[int, list[Proposal]]:
        return self._proposals

    def get_presence_matrix(self) -> np.ndarray:
        presence_matrix = np.full((self.get_object_max_id() + 1, self.get_storage_max_id() + 1), '-       -', 'U9')

        for object in self.get_object_list():
            for storage_id in object.get_storages_id():
                presence_matrix[object.get_id(), storage_id] = f'({object.get_id()}, {storage_id})    '

        return presence_matrix

    def log_visualization(self, tracked_objects: list[int], tracked_storages: list[int]):
        with open('basic_visualization/' + dt.datetime.now().ctime().replace(':', '-') + '.txt', 'x') as file:
            file.write(
                'Number of OBJECTS : ' +\
                str(len(self._objects)) +\
                ' - Number of STORAGES: ' +\
                str(len(self._storages)) +\
                '\n---------------------\n' +\
                'Presence matrix indicating (object, storage) when object is in storage (using indexes)\n\n'
            )
            file.write(np.array2string(self.get_presence_matrix(), max_line_width=99999999999999))
            for tracked_object in tracked_objects:
                file.write(Tracker(self, self.get_objects()[tracked_object], None, True).track())
            for tracked_storage in tracked_storages:
                file.write(Tracker(self, None, self.get_storages()[tracked_storage], True).track())


class Tracker:
    def __init__(self, problem: Problem, object: Object, storage: Storage, in_depth: bool = False) -> None:
        self._problem = problem
        self._object = object
        self._storage = storage
        self._in_depth = in_depth

    def track_storage(self) -> str:
        header: str = f'STORAGE {self._storage.get_id()}\n---\n'
        if not self._in_depth:
            return header + self._storage.get_full_resources_str()
        else:
            objects: str = ''
            for object in self._storage.get_objects_id():
                objects += Tracker(self._problem, self._problem.get_objects()[object], None).track()
            return header + self._storage.get_full_resources_str() + '\n---------\n' + objects + '\n\n\n---------------------\n\n\n'

    def track_object(self) -> str:
        header: str = f'OBJECT {self._object.get_id()}\n---\n\n'
        if not self._in_depth:
            return header + str(self._object.get_resources_values()) + '\n---\n'
        else:
            storages: str = ''
            for storage in self._object.get_storages_id():
                storages += Tracker(self._problem, None, self._problem.get_storages()[storage]).track()
            return header + str(self._object.get_resources_values()) + '\n---------\n' + storages + '\n\n\n---------------------\n\n\n'

    def track(self) -> str:
        if self._storage is None:
            return self.track_object()
        else:
            return self.track_storage()