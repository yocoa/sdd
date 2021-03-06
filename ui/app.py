#!/usr/bin/env python
# encoding: utf-8

import web
import threading
import time
import json

import sys
sys.path.append('../services')
import Service

DEBUG = False

urls = (
    '/', 'index',
    '/bgp', 'bgp',
    '/visual', 'visual',
    '/feature', 'feature',
    '/relation', 'relation',
)
render = web.template.render('templates/', cache=False)
app = web.application(urls, globals())

class MyWebServer(threading.Thread):
    def run(self):
        app.run()
        print 'Served!'

'''
View
'''
class index:
    def GET(self):
        return render.index()

'''
Ajax
'''
class bgp:
    def GET(self):
        data = web.input(query=None)
        result = {}
        cleand_q = '.'.join(data.query.lower().split('.')[-2:])
        if cleand_q:
            if DEBUG:
                #time.sleep(3)
                result = Service.BA.run_test(cleand_q)
                result['site'] = 'http://www.' + result['url']
            else:
                result = Service.BA.run(cleand_q)
        return json.dumps(result)

class visual:
    def GET(self):
        data = web.input(query=None)
        result = {}
        if data.query.lower():
            if DEBUG:
                #time.sleep(3)
                result = Service.VA.run_test(data.query.lower())
            else:
                result = Service.VA.run(data.query.lower())
        return json.dumps(result)

class feature:
    def GET(self):
        data = web.input(query=None)
        result = {}
        cleand_q = '.'.join(data.query.lower().split('.')[-2:])
        if cleand_q:
            if DEBUG:
                #time.sleep(3)
                result = Service.MA.run_test(cleand_q)
            else:
                result = Service.MA.run(cleand_q)
        return json.dumps(result)

class relation:
    def GET(self):
        data = web.input(query=None)
        if data.query.lower():
            if DEBUG:
                #time.sleep(3)
                result, mapper = Service.AA.run_test(data.query.lower())
                q = data.query.lower()
                tmp = sorted(result.iteritems(), key=lambda i:i[1])
                relations = []
                for name, weight in tmp:
                    if name in mapper:
                        relations.append([name, list(mapper[name]), weight])
                    if len(relations) >= 5000:
                        break

                new_q = q.split('.')[-2]
                new_result = [result[new_q] if new_q in result else '', relations]
                return json.dumps(new_result)
            else:
                result, mapper = Service.AA.run(data.query.lower())
                q = data.query.lower()
                tmp = sorted(result.iteritems(), key=lambda i:i[1])
                relations = []
                for name, weight in tmp:
                    if name in mapper:
                        relations.append([name, list(mapper[name]), weight])
                    if len(relations) >= 5000:
                        break

                new_q = q.split('.')[-2]
                new_result = [result[new_q] if new_q in result else '', relations]
                return json.dumps(new_result)

if __name__ == '__main__':
    t = MyWebServer()
    t.daemon = True
    t.start()
    while True:
        time.sleep(10)
