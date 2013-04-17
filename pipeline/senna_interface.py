# -*- coding: utf-8 -*-
"""
Created on 20130325

@author: gavinhackeling@gmail.com

/senna-linux64 -posvbs <<< 'I ate a cake.'

"""
from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), '../'))
from subprocess import Popen, PIPE, STDOUT
from model import semantic_role as sr


class Senna_interface(object):

    def __init__(self):
        self.senna_path = join(dirname(__file__), '../../senna')

    def is_transitive(self, predicate, text):
        arg_list = self.get_arg_types_for_predicate(predicate, text)
        arg_types = [a[-2:] for a in arg_list]
        if 'A0' in arg_types and 'A1' in arg_types:
            return True
        return False

    def get_parse(self, text_str):
        print self.senna_path
        print self.senna_path + '/senna2'
        pipe = Popen([
            self.senna_path + '/senna2',
            '-posvbs'],
            cwd=self.senna_path,
            stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        out = pipe.communicate(input='%s' % text_str.encode('utf-8', 'ignore'))[0]
        return out

    def get_predicate_index(self, roles):
        for index, role in enumerate(roles):
            if role != 'O' and role[2] == 'V':
                return index
        return -1

    def get_arg_types_for_predicate(self, predicate, text):
        predicates_and_arg_lists = self.get_arg_types_for_all_predicates(text)
        arg_list = []
        try:
            arg_list = predicates_and_arg_lists[predicate]
        except:
            print 'SENNA did not identify %s as a predicate' % \
            predicate.encode('utf-8', 'ignore')
        return arg_list

    def get_arg_types_for_all_predicates(self, text_str):
        out = self.get_parse(text_str)
        out_lines = out.split('\n')
        out_lines = [l for l in out_lines if 1 != '\n']
        out_lines = [l for l in out_lines if not l.startswith('WARNING')]
        print 'out\n', out_lines
        unparsed_role_labels = out_lines[5:]
        tokens = out_lines[0].split('\t')[1:]
        semantic_role_labels = {}
        print 'unparsed role lables\n', unparsed_role_labels
        for parse in unparsed_role_labels:
            print 'parse', parse
            roles = parse.split('\t')[1:]
            print 'roles', roles
            print 'toknes', tokens
            predicate = tokens[self.get_predicate_index(roles)]
            semantic_role_labels[predicate] = roles
        return semantic_role_labels

    def get_semantic_roles(self, text_str):
        out = self.get_parse(text_str)
        out_lines = out.split('\n')
        out_lines = [l for l in out_lines if 1 != '\n']
        unparsed_role_labels = out_lines[5:]

        tokens = out_lines[0].split('\t')[1:]
        pos_tags = out_lines[1].split('\t')[1:]
        chunk_tags = out_lines[2].split('\t')[1:]
        ne_labels = out_lines[3].split('\t')[1:]
        #semantic_role_labels = out_lines[5].split('\t')[1:]
        semantic_role_labels = []
        for parse in unparsed_role_labels:
            roles = parse.split('\t')[1:]
            predicate_index = self.get_predicate_index(roles)
            predicate = tokens[predicate_index]
            semantic_role_labels.append((predicate, roles))
            print 'the predicate for this parse is', predicate
            print 'the roles are', roles

        #is_symmetric = self.is_symmetric(semantic_role_labels)
        argument_types = []
        for label in semantic_role_labels:
            if label == 'O':
                argument_types.append(label)
            else:
                argument_types.append(label[2:])

        semantic_roles = []
        token_start_index = 0
        token_end_index = 0
        for i, label in enumerate(semantic_role_labels):
            if label[0] == 'S':
                phrase_indices = []
                role = sr.Semantic_role(
                    [tokens[i]],
                    [token_start_index],
                    pos_tags[i],
                    chunk_tags[i],
                    ne_labels[i],
                    [argument_types[i]]
                )
                token_start_index += 1
                semantic_roles.append(role)
            elif label[0] == 'B':
                phrase_indices = [i]
            #elif label[0] == 'I':
                #token_start_index += 1
                #print '1'
            elif label[0] == 'E':
                phrase_indices.append(i + 1)
                token_end_index = token_start_index + len(
                    tokens[phrase_indices[0]:phrase_indices[1]])
                role = sr.Semantic_role(
                    tokens[phrase_indices[0]:phrase_indices[1]],
                    range(token_start_index, token_end_index),
                    pos_tags[phrase_indices[0]:phrase_indices[1]],
                    chunk_tags[phrase_indices[0]:phrase_indices[1]],
                    ne_labels[phrase_indices[0]:phrase_indices[1]],
                    argument_types[phrase_indices[0]:phrase_indices[1]]
                )
                token_start_index = token_end_index
                semantic_roles.append(role)
            elif label[0] == 'O':
                phrase_indices = []
                semantic_roles.append(sr.Semantic_role(
                    [tokens[i]],
                    [token_start_index],
                    pos_tags[i],
                    chunk_tags[i],
                    ne_labels[i],
                    [argument_types[i]]
                ))
                token_start_index += 1

        return semantic_roles


if __name__ == '__main__':
    si = Senna_interface()
    t = 'Pope Francis will continue to use the papal library on the second floor.'
    #roles = si.get_semantic_roles(t)
    #roles = si.get_arg_types_for_all_predicates(t)
    #print si.get_parse(t)
    #for i in roles:
        #print i, '\n'
    #print si.is_transitive('use', t)
    #print si.is_transitive('continue', t)
    t = 'Carolina beat Duke'
    print si.is_transitive('beat', t)
    t = 'George is tall.'
    print si.is_transitive('is', t)
    t = 'I jumped over the hill'
    print si.is_transitive('jumped', t)