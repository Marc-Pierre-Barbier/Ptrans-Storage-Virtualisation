from enum import Enum


class Volume:
    """A basic container class."""

    def __init__(self, limits: list[int], efficiencies: list[int], resources_used: list[int]):
        self._limits: list[int] = limits  # cannot be skipped
        self._resources_used: list[int] = resources_used
        self._efficiencies: list[int] = efficiencies
        # maybe we should add a priority for each efficiency. does it come from characteristics?
        # self._location -> could be a leaf of a tree representing the geographical regions
        # self._state -> enumeration of the different states of the node (OK, no response, ...)

    def get_limits(self) -> list[int]:
        return self._limits

    def get_efficiencies(self) -> list[int]:
        return self._efficiencies

    def get_resources_used(self) -> list[int]:
        return self._resources_used


class ConditionType(Enum):
    RESOURCE_CONDITION = 0,
    LOCATION_CONDITION = 1
    # To be continued...


class Condition:
    """A class describing what an item needs and what is the priority, in percentages, of this need."""

    def __init__(self, condition_type: ConditionType, priority: float, **kwargs):
        """We shall add more documentation here."""
        self._type: ConditionType = condition_type
        self._priority = priority
        # kwargs is a dictionary used to add named variables only
        # for example :
        self.val = kwargs.get('val', "default value")
        # should be called as Condition(conditionType, priority, val="value")

    def get_condition_type(self) -> ConditionType:
        return self._type

    def get_priority(self) -> float:
        return self._priority


class Resources:
    """A class describing resources for an item."""

    def __init__(self, resources_used, utilities):
        self._resources_used: list[int] = resources_used
        self._utilities: list[int] = utilities

    def get_resources_used(self) -> list[int]:
        return self._resources_used

    def get_utilities(self) -> list[int]:
        return self._utilities


class Item:
    """A basic object class."""

    def __init__(self, instances: dict[Volume, Resources], conditions: list[Condition]):
        self._instances: dict[Volume, Resources] = instances  # can be null if the item is not placed
        self._conditions: list[Condition] = conditions
        # self._synchronization: bool = true -> is the object synchronized well?
        # self._state -> enumeration of the different states of the object
        # (what does it look like? maybe object in the system or not?)

    def get_instances(self) -> dict[Volume, Resources]:
        return self._instances

    def get_conditions(self) -> list[Condition]:
        return self._conditions


class ProblemInstance:
    """An instance of the problem can be viewed as an object of this class."""

    def __init__(self, volumes: list[Volume], items: list[Item]):
        self._volumes: list[Volume] = volumes
        self._items: list[Item] = items

    def get_volumes(self) -> list[Volume]:
        return self._volumes

    def get_items(self) -> list[Item]:
        return self._items
