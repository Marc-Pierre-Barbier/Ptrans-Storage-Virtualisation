from scoring import mean_abs_deviation
from solutionEvaluator import evaluate
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
    inital_evla = evaluate(solver.get_basic_problem())
    problem = solver.solve()

    check_problem(problem)

    evaluation = evaluate(problem)

    print(inital_evla)
    print(evaluation)

    print("Change: initial / result")
    print((evaluation / inital_evla))

    print(f"score: {-(mean_abs_deviation(evaluation) - mean_abs_deviation(inital_evla))}")
