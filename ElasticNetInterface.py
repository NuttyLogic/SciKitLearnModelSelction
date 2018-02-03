#! /usr/bin/env python3

import numpy as np
import ElasticNetCV_wrapper
import pickle


class ParseClassInput:

    def __init__(self, input_dictionary=None):
        if isinstance(input_dictionary, dict):
            self.input_dictionary = input_dictionary
        else:
            self.input_dictionary = pickle.load(input_dictionary, 'wb')
        self.run()

    def run(self):
        self.process_kwargs()
        self.elastic_instance()

    def process_kwargs(self):
        if not isinstance(self.input_dictionary['x'], (np.ndarray, np.generic)):
            self.input_dictionary['x'] = np.load(self.input_dictionary['x'])
        assert isinstance(self.input_dictionary['y'], list)

    def elastic_instance(self):
        ElasticNetCV_wrapper.ElasticNet(**self.input_dictionary)
