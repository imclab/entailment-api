# -*- coding: utf-8 *-*
"""
Created on Fri Jan 11 19:38:12 2013

@author: gavin
"""
import sys
import logging
import unittest
from nltk import word_tokenize
sys.path.append('/home/gavin/dev/entailment-api')
import Aligner
import Pipeline


class Test_pipeline(unittest.TestCase):

    def setUp(self):
        #self.p = "An Irishman won a Nobel Prize."
        #self.h = "An Irishman won the Nobel Prize for Literature."
        self.p = "Millard Fillmore was the last president who was neither a Democrat nor a Republican."
        self.h = "was Millard Fillmore a Democrat"
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 6

    def runTest(self):
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)

        print 'Alignments:\n'
        for a in alignments:
            print a

        sequenced_edits, prediction = Pipeline.get_entailment(
            self.p_str_tokens, self.h_str_tokens, alignments)

        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()

