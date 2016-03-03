#!/usr/bin/env python
# encoding: utf-8

import web
import threading
import time

urls = (
    '/', 'index'
)
render = web.template.render('templates/', cache=False)
app = web.application(urls, globals())

class MyWebServer(threading.Thread):
    def run(self):
        app.run()

class index:
    def GET(self):
        return render.index()

if __name__ == '__main__':
    t = MyWebServer()
    t.daemon = True
    t.start()
    while True:
        time.sleep(100)
