# -*- coding: utf-8 *-*
"""

TODO: It associates NNPs too readily!!!


"""
import sys
import logging
import unittest
sys.path.append('/home/gavin/dev/entailment-api')
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

        #self.p = "Butler did not defeat Marquette"
        #self.h = "Did Marquette lose to Butler?"
        self.p = "The Communist Party USA was a small Maoist political party which was founded in 1965 by members of the Communist Party around Michael Laski who took the side of China in the Sino-Soviet split."
        #self.h = "the first president of the United States"
        self.h = "Michael Laski was an opponent of China."
        self.p_str_tokens = word_tokenize(self.p)
        self.h_str_tokens = word_tokenize(self.h)
        self.weights = 'default'
        self.aligner = Aligner.Aligner()
        self.target = 6

    def runTest(self):
        start = time()
        alignments, alignments_score = self.aligner.align(
            self.p_str_tokens, self.h_str_tokens, self.weights)
        print "Alignment %s" % (time() - start)
        #print 'Alignments:\n'
        for a in alignments:
            print a

        sequenced_Edits, prediction = Pipeline.get_entailment(
            self.p_str_tokens, self.h_str_tokens, alignments)
        logging.info('Target: %s' % self.target)
        logging.info('Prediction: %s' % prediction)
        print 'Answer: %s' % self.answer[prediction]
        self.assertEqual(prediction, self.target)

if __name__ == '__main__':
    unittest.main()