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
#import multiprocess_entailer


#class MultiEntailmentHandler(tornado.web.RequestHandler):
    #"""?p[]=premise 1&p[]=premise 2&p[]=premise 3&h=hypothesis"""

    #def get(self):
        ## Get the premises and hypothesis from arguments
        #premises = self.get_arguments("p[]", strip=True)
        #hypothesis = self.get_argument("h", strip=True)

        #premise, entailment_code, entailment = multiprocessor.entail(
            #premises, hypothesis)

        #response_dict = {
            #'p': premise,
            #'h': hypothesis,
            #'entailment_code': str(entailment_code),
            #'entailment': entailment_code
            #}
        #response = json.dumps(response_dict, sort_keys=True, indent=4)
        #self.write(response)

class PitchHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class DemoHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('demo.html')


class EntailmentHandler(tornado.web.RequestHandler):
    def get(self):
        entailment = ['yes', 'yes', 'unknown', 'no', 'no', 'no', 'no']
        p = self.get_argument("p", strip=True)
        h = self.get_argument("h", strip=True)
        print 'p', p.encode('utf-8', 'replace')
        print 'h', h.encode('utf-8', 'replace')
        p_str_tokens = word_tokenize(p)
        h_str_tokens = word_tokenize(h)
        p_str_tokens = [unicode(t) for t in p_str_tokens]
        h_str_tokens = [unicode(t) for t in h_str_tokens]
        print 'p', p
        print 'h', h

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

    def post(self):
        data_json = tornado.escape.json_decode(self.request.body)
        print data_json
        p = data_json['p']
        print 'p:', p
        h = data_json['h']
        print 'h:', h
        w = data_json['w']
        print 'w:', w

        entailment = ['yes', 'yes', 'unknown', 'no', 'no', 'no', 'no']
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
            (r"/e", EntailmentHandler),
            (r"/pitch", PitchHandler),
            (r"/demo", DemoHandler),
            #(r"/v1/entail", MultiEntailmentHandler)
            ]


settings = dict(template_path=os.path.join(
    os.path.dirname(__file__), "templates"))
application = tornado.web.Application(handlers, **settings)
define("port", default=8001, help="run on the given port", type=int)

if __name__ == "__main__":
    #multiprocessor = multiprocess_entailer.Multiprocess_entailer()
    aligner = aligner.Aligner()
    pipeline = pipeline.Pipeline()
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()