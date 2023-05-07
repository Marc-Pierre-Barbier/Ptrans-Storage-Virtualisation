from solvers.solver import Solver
from ortools.linear_solver import pywraplp


class ProposalsSolver(Solver):
    def __init__(self, path: str):
        super().__init__(path)

    def solve(self):
        data = {}
        data['items_weight0'] = [item.get_resources()[0] for item in self.get_problem().get_items()]
        data['items_weight1'] = [item.get_resources()[1] for item in self.get_problem().get_items()]
        data['items_weight2'] = [item.get_resources()[2] for item in self.get_problem().get_items()]
        data['items_weight3'] = [item.get_resources()[3] for item in self.get_problem().get_items()]
        data['items_weight4'] = [item.get_resources()[4] for item in self.get_problem().get_items()]

        data['items_number'] = len(data['items_weight0'])
        data['items_ortools_ids'] = range(data['items_number'])

        data['volumes_capacity0'] = [volume.get_limits()[0] for volume in self.get_problem().get_volumes()]
        data['volumes_capacity1'] = [volume.get_limits()[1] for volume in self.get_problem().get_volumes()]
        data['volumes_capacity2'] = [volume.get_limits()[2] for volume in self.get_problem().get_volumes()]
        data['volumes_capacity3'] = [volume.get_limits()[3] for volume in self.get_problem().get_volumes()]
        data['volumes_capacity4'] = [volume.get_limits()[4] for volume in self.get_problem().get_volumes()]

        data['volumes_number'] = len(data['volumes_capacity0'])
        data['volumes_ortools_ids'] = range(data['volumes_number'])

        data['proposals_problem_ids'] = [proposal.get_id() for proposal in self.get_problem().get_proposals()]
        data['proposals_items_concerned'] = [proposal.get_item_id() for proposal in self.get_problem().get_proposals()]
        data['proposals_volumes_concerned'] = [proposal.get_proposed_volumes() for proposal in self.get_problem().get_proposals()]
        data['proposals_original_volumes'] = [proposal.get_original_volumes() for proposal in self.get_problem().get_proposals()]
        data['proposals_priority'] = [proposal.get_priority() for proposal in self.get_problem().get_proposals()]

        data['proposals_number'] = len(data['proposals_problem_ids'])
        data['proposals_ortools_ids'] = range(data['proposals_number'])

        data['original_affectations'] = {}
        for item in self.get_problem().get_items():
            data['original_affectations'][item.get_id()] = []
            for volume in item.get_volumes():
                data['original_affectations'][item.get_id()].append(volume)

        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')
        if solver is None:
            print('SCIP solver unavailable.')
            return

        proposals_kept = {}
        for proposal_id in data['proposals_ortools_ids']:
            proposals_kept[proposal_id] = solver.BoolVar(f'proposals_kept_{proposal_id}')

        affectations = {}
        for item_id in data['items_ortools_ids']:
            for volume_id in data['volumes_ortools_ids']:
                affectations[item_id, volume_id] = solver.BoolVar(f'affectations_{item_id}_{volume_id}')

        for item_id in data['items_ortools_ids']:
            for volume_id in data['volumes_ortools_ids']:
                solver.Add(
                    affectations[item_id, volume_id] == (
                        (
                            (
                                data['original_affectations'][item_id].count(volume_id) >= 1
                            ) and (
                                sum(
                                    [proposals_kept[proposal_id] for proposal_id in data['proposals_ortools_ids'] if (data['proposals_items_concerned'][proposal_id] == item_id and data['proposals_original_volumes'][proposal_id].count(volume_id) >= 1)]
                                ) == 0
                            )
                        ) or (
                            (
                                data['original_affectations'][item_id].count(volume_id) == 0
                            ) and (
                                sum(
                                    [proposals_kept[proposal_id] for proposal_id in data['proposals_ortools_ids'] if (data['proposals_items_concerned'][proposal_id] == item_id and data['proposals_volumes_concerned'][proposal_id].count(volume_id) >= 1)]
                                ) >= 1
                            )
                        )
                    ),
                    "Link between affectations and proposals"
                )

                solver.Add(
                    sum(
                        [proposals_kept[proposal_id] for proposal_id in data['proposals_ortools_ids'] if (data['proposals_items_concerned'][proposal_id] == item_id and data['proposals_volumes_concerned'][proposal_id].count(volume_id) > 0)]
                    ) <= 1
                )

        for item_id in data['items_ortools_ids']:
            solver.Add(
                sum(affectations[item_id, volume_id] for volume_id in data['volumes_ortools_ids']) >= 1
            )

        for volume_id in data['volumes_ortools_ids']:
            solver.Add(
                sum(affectations[item_id, volume_id] * data['items_weight0'][item_id] for item_id in data['items_ortools_ids']) <= data['volumes_capacity0'][volume_id]
            )
            solver.Add(
                sum(affectations[item_id, volume_id] * data['items_weight1'][item_id] for item_id in data['items_ortools_ids']) <= data['volumes_capacity1'][volume_id]
            )
            solver.Add(
                sum(affectations[item_id, volume_id] * data['items_weight2'][item_id] for item_id in data['items_ortools_ids']) <= data['volumes_capacity2'][volume_id]
            )
            solver.Add(
                sum(affectations[item_id, volume_id] * data['items_weight3'][item_id] for item_id in data['items_ortools_ids']) <= data['volumes_capacity3'][volume_id]
            )
            solver.Add(
                sum(affectations[item_id, volume_id] * data['items_weight4'][item_id] for item_id in data['items_ortools_ids']) <= data['volumes_capacity4'][volume_id]
            )

        for proposal_id in data["proposals_ortools_ids"]:
            solver.Add(
                sum(proposals_kept[proposal_id]) == 100
            )

        objective = solver.Objective()
        for proposal_id in data["proposals_ortools_ids"]:
            objective.setCoefficient(proposals_kept[proposal_id], data['proposals_priority'])
        objective.SetMaximization()

        status = solver.Solve()

        if status != pywraplp.Solver.OPTIMAL:
            return "Error : the problem cannot be solved."

        problem_proposals_kept: list[int] = []

        for proposal_id in data["proposals_ortools_ids"]:
            if proposals_kept[proposal_id].solution_value() > 0:
                problem_proposals_kept.append(data['proposals_problem_ids'][proposal_id])

        self.set_proposals_kept(problem_proposals_kept)
