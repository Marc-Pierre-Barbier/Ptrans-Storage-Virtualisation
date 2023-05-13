from solvers.proposals_solver import ProposalsSolver
from validator import check_problem


def test_problem() -> ProposalsSolver:
    solver = ProposalsSolver('fast_server_medium_usage')
    check_problem(solver.get_basic_problem())
    return solver


if __name__ == "__main__":
    solver = test_problem()
    solver.solve()
    problem = solver.update_basic_problem()

    check_problem(problem)
