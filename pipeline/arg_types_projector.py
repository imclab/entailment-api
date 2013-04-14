# -*- coding: utf-8 -*-
'''

'''
import senna_interface


class Arg_type_projector(object):

    def __init__(self):
        self.senna = senna_interface.Senna_interface()

    def project(self, p, h, predicate, alignments):
        '''
        Project lexical entailment predictions based the argument types of the
        tokens in the edit.
        '''
        p_all_arg_types = self.senna.get_arg_types_for_all_predicates(p)
        h_all_arg_types = self.senna.get_arg_types_for_all_predicates(h)
        p_arg_types = p_all_arg_types[predicate.p_token]
        h_arg_types = h_all_arg_types[predicate.h_token]
        p_arg_types = [t[-2:] for t in p_arg_types]
        h_arg_types = [t[-2:] for t in h_arg_types]

        for alignment in alignments:
            if alignment.edit_type in ['SUB', 'EQ']:
                p_arg = p_arg_types[alignment.p_index]
                h_arg = h_arg_types[alignment.h_index]
                arg_types = ['A0', 'A1']
                if p_arg != h_arg and p_arg in arg_types and h_arg in arg_types:
                    print 'mismatch on', alignment.p_token, alignment.h_token
                    if alignment.lexical_entailment in [0, 1, 2]:
                        print 'previously was match'
                        alignment.lexical_entailment = 4
                        print 'now set to', alignment.lexical_entailment

        return alignments