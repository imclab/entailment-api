# -*- coding: utf-8 -*-
'''
TODO
-Need to support many-to-one alignments?
'''
import re
import numpy as np
from nltk import word_tokenize, pos_tag, WordNetLemmatizer
from nltk.corpus import wordnet as wn
import Edit_featurizer
from model import Alignment_eq as Eq
from model import Alignment_sub as Sub
from model import Alignment_del as Del
from model import Alignment_ins as Ins
from model import Token
import Stable_marriage_finder


class Aligner(object):

    def __init__(self):
        self.weights = [
        3.48961282e-01,
        3.75654800e-01,
        4.12711607e-01,
        -7.24616082e-01,
        3.77362029e-02,
        1.15394180e-02,
        1.33443409e-02,
        1.64232249e-02,
        -3.36975735e-02,
        -5.02300279e-03,
        -3.17276960e-02,
        -2.94709012e-02,
        1.09211720e-03,
        -1.68436954e-02,
        7.09680460e-03,
        1.01815575e-03,
        -2.07404857e-02,
        -3.86330862e-02,
        1.66864534e-06,
        9.97633950e-04,
        7.88702336e-04,
        -1.04303582e-02,
        6.93624232e-02,
        7.89814727e-03
        ]
        self.lemmatizer = WordNetLemmatizer()

    def get_tokens(self, tagged_tokens):
        tagConversionDict = {
            'NN': wn.NOUN, 'JJ': wn.ADJ, 'VB': wn.VERB, 'RB': wn.ADV}
        tokens = []
        for index, tagged_token in enumerate(tagged_tokens):
            token = Token.Token(tagged_token[0], index, tagged_token[1])
            if token.penn_tag[:2] in tagConversionDict:
                token.wn_tag = tagConversionDict[token.penn_tag[:2]]
                token.lemma = self.lemmatizer.lemmatize(
                    token.token, token.wn_tag)
            tokens.append(token)
        return tokens

    def align(self, p_str_tokens, h_str_tokens, weights):
        if weights == 'default':
            weights = self.weights

        alignments_score = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        all_alignments = dict()
        predicted_alignments = []
        all_features = dict()

        # Add INS and DEL tokens so that len(p) == len(h)
        p_start = []
        for index, token in enumerate(h_str_tokens):
            p_start.append((u'INS', u'SKIP'))
        h_start = []
        for index, token in enumerate(p_str_tokens):
            h_start.append((u'DEL', u'SKIP'))

        p_tagged_tokens = pos_tag(p_str_tokens) + p_start
        h_tagged_tokens = pos_tag(h_str_tokens) + h_start
        p_tokens = self.get_tokens(p_tagged_tokens)
        h_tokens = self.get_tokens(h_tagged_tokens)

        # For each p token, order the set of h tokens from most to least
        # preferable alignment.
        all_p_prefs = []
        for p_index, p_token in enumerate(p_tokens):
            # An unordered list of tuples.
            # tuple[i][0] = alignment score
            # tuple[i][1] = h token
            scored_alignments_to_h = []
            # Create the appropriate Alignment for the current p and h tokens.
            for h_index, h_token in enumerate(h_tokens):
                if p_token.token == u'INS':
                    alignment = Ins.Ins(h_token.token)
                elif h_token.token == u'DEL':
                    alignment = Del.Del(p_token.token)
                elif h_token.lemma == p_token.lemma:
                    alignment = Eq.Eq(
                        p_token.token, p_token.lemma,
                        p_token.penn_tag, p_token.index,
                        h_token.token, h_token.lemma,
                        h_token.penn_tag, h_token.index)
                else:
                    alignment = Sub.Sub(
                        p_token.token, p_token.lemma,
                        p_token.penn_tag, p_token.index,
                        h_token.token, h_token.lemma,
                        h_token.penn_tag, h_token.index)
                # Store the Alignment in all_alignments using
                # p_lemma + p_index + h_lemma + h_index as the key
                all_alignments[
                    p_token.lemma + u'_' + unicode(p_token.index) +
                    h_token.lemma + u'_' + unicode(h_token.index)] = alignment
                # Score the alignment
                features = Edit_featurizer.featurize(
                    alignment, p_str_tokens, h_str_tokens,
                    len(p_str_tokens), len(h_str_tokens))
                alignment_score = np.dot(features, weights)

                scored_alignments_to_h.append([alignment_score,
                h_token.lemma + u'_' + unicode(h_token.index)])
                all_features[
                    p_token.lemma + u'_' + unicode(p_index) +
                    h_token.lemma + u'_' + unicode(h_index)] = features
            all_p_prefs.append(
                [p_token.lemma + u'_' + unicode(p_token.index),
                sorted(scored_alignments_to_h, reverse=True)])

        # Format the preference list for use with the marriage finder.
        p_preferences_smf = []
        for i in all_p_prefs:
            p_preferences_smf.append((i[0], [j[1] for j in i[1]]))

        # for each h token, order the set of p tokens from most to least
        # preferable alignment.
        all_h_prefs = []
        for h_index, h_token in enumerate(h_tokens):
            scored_alignments_to_p = []
            for p_index, p_token in enumerate(p_tokens):
                if p_token.token == u'INS':
                    alignment = Ins.Ins(h_token.token)
                elif h_token.token == u'DEL':
                    alignment = Del.Del(p_token.token)
                elif h_token.lemma == p_token.lemma:
                    alignment = Eq.Eq(
                        p_token.token, p_token.lemma,
                        p_token.penn_tag, p_token.index,
                        h_token.token, h_token.lemma,
                        h_token.penn_tag, h_token.index)
                else:
                    alignment = Sub.Sub(
                        p_token.token, p_token.lemma,
                        p_token.penn_tag, p_token.index,
                        h_token.token, h_token.lemma,
                        h_token.penn_tag, h_token.index)

                #print 'Alignment:\n', alignment

                features = Edit_featurizer.featurize(alignment,
                    p_str_tokens, h_str_tokens,
                    len(p_str_tokens), len(h_str_tokens))
                all_alignments[
                    h_token.lemma + u'_' + unicode(h_token.index) +
                    p_token.lemma + u'_' + unicode(p_token.index)] = alignment

                alignment_score = np.dot(features, weights)
                scored_alignments_to_p.append((alignment_score,
                    p_token.lemma + u'_' + unicode(p_token.index)))
                all_features[
                    h_token.lemma + u'_' + unicode(h_index) +
                    p_token.lemma + u'_' + unicode(p_index)] = features
            all_h_prefs.append((h_token.lemma + u'_' + unicode(h_token.index),
                sorted(scored_alignments_to_p, reverse=True)))
        # Format the preference list for use with the marriage finder.
        h_preferences_smf = []

        for i in all_h_prefs:
            h_preferences_smf.append((i[0], [j[1] for j in i[1]]))

        alignment_preferences = Stable_marriage_finder.get_marriages(
            p_preferences_smf, h_preferences_smf)

        # TODO get alignment score
        # is this the sum of all alignment scores

        # Append the alignment if it is not a DEL-INS SUB or EQ
        stop_types = [u'DEL', u'INS']
        for alignment in alignment_preferences:
            if re.sub(r"_.+", '', alignment[0]) not in stop_types \
            or re.sub(r"_.+", '', alignment[1]) not in stop_types:
                predicted_alignments.append(
                    all_alignments[alignment[0] + alignment[1]])


        summed_weights = 0
        for alignment in predicted_alignments:
            alignment_score = Edit_featurizer.featurize(alignment,
                p_str_tokens, h_str_tokens,
                len(p_str_tokens), len(h_str_tokens))
            alignments_score += alignment_score
            weight = np.dot(alignment_score, self.weights)
            summed_weights += weight
            print alignment
            print 'features', alignment_score
            print 'weight', weight, '\n\n'

        print 'average weight', summed_weights / len(predicted_alignments)
        #print np.dot(alignments_score, self.weights)
        return predicted_alignments, alignments_score


if __name__ == '__main__':
    #p = "An man won the Nobel Prize."
    #h = "An Irishman won the Nobel Prize for literature."
    p = "Barack Obama was the president"
    h = "Barack Obama"
    #h = "fat"
    aligner = Aligner()
    p_str_tokens = word_tokenize(p)
    h_str_tokens = word_tokenize(h)
    alignments, alignments_score = aligner.align(
        p_str_tokens, h_str_tokens, 'default')

    #print alignments_score, '\n'
    #for alignment in alignments:
        #print alignment

