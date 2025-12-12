import pytz
import json
import pandas as pd
from datetime import datetime
from typing import List, Optional
from robertcommonio.system.io.mongo import MongoAccessor, MongoConfig, MongoFunc, convert_time
from bson.codec_options import CodecOptions


def test_mongo_utc():
    #accsss = MongoAccessor(config=MongoConfig('106.15.207.63', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None, True, 'Asia/Shanghai'))
    accsss = MongoAccessor(config=MongoConfig('106.15.207.63', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    records = list(accsss.find('proj_log', {'proj_id': '1', 'create_time_utc': {'$gte': datetime(2023, 4, 3, 6, 6, 0), '$lte': datetime(2023, 4, 3, 6, 7, 0)}}))
    print(records)


def test_mongo_utc1():
    accsss = MongoAccessor(config=MongoConfig('106.15.207.63', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    collection = accsss._get_coll('proj_log')
    # collection = accsss._get_coll('proj_log').with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))
    records = list(collection.find({'proj_id': '1', 'create_time_utc': {'$gte': datetime(2023, 4, 3, 6, 6, 0), '$lte': datetime(2023, 4, 3, 6, 7, 0)}}))
    print(records)


def load_history_data(start_time: datetime, end_time: datetime, interval: str, point_names: Optional[list] = None) -> pd.DataFrame:
    accessor = MongoAccessor(config=MongoConfig('106.14.226.254', 6517, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    result = pd.DataFrame()
    if isinstance(accessor, MongoAccessor):
        query_match = {'time': MongoFunc.get_time_query_match(start_time, end_time, interval)}
        if point_names:
            query_match.update({'name': {'$in': point_names}})

        pipe: List = [{'$match': query_match},  # 过滤数据
                      {'$project': MongoFunc.get_time_projection_match(start_time, interval)},
                      # 修改输⼊⽂档的结构， 如重命名、 增加、 删除字段、 创建计算结果
                      {'$unwind': '$value'},  # 会把数组中的数据分多条数据，数组外公共数据相同
                      {'$sort': {'value.time': 1}},  # 将输⼊⽂档排序后输出
                      {'$match': MongoFunc.get_value_query_match(start_time, end_time, interval)},
                      {'$project': {'name': 1, 'value': '$value.value', 'time': '$value.time'}}
                      ]
        collection = accessor._get_coll('proj_history_data_1').with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))
        query_df = pd.DataFrame(collection.aggregate(pipe, allowDiskUse=True))
        if not query_df.empty:
            query_df = query_df.set_index(['time', 'name'])
            if not query_df.index.is_unique:
                query_df = query_df[~query_df.index.duplicated(keep='first')]
            result = query_df.unstack().droplevel(level=0, axis=1)
    return result


def load_history_data1(start_time: datetime, end_time: datetime, interval: str, point_names: Optional[list] = None) -> pd.DataFrame:
    accessor = MongoAccessor(config=MongoConfig('106.14.226.254', 6517, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    result = pd.DataFrame()
    if isinstance(accessor, MongoAccessor):

        pipe1: List = [{'$match': {'name': {'$in': point_names}, 'time': {'$lte': start_time.replace(hour=0, minute=0, second=0)}}},  # 过滤数据 点名包含 时间小于查询时间
                       {'$project': MongoFunc.get_time_projection_match(start_time, "m1")},
                       {'$unwind': '$value'},
                       {'$project': {'name': 1, 'v': '$value.value', 't': '$value.time'}},
                       {"$sort": {'t': 1}},
                       {'$match': {'v': {'$exists': True, '$nin': list(MongoFunc.get_none_values())}}},
                       {"$group": {"_id": "$name", "value": {"$last": '$v'}}},
                        ]

        pipe2: List = [{'$match': {'name': {'$in': point_names}, 'time': {'$lte': start_time.replace(hour=0, minute=0, second=0), '$gte': start_time.replace(day=1, hour=0, minute=0, second=0)}}},
                       # 过滤数据 点名包含 时间小于查询时间
                       {'$project': {'_id': 0,  'name': 1, 'value': [{'value': f'$value.{_h}.{_m}'} for _h in range(0, 24) for _m in range(0, 60, 1)]}},
                       {"$sort": {'time': -1}},
                       {'$unwind': '$value'},
                       {'$project': {'name': 1, 'value': '$value.value'}},
                       #{"$sort": {'t': 1}},
                       {'$match': {'value': {'$exists': True, '$nin': list({'', None, 'None', 'none', 'null', 'Null', 'NULL', 'nan', 'NaN'})}}},
                       {"$group": {"_id": "$name", "value": {"$first": '$value'}}},
                       ]

        pipe21: List = [{'$match': {'name': {'$in': point_names}, 'time': {'$lte': start_time.replace(hour=0, minute=0, second=0), '$gte': start_time.replace(day=1, hour=0, minute=0, second=0)}}},
                       # 过滤数据 点名包含 时间小于查询时间
                        {'$project': MongoFunc.get_time_projection_match(start_time, "m1")},
                        {'$unwind': '$value'},
                        {'$sort': {'value.time': -1}},  # 将输⼊⽂档排序后输出
                        {'$match': {'value.time': {'$lte': start_time}, 'value.value': {'$exists': True, '$nin': list(MongoFunc.get_none_values())}}},
                        {"$limit": 1},
                        {'$project': {'name': 1, 'value': '$value.value', 'time': '$value.time'}}
                       ]

        pipe3: List = [{'$match': {'name': {'$in': point_names}, 'time': {'$lte': start_time.replace(hour=0, minute=0, second=0)}}},
                       # 过滤数据 点名包含 时间小于查询时间
                       #{'$project': {'_id': 0,  'name': 1, 'value': [{'value': f'$value.{_h}.{_m}'} for _h in range(0, 24) for _m in range(0, 60, 1)]}},
                       {"$sort": {'time': -1}},
                       {"$group": {"_id": "$name", "value": {"$first": '$value'}}},
                       {'$project': {'name': 1, 'time': 1, 'value': 1}},
                       {'$project': {'name': 1, 'value': [{'value': f'$value.{_h}.{_m}'} for _h in range(0, 24) for _m in range(0, 60, 1)]}},
                       {'$unwind': '$value'},
                       {'$project': {'name': 1, 'value': '$value.value'}},
                       #{'$unwind': '$value'},
                       #{'$project': {'name': 1, 'value': '$value.value'}},
                       #{"$sort": {'t': 1}},
                       {'$match': {'value': {'$exists': True, '$nin': list(MongoFunc.get_none_values())}}},
                       #{"$group": {"_id": "$name", "value": {"$first": '$value'}}},
                       ]


        collection = accessor._get_coll('proj_history_data_1').with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))
        query_df = pd.DataFrame(collection.aggregate(pipe2, allowDiskUse=True))
        if not query_df.empty:
            query_df = query_df.set_index(['time', 'name'])
            if not query_df.index.is_unique:
                query_df = query_df[~query_df.index.duplicated(keep='first')]
            result = query_df.unstack().droplevel(level=0, axis=1)
    return result


def get_last_history_data(start_time: datetime, point_names: Optional[list] = None) -> pd.DataFrame:
    accessor = MongoAccessor(config=MongoConfig('106.14.226.254', 6517, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    result = pd.DataFrame()

    if isinstance(accessor, MongoAccessor):
        for point_name in point_names:
            for record in list(accessor.find('proj_history_data_1', {'name': point_name, 'time': {'$lte': start_time.replace(hour=0, minute=0, second=0)}}, sort=[('time', -1)], limit=1)):
                values = record.get('value', {})
                if isinstance(values, dict):
                    print(list(values.get(list(values.keys())[-1], {}).values())[-1])

        collection = accessor._get_coll('proj_history_data_1').with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai')))
        query_df = pd.DataFrame(collection.aggregate(pipe3, allowDiskUse=True))
        if not query_df.empty:
            query_df = query_df.set_index(['time', 'name'])
            if not query_df.index.is_unique:
                query_df = query_df[~query_df.index.duplicated(keep='first')]
            result = query_df.unstack().droplevel(level=0, axis=1)
    return result


def export_mongo():
    accsss = MongoAccessor(config=MongoConfig('106.15.207.63', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    file_path = accsss.export_json_file(f"proj_page_offline", {}, limit=2, sort=[('_id', -1)], zip_compress=True)
    print()


def import_mongo():
    accsss = MongoAccessor(config=MongoConfig('127.0.0.1', 27017, 'gateway', 'gateway@123456', 'iot_engine', None, None, None))
    file_path = accsss.import_json_file(f"proj_page_offline.json.gz", 'proj_page_offline1', limit=2, action='replace')
    print()


export_mongo()
import_mongo()
#load_history_data1(datetime(2023, 10, 15, 0, 0, 0), datetime(2023, 10, 15, 5, 0, 0), 'm1', ['Plant1ThisDayJianChillerRoomPowerTotal'])
# get_last_history_data(datetime(2023, 10, 15, 0, 0, 0), ['Plant1ThisDayJianChillerRoomPowerTotal', 'Plant3ThisDayJianChillerRoomPowerTotal'])