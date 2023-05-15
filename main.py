from solvers.proposals_solver import ProposalsSolver
from validator import check_problem


def test_problem() -> ProposalsSolver:
    solver = ProposalsSolver('supa_smol')
    # check if the stored problem is valid
    # if it's not valid it will throw an exception
    check_problem(solver.get_basic_problem())
    return solver


if __name__ == "__main__":
    solver = test_problem()
    solver.solve()
    problem = solver.update_basic_problem()

    check_problem(problem)
