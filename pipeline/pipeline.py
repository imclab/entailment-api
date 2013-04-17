# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavinhackeling@gmail.com
"""
from os.path import dirname, join
import sys
sys.path.append('/home/gavin/dev/entailment-api')
from classifiers import classifier
#from monotonicity import Marking_collector as Marker
from monotonicity import marker_interface
import sequencer
from projector_monotonicity import project_monotonicity
import arg_types_projector
import joiner


class Pipeline(object):

    def __init__(self):
        self.sequencer = sequencer.Sequencer()
        self.joiner = joiner.Joiner()
        monotonicity_operators_file = join(dirname(__file__),
        '../resources/monotonicity_operators_list.txt')
        with open(monotonicity_operators_file) as f:
            monotonicity_operators = f.readlines()
        self.mon_operators = [l.rstrip() for l in monotonicity_operators]
        self.classifier = classifier.Classifier()
        self.marker = marker_interface.Marker_interface()
        self.arg_types_projector = arg_types_projector.Arg_type_projector()

    def get_entailment(self, p, h, p_tokens, h_tokens, edits):
        if len([t for t in p_tokens if t in self.mon_operators]) > 0:
            p_tokens = [t.encode('utf-8', 'ignore') for t in p_tokens]
            print p_tokens
            p_markings = self.marker.mark(' '.join(p_tokens))
            p_marked_tokens = dict(zip(p_tokens, p_markings))
        else:
            p_monotonicity_markings = ['up'] * len(p_tokens)
            p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))

        if len([t for t in h_tokens if t in self.mon_operators]) > 0:
            h_tokens = [t.encode('utf-8', 'ignore') for t in h_tokens]
            print h_tokens
            h_markings = self.marker.mark(' '.join(h_tokens))
            h_marked_tokens = dict(zip(h_tokens, h_markings))
        else:
            h_monotonicity_markings = ['up'] * len(h_tokens)
            h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))

        # Classify the alignments
        self.classifier.classify_edits(edits)
        # Sequence the alignments
        sequenced_edits, use_arg_type_features, matched_predicate = \
        self.sequencer.sequence(p, h, edits, p_marked_tokens, h_marked_tokens)

        print 'the matching predicate is\n', matched_predicate

        # If the sentences have similar transitive predicates, correct
        # predicted entailments for edits with subject/object mismatches
        #if use_arg_type_features:
            #sequenced_edits = self.arg_types_projector.project(
                #p, h, matched_predicate, sequenced_edits)

        # Project the predicted entailments based on the monotonicities
        projected_entailments = project_monotonicity(sequenced_edits)

        for entailment in projected_entailments:
            print entailment

        # Join the projections
        entailment = self.joiner.join(projected_entailments)
        return sequenced_edits, entailment
