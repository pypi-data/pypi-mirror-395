import logging
import threading
import time
from datetime import datetime, timedelta
from typing import (Any, Callable, Dict, NoReturn, Optional, Sequence, Tuple,
                    TypeVar)

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.connections import Connection as MySqlConnection
from pymysql.cursors import Cursor as MySQLCursor


class MySqlAccessor:

    class ConnectionPoolInfo:
        def __init__(self, pool: PooledDB, last_active_time: datetime, pool_id: str = None):
            self.pool = pool
            self.last_active_time = last_active_time
            self.pool_id = pool_id

    class RecycleThread(threading.Thread):
        def __init__(self, max_idle_duration: timedelta):
            threading.Thread.__init__(self, daemon=True)
            self.max_idle_duration = max_idle_duration

        def run(self):
            while (True):
                try:
                    time.sleep(self.max_idle_duration.total_seconds() / 2)
                    MySqlAccessor._recycle_idle_pools(self.max_idle_duration)
                except:
                    logging.error('Failed to recycle idle connection pools',
                                  exc_info=True)

    _lock = threading.Lock()
    _pool_size = 10
    _max_idle_duration_seconds = 180
    _pool_recycle_thread = None
    _pools: Dict[Any, ConnectionPoolInfo] = {}

    def __init__(self, host: str, port: int, user: str, pwd: str, db: str = None):
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd
        self._db_name = db

    @classmethod
    def _recycle_idle_pools(cls, max_conn_age: timedelta):
        with cls._lock:
            now = datetime.now()
            recycled = {}
            for k, pi in cls._pools.items():
                if now - pi.last_active_time > max_conn_age and \
                        pi.pool._connections == 0:
                    recycled[k] = pi
            if recycled:
                cls._pools = {k: pi for k,
                              pi in cls._pools.items() if k not in recycled}
                for pi in recycled.values():
                    pi.pool.close()
                    logging.debug(f'connection pool recycled: {pi.pool_id}')

    def _get_pool(self) -> PooledDB:
        key = (self._host, self._port, self._user, self._pwd)
        pool_info = MySqlAccessor._pools.get(key)
        if not pool_info:
            pool = PooledDB(creator=pymysql,
                            maxconnections=self._pool_size,
                            maxcached=3,
                            host=self._host,
                            port=self._port,
                            user=self._user,
                            password=self._pwd,
                            connect_timeout=60,
                            read_timeout=120,
                            write_timeout=120)
            pool_info = MySqlAccessor.ConnectionPoolInfo(
                pool, datetime.now(), f'{self._host}:{self._port}-{hex(id(pool))}')
            logging.debug(f'connection pool created: {pool_info.pool_id}')
            MySqlAccessor._pools[key] = pool_info

            # start connection pool recycle thread as needed
            if not MySqlAccessor._pool_recycle_thread:
                MySqlAccessor._pool_recycle_thread = MySqlAccessor.RecycleThread(
                    timedelta(seconds=MySqlAccessor._max_idle_duration_seconds))
                MySqlAccessor._pool_recycle_thread.start()

        else:
            pool_info.last_active_time = datetime.now()

        return pool_info.pool

    def get_conn(self, db_name: Optional[str] = None) -> MySqlConnection:
        return self._get_conn(db_name)

    def _get_conn_from_pool(self, database: str):
        conn = None
        try:
            with MySqlAccessor._lock:
                pool = self._get_pool()
                conn = pool.connection()
                if database:
                    conn._con._con.select_db(database)
        except:
            logging.warning(
                f'Failed to get connection from pool', exc_info=True, stack_info=True)

        return conn

    def _get_conn(self, db_name: str) -> MySqlConnection:
        try:
            db_name = db_name or self._db_name
            conn = self._get_conn_from_pool(db_name)
            if not conn:
                conn = pymysql.connect(host=self._host,
                                       port=self._port,
                                       user=self._user,
                                       password=self._pwd,
                                       database=db_name)
            return conn
        except Exception:
            logging.critical('Failed to get mysql connection', exc_info=True)
            raise

    T = TypeVar('T')

    def _execute(self,
                 db_name: str,
                 f: Callable[[MySQLCursor], T]) -> T:
        conn = None
        cursor = None
        try:
            conn = self._get_conn(db_name)
            cursor = conn.cursor()
            dbrv = f(cursor)
            conn.commit()
            return dbrv
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def write_sql(self,
                  sql: str,
                  params: Optional[Tuple] = None,
                  db_name: str = None
                  ) -> NoReturn:
        logging.debug(f'sql write: {sql}, db: {db_name}')
        return self._execute(
            db_name, lambda cursor: cursor.execute(sql, params))

    def write_sql_many(self,
                       sql: str,
                       params_list: Sequence[Optional[Tuple]],
                       db_name: str = None
                       ) -> NoReturn:
        logging.debug(f'sql write: {sql}, db: {db_name}')
        return self._execute(
            db_name, lambda cursor: cursor.executemany(sql, params_list))

    def read_sql(self,
                 sql: str,
                 params: Optional[Tuple] = None,
                 db_name: str = None) -> Tuple[Tuple, ...]:
        logging.debug(f'sql read: {sql}, db: {db_name}')

        def _execute_sql(cursor: MySQLCursor) -> Tuple[Tuple, ...]:
            cursor.execute(sql, params)
            return cursor.fetchall()

        return self._execute(db_name, _execute_sql)