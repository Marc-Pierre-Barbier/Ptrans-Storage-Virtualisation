from problem_generator import ProblemGenerator, ResourceValues, FileGenerator, get_hdd_server, get_ssd_server
from modelizations.basic_modelization import Problem
from modelizations.parser import store_problem
from solvers.proposals_solver import ProposalsSolver, Solver


def create_problem():
    file_max = ResourceValues(
        10000000000,
        1000,
        10000000,
        1000,
        5000000
    )

    file_generator = FileGenerator(file_max, 0.1, 0.2, 0.5)

    generator = ProblemGenerator(30000, 100, [tuple([get_ssd_server(), 20]), tuple([get_hdd_server(), 100])], file_generator)
    problem: Problem = generator.generate()

    problem.log_visualization([0, 1, 2], [0, 1, 2])

    store_problem('test', problem)


def test_problem():
    solver: Solver = ProposalsSolver('test')
    return solver


if __name__ == "__main__":
    # create_problem()
    solver = test_problem()
    solver.solve()
    solver.update_basic_problem()
