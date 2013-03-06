# -*- coding: utf-8 -*-
from __future__ import division
import sys
import unittest
sys.path.append('/home/gavin/dev/aissist')
from model import Alignment_sub as Sub
import Classifier


class Test_classifier(unittest.TestCase):

    def setUp(self):
        edit0 = Sub.Sub('like', 'VB', 0, 'dislike', 'VB', 0)
        edit1 = Sub.Sub('incomplete', 'JJ', 0, 'complete', 'JJ', 0)
        edit2 = Sub.Sub('on', 'IN', 0, 'off', 'IN', 0)
        edit3 = Sub.Sub('dead', 'JJ', 0, 'alive', 'JJ', 0)
        edit4 = Sub.Sub('living', 'JJ', 0, 'dead', 'JJ', 0)
        edit5 = Sub.Sub('able', 'JJ', 0, 'unable', 'JJ', 0)
        edit6 = Sub.Sub('competent', 'JJ', 0, 'incompetent', 'JJ', 0)
        edit7 = Sub.Sub('unavailable', 'JJ', 0, 'available', 'JJ', 0)
        edit8 = Sub.Sub('domestic', 'JJ', 0, 'foreign', 'JJ', 0)
        edit9 = Sub.Sub('in-stock', 'JJ', 0, 'sold-out', 'JJ', 0)
        edit10 = Sub.Sub('complete', 'JJ', 0, 'incomplete', 'JJ', 0)
        edit11 = Sub.Sub('unstable', 'JJ', 0, 'stable', 'JJ', 0)

        self.edits = [
            edit0, edit1, edit2, edit3, edit4, edit5, edit6, edit7, edit8,
            edit9, edit10, edit11, ]
        self.target = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        for prediction, edit in zip(predictions, self.edits):
            if prediction != 3:
                print prediction, edit
        self.assertEqual(predictions, self.target)

if __name__ == '__main__':
    unittest.main()
