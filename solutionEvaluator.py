from math import isclose, log, sqrt
import os
from typing import Callable
import numpy as np
from modelizations.basic_modelization import Problem, ResourceValues, Storage
from modelizations.parser import parse_problem
from validator import check_problem


def absolute_deviation(list: list[float]) -> float:
    mean = float(np.mean(list))
    dev: float = 0
    for i in list:
        dev = dev + abs(i - mean)
    return dev


def entropy(data: list[float]) -> float:
    # rounding to a limited number of decimal places is essencial to determine the density
    data = list(map(lambda a: round(a, 2), data))

    _, counts = np.unique(data, return_counts=True)
    probs = counts / len(data)
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.

    for i in probs:
        ent -= i * log(i, 2)

    return ent


def moy_ecart_type(list: list[float]) -> tuple[float, float, float]:
    avg = float(np.average(list))
    avg_of_cubed = float(np.average(np.multiply(list, list)))

    if isclose(avg * avg, avg_of_cubed):
        return (avg, 0, 0)

    var = avg_of_cubed - (avg * avg)

    return (avg, var, sqrt(var))


# take a function that convert a list of values to a score
# this way we can compute both the entrop and absolude deviation using a single function
def problem_agregator(problem: Problem, algorithm: Callable[[list[float]], float]) -> ResourceValues:
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
        algorithm(capacities),
        algorithm(w_iops),
        algorithm(r_iops),
        algorithm(w_bandwidth),
        algorithm(r_bandwidth)
    )


class Stats:
    mean: float = 0
    var: float = 0
    dev: float = 0

    def __init__(self, mean: float, var: float, dev: float) -> None:
        self.mean = mean
        self.var = var
        self.dev = dev


def problem_stats(problem: Problem) -> dict[str, Stats]:
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

    results: dict[str, Stats] = {}

    # calcule de l'entropie
    capacities = list(map(get_capacity, ressources))
    r_capacities = moy_ecart_type(capacities)
    results["capacity"] = Stats(r_capacities[0], r_capacities[1], r_capacities[2])

    w_iops = list(map(get_w_iops, ressources))
    r_w_iops = moy_ecart_type(w_iops)
    results["w_iops"] = Stats(r_w_iops[0], r_w_iops[1], r_w_iops[2])

    r_iops = list(map(get_r_iops, ressources))
    r_r_iops = moy_ecart_type(r_iops)
    results["r_iops"] = Stats(r_r_iops[0], r_r_iops[1], r_r_iops[2])

    w_bandwidth = list(map(get_w_bandwidth, ressources))
    r_w_bandwidth = moy_ecart_type(w_bandwidth)
    results["w_bandwidth"] = Stats(r_w_bandwidth[0], r_w_bandwidth[1], r_w_bandwidth[2])

    r_bandwidth = list(map(get_r_bandwidth, ressources))
    r_r_bandwidth = moy_ecart_type(r_bandwidth)
    results["r_bandwidth"] = Stats(r_r_bandwidth[0], r_r_bandwidth[1], r_r_bandwidth[2])

    return results


class Evaluation:
    entropy: ResourceValues
    abs_deviation: ResourceValues
    stats: dict[str, Stats] | None

    def __init__(self, entropy: ResourceValues, abs_deviation: ResourceValues, stats: dict[str, Stats] | None) -> None:
        self.entropy = entropy
        self.abs_deviation = abs_deviation
        self.stats = stats

    def __str__(self) -> str:
        return f"Abs deviation lower is better: \n{self.abs_deviation}"

    def __truediv__(self, other: 'Evaluation') -> 'Evaluation':
        return Evaluation(self.entropy / other.entropy, self.abs_deviation / other.abs_deviation, None)

    def __mul__(self, other: int) -> 'Evaluation':
        return Evaluation(self.entropy * 100, self.abs_deviation * 100, None)


def evaluate(problem: Problem) -> Evaluation:
    entropy_result = problem_agregator(problem, entropy)
    deviation_result = problem_agregator(problem, absolute_deviation)
    stats = problem_stats(problem)

    return Evaluation(entropy_result, deviation_result, stats)


# to use this function you need to provide a scoring function, look in scoring.py
def batch_evaluate(solver: Callable[[Problem], Problem], monoscore: Callable[[Evaluation, Evaluation], float] = (lambda _, __: 0), print_score: bool = True) -> dict[str, tuple[Evaluation, Evaluation, float]]:
    """Evaluate a solver using problems in the data_sample directory

    Parameters
    ----------
    solver : Callable[[Problem], Problem]
        the solver to call
    monoscore : Callable[[Evaluation, Evaluation], float], optional
        function used to generate the score
    print_score : bool, optional
        use print() to display the score when computed

    Returns
    -------
    dict[str, tuple[Evaluation, Evaluation, float]]
        the key of the dict is the name of the file in data_sample,
        the tuple containse in order the evaluation before the solver, then the evaluation after and finally the score
    """
    evals: dict[str, tuple[Evaluation, Evaluation, float]] = {}

    # validate all problem files before running.
    for file in os.scandir("data_sample"):
        if file.name.endswith("txt"):
            prob: Problem = parse_problem(file.path)
            check_problem(prob)

    # run all tests
    for file in os.scandir("data_sample"):
        if file.name.endswith("txt"):
            print("evaluating: " + file.name)
            prob = parse_problem(file.path)
            evaluation_before = evaluate(prob)
            evaluation_after = evaluate(solver(prob))
            score = monoscore(evaluation_before, evaluation_after)
            evals[file.name] = (evaluation_before, evaluation_after, score)

            if print_score:
                print(score)

    # return for automations
    return evals
