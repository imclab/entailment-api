# -*- coding: utf-8 -*-
'''

'''
import socket
from time import time


class Marker_interface(object):

    def __init__(self):
        '''
        Connect to the socket
        '''
        HOST = 'localhost'
        PORT = 8020
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def mark(self, sentence):
        '''
        Send a sentence to the socket and return the monotonicity markings
        '''
        print 'Sending'
        self.sock.sendall(sentence + '\n')
        print 'Getting response'
        response = self.sock.recv(4096)
        # Get a newline that is sent for some reason
        self.sock.recv(4096)
        #print response, type(response)
        response = response[1:-1].split(', ')
        #print response, type(response)
        return response

if __name__ == '__main__':
    interface = Marker_interface()
    start = time()
    print interface.mark(
        "An Irishman did not win the Nobel Prize for Literature .")
    print 'first', time() - start

    start2 = time()
    print interface.mark(
        "An man won .")
    print 'second', time() - start2

    start3 = time()
    print interface.mark(
        "An man won the Nobel Prize for Literature and had some bacon .")
    print 'third', time() - start3

    start4 = time()
    print interface.mark(
        "An man won .")
    print 'fourth', time() - start4