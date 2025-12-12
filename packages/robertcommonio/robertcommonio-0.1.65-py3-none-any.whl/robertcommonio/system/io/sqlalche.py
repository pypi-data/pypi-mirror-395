import re
from typing import Optional, Any, Union, List, Dict

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool.impl import QueuePool
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.declarative import declarative_base
from robertcommonbasic.basic.dt.utils import DATETIME_FMT_FULL, datetime


class SQLQueryBuilder:
    """SQL命令构建"""

    def __init__(self, **kwargs):
        self.is_oracle = kwargs.get('is_oracle', False)
        self.page_size = 0
        self.query = ""
        self.params = []

    def __str__(self):
        return self.build_query()

    def select(self, columns: Optional[Union[str, list, tuple, dict]] = None):
        """字段选择"""
        if columns is None:
            columns = '*'
        if isinstance(columns, str):
            self.query = f"{self.query} Select {columns}"
        elif isinstance(columns, list) or isinstance(columns, tuple):
            self.query = f"{self.query} Select {', '.join([str(col) for col in columns])}"
        elif isinstance(columns, dict):
            self.query = f"""{self.query} Select {', '.join([f"{col} AS {col_alias}" for col_alias, col in columns.items() if col is not None])}"""
        return self

    def from_table(self, tables: Union[str, list, dict]):
        """表"""
        if isinstance(tables, str):
            self.query = f"{self.query} From {tables}"
        elif isinstance(tables, list):
            self.query = f"{self.query} From {', '.join(tables)}"
        elif isinstance(tables, dict):
            self.query = f"{self.query} From {', '.join(f'{v} as {k}' for k, v in tables.items())}"
        return self

    def insert_into(self, table: str):
        """插入"""
        self.query = f"{self.query} Insert into {table}"
        return self

    def replace_into(self, table: str):
        """替换"""
        self.query = f"{self.query} Replace into {table}"
        return self

    def delete_from(self, table: str):
        """删除数据"""
        self.query = f"{self.query} delete from {table}"
        return self

    def drop(self, table: str, add_exists: bool = True):
        """删除表"""
        self.query = f"DROP TABLE {'IF EXISTS ' if add_exists else ''} `{table}`"
        return self

    def update(self, table: str):
        """更新数据"""
        self.query = f"{self.query} Update {table}"
        return self

    def values(self, values: Union[dict, list]):
        """插入数据字段"""
        if len(values) > 0:
            if isinstance(values, dict):
                if self.is_oracle is False:
                    self.query = f"{self.query} (`{'`, `'.join(values.keys())}`) Values ({', '.join(['%s'] * len(values))})"
                else:
                    self.query = f"{self.query} ({', '.join(values.keys())}) Values ({', '.join(['%s'] * len(values))})"
                self.params.extend(list(values.values()))
            elif isinstance(values, list):
                if self.is_oracle is False:
                    self.query = f"{self.query} (`{'`, `'.join(values[0].keys())}`) Values "
                else:
                    self.query = f"{self.query} ({', '.join(values[0].keys())}) Values "
                for value in values:
                    self.query = f"{self.query} ({', '.join(['%s'] * len(value))}),"
                    self.params.extend(list(value.values()))
                self.query = self.query[:-1]
        return self

    def set(self, values: dict):
        """更新数据字段"""
        self.query = f"{self.query} SET {', '.join([f'`{column}` = %s' if column.find('.') < 0 and self.is_oracle is False else f'{column} = %s' for column in values.keys()])}"
        self.params.extend([value for value in values.values()])
        return self

    def where(self, conditions: Union[str, dict], operator: str = "AND"):
        """过滤条件"""
        if isinstance(conditions, str) and len(conditions) > 0:
            self.query = f" {self.query} {'Where' if self.query.find('Where') <= 0 else operator} {conditions}"
        elif isinstance(conditions, dict) and len(conditions) > 0:
            conditions_with_params = []
            for column, condition in conditions.items():
                column = f"`{column}`" if column.find('.') < 0 and self.is_oracle is False else f"{column}"
                if isinstance(condition, dict):
                    condition_operator = condition["operator"].upper()
                    condition_value = condition["value"]
                    if condition_operator in ["IN", "NOT IN"]:
                        if not isinstance(condition_value, (list, tuple)):
                            raise ValueError("Value for IN operator must be a list or tuple")
                        if len(condition_value) > 0:
                            placeholders = ", ".join(["%s"] * len(condition_value))
                            conditions_with_params.append(f"{column} {condition_operator} ({placeholders})")
                            self.params.extend(condition_value)
                    elif condition_operator in ["IS NULL", "IS NOT NULL"]:
                        conditions_with_params.append(f"{column} {condition_operator}")
                    elif condition_operator in ['CONTAIN', 'LIKE']:
                        if isinstance(condition_value, str) and len(condition_value) > 0:
                            conditions_with_params.append(f"{column} like %s")
                            self.params.append(f"%%{condition_value}%%")
                    elif condition_operator in ['NOT CONTAIN', "NOT LIKE"]:
                        if isinstance(condition_value, str) and len(condition_value) > 0:
                            conditions_with_params.append(f"{column} not like %s")
                            self.params.append(f"%%{condition_value}%%")
                    elif condition_operator in ['RANGE', 'BETWEEN']:
                        if isinstance(condition_value, list) and len(condition_value) > 0:
                            conditions_with_params.append(f"{column} >= %s and {column} <= %s")
                            self.params.extend(condition_value)
                    elif condition_operator in ["=", "<", ">", "<=", ">=", "!=", 'IS']:
                        conditions_with_params.append(f"{column} {condition_operator} %s")
                        self.params.append(condition_value)
                    else:
                        raise ValueError(f"Invalid operator: {condition_operator}")
                else:
                    conditions_with_params.append(f"{column} = %s")
                    self.params.append(condition)
            if len(conditions_with_params) > 0:
                self.query = f" {self.query} {'Where' if self.query.find('Where') <= 0 else operator} {f' {operator} '.join(conditions_with_params)}"
        return self

    def having(self, havings):
        # self.query = f" {self.query} {f' {operator} '.join(conditions_with_params)}"
        # TODO
        return self

    def join(self, tables: Union[str, dict], on: Union[str, dict] = '', join_type: str = "INNER"):
        join_type = join_type.upper()
        if join_type == "" or join_type not in ["INNER", "LEFT OUTER", "RIGHT OUTER", "FULL OUTER", "CROSS"]:
            return self
        if not tables:
            return self
        if isinstance(tables, dict) or isinstance(tables, str):
            self.query = f" {self.query} {join_type} JOIN {self._prepare_aliases(tables)}"
        else:
            return self

        if on:
            if isinstance(on, str):
                self.query = f" {self.query} ON {on}"
            elif isinstance(on, dict):
                ons = []
                for field1, field2 in on.items():
                    ons.append(f" {field1} = {field2}")
                self.query = f" {self.query} ON {' AND '.join(ons)}"
            else:
                return self
        return self

    def group_by(self, columns: Union[str, list, tuple]):
        """分组"""
        self.query = f"{self.query} GROUP BY {','.join(columns) if isinstance(columns, (list, tuple)) else columns}"
        return self

    def order_by(self, orders: Optional[Union[str, dict]] = None):
        """排序"""
        if orders is not None and len(orders) > 0:
            if isinstance(orders, str):
                self.query = f"{self.query} ORDER BY {orders}"
            elif isinstance(orders, dict):
                order_by_clause = []
                for column, ascending in orders.items():
                    order_by_clause.append(f" {column} {ascending}")
                self.query = f"{self.query} ORDER BY {', '.join(order_by_clause)}"
            elif isinstance(orders, list):
                order_by_clause = []
                for (column, ascending) in orders:
                    order_by_clause.append(f" {column} {ascending}")
                self.query = f"{self.query} ORDER BY {', '.join(order_by_clause)}"
        return self

    def limit(self, limit: int):
        """限制"""
        if self.is_oracle is False:
            self.query = f"{self.query} Limit {limit}"
        else:
            self.page_size = limit
        return self

    def offset(self, offset: int):
        """偏移"""
        if self.is_oracle is False:
            self.query = f"{self.query} offset {offset}"
        else:
            self.query = f"{self.query} {'Where' if self.query.find('Where') <= 0 else 'and'} rownum>={offset} and rownum<{offset + self.page_size} "
        return self

    def build(self) -> tuple:
        return f"{self.query};", self.params

    def build_query(self) -> str:
        query_string = self.query
        if self.params:
            for param in self.params:
                if isinstance(param, str):
                    param = f"'{param}'"
                elif isinstance(param, datetime):
                    if self.is_oracle is True:
                        param = f"to_date('{param.strftime(DATETIME_FMT_FULL)}', 'YYYY-MM-DD HH24:MI:SS')"
                    else:
                        param = param.strftime(DATETIME_FMT_FULL)
                else:
                    param = str(param)
                query_string = query_string.replace("%s", 'NULL' if param in [None, 'None', 'NULL'] else param, 1)
        return f"{query_string}{';' if self.is_oracle is False else ''}"

    @staticmethod
    def sanitize_input(value):
        # Remove any SQL special characters that can be used for injection
        sanitized_value = re.sub(r"[;\\'\"]", '', value)
        return sanitized_value

    def _prepare_aliases(self, items: Union[str, list, dict], as_list: bool = False) -> Union[str, list]:
        if not items:
            return ""

        sql = []
        if isinstance(items, str):
            sql.append(items)
        elif isinstance(items, list) or isinstance(items, dict):
            for item in items:
                if isinstance(items, list):
                    if isinstance(item, str):
                        sql.append(item)
                    elif isinstance(item, dict):
                        first_item = list(item.values())[0]
                        alias = list(item.keys())[0]
                        sql.append(first_item if isinstance(alias, int) else f"{first_item} AS {alias}")
                elif isinstance(items, dict):
                    new_item = items[item]
                    sql.append(new_item if isinstance(item, int) else f"{new_item} AS {item}")
        else:
            return ""
        return self._prepare_fieldlist(sql) if not as_list else sql

    def _prepare_conditions(self, where: Union[str, list]) -> dict:
        result = {"sql": "", "values": []}
        sql = ""

        if not where:
            return result

        if isinstance(where, str):
            sql += where
        elif isinstance(where, list):
            for cond in where:
                if isinstance(cond, list):
                    if len(cond) == 2:
                        field = self._prepare_field(cond[0])
                        value = cond[1]

                        if isinstance(value, str) and value.lower() == "is null":
                            operator = "IS NULL"
                            sql += f"({field} {operator})"
                        elif isinstance(value, str) and value.lower() == "is not null":
                            operator = "IS NOT NULL"
                            sql += f"({field} {operator})"
                        elif isinstance(value, list) or isinstance(value, tuple):
                            operator = "IN"
                            values = ("?," * len(value)).rstrip(",")
                            sql += f"({field} {operator} ({values}))"
                            for item in value:
                                result["values"].append(item)
                        else:
                            operator = "="
                            sql += f"({field} {operator} ?)"
                            result["values"].append(value)
                    elif len(cond) == 3:
                        field = self._prepare_field(cond[0])
                        operator = cond[1].upper()
                        value = cond[2]
                        if operator in ["=", ">", "<", ">=", "<=", "!=", "LIKE", "NOT LIKE", "CONTAIN", "NOT CONTAIN", "IN", "NOT IN"]:
                            if operator == "IN" and (isinstance(value, list) or isinstance(value, tuple)):
                                values = ("?," * len(value)).rstrip(",")
                                sql += f"({field} {operator} ({values}))"
                                for item in value:
                                    result["values"].append(item)
                            else:
                                sql += f"({field} {operator} ?)"
                                result["values"].append(value)
                elif isinstance(cond, str):
                    upper = cond.upper()
                    if upper in ["AND", "OR", "NOT"]:
                        sql += f" {upper} "
        else:
            return result
        result["sql"] = sql
        return result

    def _prepare_field(self, field: str = "") -> str:
        if not field:
            return ""

        if field.find("(") > -1 or field.find(")") > -1 or field.find("*") > -1:
            if field.find(" AS ") > -1:
                field = field.replace(" AS ", " AS `")
                return f"{field}`"
            else:
                return field
        else:
            field = field.replace(".", "`.`")
            field = field.replace(" AS ", "` AS `")
            return f"`{field}`"

    def _prepare_fieldlist(self, fields: Union[str, tuple, list] = ()) -> str:
        result = ""
        if not fields:
            return result

        if isinstance(fields, str):
            result = self._prepare_field(fields)
        elif isinstance(fields, tuple) or isinstance(fields, list):
            fields = [self._prepare_field(field) for field in fields]
            result = ", ".join(fields)
        return result


class SQLAlCheAccessor:

    def __init__(self):
        self.engine: dict = {}
        self.engine_factory: dict = {}

    def add_engine(self, engine_name: str, engine_conn: str, engine_pool_class: Any = QueuePool, engine_pool_recycle: int = 300, text_factory: Optional[Any] = None, **kwargs):
        """
                添加一个数据库连接池
                quote_plus(psw)
                @Example:
                    PostgreSQL
                        # default
                        engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
                        # psycopg2
                        engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
                        # pg8000
                        engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')

                    MySQL
                        # default
                        engine = create_engine('mysql://scott:tiger@localhost/foo')
                        # mysqlclient (a maintained fork of MySQL-Python)
                        engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
                        # PyMySQL
                        engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')
                        # mysql+pymysql://root:XXX@localhost:3306/foo?charset=utf8

                    Oracle
                        engine = create_engine('oracle://scott:tiger@127.0.0.1:1521/sidname')
                        engine = create_engine('oracle+cx_oracle://scott:tiger@tnsname')

                    SQL Server
                        # pyodbc
                        engine = create_engine('mssql+pyodbc://scott:tiger@mydsn')
                        # pymssql
                        engine = create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')

                    SQLite
                        engine = create_engine('sqlite:///foo.db')  # 相对地址
                        engine = create_engine('sqlite:///C:\\path\\to\\foo.db')    # 绝对地址

            """
        if engine_name not in self.engine.keys():
            engine = create_engine(engine_conn, poolclass=engine_pool_class, pool_recycle=engine_pool_recycle, **kwargs)
            if engine:
                if text_factory is not None:
                    engine.raw_connection().connection.text_factory = text_factory
                    engine.connect().connection.connection.text_factory = text_factory
                self.engine_factory[engine_name] = text_factory
                self.engine[engine_name] = engine
        return self.engine.get(engine_name)

    def get_engine(self, engine_name: str):
        return self.engine.get(engine_name)

    def check_text_factory(self, engine_name: str, conn):
        text_factory = self.engine_factory.get(engine_name)
        if text_factory is not None and conn.connection.connection.text_factory != text_factory:
            conn.connection.connection.text_factory = text_factory

    def to_dict(self, records: Union[List[Optional[Dict]], Dict]):
        if isinstance(records, Dict):
            return {k: v for k, v in records.items()}
        elif isinstance(records, List):
            return [{k: v for k, v in record.items()} for record in records]

    def read_sql(self, engine_name: str, sql_cmd: str, to_dict: bool = True, case_sensitive: Optional[str] = None) -> list:
        with self.get_engine(engine_name).connect() as conn:
            self.check_text_factory(engine_name, conn)
            if case_sensitive is None:
                records = conn.execute(sql_cmd).mappings().all()
                if to_dict is True:
                    return self.to_dict(records)
                return records
            else:
                cursor = conn.execute(sql_cmd).cursor
                if case_sensitive == 'lower':
                    return [dict(zip([str(field[0]).lower() for field in cursor.description], d)) for d in cursor.fetchall()]
                elif case_sensitive == 'upper':
                    return [dict(zip([str(field[0]).upper() for field in cursor.description], d)) for d in cursor.fetchall()]
                return [dict(zip([field[0] for field in cursor.description], d)) for d in cursor.fetchall()]

    def read_sql_dataframe(self, engine_name: str, sql_cmd: str):
        with self.get_engine(engine_name).connect() as conn:
            self.check_text_factory(engine_name, conn)
            return pd.read_sql_query(sql_cmd, conn)

    def execute_sql(self, engine_name: str, sql_cmd: str, params: Optional[list] = None):
        with self.get_engine(engine_name).connect() as conn:
            result = conn.execute(text(sql_cmd), params)
            if str(conn.engine.driver).lower().find('oracle') < 0:
                if result.lastrowid > 0:
                    return result.lastrowid
            return result.rowcount

    def execute_update_sql(self, engine_name: str, sql_cmd: str, params: Optional[list] = None) -> int:
        with self.get_engine(engine_name).connect() as conn:
            result = conn.execute(text(sql_cmd), params)
            if str(conn.engine.driver).lower().find('oracle') < 0:
                if result.lastrowid > 0:
                    return result.lastrowid
            return result.rowcount

    def execute_multi_sql(self, engine_name: str, cmd_tuple: list):
        with self.get_engine(engine_name).begin() as conn:
            rowcount = 0
            for cmd in cmd_tuple:
                rowcount = conn.execute(text(cmd[0]), cmd[1]).rowcount + rowcount
            return rowcount

    def get_table_struct(self, engine_name: str, table_name: str):
        engine = self.get_engine(engine_name)
        if engine is not None:
            base = declarative_base()
            base.metadata.reflect(engine)
            # 获取原表对象
            old_table = base.metadata.tables[table_name]
            # 获取原表建表语句
            crate_sql = str(CreateTable(old_table))
            base.metadata.clear()
            return crate_sql
        return None

    def generate_sql_format(self, table_name: str, action: str = 'replace', colums: Optional[list] = None, filter_column: Optional[list] = None, add_syntax: bool = False):
        insert_fmt = '{}' if add_syntax is False else '`{}`'
        insert_value_fmt = ':{}'
        updte_value_fmt = '{} = :{}' if add_syntax is False else '`{}` = :{}'
        if action in ['replace', 'append']:
            return f"insert into {table_name} ({', '.join(insert_fmt.format(k) for k in colums)}) VALUES ({', '.join(insert_value_fmt.format(k) for k in colums)})"
        elif action == 'update':
            return f"update {table_name} set {', '.join(updte_value_fmt.format(k, k) for k in colums)} where {', and '.join(updte_value_fmt.format(k, k) for k in filter_column)}"
        elif action == 'delete':
            return f"delete from {table_name} where {', and '.join(updte_value_fmt.format(k, k) for k in filter_column)}"

    def generate_sql_cmds(self, table_name: str, records: list, action: str = 'replace', colums: list = None, filter_column: list = None, add_syntax: bool = False):
        cmds = []
        if len(records) > 0:
            if action == 'replace':
                if filter_column is None:
                    cmds.append((f"delete from {table_name}", None))
                else:
                    cmds.append((self.generate_sql_format(table_name, 'delete', None, filter_column), records))
            cmds.append((self.generate_sql_format(table_name, action, records[0].keys() if colums is None else colums, filter_column, add_syntax), records))
        return cmds

    def copy_table_struct(self, engine_name: str, table_name: str, new_table_name: str):
        crate_sql = self.get_table_struct(engine_name, table_name)
        if crate_sql is not None:
            return self.execute_sql(engine_name, crate_sql.replace("CREATE TABLE " + table_name, "CREATE TABLE if not exists " + new_table_name))

    def syn_table_record(self, engine_name: str, sql_cmd: str, engine_name_new: str, table_name_new: str,  if_exists: str = 'replace'):
        engine = self.get_engine(engine_name)
        engine_new = self.get_engine(engine_name_new)
        if engine and engine_new:
            pd.read_sql(sql_cmd, engine).to_sql(table_name_new, engine_new, if_exists=if_exists)
            return True
        return False
