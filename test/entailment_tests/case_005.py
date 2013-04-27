# -*- coding: utf-8 *-*
"""
It generates a correct prediction, but for the wrong reasons.
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
        self.p = "The current documentation emphasizes that Flask is best suited to smaller projects"
        self.h = "is flask good for large apps"
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 4

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