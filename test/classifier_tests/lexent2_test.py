# -*- coding: utf-8 -*-
from __future__ import division
import sys
sys.path.append('/home/gavin/dev/aissist')
import logging
import unittest
import Classifier
from model import Alignment_sub as Sub


class Test_classifier(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.WARN)
        edit0 = Sub.Sub('tool', 'NN', 0, 'screwdriver', 'NN', 0)
        edit1 = Sub.Sub('animal', 'NN', 0, 'hawk', 'NN', 0)
        edit2 = Sub.Sub('publication', 'NN', 0, 'book', 'NN', 0)
        edit3 = Sub.Sub('clothes', 'NNS', 0, 'pants', 'NNS', 0)
        edit4 = Sub.Sub('clothing', 'NNS', 0, 'shirt', 'NN', 0)
        edit5 = Sub.Sub('clothes', 'NNS', 0, 'socks', 'NNS', 0)
        edit6 = Sub.Sub('clothing', 'NN', 0, 'socks', 'NNS', 0)
        edit7 = Sub.Sub('computer', 'NN', 0, 'laptop', 'NN', 0)
        edit8 = Sub.Sub('object', 'NN', 0, 'car', 'NN', 0)
        edit9 = Sub.Sub('vehicle', 'NN', 0, 'truck', 'NN', 0)
        edit10 = Sub.Sub('cars', 'NNS', 0, 'convertibles', 'NNS', 0)

        self.edits = [
            edit0, edit1, edit2, edit3, edit4, edit5, edit6, edit7, edit8,
            edit9, edit10]
        self.target = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        num_incorrect = 0
        for prediction, edit in zip(predictions, self.edits):
            if prediction != 2:
                num_incorrect += 1
                print 'Predicted: %s, target: 2' % prediction
                print edit
                print num_incorrect, len(predictions)
        print '%s percent correct' % (
            (len(predictions) - num_incorrect) / len(predictions) * 100)
        self.assertEqual(predictions, self.target)
if __name__ == '__main__':
    unittest.main()
