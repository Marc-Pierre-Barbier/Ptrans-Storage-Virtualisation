from ortools.linear_solver.linear_solver_natural_api import LinearExpr
from modelizations.abstract_modelization import ProblemInstance
from modelizations.basic_modelization import Problem
from solvers.solver import Solver
from ortools.linear_solver import pywraplp
from time import time


# only usefull for typings
class BlownupProblem:
    def __init__(self, problem: ProblemInstance):

        # ITEMS #

        self.items_weight0: dict[int, float] = {}
        self.items_weight1: dict[int, float] = {}
        self.items_weight2: dict[int, float] = {}
        self.items_weight3: dict[int, float] = {}
        self.items_weight4: dict[int, float] = {}

        for item in problem.get_items():
            self.items_weight0[item.get_id()] = item.get_resources()[0]
            self.items_weight1[item.get_id()] = item.get_resources()[1]
            self.items_weight2[item.get_id()] = item.get_resources()[2]
            self.items_weight3[item.get_id()] = item.get_resources()[3]
            self.items_weight4[item.get_id()] = item.get_resources()[4]

        self.items_ids: list[int] = list(self.items_weight0.keys())

        # VOLUMES #

        self.volumes_capacity0: dict[int, float] = {}
        self.volumes_capacity1: dict[int, float] = {}
        self.volumes_capacity2: dict[int, float] = {}
        self.volumes_capacity3: dict[int, float] = {}
        self.volumes_capacity4: dict[int, float] = {}

        for volume in problem.get_volumes():
            self.volumes_capacity0[volume.get_id()] = volume.get_limits()[0]
            self.volumes_capacity1[volume.get_id()] = volume.get_limits()[1]
            self.volumes_capacity2[volume.get_id()] = volume.get_limits()[2]
            self.volumes_capacity3[volume.get_id()] = volume.get_limits()[3]
            self.volumes_capacity4[volume.get_id()] = volume.get_limits()[4]

        self.volumes_ids: list[int] = list(self.volumes_capacity0.keys())

        # PROPOSALS #

        self.proposals_item_concerned: dict[int, int] = {}
        self.proposals_volumes_origin: dict[int, list[int]] = {}
        self.proposals_volumes_destination: dict[int, list[int]] = {}
        self.proposals_for_item_volume: dict[tuple[int, int], list[int]] = {}
        self.proposals_for_item: dict[int, list[int]] = {}

        for proposal in problem.get_proposals():
            self.proposals_item_concerned[proposal.get_id()] = proposal.get_item_id()
            self.proposals_volumes_origin[proposal.get_id()] = proposal.get_original_volumes()
            self.proposals_volumes_destination[proposal.get_id()] = proposal.get_proposed_volumes()

            for volume_id in proposal.get_original_volumes():
                if (proposal.get_item_id(), volume_id) not in self.proposals_for_item_volume:
                    self.proposals_for_item_volume[proposal.get_item_id(), volume_id] = []

                if proposal.get_item_id() not in self.proposals_for_item:
                    self.proposals_for_item[proposal.get_item_id()] = []

                if proposal.get_id() not in self.proposals_for_item_volume[proposal.get_item_id(), volume_id]:
                    self.proposals_for_item_volume[proposal.get_item_id(), volume_id].append(proposal.get_id())

                if proposal.get_id() not in self.proposals_for_item[proposal.get_item_id()]:
                    self.proposals_for_item[proposal.get_item_id()].append(proposal.get_id())

        self.proposals_ids: list[int] = list(self.proposals_item_concerned.keys())

        # ORIGINAL AFFECTATIONS BETWEEN VOLUMES AND ITEMS #

        self.original_affectations: dict[int, list[int]] = {}

        for item in problem.get_items():
            self.original_affectations[item.get_id()] = []

            for volume_id in item.get_volumes():
                self.original_affectations[item.get_id()].append(volume_id)


class ProposalsSolver(Solver):
    def __init__(self, problem: str | Problem):
        super().__init__(problem)

    def solve(self, limit_proposals: bool = False) -> Problem:
        self.blownup_problem = BlownupProblem(self.get_problem())
        # the type of the solver should have a significant impact but we don't know what because or-tools has no documentation explaining this
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if solver is None:
            raise Exception('SCIP solver unavailable.')

        # We initialize the variables (boolean, aka intvar 0/1) that will be modified by ortools algorithm
        proposals_kept: dict[int, pywraplp.Variable] = {}
        for proposal_id in self.blownup_problem.proposals_ids:
            proposals_kept[proposal_id] = solver.IntVar(0, 1, f'proposals_kept_{proposal_id}')

        affectations: dict[tuple[int, int], pywraplp.Variable] = {}
        for item_id in self.blownup_problem.items_ids:
            for volume_id in self.blownup_problem.volumes_ids:
                affectations[item_id, volume_id] = solver.IntVar(0, 1, f'affectations_{item_id}_{volume_id}')

        # Establishing the link between affectations and proposals. Very particular in its approach and very difficult to perform better.
        for proposal_id in self.blownup_problem.proposals_ids:
            item_id = self.blownup_problem.proposals_item_concerned[proposal_id]

            for volume_id in self.blownup_problem.proposals_volumes_origin[proposal_id]:
                if volume_id not in self.blownup_problem.proposals_volumes_destination[proposal_id]:
                    solver.Add(affectations[item_id, volume_id] + proposals_kept[proposal_id] <= 1)

            for volume_id in self.blownup_problem.proposals_volumes_destination[proposal_id]:
                if volume_id not in self.blownup_problem.proposals_volumes_origin[proposal_id]:
                    solver.Add(affectations[item_id, volume_id] - proposals_kept[proposal_id] >= 0)

        for item_id in self.blownup_problem.items_ids:
            if item_id not in self.blownup_problem.proposals_for_item:
                continue

            # We cannot have multiple proposals accepted at a same time for a proposal
            solver.Add(sum([proposals_kept[proposal_id] for proposal_id in self.blownup_problem.proposals_for_item[item_id]]) <= 1)

            for volume_id in self.blownup_problem.original_affectations[item_id]:
                if (item_id, volume_id) not in self.blownup_problem.proposals_for_item_volume:
                    # If there are no proposals and the item is already affected, then it will be affected
                    solver.Add(affectations[item_id, volume_id] == 1)
                else:
                    # These two constraints deal with the rest of the cases. Hard to understand (it always takes us 5 minutes to remember how it works...) but it does work as we checked it multiple times
                    solver.Add(sum(
                        [proposals_kept[proposal_id] for proposal_id in self.blownup_problem.proposals_for_item_volume[item_id, volume_id] if volume_id not in self.blownup_problem.proposals_volumes_destination[proposal_id]]
                    ) + affectations[item_id, volume_id] >= 1)
                    # -affection + sum instead of the oposite since unary - is define but int - var isn't (var - int is)
                    # this doesn't affect functionnality as both work but it fixes the typing error
                    solver.Add(-affectations[item_id, volume_id] + sum(
                        [proposals_kept[proposal_id]for proposal_id in self.blownup_problem.proposals_for_item_volume[item_id, volume_id] if volume_id in self.blownup_problem.proposals_volumes_destination[proposal_id]]
                    ) <= 0)

        # no more than one affectation of an item to a volume
        for item_id in self.blownup_problem.items_ids:
            solver.Add(sum([affectations[item_id, volume_id] for volume_id in self.blownup_problem.volumes_ids]) >= 1)

        # capacity limit -> hard constraint
        for volume_id in self.blownup_problem.volumes_ids:
            solver.Add(sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight0[item_id] for item_id in self.blownup_problem.items_ids]) <= self.blownup_problem.volumes_capacity0[volume_id])

        # capacity limit -> hard constraint
        for volume_id in self.blownup_problem.volumes_ids:
            solver.Add(sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight0[item_id] for item_id in self.blownup_problem.items_ids]) <= self.blownup_problem.volumes_capacity0[volume_id])

        volume_value: dict[tuple[int, int], LinearExpr] = {}
        for volume_id in self.blownup_problem.volumes_ids:
            volume_value[volume_id, 0] = (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight0[item_id] for item_id in self.blownup_problem.items_ids]) / self.blownup_problem.volumes_capacity0[volume_id])  # type: ignore
            volume_value[volume_id, 1] = (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight1[item_id] for item_id in self.blownup_problem.items_ids]) / self.blownup_problem.volumes_capacity1[volume_id])  # type: ignore
            volume_value[volume_id, 2] = (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight2[item_id] for item_id in self.blownup_problem.items_ids]) / self.blownup_problem.volumes_capacity2[volume_id])  # type: ignore
            volume_value[volume_id, 3] = (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight3[item_id] for item_id in self.blownup_problem.items_ids]) / self.blownup_problem.volumes_capacity3[volume_id])  # type: ignore
            volume_value[volume_id, 4] = (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight4[item_id] for item_id in self.blownup_problem.items_ids]) / self.blownup_problem.volumes_capacity4[volume_id])  # type: ignore

        # This variable is set as equal to a variable that is fully constrained so this is a definition. Used for the optimization function.
        for volume_id in self.blownup_problem.volumes_ids:
            solver.Add(volume_value[volume_id, 0] == (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight0[item_id] for item_id in self.blownup_problem.items_ids])
                                                      / self.blownup_problem.volumes_capacity0[volume_id]))
            solver.Add(volume_value[volume_id, 1] == (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight1[item_id] for item_id in self.blownup_problem.items_ids])
                                                      / self.blownup_problem.volumes_capacity1[volume_id]))
            solver.Add(volume_value[volume_id, 2] == (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight2[item_id] for item_id in self.blownup_problem.items_ids])
                                                      / self.blownup_problem.volumes_capacity2[volume_id]))
            solver.Add(volume_value[volume_id, 3] == (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight3[item_id] for item_id in self.blownup_problem.items_ids])
                                                      / self.blownup_problem.volumes_capacity3[volume_id]))
            solver.Add(volume_value[volume_id, 4] == (sum([affectations[item_id, volume_id] * self.blownup_problem.items_weight4[item_id] for item_id in self.blownup_problem.items_ids])
                                                      / self.blownup_problem.volumes_capacity4[volume_id]))

        comparison_score: dict[tuple[int, int, int], pywraplp.Variable] = {}
        for volume_id_a in self.blownup_problem.volumes_ids:
            for volume_id_b in self.blownup_problem.volumes_ids:
                for i in range(5):
                    comparison_score[volume_id_a, volume_id_b, i] = solver.NumVar(0, solver.infinity(), f'comparison_score[{volume_id_a}, {volume_id_b}_{i}]')

        for volume_id_a in self.blownup_problem.volumes_ids:
            for volume_id_b in self.blownup_problem.volumes_ids:
                for i in range(5):
                    solver.Add(comparison_score[volume_id_a, volume_id_b, i] >= volume_value[volume_id_a, i] - volume_value[volume_id_b, i])
                    solver.Add(comparison_score[volume_id_b, volume_id_a, i] >= volume_value[volume_id_a, i] - volume_value[volume_id_b, i])

        if limit_proposals:
            max_proposal = min((len(self.blownup_problem.proposals_ids) / len(self.blownup_problem.volumes_ids)) * 0.6, len(self.blownup_problem.proposals_ids) * 0.10)
            solver.Add(
                sum([proposals_kept[proposal_id] for proposal_id in self.blownup_problem.proposals_ids]) <= min((len(self.blownup_problem.proposals_ids) / len(self.blownup_problem.volumes_ids)) * 0.6, len(self.blownup_problem.proposals_ids) * 0.10)
            )
            print("only keeping:" + str(max_proposal))

        # declaring the objective function
        objective = solver.Objective()

        proposal_weight: float = 0  # need for tests (value between 0 and 10 probably, most likely between 0 and 2)

        for proposal_id in self.blownup_problem.proposals_ids:
            objective.SetCoefficient(proposals_kept[proposal_id], proposal_weight)

        for volume_id_a in self.blownup_problem.volumes_ids:
            for volume_id_b in self.blownup_problem.volumes_ids:
                for i in range(5):
                    objective.SetCoefficient(comparison_score[volume_id_a, volume_id_b, i], 1)

        objective.SetMinimization()

        print('Solver launched')
        a = time()

        solver.Solve()

        b = time()
        print(f"time: {b - a}s")

        problem_proposals_kept: list[int] = []

        for proposal_id in self.blownup_problem.proposals_ids:
            if proposals_kept[proposal_id].solution_value() > 0:
                problem_proposals_kept.append(proposal_id)

        self.set_proposals_kept(problem_proposals_kept)

        return self.update_basic_problem()
