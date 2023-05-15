from modelizations.abstract_modelization import ProblemInstance
from modelizations.basic_modelization import Problem
from solvers.solver import Solver
from ortools.linear_solver import pywraplp
from time import time


# only usefull for typings
class BlowupProblem:
    def __init__(self, problem: ProblemInstance):
        self.items_weight0 = [item.get_resources()[0] for item in problem.get_items()]
        self.items_weight1 = [item.get_resources()[1] for item in problem.get_items()]
        self.items_weight2 = [item.get_resources()[2] for item in problem.get_items()]
        self.items_weight3 = [item.get_resources()[3] for item in problem.get_items()]
        self.items_weight4 = [item.get_resources()[4] for item in problem.get_items()]

        self.items_number = len(self.items_weight0)
        self.items_ortools_ids = range(self.items_number)

        self.volumes_capacity0 = [volume.get_limits()[0] for volume in problem.get_volumes()]
        self.volumes_capacity1 = [volume.get_limits()[1] for volume in problem.get_volumes()]
        self.volumes_capacity2 = [volume.get_limits()[2] for volume in problem.get_volumes()]
        self.volumes_capacity3 = [volume.get_limits()[3] for volume in problem.get_volumes()]
        self.volumes_capacity4 = [volume.get_limits()[4] for volume in problem.get_volumes()]

        self.volumes_number = len(self.volumes_capacity0)
        self.volumes_ortools_ids = range(self.volumes_number)

        self.proposals_problem_ids = [proposal.get_id() for proposal in problem.get_proposals()]
        self.proposals_item_concerned = [proposal.get_item_id() for proposal in problem.get_proposals()]
        self.proposals_volumes_concerned = [proposal.get_proposed_volumes() for proposal in problem.get_proposals()]
        self.proposals_original_volumes = [proposal.get_original_volumes() for proposal in problem.get_proposals()]
        self.proposals_priority: dict[int, float] = {}
        for proposal in problem.get_proposals():
            self.proposals_priority[proposal.get_id()] = proposal.get_priority()

        self.proposals_number = len(self.proposals_problem_ids)
        self.proposals_ortools_ids = range(self.proposals_number)

        self.original_affectations: dict[int, list[int]] = {}
        for item in problem.get_items():
            self.original_affectations[item.get_id()] = []
            for volume in item.get_volumes():
                self.original_affectations[item.get_id()].append(volume)


class ProposalsSolver(Solver):
    def __init__(self, path: str):
        super().__init__(path)

    def solve(self) -> Problem:
        self.blowup_problem = BlowupProblem(self.get_problem())
        # the type of the solver should have a significant impact but we don't know what because or-tools has no documentation explaining this
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if solver is None:
            raise Exception('SCIP solver unavailable.')

        # We initialize the variables (boolean, aka intvar 0/1) that will be modified by ortools algorithm
        proposals_kept: dict[int, pywraplp.Variable] = {}
        for proposal_id in self.blowup_problem.proposals_ortools_ids:
            proposals_kept[proposal_id] = solver.IntVar(0, 1, f'proposals_kept_{proposal_id}')

        affectations: dict[tuple[int, int], pywraplp.Variable] = {}
        for item_id in self.blowup_problem.items_ortools_ids:
            for volume_id in self.blowup_problem.volumes_ortools_ids:
                affectations[item_id, volume_id] = solver.IntVar(0, 1, f'affectations_{item_id}_{volume_id}')

        '''for item_id in self.blowup_problem.items_ortools_ids:
            for volume_id in self.blowup_problem.volumes_ortools_ids:
                solver.Add(
                    sum(
                        [proposals_kept[proposal_id] for proposal_id in self.blowup_problem.proposals_ortools_ids if (self.blowup_problem.proposals_item_concerned[proposal_id] == item_id and volume_id in self.blowup_problem.proposals_volumes_concerned[proposal_id])]
                    ) <= 1
                )'''

        # Establishing the link between affectations and proposals. Very particular in its approach and very difficult to perform better.
        for proposal_id in self.blowup_problem.proposals_ortools_ids:
            for volume_id in self.blowup_problem.proposals_volumes_concerned[proposal_id]:
                item_id = self.blowup_problem.proposals_item_concerned[proposal_id]
                has_volume = volume_id in self.blowup_problem.original_affectations[item_id]

                if has_volume:
                    solver.Add(affectations[item_id, volume_id] - proposals_kept[proposal_id] >= 0, "Link between affectations and proposals 1")
                else:
                    solver.Add(affectations[item_id, volume_id] + proposals_kept[proposal_id] <= 1, "Link between affectations and proposals 2")

        '''Other trials for establishing links between proposals and affectations, unfortunately not working on big instances for a unknown reason

        for item_id in self.blowup_problem.items_ortools_ids:
            for volume_id in self.blowup_problem.volumes_ortools_ids:

                has_volume = volume_id in self.blowup_problem.original_affectations[item_id]

                if has_volume:
                    interesting_original_proposals: list[int] = [proposal_id for proposal_id in self.blowup_problem.proposals_ortools_ids if (self.blowup_problem.proposals_item_concerned[proposal_id] == item_id and volume_id in self.blowup_problem.proposals_original_volumes[proposal_id])]
                    for proposal_id in interesting_original_proposals:
                        solver.Add(affectations[item_id, volume_id] - proposals_kept[proposal_id] >= 0, "Link between affectations and proposals 1")
                else:
                    interesting_destination_proposals: list[int] = [proposal_id for proposal_id in self.blowup_problem.proposals_ortools_ids if (self.blowup_problem.proposals_item_concerned[proposal_id] == item_id and volume_id in self.blowup_problem.proposals_volumes_concerned[proposal_id])]
                    for proposal_id in interesting_destination_proposals:
                        solver.Add(affectations[item_id, volume_id] + proposals_kept[proposal_id] <= 1, "Link between affectations and proposals 2")

                original_proposal_count = sum(
                    [proposals_kept[proposal_id] for proposal_id in self.blowup_problem.proposals_ortools_ids if (self.blowup_problem.proposals_item_concerned[proposal_id] == item_id and volume_id in self.blowup_problem.proposals_original_volumes[proposal_id])]
                ) == 0

                proposal_count = sum(
                    [proposals_kept[proposal_id] for proposal_id in self.blowup_problem.proposals_ortools_ids if (self.blowup_problem.proposals_item_concerned[proposal_id] == item_id and volume_id in self.blowup_problem.proposals_volumes_concerned[proposal_id])]
                ) >= 1

                var = (
                        (
                            has_volume and original_proposal_count
                        ) or (
                            (not has_volume) and proposal_count
                        )
                )'''

        # no more than one affectation of an item to a volume
        for item_id in self.blowup_problem.items_ortools_ids:
            solver.Add(
                sum(affectations[item_id, volume_id] for volume_id in self.blowup_problem.volumes_ortools_ids) >= 1
            )

        # capacity limit -> hard constraint
        for volume_id in self.blowup_problem.volumes_ortools_ids:
            solver.Add(
                sum(affectations[item_id, volume_id] * self.blowup_problem.items_weight0[item_id] for item_id in self.blowup_problem.items_ortools_ids) <= self.blowup_problem.volumes_capacity0[volume_id]
            )

        solver.Add(
            sum([proposals_kept[proposal_id] for proposal_id in self.blowup_problem.proposals_ortools_ids]) >= 10
        )

        solver.Add(
            sum([proposals_kept[proposal_id] for proposal_id in self.blowup_problem.proposals_ortools_ids]) <= 32
        )

        # declaring the objective function
        objective = solver.Objective()

        proposal_weight: float = 0.5  # need for tests (value between 0 and 10 probably, most likely between 0 and 2)

        for proposal_id in self.blowup_problem.proposals_ortools_ids:
            objective.SetCoefficient(proposals_kept[proposal_id], proposal_weight)

        for volume_id in self.blowup_problem.volumes_ortools_ids:
            for item_id in self.blowup_problem.items_ortools_ids:
                objective.SetCoefficient(affectations[item_id, volume_id],
                                         (self.blowup_problem.items_weight1[item_id] / self.blowup_problem.volumes_capacity1[volume_id])
                                         * (self.blowup_problem.items_weight2[item_id] / self.blowup_problem.volumes_capacity2[volume_id])
                                         * (self.blowup_problem.items_weight3[item_id] / self.blowup_problem.volumes_capacity3[volume_id])
                                         * (self.blowup_problem.items_weight4[item_id] / self.blowup_problem.volumes_capacity4[volume_id]))

        objective.SetMinimization()

        print('Solver launched')
        a = time()

        status = solver.Solve()

        b = time()
        print(b - a)

        if status != pywraplp.Solver.OPTIMAL:
            print('aie aie aie')
            # return "Error : the problem cannot be solved."

        problem_proposals_kept: list[int] = []

        for proposal_id in self.blowup_problem.proposals_ortools_ids:
            if proposals_kept[proposal_id].solution_value() > 0:
                problem_proposals_kept.append(self.blowup_problem.proposals_problem_ids[proposal_id])

        self.set_proposals_kept(problem_proposals_kept)

        return self.update_basic_problem()
