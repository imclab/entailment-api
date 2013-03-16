# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavin

Features:
0 EQ                    boolean
1 SUB                   boolean
2 DEL                   boolean
3 INS                   boolean
4 SIM: max of           real
    -path               real
    -synonymy           boolean
    -antonymy           boolean
    -hypernymy          real
    -hyponymy           real
    -JC                 real
    -lin                real
    -nomb               .75 or 0
    -string             real
5 distortion            real
6 matching predecessor  boolean
7 matching successor    boolean
8 both CC               boolean
9 both CD               boolean
10 both DT              boolean
11 both IN              boolean
12 both NN              1 iff same POS, .75 if same group
13 both VB              1 iff same POS, .75 if same group
14 both JJ              1 iff same POS, .75 if same group
15 both RB              1 iff same POS, .75 if same group
16 both POS             boolean
17 both TO              boolean
18 both WDT             boolean
19 both WP              boolean
20 both WP$             boolean                            DOES NOT WORK
21 both WRB             boolean
22 are same lowercased  boolean
23 misc_align           boolean
"""
from __future__ import division
import os
import csv
from math import fabs
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.corpus.reader.wordnet import WordNetError
from nltk.metrics import edit_distance
from nltk.tokenize import word_tokenize
import numpy as np
from model import Alignment_sub as SUB

# Make a list of nominals: verb, adj (nom)
nom_adj_verb_tuples_file = os.path.join(os.path.dirname(__file__),
    'resources/verb_nom_tuples.txt')
with open(nom_adj_verb_tuples_file) as f:
    nom_adj_verb_tuples = f.readlines()

# Make a list of miscelleneous tuples that should be aligned
misc_align_tuples_file = os.path.join(os.path.dirname(__file__),
    'resources/misc_align_tuples.txt')
with open(misc_align_tuples_file) as f:
    misc_align_tuples = f.read().splitlines()

# Make list of previously misclassified antonyms
antonym_file = os.path.join(os.path.dirname(__file__),
    'resources/antonyms.txt')
reader = csv.reader(open(antonym_file, "rb"), delimiter=",")
antonym_tuples = []
for ant_tuple in reader:
    antonym_tuples.append((ant_tuple[0], ant_tuple[1]))


lemmatizer = WordNetLemmatizer()
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')


def get_synsets(token, wn_tag):
    if wn_tag != 'SKIP':
        lemma = lemmatizer.lemmatize(token, pos=wn_tag)
        return wn.synsets(lemma, pos=wn_tag)
    return []


def featurize(edit, p_tokens, h_tokens, p_len, h_len):
    features = np.zeros(24, dtype=float)
    if edit.edit_type == 'EQ':
        features[0] = 1
        features[4] = 1

    elif edit.edit_type == 'SUB':
        p_synsets = get_synsets(edit.p_token, edit.p_wn_tag)
        h_synsets = get_synsets(edit.h_token, edit.h_wn_tag)
        features[1] = 1
        features[4] = max(
            get_path_similarity(p_synsets, h_synsets),
            get_synonymy(edit, p_synsets, h_synsets),
            get_antonymy(edit, p_synsets, h_synsets),
            get_hypernymy(p_synsets, h_synsets),
            get_hyponymy(p_synsets, h_synsets),
            get_jiang_conrath_similarity(p_synsets, h_synsets),
            get_lin_similarity(p_synsets, h_synsets),
            get_nomb(edit.p_token, edit.h_token),
            get_string_similarity(edit.p_token, edit.h_token),
        )
    elif edit.edit_type == 'DEL':
        features[2] = 1
    elif edit.edit_type == 'INS':
        features[3] = 1

    if edit.edit_type == 'EQ' or edit.edit_type == 'SUB':
        features[5] = get_distortion(edit, p_len, h_len)
        features[6] = get_predecessor_match(
            edit.p_index, edit.h_index, p_tokens, h_tokens)
        features[7] = get_successor_match(
            edit.p_index, edit.h_index, p_tokens, h_tokens)
        features[8] = is_matching_CC(edit)
        features[9] = is_matching_CD(edit)
        features[10] = is_matching_DT(edit)
        features[11] = is_matching_IN(edit)
        features[12] = is_matching_NN(edit)
        features[13] = is_matching_VB(edit)
        features[14] = is_matching_JJ(edit)
        features[15] = is_matching_RB(edit)
        features[16] = is_matching_POS(edit)
        features[17] = is_matching_TO(edit)
        features[18] = is_matching_WDT(edit)
        features[19] = is_matching_WP(edit)
        features[20] = is_matching_WPP(edit)
        features[21] = is_matching_WRB(edit)
        features[22] = is_same_lowercased(edit)
        features[23] = misc_align(edit)
    return features


def is_same_lowercased(edit):
    '''
    Return 1 if the tokens are the same when lowercased.
    '''
    if edit.p_token.lower() == edit.h_token.lower():
        return 1
    return 0


def misc_align(edit):
    '''
    Return 1 if the tokens are a pair in the misc align list.
    '''
    if ','.join((edit.p_token, edit.h_token)) in misc_align_tuples \
    or ','.join((edit.h_token, edit.p_token)) in misc_align_tuples:
        return 1
    return 0


def get_successor_match(p_str_index, h_str_index, p_tokens, h_tokens):
    '''
    Return 1 if the successor edit matches

    Keyword arguments:
    p_index -- the index of the token in p
    h_index -- the index of the token in h
    p_tokens -- the tokens of p
    h_tokens -- the tokens of h
    '''
    if p_str_index + 1 < len(p_tokens) and h_str_index + 1 < len(h_tokens):
        if p_tokens[p_str_index + 1] == h_tokens[h_str_index + 1]:
            return 1
    return 0


def get_predecessor_match(p_str_index, h_str_index, p_tokens, h_tokens):
    '''
    Return 1 if the predecessor edit matches

    Keyword arguments:
    p_index -- the index of the token in p
    h_index -- the index of the token in h
    p_tokens -- the tokens of p
    h_tokens -- the tokens of h
    '''
    DT = ['a', 'an', 'the']
    if p_str_index > 0 and h_str_index > 0:
        if p_tokens[p_str_index - 1] == h_tokens[h_str_index - 1]:
            return 1
        if p_tokens[p_str_index - 1] in DT and h_tokens[h_str_index - 1] in DT:
            return 1
    return 0


def get_path_similarity(p_synsets, h_synsets):
    '''

    '''
    scores = [0]
    for p_synset in p_synsets:
        h_synset_scores = [0]
        for h_synset in h_synsets:
            path_sim = p_synset.path_similarity(h_synset)
            if path_sim is None:
                path_sim = 0
            h_synset_scores.append(path_sim)
        scores.append(max(h_synset_scores))
    return max(scores)


def get_distortion(edit, p_len, h_len):
    '''
    Return real distortion value

    Keyword arguments:
    edit -- the edit being featurized
    p -- the premise sentence
    h -- the hypothesis sentence
    '''
    return 1 - fabs(((edit.p_index + 1) / p_len) - ((edit.h_index + 1) / h_len))


def is_matching_NN(edit):
    '''
    TODO
    -Also score if NN matches pronoun
    '''
    if edit.p_wn_tag == edit.h_wn_tag == wn.NOUN:
        if edit.p_penn_tag == edit.h_penn_tag:
            return 1
        else:
            return 0.75
    return 0


def is_matching_VB(edit):
    if edit.p_wn_tag == edit.h_wn_tag == wn.VERB:
        if edit.p_penn_tag == edit.h_penn_tag:
            return 1
        else:
            return 0.75
    return 0


def is_matching_JJ(edit):
    if edit.p_wn_tag == edit.h_wn_tag == wn.ADJ:
        if edit.p_penn_tag == edit.h_penn_tag:
            return 1
        else:
            return 0.75
    return 0


def is_matching_RB(edit):
    if edit.p_wn_tag == edit.h_wn_tag == wn.ADV:
        if edit.p_penn_tag == edit.h_penn_tag:
            return 1
        else:
            return 0.75
    return 0


def is_matching_CC(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'CC':
        return 1
    return 0


def is_matching_CD(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'CD':
        return 1
    return 0


def is_matching_DT(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'DT':
        return 1
    return 0


def is_matching_IN(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'IN':
        return 1
    return 0


def is_matching_POS(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'POS':
        return 1
    return 0


def is_matching_TO(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'TO':
        return 1
    return 0


def is_matching_WDT(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'WDT':
        return 1
    return 0


def is_matching_WP(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'WP':
        return 1
    return 0


def is_matching_WPP(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'WP$':
        return 1
    return 0


def is_matching_WRB(edit):
    if edit.p_penn_tag == edit.h_penn_tag == 'WRB':
        return 1
    return 0


def get_synonymy(edit, p_synsets, h_synsets):
    h_synonyms = [l.name for s in h_synsets for l in s.lemmas]
    p_synonyms = [l.name for s in p_synsets for l in s.lemmas]
    if edit.h_token in p_synonyms:
        return 1
    elif edit.p_token in h_synonyms:
        return 1
    else:
        return 0


def get_antonymy(edit, p_synsets, h_synsets):
    # if (p,h) in list or if (h,p) in antonym_tuples
    if (edit.p_token, edit.h_token) in antonym_tuples or \
    (edit.h_token, edit.p_token) in antonym_tuples:
        return 1

    # Antonyms of h
    h_antonym_synsets = [l.antonyms() for s in h_synsets for l in s.lemmas]
    h_antonyms = []
    for lemma_list in h_antonym_synsets:
        for lemma in lemma_list:
            h_antonyms += [name for name in lemma.synset.lemma_names]
    # Antonyms of p
    p_antonym_synsets = [l.antonyms() for s in p_synsets for l in s.lemmas]
    p_antonyms = []
    for lemma_list in p_antonym_synsets:
        for lemma in lemma_list:
            p_antonyms += [name for name in lemma.synset.lemma_names]
    # Synonyms of p
    p_lemmas = []
    for synset in p_synsets:
        p_lemmas += synset.lemma_names
    # Synonyms of h
    h_lemmas = []
    for synset in h_synsets:
        h_lemmas += synset.lemma_names
    # Check if pair are antonyms
    for p_synonym in p_lemmas:
        if p_synonym in h_antonyms:
            return 1
    for h_synonym in h_lemmas:
        if h_synonym in p_antonyms:
            return 1
    return 0


def get_hypernymy(p_synsets, h_synsets):
    path_distances = []
    for p_synset in p_synsets:
        #logging.info('p synset is ' + str(p_synset))
        p_hypernyms = p_synset.hypernym_distances()
        for h_synset in h_synsets:
            #logging.info('h synset is ' + str(h_synset))
            if h_synset in [synset_dist_tuple[0] for synset_dist_tuple in p_hypernyms]:
                for synset in p_hypernyms:
                    if synset[0] == h_synset:
                        #logging.info('Found h as hypernym of p: ' + str(synset))
                        if synset[1] != 0:
                            path_distances.append(synset[1])
    if len(path_distances) > 0:
        #logging.info(path_distances)
        shortest_path = min(path_distances)
        score = 1 - (shortest_path / 8)
        return score
    else:
        return 0


def get_hyponymy(p_synsets, h_synsets):
        path_distances = []
        for h_synset in h_synsets:
            #logging.info('h synset is ' + str(h_synset))
            h_hypernyms = h_synset.hypernym_distances()
            for p_synset in p_synsets:
                #logging.info('p synset is ' + str(p_synset))
                if p_synset in [synset_dist_tuple[0] for synset_dist_tuple in h_hypernyms]:
                    for synset in h_hypernyms:
                        if synset[0] == p_synset:
                            #logging.info('Found p as hypernym of h: ' + str(synset))
                            if synset[1] != 0:
                                path_distances.append(synset[1])
        if len(path_distances) > 0:
            #logging.info(path_distances)
            shortest_path = min(path_distances)
            score = 1 - (shortest_path / 8)
            return score
        else:
            return 0


def get_jiang_conrath_similarity(p_synsets, h_synsets):
    scores = [0]
    for p_synset in p_synsets:
        for h_synset in h_synsets:
            try:
                brown_score = p_synset.jcn_similarity(h_synset, brown_ic)
                scores.append(min(brown_score, 1))
                #logging.info('Brown score: %s, %s: %s' % (p_synset, h_synset, brown_score))
            except WordNetError:
                pass
            try:
                semcor_score = p_synset.jcn_similarity(h_synset, semcor_ic)
                scores.append(min(semcor_score, 1))
                #logging.info('Semcor score: %s, %s: %s' % (p_synset, h_synset, semcor_score))
            except WordNetError:
                pass
    return max(scores)


def get_nomb(p_token, h_token):
    pair1 = h_token + ',' + p_token + '\n'
    pair2 = p_token + ',' + h_token + '\n'
    if pair1 in nom_adj_verb_tuples:
        return 0.75
    elif pair2 in nom_adj_verb_tuples:
        return 0.75
    return 0


def get_lin_similarity(p_synsets, h_synsets):
    scores = [0]
    for p_synset in p_synsets:
        for h_synset in h_synsets:
            if p_synset.pos == h_synset.pos != 's':
                try:
                    brown_score = p_synset.lin_similarity(h_synset, brown_ic)
                    scores.append(min(brown_score, 1))
                    #logging.info('DLin: %s. %s: %s' % (p_synset, h_synset, brown_score))
                except WordNetError:
                    pass
                try:
                    semcor_score = p_synset.lin_similarity(h_synset, semcor_ic)
                    scores.append(min(semcor_score, 1))
                    #logging.info('DLin: %s. %s: %s' % (p_synset, h_synset, semcor_score))
                except WordNetError:
                    pass
    return max(scores)


def get_string_similarity(p_token, h_token):
    distance = edit_distance(h_token, p_token)
    max_length = max(len(h_token), len(p_token))
    score = 0
    if max_length > 2:
        score = 1 - (distance / (max_length - 1.99999999999999))
    #if score > 1:
        #logging.warning('score > 1 for %s, %s' % (p_token, h_token))
    return max(0, score)


if __name__ == '__main__':
    feature_names = [
        'EQ', 'SUB', 'DEL', 'INS', 'SIM', 'distortion', 'matching predecessor',
        'matching successor', 'both CC', 'both CD', 'both DT', 'both IN',
        'both NN', 'both VB', 'both JJ', 'both RB', 'both POS', 'both TO',
        'both WDT', 'both WP', 'both WP$', 'both WRB']
#    edit1 = Alignment_sub.Alignment_sub('happy', 'JJ', 'sad', 'JJ')
#    edit1 = Alignment_sub.Alignment_sub('happy', 'JJ', 'mad', 'JJ')
#    edit1 = Alignment_sub.Alignment_sub('abort', 'VB', 'abortion', 'NN')
    #p = "I ate an apple at the fruit stand."
    p = "I ate an apple."
    h = "I ate a fruit."
    #edit1 = SUB.Sub('I', 'PRP', 0, 'I', 'PRP', 0)
    #edit2 = SUB.Sub('ate', 'VBD', 1, 'ate', 'VBD', 1)
    #edit3 = SUB.Sub('an', 'DT', 2, 'a', 'DT', 2)
    #edit4 = SUB.Sub('apple', 'NN', 3, 'fruit', 'NN', 3)
    #edit5 = SUB.Sub('.', '.', 4, '.', '.', 4)
    #edit4 = SUB.Sub('The', 'DT', 1, 'the', 'DT', 4)
    #edit4 = SUB.Sub('living', 'NNS', 3, 'dead', 'NNS', 3)
    edit4 = SUB.Sub("exchange", 'VB', 3, 'exchanged', 'VBD', 3)

    p_tokens = word_tokenize(p)
    h_tokens = word_tokenize(h)
    p_len = len(p_tokens)
    h_len = len(h_tokens)

    features = featurize(edit4, p_tokens, h_tokens, p_len, h_len)
    #print 'EQ:   %s' % features[0]
    #print 'SUB:  %s' % features[1]
    ##print 'DEL:  %s' % features[2]
    #print 'INS:  %s' % features[3]
    #print 'SIM:  %s' % features[4]
    #print 'DIST: %s' % features[5]
    #print 'MP:   %s' % features[6]
    #print 'MS:   %s' % features[7]
    print features[23]
    zipped = zip(feature_names, features)
    for name, feature in zipped:
        print name, feature