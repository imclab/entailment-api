# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 19:38:12 2012

@author: gavin

#symbols = {0:'≡',  1:'⊏',  2:'⊐',  3:'^',  4:'|',  5:'C',  6:'#'}
#names = {0:'identical',  1:'forward',  2:'reverse',  3:'negate',
4:'alternate',  5:'cover',  6:'independent'}
"""
import numpy as np


join_table = np.array([
    [0, 1, 2, 3, 4, 5, 6],
    [1, 1, 6, 4, 4, 6, 6],
    [2, 6, 2, 5, 6, 5, 6],
    [3, 5, 4, 0, 2, 1, 6],
    [4, 6, 4, 1, 6, 1, 6],
    [5, 5, 6, 2, 2, 6, 6],
    [6, 6, 6, 6, 6, 6, 6],
], dtype=np.uint)


def join_atomic_entailments(atomic_entailments):
    '''
    Given a sequence of atomic entailment relations,
    compose an entailment relation for the sequence.
    '''
    previousComposition = 0
    for i in atomic_entailments:
        previousComposition = join_table[previousComposition][i]
    return previousComposition













