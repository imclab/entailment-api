# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavinhackeling@gmail.com
"""
from os.path import dirname, join
from classifiers import classifier
import Marking_collector as Marker
import sequencer
from projector import project
import joiner


class Pipeline(object):

    def __init__(self):
        self.sequencer = sequencer.Sequencer()
        self.joiner = joiner.Joiner()
        monotonicity_operators_file = join(dirname(__file__),
        'resources/monotonicity_operators_list.txt')
        with open(monotonicity_operators_file) as f:
            monotonicity_operators = f.readlines()
        self.mon_operators = [l.rstrip() for l in monotonicity_operators]
        self.classifier = classifier.Classifier()

    def get_entailment(self, p_tokens, h_tokens, edits):
        if len([t for t in p_tokens if t in self.mon_operators]) > 0:
            p_monotonicity_markings = Marker.get_markings(p_tokens)
            p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))
        else:
            p_monotonicity_markings = ['up'] * len(p_tokens)
            p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))

        if len([t for t in h_tokens if t in self.mon_operators]) > 0:
            h_monotonicity_markings = Marker.get_markings(h_tokens)
            h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))
        else:
            h_monotonicity_markings = ['up'] * len(h_tokens)
            h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))

        # Classify the alignments
        self.classifier.classify_edits(edits)
        # Sequence the alignments
        sequenced_edits = self.sequencer.sequence(
            edits, p_marked_tokens, h_marked_tokens)

        for e in sequenced_edits:
            print e

        # Project the predicted entailments based on the monotonicities
        projected_atomic_entailments = project(sequenced_edits)
        # Join the projections
        entailment = self.joiner.join(projected_atomic_entailments)
        return sequenced_edits, entailment
