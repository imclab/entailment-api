# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:11:02 2012

@author: gavin

"""
#import os
from os.path import dirname, realpath
import subprocess


def get_monotonicity_markings(tokens):
    path = dirname(realpath(__file__)) + '/MonotonicityMarker.jar'
    jar_call = ['java', '-jar', path, '-q']
    for token in tokens:
        jar_call.append(token.encode('utf-8', 'ignore'))
    print 'Calling MonotonicityMarker.jar:\n', jar_call
    monotonicity_markings_out = subprocess.check_output(jar_call).rstrip('\n')
    return monotonicity_markings_out.split('\n')[1:]

if __name__ == '__main__':
    print get_monotonicity_markings(['he', 'did', 'not', 'eat'])