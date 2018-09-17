from flask import Blueprint, redirect, render_template, send_file
from flask import jsonify
import settings
import json
from service import mongodb
from bson.json_util import dumps
# 可以为蓝图独立Temp 和 static    而flask实例化的时候不需要定义名称
collector = Blueprint("collector", __name__)


@collector.route("/audio_list", methods=['GET', "POST"])
def audio_list():   # 备注（坑）：蓝图注册名称，与蓝图的路由函数名称不能重复。
    db, collection = mongodb.get_db_client('nutapp', 'content')
    data = mongodb.find_all(collection)

    data = list(data)
    for index, item in enumerate(data):
        data[index]["_id"] = str(item.get("_id"))
    # print('data', type(data), data)
    return jsonify(data)


@collector.route("/file/<type>/<id>", methods=['GET', "POST"])
def get_file(type, id):
    print(id)
    # db, collection = mongodb.get_db_client('nutapp', 'content')
    # data = mongodb.find_one(collection, id=id)
    # print('data', data, type(data))
    type = str(type)
    content_path = type + '/' + id
    return send_file(content_path)
