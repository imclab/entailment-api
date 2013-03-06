# -*- coding: utf-8 -*-
'''

'''
#import sys
#sys.path.insert(0, '/home/gavin/dev/scikit-learn')
#import sklearn
#print sklearn.__version__
import os
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.ensemble import AdaBoostClassifier
from sklearn import tree


class Lexent_classifier_sub:

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

        #self.clf = tree.DecisionTreeClassifier()
        #self.clf = RandomForestClassifier(compute_importances=False)
        self.clf = RandomForestClassifier()
        #self.clf = RandomForestClassifier(
            #n_estimators=10,
            #max_features='auto',
            #criterion='gini',
            #compute_importances=False
            #)
        #self.clf = ExtraTreesClassifier(
            #n_estimators=50, max_depth=None,
            #min_samples_split=1, random_state=0)
        #self.clf = ExtraTreesClassifier()
        #self.clf = GradientBoostingClassifier(
            #n_estimators=500,
            #learning_rate=1.0,
            #max_depth=1,
            #random_state=0)

        #self.clf = AdaBoostClassifier(n_estimators=500)
        self.clf = self.clf.fit(training_data, targets)

    def predict(self, feature_vector):
        return self.clf.predict(feature_vector)