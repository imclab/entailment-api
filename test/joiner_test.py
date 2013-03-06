# -*- coding: utf-8 -*-
import sys, unittest
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
import Joiner

class Test_sequencer(unittest.TestCase):
    
    def setUp(self):
        self.atomic_entailments = [[4,3,1], [4,3,1], [0, 4, 0, 3, 1, 1, 1]]
        self.targets = [1,1,1]
                
    def test_join_atomic_entailments(self):
        predictions = []
        for i in self.atomic_entailments:
            predictions.append(Joiner.join_atomic_entailments(i))
        
        print 'Targets: %s' % self.targets
        print 'Predictions: %s' % predictions
        self.assertEqual(predictions, self.targets)
    
if __name__ == '__main__':
    unittest.main()
