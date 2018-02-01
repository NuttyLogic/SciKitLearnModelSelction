#! /usr/env/ python3

from sklearn.linear_model import ElasticNetCV
from sklearn.externals import joblib
import numpy as np
import random


def stc(input_list):
    """Simple string conversion function"""
    return [str(x) for x in input_list]


class ElasticNet:
    """Wrapper for SciKitLearn linear_model.ElasticNetCV to help with model optimization"""

    def __init__(self, x='numpy_array', y='predictor', sample_labels=None,
                 test_split=.2, sk_elastic_net_kwargs=None, regression_site_labels=None):
        assert isinstance(sk_elastic_net_kwargs, dict)
        assert isinstance(sample_labels, list)
        assert isinstance(regression_site_labels, list)
        self.x = x
        self.y = y
        self.test_split = test_split
        self.en_kwargs = sk_elastic_net_kwargs
        # test_container/ train_container [array, outcomes, labels]
        self.test_container = [[], [], []]
        self.train_container = [[], [], []]
        self.en_model = None
        self.sample_labels = sample_labels
        self.regression_sit_labels = regression_site_labels
        self.model_stats = None
        self.run()

    def run(self):
        self.set_test_samples()
        self.fit_model()
        self.model_stats()

    def set_test_samples(self):
        test_size = int(round(len(self.y) * self.test_split, 0))
        test_samples = random.sample([x for x in range(len(self.y))], test_size)

        # test_container/ validation_container [test_array, test_outcomes, labels]

        for count, info in enumerate(zip(self.x, self.y, self.sample_labels)):
            if count in test_samples:
                self.test_container[0].append(info[0])
                self.test_container[1].append(info[1])
                self.test_container[2].append(info[2])
            else:
                self.train_container[0].append(info[0])
                self.train_container[1].append(info[1])
                self.train_container[2].append(info[2])
        self.test_container[0] = np.asarray(self.test_container[0])
        self.train_container[0] = np.asarray(self.train_container[0])

    def fit_model(self):
        self.en_model = ElasticNetCV(**self.en_kwargs).fit(self.train_container[0], self.train_container[1])

    def model_stats(self):
        regression_sites = []
        for site in zip(self.regression_sit_labels, list(self.en_model.get_params)):
            if site[1]:
                regression_sites.append(site[0])
        model_score = self.en_model.score(self.test_container[0], self.test_container[1])
        predited_values = self.en_model.predict(self.test_container[0])
        self.model_stats = (regression_sites, model_score, predited_values)

    def model_output(self, output_directory='path', output_name='name'):
        """
        :param output_directory:
        :param output_name:
        :return:
        -----------------------------------------
        Model Information Output
        Model Name
        """
        kwarg_pair = []
        for key, value in self.en_kwargs.items():
            kwarg_pair.append('%s:%s' % (key, str(value)))

        output_path = '%s%s' % (output_directory, output_name)

        joblib.dump(self.en_model, output_path + '.model')

        out = open(output_path + '.model_info.txt', 'w')
        out.write('%s\n' % output_name)
        out.write('Model Score (R^2) = %s\n' % str(self.model_stats[1]))
        out.write('%s\n' % '\t'.join(kwarg_pair))
        out.write('Test Samples \t%s\n' % '\t'.join(stc(self.test_container[2])))
        out.write('Test Samples Predicted Values \t%s\n' % '\t'.join(stc(self.model_stats[2])))
        out.write('Test Samples Actual Values \t%s\n' % '\t'.join(stc(self.test_container[1])))
        out.write('Training Samples \t%s\n' % '\t'.join(stc(self.train_container[2])))
        out.write('Training Samples Actual Values \t%s' % '\t'.join(stc(self.train_container[1])))
        out.write('Regression Sites \t%s\n' % '\t'.join(self.model_stats[0]))
        out.close()
