# -*- coding: utf-8 -*-
import aligner as al


def alignment_worker(premise, p_tokens, h_tokens, manager_dict):
    '''
    Given a premise and hypothesis, add their similarity score and entailment
    code to the process manager_dict
    '''
    aligner = al.Aligner()
    alignments, score = aligner.align(p_tokens, h_tokens, 'default')

    manager_dict[premise] = {
        'alignments': alignments,
        'score': score,
        'p_tokens': p_tokens
        }