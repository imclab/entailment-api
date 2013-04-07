# -*- coding: utf-8 -*-
'''

'''
import os
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
from sklearn.ensemble import RandomForestClassifier


class Lexent_classifier_sub(object):

    def __init__(self):
        sub_model_file = os.path.join(
            os.path.dirname(__file__), 'classifier_models/sub_model.p')
        training_file = open(sub_model_file)
        training_data = pickle.load(training_file)
        training_file.close()
        sub_target_file = os.path.join(
            os.path.dirname(__file__), 'classifier_models/sub_targets.p')
        targets_file = open(sub_target_file)
        targets = pickle.load(targets_file)
        targets_file.close()

        self.clf = RandomForestClassifier()
        self.clf = self.clf.fit(training_data, targets)

    def predict(self, feature_vector):
        return self.clf.predict(feature_vector)