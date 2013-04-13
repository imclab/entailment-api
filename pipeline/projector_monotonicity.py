# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavin

"""


def project_monotonicity(edits):
    '''
    Project the lexical entailment predictions based on the alignment's
    monotonicity.
    '''
    projected_atomic_entailments = []
    for edit in edits:
        if edit.monotonicity == 'non':
            projected_atomic_entailments.append(6)
        elif edit.monotonicity == 'down' and int(edit.lexical_entailment) == 1:
            projected_atomic_entailments.append(2)
        elif edit.monotonicity == 'down' and int(edit.lexical_entailment) == 2:
            projected_atomic_entailments.append(1)
        elif edit.monotonicity == 'down' and int(edit.lexical_entailment) == 4:
            projected_atomic_entailments.append(5)
        elif edit.monotonicity == 'down' and int(edit.lexical_entailment) == 5:
            projected_atomic_entailments.append(4)
        else:
            projected_atomic_entailments.append(edit.lexical_entailment)
    return projected_atomic_entailments