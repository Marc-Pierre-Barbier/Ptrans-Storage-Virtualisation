from modelizations.abstract_modelization import ProblemInstance
from modelizations.basic_to_abstract_modelization import basic_to_abstract_problem
from modelizations.basic_modelization import Problem
from problem_generator import generate_problem


class Solver:
    """A class implementing a solver to choose dynamically a method to solve the problem."""

    def __init__(self, server_count: int, usage: int, proposals_count: int):
        basic_problem: Problem = generate_problem(server_count, usage, proposals_count)
        # Affichage
        self._problem: ProblemInstance = basic_to_abstract_problem(basic_problem)
        # Affichage
        self._solved_problem: ProblemInstance = None

    def set_solved_problem(self, solved_problem: ProblemInstance):
        self._solved_problem = solved_problem
        # Affichage