from solvers.solver import Solver
from ortools.linear_solver import pywraplp
from modelizations.abstract_modelization import *


class AssignmentORToolsSolver(Solver):
    """A class implementing a solver to choose dynamically a method to solve the problem."""

    def __init__(self, server_count: int, usage: float, usage_var: float, proposals_count: int):
        super().__init__(server_count, usage, usage_var, proposals_count)

    def solve(self):
        data = {}
        data['weights'] = [sum([value.get_resources_used()[0] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights1'] = [sum([value.get_resources_used()[1] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights2'] = [sum([value.get_resources_used()[2] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights3'] = [sum([value.get_resources_used()[3] for value in item.get_instances().values()]) for item in self._problem.get_items()]
        data['weights4'] = [sum([value.get_resources_used()[4] for value in item.get_instances().values()]) for item in self._problem.get_items()]

        data['num_items'] = len(data['weights'])
        data['all_items'] = range(data['num_items'])

        data['bin_capacities'] = [volume.get_limits()[0] for volume in self._problem.get_volumes()]
        data['bin_capacities1'] = [volume.get_limits()[1] for volume in self._problem.get_volumes()]
        data['bin_capacities2'] = [volume.get_limits()[2] for volume in self._problem.get_volumes()]
        data['bin_capacities3'] = [volume.get_limits()[3] for volume in self._problem.get_volumes()]
        data['bin_capacities4'] = [volume.get_limits()[4] for volume in self._problem.get_volumes()]

        data['num_bins'] = len(data['bin_capacities'])
        data['all_bins'] = range(data['num_bins'])

        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')
        if solver is None:
            print('SCIP solver unavailable.')
            return

        x = {}
        for i in data['all_items']:
            for b in data['all_bins']:
                x[i, b] = solver.BoolVar(f'x_{i}_{b}')

        for i in data['all_items']:
            solver.Add(
                sum(x[i, b] for b in data['all_bins']) <= 1
            )
            solver.Add(
                sum(x[i, b] for b in data['all_bins']) >= 1
            )

        for b in data['all_bins']:
            solver.Add(
                sum(x[i, b] * data['weights'][i] for i in data['all_items']) <= data['bin_capacities'][b]
            )
            solver.Add(
                sum(x[i, b] * data['weights1'][i] for i in data['all_items']) <= data['bin_capacities1'][b]
            )
            solver.Add(
                sum(x[i, b] * data['weights2'][i] for i in data['all_items']) <= data['bin_capacities2'][b]
            )
            solver.Add(
                sum(x[i, b] * data['weights3'][i] for i in data['all_items']) <= data['bin_capacities3'][b]
            )
            solver.Add(
                sum(x[i, b] * data['weights4'][i] for i in data['all_items']) <= data['bin_capacities4'][b]
            )

        objective = solver.Objective()
        for i in data['all_items']:
            for b in data['all_bins']:
                objective.SetCoefficient(x[i, b], data['bin_capacities'][b]*2)
        objective.SetMinimization()

        status = solver.Solve()

        if status != pywraplp.Solver.OPTIMAL:
            return("Error : the problem cannot be solved.")


        items: list[Item] = []
        volumes: list[Volume] = []

        for b in data['all_bins']:
            volumes.append(Volume(
                [
                    data['bin_capacities'][b],
                    data['bin_capacities1'][b],
                    data['bin_capacities2'][b],
                    data['bin_capacities3'][b],
                    data['bin_capacities4'][b]
                ],
                [],
                []
            ))

        for i in data['all_items']:
            instances: dict[Volume, Resources] = {}
            for b in data['all_bins']:
                if x[i, b].solution_value() > 0:
                    instances[volumes[b]] = Resources(
                        [
                        data['weights'][i],
                        data['weights1'][i],
                        data['weights2'][i],
                        data['weights3'][i],
                        data['weights4'][i]
                        ],
                        []
                    )
            items.append(Item(instances, []))

        for b in data['all_bins']:
            resources_used: list[int] = [0, 0, 0, 0, 0]
            for i in data['all_items']:
                if items[i].get_instances().get(volumes[b]) != None:
                    resources_used = [
                        resources_used[0] + items[i].get_instances()[volumes[b]].get_resources_used()[0],
                        resources_used[1] + items[i].get_instances()[volumes[b]].get_resources_used()[1],
                        resources_used[2] + items[i].get_instances()[volumes[b]].get_resources_used()[2],
                        resources_used[3] + items[i].get_instances()[volumes[b]].get_resources_used()[3],
                        resources_used[4] + items[i].get_instances()[volumes[b]].get_resources_used()[4]
                    ]
            volumes[b].set_resources_used(resources_used)

        """total_weight = 0
        for b in data['all_bins']:
            print(f'Bin {b}')
            bin_weight = 0
            bin_value = 0
            for i in data['all_items']:
                if x[i, b].solution_value() > 0:
                    print(
                        f"Item {i} weight: {data['weights'][i]}"
                    )
                    bin_weight += data['weights'][i]
            print(f'Packed bin weight: {bin_weight}')
            print(f'Packed bin value: {bin_value}\n')
            total_weight += bin_weight
        print(f'Total packed weight: {total_weight}')"""

        self.set_solved_problem(ProblemInstance(volumes, items))
