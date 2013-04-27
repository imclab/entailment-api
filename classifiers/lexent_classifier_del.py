# -*- coding: utf-8 -*-
'''

'''
from os.path import dirname, join
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
from sklearn import tree


class Lexent_classifier_del(object):

    def __init__(self):
        del_model_file = join(dirname(__file__),
            '../classifier_models/del_model.p')
        training_file = open(del_model_file)
        training_data = pickle.load(training_file)
        training_file.close()
        del_target_file = join(dirname(__file__),
            '../classifier_models/del_targets.p')
        targets_file = open(del_target_file)
        targets = pickle.load(targets_file)
        targets_file.close()

        self.clf = tree.DecisionTreeClassifier()
        self.clf.fit(training_data, targets)

    def predict(self, feature_vector):
        predicted_target = self.clf.predict(feature_vector)
        return predicted_target


if __name__ == '__main__':
    clf = Lexent_classifier_del()
    # the feature vector for 'went'
    print clf.predict([0, 0, 0, 0, 0, 0, 0, 0, 0])