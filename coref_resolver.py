# -*- coding: utf-8 -*-
'''
I will also require coref for place names: eg. Atlanta == Atlanta, Georgia
'''
from itertools import chain
import re
import ner


class Coref_resolver:

    def __init__(self):
        self.tagger = ner.SocketNER(
            host='localhost', port=8008, output_format="slashTags")

    def is_safe_to_proceed_with(self, entities):
        '''
        It is only safe to proceed with this coref method if there is only one
        unique entity per entity type in the texts.
        Need to also check len of people
        '''
        if len(entities) == 0:
            return False
        if self.get_num_of_entity_type(entities) < 2:
            return True
        return False

    def get_num_of_entity_type(self, entities):
        '''
        Find the number of unique entities in the list.
        An entity is unique if it is not a substituend in any other entity.
        '''
        entities.sort(key=lambda s: len(s), reverse=True)
        unique_entities = []
        for entity in entities:
            add = True
            for unique_entity in unique_entities:
                if entity in unique_entity:
                    add = False
            if add:
                unique_entities.append(entity)
        return len(unique_entities)

    def get_canonical_name_and_aliases(self, person_entities):
        '''
        Should check that all aliases are substiuends in canonical name?
        '''
        person_entities.sort(key=lambda s: len(s), reverse=True)
        canonical_name = person_entities[0].replace(" ", "_")
        aliases = person_entities
        aliases.extend(['he', 'He', 'she', 'She'])
        return canonical_name, aliases

    def resolve_person_coreferences(self, p, h):
        entities = self.tagger.get_entities(p.encode('utf-8', 'replace'))
        people = [i[1] for i in entities.items() if i[0] == 'PERSON']
        entities = self.tagger.get_entities(h.encode('utf-8', 'replace'))
        people.extend([i[1] for i in entities.items() if i[0] == 'PERSON'])
        people = list(set(chain.from_iterable(people)))
        if self.is_safe_to_proceed_with(people):
            name, aliases = self.get_canonical_name_and_aliases(people)
            for alias in aliases:
                # TODO need to do safer replacement
                alias = unicode(alias)
                p = re.sub(r'\b%s\b' % alias, name, p)
                h = re.sub(r'\b%s\b' % alias, name, h)
            return p.replace('_', ' '), h.replace('_', ' ')
        else:
            print 'This coref is unsafe.'
            return p, h

    def get_entity_type(self, text):
        return self.tagger.get_entities(text.encode('utf-8', 'replace'))

    def test_names(self, text):
        entities = self.tagger.get_entities(text.encode('utf-8', 'replace'))
        for i in entities:
            print i

if __name__ == '__main__':
    coref = Coref_resolver()
    #print coref.resolve_person_coreferences(
        #"Michael Jordan Jr dunked. Jordan dunked it.",
        #"Jordan dunked. He dunked hard."
        #)
    coref.test_names("Carl")