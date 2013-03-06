# -*- coding: utf-8 -*-
from __future__ import division
import sys, unittest, logging

sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')


import lexent_featurizer_sub
import lexent_classifier_sub

import alignment


class Test_lexent_classifier(unittest.TestCase):
    
    def setUp(self):
#        self.a = alignment.Phrase_Alignment('SUB', 'ahmedinejad', 'NN', 'adhadinejad', 'NN')
        self.featurizer_sub = lexent_featurizer_sub.Lexent_featurizer_sub()
        self.classifier_sub = lexent_classifier_sub.Lexent_classifier_sub()
        self.alignments = []
        self.targets = []
        with open('test2.txt') as f:
            self.test_cases = f.readlines()
        
        for index, line in enumerate(self.test_cases):
            parts = line.strip().split('\t')
            print parts    
            p_tokens = parts[1].split(' ')  
            
            h_tokens = parts[2].split(' ')    
              
            self.targets.append(int(parts[3]))
            p_pos_tag = parts[4].split(';')
            h_pos_tag = parts[5].split(';')
            
            a = alignment.Phrase_Alignment(\
                'SUB', p_tokens[0], p_pos_tag[0], h_tokens[0], h_pos_tag[0])
                
            if len(h_tokens) > 1:
                for i in range(1,len(h_tokens)):
                    if len(h_tokens) == len(h_pos_tag):
                        alignment.addHToken(h_tokens[i], h_pos_tag[i])
                    elif len(p_pos_tag) == 1:
                        alignment.addPToken(h_tokens[i], h_pos_tag[0])
            if len(p_tokens) > 1:
                for i in range(1,len(p_tokens)):
                    if len(p_tokens) == len(p_pos_tag):
                        alignment.addPToken(p_tokens[i], p_pos_tag[i])
                    elif len(p_pos_tag) == 1:
                        alignment.addPToken(p_tokens[i], p_pos_tag[0])                
            self.alignments.append(a)
                
    def test_predict(self):
        predictions = []
        for index, a in enumerate(self.alignments):
            feature_vector = self.featurizer_sub.getFeatures(a)
            logging.info('Alignment:')
            logging.info(str(a))
            logging.info('Feature vector:')
            logging.info(feature_vector.tolist())
            prediction = self.classifier_sub.predict(feature_vector)
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