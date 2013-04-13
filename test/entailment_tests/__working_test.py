# -*- coding: utf-8 *-*
"""
Created on Fri Jan 11 19:38:12 2013

@author: gavin
"""
import sys
import unittest
from nltk import word_tokenize
sys.path.append('/home/gavin/dev/entailment-api')
from alignment import aligner
from pipeline import pipeline


class Test_pipeline(unittest.TestCase):

    def setUp(self):
        #self.p = "An Irishman won a Nobel Prize."
        #self.h = "An Irishman won the Nobel Prize for Literature."
        self.p = "ChaCha Answer Millard Fillmore was the last president who was neither a Democrat or a Re"
        self.h = "was Millard Fillmore a Democrat"
        #self.p = "Carolina defeated Duke"
        #self.h = "Carolina is a school near Duke"
        #self.h = "Duke beat Carolina"
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = aligner.Aligner()
        self.pipeline = pipeline.Pipeline()
        self.target = 6

    def runTest(self):
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)

        print 'Alignments:\n'
        for a in alignments:
            print a

        sequenced_edits, prediction = self.pipeline.get_entailment(
            self.p, self.h, self.p_str_tokens, self.h_str_tokens, alignments)

        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()

