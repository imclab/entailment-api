# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:11:02 2012

@author: gavin

!!!! TODO !!!!!
Add website name/website URL feature
eg, Wikipedia, wikipedia.org, http://www.wikipedia.org
This belongs more in the coref module

Feature vector encodes:
[
    WNSyn, (1 iff p and h are synonyms)                                         -DONE
    WNAnt, (1 iff p and h are antonyms)                                         -DONE
    WNHyper, (1-(n/8) iff h is a hypernym of p, where n is # of links)          -DONE
    WNHypo, (inverse of above)                                                  -DONE
    JiCo, (0-1)                                                                 -DONE
    NomB, (.75 iff in list)                                                     -DONE
    DLin, (score/(max for pos)) (~1 for synonyms)                               -DONE
    LemStrSim, (0-1)                                                            -DONE
    LemSubSeqF, (1 iff p contains h)                                            -NA
    LemSubSeqR, (1 iff h contains p)                                            -NA
    LemSubSeqE, (1 iff p = h)                                                   -NA
    LemSubSeqN, (1 iff p # h)                                                   -NA
    Light, (1 iff in stoplist)                                                  -DONE
    Preps, (1 iff both are prepositions)                                        -DONE
    Pronoun, (1 iff both are pronouns)                                          -DONE
    NNNN, (1 iff both are NN or both are NNP)                                   -DONE
    is_quantifier_lexent_1                                                      -DONE
    is_quantifier_lexent_4                                                      -DONE
    is_quantifier_lexent_6                                                      -DONE
    is_quantifier_all                                                           -DONE
    is_quantifier_some                                                          -DONE
    is_quantifier_none                                                          -DONE
    is_same_lowercased                                                          -DONE
    QuantifierNum, (1 if in [specific cardinal numbers])
    About8MoreQuantifiers,                                                      TODO
    is_un_in_dis_pair
    Quantifier#, (else 1)
    NeqNum, (1 iff both are numbers and p!=h)                                   -DONE
    CoordinateTerms (1-(n/8) if a path connects p and h)                        -DONE
    is_misc_sub_0                                                               -DONE
    is_misc_sub_4                                                               -DONE
    has_same_lemma                                                              -DONE
    are_same_entity_type                                                        -TODO
]


"""
from __future__ import division
import os
import csv
import sys
sys.path.append('/home/gavin/dev/entailment-api')
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.metrics import edit_distance
from nltk.corpus.reader.wordnet import WordNetError
import numpy as np
from model import Alignment_sub
from pipeline import coref_resolver


class Lexent_featurizer_sub(object):

    def __init__(self):
        # Make distribution corpora
        self.brown_ic = wordnet_ic.ic('ic-brown.dat')
        self.semcor_ic = wordnet_ic.ic('ic-semcor.dat')

        # Create coreference and named entity tagger
        self.coref = coref_resolver.Coref_resolver()

        # Make list of misc sub 0
        misc_sub_0_file = os.path.join(os.path.dirname(__file__),
            '../resources/MiscSub0.txt')
        with open(misc_sub_0_file) as f:
            self.misc_sub_0 = f.read().splitlines()

        # Make list of misc sub 4
        misc_sub_4_file = os.path.join(os.path.dirname(__file__),
            '../resources/MiscSub4.txt')
        with open(misc_sub_4_file) as f:
            self.misc_sub_4 = f.read().splitlines()

        # Make list of previously misclassified antonyms
        antonym_file = os.path.join(os.path.dirname(__file__),
            '../resources/antonyms.txt')
        reader = csv.reader(open(antonym_file, "rb"), delimiter=",")
        self.antonym_tuples = []
        for ant_tuple in reader:
            self.antonym_tuples.append((ant_tuple[0], ant_tuple[1]))

        filename = os.path.join(os.path.dirname(__file__),
        '../resources/verb_nom_tuples.txt')
        with open(filename) as f:
            self.nom_adj_verb_tuples = f.readlines()
        self.stoplist = []
        stoplistFile = os.path.join(os.path.dirname(__file__),
        '../resources/stoplist.txt')
        with open(stoplistFile) as f:
            self.stoplist = f.read().splitlines()
        self.prepositions = []
        prepositionsFile = os.path.join(os.path.dirname(__file__),
        '../resources/prepositions.txt')
        with open(prepositionsFile) as f:
            self.prepositions = f.read().splitlines()
        self.pronouns = []
        pronounsFile = os.path.join(os.path.dirname(__file__),
        '../resources/pronouns.txt')
        with open(pronounsFile) as f:
            self.pronouns = f.read().splitlines()
        self.noun_types = ['NN', 'NNS']
        self.proper_noun_types = ['NNP', 'NNPS']
        self.wn_tags = ['n', 'v', 'a', 'r']
        self.quant_1_tuples = [('all', 'some'), ]


    def are_same_entity_type(self, alignment):
        '''
        Return 1 if the tokens are the same entity type
        '''
        p_type = self.coref.get_entity_type(alignment.p_token).keys()
        h_type = self.coref.get_entity_type(alignment.h_token).keys()
        if p_type == h_type:
            return 1
        return 0

    def is_un_in_dis_pair(self, alignment):
        '''
        If (p, h) == (un$1, $1) or ($1, un$1), return 1
        (un-, in-, dis-)
        TODO:
            This should be performed on lemmas, as long as
            the lemmatizer retains these prefixes
        '''

        if alignment.p_token.startswith('un'):
            if alignment.h_token == alignment.p_token[2:]:
                return 1
        if alignment.h_token.startswith('un'):
            if alignment.p_token == alignment.h_token[2:]:
                return 1
        if alignment.p_token.startswith('in'):
            if alignment.h_token == alignment.p_token[2:]:
                return 1
        if alignment.h_token.startswith('in'):
            if alignment.p_token == alignment.h_token[2:]:
                return 1
        if alignment.p_token.startswith('dis'):
            if alignment.h_token == alignment.p_token[3:]:
                return 1
        if alignment.h_token.startswith('dis'):
            if alignment.p_token == alignment.h_token[3:]:
                return 1
        return 0

    def has_same_lemma(self, alignment):
        if alignment.p_lemma == alignment.h_lemma:
            return 1
        return 0


    def is_misc_sub_0(self, alignment):
        if ','.join((alignment.p_lemma, alignment.h_lemma)) in self.misc_sub_0 \
        or ','.join((alignment.h_lemma, alignment.p_lemma)) in self.misc_sub_0:
            return 1
        return 0

    def is_misc_sub_4(self, alignment):
        if ','.join((alignment.p_lemma, alignment.h_lemma)) in self.misc_sub_4 \
        or ','.join((alignment.h_lemma, alignment.p_lemma)) in self.misc_sub_4:
            return 1
        return 0

    def is_same_lowercased(self, alignment):
        if alignment.p_token.lower() == alignment.h_token.lower():
            return 1
        return 0

    def is_quantifier_some(self, alignment):
        quantifiers_some = ['some', 'something', 'several', 'sometime',
            'sometimes', 'few', 'any']
        if alignment.p_token in quantifiers_some \
        and alignment.h_token in quantifiers_some:
            return 1
        return 0

    def is_quantifier_all(self, alignment):
        quantifiers_all = ['all', 'every', 'each', 'both', 'everybody',
            'everything', 'everywhere']
        if alignment.p_token in quantifiers_all \
        and alignment.h_token in quantifiers_all:
            return 1
        return 0

    def is_quantifier_none(self, alignment):
        quantifiers_none = ['no', 'none', 'nothing', 'nobody', 'noone',
            'neither', 'nor']
        if alignment.p_token in quantifiers_none \
        and alignment.h_token in quantifiers_none:
            return 1
        return 0

    def is_quantifier_lexent_1(self, alignment):
        '''
        Return 1 if (p_token, h_token) is in a list of
        tuples of quantifiers that produce lexent 1
        '''
        if (alignment.p_token, alignment.h_token) in self.quant_1_tuples:
            return 1
        return 0

    def is_quantifier_lexent_2(self, alignment):
        '''
        Return 1 if (h_token, p_token) is in a list of
        tuples of quantifiers that produce lexent 1
        '''
        if (alignment.h_token, alignment.p_token) in self.quant_1_tuples:
            return 1
        return 0

    def is_quantifier_lexent_4(self, alignment):
        '''
        TODO: not sure of h, p also valid here
        Return 1 if (p_token, h_token) or (h_token, p_token) is in a list of
        tuples of quantifiers that produce lexent 4
        '''
        lexent_4_quant_tuples = [('all', 'none'), ]
        if (alignment.p_token, alignment.h_token) in lexent_4_quant_tuples \
        or (alignment.h_token, alignment.p_token) in lexent_4_quant_tuples:
            return 1
        return 0

    def is_quantifier_lexent_6(self, alignment):
        '''
        Return 1 if (p_token, h_token) or (h_token, p_token) is in a list of
        tuples of quantifiers that produce lexent 1
        '''
        lexent_6_quant = ['all']
        if alignment.p_token in lexent_6_quant:
            if alignment.h_penn_tag == 'CD':
                return 1
        elif alignment.h_token in lexent_6_quant:
            if alignment.p_penn_tag == 'CD':
                return 1
        return 0

    def getNeqNum(self, alignment):
        if alignment.p_penn_tag == 'CD' and alignment.h_penn_tag == 'CD':
            if alignment.p_token != alignment.h_token:
                return 1
        return 0

    def getNomB(self, alignment):
        h = alignment.h_token
        p = alignment.p_token
        pair1 = h + ',' + p + '\n'
        pair2 = p + ',' + h + '\n'
        if pair1 in self.nom_adj_verb_tuples:
            return 0.75
        elif pair2 in self.nom_adj_verb_tuples:
            return 0.75
        return 0

    def getNNNN(self, alignment):
        h_misses = [
            tag for tag in alignment.h_penn_tag if tag not in self.noun_types]
        p_misses = [
            tag for tag in alignment.p_penn_tag if tag not in self.noun_types]
        if len(h_misses) == 0 and len(p_misses) == 0:
            return 1
        h_misses = [
            tag for tag in alignment.h_penn_tag
            if tag not in self.proper_noun_types]
        p_misses = [
            tag for tag in alignment.p_penn_tag
            if tag not in self.proper_noun_types]
        if len(h_misses) == 0 and len(p_misses) == 0:
            return 1
        return 0

    def getPronoun(self, alignment):
        if alignment.h_token in self.pronouns \
        and alignment.p_token in self.pronouns:
            return 1
        return 0

    def getLemStrSim(self, alignment):
        p = alignment.p_token
        h = alignment.h_token
        distance = edit_distance(h, p)
        max_length = max(len(h), len(p))
        score = 1 - (distance / (max_length - 2.000000001))
        return max(0, score)

    def getLight(self, alignment):
        if alignment.h_token in self.stoplist \
        and alignment.p_token in self.stoplist:
            return 1
        return 0

    def getPreps(self, alignment):
        if alignment.h_token in self.prepositions \
        and alignment.p_token in self.prepositions:
            return 1
        return 0

    def contains(self, small, big):
        for i in xrange(len(big) - len(small) + 1):
            for j in xrange(len(small)):
                if big[i + j] != small[j]:
                    break
            else:
                #return i, i+len(small)
                return True
        return False

    def phrase_contains(self, p, h):
        if self.contains(p, h) or self.contains(h, p):
            return True
        return False

    # The LemSubSeq features are not relevant for a single token
    # alignment representation.
    def getLemSubSeqF(self, alignment):
        p = alignment.p_token
        h = alignment.h_token
        if h in p and p != h:
            return 1
        return 0

    def getLemSubSeqR(self, alignment):
        p = alignment.p_token
        h = alignment.h_token
        if p in h and p != h:
            return 1
        return 0

    def getLemSubSeqE(self, alignment):
        if alignment.h_token == alignment.p_token:
            return 1
        return 0

    def getLemSubSeqN(self, alignment):
        p = alignment.p_token
        h = alignment.h_token
        if p != h \
        and p not in h \
        and h not in p:
            return 1
        return 0

    def are_coordinate_terms(self, alignment, p_synsets, h_synsets):
        if alignment.p_wn_tag in self.wn_tags:
            distances = [100]
            for p_synset in p_synsets:
                for h_synset in h_synsets:
                    distances.append(p_synset.shortest_path_distance(h_synset))
            shortest_distance = min([i for i in distances if i is not None])
            return max(0, 1 - (shortest_distance / 15))
        return 0

    def get_dlin(self, pSynsets, hSynsets):
        scores = [0]
        for p_synset in pSynsets:
            for h_synset in hSynsets:
                try:
                    brown_score = p_synset.lin_similarity(
                        h_synset, self.brown_ic)
                    scores.append(min(brown_score, 1))
                    #logging.info('DLin: %s. %s: %s' % (
                        #p_synset, h_synset, brown_score))
                except WordNetError:
                    pass
                try:
                    semcor_score = p_synset.lin_similarity(
                        h_synset, self.semcor_ic)
                    scores.append(min(semcor_score, 1))
                    #logging.info('DLin: %s. %s: %s' % (
                        #p_synset, h_synset, semcor_score))
                except WordNetError:
                    pass
        return max(scores)

    # TODO if both synsets contain same synset, should that score be counted?
    def getJiCo(self, pSynsets, hSynsets):
        scores = [0]
        for p_synset in pSynsets:
            for h_synset in hSynsets:
                try:
                    brown_score = p_synset.jcn_similarity(
                        h_synset, self.brown_ic)
                    scores.append(min(brown_score, 1))
                    #logging.info('Brown score: %s, %s: %s' % (
                        #p_synset, h_synset, brown_score))
                except WordNetError:
                    pass
                try:
                    semcor_score = p_synset.jcn_similarity(
                        h_synset, self.semcor_ic)
                    scores.append(min(semcor_score, 1))
                    #logging.info('Semcor score: %s, %s: %s' % (
                        #p_synset, h_synset, semcor_score))
                except WordNetError:
                    pass
        return max(scores)

    def getWNHyper(self, pSynsets, hSynsets):
        path_distances = []
        for p_synset in pSynsets:
            #logging.info('p synset is ' + str(p_synset))
            p_hypernyms = p_synset.hypernym_distances()
            for h_synset in hSynsets:
                #logging.info('h synset is ' + str(h_synset))
                if h_synset in [
                    synset_dist_tuple[0] for synset_dist_tuple in p_hypernyms]:
                    for synset in p_hypernyms:
                        if synset[0] == h_synset:
                            #logging.info('Found h as hyper: ' + str(synset))
                            if synset[1] != 0:
                                path_distances.append(synset[1])
        if len(path_distances) > 0:
            #logging.info(path_distances)
            shortest_path = min(path_distances)
            score = 1 - (shortest_path / 8)
            return score
        else:
            return 0

    def getWNHypo(self, pSynsets, hSynsets):
        path_distances = []
        for h_synset in hSynsets:
            #logging.info('h synset is ' + str(h_synset))
            h_hypernyms = h_synset.hypernym_distances()
            for p_synset in pSynsets:
                #logging.info('p synset is ' + str(p_synset))
                if p_synset in [
                    synset_dist_tuple[0] for synset_dist_tuple in h_hypernyms]:
                    for synset in h_hypernyms:
                        if synset[0] == p_synset:
                            #logging.info('Found p as hyper: ' + str(synset))
                            if synset[1] != 0:
                                path_distances.append(synset[1])
        if len(path_distances) > 0:
            #logging.info(path_distances)
            shortest_path = min(path_distances)
            score = 1 - (shortest_path / 8)
            return score
        else:
            return 0

    def getWNAnt(self, alignment, p_synsets, h_synsets):
        # If (p_token, h_token) or (h_token, p_token) is in the list of
        # misclassified antonyms, return 1
        if (alignment.p_token, alignment.h_token) in self.antonym_tuples or \
        (alignment.h_token, alignment.p_token) in self.antonym_tuples:
            return 1

        # Antonyms of h
        h_antonym_synsets = [l.antonyms() for s in h_synsets for l in s.lemmas]
        h_antonyms = []
        for lemma_list in h_antonym_synsets:
            for lemma in lemma_list:
                h_antonyms += [name for name in lemma.synset.lemma_names]
        #print '\nH: %s\nants:\n%s' % (h_synsets, h_antonyms)

        # Antonyms of p
        p_antonym_synsets = [l.antonyms() for s in p_synsets for l in s.lemmas]
        p_antonyms = []
        for lemma_list in p_antonym_synsets:
            for lemma in lemma_list:
                p_antonyms += [name for name in lemma.synset.lemma_names]
        #print '\nP: %s\nants:\n%s' % (p_synsets, p_antonyms)

        # Synonyms of p
        p_lemmas = []
        for synset in p_synsets:
            p_lemmas += synset.lemma_names
        #print '\nP synonyms:\n%s' % p_lemmas
        # Synonyms of h
        h_lemmas = []
        for synset in h_synsets:
            h_lemmas += synset.lemma_names
        #print '\nH synonyms:\n%s' % h_lemmas

        for p_synonym in p_lemmas:
            if p_synonym in h_antonyms:
                #print 'ANTONYM: %s' % (p_synonym)
                return 1
        for h_synonym in h_lemmas:
            if h_synonym in p_antonyms:
                #print 'ANTONYM: %s' % (h_synonym)
                return 1
        return 0

    # return 1 if p and h are synonyms
    def getWNSyn(self, alignment, pSynsets, hSynsets):
        h_synonyms = [l.name for s in hSynsets for l in s.lemmas]
        p_synonyms = [l.name for s in pSynsets for l in s.lemmas]
        #logging.info(h_synonyms)
        #logging.info(p_synonyms)
        if alignment.h_token in p_synonyms:
            #logging.info('h is a synonym of p')
            return 1
        elif alignment.p_token in h_synonyms:
            #logging.info('p is a synonym of h')
            return 1
        else:
            #logging.info('p and h are not synonyms')
            return 0

    def is_NNP_and_NN(self, alignment):
        '''
        Return 1 if p == NNP and h == NN
        '''
        if alignment.p_penn_tag == 'NNP' and alignment.h_penn_tag == 'NN':
            return 1
        return 0

    def is_NN_and_NNP(self, alignment):
        '''
        Return 1 if p == NN and h == NNP
        '''
        if alignment.p_penn_tag == 'NN' and alignment.h_penn_tag == 'NNP':
            return 1
        return 0

    def get_features(self, alignment):
        pSynsets = []
        if alignment.p_wn_tag != 'SKIP':
            pSynsets = wn.synsets(alignment.p_token, pos=alignment.p_wn_tag)
        hSynsets = []
        if alignment.h_wn_tag != 'SKIP':
            hSynsets = wn.synsets(alignment.h_token, pos=alignment.h_wn_tag)
        features = np.zeros(28, dtype=float)
        features[0] = self.getWNSyn(alignment, pSynsets, hSynsets)
        features[1] = self.getWNAnt(alignment, pSynsets, hSynsets)
        features[2] = self.getWNHyper(pSynsets, hSynsets)
        features[3] = self.getWNHypo(pSynsets, hSynsets)
        features[4] = self.getJiCo(pSynsets, hSynsets)
        features[5] = self.get_dlin(pSynsets, hSynsets)
        #features[6] = self.getLemSubSeqF(alignment)
        #features[7] = self.getLemSubSeqR(alignment)
        #features[8] = self.getLemSubSeqE(alignment)
        #features[9] = self.getLemSubSeqN(alignment)
        features[6] = self.is_same_lowercased(alignment)
        features[7] = self.is_NNP_and_NN(alignment)
        features[8] = self.is_NN_and_NNP(alignment)
        features[9] = self.is_un_in_dis_pair(alignment)
        features[10] = self.getLight(alignment)
        features[11] = self.getPreps(alignment)
        features[12] = self.getPronoun(alignment)
        features[13] = self.getLemStrSim(alignment)
        features[14] = self.getNNNN(alignment)
        features[15] = self.getNomB(alignment)
        features[16] = self.is_quantifier_lexent_1(alignment)
        features[17] = self.is_quantifier_lexent_4(alignment)
        features[18] = self.is_quantifier_lexent_6(alignment)
        features[19] = self.is_quantifier_all(alignment)
        features[20] = self.is_quantifier_some(alignment)
        features[21] = self.is_quantifier_none(alignment)
        features[22] = self.getNeqNum(alignment)
        features[23] = self.are_coordinate_terms(alignment, pSynsets, hSynsets)
        features[24] = self.is_misc_sub_0(alignment)
        features[25] = self.is_misc_sub_4(alignment)
        features[26] = self.has_same_lemma(alignment)
        features[27] = self.are_same_entity_type(alignment)
        return features


if __name__ == '__main__':
    #edit1 = Alignment_sub.Sub('99', 'CD', 0, '7.5', 'CD', 0)
    #edit1 = Alignment_sub.Sub('red', 'red', 'NN', 0, 'green', 'green', 'NN', 0)
    edit1 = Alignment_sub.Sub(
        'Carl', 'Carl', 'NNP', 0, 'John', 'John', 'NNP', 0)
    featurizer = Lexent_featurizer_sub()
    #print 'NeqNum: %s' % featurizer.getNeqNum(edit1)
    pSynsets = []
    if edit1.p_wn_tag != 'SKIP':
        pSynsets = wn.synsets(edit1.p_token, pos=edit1.p_wn_tag)
    hSynsets = []
    if edit1.h_wn_tag != 'SKIP':
        hSynsets = wn.synsets(edit1.h_token, pos=edit1.h_wn_tag)
    #print 'CoordinateTerms: %s' % featurizer.are_coordinate_terms(
        #edit1, pSynsets, hSynsets)
    #print featurizer.get(edit1, pSynsets, hSynsets)
    #print featurizer.is_same_lowercased(edit1)
    # print featurizer.is_misc_sub_0(edit1)
    print featurizer.are_same_entity_type(edit1)