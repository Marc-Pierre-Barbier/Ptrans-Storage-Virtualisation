
from modelizations.basic_modelization import Problem

def glouton(problem: Problem):
    for proposal in problem.get_proposals():
        object_proposals = problem.get_proposals()[proposal]
        for object_proposal in object_proposals:
            found = True
            proposed_object = object_proposal.get_proposed_object()
            for location in proposed_object.get_locations():
                if proposed_object.get_resources_values() > location.get_resources_limits():
                    found = False
                    break

            if found:
                for location in proposed_object.get_locations():
                    location._resources_current += proposed_object.get_resources_values()
                for location in object_proposal.get_original_object().get_locations():
                    location._resources_current -= object_proposal.get_original_object().get_resources_values()
                break
