# This code contains basic error checkers for problems.
# Theses are meant to check when reading something or when generating a file

from modelizations.basic_modelization import Problem, ResourceValues


def storage_collapser(problem: Problem, storage_id: int) -> ResourceValues:
    """Return the usage of each storages, storages_list[i] <=> return[i]"""
    ressources = ResourceValues(0, 0, 0, 0, 0)
    for id in problem.get_storages()[storage_id].get_objects_ids():
        ressources += problem.get_objects()[id].get_resources_values()

    return ressources


def check_against_collapse(problem: Problem):
    for storage in problem.get_storage_list():
        collapsed_storage = storage_collapser(problem, storage.get_id())
        if storage.get_resources_current() != collapsed_storage:
            print(storage.get_resources_current())
            print(collapsed_storage)
            raise Exception("Inconsistent current and computer ressources: " + str(storage.get_id()))


def check_for_overfill(problem: Problem):
    for storage in problem.get_storage_list():
        # only greater if all member of the object are greater. so not < is not the same as >=
        if not storage.get_resources_current().get_capacity() < storage.get_resources_limits().get_capacity():
            raise Exception("Overfilled storage", str(storage.get_id()))


def check_problem(problem: Problem):
    check_against_collapse(problem)
    check_for_overfill(problem)
