# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 11:25:40 2012

@author: gavin
"""
import lexent_featurizer_del
import lexent_featurizer_sub
import lexent_classifier_sub
from model import Alignment_del
import Lexent_classifier_del_tree


def convert_del_to_ins(prediction):
    if prediction == 1:
        return 2
    elif prediction == 2:
        return 1
    return prediction


def classify_edits(edits):
    featurizer_del = lexent_featurizer_del.Lexent_featurizer_del()
    featurizer_sub = lexent_featurizer_sub.Lexent_featurizer_sub()
    classifier_del = Lexent_classifier_del_tree.Lexent_classifier_del()
    classifier_sub = lexent_classifier_sub.Lexent_classifier_sub()

    for edit in edits:
        if edit.edit_type == 'SUB':
            feature_vector = featurizer_sub.getFeatures(edit)
            edit.lexical_entailment = classifier_sub.predict(feature_vector)[0]
        #elif edit.edit_type == 'EQ':
            #feature_vector = featurizer_sub.getFeatures(edit)
            #edit.lexical_entailment = classifier_sub.predict(feature_vector)[0]
        elif edit.edit_type == 'DEL':
            feature_vector = featurizer_del.getFeatures(edit)
            edit.lexical_entailment = classifier_del.predict(feature_vector)[0]
        elif edit.edit_type == 'INS':
            tmp_del = Alignment_del.Del(edit.h_token)
            feature_vector = featurizer_del.getFeatures(tmp_del)
            edit.lexical_entailment = convert_del_to_ins(
                classifier_del.predict(feature_vector)[0])
