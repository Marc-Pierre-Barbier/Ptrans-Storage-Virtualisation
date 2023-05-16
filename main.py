from modelizations.basic_modelization import Problem
from scoring import change_abs_deviation
from solutionEvaluator import batch_evaluate
from solvers.proposals_solver import ProposalsSolver


if __name__ == "__main__":
    def evaluate(problem: Problem) -> Problem:
        solver = ProposalsSolver(problem)
        return solver.solve(True)

    results = batch_evaluate(evaluate, change_abs_deviation)

    for file in results:
        old_eval, new_eval, score = results[file]
        print(f"file: {file} finished with score: {score}")
        print("Stock config is: ")
        print(old_eval)
        print("Result is: ")
        print(new_eval)
