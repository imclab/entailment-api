# -*- coding: utf-8 -*-
from __future__ import division
import sys, unittest, logging

sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')


import lexent_featurizer_del
import lexent_classifier_del

import Del


class Test_lexent_classifier(unittest.TestCase):
    
    def setUp(self):
        self.featurizer_del = lexent_featurizer_del.Lexent_featurizer_del()
        self.classifier_del = lexent_classifier_del.Lexent_classifier_del()
        self.alignments = []
        self.targets = []
        with open('test_del.txt') as f:
            self.test_cases = f.readlines()
        
        for index, line in enumerate(self.test_cases):
            parts = line.strip().split('\t')
            print parts    
            p_tokens = parts[1].split(' ')                            
            self.targets.append(int(parts[2]))            
            self.alignments.append(Del.Del(p_tokens[0]))
                
    def test_predict(self):
        predictions = []
        for index, a in enumerate(self.alignments):
            feature_vector = self.featurizer_del.getFeatures(a)
            logging.info('Alignment:\n%s' % str(a))
            logging.info('Feature vector:')
            logging.info(feature_vector.tolist())
            prediction = self.classifier_del.predict(feature_vector)
            predictions.append(prediction[0])
        print 'Predictions: %s' % predictions
        for i in range(len(predictions)):
            if predictions[i] != self.targets[i]:
                print 'prediction: %s, target: %s, %s' % \
                (predictions[i], self.targets[i], str(self.alignments[i]))
        print 'Precision: %s' % str(len([i for i, j in zip(predictions, self.targets) if i == j]) / len(predictions))
        self.assertEqual(predictions, self.targets)
        
        
        
#    def tearDown():    
#        pass
    
if __name__ == '__main__':
    unittest.main()