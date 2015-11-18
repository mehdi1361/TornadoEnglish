__author__ = 'mehdi'
from celery import Celery
import MySQLdb
import datetime
import collections
import json

from celery import group

app = Celery('tasks', broker='amqp://guest@localhost//')

# host = "127.0.0.1"
# user = "root"
# password = 1361522
# database = 'Learning_English'
# @app.task()
def sign_up(email, username, password):
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
    cursor = db.cursor()
    result = cursor.execute('''INSERT INTO users(email, username, password) VALUES (%s, %s, %s);''',
                            (email, username, password))
    write_to_file.delay(email, result)
    db.commit()
    db.close()


# @app.task()
def sign_in(email, password):
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
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
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
    cursor = db.cursor()
    result = cursor.execute(
        '''INSERT INTO level(level_title, level_description) VALUES ('%s', '%s');''' % (level_title, level_description))
    write_to_file.delay(level_title, result)
    db.commit()
    db.close()


def db_get_level():
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
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


def db_set_lesson(lesson_title, lesson_description,level_level_id):
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
    cursor = db.cursor()
    result = cursor.execute( '''INSERT INTO lesson(lesson_title, lesson_description, level_level_id)  VALUES ('%s', '%s', %s);''' % (lesson_title, lesson_description,level_level_id))
    write_to_file.delay(lesson_title, result)
    db.commit()
    db.close()


def db_get_lesson(level_level_id):
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
    cursor = db.cursor()
    cursor.execute('''select lesson_id,lesson_title,lesson_description from lesson  where level_level_id=%s;''' % level_level_id)
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

def db_get_questions(lesson_lesson_id):
    db = MySQLdb.connect("127.0.0.1", "root", '13610522', 'Learning_English', charset='utf8')
    cursor = db.cursor()
    cursor.execute('''select question_id,question_title,question_description,question_time,question_expireStart,question_expireEnd,score,question_kind from question where lesson_lesson_id=%s''' % lesson_lesson_id)
    db.commit()
    db.close()
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['question_id'] = row[0]
        d['question_title'] = row[1]
        d['question_description'] = row[2]
        d['score'] = row[6]
        d['question_kind'] = row[7]
        objects_list.append(d)
    j = json.dumps(objects_list)
    return j

def db_set_question(question_title, question_description, question_time, question_expireStart, question_expireEnd, score, question_type_idquestion_type, lesson_lesson_id, question_kind):
    db = MySQLdb.connect("127.0.0.1", "root", 1361522, 'Learning_English', charset='utf8')
    cursor = db.cursor()
    result = cursor.execute('''insert into question(question_title, question_description, question_time, question_expireStart, question_expireEnd, score, question_type_idquestion_type, lesson_lesson_id, question_kind) VALUES ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s)''' % (question_title, question_description, question_time, question_expireStart, question_expireEnd, score, question_type_idquestion_type, lesson_lesson_id, question_kind))
    # write_to_file.delay(lesson_title, result)
    db.commit()
    db.close()

@app.task(trail=True)
def A(how_many):
    return group(B.s(i) for i in range(how_many))()
@app.task(trail=True)
def B(i):
    return pow2.delay(i)

@app.task(trail=True)
def pow2(i):
    return i ** 2
@app.task
def write_to_file(email, Result):
    print "Hello"
    f = open('Log/myfile.out', 'a')
    f.write('insert to DataBase with email: %s Successfull:{%s} at :%s\n'
            % (email, Result, datetime.datetime.now()))
    f.close()
