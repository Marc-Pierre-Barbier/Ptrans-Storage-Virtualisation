from math import isclose, log, sqrt
import numpy as np
from modelizations.basic_modelization import Problem, ResourceValues, Storage


def absolute_deviation(list: list[int], mean: float) -> float:
    dev = 0
    for i in list:
        dev = dev + abs(i - mean)
    return dev


def entropy(list: list[float]) -> float:
    _, counts = np.unique(list, return_counts=True)
    probs = counts / len(list)
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.

    # Compute entropy
    for i in probs:
        ent -= 100 * i * i * log(i, 2)

    return ent


def moy_ecart_type(list: list[float]) -> tuple[float, float, float]:
    avg = float(np.average(list))
    avg_of_cubed = float(np.average(np.multiply(list, list)))

    if isclose(avg * avg, avg_of_cubed):
        return (avg, 0, 0)

    var = avg_of_cubed - (avg * avg)

    return (avg, var, sqrt(var))


def problem_entropy(problem: Problem) -> ResourceValues:
    if len(problem.get_storages()) <= 1:
        return ResourceValues(0, 0, 0, 0, 0)

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

    ressources = list(map(get_ressources, problem.get_storage_list()))

    # calcule de l'entropie
    capacities = list(map(get_capacity, ressources))
    w_iops = list(map(get_w_iops, ressources))
    r_iops = list(map(get_r_iops, ressources))
    w_bandwidth = list(map(get_w_bandwidth, ressources))
    r_bandwidth = list(map(get_r_bandwidth, ressources))

    return ResourceValues(
        entropy(capacities),
        entropy(w_iops),
        entropy(r_iops),
        entropy(w_bandwidth),
        entropy(r_bandwidth)
    )


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

    ressources = list(map(get_ressources, problem.get_storage_list()))

    # calcule de l'entropie
    capacities = list(map(get_capacity, ressources))
    r_capacities = moy_ecart_type(capacities)
    print("Capacite: AVG=%.4f VAR=%.4f ECType=%.4f" % (r_capacities[0], r_capacities[1], r_capacities[2]))

    w_iops = list(map(get_w_iops, ressources))
    r_w_iops = moy_ecart_type(w_iops)
    print("W_IOPS: AVG=%.4f VAR=%.4f ECType=%.4f" % (r_w_iops[0], r_w_iops[1], r_w_iops[2]))

    r_iops = list(map(get_r_iops, ressources))
    r_r_iops = moy_ecart_type(r_iops)
    print("R_IOPS: AVG=%.4f VAR=%.4f ECType=%.4f" % (r_r_iops[0], r_r_iops[1], r_r_iops[2]))

    w_bandwidth = list(map(get_w_bandwidth, ressources))
    r_w_bandwidth = moy_ecart_type(w_bandwidth)
    print("W_Bandwidth: AVG=%.4f VAR=%.4f ECType=%.4f" % (r_w_bandwidth[0], r_w_bandwidth[1], r_w_bandwidth[2]))

    r_bandwidth = list(map(get_r_bandwidth, ressources))
    r_r_bandwidth = moy_ecart_type(r_bandwidth)
    print("R_Bandwidth: AVG=%.4f VAR=%.4f ECType=%.4f" % (r_r_bandwidth[0], r_r_bandwidth[1], r_r_bandwidth[2]))


def evaluate(problem: Problem):
    entropy = problem_entropy(problem)
    print("===== ENTROPY (lower is better) =====")
    print(entropy)
    print("===== STATS =====")
    problem_stats(problem)
