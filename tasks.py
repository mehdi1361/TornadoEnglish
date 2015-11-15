__author__ = 'mehdi'
from celery import Celery
import MySQLdb
import datetime
import collections
import json
app = Celery('tasks', broker='amqp://guest@localhost//')

# @app.task(trail=True)
def sign_up(email, username, password):
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "Learning_English")
    cursor = db.cursor()
    result = cursor.execute('''INSERT INTO users(email, username, password) VALUES (%s, %s, %s);''', (email, username, password))
    write_to_file.delay(email, result)
    db.commit()
    db.close()

# @app.task()
def sign_in(email, password):
    db = MySQLdb.connect("localhost", "root", "13610522", "Learning_English")
    cursor = db.cursor()
    cursor.execute('''select email,password,user_id,username,image_url,score from users
                               where email = '%s' and password=%s limit 1;''' % (email, password))
    db.commit()
    db.close()
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['email'] = row[0]
        d['password'] = row[1]
        d['user_id'] = row[2]
        d['username'] = row[3]
        d['image_url'] = row[4]
        d['score'] = row[5]
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j

# @app.task()
def db_set_level(level_title, level_description):
    db = MySQLdb.connect("127.0.0.1", "root", "13610522", "Learning_English")
    cursor = db.cursor()
    result = cursor.execute('''INSERT INTO level(level_title, level_description) VALUES ('%s', '%s');'''% (level_title, level_description))
    write_to_file.delay(level_title, result)
    db.commit()
    db.close()

def db_get_level():
    db = MySQLdb.connect("localhost", "root", "13610522", "Learning_English")
    cursor = db.cursor()
    cursor.execute('''select level_id,level_title,level_description from level;''')
    db.commit()
    db.close()
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['level_id'] = row[0]
        d['level_title'] = row[1]
        d['level_description'] = row[2]
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j

def get_lesson(level_id):
    db = MySQLdb.connect("localhost", "root", "1361522", "Learning_English")
    cursor = db.cursor()
    cursor.execute('''select l.lesson_id,l.lesson_title,l.lesson_description from lesson l where l.level_level_id=%s;'''% level_id)
    db.commit()
    db.close()
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['lesson_id'] = row[0]
        d['lesson_title'] = row[1]
        d['lesson_description'] = row[2]
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j
@app.task
def write_to_file(email, Result):
    print "Hello"
    f = open('Log/myfile.out', 'a')
    f.write('insert to DataBase with email: %s Successfull:{%s} at :%s\n'
            % (email, Result, datetime.datetime.now()))
    f.close()

