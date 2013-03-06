# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/gavin/dev/aissist')
import logging
import numpy as np
from model import Alignment_del as align
import lexent_featurizer_del

try:
    import cPickle as pickle
except:
    import pickle  # lint:ok

#with open('test1.txt') as f:
with open('../training_data/train_del.txt') as f:
    lines = f.readlines()

feature_vectors = []
targets = np.zeros(len(lines), dtype=np.int)

print 'number of alignments: %s' % len(lines)

for index, line in enumerate(lines):
    parts = line.strip().split('\t')
    print parts
    p_tokens = parts[1].split(' ')
    lexicalEntailment = parts[2]
    print 'lex: %s ' % lexicalEntailment
    targets[index] = lexicalEntailment
    alignment = align.Del(p_tokens[0])

    print '\nAlignment:\n %s' % str(alignment)
    featurizer = lexent_featurizer_del.Lexent_featurizer_del()
    features = featurizer.getFeatures(alignment)
    feature_vectors.append(features)
    print features.tolist()
    logging.info('Light: %s' % features[0])
    logging.info('Pronoun: %s' % features[1])
    logging.info('MiscDel0: %s' % features[2])
    logging.info('MiscDel1: %s' % features[3])
    logging.info('MiscDel2: %s' % features[4])
    logging.info('MiscDel3: %s' % features[5])
    logging.info('MiscDel4: %s' % features[6])
    logging.info('MiscDel5: %s' % features[7])
    logging.info('MiscDel6: %s' % features[8])


feature_vectors_matrix = np.vstack(feature_vectors)
print feature_vectors_matrix

f = open('../classifier_models/del_model.p', "w+b")
pickle.dump(feature_vectors_matrix, f)
f.close()

targets_file = open('../classifier_models/del_targets.p', 'w+b')
pickle.dump(targets, targets_file)
targets_file.close()
print 'targets:\n%s' % targets
logging.info('DEL model trained')






























