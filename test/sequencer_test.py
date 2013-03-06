# -*- coding: utf-8 -*-
from __future__ import division
import sys
import unittest
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
import Del
import Alignment_sub
import Alignment_ins
import Sequencer


class Test_sequencer(unittest.TestCase):

    def setUp(self):
        edit1 = Alignment_sub.Alignment_sub(
            'Jimmy Dean', 'NNP', 'James Dean', 'NNP')
        edit2 = Del.Del('refused')
        edit3 = Alignment_sub.Alignment_sub('move', 'VB', 'dance', 'VB')
        edit4 = Del.Del('blue')
        edit5 = Alignment_sub.Alignment_sub('jeans', 'NNS', 'pants', 'NNS')
        edit6 = Alignment_ins.Alignment_ins('did')
        edit7 = Alignment_ins.Alignment_ins("n't")

        self.unordered_edits = [
            edit1, edit2, edit3, edit4, edit5, edit6, edit7]
        self.targets = [edit4, edit1, edit3, edit5, edit2, edit6, edit7]

    def test_sequence(self):
        sequenced_edits = Sequencer.sequence(self.unordered_edits)
        print 'Sequenced edits:\n'
        for i in sequenced_edits:
            print i
        self.assertEqual(sequenced_edits, self.targets)

if __name__ == '__main__':
    unittest.main()
