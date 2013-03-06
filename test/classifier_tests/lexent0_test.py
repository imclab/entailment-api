# -*- coding: utf-8 -*-
from __future__ import division
import sys
import unittest
sys.path.append('/home/gavin/dev/aissist')
from model import Alignment_sub as Sub
import Classifier


class Test_classifier(unittest.TestCase):

    def setUp(self):
        edit0 = Sub.Sub('pig', 'pig', 'NN', 0, 'hog', 'hog', 'NN', 0)
        edit1 = Sub.Sub('buddy', 'buddy', 'NN', 0, 'friend', 'friend', 'NN', 0)
        edit2 = Sub.Sub('Mitt', 'Mitt', 'NNP', 0, 'Romney', 'Romney', 'NNP', 0)
        edit3 = Sub.Sub('Obama', 'Obama', 'NNP', 0, 'Obamma', 'Obamma', 'NNP', 0)
        edit4 = Sub.Sub('happy', 'JJ', 0, 'glad', 'JJ', 0)
        edit5 = Sub.Sub('jump', 'VB', 0, 'leap', 'VB', 0)
        edit6 = Sub.Sub('is', 'VB', 0, 'was', 'VB', 0)
        edit7 = Sub.Sub('bucket', 'NN', 0, 'pail', 'NN', 0)
        edit8 = Sub.Sub('hit', 'VB', 0, 'strike', 'VN', 0)
        edit9 = Sub.Sub('crush', 'VB', 0, 'defeat', 'VB', 0)
        edit9 = Sub.Sub('films', 'NNS', 0, 'movies', 'NNS', 0)
        edit10 = Sub.Sub('go', 'VB', 0, 'attend', 'VB', 0)
        self.edits = [
            edit0, edit1, edit2, edit3, edit4, edit5, edit6, edit7, edit8,
            edit9, edit10, ]
        self.target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        num_incorrect = 0
        for prediction, edit in zip(predictions, self.edits):
            if prediction != 0:
                num_incorrect += 1
                print 'Predicted: %s, target: 0' % prediction
                print edit
                print num_incorrect, len(predictions)
        print '%s percent correct' % (
            (len(predictions) - num_incorrect) / len(predictions) * 100)
        self.assertEqual(predictions, self.target)

if __name__ == '__main__':
    unittest.main()
