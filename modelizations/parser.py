import functools
from modelizations.basic_modelization import Object, Problem, Proposal, ProposalType, Storage, ResourceValues

PROPOSAL_MODE = "=== Proposals ==="
OBJECT_MODE = "=== Objects ==="
STORAGE_MODE = "=== Storages ==="


def parse_problem(path: str) -> Problem:
    with open('data_sample/' + path + ".txt", 'r') as file:
        emptyRessource = ResourceValues(0, 0, 0, 0, 0)
        storages: dict[int, Storage] = {}
        objects: dict[int, Object] = {}
        proposals: dict[int, list[Proposal]] = {}
        mode: str | None = None
        for rawline in file:
            line = rawline.rstrip()

            if len(line) == 0:
                continue

            if line.startswith("=="):
                mode = line
                continue

            if mode == STORAGE_MODE:
                parameters = line.split(' ')

                id = int(parameters[0])
                capacity = float(parameters[1])
                rops = float(parameters[2])
                rband = float(parameters[3])
                wops = float(parameters[4])
                wband = float(parameters[5])
                resources = ResourceValues(capacity, rops, rband, wops, wband)

                storages[id] = Storage(id, [], resources, emptyRessource)
                continue

            if mode == OBJECT_MODE:
                parameters = line.split(' ')

                id = int(parameters[0])
                capacity = float(parameters[1])
                rops = float(parameters[2])
                rband = float(parameters[3])
                wops = float(parameters[4])
                wband = float(parameters[5])
                resources = ResourceValues(capacity, rops, rband, wops, wband)
                objects[id] = Object(id, list(map(int, parameters[6::])), resources)

                for storage in parameters[6::]:
                    storages[int(storage)].add_object_id(id)
                    storages[int(storage)].set_resources_current(storages[int(storage)].get_resources_current() + resources)
                continue

            if mode == PROPOSAL_MODE:
                parameters = line.split(' ')
                id = int(parameters[0])
                object_id = int(parameters[1])
                proposal_type = ProposalType.from_id(int(parameters[2]))
                priority = float(parameters[3])

                if object_id not in proposals:
                    proposals[object_id] = []

                proposals[object_id].append(Proposal(id, objects[object_id], list(map(int, parameters[4::])), proposal_type, priority))

        object_max: int = functools.reduce(lambda a, b: a if a > b else b, list(objects.keys()))
        storage_max: int = functools.reduce(lambda a, b: a if a > b else b, list(proposals.keys()))

        return Problem(storage_max, storages, object_max, objects, proposals)


def store_problem(file_name: str, problem: Problem) -> None:
    with open('data_sample/' + file_name + '.txt', 'xt') as file:
        file.write(STORAGE_MODE + '\n')
        for storage in problem.get_storage_list():
            limits = storage.get_resources_limits()
            line: str = ""
            line += str(storage.get_id())
            line += " "
            line += str(limits.get_capacity())
            line += " "
            line += str(limits.get_read_ops())
            line += " "
            line += str(limits.get_read_bandwidth())
            line += " "
            line += str(limits.get_write_ops())
            line += " "
            line += str(limits.get_write_bandwidth())
            file.write(line + '\n')

        file.write(OBJECT_MODE + '\n')
        for object in problem.get_object_list():
            ressources = object.get_resources_values()
            line: str = ""
            line += str(object.get_id())
            line += " "
            line += str(ressources.get_capacity())
            line += " "
            line += str(ressources.get_read_ops())
            line += " "
            line += str(ressources.get_read_bandwidth())
            line += " "
            line += str(ressources.get_write_ops())
            line += " "
            line += str(ressources.get_write_bandwidth())
            line += " "
            line += " ".join(map(str, object.get_storages_ids()))
            file.write(line + '\n')

        file.write(PROPOSAL_MODE + '\n')
        proposals = problem.get_proposals_list()
        proposals.sort(key=lambda a: a.get_id())
        for proposal in proposals:
            line: str = ""
            line += str(proposal.get_id())
            line += " "
            line += str(proposal.get_object_id())
            line += " "
            line += str(proposal.get_proposal_type()._value_)
            line += " "
            line += str(proposal.get_priority())
            line += " "
            line += " ".join(map(str, proposal.get_proposed_storages()))
            file.write(line + '\n')
