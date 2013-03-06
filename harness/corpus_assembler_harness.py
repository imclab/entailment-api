# -*- coding: utf-8 -*-
import os


path = '/home/gavin/dev/Factoid-Question-Answering/corpora/data/coarse'
questions = []

for dirname, dirnames, filenames in os.walk(path):
    #for subdirname in dirnames:
        #print os.path.join(dirname, subdirname)

    for filename in filenames:
        print os.path.join(dirname, filename)

        question_file = os.path.join(dirname, filename)
        with open(question_file) as f:
            questions.append(f.read())

questions_list_file = open('/home/gavin/dev/Factoid-Question-Answering/corpora/data/coarse/out.txt', 'w')
for item in questions:
    questions_list_file.write("%s\n" % item)