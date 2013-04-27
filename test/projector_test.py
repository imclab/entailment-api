# -*- coding: utf-8 -*-
import sys, unittest
sys.path.append('/home/gavin/dev/spyder-workspace/lexicalEntailmentClassifier')
import Alignment_sub, Del, Alignment_ins
import Projector

class Test_sequencer(unittest.TestCase):
    
    def setUp(self):
        edit1 = Alignment_sub.Alignment_sub('Jimmy Dean', 'NNP', 'James Dean', 'NNP')
        edit1.lexical_entailment = 0
        edit1.monotonicity = 'up'
        
        edit2 = Del.Del('refused to')
        edit2.lexical_entailment = 4
        edit2.monotonicity = 'up'
        
        edit3 = Alignment_ins.Alignment_ins('did')
        edit3.lexical_entailment = 0
        edit3.monotonicity = 'down'
        
        edit4 = Alignment_ins.Alignment_ins("n't")
        edit4.lexical_entailment = 3
        edit4.monotonicity = 'up'
                
        edit5 = Alignment_sub.Alignment_sub('move', 'VB', 'dance', 'VB')
        edit5.lexical_entailment = 2
        edit5.monotonicity = 'down'
        
        edit6 = Del.Del('blue')
        edit6.lexical_entailment = 1
        edit6.monotonicity = 'up'
        
        edit7 = Alignment_sub.Alignment_sub('jeans', 'NNS', 'pants', 'NNS')
        edit7.lexical_entailment = 1
        edit7.monotonicity = 'up'

        self.edits = [edit1, edit2, edit3, edit4, edit5, edit6, edit7]
        self.targets = [0, 4, 0, 3, 1, 1, 1]
                
    def test_get_projected_atomic_entailments(self):
        predictions = Projector.get_projected_atomic_entailments(self.edits)
        print 'Targets:      %s' % self.targets
        print 'Predictions:  %s' % predictions
        self.assertEqual(predictions, self.targets)
    
if __name__ == '__main__':
    unittest.main()