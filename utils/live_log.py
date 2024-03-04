# -*- coding: utf-8 -*-
"""
    Created by w at 2024/2/21.
    Description:
    Changelog: all notable changes to this file will be documented
"""
import io
import time
import logging as logger
from datetime import datetime
from io import StringIO
from threading import BoundedSemaphore
import psycopg2
from psycopg2.extensions import TRANSACTION_STATUS_UNKNOWN, TRANSACTION_STATUS_IDLE
from psycopg2.pool import SimpleConnectionPool
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from threading import Lock
import pandas as pd

from utils.decorator import singleton
from config import Config


class BasePostgreSQL(object):
    WAIT_TIME = [0, 3, 60, 180, 1800]

    def __init__(self, field, conf=None, readonly=False):
        self.field = field
        self.conf = conf
        self.readonly = readonly
        self.conn_pool = None
        self.max_jobs = None

    def init(self):
        self.conn_pool = SimpleConnectionPool(
            1,
            self.conf["pool_size"],
            database=self.conf["db_name"],
            host=self.conf["host"],
            port=self.conf["port"],
            user=self.conf["user"],
            password=self.conf["password"],
        )
        self.max_jobs = BoundedSemaphore(self.conf["pool_size"])

    def get_engine(self):
        url = f"postgresql://{self.conf['user']}:{self.conf['password']}@{self.conf['host']}:{self.conf['port']}/{self.conf['db_name']}"
        return create_engine(url)

    def connect(self):
        conn = self.conn_pool.getconn()
        # 从连接池拿出的连接可能闲置太久超时，连接已经被服务端释放
        if not conn.closed:
            status = conn.get_transaction_status()
            if status == TRANSACTION_STATUS_UNKNOWN:
                self.conn_pool.putconn(conn, close=True)
                return self.connect()
            elif status != TRANSACTION_STATUS_IDLE:
                conn.rollback()
                return conn
            else:
                return conn
        self.conn_pool.putconn(conn, close=True)
        return self.connect()

    def _exec(self, func, sql):
        """嵌套避免出现连接池耗尽"""
        try:
            self.max_jobs.acquire()
            return self._exec_retry(func, sql)
        except Exception as e:
            logger.error(f"_exec sql fail", exc_info=e, extra={"sql": sql})
        finally:
            self.max_jobs.release()

    def _exec_retry(self, func, sql, retry=0):
        """嵌套重试封装"""
        conn = None
        try:
            conn = self.connect()
            conn.set_session(autocommit=True)
            if func == "execute_pd":

                return pd.read_sql(sql, conn, coerce_float=False)
            cursor = conn.cursor()
            cursor.execute(sql)
            if func == "execute":
                return
            return getattr(cursor, func)()
        except psycopg2.ProgrammingError:
            raise
        except Exception as e:
            msg = str(e)
            if (
                msg.startswith("permission")
                or msg.startswith("operator")
                or msg.startswith("syntax error")
                or msg.startswith("Execution failed")
            ):
                raise
            logger.error(f"{func} sql fail", exc_info=e, extra={"sql": sql})
            if retry >= len(self.WAIT_TIME):
                return
            self.conn_pool.putconn(conn)
            conn = None
            time.sleep(self.WAIT_TIME[retry])
            return self._exec_retry(func, sql, retry + 1)
        finally:
            if conn:
                try:
                    self.conn_pool.putconn(conn)
                except Exception:
                    pass

    def execute(self, sql):
        return self._exec("execute", sql)

    def fetchone(self, sql):
        return self._exec("fetchone", sql)

    def fetchall(self, sql):
        return self._exec("fetchall", sql)

    def execute_pd(self, sql):
        return self._exec("execute_pd", sql)

    def execute_pd_copy(self, sql, retry=0):
        sql_copy = f"COPY ({sql}) TO STDOUT WITH DELIMITER ',' CSV HEADER"
        conn = None
        try:
            import pandas as pd

            conn = self.connect()
            cursor = conn.cursor()
            with StringIO() as f:
                cursor.copy_expert(sql_copy, f)
                with StringIO(f.getvalue()) as w:
                    res = pd.read_csv(w, sep=",", na_filter=False)
            for column in res.columns:
                if column in ["log_date", "reg_date"]:
                    res[column] = res[column].apply(
                        lambda x: datetime.strptime(x, "%Y-%m-%d")
                    )
                if column in ["order_time", "log_time"]:
                    res[column] = res[column].apply(
                        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
                    )
            return res
        except Exception as e:
            logger.error(f"execute_pd_copy sql fail", exc_info=e, extra={"sql": sql})
            if retry >= len(self.WAIT_TIME):
                return
            self.conn_pool.putconn(conn)
            conn = None
            time.sleep(self.WAIT_TIME[retry])
            return self.execute_pd_copy(sql, retry + 1)
        finally:
            if conn:
                try:
                    self.conn_pool.putconn(conn)
                except Exception:
                    pass


mutex = Lock()


class DBDws(BasePostgreSQL):

    def __init__(self, field, conf=None, readonly=False):
        """
        dws产品数据库dwd层数据连接
        :param field: 游戏ID
        :param conf:
        :param readonly:
        """
        super().__init__(field, conf, readonly)
        if not conf:
            conf = Config().db_dws(self.field)
        self.conf = conf
        self.init()


@singleton
class DBDwsManage:
    client_map = dict()

    def client(self, game_id, readonly=False):
        mutex.acquire()
        if not self.client_map.get(game_id):
            self.client_map[game_id] = DBDws(game_id, readonly=readonly)
        mutex.release()
        return self.client_map[game_id]


class LiveLog(object):
    def __init__(self, game_id: int, conn_pool=None):
        self.db_dws_manage = conn_pool or DBDwsManage().client(game_id)

    def read_live_info(
        self, platform: str, start_time: datetime = None, end_time: datetime = None
    ):
        end_time: datetime = end_time or datetime.now()
        start_time: datetime = start_time or end_time + timedelta(minutes=-30)
        sql: str = f"""SELECT * FROM dwd_live_info
        WHERE platform = '{platform}' AND create_time BETWEEN '{start_time}' AND '{end_time}' 
        """
        print(sql)
        data = self.db_dws_manage.execute_pd(sql)
        return data

    def read_live_chat(
        self, platform: str, start_time: datetime = None, end_time: datetime = None
    ):
        end_time: datetime = end_time or datetime.now()
        start_time: datetime = start_time or end_time + timedelta(minutes=-30)
        sql: str = f"""SELECT * FROM dwd_live_chat
        WHERE  platform = '{platform}' AND create_time BETWEEN '{start_time}' AND '{end_time}' 
        """
        print(sql)
        data = self.db_dws_manage.execute_pd(sql)
        return data

    def write_chat(self, data):
        table = "dwd_live_chat"
        if isinstance(data, list):
            data = pd.DataFrame(data)
        elif isinstance(data, dict):
            data = pd.DataFrame([data])

        columns = ", ".join(data.columns)
        values = ", ".join(
            [
                f"""({', '.join([str(val) if not isinstance(val, (str, datetime)) else f"'{val}'"  for val in row.values])})"""
                for _, row in data.iterrows()
            ]
        )

        sql = f"INSERT INTO {table} ({columns}) VALUES {values};"
        # print(sql)
        self.db_dws_manage.execute(sql=sql)

    def write_chat_word(self, data, log_date, platform):
        table = "dwd_live_chat_word"
        if isinstance(data, list):
            data = pd.DataFrame(data)
        elif isinstance(data, dict):
            data = pd.DataFrame([data])
        sql = f"""DELETE FROM {table} WHERE platform = '{platform}' AND log_date = '{log_date}'"""
        print(sql)
        self.db_dws_manage.execute(sql=sql)
        data["log_date"] = log_date
        data["platform"] = platform
        self.db_dws_manage.write_to_table(df=data, table_name=table)
