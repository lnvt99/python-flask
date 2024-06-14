import time
import psycopg2
import os
from psycopg2.extras import DictCursor
from config import config
from common.logger import Logger


class DAL:
    """Data access Layer class."""

    def __init__(self, autocommit: bool):
        """_summary_

        Args:
            autocommit (bool): _ Whether to auto-commit.
        """
        self.__logger = Logger().setup_logging()
        self.__autocommit = autocommit
        self.__con = self.__get_connection()
        self.__con.autocommit = autocommit
        self.__SET_TIMEOUT = "SET statement_timeout TO {0}".format(
            os.environ.get('TIMEOUT')
        )

    def __del__(self):
        """
        Destructor.
        -----
        This destructor closes the DB connection.
        """
        if self.__autocommit == False:
            self.__con.rollback()
        self.close_connection()

    def execute_select_one(self, sql: str, params: dict):
        """
        Execute select SQL and fetch one result.

        Args:
            sql (str): sql string
            params (dict): parameter dict

        Returns:
            [dict]: return one row result
        """

        with self.__con.cursor(cursor_factory=DictCursor) as dict_cur:
            self.__logger.info(sql)
            self.__logger.info(params)
            start_time = time.time()

            dict_cur.execute(self.__SET_TIMEOUT)
            dict_cur.itersize = config.co.CURSOR_ITERSIZE
            # callproc(self, procname, vars=None)
            dict_cur.callproc(sql, params)

            # Log output SQL processing time
            end_time = time.time()
            self.__logger.debug(
                "SQL processing time:{0} s".format(end_time - start_time)
            )

            row = dict_cur.fetchone()
            if row is None:
                row = {}

        return dict(row)

    def execute_select_all(self, sql: str, params: dict):
        """
         Execute select SQL and fetch all result.

        Args:
            sql (str): sql string
            params (dict): parameter dict

        Returns:
            [array]: return results
        """
        with self.__con.cursor(cursor_factory=DictCursor) as dict_cur:
            self.__logger.info(sql)
            self.__logger.info(params)
            start_time = time.time()

            dict_cur.execute(self.__SET_TIMEOUT)
            dict_cur.itersize = config.co.CURSOR_ITERSIZE
            dict_cur.callproc(sql, params)

            end_time = time.time()
            self.__logger.info(
                "SQL processing time:{0} s".format(end_time - start_time)
            )

            rows = dict_cur.fetchall()

            dict_results = []
            for row in rows:
                dict_results.append(dict(row))

        return dict_results

    def execute_query(self, sql: str):
        """
        Execute insert/update/delete SQL.

        Args:
            sql (str): sql string
            params (dict): dictionary of parameter
        """

        with self.__con.cursor() as cur:
            self.__logger.info(sql)
            start_time = time.time()

            data = cur.execute(sql)

            end_time = time.time()
            self.__logger.info(
                "SQL processing time:{0} s".format(end_time - start_time)
            )
            return data

    def close_connection(self):
        """
        Close DB connection.
        """
        if self.__con is not None:
            self.__logger.info(
                "Start DB connection close processing"
            )  # DB接続クローズ処理開始
            self.__con.close()
            self.__logger.info(
                "DB connection close processing ends"
            )  # DB接続クローズ処理終了

    def rollback(self):
        """
        Roll back DB update.
        """
        if self.__con is not None:
            self.__logger.info("Start DB rollback processing")  # DBロールバック処理開始
            self.__con.rollback()
            self.__logger.info("DB rollback processing end")  # DBロールバック処理終了

    def commit(self):
        """
        Commit the DB update.
        """
        if self.__con is not None:
            self.__logger.info("Start DB commit processing")  # DBコミット処理開始
            self.__con.commit()
            self.__logger.info("DB commit processing end")  # DBコミット処理終了

    def reopen(self):
        """
        reopen connection
        """
        self.close_connection()
        self.__con = self.__get_connection()

    def __get_connection(self):
        """
        Get DB connection information from config file and return DB connection.

        Returns:
            [Object]: Object connection
        """
        # config for server
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT')
        db_name = os.environ.get('DB_NAME')
        db_username = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASSWORD')

        self.__logger.info(
            "Start DB connection open processing"
        )  # DB接続オープン処理開始

        connection = psycopg2.connect(
            "host={0} port={1} dbname={2} user={3} password={4}".format(
                db_host, db_port, db_name, db_username, db_password
            )
        )

        self.__logger.info(
            "DB connection open processing ends"
        )  # DB接続オープン処理終了

        return connection
