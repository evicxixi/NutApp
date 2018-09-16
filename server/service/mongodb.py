from pymongo import MongoClient


def get_db_client(db, collection):
    '''
    创建一个数据库连接并指定collection
    返回 db对象 & collection对象
    '''
    client = MongoClient('localhost', 27017)  # 连接MongoDB
    db = client[db]  # 使用指定数据库
    collection = db[collection]  # 使用指定collection
    return db, collection


def find_one(collection, username=None, user_id=None):
    '''
    查找是否存在指定用户
    '''
    if user_id:
        user_obj = collection.find_one({'_id': user_id})
    else:
        user_obj = collection.find_one({'username': username})
    if user_obj:
        return user_obj
    else:
        return False


def insert_one(collection, data):
    '''
    在指定MongoDB的collection中插入一条数据
    '''
    username = data.get('username')
    if find_one(collection, username=username):
        return False
    else:
        collection.insert_one(data)
        return True
