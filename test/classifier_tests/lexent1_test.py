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
        edit0 = Sub.Sub('birds', 'bird', 'NNS', 0, 'animals', 'animal', 'NNS', 0)
        edit1 = Sub.Sub('bird', 'bird', 'NN', 0, 'creature', 'creature', 'NN', 0)
        edit2 = Sub.Sub('hammer', 'hammer', 'NN', 0, 'tool', 'tool', 'NN', 0)
        edit3 = Sub.Sub('squirrel', 'squirrel', 'NN', 0, 'mammal', 'mammal', 'NN', 0)
        edit4 = Sub.Sub('pelicans', 'politican', 'NNS', 0, 'birds', 'bird', 'NNS', 0)
        edit5 = Sub.Sub('rat', 'rat', 'NN', 0, 'rodent', 'rodent', 'NN', 0)
        edit6 = Sub.Sub('potato', 'potato', 'NN', 0, 'food', 'food', 'NN', 0)
        edit7 = Sub.Sub('apple', 'apple', 'NN', 0, 'fruit', 'fruit', 'NN', 0)
        edit8 = Sub.Sub('water', 'water', 'NNS', 0, 'substance', 'substance', 'NNS', 0)
        edit9 = Sub.Sub('music', 'music', 'NNS', 0, 'sound', 'squid', 'NNS', 0)
        edit10 = Sub.Sub('music', 'music', 'NNS', 0, 'sound', 'sound', 'NNS', 0)
        edit11 = Sub.Sub('anger', 'anger', 'NN', 0, 'emotion', 'emotion', 'NN', 0)
        edit12 = Sub.Sub('peanuts', 'peanut', 'NNS', 0, 'nuts', 'nut', 'NNS', 0)
        edit13 = Sub.Sub('noise', 'noise', 'NN', 0, 'sound', 'sound', 'NN', 0)
        edit14 = Sub.Sub('Carl', 'Carl', 'NNP', 0, 'human', 'human', 'NN', 0)
        edit15 = Sub.Sub('apple', 'apple', 'NNP', 0, 'company', 'company', 'NN', 0)
        edit16 = Sub.Sub('apple', 'apple', 'NNP', 0, 'business', 'business', 'NN', 0)
        edit17 = Sub.Sub('bed', 'bed', 'NN', 0, 'furniture', 'furniture', 'NN', 0)
        edit18 = Sub.Sub('desk', 'desk', 'NN', 0, 'furniture', 'furniture', 'NN', 0)
        edit19 = Sub.Sub('couch', 'couch', 'NN', 0, 'object', 'object', 'NN', 0)
        edit20 = Sub.Sub('horse', 'horse', 'NN', 0, 'equid', 'equid', 'NN', 0)
        edit21 = Sub.Sub('cow', 'cow', 'NN', 0, 'ungulate', 'ungulate', 'NN', 0)
        edit22 = Sub.Sub('horses', 'horse', 'NN', 0, 'equids', 'equid', 'NNS', 0)
        edit23 = Sub.Sub('horse', 'horse', 'NN', 0, 'ungulate', 'ungulate',  'NN', 0)
        edit24 = Sub.Sub('horses', 'horse', 'NNS', 0, 'ungulates', 'ungulate',  'NNS', 0)
        edit25 = Sub.Sub('cattle', 'cattle', 'NNS', 0, 'ungulateS', 'ungulate', 'NNS', 0)
        edit26 = Sub.Sub('cats', 'cat', 'NNS', 0, 'mammals', 'mammal', 'NNS', 0)
        edit27 = Sub.Sub('cat', 'cat', 'NN', 0, 'mammal', 'mammal', 'NN', 0)
        edit28 = Sub.Sub('dog', 'dog', 'NN', 0, 'mammal', 'mammal', 'NN', 0)
        edit29 = Sub.Sub('girl', 'girl', 'NN', 0, 'person', 'person', 'NN', 0)
        edit30 = Sub.Sub('hotdog', 'hotdog', 'NN', 0, 'food', 'food', 'NN', 0)
        edit31 = Sub.Sub('dinners', 'dinner', 'NNS', 0, 'lunches', 'meal', 'NNS', 0)
        edit32 = Sub.Sub('bulldozer', 'bulldozer', 'NN', 0, 'machine', 'machine', 'NN', 0)
        edit33 = Sub.Sub('turkey', 'turkey', 'NN', 0, 'meat', 'meat', 'NN', 0)
        edit34 = Sub.Sub('turkey', 'turkey', 'NN', 0, 'bird', 'bird', 'NN', 0)
        edit35 = Sub.Sub('chickens', 'chicken', 'NNS', 0, 'birds', 'bird', 'NNS', 0)
        edit36 = Sub.Sub('duck', 'duck', 'NN', 0, 'organism', 'organism', 'NN', 0)
        edit37 = Sub.Sub('cat', 'cat', 'NN', 0, 'vertebrate', 'vertebrate', 'NN', 0)
        edit38 = Sub.Sub('iPhone', 'iPhone', 'NNP', 0, 'phone', 'phone', 'NN', 0)
        edit39 = Sub.Sub('Android', 'Android', 'NNP', 0, 'OS', 'OS', 'NN', 0)
        edit40 = Sub.Sub('plumber', 'plumber', 'NN', 0, 'occupation', 'occupation', 'NN', 0)
        edit41 = Sub.Sub('liver', 'liver', 'NN', 0, 'organ', 'organ', 'NN', 0)
        edit42 = Sub.Sub('quail', 'quail', 'NN', 0, 'bird', 'bird', 'NN', 0)
        edit43 = Sub.Sub('tag', 'tag', 'NN', 0, 'game', 'game', 'NN', 0)
        edit44 = Sub.Sub('Motorola', 'Motorola', 'NNP', 0, 'company', 'company', 'NN', 0)
        edit45 = Sub.Sub('computers', 'computer', 'NNS', 0, 'machines', 'machine', 'NNS', 0)
        edit46 = Sub.Sub('salmon', 'salmon', 'NN', 0, 'fish', 'fish', 'NN', 0)
        edit47 = Sub.Sub('trouts', 'trout', 'NNS', 0, 'fish', 'fish', 'NNS', 0)
        edit48 = Sub.Sub('hamburger', 'hamburger', 'NN', 0, 'food', 'food', 'NN', 0)
        edit49 = Sub.Sub('cheeseburgers', 'cheeseburger', 'NNS', 0, 'foods', 'food', 'NN', 0)
        edit50 = Sub.Sub('TCP', 'TCP', 'NNP', 0, 'protocol', 'protocol', 'NN', 0)
        edit51 = Sub.Sub('red', 'red', 'NN', 0, 'color', 'color', 'NN', 0)
        edit52 = Sub.Sub('vanilla', 'vanilla', 'NN', 0, 'flavor', 'flavor', 'NN', 0)
        edit53 = Sub.Sub('iPad', 'iPad', 'NNP', 0, 'tablet', 'tablet', 'NN', 0)
        edit54 = Sub.Sub('iPads', 'iPad', 'NNPS', 0, 'tablets', 'tablet', 'NNS', 0)
        edit55 = Sub.Sub('SVM', 'SVM', 'NN', 0, 'classifier', 'classifier', 'NN', 0)
        edit56 = Sub.Sub('goat', 'goat', 'NN', 0, 'animal', 'animal', 'NN', 0)
        edit57 = Sub.Sub('bears', 'bear', 'NNS', 0, 'animals', 'animal', 'NNS', 0)
        edit58 = Sub.Sub('mustard', 'mustard', 'NN', 0, 'condiment', 'condiment', 'NN', 0)
        edit59 = Sub.Sub('ketchups', 'ketchup', 'NNS', 0, 'condiments', 'condiment', 'NNS', 0)
        edit60 = Sub.Sub('spider', 'spider', 'NN', 0, 'arachnid', 'arachnid', 'NN', 0)

        self.edits = [
            edit0, edit1, edit2, edit3, edit4, edit5, edit6, edit7, edit8,
            edit9, edit10, edit11, edit12, edit13, edit14, edit15, edit16,
            edit17, edit18, edit19, edit20, edit21, edit22, edit23, edit24,
            edit25, edit26, edit27, edit28, edit29, edit30, edit31, edit32,
            edit33, edit34, edit35, edit36, edit37, edit38, edit39, edit40,
            edit41, edit42, edit43, edit44, edit45, edit46, edit47, edit48,
            edit49, edit50, edit51, edit52, edit53, edit54, edit55, edit56,
            edit57, edit58, edit59, edit60]
        self.target = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, ]

    def runTest(self):
        Classifier.classify_edits(self.edits)
        predictions = [edit.lexical_entailment for edit in self.edits]
        num_incorrect = 0
        for prediction, edit in zip(predictions, self.edits):
            if prediction != 1:
                num_incorrect += 1
                print 'Predicted: %s, target: 1' % prediction
                print edit
                print num_incorrect, len(predictions)
        print '%s percent correct' % (
            (len(predictions) - num_incorrect) / len(predictions) * 100)
        self.assertEqual(predictions, self.target)

if __name__ == '__main__':
    unittest.main()
