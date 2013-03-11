# -*- coding: utf-8 -*-
'''
Return the summed feature vectors of each alignment in the problem
'''
import os
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
import Edit_featurizer


def featurize(problem):
    '''
    Return the summed feature vectors of each alignment in the problem
    '''
    features = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, ]
    for edit in problem.gold:
        features += Edit_featurizer.featurize(
            edit, problem.p_str_tokens, problem.h_str_tokens,
            len(problem.p_str_tokens), len(problem.h_str_tokens))
    return features


if __name__ == '__main__':
    pickle_file = os.path.join(os.path.dirname(__file__),
    'training_data/alignment_problems.p')
    training_set = open(pickle_file)
    training_data = pickle.load(training_set)
    training_set.close()
    features = featurize(training_data[11])
    print features

