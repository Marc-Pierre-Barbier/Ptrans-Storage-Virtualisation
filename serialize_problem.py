from modelizations.basic_modelization import Problem
import pickle


def serialize(problem: Problem, output: str):
    with open(output, 'wb') as output_file:
        pickle.dump(problem, output_file)


def deserialize(input: str) -> Problem:
    with open(input, 'rb') as input_file:
        return pickle.load(input_file)
