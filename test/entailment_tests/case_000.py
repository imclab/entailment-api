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
import aligner_interface


class Test_pipeline(unittest.TestCase):

    def setUp(self):
        #self.p = """
        #Highland Park native was overwhelmed by prospect of prison from charges
        #that he stole MIT articles electronically.
        #"""
        #self.h = "the highland park native was overwhelmed."
        #p = "the cat ate the tasty pizza"
        #h = 'the cat never ate'
        p = 'I did not eat some tasty pizza.'
        h = 'I ate some food.'
        self.p_str_tokens = word_tokenize(p)
        self.h_str_tokens = word_tokenize(h)
        self.weights = 'default'
        #self.aligner = aligner_interface.Aligner_interface()
        self.aligner = Aligner.Aligner()
        self.target = 1


    def runTest(self):
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)

        print 'Alignments:\n'
        for a in alignments:
            print a

        sequenced_edits, entailment_prediction = Pipeline.get_entailment(
            self.p_str_tokens, self.h_str_tokens, alignments)
        logging.info('Target: %s' % self.target)
        logging.info('Prediction: %s' % entailment_prediction)
        self.assertEqual(entailment_prediction, self.target)

if __name__ == '__main__':
    unittest.main()

