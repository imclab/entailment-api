# -*- coding: utf-8 -*-

import lexent_featurizer_del
import lexent_featurizer_sub
import lexent_classifier_sub
import lexent_classifier_del
from model import Alignment_del


class Lexent_classifier(object):

    def __init__(self):
        self.featurizer_del = lexent_featurizer_del.Lexent_featurizer_del()
        self.classifier_del = lexent_classifier_del.Lexent_classifier_del()
        self.featurizer_sub = lexent_featurizer_sub.Lexent_featurizer_sub()
        self.classifier_sub = lexent_classifier_sub.Lexent_classifier_sub()

    def convert_del_to_ins(self, prediction):
        if prediction == 1:
            return 2
        elif prediction == 2:
            return 1
        return prediction

    def classify(self, alignments):
        for alignment in alignments:
            if alignment.edit_type == 'SUB':
                feature_vector = self.featurizer_sub.get_features(alignment)
                alignment.lexical_entailment = self.classifier_sub.predict(
                    feature_vector)[0]
            elif alignment.edit_type == 'DEL':
                feature_vector = self.featurizer_del.get_features(alignment)
                alignment.lexical_entailment = self.classifier_del.predict(
                    feature_vector)[0]
            elif alignment.edit_type == 'INS':
                tmp_del = Alignment_del.Del(alignment.h_token)
                feature_vector = self.featurizer_del.get_features(tmp_del)
                alignment.lexical_entailment = self.convert_del_to_ins(
                    self.classifier_del.predict(feature_vector)[0])