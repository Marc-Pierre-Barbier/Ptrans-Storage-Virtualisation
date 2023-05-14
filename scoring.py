"""
None of these functions are meant to be used standalone.

these are made to be used with the batch evaluator in solutionEvaluator
"""

import numpy as np
from solutionEvaluator import evaluation


def mean_entropy(eval: evaluation) -> int:
    return int(np.mean([eval.entropy.get_capacity(), eval.entropy.get_read_bandwidth(), eval.entropy.get_read_ops(), eval.entropy.get_write_bandwidth(), eval.entropy.get_write_ops()]))


def max_entropy(eval: evaluation) -> int:
    return int(max([eval.entropy.get_capacity(), eval.entropy.get_read_bandwidth(), eval.entropy.get_read_ops(), eval.entropy.get_write_bandwidth(), eval.entropy.get_write_ops()]))


def mean_abs_deviation(eval: evaluation) -> int:
    return int(np.mean([eval.abs_deviation.get_capacity(), eval.abs_deviation.get_read_bandwidth(), eval.abs_deviation.get_read_ops(), eval.abs_deviation.get_write_bandwidth(), eval.abs_deviation.get_write_ops()]))


def max_abs_deviation(eval: evaluation) -> int:
    return int(max([eval.abs_deviation.get_capacity(), eval.abs_deviation.get_read_bandwidth(), eval.abs_deviation.get_read_ops(), eval.abs_deviation.get_write_bandwidth(), eval.abs_deviation.get_write_ops()]))
