# -*- coding: utf-8 *-*
"""
Created on Fri Jan 11 19:38:12 2013

@author: gavin
"""
import sys
from nltk import word_tokenize
sys.path.append('/home/gavin/dev/entailment-api')
import aligner
import pipeline
from time import time


class Test(object):

    def __init__(self):
        self.aligner = aligner.Aligner()
        self.pipeline = pipeline.Pipeline()

    def test(self, p, h):
        start = time()
        p_str_tokens = word_tokenize(p)
        h_str_tokens = word_tokenize(h)
        weights = 'default'

        alignments, alignments_score = self.aligner.align(
            p_str_tokens, h_str_tokens, weights)

        sequenced_edits, prediction = self.pipeline.get_entailment(
            p_str_tokens, h_str_tokens, alignments)
        print 'completed test in', time() - start

if __name__ == '__main__':
    tester = Test()
    #p1 = "ChaCha Answer Millard Fillmore was the last president who was neither a Democrat or a Re"
    #h1 = "was Millard Fillmore a Democrat"
    p1 = "An Irishman won a Nobel Prize."
    h1 = "An Irishman won the Nobel Prize for Literature."
    tester.test(p1, h1)
    tester.test(p1, h1)