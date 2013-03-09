# -*- coding: utf-8 -*-
"""


"""
import os
import tornado.web
import tornado.ioloop
from tornado.options import define, options
import json
from nltk import word_tokenize
import Pipeline
import Aligner
from model import Response

class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('service minimally online')


class EntailmentHandler(tornado.web.RequestHandler):
    def get(self):
        entailment = ['yes', 'yes', 'unknown', 'no', 'no', 'no', 'no']
        p = self.get_argument("p", strip=True)
        h = self.get_argument("h", strip=True)
        p_str_tokens = word_tokenize(p)
        h_str_tokens = word_tokenize(h)
        print 'p', p.encode('utf-8', 'replace')
        print 'h', h.encode('utf-8', 'replace')

        alignments, score = aligner.align(
            p_str_tokens, h_str_tokens, 'default')
        sequenced_edits, entailment_code = Pipeline.get_entailment(
            p_str_tokens, h_str_tokens, alignments)

        response = {
            'p': p,
            'h': h,
            'entailment_code': str(entailment_code),
            'entailment': entailment[entailment_code]
            }
        d = json.dumps(response, sort_keys=True, indent=4)
        self.write(d)

handlers = [
            (r"/check", CheckHandler),
            (r"/e", EntailmentHandler),
            ]


settings = dict(template_path=os.path.join(
    os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8001, help="run on the given port", type=int)

if __name__ == "__main__":
    aligner = Aligner.Aligner()
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()