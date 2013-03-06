# -*- coding: utf-8 -*-
'''
Read RTE training problems, build training problems, and pickle.

TODO
-need to .lower() tokens


'''
import os
import sys
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
sys.path.append('/home/gavin/dev/aissist')
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
from model import Alignment_ins as Ins

training_problems = []

# read the problems txt
filename = os.path.join(os.path.dirname(__file__),
'../training_data/rte_set_1_cleaned.txt')
with open(filename) as f:
    rte_raw = f.readlines()

lemmatizer = WordNetLemmatizer()
tag_converter = {'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV}


def pairwise(iterable):
    "s -> (s0,s1), (s2,s3), (s4, s5), ..."
    a = iter(iterable)
    return izip(a, a)


for p, h in pairwise(rte_raw):
    print p
    p_tokens = p.rstrip().split(' ')
    p_tagged_tokens = pos_tag(p_tokens)
    p_tags = [i[1] for i in p_tagged_tokens]

    p_wn_tagged = []
    for t in p_tagged_tokens:
        if t[1][:2] in tag_converter.keys():
            p_wn_tagged.append((t[0], tag_converter[t[1][:2]]))
        else:
            p_wn_tagged.append((t[0], 'SKIP'))

    p_final_tokens = []
    for t in p_wn_tagged:
        if t[1] != 'SKIP':
            p_final_tokens.append(lemmatizer.lemmatize(t[0], pos=t[1]))
        else:
            p_final_tokens.append(t[0])

    p_unaccounted = deepcopy(p_tokens)

    h_raw = h.rstrip().split(' ')
    h_final_tokens = [t for t in h_raw if not t.startswith('(')]
    h_tagged_tokens = pos_tag(h_final_tokens)
    h_tags = [i[1] for i in h_tagged_tokens]
    h_partners = [i for i in h_raw[1::2]]

    h_wn_tagged = []
    for t in h_tagged_tokens:
        if t[1][:2] in tag_converter.keys():
            h_wn_tagged.append((t[0], tag_converter[t[1][:2]]))
        else:
            h_wn_tagged.append((t[0], 'SKIP'))

    h_final_tokens = []
    for t in h_wn_tagged:
        if t[1] != 'SKIP':
            h_final_tokens.append(lemmatizer.lemmatize(t[0], pos=t[1]))
        else:
            h_final_tokens.append(t[0])

    gold = []

    for i, h_token in enumerate(h_final_tokens):
        h_index = i
        if h_partners[i][1] == 'n' or h_partners[i][1] == 'N':
            edit = Ins.Ins(h_token)
        else:
            h_tag = h_tags[i]
            p_index = int(h_partners[i][1:-1])
            p_token = p_tokens[p_index - 1]
            p_tag = p_tags[p_index - 1]
            if h_token == p_token:
                edit = Eq.Eq(
                    p_token, p_tag, p_index - 1,
                    h_token, h_tag, h_index)
                print edit
                try:
                    p_unaccounted.remove(p_token)
                except:
                    print 'Failed to remove', p_token
            else:
                edit = Sub.Sub(
                    p_token, p_tag, p_index - 1,
                    h_token, h_tag, h_index)
                print edit
                try:
                    p_unaccounted.remove(p_token)
                except:
                    print 'Failed to remove', p_token
        gold.append(edit)
    for p_token in p_unaccounted:
        edit = Del.Del(p_token)
        gold.append(edit)

    training_problem = Training_problem.Training_problem(
        p_tokens, h_final_tokens, gold)
    training_problems.append(training_problem)


# Write the problems
training_set_file = open('../training_data/alignment_problems.p', 'w+b')
pickle.dump(training_problems, training_set_file)
training_set_file.close()

print '\nCollected %s problems' % len(training_problems)
