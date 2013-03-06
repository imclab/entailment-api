# -*- coding: utf-8 *-*
"""
Not sure why this is generating 2.
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

        self.answer = {
            0: 'Yes',
            1: 'Yes',
            2: 'No',
            3: 'No',
            4: 'No',
            5: 'No',
            6: 'No'
        }


        self.p = "There's no official Google API for the text to speech"
        self.h = "does google have a text to speech API"
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 3

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
        print 'Answer: %s' % self.answer[prediction]
        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()