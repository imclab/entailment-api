# -*- coding: utf-8 -*-
"""
Created on 20130325

@author: gavin

A collection of tagged (Penn POS, WN POS, chunk, and NE) tokens that comprise
an arugment or predicate.
"""
from nltk.corpus import wordnet as wn


class Semantic_role(object):

    def __init__(
        self, tokens, token_indices, penn_tags, chunk_tags, ne_labels,
        full_arg_type):

        self.tag_conversion_dict = {
            'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV
        }
        self.tokens = tokens
        self.token_indices = token_indices
        self.penn_tags = penn_tags
        self.wn_tags = self.get_wn_tags(self.penn_tags)
        self.chunk_tags = chunk_tags
        self.ne_labels = ne_labels
        self.full_arg_type = full_arg_type
        self.monotonicities = []

    def get_arg_type(self):
        return self.full_arg_type[0][-2:]

    def get_wn_tags(self, penn_tags):
        wn_tags = []
        for penn_tag in penn_tags:
            if penn_tag[:2] in self.tag_conversion_dict.keys():
                wn_tags.append(self.tag_conversion_dict[penn_tag[:2]])
            else:
                wn_tags.append('SKIP')
        return wn_tags

    def __hash__(self):
        return hash((self.tokens, self.token_indices))

    def __eq__(self, other):
        return (self.tokens, self.token_indices) == (other.tokens, other.token_indices)

    def __repr__(self):
        return ('''
tokens: %s
token indices: %s
pos_tags: %s
chunk tags: %s
ne labels: %s
full_arg_type: %s''' % (
        self.tokens,
        self.token_indices,
        self.penn_tags,
        self.chunk_tags,
        self.ne_labels,
        self.full_arg_type
        )).encode('utf-8', 'ignore')
