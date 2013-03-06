# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/gavin/dev/aissist')
import numpy as np
import question_featurizer
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
from nltk import word_tokenize

with open('../resources/6530_factoid_questions.txt') as f:
    factoid_questions = f.readlines()

with open('../resources/entailment_questions_unannotated.txt') as f:
    entailment_questions = f.readlines()

targets_factoid = np.zeros(len(factoid_questions), dtype=np.int)
targets_entailment = np.ones(len(entailment_questions), dtype=np.int)
targets = np.concatenate([targets_factoid, targets_entailment])
feature_vectors = []

training_set = factoid_questions + entailment_questions
print 'Training set length:', len(training_set)
featurizer = question_featurizer.Type_featurizer()

for problem in training_set:
    tokens = word_tokenize(problem)
    feature_vectors.append(featurizer.get_features(tokens))


feature_vectors_matrix = np.vstack(feature_vectors)
print feature_vectors_matrix

f = open('../classifier_models/question_type_model.p', "w+b")
pickle.dump(feature_vectors_matrix, f)
f.close()

targets_file = open('../classifier_models/question_type_targets.p', 'w+b')
pickle.dump(targets, targets_file)
targets_file.close()
print 'Training complete'