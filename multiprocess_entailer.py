# -*- coding: utf-8 -*-
from multiprocessing import Process, Manager
import entailment_worker
import alignment_worker
from time import time

import aligner as al
import pipeline
from nltk import word_tokenize

from os.path import join, dirname

import lexent_classifier
import Projector
import Joiner
import Sequencer
import Marking_collector as Marker


class Multiprocess_entailer(object):

    def __init__(self):
        # Create the process manager
        self.manager = Manager()
        self.classifier = lexent_classifier.Lexent_classifier()

        # Create a list of monotonicity operators
        monotonicity_operators_file = join(dirname(__file__),
        'resources/monotonicity_operators_list.txt')
        with open(monotonicity_operators_file) as f:
            monotonicity_operators = f.readlines()
        self.mon_operators = [
            l.rstrip() for l in monotonicity_operators]


    def entail(self, premises, hypothesis):
        start_time = time()
        for p in premises:
            print 'p', p.encode('utf-8', 'replace')
        print 'h', hypothesis.encode('utf-8', 'replace')

        manager_dict = self.manager.dict()
        jobs = []

        h_tokens = word_tokenize(hypothesis)
        for premise in premises:
            p_tokens = word_tokenize(premise)
            process = Process(
                target=alignment_worker.alignment_worker,
                args=(premise, p_tokens, h_tokens, manager_dict))
            jobs.append(process)
            process.start()

        for job in jobs:
            job.join()

        for i in manager_dict.values():
            alignments = i['alignments']
            score = i['score']
            p_tokens = i['p_tokens']

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

            self.classifier.classify(alignments)
            sequenced_edits = Sequencer.sequence(
                alignments, p_marked_tokens, h_marked_tokens)
            projected_atomic_entailments = Projector.get_projections(
                sequenced_edits)
            entailment = Joiner.join_atomic_entailments(
                projected_atomic_entailments)
            print 'Multi:', entailment


        #return sequenced_edits, entailment

        #multiprocess worker alignment
        #serial the rest

        #print '\nCompleted multiprocessing'
        #for i in manager_dict.values():
            #print i['entailment_code'], i['premise']
        # Values should be (sim score, ent code)
        # Then need to predict based on values
        # Should make feature vector by extending values
        #entailment_code = entailment_classifier.classify(feature_vector)

        print '\n\nCompleted in multi', time() - start_time

        entailment_readable = ['yes', 'yes', 'unknown', 'no', 'no', 'no', 'no']
        premise = ''
        entailment_code = -1

        return premise, entailment_code, entailment_readable[entailment_code]





    def slow(self, premises, hypothesis):
        aligner = al.Aligner()
        h_tokens = word_tokenize(hypothesis)
        all_start = time()
        codes = []
        for premise in premises:
            start_time = time()
            p_tokens = word_tokenize(premise)
            alignments, score = aligner.align(p_tokens, h_tokens, 'default')
            sequenced_edits, entailment_code = pipeline.get_entailment(
                p_tokens, h_tokens, alignments)
            codes.append(entailment_code)
            print 'one:', time() - start_time
        #print '\nCompleted serial processing'
        #for i in codes:
            #print i
        print 'Completed all, serially in', time() - all_start

if __name__ == '__main__':
    premises = [
        'I ate pizza',
        'I ate cake',
        'I jumped',
        'Cats are great'
        ]
    hypothesis = 'I ate food'
    multiprocessor0 = Multiprocess_entailer()
    multiprocessor0.entail(premises, hypothesis)

    multiprocessor2 = Multiprocess_entailer()
    multiprocessor2.slow(premises, hypothesis)
