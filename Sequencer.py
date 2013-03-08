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
import os


def get_operators_list():
    monotonicity_operators_file = os.path.join(
            os.path.dirname(__file__),
            'resources/monotonicity_operators_list.txt')
    with open(monotonicity_operators_file) as f:
        monotonicty_operators = f.read().splitlines()
    for i in monotonicty_operators:
        print i
    monotonicty_operators = []
    #for line in lines:
        #if not line.startswith('#') \
        #and not line.startswith('\n') \
        #and len(line) > 0:
            #monotonicty_operators.append(line.split(',')[0])
    return monotonicty_operators


def sequence(edits, p_marked_tokens, h_marked_tokens):
    upward_dels = []
    upward_subs = []
    upward_ins = []
    downward_dels = []
    downward_subs = []
    downward_ins = []
    monotonicty_operators = get_operators_list()

    for edit in edits:
        if edit.edit_type == 'DEL':
            if edit.p_token is 'INS':
                continue
            edit.monotonicity = p_marked_tokens[edit.p_token]
            if edit.p_token in monotonicty_operators:
                downward_dels.append(edit)
            else:
                upward_dels.append(edit)
        elif edit.edit_type == 'SUB':
            # TODO determine if SUB and SUB N/D need to
            # take monotonicity markings from p or h
            if edit.p_token in monotonicty_operators or \
            edit.h_token in monotonicty_operators:
                edit.monotonicity = p_marked_tokens[edit.p_token]
                downward_subs.append(edit)
            else:
                edit.monotonicity = p_marked_tokens[edit.p_token]
                upward_subs.append(edit)
        elif edit.edit_type == 'INS':
            if edit.h_token is 'DEL':
                continue
            edit.monotonicity = h_marked_tokens[edit.h_token]
            if edit.h_token in monotonicty_operators:
                downward_ins.append(edit)
            else:
                upward_ins.append(edit)
        #elif edit.edit_type == 'EQ':
            ## TODO should down/non EQ take marking from p or h?
            #edit.monotonicity = p_marked_tokens[edit.p_token]
            #upward_subs.append(edit)

    return upward_dels + upward_subs + downward_dels + downward_subs \
                + downward_ins + upward_ins


if __name__ == '__main__':
    pass








