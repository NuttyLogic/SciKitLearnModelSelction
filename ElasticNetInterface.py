#! /usr/bin/env python3

import numpy as np
import ElasticNetCV_wrapper
import pickle


class ParseClassInput:

    def __init__(self, input_dictionary=None):
        if isinstance(input_dictionary, dict):
            self.input_dictionary = input_dictionary
        else:
            with open(input_dictionary, 'rb') as handle:
                self.input_dictionary = pickle.load(handle)
        self.run()

    def run(self):
        self.process_kwargs()
        self.elastic_instance()

    def process_kwargs(self):
        if not isinstance(self.input_dictionary['x'], (np.ndarray, np.generic)):
            self.input_dictionary['x'] = np.load(self.input_dictionary['x'])
        if not isinstance(self.input_dictionary['sample_labels'], list):
            with open(self.input_dictionary['sample_labels'], 'rb') as samples:
                self.input_dictionary['sample_labels'] = pickle.load(samples)
        if not isinstance(self.input_dictionary['regression_site_labels'], list):
            with open(self.input_dictionary['regression_site_labels'], 'rb') as cpg_sites:
                self.input_dictionary['regression_site_labels'] = pickle.load(cpg_sites)
        assert isinstance(self.input_dictionary['y'], list)

    def elastic_instance(self):
        ElasticNetCV_wrapper.ElasticNet(**self.input_dictionary)
