# -*- coding: utf-8 -*-
from __future__ import division
import sys
import unittest
sys.path.append('/home/gavin/dev/aissist')
from model import Alignment_sub as Sub
import Classifier


class Test_classifier(unittest.TestCase):

    def setUp(self):
        edit0 = Sub.Sub('birds', 'bird', 'NNS', 0, 'hammer', 'hammer', 'NN', 0)
        edit1 = Sub.Sub('poddle', 'poddle', 'NN', 0, 'laser', 'laser', 'NN', 0)
        edit2 = Sub.Sub('nudist', 'nudist', 'NN', 0, 'sink', 'sink', 'NN', 0)
        edit3 = Sub.Sub('toilet', 'toilet', 'NN', 0, 'dogs', 'dog', 'NNS', 0)
        edit4 = Sub.Sub('Romney', 'Romney', 'NNP', 0, 'red', 'red', 'JJ', 0)
        edit5 = Sub.Sub('hats', 'hat', 'NNS', 0, 'foot', 'foot', 'NN', 0)

        self.edits = [
            edit0, edit1, edit2, edit3, edit4, edit5
        ]
        self.target = [
            6, 6, 6, 6, 6,
        ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        print 'Edit:\n%s\nTarget: %s\nPrediction: %s' % (
            self.edits[0], self.target[0], predictions[0])
        self.assertEqual(predictions[0], self.target[0])

if __name__ == '__main__':
    unittest.main()
