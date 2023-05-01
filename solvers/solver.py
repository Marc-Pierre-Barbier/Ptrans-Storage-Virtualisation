from modelizations.abstract_modelization import ProblemInstance
from modelizations.basic_modelization import Problem
from modelizations.parser import parse_problem


class Solver:
    """A class implementing a solver to choose dynamically a method to solve the problem."""

    def __init__(self, path: str):
        self._basic_problem: Problem = parse_problem(path)
        self._basic_problem.log_visualization([0, 1, 2], [0, 1, 2])
        self._problem: ProblemInstance = ProblemInstance(self._basic_problem)
        self._proposals_kept: list[int] = []

    def set_proposals_kept(self, proposals_kept: list[int]) -> None:
        self._proposals_kept: list[int] = proposals_kept

    def update_basic_problem(self) -> None:
        self._basic_problem.update_modelization(self._proposals_kept)
        self._problem: ProblemInstance = ProblemInstance(self._basic_problem)
        self._proposals_kept: list[int] = []
