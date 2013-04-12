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


class Classifier(object):

    def __init__(self):
        self.featurizer_del = lexent_featurizer_del.Lexent_featurizer_del()
        self.featurizer_sub = lexent_featurizer_sub.Lexent_featurizer_sub()
        self.clf_del = Lexent_classifier_del_tree.Lexent_classifier_del()
        self.clf_sub = lexent_classifier_sub.Lexent_classifier_sub()

    def convert_del_to_ins(self, prediction):
        if prediction == 1:
            return 2
        elif prediction == 2:
            return 1
        return prediction

    def classify_edits(self, edits):
        for edit in edits:
            if edit.edit_type == 'SUB':
                feature_vector = self.featurizer_sub.get_features(edit)
                edit.lexical_entailment = self.clf_sub.predict(
                    feature_vector)[0]
            elif edit.edit_type == 'DEL':
                feature_vector = self.featurizer_del.get_features(edit)
                edit.lexical_entailment = self.clf_del.predict(
                    feature_vector)[0]
            elif edit.edit_type == 'INS':
                tmp_del = Alignment_del.Del(edit.h_token)
                feature_vector = self.featurizer_del.get_features(tmp_del)
                edit.lexical_entailment = self.clf_del.predict(
                    feature_vector)[0]
