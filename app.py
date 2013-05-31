# -*- coding: utf-8 -*-
"""


"""
import os
import tornado.web
import tornado.ioloop
from tornado.options import define, options
import json
from nltk import word_tokenize
from pipeline import pipeline
from alignment import aligner


class PitchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ShortPitchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index_short.html')


class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('demo.html')


class EntailmentHandler(tornado.web.RequestHandler):
    def get(self):
        entailment = ['yes', 'yes', 'unknown', 'no', 'no', 'no', 'no']
        p = self.get_argument("p", strip=True)
        h = self.get_argument("h", strip=True)
        p_str_tokens = word_tokenize(p)
        h_str_tokens = word_tokenize(h)
        p_str_tokens = [unicode(t) for t in p_str_tokens]
        h_str_tokens = [unicode(t) for t in h_str_tokens]

        alignments, score = aligner.align(
            p_str_tokens, h_str_tokens, 'default')
        sequenced_edits, entailment_code = pipeline.get_entailment(
            p, h, p_str_tokens, h_str_tokens, alignments)

        response = {
            'p': p,
            'h': h,
            'entailment_code': str(entailment_code),
            'entailment': entailment[entailment_code]
            }
        d = json.dumps(response, sort_keys=True, indent=4)
        self.write(d)


handlers = [
            (r"/v1/entailment", EntailmentHandler),
            (r"/pitch", PitchHandler),
            (r"/short_pitch", ShortPitchHandler),
            (r"/demo", DemoHandler),
            ]


settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8001, help="run on the given port", type=int)

if __name__ == "__main__":
    aligner = aligner.Aligner()
    pipeline = pipeline.Pipeline()
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()