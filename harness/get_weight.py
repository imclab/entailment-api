# -*- coding: utf-8 -*-
"""
inputs:
    training problems
    corresponding gold alignments
    # of learning epochs - 50
    burn in period - 10
    learning rate 1
    learning rate multiplier 0.8
    vector of feature functions
    aligner that finds a good alignment
    weight vector w

initialize:
    set w=0

repeat for 1 to 50:
    set learning rate = learning rate * multiplier
        R = R * 0.8
    shuffle training problems
    for each training problem
        predictedA = align(trainingProblem, w)
        w = w + learningRate * (features(GoldAlignment) -
            features(predictedAlignment))
        l2 normalize w
        w[i] = w

return w.avg = 1 / (N - N)
return an averaged weight vector that discounts the burn in period

w[burnIn+1:len(w)] / N - burnIn

"""
from __future__ import division
import sys
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
from random import shuffle
from math import sqrt
import os
import logging
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
import Aligner
import Gold_problem_featurizer as gold_featurizer


def learn_weights(training_set, learning_epochs, burn_in_epochs,
learning_rate, learning_rate_multiplier):
    #weights = [
        #0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    weights = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    weights_history = []

    for i in range(learning_epochs):
        print '*** Starting epoch %s ***' % i
        learning_rate *= learning_rate_multiplier
        logging.warning('Starting epoch %s with learning rate %s' %
        (i, learning_rate))
        shuffle(training_set)

        for index, problem in enumerate(training_set):
            print '* Starting problem %s of %s in epoch %s*' % (index, len(training_set), i)
            gold_features = gold_featurizer.featurize(problem)
            logging.warning('\nStarting weights:\n%s' % weights)
            #logging.warning('Problem:\n%s\n%s' % (problem.p_str_tokens,
            #problem.h_str_tokens))
            #logging.warning('\nGold features:\n%s' % (gold_features))

            predicted_alignment, predicted_features = Aligner.align(
                    problem.p_str_tokens, problem.h_str_tokens, weights)
            #logging.warning('\nPredicted features\n:%s' % predicted_features)

            weights = weights + (learning_rate *
            (gold_features - predicted_features))
            #diff =  gold_features - predicted_features
            #logging.warning('\nUnrated weights difference:\n%s' % diff)
            logging.warning('Summed rated weights:\n%s' % weights)

        weights = weights / sqrt(sum([i ** 2 for i in weights]))
        logging.warning('L2 normalization:\n%s' % weights)
        weights_history.append(weights)
        logging.warning('\n\nWeights history:\n%s' % weights_history)

    weights_averaged = 1 / (learning_epochs
    - burn_in_epochs) * sum(weights_history[burn_in_epochs:])
    return weights_averaged


def get_weight(training_set):
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    features, weights = Aligner.align(training_set.p_str_tokens,
        training_set.h_str_tokens, weights)
    print weights

if __name__ == '__main__':
    # Read the problems
    pickle_file = os.path.join(os.path.dirname(__file__),
    'training_data/alignment_problems.p')
    training_set = open(pickle_file)
    training_data = pickle.load(training_set)
    training_set.close()
    get_weight(training_data[11])