from solvers.solver import *
from solvers.ortools_gap_solver import *
#from modelizations.abstract_modelization import *
#from modelizations.basic_modelization import *
#from modelizations.basic_to_abstract_modelization import *


def main():
    solver = AssignmentORToolsSolver(10, 75, 0.5, 0)
    solver.solve()

if __name__ == "__main__":
    main()