# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:25:40 2012

@author: gavin
"""


class Del:

    def __init__(self, p_token):
        self.edit_type = 'DEL'
        self.p_token = p_token
        self.lexical_entailment = 'NONE'
        self.monotonicity = 'NONE'

    def __repr__(self):
        return 'Type %s\np: %s\nMonotonicity: %s\nLexent: %s\n' % \
        (self.edit_type,
        self.p_token.encode('utf-8', 'ignore'),
        self.monotonicity,
        self.lexical_entailment)

