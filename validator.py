# TODO: implement a few error checker

from modelizations.basic_modelization import Problem, ResourceValues


def storage_collapser(problem: Problem, storageId: int) -> ResourceValues:
    """Return the usage of each storages, storages_list[i] <=> return[i]"""
    ressouces = ResourceValues(0, 0, 0, 0, 0)
    for id in problem.get_storages()[storageId].get_objects_ids():
        ressouces += problem.get_objects()[id].get_resources_values()

    return ressouces


def check_against_collapse(problem: Problem):
    for storageId, storage in problem.get_storages().items():
        collapsed_storage = storage_collapser(problem, storageId)
        if storage.get_resources_current() != collapsed_storage:
            print(storage.get_resources_current())
            print(collapsed_storage)
            raise Exception("Inconsistent current and computer ressources: " + str(storageId))


def check_problem(problem: Problem):
    return check_against_collapse(problem)
