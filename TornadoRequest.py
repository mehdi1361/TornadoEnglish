__author__ = 'mehdi'
import datetime
import logging
import memcache
import sys, time
from users import *
from tornado import websocket, web, ioloop

class Caching(object):
    def __init__(self, hostname="127.0.0.1", port="11211"):
        self.hostname = "%s:%s" % (hostname, port)
        self.server = memcache.Client([self.hostname])

    def set(self, key, value, expiry=900):
        self.server.set(key, value, expiry)

    def get(self, key):
        return self.server.get(key)

    def delete(self, key):
        self.server.delete(key)

class IndexHandler(web.RequestHandler):
    ''' index http normal handler'''
    def get(self):
        # self.render("index.html")
        print "service worked"

class SignUpHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'email': self.get_argument("email"),
            'username': self.get_argument("username"),
            'password': self.get_argument("password"),
        }
        # logging.debug('This message should go to the log file')
        # sys.stdout.write(str(time.time() - aaa)+"\n")
        # sys.stdout.write(self.request.remote_ip)
        # sys.stdout.write(" [%s] " % datetime.datetime.now())
        # sys.stdout.write(self.request.uri)
        self.finish()

    def on_finish(self):
        # checkcache = Caching()
        # s = checkcache.get(str(self._data['email']))
        # if s is None:
        #     checkcache.set(str(self._data['email']), self._data['username'])
            print 'on finish'
            sign_up(**self._data)

class SignInHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'email': self.get_argument("email"),
            'password': self.get_argument("password"),
        }
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.finish()

    def on_finish(self):
        checkcache = Caching()
        s = checkcache.get(str(self._data['email']))
        if s is None:
            checkcache.set(str(self._data['email']), self._data['username'])
            s = sign_in.delay(**self._data)
        return s
app = web.Application([
    (r'/', IndexHandler),
    (r'/sign_up', SignUpHandler),
    (r'/sign_in', SignUpHandler),
])

if __name__ == '__main__':
    app.listen(2051)
    ioloop.IOLoop.instance().start()
