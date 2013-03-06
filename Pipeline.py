# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavin

TODO:
    need to add index distortion feature to edit featurizer
    need to penalize aligning words from relatively different indices

"""
import os
from nltk import word_tokenize
import Classifier
import Marking_collector as Marker
import Sequencer
import Projector
import Joiner
from time import time


def get_entailment(p_tokens, h_tokens, edits):
    monotonicity_operators_file = os.path.join(os.path.dirname(__file__),
    'resources/monotonicity_operators_list.txt')
    with open(monotonicity_operators_file) as f:
        monotonicity_operators = f.readlines()
    monotonicity_operators = [l.rstrip() for l in monotonicity_operators]

    pipeline_start = time()
    p_start = time()
    print 'P tokens:\n%s' % [t.encode('utf-8', 'replace') for t in p_tokens]

    if len([t for t in p_tokens if t in monotonicity_operators]) > 0:
        p_mark_start = time()
        p_monotonicity_markings = Marker.get_monotonicity_markings(p_tokens)
        print 'P markings:   %s' % p_monotonicity_markings
        print 'p tokens:     %s' % p_tokens
        p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))
    else:
        print 'Not marking p'
        p_monotonicity_markings = ['up'] * len(p_tokens)
        p_marked_tokens = dict(zip(p_tokens, p_monotonicity_markings))

    print 'H tokens:\n%s' % [t.encode('utf-8', 'replace') for t in h_tokens]
    h_start = time()

    if len([t for t in h_tokens if t in monotonicity_operators]) > 0:
        h_mark_start = time()
        h_monotonicity_markings = Marker.get_monotonicity_markings(h_tokens)
        h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))
        print 'H marked in %s' % (time() - h_mark_start)
    else:
        print 'Not marking h'
        h_monotonicity_markings = ['up'] * len(h_tokens)
        h_marked_tokens = dict(zip(h_tokens, h_monotonicity_markings))

    classify_start = time()
    Classifier.classify_edits(edits)
    print 'Classified in %s' % (time() - classify_start)
    sequence_start = time()
    sequenced_edits = Sequencer.sequence(
        edits, p_marked_tokens, h_marked_tokens)
    print 'Sequenced in %s' % (time() - sequence_start)

    print 'Sequenced edits:\n'
    for edit in sequenced_edits:
        print edit

    project_start = time()
    projected_atomic_entailments = Projector.get_projected_atomic_entailments(
        sequenced_edits)
    print 'Projected in %s' % (time() - project_start)
    entailment = Joiner.join_atomic_entailments(projected_atomic_entailments)
    print 'Entailment: %s' % entailment
    print 'Pipeline %s' % (time() - pipeline_start)
    print 'returning', entailment
    return sequenced_edits, entailment
