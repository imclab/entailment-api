# -*- coding: utf-8 *-*
"""
Created on Fri Jan 11 19:38:12 2013

@author: gavin
"""
import sys
import logging
import unittest
sys.path.append('/home/gavin/dev/aissist')
from nltk import word_tokenize
import Aligner
import Pipeline


class Test_pipeline(unittest.TestCase):

    def setUp(self):
        self.p = "he ate the hats"
        self.h = "he ate the pears"
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 6

    def runTest(self):
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)

        #print 'Alignments:\n'
        for a in alignments:
            print a

        prediction = Pipeline.get_entailment(
            self.p_str_tokens, self.h, alignments)
        logging.info('Target: %s' % self.target)
        logging.info('Prediction: %s' % prediction)
        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()

