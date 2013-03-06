# -*- coding: utf-8 -*-
from __future__ import division
import sys
import unittest
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
from model import Alignment_sub as Sub
import Classifier


class Test_classifier(unittest.TestCase):

    def setUp(self):
        edit0 = Sub.Sub('birds', 'bird', 'NNS', 0, 'hammer', '', 'NN', 0)
        self.edits = [
            edit0, 
        ]
        self.target = [
            5, 
        ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        print 'Edit:\n%s\nTarget: %s\nPrediction: %s' % (
            self.edits[0], self.target[0], predictions[0])
        self.assertEqual(predictions[0], self.target[0])

if __name__ == '__main__':
    unittest.main()
