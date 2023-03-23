from solvers.solver import Solver
from ortools.linear_solver import pywraplp


class AssignmentORToolsSolver(Solver):
    """A class implementing a solver to choose dynamically a method to solve the problem."""

    def __init__(self, server_count: int, usage: int, proposals_count: int):
        super().__init__(server_count, usage, proposals_count)

    def create_ortools_data(self):
        data = {}
        data['weights'] = [sum([value.get_resources_used()[0] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights1'] = [sum([value.get_resources_used()[1] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights2'] = [sum([value.get_resources_used()[2] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights3'] = [sum([value.get_resources_used()[3] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights4'] = [sum([value.get_resources_used()[4] for value in item.get_instances().values()]) for item in self._problem.get_items()]

        assert len(data['weights']) == len(data['values'])
        data['num_items'] = len(data['weights'])
        data['all_items'] = range(data['num_items'])

        data['bin_capacities'] = [volume.get_limits()[0] for volume in self._problem.get_volumes()]
        data['bin_capacities1'] = [volume.get_limits()[1] for volume in self._problem.get_volumes()]
        data['bin_capacities2'] = [volume.get_limits()[2] for volume in self._problem.get_volumes()]
        data['bin_capacities3'] = [volume.get_limits()[3] for volume in self._problem.get_volumes()]
        data['bin_capacities4'] = [volume.get_limits()[4] for volume in self._problem.get_volumes()]

        data['num_bins'] = len(data['bin_capacities'])
        data['all_bins'] = range(data['num_bins'])

        return data

    def ortools_create_solver(self, data):
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')
        if solver is None:
            print('SCIP solver unavailable.')
            return

        x = {}
        for i in data['all_items']:
            for b in data['all_bins']:
                x[i, b] = solver.BoolVar(f'x_{i}_{b}')

        for i in data['all_items']:
            solver.Add(sum(x[i, b] for b in data['all_bins']) <= 1)

        for b in data['all_bins']:
            solver.Add(
                sum(x[i, b] * data['weights'][i]
                    for i in data['all_items']) <= data['bin_capacities'][b])
            solver.Add(
                sum(x[i, b] * data['weights1'][i]
                    for i in data['all_items']) <= data['bin_capacities1'][b])
            solver.Add(
                sum(x[i, b] * data['weights22'][i]
                    for i in data['all_items']) <= data['bin_capacities2'][b])
            solver.Add(
                sum(x[i, b] * data['weights3'][i]
                    for i in data['all_items']) <= data['bin_capacities3'][b])
            solver.Add(
                sum(x[i, b] * data['weights4'][i]
                    for i in data['all_items']) <= data['bin_capacities4'][b])

        objective = solver.Objective()
        for i in data['all_items']:
            for b in data['all_bins']:
                objective.SetCoefficient(x[i, b], data['bin_capacities'][b])
        objective.SetMinimization()

        return x, solver, objective

    def solve(self):
        data = self.create_ortools_data()
        x, solver, objective = self.ortools_create_solver(data)
        status = solver.Solve()

        if status != pywraplp.Solver.OPTIMAL:
            return("Error : the problem cannot be solved.")

        print(f'Total packed value: {objective.Value()}')
        total_weight = 0
        for b in data['all_bins']:
            print(f'Bin {b}')
            bin_weight = 0
            bin_value = 0
            for i in data['all_items']:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]} value: {data['values'][i]}"
                    )
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
            print(f'Packed bin weight: {bin_weight}')
            print(f'Packed bin value: {bin_value}\n')
            total_weight += bin_weight
        print(f'Total packed weight: {total_weight}')