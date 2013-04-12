# -*- coding: utf-8 -*-
"""

   python marriage.py  [menfile]  [womenfile]  V

for verbose mode.
"""
import sys


class Person:
    def __init__(self, name, priorities):
        self.name = name
        self.priorities = priorities
        self.partner = None


class Man(Person):
    """
    Represents a man
    """
    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)
        self.proposalIndex = 0

    def nextProposal(self):
        goal = self.priorities[self.proposalIndex]
        self.proposalIndex += 1
        return goal


class Woman(Person):
    """
    Represents a woman
    """
    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)

        # now compute a reverse lookup for efficient candidate rating
        self.ranking = {}
        for rank in range(len(priorities)):
            self.ranking[priorities[rank]] = rank

    def evaluateProposal(self, suitor):
        """
        Evaluates a proposal, though does not enact it.

        suitor is the string identifier for the man who is proposing

        returns True if proposal should be accepted, False otherwise
        """
        return self.partner == None or self.ranking[suitor] < self.ranking[self.partner]


def parseFile(filename):
    """
    Returns a list of (name,priority) pairs.
    """
    people = []
    f = file(filename)
    for line in f:
        pieces = line.split(':')
        name = pieces[0].strip()
        if name:
            priorities = pieces[1].strip().split(',')
            for i in range(len(priorities)):
                priorities[i] = priorities[i].strip()
            people.append((name, priorities))
    f.close()
    return people


def printPairings(men):
    for man in men.values():
        print man.name, 'is paired with', str(man.partner)


def get_marriages(p_preferences, h_preferences):
    '''
    Keyword arguments:
    p_preferences     -- a list of tuples. tuple[i][0] is a token from p.
        tuple[i][1] is an ordered list of h tokens to align with the p token.
    h_preferences     -- a list of tuples. tuple[i][0] is a token from h.
        tuple[i][1] is an ordered list of p tokens to align with the h token.
    Currently, the token's index is appended to the token in tuple[i][0].
    ('Park_8', ['park_20', 'highland_19', ..., 'DEL_0']),
    ('INS_3', ['the_18', 'park_20', ..., 'DEL_1', 'DEL_0', '._24']),
    '''
    alignments = []

    # initialize dictionary of p
    p = dict()
    for p_preference in p_preferences:
        p[p_preference[0]] = Man(p_preference[0], p_preference[1])
    unaligned_p = p.keys()

    # initialize dictionary of h
    h = dict()
    for h_preference in h_preferences:
        h[h_preference[0]] = Woman(h_preference[0], h_preference[1])

    while unaligned_p:
        #print women.keys()
        m = p[unaligned_p[0]]             # pick arbitrary unwed man
        w = h[m.nextProposal()]      # identify highest-rank woman to which
                                         #    m has not yet proposed
        if w.evaluateProposal(m.name):
            if w.partner:
                # previous partner is getting dumped
                mOld = p[w.partner]
                mOld.partner = None
                unaligned_p.append(mOld.name)

            unaligned_p.remove(m.name)
            w.partner = m.name
            m.partner = w.name

    for p_token in p.values():
        alignments.append([p_token.name, p_token.partner])

    return alignments


if __name__ == "__main__":
    verbose = len(sys.argv) > 3

    # initialize dictionary of men
    menlist = parseFile(sys.argv[1])
    print 'menlist:\n', menlist

    men = dict()
    for person in menlist:
        men[person[0]] = Man(person[0], person[1])
    unwedMen = men.keys()

    # initialize dictionary of women
    womenlist = parseFile(sys.argv[2])
    print 'womenlist:\n', womenlist

    women = dict()
    for person in womenlist:
        women[person[0]] = Woman(person[0], person[1])

    ############################### the real algorithm ###################
    while unwedMen:
        m = men[unwedMen[0]]             # pick arbitrary unwed man
        w = women[m.nextProposal()]      # identify highest-rank woman to which
                                         #    m has not yet proposed

        if w.evaluateProposal(m.name):
            if w.partner:
                # previous partner is getting dumped
                mOld = men[w.partner]
                mOld.partner = None
                unwedMen.append(mOld.name)

            unwedMen.remove(m.name)
            w.partner = m.name
            m.partner = w.name

        if verbose:
            print "Tentative Pairings are as follows:"
            printPairings(men)
            print
