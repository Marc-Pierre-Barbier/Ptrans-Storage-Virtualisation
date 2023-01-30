import datetime
from math import isclose, log, sqrt
import numpy as np
from modelizations.basic_modelization import Problem, ResourceValues, Storage
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
        ent -= i * log(i, 2)

    return ent


def moy_ecart_type(list: list[int]) -> tuple[float, float, float]:
    avg = float(np.average(list))
    avg_of_cubed = float(np.average(np.multiply(list, list)))

    if isclose(avg * avg, avg_of_cubed):
        return (avg, 0, 0)

    var = avg_of_cubed - (avg * avg)

    print(var)

    return (avg, var, sqrt(var))


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


def problem_stats(problem: Problem) -> None:
    if len(problem.get_storages()) <= 1:
        return

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
    r_capacities = moy_ecart_type(capacities)
    print("CAPCACITE:   AVG=" + str(r_capacities[0]) + "  VAR=" + str(r_capacities[1]) + "  ECType=" + str(r_capacities[2]))

    w_iops = list(map(get_w_iops, ressources))
    r_w_iops = moy_ecart_type(w_iops)
    print("W_IOPS:   AVG=" + str(r_w_iops[0]) + "  VAR=" + str(r_w_iops[1]) + "  ECType=" + str(r_w_iops[2]))

    r_iops = list(map(get_r_iops, ressources))
    r_r_iops = moy_ecart_type(r_iops)
    print("R_IOPS:   AVG=" + str(r_r_iops[0]) + "  VAR=" + str(r_r_iops[1]) + "  ECType=" + str(r_r_iops[2]))

    w_bandwidth = list(map(get_w_bandwidth, ressources))
    r_w_bandwidth = moy_ecart_type(w_bandwidth)
    print("R_IOPS:   AVG=" + str(r_w_bandwidth[0]) + "  VAR=" + str(r_w_bandwidth[1]) + "  ECType=" + str(r_w_bandwidth[2]))

    r_bandwidth = list(map(get_r_bandwidth, ressources))
    r_r_bandwidth = moy_ecart_type(r_bandwidth)
    print("R_IOPS:   AVG=" + str(r_r_bandwidth[0]) + "  VAR=" + str(r_r_bandwidth[1]) + "  ECType=" + str(r_r_bandwidth[2]))


def evaluate(problem: Problem):
    entropy = problem_entropy(problem)
    print("===== ENTROPY (lower is better) =====")
    print(entropy)
    print("===== STATS =====")
    problem_stats(problem)

if __name__ == "__main__":
    time = datetime.datetime.now()
    problem = generate_problem(1000, 20, 0)
    evaluate(problem)
    print("Time spend:" + str(datetime.datetime.now() - time))
