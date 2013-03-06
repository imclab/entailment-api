# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:11:02 2012

@author: gavin

Feature vector encodes:
[
    Light, (1 iff in stoplist)                                     -DONE
    Pronoun, (1 iff both are pronouns)                             -DONE
    MiscDel, (set of entailment relations)                         -DONE
        -0
        -1
        -2
        -3
        -4
        -5
        -6
]

TODO for MiscDel features, create separate lists for implicative operators,
but read these lists in the existing functions.

– Deletions of modal verbs often yield #. Thus del(could ) and del(should )
should yield |.
TODO does he mean #?

TODO when checking lists, use lemma for token. -No, lemmatizing is costly and
inaccurate. Just add all surface forms to list.

"""
from __future__ import division
#from nltk.corpus import wordnet as wn
from model import Alignment_del
import numpy as np
import os


class Lexent_featurizer_del:

    def __init__(self):
        filename = os.path.join(os.path.dirname(__file__),
        'resources/verb_nom_tuples.txt')
        with open(filename) as f:
            self.nom_adj_verb_tuples = f.read().splitlines()
        stoplistFile = os.path.join(os.path.dirname(__file__),
        'resources/stoplist.txt')
        with open(stoplistFile) as f:
            self.stoplist = f.read().splitlines()
        prepositionsFile = os.path.join(os.path.dirname(__file__),
        'resources/prepositions.txt')
        with open(prepositionsFile) as f:
            self.prepositions = f.read().splitlines()
        pronounsFile = os.path.join(os.path.dirname(__file__),
        'resources/pronouns.txt')
        with open(pronounsFile) as f:
            self.pronouns = f.read().splitlines()
        miscDel0File = os.path.join(os.path.dirname(__file__),
        'resources/MiscDel0.txt')
        with open(miscDel0File) as f:
            self.miscDel0 = f.read().splitlines()
        self.miscDel1 = ['force']
        self.miscDel2 = []
        miscDel3File = os.path.join(os.path.dirname(__file__),
        'resources/MiscDel3.txt')
        with open(miscDel3File) as f:
            self.miscDel3 = f.read().splitlines()
        miscDel4File = os.path.join(os.path.dirname(__file__),
        'resources/MiscDel4.txt')
        with open(miscDel4File) as f:
            self.miscDel4 = f.read().splitlines()
        self.miscDel5 = []
        miscDel6File = os.path.join(os.path.dirname(__file__),
        'resources/MiscDel6.txt')
        with open(miscDel6File) as f:
            self.miscDel6 = f.read().splitlines()
        v_implicatives_npFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_np.txt')
        with open(v_implicatives_npFile) as f:
            self.v_implicatives_np = f.read().splitlines()
        v_implicatives_poFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_po.txt')
        with open(v_implicatives_poFile) as f:
            self.v_implicatives_po = f.read().splitlines()
        v_implicatives_noFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_no.txt')
        with open(v_implicatives_noFile) as f:
            self.v_implicatives_no = f.read().splitlines()
        v_implicatives_pnFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_pn.txt')
        with open(v_implicatives_pnFile) as f:
            self.v_implicatives_pn = f.read().splitlines()
        v_implicatives_onFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_on.txt')
        with open(v_implicatives_onFile) as f:
            self.v_implicatives_on = f.read().splitlines()
        v_implicatives_noFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_no.txt')
        with open(v_implicatives_noFile) as f:
            self.v_implicatives_no = f.read().splitlines()
        v_implicatives_opFile = os.path.join(os.path.dirname(__file__),
        'resources/v_implicatives_op.txt')
        with open(v_implicatives_opFile) as f:
            self.v_implicatives_op = f.read().splitlines()
        v_factives_ooFile = os.path.join(os.path.dirname(__file__),
        'resources/v_factives_oo.txt')
        with open(v_factives_ooFile) as f:
            self.v_factives_oo = f.read().splitlines()
        v_factives_nnFile = os.path.join(os.path.dirname(__file__),
        'resources/v_factives_nn.txt')
        with open(v_factives_nnFile) as f:
            self.v_factives_nn = f.read().splitlines()
        v_factives_ppFile = os.path.join(os.path.dirname(__file__),
        'resources/v_factives_pp.txt')
        with open(v_factives_ppFile) as f:
            self.v_factives_pp = f.read().splitlines()

    def getLight(self, alignment):
        if alignment.p_token.lower() in self.stoplist:
            return 1
        return 0

    def getPronoun(self, alignment):
        if alignment.p_token.lower() in self.pronouns:
            return 1
        return 0

    def getMiscDel0(self, alignment):
        if alignment.p_token.lower() in self.miscDel0 or \
        alignment.p_token.lower() in self.v_implicatives_pn:
            return 1
        return 0

    def getMiscDel1(self, alignment):
        if alignment.p_token.lower() in self.miscDel1 or \
        alignment.p_token.lower() in self.v_implicatives_po:
            return 1
        return 0

    def getMiscDel2(self, alignment):
        if alignment.p_token.lower() in self.miscDel2 or \
        alignment.p_token.lower() in self.v_implicatives_on:
            return 1
        return 0

    def getMiscDel3(self, alignment):
        if alignment.p_token.lower() in self.miscDel3 or \
        alignment.p_token.lower() in self.v_implicatives_np:
            return 1
        return 0

    def getMiscDel4(self, alignment):
        if alignment.p_token.lower() in self.miscDel4 or \
        alignment.p_token.lower() in self.v_implicatives_no:
            return 1
        return 0

    def getMiscDel5(self, alignment):
        if alignment.p_token.lower() in self.miscDel5 or \
        alignment.p_token.lower() in self.v_implicatives_op:
            return 1
        return 0

    def getMiscDel6(self, alignment):
        if alignment.p_token.lower() in self.miscDel6 or \
        alignment.p_token.lower() in self.v_factives_oo:
            return 1
        return 0

    def getFeatures(self, alignment):
        features = np.zeros(9, dtype=float)
        features[0] = self.getLight(alignment)
        features[1] = self.getPronoun(alignment)
        features[2] = self.getMiscDel0(alignment)
        features[3] = self.getMiscDel1(alignment)
        features[4] = self.getMiscDel2(alignment)
        features[5] = self.getMiscDel3(alignment)
        features[6] = self.getMiscDel4(alignment)
        features[7] = self.getMiscDel5(alignment)
        features[8] = self.getMiscDel6(alignment)
        return features


if __name__ == '__main__':
    edit1 = Alignment_del.Del('Were')
    print edit1
    featurizer = Lexent_featurizer_del()
    print featurizer.getFeatures(edit1)













