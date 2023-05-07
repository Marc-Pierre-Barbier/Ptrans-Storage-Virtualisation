from enum import Enum
from itertools import chain
import sys
import numpy as np
import datetime as dt
import bisect

np.set_printoptions(threshold=sys.maxsize)


class ProposalType(Enum):
    UNKNOWN = 0
    ADD = 1
    MOVE = 2
    DELETE = 3

    @staticmethod
    def from_id(id: int) -> 'ProposalType':
        match id:
            case 0:
                return ProposalType.UNKNOWN
            case 1:
                return ProposalType.ADD
            case 2:
                return ProposalType.MOVE
            case 3:
                return ProposalType.DELETE
            case _:
                return ProposalType.UNKNOWN


class ResourceValues:
    def __init__(self, capacity: int | float, read_ops: int | float, read_bandwidth: int | float, write_ops: int | float, write_bandwidth: int | float) -> None:
        self._capacity = float(capacity)
        self._read_ops = float(read_ops)
        self._read_bandwidth = float(read_bandwidth)
        self._write_ops = float(write_ops)
        self._write_bandwidth = float(write_bandwidth)

    def get_capacity(self) -> float:
        return self._capacity

    def get_read_ops(self) -> float:
        return self._read_ops

    def get_read_bandwidth(self) -> float:
        return self._read_bandwidth

    def get_write_ops(self) -> float:
        return self._write_ops

    def get_write_bandwidth(self) -> float:
        return self._write_bandwidth

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ResourceValues):
            return self._capacity == other._capacity and self._read_bandwidth == other._read_bandwidth and self._read_ops == other._read_ops and self._write_bandwidth == other._write_bandwidth and self._write_ops == other._write_ops
        return False

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
    def __init__(self, id: int, objects_ids: list[int], resources_limits: ResourceValues, resources_current: ResourceValues) -> None:
        self._id = id
        self._resources_limits = resources_limits
        self._resources_current = resources_current
        self._objects_ids = objects_ids

    def get_id(self) -> int:
        return self._id

    def get_resources_limits(self) -> ResourceValues:
        return self._resources_limits

    def get_resources_current(self) -> ResourceValues:
        return self._resources_current

    def set_resources_current(self, resources_current: ResourceValues) -> None:
        self._resources_current = resources_current

    def get_objects_ids(self) -> list[int]:
        return self._objects_ids

    def add_object_id(self, object_id: int) -> None:
        i = bisect.bisect_right(self.get_objects_ids(), object_id)
        if i == 0 or self.get_objects_ids()[i - 1] != object_id:
            self._objects_ids.insert(i, object_id)

    def remove_object_id(self, object_id: int) -> None:
        i = bisect.bisect_left(self.get_objects_ids(), object_id)
        if i != len(self.get_objects_ids()) and self.get_objects_ids()[i] == object_id:
            self._objects_ids.pop(i)

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
    def __init__(self, id: int, storages_ids: list[int], resource_values: ResourceValues) -> None:
        self._id = id
        self._storages_ids = storages_ids
        self._resource_values = resource_values

    def get_id(self) -> int:
        return self._id

    def get_storages_ids(self) -> list[int]:
        return self._storages_ids

    def get_resources_values(self) -> ResourceValues:
        return self._resource_values

    def set_storages_ids(self, storages_ids: list[int]) -> None:
        self._storages_id = storages_ids


class Proposal:
    def __init__(self, id: int, object: Object, proposed_storages: list[int], proposal_type: ProposalType, priority: float) -> None:
        self._id = id
        self._object_id = object.get_id()
        self._proposed_storages = proposed_storages
        self._proposal_type = proposal_type
        self._priority = priority
        self._original_storages = object.get_storages_ids()

    def get_id(self) -> int:
        return self._id

    def get_object_id(self) -> int:
        return self._object_id

    def get_item_id(self) -> int:
        return self._object_id

    def get_original_storages(self) -> list[int]:
        return self._original_storages

    def get_original_volumes(self) -> list[int]:
        return self._original_storages

    def get_proposed_storages(self) -> list[int]:
        return self._proposed_storages

    def get_proposed_volumes(self) -> list[int]:
        return self._proposed_storages

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
        return list(self._storages.values())

    def get_object_list(self) -> list[Object]:
        return list(self._objects.values())

    """
        return
            dict[objectid, proposal list]
    """
    def get_proposals(self) -> dict[int, list[Proposal]]:
        return self._proposals

    def get_proposals_list(self) -> list[Proposal]:
        return list(chain(*self._proposals.values()))

    def update_modelization(self, proposals_kept: list[int]) -> None:
        for proposal_id in proposals_kept:
            proposal: Proposal = self.get_proposals()[proposal_id]
            object: Object = self.get_objects()[proposal.get_object_id()]

            for storage_id in object.get_storages_ids():
                self.get_storages()[storage_id].remove_object_id(object.get_id())

            storages_ids: list[int] = proposal.get_proposed_storages()
            object._storages_id = storages_ids
            for storage_id in storages_ids:
                storage: Storage = self.get_storages()[storage_id]

                storage.add_object_id(object.get_id())

    def get_presence_matrix(self) -> np.ndarray:
        presence_matrix = np.full((self.get_object_max_id() + 1, self.get_storage_max_id() + 1), '-       -', 'U9')

        for object in self.get_object_list():
            for storage_id in object.get_storages_ids():
                presence_matrix[object.get_id(), storage_id] = f'({object.get_id()}, {storage_id})    '

        return presence_matrix

    def log_visualization(self, tracked_objects: list[int], tracked_storages: list[int]) -> None:
        with open('basic_visualization/' + dt.datetime.now().ctime().replace(':', '-') + '.txt', 'x') as file:
            file.write(
                'Number of OBJECTS : ' +
                str(len(self._objects)) +
                ' - Number of STORAGES: ' +
                str(len(self._storages)) +
                '\n---------------------\n' +
                'Presence matrix indicating (object, storage) when object is in storage (using indexes)\n\n'
            )
            # file.write(np.array2string(self.get_presence_matrix(), max_line_width=99999999999999))
            for tracked_object in tracked_objects:
                file.write(Tracker(self, self.get_objects()[tracked_object], None, True).track())
            for tracked_storage in tracked_storages:
                file.write(Tracker(self, None, self.get_storages()[tracked_storage], True).track())


class Tracker:
    def __init__(self, problem: Problem, object: Object, storage: Storage | None, in_depth: bool = False) -> None:
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
            for object in self._storage.get_objects_ids():
                objects += Tracker(self._problem, self._problem.get_objects()[object], None).track()
            return header + self._storage.get_full_resources_str() + '\n---------\n' + objects + '\n\n\n---------------------\n\n\n'

    def track_object(self) -> str:
        header: str = f'OBJECT {self._object.get_id()}\n---\n\n'
        if not self._in_depth:
            return header + str(self._object.get_resources_values()) + '\n---\n'
        else:
            storages: str = ''
            for storage in self._object.get_storages_ids():
                storages += Tracker(self._problem, None, self._problem.get_storages()[storage]).track()
            return header + str(self._object.get_resources_values()) + '\n---------\n' + storages + '\n\n\n---------------------\n\n\n'

    def track(self) -> str:
        if self._storage is None:
            return self.track_object()
        else:
            return self.track_storage()
