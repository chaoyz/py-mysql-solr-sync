#!/usr/local/env python
# coding:utf8

import db_abstract
import MySQLdb
from pymysqlreplication import BinLogStreamReader


class MysqlData(db_abstract):

    def __init__(self, mysql_config, logger):
        self._mysql_config = mysql_config
        self._logger = logger
        pass

    def get_table_information(self, conn, table_name):
        pass