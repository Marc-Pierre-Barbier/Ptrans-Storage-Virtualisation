from typing import List
from modelization import Problem, Storage, Proposal, ResourceValues
import random

def generate_problem(serverCount: int, proposalsCount: int) -> Problem:
    storages: List[Storage] = []
    proposals: List[Proposal] = []

    for i in range(0, serverCount):
        ResourceValues(
            random.randint(10000, 10000000)
            random.randint()
        )
        Storage(False, )


    return Problem(storages, proposals)
