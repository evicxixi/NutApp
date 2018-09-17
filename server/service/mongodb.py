from pymongo import MongoClient
from bson.objectid import ObjectId


def get_db_client(db, collection):
    '''
    创建一个数据库连接并指定collection
    返回 db对象 & collection对象
    '''
    client = MongoClient('localhost', 27017)  # 连接MongoDB
    db = client[db]  # 使用指定数据库
    collection = db[collection]  # 使用指定collection
    return db, collection


def find_one(collection, username=None, id=None):
    '''
    查找是否存在指定用户
    '''
    # id = '123456777777123456777777'
    if id:
        print('id', type(id), id)
        data = collection.find_one({'_id': ObjectId(id)})
        data['_id'] = str(data.get('_id'))
    else:
        data = collection.find_one({'username': username})
    if data:
        return data
    else:
        return False


def find_all(collection):
    '''
    查找
    '''

    data = collection.find()
    # print('data', type(data), data)
    return data


def insert_one(collection, data):
    '''
    在指定MongoDB的collection中插入一条数据
    '''
    collection.insert_one(data)
    return True
