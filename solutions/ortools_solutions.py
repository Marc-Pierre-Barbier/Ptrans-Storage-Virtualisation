from modelizations.abstract_modelization import *
from modelizations.basic_modelization import *
from modelizations.basic_to_abstract_modelization import *

from ortools.algorithms import pywrapknapsack_solver


class ORTools:
    """La classe qui concatène les infos précédents pour en faire un truc OR-Tools friendly"""

    def __init__(self, problem: Problem) -> None:
        self.problem = problem

    def simple_knapsack_solution(self):
        """Solution un peu bête qui consiste à regarder stockage après stockage les objets qu'on va mettre dedans
        avec un solveur. On suppose ici que object.get_locations() ne renvoie qu'un élément à chaque fois (et que des
        déplacements on le rappelle !). """

        raw_storages = self.problem.get_storages()  # à trier ?
        proposals = self.problem.get_proposals()

        for i in range(len(raw_storages)):
            storage_considered: Storage = raw_storages[i]

            candidates_objects: dict[tuple[int, int], Object] = {}
            values: list[int] = []
            weights: list[list[int]] = []
            weights[0] = []

            for proposal_list in proposals.values():
                for proposal in proposal_list:
                    if storage_considered in proposal.get_proposed_object().get_locations():
                        resource_values_object: ResourceValues = proposal.get_proposed_object().get_resources_values()

                        weight = resource_values_object.get_capacity()
                        value = resource_values_object.get_read_bandwidth() + resource_values_object.get_read_ops() + \
                            resource_values_object.get_write_bandwidth() + resource_values_object.get_write_ops()

                        candidates_objects[(value, weight)] = proposal.get_proposed_object()
                        values.append(value)
                        weights[0].append(weight)

            capacities: list[int] = [
                storage_considered.get_resources_limits().get_capacity() -
                storage_considered.get_resources_current().get_capacity()
            ]

            solver = pywrapknapsack_solver.KnapsackSolver(
                pywrapknapsack_solver.KnapsackSolver.KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'Knapsack')

            solver.Init(values, weights, capacities)
            solver.Solve()

            packed_items = []
            packed_weights = []
            total_weight = 0

            for i in range(len(values)):
                if solver.BestSolutionContains(i):
                    packed_items.append(i)
                    packed_weights.append(weights[0][i])
                    total_weight += weights[0][i]

            proposals_kept: list[Proposal] = []

            for i in range(len(packed_items)):
                for proposal in proposals[candidates_objects.pop((packed_items[i], packed_weights[i]))]:
                    if proposal.get_proposed_object().get_locations()[0] == storage_considered:
                        proposals_kept.append(proposal)

            return proposals_kept, proposals  # propositions gardées et propositions encore possibles
