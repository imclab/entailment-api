# -*- coding: utf-8 -*-
'''
TODO:
    Need to add sub feature for detecting mismatched numbers and equivalent
    numbers.


'''
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
        edit0 = Sub.Sub('hammer', 'hammer', 'NN', 0, 'screwdriver', 'screwdriver', 'NN', 0)
        edit1 = Sub.Sub('eagle', 'eagle', 'NN', 0, 'hawk', 'hawk', 'NN', 0)
        edit2 = Sub.Sub('pamphlet', 'pamphlet', 'NN', 0, 'book', 'book', 'NN', 0)
        edit3 = Sub.Sub('happy', 'happy', 'JJ', 0, 'angry', 'angry', 'JJ', 0)
        edit4 = Sub.Sub('pants', 'pants',' NN', 0, 'shirt', 'shirt', 'NN', 0)
        edit5 = Sub.Sub('underwear', 'underwear', 'NN', 0, 'socks', 'socks', 'NNS', 0)
        edit6 = Sub.Sub('laptop', 'laptop', 'NN', 0, 'tablet', 'tablet', 'NN', 0)
        edit7 = Sub.Sub('Android', 'Android',' NNP', 0, 'iPhone', 'iPhone', 'NNP', 0)
        edit8 = Sub.Sub('Apple', 'Apple', 'NNP', 0, 'Samsung', 'Samsung', 'NNP', 0)
        edit9 = Sub.Sub('cars', 'cars', 'NNS', 0, 'trucks', 'trucks', 'NNS', 0)
        edit10 = Sub.Sub('boats', 'boats', 'NNS', 0, 'cars', 'cars', 'NNS', 0)
        edit11 = Sub.Sub('tables', 'table', 'NNS', 0, 'beds', 'bed', 'NNS', 0)
        edit12 = Sub.Sub('red', 'red', 'JJ', 0, 'green', 'green', 'JJ', 0)
        edit13 = Sub.Sub('purples', 'purples' ,' NNS', 0, 'blues', 'blues', 'NNS', 0)
        edit14 = Sub.Sub('high', 'high', 'JJ', 0, 'low', 'low', 'JJ', 0)
        edit15 = Sub.Sub('attractive', 'attractive', 'JJ', 0, 'ugly', 'ugly', 'JJ', 0)
        edit16 = Sub.Sub('14', '14', 'CD', 0, '999', '999', 'CD', 0)
        edit17 = Sub.Sub('1', '1', 'CD', 0, '3.5', '3,5', 'CD', 0)
        edit18 = Sub.Sub('5', '5', 'CD', 0, '3', '3', 'CD', 0)
        edit19 = Sub.Sub('100', '100', 'CD', 0, '1000', '1000', 'CD', 0)
        edit20 = Sub.Sub('5.4', '5.4', 'CD', 0, '8.8', '8.8', 'CD', 0)
        edit21 = Sub.Sub('apples', 'apple', 'NNS', 0, 'oranges', 'orange', 'NNS', 0)
        edit22 = Sub.Sub('fruits', 'fruit', 'NNS', 0, 'vegetables', 'vegetable', 'NNS', 0)
        edit23 = Sub.Sub('potato', 'potato', 'NN', 0, 'tomato', 'tomato', 'NN', 0)
        edit24 = Sub.Sub('cat', 'cat', 'NN', 0, 'dog', 'dog', 'NN', 0)
        edit25 = Sub.Sub('eagles', 'eagle', 'NNS', 0, 'hawks', 'hawk', 'NNS', 0)
        edit26 = Sub.Sub('eagle', 'eagle', 'NN', 0, 'turkeys', 'turkey', 'NNS', 0)
        edit27 = Sub.Sub('SSD', 'SSD', 'NN', 0, 'HDD', 'HDD', 'NN', 0)
        edit28 = Sub.Sub('drill', 'drill', 'NN', 0, 'saw', 'saw',' NN', 0)
        edit29 = Sub.Sub('Carl', 'Carl', 'NNP', 0, 'John', 'John', 'NNP', 0)
        edit30 = Sub.Sub('Romney', 'Romney', 'NNP', 0, 'Obama', 'Obama', 'NNP', 0)
        edit31 = Sub.Sub('igneous', 'igneous', 'JJ', 0, 'metamorphic', 'metamorphic', 'JJ', 0)
        edit32 = Sub.Sub('oak', 'oak', 'NN', 0, 'pine', 'pine', 'NN', 0)
        edit33 = Sub.Sub('Greek', 'Greek', 'NNP', 0, 'Russian', 'Russian', 'NNP', 0)
        edit34 = Sub.Sub('Christianity', 'Christianity', 'NNP', 0, 'Judaism', 'Judaism', 'NNP', 0)
        edit35 = Sub.Sub('dumb', 'dumb', 'JJ', 0, 'smart', 'smart', 'JJ', 0)
        edit36 = Sub.Sub('happy', 'happy', 'JJ', 0, 'angry', 'angry', 'JJ', 0)
        edit37 = Sub.Sub('dove', 'dove', 'NN', 0, 'owl', 'owl', 'NN', 0)
        edit38 = Sub.Sub('pond', 'pond', 'NN', 0, 'lake', 'lake', 'NN', 0)
        edit39 = Sub.Sub('phone', 'phone', 'NN', 0, 'smartphone', 'smartphone', 'NN', 0)


        self.edits = [
            edit0, edit1, edit2, edit3, edit4,
            edit5, edit6, edit7, edit8, edit9,
            edit10, edit11, edit12, edit13, edit14,
            edit15, edit16, edit17, edit18, edit19,
            edit20, edit21, edit22, edit23, edit24,
            edit25, edit26, edit27, edit28, edit29,
            edit30, edit31, edit32, edit33, edit34,
            edit35, edit36, edit37, edit38, edit39,
        ]
        self.target = [
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
            4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
        ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        num_incorrect = 0
        for prediction, edit in zip(predictions, self.edits):
            if prediction != 4:
                num_incorrect += 1
                print 'Predicted: %s, target: 4' % prediction
                print edit
        print num_incorrect, len(predictions)
        print '%s percent correct' % (
            (len(predictions) - num_incorrect) / len(predictions) * 100)
        self.assertEqual(predictions, self.target)

if __name__ == '__main__':
    unittest.main()
