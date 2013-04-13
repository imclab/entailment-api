# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 23:11:02 2012

@author: gavin

Edits should be sequenced as follows:
DEL
SUB
DEL N/D
SUB N/D
INS N/D
INS
"""
from os.path import join, dirname
import senna_interface


class Sequencer(object):

    def __init__(self):
        self.mon_operators = []
        monotonicity_operators_file = join(dirname(__file__),
            '../resources/monotonicity_operators_list.txt')
        with open(monotonicity_operators_file) as f:
            self.mon_operators = f.read().splitlines()
        self.senna = senna_interface.Senna_interface()

    def need_to_use_arg_types(self, p, h, edit):
        '''
        Return true if the argument types of the roles tokens are constituents
        of need to be considered.

        These argument types should be considered when both sentences have
        predicates with similar, transitive verbs
        '''
        if edit.p_wn_tag == edit.h_wn_tag == 'v':
            if edit.lexical_entailment in [0, 1, 2]:
                p_transitive = self.senna.is_transitive(edit.p_token, p)
                h_transitive = self.senna.is_transitive(edit.h_token, h)
                if p_transitive and h_transitive:
                    print 'p and h share a similar transitive verb ' + \
                    'therefore arg types must be considered'
                    return True
        return False

    def sequence(self, p, h, edits, p_marked_tokens, h_marked_tokens):
        '''
        Return the sequenced edit list and a flag to use argument type features
        '''
        using_arg_types = False
        upward_dels = []
        upward_subs = []
        upward_ins = []
        downward_dels = []
        downward_subs = []
        downward_ins = []
        matched_predicate = None

        for edit in edits:

            if edit.edit_type == 'DEL':
                if edit.p_token is 'INS':
                    continue
                edit.monotonicity = p_marked_tokens[edit.p_token]
                if edit.p_token in self.mon_operators:
                    downward_dels.append(edit)
                else:
                    upward_dels.append(edit)

            elif edit.edit_type == 'SUB' or edit.edit_type == 'EQ':
                if not using_arg_types:
                    using_arg_types = self.need_to_use_arg_types(p, h, edit)
                    if using_arg_types:
                        matched_predicate = edit
                '''
                If h pos and p pos are v and lexent == 0/1/2
                    if the verbs in this pair both have a0 and a1+
                        get shallow parse
                            for each edit, get arg type at edit index
                        set flag to
                        activate argtype features
                        set sub/eq 0/1/2 to 4 if arg types mismatched a0/a1+
                '''
                # TODO determine if SUB and SUB N/D need to
                # take monotonicity markings from p or h
                if edit.p_token in self.mon_operators or \
                edit.h_token in self.mon_operators:
                    edit.monotonicity = p_marked_tokens[edit.p_token]
                    downward_subs.append(edit)
                else:
                    edit.monotonicity = p_marked_tokens[edit.p_token]
                    upward_subs.append(edit)

            elif edit.edit_type == 'INS':
                if edit.h_token is 'DEL':
                    continue
                edit.monotonicity = h_marked_tokens[edit.h_token]
                if edit.h_token in self.mon_operators:
                    downward_ins.append(edit)
                else:
                    upward_ins.append(edit)

        return upward_dels + \
                upward_subs + \
                downward_dels + \
                downward_subs + \
                downward_ins + \
                upward_ins, \
                using_arg_types, \
                matched_predicate





