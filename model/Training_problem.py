# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 11:25:40 2012

@author: gavin
"""


class Training_problem:

    def __init__(self, p_str_tokens, h_str_tokens, gold):
        self.p_str_tokens = p_str_tokens
        self.h_str_tokens = h_str_tokens
        self.gold = gold

    def __str__(self):
        return 'P: %s\nH: %s\nGold: %s\n' % (
            self.p_str_tokens, self.h_str_tokens, self.gold)

