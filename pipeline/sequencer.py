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


class Sequencer(object):

    def __init__(self):
        self.mon_operators = []
        monotonicity_operators_file = join(dirname(__file__),
                'resources/monotonicity_operators_list.txt')
        with open(monotonicity_operators_file) as f:
            self.mon_operators = f.read().splitlines()

    def sequence(self, edits, p_marked_tokens, h_marked_tokens):
        upward_dels = []
        upward_subs = []
        upward_ins = []
        downward_dels = []
        downward_subs = []
        downward_ins = []

        for edit in edits:
            if edit.edit_type == 'DEL':
                if edit.p_token is 'INS':
                    continue
                edit.monotonicity = p_marked_tokens[edit.p_token]
                if edit.p_token in self.mon_operators:
                    downward_dels.append(edit)
                else:
                    upward_dels.append(edit)
            elif edit.edit_type == 'SUB':
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

        return upward_dels + upward_subs + downward_dels + downward_subs \
                    + downward_ins + upward_ins





