# TODO: implement a few error checker

from modelizations.basic_modelization import Problem, ResourceValues


def storage_collapser(problem: Problem, storageId: int) -> ResourceValues:
    """Return the usage of each storages, storages_list[i] <=> return[i]"""
    ressouces = ResourceValues(0, 0, 0, 0, 0)
    for id in problem.get_storages()[storageId].get_objects_ids():
        ressouces += problem.get_objects()[id].get_resources_values()

    return ressouces


def check_against_collapse(problem: Problem):
    for storage in problem.get_storage_list():
        collapsed_storage = storage_collapser(problem, storage.get_id())
        if storage.get_resources_current() != collapsed_storage:
            print(storage.get_resources_current())
            print(collapsed_storage)
            raise Exception("Inconsistent current and computer ressources: " + str(storage.get_id()))


def check_for_overfill(problem: Problem):
    for storage in problem.get_storage_list():
        if storage.get_resources_current() > storage.get_resources_limits():
            raise Exception("Overfilled storage", str(storage.get_id()))


def check_problem(problem: Problem):
    check_against_collapse(problem)
    check_for_overfill(problem)
