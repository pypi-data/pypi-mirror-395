from bson import ObjectId
from datetime import datetime, timedelta
from enum import Enum, unique
from typing import Dict, List, Any, NamedTuple, Optional, Union

from robertcommonbasic.basic.dt.utils import DateRange
from robertcommonbasic.basic.data.datatuple import pd, np
from robertcommonbasic.basic.data.conversion import try_convert_value
from robertcommonbasic.basic.validation import input

from .mysql import MySqlAccessor
from .mongo import MongoFunc, MongoAccessor, ASCENDING, MongoConfig, TimeInterval


@unique
class DsType(Enum):
    """
    Data source type enumeration.
    """
    # A raw point reference
    DSA_RAW = -1
    # A site point reference
    DSA_SITE = 0
    # A virtual point reference
    DSA_VIRTUAL = 1
    # A calculation point reference
    DSA_CALC = 2
    # A DHive point attribute reference
    DHIVE_POINT = 3
    # A DHive MCU reference
    DHIVE_MCU = 4
    # a Files point
    FILES_POINT = 5


@unique
class DsRefType(Enum):
    # Point name: @888|Z9_L10_AHU_01_SaTemp
    DSA = 'DSA'
    # DHive attribute ID: $888|5d3aa4107a05d900234f1154
    DHIVE = 'DHIVE'
    # Fils Point name: @5d3aa4107a05d900234f1154|Z9_L10_AHU_01_SaTemp
    FILES = 'FILES'


class DsRef(NamedTuple):
    """
    Data Source Reference
    """
    ref_type: DsRefType
    # ds_repo_id Union
    # proj_id: str
    # files_id: ObjectId
    ds_repo_id: Union[int, ObjectId]
    # For POINT, ds_name is the cloud point name
    # For DHIVE, ds_name is the Object ID of the node attribute
    ds_name: str

    @property
    def proj_id(self):
        if self.ref_type in (DsRefType.DSA, DsRefType.DHIVE):
            return self.ds_repo_id

    @property
    def files_id(self):
        if self.ref_type == DsRefType.FILES:
            return self.ds_repo_id

    @property
    def his_point_name(self):
        if self.ref_type == DsRefType.DHIVE:
            return f'MCU__{self.ds_name}'
        else:
            return self.ds_name


class DsIdParser:

    _DHIVE_STARTER = '$'
    _DSA_STARTER = '@'
    _SEPARATOR = '|'

    @classmethod
    def _parse(cls, ds_item_id: Union[str, DsRef], raise_on_error: bool = True) -> Optional[DsRef]:
        if isinstance(ds_item_id, DsRef):
            return ds_item_id

        if not ds_item_id:
            if raise_on_error:
                raise ValueError(f"Empty ds_item_id")
            else:
                return None

        if len(ds_item_id) < 4:
            if raise_on_error:
                raise ValueError(f"ds_item_id is too short: {ds_item_id}")
            else:
                return None

        parts = ds_item_id[1:].split(cls._SEPARATOR, 1)
        if len(parts) != 2:
            if raise_on_error:
                raise ValueError(f"{ds_item_id} does not have correct parts "
                                 f"separated by {cls._SEPARATOR}!")
            else:
                return None

        if ObjectId.is_valid(parts[0]):
            ds_ref_type = DsRefType.FILES
            ds_repo_id = input.ensure_not_none_objid(ds_item_id, parts[0])
        elif ds_item_id.startswith(cls._DHIVE_STARTER):
            ds_ref_type = DsRefType.DHIVE
            ds_repo_id = input.ensure_not_none_int(ds_item_id, parts[0])
        elif ds_item_id.startswith(cls._DSA_STARTER):
            ds_ref_type = DsRefType.DSA
            ds_repo_id = input.ensure_not_none_int(ds_item_id, parts[0])
        else:
            if raise_on_error:
                raise ValueError(
                    f"'{ds_item_id}' does not have a valid starter.")
            else:
                return None

        ds_name = parts[1]
        if ds_ref_type == DsRefType.DHIVE and not ObjectId.is_valid(ds_name):
            if raise_on_error:
                raise ValueError(f"Invalid ds_item_id: {ds_item_id}")
            else:
                return None
        return DsRef(ds_ref_type, ds_repo_id, ds_name)

    @classmethod
    def parse_one(cls, ds_item_id: Union[str, DsRef], raise_on_error: bool = True) -> Optional[DsRef]:
        return cls._parse(ds_item_id, raise_on_error)

    @classmethod
    def parse_as_list(cls, ds_item_ids: List[Union[str, DsRef]], raise_on_error: bool = True) -> List[DsRef]:
        return [cls._parse(ds_item_id, raise_on_error=raise_on_error) for ds_item_id in ds_item_ids]

    @classmethod
    def fmt(cls, ds_ref: DsRef) -> Optional[str]:
        if ds_ref.ref_type in (DsRefType.DSA, DsRefType.FILES):
            starter = cls._DSA_STARTER
        elif ds_ref.ref_type == DsRefType.DHIVE:
            starter = cls._DHIVE_STARTER
        else:
            raise NotImplementedError()
        if ds_ref.ref_type == DsRefType.FILES:
            return f"{starter}{ds_ref.files_id}|{ds_ref.ds_name}"
        else:
            return f"{starter}{ds_ref.proj_id}|{ds_ref.ds_name}"

    @classmethod
    def parse_as_groups(cls, ds_item_ids: List[str]) -> Dict[Union[int, ObjectId], List[str]]:
        result: Dict[Union[str, int, ObjectId], List[str]] = {}
        for ds_item_id in cls.parse_as_list(ds_item_ids):
            ds_repo_id = str(ds_item_id.ds_repo_id)
            if ds_repo_id in result.keys():
                result[ds_repo_id].append(ds_item_id.his_point_name)
            else:
                result[ds_repo_id] = [ds_item_id.his_point_name]
        return result


class DataEngineBase(object):

    def __init__(self,  accessor: Any, proj_id: str, point_names: List[str] = None, date_range: Optional[DateRange] = None):
        self.accessor = accessor
        self.proj_id = proj_id
        self.point_names = point_names
        self.date_range = date_range

    def get_history_tb(self) -> str:
        return f"proj_history_{self.proj_id}"

    def get_real_tb(self) -> str:
        return f"proj_rtdata_{self.proj_id}"

    def get_log_tb(self) -> str:
        return f"proj_log_{self.proj_id}"

    def load_history_data(self) -> pd.DataFrame:
        result = pd.DataFrame()
        if isinstance(self.accessor, MongoAccessor):
            query_match = {'time': MongoFunc.get_time_query_match(self.date_range.start_time, self.date_range.end_time, self.date_range.interval.value)}
            if self.point_names:
                query_match.update({'name': {'$in': self.point_names}})

            pipe: List = [{'$match': query_match},  # 过滤数据
                          {'$project': MongoFunc.get_time_projection_match(self.date_range.start_time, self.date_range.interval.value)},    # 修改输⼊⽂档的结构， 如重命名、 增加、 删除字段、 创建计算结果
                          {'$unwind': '$value'},    # 会把数组中的数据分多条数据，数组外公共数据相同
                          {'$sort': {'value.time': 1}},  # 将输⼊⽂档排序后输出
                          {'$match': MongoFunc.get_value_query_match(self.date_range.start_time, self.date_range.end_time, self.date_range.interval.value)},
                          {'$project': {'name': 1, 'value': '$value.value', 'time': '$value.time'}}
                          ]

            query_df = pd.DataFrame(self.accessor.aggr(self.get_history_tb(), pipe, allow_disk_use=True))
            if not query_df.empty:
                query_df = query_df.set_index(['time', 'name'])
                if not query_df.index.is_unique:
                    query_df = query_df[~query_df.index.duplicated(keep='first')]
                result = query_df.unstack().droplevel(level=0, axis=1)
        return result

    def write_history_data(self, data_df: pd.DataFrame) -> bool:
        if isinstance(self.accessor, MongoAccessor):
            data_df.reset_index(inplace=True)
            data: pd.Series = data_df.apply(lambda record: MongoFunc.convert_point_df(record), axis=1)
            self.accessor.mdbBb[self.get_history_tb()].bulk_write(data.to_list())
            self.accessor.mdbBb[self.get_history_tb()].create_index([('time', ASCENDING), ('name', ASCENDING)], unique=True)
            return True
        return False

    def del_history_data(self):
        if isinstance(self.accessor, MongoAccessor):
            query_match = {'time': MongoFunc.get_time_query_match(self.date_range.start_time, self.date_range.end_time, self.date_range.interval.value)}
            if self.point_names:
                query_match.update({'name': {'$in': self.point_names}})
            self.accessor.delete_many(self.get_history_tb(), query_match)

    def load_real_data(self) -> pd.DataFrame:
        df = pd.DataFrame()
        if isinstance(self.accessor, MySqlAccessor):
            sql = f"""SELECT time, name, value FROM {self.get_real_tb()} {f'''WHERE name in ('{"','".join(self.point_names)}')''' if self.point_names is not None and len(self.point_names) > 0 else ""}"""
            df = pd.read_sql(sql, con=self.accessor.get_conn(), index_col='name', coerce_float=True)
            if not df.empty:
                df['time'] = df['time'].apply(lambda time: datetime.strftime(time, '%Y-%m-%d %H:%M:%S'))
                df = df[~df.index.duplicated(keep='first')]
        return df

    def write_real_data(self, data_df: pd.DataFrame) -> bool:
        if isinstance(self.accessor, MySqlAccessor):
            data_df.reset_index(inplace=True)
            data_df.set_index('name', inplace=True)
            data_df.drop_duplicates(keep='last', inplace=True)
            data_df['value'] = data_df['value'].apply(lambda value: try_convert_value(value))
            data_df['time'] = data_df['time'].astype(str)

            create_tb = f"""CREATE TABLE IF NOT EXISTS {self.get_real_tb()} 
                            (`time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            `name` varchar(128) NOT NULL DEFAULT '',
                            `value` text,
                            PRIMARY KEY (`name`)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

            self.accessor.write_sql(create_tb)

            params_list = [tuple(item) for item in data_df.to_records()]
            self.accessor.write_sql_many(f'replace into {self.get_real_tb()} (name, time, value) values (%s,%s,%s)', params_list)
            return True
        return False

    def load_first_data_time(self) -> datetime:
        if isinstance(self.accessor, MongoAccessor):
            doc: Dict = self.accessor.mdbBb[self.get_history_tb()].find_one({}, sort=[("time", ASCENDING)])
            result: Optional[datetime] = None
            if doc:
                result = doc['time']
                time_group = list(self.accessor.mdbBb[self.get_history_tb()].find({"time": result}))
                min_item = min(time_group, key=lambda i: min(map(int, i["value"].keys())))
                min_hour = min(min_item["value"].keys(), key=lambda i: int(i))
                min_minute = min(min_item['value'][min_hour].keys(), key=lambda i: int(i))
                result += timedelta(hours=float(min_hour), minutes=float(min_minute))
            return result

    def write_data(self, data_df: pd.DataFrame) -> bool:
        if isinstance(self.accessor, MySqlAccessor):
            return self.write_real_data(data_df)
        elif isinstance(self.accessor, MongoAccessor):
            return self.write_history_data(data_df)
        return False

    def write_record(self, tb_name: str, records: list) -> bool:
        if isinstance(self.accessor, MongoAccessor):
            self.accessor.mdbBb[tb_name].bulk_write(MongoFunc.convert_insert_records(records))
            return True
        return False

    def write_log(self, records: list) -> bool:
        return self.write_record(self.get_log_tb(), records)

    def read_record(self, tb_name: str, start: Optional[datetime], end: Optional[datetime], page_index: Optional[int] = None, page_size: Optional[int] = None, sort_order: Optional[str] = None, **kwargs):
        if isinstance(self.accessor, MongoAccessor):
            finds = {'$query': {}, '$orderby': {'time': 1}}
            if isinstance(start, datetime):
                if 'time' not in finds['$query'].keys():
                    finds['$query']['time'] = {}
                finds['$query']['time']['$gte'] = start

            if isinstance(end, datetime):
                if 'time' not in finds['$query'].keys():
                    finds['$query']['time'] = {}
                finds['$query']['time']['$lte'] = end

            if len(kwargs) > 0:
                finds['$query'].update(kwargs)

            if sort_order == 'des':
                finds['$orderby'] = {'time': -1}
            cursor = self.accessor.mdbBb[tb_name].find(finds)
            if isinstance(page_index, int) and isinstance(page_size, int):
                page_index = page_index - 1 if page_index > 0 else page_index
                if page_index > 0:
                    cursor = cursor.skip(page_size * page_index)
                cursor = cursor.limit(page_size)
            return list(cursor)

    def delete_record(self, tb_name: str, start: Optional[datetime], end: Optional[datetime],  **kwargs) -> bool:
        if isinstance(self.accessor, MongoAccessor):
            if isinstance(start, datetime):
                if 'time' not in kwargs.keys():
                    kwargs['time'] = {}
                kwargs['time']['$gte'] = start

            if isinstance(end, datetime):
                if 'time' not in kwargs.keys():
                    kwargs['time'] = {}
                kwargs['time']['$lte'] = end

            self.accessor.mdbBb[tb_name].remove(kwargs)
            return True
        return False


class DataEngineFactory(object):

    @classmethod
    def get_engine_by_proj_id(cls, accessor: Any, proj_id: str, point_names: List[str] = None, date_range: Optional[DateRange] = None) -> Optional[DataEngineBase]:
        return DataEngineBase(accessor, proj_id, point_names, date_range)

    @classmethod
    def get_data_engines(cls, accessor: Any, point_names: List[str], date_range: Optional[DateRange] = None, proj_id: Optional[str] = None) -> Dict:
        results = {}
        if len(point_names) > 0:
            for proj_id, his_point_names in DsIdParser.parse_as_groups(point_names).items():
                if isinstance(proj_id, str) and proj_id not in results.keys():
                    engine = cls.get_engine_by_proj_id(accessor, proj_id, his_point_names, date_range)
                    if engine is not None:
                        results[proj_id] = engine
        else:
            if proj_id is not None:
                engine = cls.get_engine_by_proj_id(accessor, proj_id, point_names, date_range)
                if engine is not None:
                    results[proj_id] = engine
        return results


class DataStorage(object):

    @staticmethod
    def combine_series_func(old_series: pd.Series, new_series: pd.Series):
        old_series.update(new_series)
        return old_series

    @staticmethod
    def data_to_dataframe(data: List[List]) -> pd.DataFrame:
        data_df = pd.DataFrame(data, columns=['time', 'name', 'value'])
        data_df['value'] = data_df['value'].astype(str)
        data_df['value'] = data_df['value'].map(lambda value: try_convert_value(value))
        data_df['time'] = data_df['time'].astype('datetime64[ns]')
        data_df.set_index('time', inplace=True)
        data_df.sort_index(inplace=True)
        return data_df

    @staticmethod
    def dataframe_to_dict(df: pd.DataFrame, orient: str = 'tight') -> list:
        return df.to_dict(orient=orient)

    @classmethod
    def load_history_data(cls, accessor: Any, date_range: DateRange, point_names: List[str], proj_id: Optional[str] = None, need_dict: bool = True):
        date_index = pd.date_range(start=date_range.start_time, end=date_range.end_time, freq=date_range.interval.pandas_freq)
        ds_item_dict = {ds_ref.his_point_name: DsIdParser.fmt(ds_ref) for ds_ref in DsIdParser.parse_as_list(point_names)}
        data_df = pd.DataFrame(columns=ds_item_dict.keys(), index=(pd.Index(date_index, name='time')))
        for proj_id, engine in DataEngineFactory.get_data_engines(accessor, list(ds_item_dict.values()), date_range, proj_id).items():
            df = engine.load_history_data()
            if not df.empty:
                data_df = data_df.combine(df, func=DataStorage.combine_series_func, overwrite=False)
                del df
        data_df.replace(np.nan, None, inplace=True)
        data_df.index = pd.Series(data_df.index).apply(str)
        return cls.dataframe_to_dict(data_df) if need_dict else data_df

    @classmethod
    def load_realtime_data(cls, accessor: Any, point_names: List[str], need_dict: bool = True):
        ds_item_dict = {ds_ref.his_point_name: DsIdParser.fmt(ds_ref) for ds_ref in DsIdParser.parse_as_list(point_names)}
        data_df = pd.DataFrame(columns=['time', 'value'], index=pd.Index(ds_item_dict.keys(), name='name'))
        for proj_id, engine in DataEngineFactory.get_data_engines(accessor, point_names).items():
            df = engine.load_real_data()
            if not df.empty:
                data_df.update(df)
        data_df['value'] = data_df['value'].apply(lambda value: try_convert_value(value))
        data_df['time'].fillna('1900-01-01 00:00:00', inplace=True)
        data_df['error'] = data_df['value'].isnull()
        data_df.rename(index=ds_item_dict, inplace=True)
        data_df.index = pd.Series(data_df.index).apply(str)
        return cls.dataframe_to_dict(data_df) if need_dict else data_df

    @classmethod
    def save_data(cls, accessors: List, data: List[List], proj_id: str = '0'):
        data_df = cls.data_to_dataframe(data)
        for accessor in accessors:
            engine = DataEngineFactory.get_engine_by_proj_id(accessor=accessor, proj_id=proj_id)
            engine.write_data(data_df)

    @classmethod
    def save_log(cls, accessors: List, logs: list, proj_id: str = '0'):
        for accessor in accessors:
            DataEngineFactory.get_engine_by_proj_id(accessor=accessor, proj_id=proj_id).write_log(logs)

    @classmethod
    def read_log(cls, accessor: Any, start: Optional[datetime], end: Optional[datetime], page_index: Optional[int] = None, page_size: Optional[int] = None, sort_order: Optional[str] = None, proj_id: str = '0', need_dict: bool = True, **kwargs):
        engine = DataEngineFactory.get_engine_by_proj_id(accessor=accessor, proj_id=proj_id)
        records = engine.read_record(engine.get_log_tb(), start, end, page_index, page_size, sort_order, **kwargs)
        return cls.dataframe_to_dict(pd.DataFrame(records)) if need_dict else pd.DataFrame(records)

    @classmethod
    def del_log(cls, accessor: Any, start: Optional[datetime], end: Optional[datetime],proj_id: str = '0', **kwargs):
        engine = DataEngineFactory.get_engine_by_proj_id(accessor=accessor, proj_id=proj_id)
        return engine.delete_record(engine.get_log_tb(), start, end, **kwargs)