import requests
import json
import mongodb
import os
import uuid
# from settings import

DB = 'nutapp'
COLLECTION = 'content'


def content_save(content_url, save_path):
    '''
    根据指定的资源url 及指定的存储路径 将资源存盘
    '''
    save_path_absolute = os.path.join(
        os.path.abspath("."),
        save_path
    )
    content = requests.get(content_url).content
    with open(save_path_absolute, 'wb') as f:
        f.write(content)


def get_content(content_id):
    '''
    根据指定喜马拉雅的资源id 将资源存盘及存库
    '''
    # content_id = '21017396'
    content_url = 'http://m.ximalaya.com/tracks/' + content_id + '.json'

    # 获取资源所有字段
    content = requests.get(content_url).content
    content_dict = json.loads(content)

    # 生成资源唯一id
    content_id = str(uuid.uuid4())

    # 存盘（audio）
    audio_url = content_dict.get('play_path_64')
    audio_save_path = os.path.join(
        'audio',
        content_id + '.' + 'mp3'
    )
    content_save(audio_url, audio_save_path)

    # 存盘（cover）
    cover_url = content_dict.get('cover_url')
    cover_save_path = os.path.join(
        'cover',
        content_id + '.' + 'jpg'
    )
    content_save(cover_url, cover_save_path)

    # 资源存库
    db, collection = mongodb.get_db_client(DB, COLLECTION)
    data = {
        'title': content_dict.get('title'),
        'category_name': content_dict.get('category_name'),
        'author': content_dict.get('nickname'),
        'audio_path': audio_save_path,
        'cover_path': cover_save_path,
    }
    mongodb.insert_one(collection, data)


get_content('21019227')
# print(content_dict, type(content_dict))
# {
#     'id': 21017396,
#     'play_path_64': 'http://audio.xmcdn.com/group18/M07/E2/C0/wKgJJVfOXReTcFg1AAoM-_xI-DQ089.m4a',
#     'play_path_32': 'http://audio.xmcdn.com/group19/M0B/E3/68/wKgJK1fOXT3CX9l_AAPaPxiTr_U031.m4a',
#     'play_path': 'http://audio.xmcdn.com/group18/M07/E2/C0/wKgJJVfOXReTcFg1AAoM-_xI-DQ089.m4a',
#     'duration': 81,
#     'title': '103 打电话',
#     'nickname': '会计Anna',
#     'uid': 5681553,
#     'waveform': 'group18/M07/E2/C0/wKgJJVfOXRXyrBXLAAAI3VMPP_82354.js',
#     'upload_id': 'u_20888942',
#     'cover_url': 'http://fdfs.xmcdn.com/group17/M07/E3/19/wKgJJFfOXKzBJtd9AACMiGpuM-M085.jpg',
#     'cover_url_142': 'http://fdfs.xmcdn.com/group17/M07/E3/19/wKgJJFfOXKzBJtd9AACMiGpuM-M085_web_large.jpg',
#     'formatted_created_at': '09月06日 14:07',
#     'is_favorited': False,
#     'play_count': 1349282,
#     'comments_count': 105,
#     'shares_count': 228,
#     'favorites_count': 2951,
#     'album_id': 5194595,
#     'album_title': '经典儿歌大全最流行益智歌曲',
#     'intro': '最流行益智儿歌卡拉OK 释放童真开阔思维拓展想象开启智慧艺术培养',
#     'have_more_intro': False,
#     'time_until_now': '2年前',
#     'category_name': 'ertong',
#     'category_title': '儿童',
#     'played_secs': None,
#     'is_paid': False,
#     'is_free': False,
#     'price': None,
#     'discounted_price': None
# }
# ret = content_dict.get('play_path_64')
# print('ret', ret)
