#! /usr/env/ python3

import itertools


class RandomizeParameters:

    def __init__(self, input_dictionary=None, randomization_dictionary=None):
        assert isinstance(input_dictionary, dict)
        assert isinstance(randomization_dictionary, dict)
        self.input_dictionary = input_dictionary
        self.randomization_dictionary = randomization_dictionary

    def get_randomized_parameters(self):
        value_parameters = []
        for key, value in self.randomization_dictionary.items():
            value_parameters.append(value)
        parameters_possibilities = list(itertools.product(*value_parameters))
        mixed_parameter_dictionary_list = []
        for parameters in parameters_possibilities:
            parameters_dict = dict(self.input_dictionary)
            for count, key in enumerate(self.randomization_dictionary.keys()):
                parameters_dict[key] = parameters[count]
            mixed_parameter_dictionary_list.append(parameters_dict)
        return tuple(mixed_parameter_dictionary_list)
