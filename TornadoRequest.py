__author__ = 'mehdi'
import datetime
import logging
import memcache
import sys, time
from tasks import *
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
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        try:
            sign_up(**self._data)
            self.write('200')
        except ValueError:
            self.write('500')
        self.finish()

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
        self.write(sign_in(**self._data))
        self.finish()

class get_level(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.write(db_get_level())
        self.finish()

class set_level(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'level_title': self.get_argument("title"),
            'level_description': self.get_argument("description"),
        }
        print self._data
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        try:
            print 'set level'
            db_set_level(**self._data)
            self.write('200')
        except ValueError:
            self.write('500')
        self.finish()

class set_lesson(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'lesson_title': self.get_argument("title"),
            'lesson_description': self.get_argument("description"),
            'level_level_id': self.get_argument("level"),
        }
        logging.debug('This set_lesson should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        try:
            db_set_lesson(**self._data)
            self.write('200')
        except ValueError:
            self.write('500')
        self.finish()

class get_lesson(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'level_level_id': self.get_argument("level"),
        }
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.write(db_get_lesson(**self._data))
        self.finish()

class get_questions(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'lesson_lesson_id': self.get_argument("lesson"),
        }
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.write(db_get_questions(**self._data))
        self.finish()

class get_question(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        aaa = time.time()
        self._data = {
            'question_id': self.get_argument("level"),
        }
        logging.debug('This message should go to the log file')
        sys.stdout.write(str(time.time() - aaa)+"\n")
        sys.stdout.write(self.request.remote_ip)
        sys.stdout.write(" [%s] " % datetime.datetime.now())
        sys.stdout.write(self.request.uri)
        self.write(db_get_questions(**self._data))
        self.finish()

app = web.Application([
    (r'/', IndexHandler),
    (r'/sign_up', SignUpHandler),
    (r'/sign_in', SignInHandler),
    (r'/get_level', get_level),
    (r'/set_level', set_level),
    (r'/set_lesson', set_lesson),
    (r'/get_questions', get_questions),
])

if __name__ == '__main__':
    app.listen(2051)
    ioloop.IOLoop.instance().start()
