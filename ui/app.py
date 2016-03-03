#!/usr/bin/env python
# encoding: utf-8

import web
import threading
import time
import json

import sys
sys.path.append('../services')
import Service

DEBUG = True

urls = (
    '/', 'index',
    '/visual', 'visual',
    '/feature', 'feature',
    '/relation', 'relation',
)
render = web.template.render('templates/', cache=False)
app = web.application(urls, globals())

class MyWebServer(threading.Thread):
    def run(self):
        app.run()

'''
View
'''
class index:
    def GET(self):
        return render.index()

'''
Ajax
'''
class visual:
    def GET(self):
        data = web.input(query=None)
        result = {}
        if data.query:
            if DEBUG:
                time.sleep(10)
                result = Service.VA.run_test(data.query)
            else:
                result = Service.VA.run(data.query)
        return json.dumps(result)

class feature:
    def GET(self):
        data = web.input(query=None)
        result = {}
        if data.query:
            if DEBUG:
                time.sleep(10)
                result = Service.MA.run_test(data.query)
            else:
                result = Service.MA.run(data.query)
        return json.dumps(result)

class relation:
    def GET(self):
        data = web.input(query=None)
        result = {}
        if data.query:
            if DEBUG:
                time.sleep(10)
                result = Service.AA.run_test(data.query)
            else:
                result = Service.AA.run(data.query)
        return json.dumps(result)

if __name__ == '__main__':
    t = MyWebServer()
    t.daemon = True
    t.start()
    while True:
        time.sleep(10)
