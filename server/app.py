from flask import Flask, render_template, request, send_file
from flask import jsonify
from service import mongodb
import settings
import bson
from blueprint import collector

# cors 跨域访问
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)  # cors 跨域访问

app.register_blueprint(collector.collector)    # 注册蓝图


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    若登陆成功 返回成功消息
    若失败 返回错误信息
    '''

    username = request.values.getlist('username')[0]
    password = request.values.getlist('password')[0]

    db, collection = mongodb.get_db_client(
        settings.DB, settings.COLLECTION)    # 获取db.collection对象
    user_obj = mongodb.find_one(collection, username=username)

    if not user_obj:
        data = {
            'username': None,
            'nickname': None,
            'msg': '登录失败 用户名不存在！',
            'code': -2,
        }
    else:
        if not password == user_obj.get('password'):
            data = {
                'username': user_obj.get('username'),
                'nickname': user_obj.get('nickname'),
                'msg': '登录失败 密码错误！',
                'code': -1,
            }
        elif password == user_obj.get('password'):
            data = {
                'username': user_obj.get('username'),
                'nickname': user_obj.get('nickname'),
                'msg': '登录成功！',
                'code': 1,
            }
    return jsonify(data)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    '''
    若用户名不冲突 存库并返回注册成功信息
    若冲突 返回错误信息
    '''
    username = request.values.getlist('username')[0]
    password = request.values.getlist('password')[0]
    nickname = request.values.getlist('nickname')[0]
    gender = request.values.getlist('gender')[0]
    age = request.values.getlist('age')[0]
    phone = request.values.getlist('phone')[0]
    data = {
        'username': username,
        'password': password,
        'nickname': nickname,
        'gender': gender,
        'age': age,
        'phone': phone,
    }

    db, collection = mongodb.get_db_client(
        settings.DB, settings.COLLECTION)    # 获取db.collection对象
    if mongodb.insert_one(collection, data):    # 存库
        data = {
            'nickname': nickname,
            'msg': '注册成功！',
            'code': 1,
        }
    else:
        data = {
            'nickname': nickname,
            'msg': '用户名已存在！',
            'code': -1,
        }
    return jsonify(data)


@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    print('----------->')
    username = request.values.getlist('username')[0]
    db, collection = mongodb.get_db_client(
        settings.DB, settings.COLLECTION)    # 获取db.collection对象
    user_obj = mongodb.find_one(collection, username=username)
    user_obj['_id'] = str(user_obj['_id'])
    print('user_id', user_obj, type(user_obj))
    return jsonify(user_obj)


if __name__ == '__main__':
    app.run(debug=True)
