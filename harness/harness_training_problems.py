# -*- coding: utf-8 -*-
'''
Read RTE training problems, build training problems, and pickle.

TODO
-need to .lower() tokens


'''
import os
import sys
sys.path.append('/home/gavin/dev/entailment-api')
from itertools import izip
from copy import deepcopy
try:
    import cPickle as pickle
except:
    import pickle  # lint:ok
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from model import Training_problem
from model import Alignment_eq as Eq
from model import Alignment_sub as Sub
from model import Alignment_del as Del
from model import Token
from model import Alignment_ins as Ins

training_problems = []
count = 0

# read the problems txt
filename = os.path.join(os.path.dirname(__file__),
'../training_data/rte_set_1_cleaned.txt')
with open(filename) as f:
    rte_raw = f.readlines()

#rte_raw = rte_raw[-2:]

lemmatizer = WordNetLemmatizer()
tag_converter = {'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV}


verbose = False

def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)

for p, h in pairwise(rte_raw):
    print 'starting', count
    # (token)
    if verbose: print 'p', p
    p_tokens = p.rstrip().split(' ')
    if verbose: print 'tokens', p_tokens
    # (token, penn_tag)
    p_tagged_tokens = pos_tag(p_tokens)
    if verbose: print 'penn tagged tokens', p_tagged_tokens
    # (tag)
    p_tags = [i[1] for i in p_tagged_tokens]
    # (token, wn_tag)
    p_wn_tagged_tokens = []
    for token, tag in p_tagged_tokens:
        if tag[:2] in tag_converter.keys():
            p_wn_tagged_tokens.append((token, tag_converter[tag[:2]]))
        else:
            p_wn_tagged_tokens.append((token, 'SKIP'))
    if verbose: print 'wn tagged tokens', p_wn_tagged_tokens
    # (lemma)
    p_token_lemma_tuples = []
    for token, tag in p_wn_tagged_tokens:
        if tag != 'SKIP':
            p_token_lemma_tuples.append((token, lemmatizer.lemmatize(token, pos=tag)))
        else:
            p_token_lemma_tuples.append((token, token))
    if verbose: print 'lemmas', p_token_lemma_tuples
    # (token)
    p_unaccounted = deepcopy(p_tokens)


    h_raw = h.rstrip().split(' ')
    h_tokens = [t for t in h_raw if not t.startswith('(')]
    h_tagged_tokens = pos_tag(h_tokens)
    h_tags = [i[1] for i in h_tagged_tokens]
    h_partners = [i for i in h_raw[1::2]]
    # (token, wn_tag)
    h_wn_tagged_tokens = []
    for token, tag in h_tagged_tokens:
        if tag[:2] in tag_converter.keys():
            h_wn_tagged_tokens.append((token, tag_converter[tag[:2]]))
        else:
            h_wn_tagged_tokens.append((token, 'SKIP'))

    # (token ,lemma)
    h_token_lemma_tuples = []
    for token, tag in h_wn_tagged_tokens:
        if tag != 'SKIP':
            h_token_lemma_tuples.append((token, lemmatizer.lemmatize(token, pos=tag)))
        else:
            h_token_lemma_tuples.append((token, token))

    gold = []

    for i, token_lemma_tuple in enumerate(h_token_lemma_tuples):
        h_index = i
        if h_partners[i][1] == 'n' or h_partners[i][1] == 'N':
            edit = Ins.Ins(token_lemma_tuple[0])
        else:
            h_tag = h_tags[i]
            p_index = int(h_partners[i][1:-1])
            p_token = p_tokens[p_index - 1]
            p_lemma = p_token_lemma_tuples[p_index - 1][1]
            p_tag = p_tags[p_index - 1]
            if token_lemma_tuple[0] == p_token:
                edit = Eq.Eq(
                    p_token, p_lemma, p_tag, p_index - 1,
                    token_lemma_tuple[0], token_lemma_tuple[1], h_tag, h_index)
                try:
                    p_unaccounted.remove(p_token)
                except:
                    if verbose: print 'Failed to remove', p_token
            else:
                edit = Sub.Sub(
                    p_token, p_lemma, p_tag, p_index - 1,
                    token_lemma_tuple[0], token_lemma_tuple[1], h_tag, h_index)
                try:
                    p_unaccounted.remove(p_token)
                except:
                    if verbose: print 'Failed to remove', p_token


        gold.append(edit)
    for p_token in p_unaccounted:
        edit = Del.Del(p_token)
        gold.append(edit)

    training_problem = Training_problem.Training_problem(
        p_tokens, h_tokens, gold)
    training_problems.append(training_problem)
    count += 1

for training_problem in training_problems:
    print training_problem

# Write the problems
training_set_file = open('../training_data/alignment_problems.p', 'w+b')
pickle.dump(training_problems, training_set_file)
training_set_file.close()

print '\nCollected %s problems' % len(training_problems)
