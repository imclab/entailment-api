# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/gavin/dev/entailment-api')
import logging
import numpy as np
from model import Alignment_sub as Sub
import lexent_featurizer_sub
from time import time
from nltk import word_tokenize
from nltk import pos_tag
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok


start = time()
lemmatizer = WordNetLemmatizer()
tagConversionDict = {'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV}

with open('../training_data/train_sub.txt') as f:
    lines = f.readlines()

feature_vectors = []
targets = np.zeros(len(lines), dtype=np.int)

print 'number of SUB edits: %s' % len(lines)

for index, line in enumerate(lines):
    parts = line.strip().split('\t')
    print parts
    p_tokens = parts[0].split(' ')
    h_tokens = parts[1].split(' ')

    lexicalEntailment = parts[2]
    targets[index] = lexicalEntailment
    p_pos_tag = parts[3].split(';')
    h_pos_tag = parts[4].split(';')

    p_token = p_tokens[0]
    h_token = h_tokens[0]
    p_pos_tag = p_pos_tag[0]
    h_pos_tag = h_pos_tag[0]

    if p_pos_tag[:2] in tagConversionDict:
        p_wn_tag = tagConversionDict[p_pos_tag[:2]]
        p_lemma = lemmatizer.lemmatize(p_token, p_wn_tag)
    else:
        p_lemma = p_token

    if h_pos_tag[:2] in tagConversionDict:
        h_wn_tag = tagConversionDict[h_pos_tag[:2]]
        h_lemma = lemmatizer.lemmatize(h_token, h_wn_tag)
    else:
        h_lemma = h_token

    alignment = Sub.Sub(
        p_token, p_lemma, p_pos_tag, 0,
        h_token, h_lemma, h_pos_tag, 0)

    print '\nAlignment:'
    print str(alignment)
    featurizer = lexent_featurizer_sub.Lexent_featurizer_sub()
    features = featurizer.getFeatures(alignment)
    feature_vectors.append(features)
    print features.tolist()
    logging.info('WNSyn: %s' % features[0])
    logging.info('WNAnt: %s' % features[1])
    logging.info('WNHyper: %s' % features[2])
    logging.info('WNHypo: %s' % features[3])
    logging.info('Jico: %s' % features[4])
    logging.info('DLin: %s' % features[5])
    logging.info('LemSUbSeqF: %s' % features[6])
    logging.info('LemSUbSeqR: %s' % features[7])
    logging.info('LemSUbSeqE: %s' % features[8])
    logging.info('LemSUbSeqN: %s' % features[9])
    logging.info('Light: %s' % features[10])
    logging.info('Preps: %s' % features[11])
    logging.info('Pronoun: %s' % features[12])
    logging.info('String edit: %s' % features[13])
    logging.info('NNNN: %s' % features[14])
    logging.info('NomB: %s' % features[15])

feature_vectors_matrix = np.vstack(feature_vectors)
print feature_vectors_matrix

# Write the SUB training data
f = open('../classifier_models/sub_model.p', "w+b")
pickle.dump(feature_vectors_matrix, f)
f.close()

# Write the SUB targets
targets_file = open('../classifier_models/sub_targets.p', 'w+b')
pickle.dump(targets, targets_file)
targets_file.close()

print targets
print 'SUB model trained'
print time()-start






























