# -*- coding: utf-8 *-*
"""

TODO: It associates NNPs too readily!!!


"""
import sys
import logging
import unittest
sys.path.append('/home/gavin/dev/aissist')
from nltk import word_tokenize
import Aligner
import Pipeline
from time import time


class Test_pipeline(unittest.TestCase):

    def setUp(self):

        self.answer = {
            0: 'Yes',
            1: 'Yes',
            2: 'No',
            3: 'No',
            4: 'No',
            5: 'No',
            6: 'No'
        }


        self.p = "I ate an apple."
        self.h = "I ate a fruit."
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 1

    def runTest(self):
        start = time()
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)
        print "Alignment %s" % (time() - start)
        #print 'Alignments:\n'
        for a in alignments:
            print a

        prediction = Pipeline.get_entailment(
            self.p_str_tokens, self.h, alignments)
        logging.info('Target: %s' % self.target)
        logging.info('Prediction: %s' % prediction)
        print 'Answer: %s' % self.answer[prediction]
        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()