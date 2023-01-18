from math import log
import numpy as np
from modelization import Problem, ResourceValues, Storage
from problem_generator import generate_problem

# TODO: ici on ne regarde que l'étant du stockage il faut donc une fonction qui prends les proposition retenu et qui extrait le stockage aprés transformation


def entropy(list: list[int]) -> float:
    _, counts = np.unique(list, return_counts=True)
    probs = counts / len(list)
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.

    # Compute entropy
    for i in probs:
        ent -= i * log(i)

    return ent


def problem_entropy(problem: Problem) -> ResourceValues:
    result = ResourceValues(0, 0, 0, 0, 0)
    if len(problem.get_storages()) <= 1:
        return result

    def get_ressources(storage: Storage):
        return storage.get_resources_current() / storage.get_resources_limits()

    def get_capacity(storage: ResourceValues):
        return storage.get_capacity()

    def get_r_iops(storage: ResourceValues):
        return storage.get_read_ops()

    def get_w_iops(storage: ResourceValues):
        return storage.get_write_ops()

    def get_r_bandwidth(storage: ResourceValues):
        return storage.get_read_bandwidth()

    def get_w_bandwidth(storage: ResourceValues):
        return storage.get_write_bandwidth()

    ressources = list(map(get_ressources, problem.get_storages()))

    # calcule de l'entropie
    capacities = list(map(get_capacity, ressources))
    result._capacity = entropy(capacities)

    w_iops = list(map(get_w_iops, ressources))
    result._write_ops = entropy(w_iops)

    r_iops = list(map(get_r_iops, ressources))
    result._read_ops = entropy(r_iops)

    w_bandwidth = list(map(get_w_bandwidth, ressources))
    result._write_bandwidth = entropy(w_bandwidth)

    r_bandwidth = list(map(get_r_bandwidth, ressources))
    result._read_bandwidth = entropy(r_bandwidth)

    return result


def evaluate(problem: Problem):
    entropy = problem_entropy(problem)
    print("===== ENTROPY (lower is better) =====")
    print(entropy)


if __name__ == "__main__":
    problem = generate_problem(1000, 35, 0)
    evaluate(problem)
