# -*- coding: utf-8 -*-
from __future__ import division
import sys
import xml.etree.ElementTree as ET
from nltk import word_tokenize
sys.path.append('/home/gavin/dev/aissist')
import Aligner
import Pipeline


tree = ET.parse('RTE3-TEST-GOLD.xml')
root = tree.getroot()
aligner = Aligner.Aligner()
answer = {
    0: 'YES',
    1: 'YES',
    2: 'NO',
    3: 'NO',
    4: 'NO',
    5: 'NO',
    6: 'NO'
}

total = 0
correct = 0
incorrect = 0
error = 0

for pair in root.findall('pair'):
    target = pair.attrib['entailment']
    pair_id = pair.attrib['id']
    p = pair.find('t').text
    h = pair.find('h').text
    print p.encode('utf-8', 'replace')
    print h.encode('utf-8', 'replace')
    print target, '\n'
    p_str_tokens = word_tokenize(p)
    h_str_tokens = word_tokenize(h)
    weights = 'default'
    alignments, alignments_score = aligner.align(
        p_str_tokens, h_str_tokens, weights)
    #print 'Alignments:\n'
    #for a in alignments:
        #print a
    try:
        prediction = Pipeline.get_entailment(p_str_tokens, h, alignments)
        print 'target:', target
        print 'prediction:', answer[prediction]
        if target != answer[prediction]:
            print 'Pair id %s incorrect' % pair_id
            incorrect += 1
        else:
            print 'Pair id %s CORRECT' % pair_id
            correct += 1
        total += 1
    except:
        error += 1
        total += 1
        pass

print 'Total:', total
print 'Correct:', correct
print 'Correct %s percent' % (correct / total * 100)
print 'Incorrect:', incorrect
print 'Incorrect %s percent' % (incorrect / total * 100)
print 'Error:', error
print 'Error %s percent' % (error / total * 100)