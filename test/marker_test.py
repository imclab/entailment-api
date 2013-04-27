# -*- coding: utf-8 -*-
import sys, unittest
from nltk.tokenize import word_tokenize
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
import Marking_collector

class Test_sequencer(unittest.TestCase):
    
    def setUp(self):
        self.tokens = word_tokenize("James Dean didn't dance without pants")
        self.targets = ['down', 'down', 'down', 'down', 'down', 'up', 'up']
                
    def test_get_monotonicity_markings(self):
        predictions = Marking_collector.get_monotonicity_markings(self.tokens)
        print 'Tokens: %s' % self.tokens
        print 'Targets: %s' % self.targets
        print 'Predictions: %s' % predictions
        self.assertEqual(predictions, self.targets)
    
if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    