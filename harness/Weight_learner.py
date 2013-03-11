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
sys.path.append('/home/gavin/dev/entailment-api')
from random import shuffle
from math import sqrt
import os
import time
import logging
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
import Aligner
import Gold_problem_featurizer as gold_featurizer


def learn_weights(training_set, learning_epochs, burn_in_epochs,
learning_rate, learning_rate_multiplier):
    weights = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ]
    weights_history = []

    for i in range(learning_epochs):
        print '*** Starting epoch %s of %s ***' % (i, learning_epochs)
        learning_rate *= learning_rate_multiplier
        #logging.warning('Starting epoch %s with learning rate %s' %
        #(i, learning_rate))
        shuffle(training_set)

        for index, problem in enumerate(training_set):
            print '* Starting problem %s of %s in epoch %s*' % \
                (index, len(training_set), i)
            print problem.p_str_tokens
            print problem.h_str_tokens
            gold_features = gold_featurizer.featurize(problem)
            #logging.warning('\nStarting weights:\n%s' % weights)

            predicted_alignment, predicted_features = aligner.align(
                    problem.p_str_tokens, problem.h_str_tokens, weights)

            print predicted_features

            weights = weights + (learning_rate *
            (gold_features - predicted_features))
            #logging.warning('Summed rated weights:\n%s' % weights)

        weights = weights / sqrt(sum([i ** 2 for i in weights]))
        #logging.warning('L2 normalization:\n%s' % weights)
        weights_history.append(weights)
        #logging.warning('\n\nWeights history:\n%s' % weights_history)

    weights_averaged = 1 / (learning_epochs
    - burn_in_epochs) * sum(weights_history[burn_in_epochs:])
    return weights_averaged


if __name__ == '__main__':
    aligner = Aligner.Aligner()
    # Read the problems
    pickle_file = os.path.join(os.path.dirname(__file__),
    '../training_data/alignment_problems.p')
    training_set = open(pickle_file)
    training_data = pickle.load(training_set)
    training_set.close()
    t0 = time.clock()
    averaged_weights = learn_weights(training_data, 50, 10, 1, 0.8)
    #averaged_weights = learn_weights(training_data, 1, 0, 1, 0.8)
    t = time.clock() - t0
    logging.warning('Trained in %s' % t)
    logging.warning('Averaged weights:\n%s' % averaged_weights)
    print '\n\n\n', averaged_weights
    weights_file = open('../training_data/weights.p', 'w+b')
    pickle.dump(averaged_weights, weights_file)
    weights_file.close()




















