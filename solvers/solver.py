from modelizations.abstract_modelization import ProblemInstance
from modelizations.basic_to_abstract_modelization import basic_to_abstract_problem
from problem_generator import generate_problem


class Solver:
    """A class implementing a solver to choose dynamically a method to solve the problem."""

    def __init__(self, server_count: int, usage: int, proposals_count: int):
        self._problem: ProblemInstance = basic_to_abstract_problem(
            generate_problem(server_count, usage, proposals_count)
        )

