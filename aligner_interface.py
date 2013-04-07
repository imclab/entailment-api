# -*- coding: utf-8 -*-

'''

'''
from urllib import urlopen
from urllib import urlencode
from json import load

class Aligner_interface(object):

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000/align/string?'

    def align(self, p_str_tokens, h_str_tokens, weights):
        parameters = {
        "p": p_str_tokens,
        "h": h_str_tokens,
        "w": weights
        }
        query_string = urlencode(parameters)
        results = load(urlopen(self.base_url + query_string))
        return results['alignments'], results['averaged_features']

if __name__ =='__main__':
    aligner = Aligner_interface()
    alignments, averaged_features = aligner.align(
        'I ate a pizza.',
        'I ate food.',
        'default'
    )