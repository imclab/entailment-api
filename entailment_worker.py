# -*- coding: utf-8 -*-
from nltk import word_tokenize
import aligner as al
import pipeline
import os
import Classifier
import Marking_collector as Marker
import Sequencer
import Projector
import Joiner
from time import time


def entailment_worker(premise, hypothesis, manager_dict):
    '''
    Given a premise and hypothesis, add their similarity score and entailment
    code to the process manager_dict
    '''
    aligner = al.Aligner()
    p_tokens = word_tokenize(premise)
    h_tokens = word_tokenize(hypothesis)
    alignments, score = aligner.align(p_tokens, h_tokens, 'default')

    #monotonicity_operators_file = os.path.join(os.path.dirname(__file__),
    #'resources/monotonicity_operators_list.txt')
    #with open(monotonicity_operators_file) as f:
        #monotonicity_operators = f.readlines()
    #monotonicity_operators = [l.rstrip() for l in monotonicity_operators]

    #pipeline_start = time()
    #if len([t for t in p_tokens if t in monotonicity_operators]) > 0:
        #p_monotonicity_markings = Marker.get_monotonicity_markings(p_tokens)
        #p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))
    #else:
        #print 'Not marking p'
        #p_monotonicity_markings = ['up'] * len(p_tokens)
        #p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))

    #if len([t for t in h_tokens if t in monotonicity_operators]) > 0:
        #h_mark_start = time()
        #h_monotonicity_markings = Marker.get_monotonicity_markings(h_tokens)
        #h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))
        #print 'H marked in %s' % (time() - h_mark_start)
    #else:
        #print 'Not marking h'
        #h_monotonicity_markings = ['up'] * len(h_tokens)
        #h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))

    #classify_start = time()
    #Classifier.classify_edits(alignments)
    #print 'Classified in %s' % (time() - classify_start)
    #sequence_start = time()
    #sequenced_edits = Sequencer.sequence(
        #alignments, p_marked_tokens, h_marked_tokens)
    #print 'Sequenced in %s' % (time() - sequence_start)

    #project_start = time()
    #projected_atomic_entailments = Projector.get_projected_atomic_entailments(
        #sequenced_edits)
    #print 'Projected in %s' % (time() - project_start)
    #entailment = Joiner.join_atomic_entailments(projected_atomic_entailments)
    #print 'Pipeline %s' % (time() - pipeline_start)

    sequenced_edits, entailment_code = pipeline.get_entailment(
        p_tokens, h_tokens, alignments)
    manager_dict[premise] = {
        'premise': premise,
        'score': score,
        'entailment_code': entailment_code
        }