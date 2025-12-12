import logging
import gzip
import pytz
import numpy as np
import pandas as pd
from bson.json_util import dumps, loads, default as bson_default
from bson.objectid import ObjectId
from bson.codec_options import CodecOptions
from datetime import datetime
from typing import NamedTuple, Optional, Iterator, List, Union, Any, Tuple
import math

from pymongo import MongoClient, ASCENDING
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference as RP
from pymongo.results import UpdateResult, DeleteResult, InsertManyResult, BulkWriteResult
from pymongo.client_session import ClientSession
from pymongo.operations import UpdateOne, UpdateMany, InsertOne, DeleteOne, DeleteMany

from robertcommonbasic.basic.validation import input
from robertcommonbasic.basic.data.utils import chunk_list
from robertcommonbasic.basic.dt.utils import parse_time, relativedelta, TimeInterval, convert_time
from robertcommonbasic.basic.os.file import create_dir_if_not_exist, check_file_exist
from robertcommonbasic.basic.cls.utils import retry
from robertcommonbasic.basic.error.utils import InputDataError

MongoWriteOp = Union[UpdateOne, UpdateMany, InsertOne, DeleteOne, DeleteMany]


class MongoConfig(NamedTuple):
    HOST: str
    PORT: int
    USER: Optional[str]
    PWD: Optional[str]
    DB_NAME: Optional[str]
    REPLICA_SET: Optional[str]
    READ_PREFERENCE: Optional[str]
    READ_PREFERENCE_TAGS: Optional[str] = None
    TZ_AWARE: Optional[bool] = None
    TZ_INFO: Optional[str] = None


class MongoAccessor:

    def __init__(self, config: MongoConfig):
        config = input.ensure_not_none_of('config', config, MongoConfig)
        self._config = config._replace(
            HOST=input.ensure_not_none_str('HOST', config.HOST),
            PORT=input.ensure_int('PORT', config.PORT) or 27017,
            DB_NAME=input.ensure_str('DB_NAME', config.DB_NAME) or 'beopdata',
            USER=input.ensure_not_none_str('USER', config.USER),
            PWD=input.ensure_not_none_str('PWD', config.PWD),
            REPLICA_SET=input.ensure_str('REPLICA_SET', config.REPLICA_SET) or None,
            READ_PREFERENCE=input.ensure_str('READ_PREFERENCE', config.READ_PREFERENCE) or None,
            READ_PREFERENCE_TAGS=input.ensure_str('READ_PREFERENCE_TAGS', config.READ_PREFERENCE_TAGS) or None,
            TZ_AWARE=input.ensure_bool('TZ_AWARE', config.TZ_AWARE) or None,
            TZ_INFO=input.ensure_str('TZ_INFO', config.TZ_INFO) or None,
        )
        self._safe_log_config = self._config._replace(PWD='*')
        self._conn = None

    def __str__(self):
        return f"[{self._config.HOST}:{self._config.PORT}]"

    def __del__(self):
        if self._conn is None:
            return
        try:
            self._conn.close()
        except Exception:
            if logging.error:
                logging.error(f"Failed to close {self._safe_log_config}")

    @property
    def conn(self):
        return self._get_connection()

    @property
    def mdbBb(self):
        return self.conn[self._config.DB_NAME]

    @property
    def use_replica(self):
        return self._config.REPLICA_SET is not None

    def _get_connection(self):
        if not self._conn:
            logging.info(f"Connecting to MongoDB: {self._safe_log_config}...")
            try:
                args = dict(
                    username=self._config.USER,
                    password=self._config.PWD,
                    maxPoolSize=300,
                    maxIdleTimeMS=60000,
                    serverSelectionTimeoutMS=120000,
                    waitQueueTimeoutMS=20000,
                    socketTimeoutMS=60000,
                    ssl=False,
                    authSource=self._config.DB_NAME,
                )
                if self._config.TZ_AWARE is not None:
                    args.update(tz_aware=self._config.TZ_AWARE, tzinfo=None if self._config.TZ_INFO is None else pytz.timezone(self._config.TZ_INFO))
                if self._config.REPLICA_SET is not None and self._config.READ_PREFERENCE is not None:
                    args.update(dict(replicaset=self._config.REPLICA_SET, readPreference=self._config.READ_PREFERENCE, readPreferenceTags=self._config.READ_PREFERENCE_TAGS or ''))
                self._conn = MongoClient(host=self._config.HOST, port=self._config.PORT, **args)
                logging.info(f"Successfully connected to {self._safe_log_config}!")
            except Exception as e:
                raise ConnectionRefusedError(f'Failed to connect to {self._safe_log_config}!')
        return self._conn

    def _get_coll(self, coll_name: str, tz_info: Optional[str] = None):
        return self.mdbBb.get_collection(coll_name) if tz_info is None else self.mdbBb.get_collection(coll_name).with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=pytz.timezone(tz_info)))

    def get_coll_names(self) -> List[str]:
        return self.mdbBb.list_collection_names()

    def find(self, coll_name: str, query: dict, projection: Optional[dict] = None, skip: Optional[int] = None, limit: Optional[int] = None, sort: Optional[List[Tuple[str, int]]] = None, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> Iterator[dict]:
        coll = self._get_coll(coll_name, tz_info)
        kwargs = {}
        if projection:
            kwargs['projection'] = projection
        if skip:
            kwargs['skip'] = skip
        if limit:
            kwargs['limit'] = limit
        if sort:
            kwargs['sort'] = sort
        if session:
            kwargs['session'] = session
        with coll.find(filter=query, **kwargs) as cursor:
            for doc in cursor:
                yield doc

    def count(self, coll_name: str, query: dict, projection: Optional[dict] = None, tz_info: Optional[str] = None) -> int:
        coll = self._get_coll(coll_name, tz_info)
        kwargs = {}
        if projection:
            kwargs['projection'] = projection
        return coll.count_documents(filter=query, **kwargs)

    def aggr(self, coll_name: str, pipeline: List, allow_disk_use: bool = False, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> Iterator[dict]:
        coll = self._get_coll(coll_name, tz_info)
        with coll.aggregate(pipeline, allowDiskUse=allow_disk_use, session=session) as cursor:
            for doc in cursor:
                yield doc

    def insert_many(self, coll_name: str, docs: List[dict], session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> InsertManyResult:
        coll = self._get_coll(coll_name, tz_info)
        result = coll.insert_many(docs, session=session)
        return result

    def update_many(self, coll_name: str, query: dict, update: dict, upsert: bool = False, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> UpdateResult:
        coll = self._get_coll(coll_name, tz_info)
        result = coll.update_many(query, update, upsert, session=session)
        return result

    def delete_many(self, coll_name: str, query: dict, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> DeleteResult:
        coll = self._get_coll(coll_name, tz_info)
        result = coll.delete_many(query, session=session)
        return result

    def start_session(self):
        return self.conn.start_session()

    def start_session_transaction(self, read_concern: Optional[ReadConcern] = None, write_concern: Optional[WriteConcern] = None, read_preference: Optional[RP] = RP.PRIMARY) -> 'MongoSessionContext':
        return MongoSessionContext(self, read_concern, write_concern, read_preference)

    def bulk_write(self, coll_name: str, ops: List[MongoWriteOp], ordered: bool = True, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> BulkWriteResult:
        coll = self._get_coll(coll_name, tz_info)
        return coll.bulk_write(ops, ordered, session=session)

    def create_index(self, coll_name: str, keys, session: Optional[ClientSession] = None, tz_info: Optional[str] = None, **kwargs):
        coll = self._get_coll(coll_name, tz_info)
        return coll.create_index(keys, session=session, **kwargs)

    def drop_coll(self, coll_name: str, session: ClientSession = None, tz_info: Optional[str] = None):
        coll = self._get_coll(coll_name, tz_info)
        coll.drop(session=session)

    def distinct(self, coll_name: str, key: str, query: Optional[dict] = None, session: Optional[ClientSession] = None, tz_info: Optional[str] = None) -> Any:
        coll = self._get_coll(coll_name, tz_info)
        rv = coll.distinct(key=key, filter=query, session=session)
        return rv
    
    def index_information(self, coll_name: str, tz_info: Optional[str] = None, **kwargs):
        coll = self._get_coll(coll_name, tz_info)
        return coll.index_information(**kwargs)

    def export_json_file(self, coll_name: str, query: dict = {}, limit: Optional[int] = 1000, sort: Optional[List[Tuple[str, int]]] = None, zip_compress: bool = False, tz_info: Optional[str] = None, file_folder: Optional[str] = None):
        """导出为Json"""
        coll = self._get_coll(coll_name, tz_info)
        count = coll.count_documents(filter=query)
        if count > 0:
            file_name = f"{coll_name}"
            if isinstance(file_folder, str) and len(file_folder) > 0:
                create_dir_if_not_exist(file_folder)
                file_name = f"{file_folder}/{file_name}"
            file_name = f"{file_name}.json" if zip_compress is False else f"{file_name}.json.gz"

            with gzip.open(file_name, 'wb') if zip_compress is True else open(file_name, 'wb') as f:
                for num in range(0, count, limit):
                    for record in coll.find(query).skip(num).limit(limit).sort(sort) if sort is not None else coll.find(query).skip(num).limit(limit):
                        f.write(f"{dumps(record, default=bson_default, ensure_ascii=False)}\n".encode())
            return file_name
        return ''

    def import_json_file(self, file_path: str, coll_name: str, limit: Optional[int] = None, action: str = 'insert', tz_info: Optional[str] = None):
        """导入json文件"""
        if check_file_exist(file_path) is True:
            coll = self._get_coll(coll_name, tz_info)
            if action == 'replace':
                coll.drop()

            with gzip.open(file_path, 'rb') if file_path.endswith('.json.gz') is True else open(file_path, 'rb') as f:
                docs = {}
                for content in f:
                    record = loads(content.decode())
                    docs[record.get('_id')] = record
                    if isinstance(limit, int) and len(docs) >= limit:
                        if action == 'update':
                            coll.delete_many({'_id': {'$in': list(docs.keys())}})
                        coll.insert_many(list(docs.values()))
                        docs = {}
                if len(docs) > 0:
                    if action == 'update':
                        coll.delete_many({'_id': {'$in': list(docs.keys())}})
                    coll.insert_many(list(docs.values()))
                return True
        return False


class MongoTransactionalSession:

    def __init__(self, accessor: MongoAccessor, read_concern: Optional[ReadConcern] = None, write_concern: Optional[WriteConcern] = None, read_preference: Optional[RP] = RP.PRIMARY):
        self._accessor = accessor
        if accessor.use_replica:
            self._session = accessor.conn.start_session()
            self._session.start_transaction(read_concern=read_concern, write_concern=write_concern, read_preference=read_preference)
        else:
            self._session = None
        self._disposed = False

    def _check(self):
        if self._disposed:
            raise RuntimeError("Current session already disposed!")

    def find(self, coll_name: str, query: dict, projection: Optional[dict] = None, skip: Optional[int] = None, limit: Optional[int] = None, sort: Optional[dict] = None) -> Iterator[dict]:
        self._check()
        return self._accessor.find(coll_name, query, projection, skip, limit, sort, session=self._session)

    def aggr(self, coll_name: str, pipeline: List, allow_disk_use: bool = False) -> Iterator[dict]:
        self._check()
        return self._accessor.aggr(coll_name, pipeline, allow_disk_use, session=self._session)

    def insert_many(self, coll_name: str, docs: List[dict]) -> InsertManyResult:
        self._check()
        return self._accessor.insert_many(coll_name, docs, session=self._session)

    def update_many(self, coll_name: str, query: dict, update: dict, upsert: bool = False) -> UpdateResult:
        self._check()
        return self._accessor.update_many(coll_name, query, update, upsert, session=self._session)

    def delete_many(self, coll_name: str, query: dict) -> DeleteResult:
        self._check()
        return self._accessor.delete_many(coll_name, query, session=self._session)

    def bulk_write(self, coll_name: str, ops: List[MongoWriteOp], ordered: bool = True):
        self._check()
        return self._accessor.bulk_write(coll_name, ops, ordered=ordered, session=self._session)

    def distinct(self, coll_name: str, key: str, query: dict):
        self._check()
        return self._accessor.distinct(coll_name, key, query, session=self._session)

    def close(self, abort=False):
        if self._accessor.use_replica:
            if abort:
                self._session.abort_transaction()
            else:
                self._session.commit_transaction()
            self._session.end_session()
        self._disposed = True


class MongoSessionContext:
    def __init__(self, accessor: MongoAccessor, read_concern: Optional[ReadConcern] = None, write_concern: Optional[WriteConcern] = None, read_preference: Optional[RP] = RP.PRIMARY):
        self._accessor = accessor
        self._read_concern = read_concern
        self._write_concern = write_concern
        self._read_preference = read_preference

    def __enter__(self):
        self._session = MongoTransactionalSession(self._accessor, self._read_concern, self._write_concern, self._read_preference)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        abort = True if exc_val else False
        self._session.close(abort)


class MongoFunc:

    @staticmethod
    def get_none_values() -> set:
        return {'', None, 'None', 'none', 'null', 'Null', 'NULL', math.nan, 'nan', 'NaN', '-inf', 'inf', math.inf, -math.inf, '1.#r', '1.#R', 'Infinity', np.nan}

    @staticmethod
    def gen_db_name(tb_name: str):
        return f"mongo_data_{tb_name}"

    @staticmethod
    def gen_insert_history_sql(datas: list, per_operation_limit: int = 30000) -> list:
        insert_sql = []
        chunk_datas = chunk_list(datas, per_operation_limit)
        for chunk_data in chunk_datas:
            insert_req = []
            for i, d in enumerate(chunk_data):
                point_name = None
                point_value = None
                point_time = None
                if isinstance(d, list) or isinstance(d, tuple):
                    point_name = d[1]
                    point_value = d[2]
                    point_time = parse_time(d[0])
                elif isinstance(d, dict):
                    point_name = d.get('name')
                    point_value = d.get('value')
                    point_time = parse_time(d.get('time'))
                if point_name is not None and point_value is not None and point_time is not None:
                    insert_req.append(UpdateOne({'name': point_name, 'time': point_time.replace(hour=0, minute=0, second=0, microsecond=0)}, {'$set': {f'value.{point_time.hour}.{point_time.minute}': point_value}}, True))
            if len(insert_req) > 0:
                insert_sql.append(insert_req)
        return insert_sql

    @staticmethod
    def insert_history_data(conn: MongoAccessor, datas: list, tb_name: str, retry_count: int = 3) -> int:
        insert_size = len(datas)
        if insert_size <= 0:
            return 0

        insert_sqls = MongoFunc.gen_insert_history_sql(datas)
        for sql in insert_sqls:
            try:
                result = retry(conn.mdbBb[MongoFunc.gen_db_name(tb_name)].bulk_write, retry_count, 1, sql)
                conn.mdbBb[MongoFunc.gen_db_name(tb_name)].create_index([('time', ASCENDING), ('name', ASCENDING)], unique=True)
            except Exception:
                pass

        return insert_size

    @staticmethod
    def delete_history_data(conn: MongoAccessor, tb_name: str, point_name: str, point_time: Union[str, datetime]) -> bool:
        del_time = convert_time(point_time, None, None, False)
        conn.mdbBb[MongoFunc.gen_db_name(tb_name)].update_one({'time': datetime(year=del_time.year, month=del_time.month, day=del_time.day), 'name': point_name}, {'$unset': {f"value.{del_time.hour}.{del_time.minute}": 1}})
        return True

    @staticmethod
    def get_months(start: datetime, end: datetime) -> list:
        months = []
        _start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        _end = end.replace(hour=0, minute=0, second=0, microsecond=0)
        while _start <= _end:
            months.append(_start)
            _start = _start + relativedelta(months=1)
        return months

    @staticmethod
    def get_time_projection(hour: int, minute: int) -> dict:
        return {'time': {'$add': ['$time', hour * 3600000 + minute * 60000]}, 'value': f'$value.{hour}.{minute}'}

    @staticmethod
    def get_time_projection_match(start: datetime, time_format: str) -> dict:
        if time_format == 's1':
            raise NotImplementedError("time_format 's1' is not supported.")
        elif time_format == 'm1':
            value_projection = [MongoFunc.get_time_projection(_h, _m) for _h in range(0, 24) for _m in range(0, 60, 1)]
        elif time_format == 'm5':
            value_projection = [MongoFunc.get_time_projection(_h, _m) for _h in range(0, 24) for _m in range(0, 60, 5)]
        elif time_format == 'h1':
            value_projection = [MongoFunc.get_time_projection(h, start.minute) for h in range(0, 24)]
        elif time_format == 'd1':
            value_projection = [MongoFunc.get_time_projection(start.hour, start.minute)]
        elif time_format == 'M1':
            value_projection = [MongoFunc.get_time_projection(start.hour, start.minute)]
        else:
            raise NotImplementedError(f"Invalid time_format {time_format}!")

        return {'_id': 0, 'time': 1, 'name': 1, 'value': value_projection}

    @staticmethod
    def get_value_query_match(start: datetime, end: datetime, time_format: str) -> dict:
        if time_format == 'M1':
            time_match = {'$gte': start.replace(hour=0, minute=0, second=0), '$lte': end.replace(hour=0, minute=0, second=0)}
        else:
            time_match = {'$gte': start, '$lte': end}
        return {'value.time': time_match, 'value.value': {'$exists': True, '$nin': list(MongoFunc.get_none_values())}}

    @staticmethod
    def get_time_query_match(start: datetime, end: datetime, time_format: str, tz_info: Optional[str] = None) -> dict:
        if time_format == 'M1':
            if tz_info is not None:
                start = convert_time(start, 'UTC', tz_info)
                end = convert_time(end, 'UTC', tz_info)
            date_range = pd.date_range(start, end, freq=TimeInterval(time_format).pandas_freq)
            time_query_match = {'$in': [(convert_time(date.to_pydatetime(), tz_info, 'UTC') if tz_info is not None else date.to_pydatetime()).replace(hour=0, minute=0, second=0) for date in date_range.to_list()]}
        else:
            time_query_match = {'$gte': start.replace(hour=0, minute=0, second=0), '$lte': end.replace(hour=0, minute=0, second=0)}
        return time_query_match

    @staticmethod
    def get_history_data(collection, time_format: str, start: Union[str, datetime], end: Union[str, datetime], points: list, is_all: bool = False):
        cursor = None
        records = []
        try:
            start = convert_time(start, None, None, False)
            end = convert_time(end, None, None, False)

            value_query_match = MongoFunc.get_value_query_match(start, end, time_format)
            time_query_match = MongoFunc.get_time_query_match(start, end, time_format)

            query_match = {'time': time_query_match}
            if not is_all:
                query_match.update({'name': {'$in': points}})

            projection = MongoFunc.get_time_projection_match(start, time_format)

            agg = [
                # Filter out day-based documents
                {
                    '$match': query_match
                },
                # Extract key-value based hour-minute value into an array
                {
                    '$project': projection
                },
                # Split hour-minute value array
                {
                    '$unwind': '$value'
                },
                {
                    '$sort': {
                        'value.time': 1
                    }
                },
                # Filter out unwanted values on the start/end day
                {
                    '$match': value_query_match
                },
                # Convert time object to string
                {
                    '$project': {
                        'name': 1,
                        'value.value': 1,
                        'value.time': {
                            '$dateToString': {
                                'date': '$value.time',
                                'format': '%Y-%m-%d %H:%M:%S'
                            }
                        }
                    }
                },
                # Group by point name
                {
                    '$group': {
                        '_id': '$name',
                        'value': {
                            '$push': '$value'
                        }
                    }
                },
                # Clear unused information
                {
                    '$project': {
                        'name': '$_id',
                        'record': '$value',
                        '_id': 0
                    }
                },
            ]

            options = {'allowDiskUse': True}

            with collection.aggregate(agg, **options) as cursor:
                rv = list(cursor)

            # 缺省值补充
            returned_point_names = set(points)
            for point_and_records in rv:
                if not is_all:
                    returned_point_names.remove(point_and_records['name'])
                for record in point_and_records['record']:
                    try:
                        record['value'] = float(record['value'])
                    except Exception:
                        pass

            records.extend(rv)

            # Sort result to match the point list order
            if not is_all:
                records.sort(key=lambda item: points.index(item.get('name')))
        except Exception:
            logging.error(
                f'Unhandled exception! collection={collection}, time_format={time_format}, start={start}, end={end}, points={points}',
                exc_info=True,
                stack_info=True)
        finally:
            if cursor:
                cursor.close()
        return records

    @staticmethod
    def get_pd_freq(time_interval: Union[TimeInterval, str]) -> str:
        time_interval = input.ensure_not_none_enum('time_interval', time_interval, TimeInterval)
        if time_interval == TimeInterval.s1:
            freq = '1S'
        elif time_interval == TimeInterval.m1:
            freq = '1T'
        elif time_interval == TimeInterval.m5:
            freq = '5T'
        elif time_interval == TimeInterval.h1:
            freq = '1H'
        elif time_interval == TimeInterval.d1:
            freq = '1D'
        elif time_interval == TimeInterval.M1:
            freq = '1MS'
        else:
            raise InputDataError(f'Can not transfer TimeInterval={time_interval} to pandas freq string')
        return freq

    @staticmethod
    def get_pd_date_range(start: datetime, end: datetime, time_interval: Union[TimeInterval, str]):
        freq = MongoFunc.get_pd_freq(time_interval)
        return pd.date_range(start=start, end=end, freq=freq)

    @staticmethod
    def get_his_data_time_chunk(start: datetime, end: datetime, time_format: Union[TimeInterval, str], use_chunk: bool = True):
        if use_chunk:
            return MongoFunc.get_pd_date_range(start, end, time_format).to_series().resample('1D').agg(['min', 'max'])
        else:
            return pd.DataFrame([{'min': start, 'max': end}])

    @staticmethod
    def his_data_json_to_df(points: list, melt: bool = True) -> pd.DataFrame:
        if len(points) > 0:
            dfs = []
            for point in points:
                df = pd.DataFrame(point['record'])
                df['point'] = point['name']
                dfs.append(df)

            if len(dfs) > 0:
                df_all = pd.concat(dfs)
                df_all['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
                df_all = df_all.set_index('time')

                if melt:
                    pass
                else:
                    df_all = df_all.pivot_table(values='value', index=df_all.index, columns='point', aggfunc='last')
                df_all = df_all.sort_index()
                return df_all
        return None

    @staticmethod
    def get_history_data_by_chunk(conn: MongoAccessor, tb_name: str, points: list, start: Union[str, datetime], end: Union[str, datetime], time_format: Union[TimeInterval, str], is_all: bool = False, use_chunk: bool = False):
        t_df = MongoFunc.get_his_data_time_chunk(start, end, time_format, use_chunk)
        for index, row in t_df.iterrows():
            row = row.to_dict()
            start = row['min']
            end = row['max']
            his_data_json = MongoFunc.get_history_data(collection=conn.mdbBb[MongoFunc.gen_db_name(tb_name)], points=points, start=start, end=end, time_format=time_format.value if isinstance(time_format, TimeInterval) else time_format, is_all=is_all)
            yield MongoFunc.his_data_json_to_df(his_data_json)

    @staticmethod
    def merge_record_to_df(record: pd.Series):
        sub_dfs = []
        sub_df = pd.DataFrame(record['record'])
        sub_df.set_index('time', inplace=True)
        sub_df.index = pd.to_datetime(sub_df.index)
        sub_df.rename(columns={"value": record['name']}, inplace=True)
        if not sub_df.index.is_unique:
            sub_df = sub_df[~sub_df.index.duplicated(keep='first')]
        sub_dfs.append(sub_df)
        return sub_dfs

    @staticmethod
    def merge_point_df(dfs: List[Optional[pd.DataFrame]], names: Optional[List[str]] = None, melt: bool = False, need_error: bool = True, only_keep_exists: bool = False):
        names = np.unique(names)
        dfs = [df for df in dfs if df is not None]
        if len(dfs) == 1:
            return dfs[0]
        elif len(dfs) == 0:
            return None
        if melt:
            df_merged = pd.concat(dfs)
            df_merged = df_merged[~df_merged.index.duplicated(keep='first')]
            if names is not None and len(names) and not only_keep_exists:
                time_index = df_merged.index.get_level_values('time').unique()
                df_merged = df_merged.reindex(pd.MultiIndex.from_product([time_index, names], names=['time', 'point']))
                if need_error:
                    df_merged['error'] = df_merged['error'].fillna(True)
        else:
            df_merged = pd.concat(dfs, axis=1)
            df_merged = df_merged[~df_merged.index.duplicated(keep='first')]
            if names is not None and len(names) and not only_keep_exists:
                names_nan = pd.Index(names).difference(df_merged.columns)
                for name in names_nan:
                    df_merged[str(name)] = np.nan
        return df_merged

    @staticmethod
    def convert_point_df(record: pd.DataFrame) -> UpdateOne:
        time: datetime = record['time'].to_pydatetime()
        query = {'name': record['name'], 'time': time.replace(hour=0, minute=0, microsecond=0)}
        values = {f'value.{time.hour}.{time.minute}': record['value']}
        return UpdateOne(filter=query, update={'$set': values},  upsert=True)

    @staticmethod
    def get_history_data_df(conn: MongoAccessor, tb_name: str, points: list, start: Union[str, datetime], end: Union[str, datetime], time_format: Union[TimeInterval, str], is_all: bool = False, use_chunk: bool = False):
        if use_chunk:
            return MongoFunc.get_history_data_by_chunk(conn, tb_name, points, start, end, time_format, is_all, use_chunk)
        else:
            dfs = list(MongoFunc.get_history_data_by_chunk(conn, tb_name, points, start, end, time_format, is_all, use_chunk))
            return MongoFunc.merge_point_df(dfs)

    @staticmethod
    def convert_insert_records(records: list) -> list:
        return [InsertOne({'_id': ObjectId(), 'time': datetime.utcnow(), **record}) for record in records if isinstance(record, dict)]
