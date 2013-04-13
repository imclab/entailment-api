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
        self.HOST = '127.0.0.1'
        self.PORT = 8020
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect((self.HOST, self.PORT))

    def mark(self, sentence):
        '''
        Send a sentence to the socket and return the monotonicity markings
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))
        print 'Sending', sentence
        sock.sendall(sentence + '\n')
        print 'Getting response'
        response = sock.recv(4096)
        # Get a newline that is sent for some reason
        #print 'other thing', sock.recv(4096)
        #print response, type(response)
        response = response[1:-1].split(', ')
        #print response, type(response)
        sock.close()
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