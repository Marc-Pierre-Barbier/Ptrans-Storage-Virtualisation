"""
None of these functions are meant to be used standalone.

these are made to be used with the batch evaluator in solutionEvaluator
"""

import numpy as np
from solutionEvaluator import Evaluation


def mean_entropy(_, new_eval: Evaluation) -> float:
    return int(np.mean([new_eval.entropy.get_capacity(), new_eval.entropy.get_read_bandwidth(), new_eval.entropy.get_read_ops(), new_eval.entropy.get_write_bandwidth(), new_eval.entropy.get_write_ops()]))


def max_entropy(_, new_eval: Evaluation) -> float:
    return int(max([new_eval.entropy.get_capacity(), new_eval.entropy.get_read_bandwidth(), new_eval.entropy.get_read_ops(), new_eval.entropy.get_write_bandwidth(), new_eval.entropy.get_write_ops()]))


def mean_abs_deviation(_, new_eval: Evaluation) -> float:
    return float(np.mean([new_eval.abs_deviation.get_capacity(), new_eval.abs_deviation.get_read_bandwidth(), new_eval.abs_deviation.get_read_ops(), new_eval.abs_deviation.get_write_bandwidth(), new_eval.abs_deviation.get_write_ops()]))


def max_abs_deviation(_, new_eval: Evaluation) -> float:
    return int(max([new_eval.abs_deviation.get_capacity(), new_eval.abs_deviation.get_read_bandwidth(), new_eval.abs_deviation.get_read_ops(), new_eval.abs_deviation.get_write_bandwidth(), new_eval.abs_deviation.get_write_ops()]))


def change_abs_deviation(old_eval: Evaluation, new_eval: Evaluation) -> float:
    return (1 - mean_abs_deviation(None, new_eval / old_eval)) * 100
