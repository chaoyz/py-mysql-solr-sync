#!/usr/local/env python
# encoding:utf8

import ConfigParser
import json
import logging
import os
import subprocess

import MySQLdb
import requests
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent

import config


class SolrSync(object):
    binlog_file = None
    binlog_pos = None

    def __init__(self):
        logging.basicConfig(filename=config.file_path,
                            level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self._solr_config = config.solr_config
        self._mysql_config = config.mysql_config
        self.mysql_column_solr_index_mapping = config.mysql_column_solr_index_mapping
        self._mysql_binlog_info_file = config.mysql_binlog_info_file
        if os.path.exists(config.mysql_binlog_info_file):
            with open(config.mysql_binlog_info_file, "r") as f:
                conf = ConfigParser.ConfigParser()
                conf.read(f)
                if conf.has_section("info"):
                    file_value = conf.get("info", "binlog_file")
                    if file_value:
                        self.binlog_file = file_value
                    pos_value = conf.get("info", "binlog_pos")
                    if pos_value:
                        self.binlog_pos = pos_value

    def _post_data_to_search_engine(self, schema, host, port, path, data, headers={'Content-type': 'application/json'}):
        url = schema + "://" + host + ":" + str(port) + path + "/update?commit=true"
        header_content_type = headers.get("Content-type")
        if header_content_type and header_content_type != "application/json":
            headers["Content-type"] = "application/json"
        post_data = json.dumps(data)
        r = requests.post(url, post_data, headers=headers)
        if r.status_code != 200:
            raise Exception("post data response not 200! data:%s" % r.content)
        result = r.json()
        if result['responseHeader']['status'] != 0:
            raise Exception("post data response not ok! data:%s" % result)
        self._save_binlog_info()
        return result

    def _first_sync_data_to_solr(self, conn):
        # get table columns
        columns = self.get_table_information(conn, config.table)
        post_solr_docs = []
        start = 0
        count = 10000
        has_more_data = True
        while has_more_data:
            rows = self.select_table_data(conn, config.table, columns, start, count)
            for row in rows:
                add_doc = {}
                for i, value in enumerate(row):
                    key = self.mysql_column_solr_index_mapping.get(columns[i])
                    if key:
                        add_doc[key] = value
                # post to solr
                post_solr_docs.append(add_doc)
            self._post_data_to_search_engine(self._solr_config.get("schema"), self._solr_config.get("host"),
                                            self._solr_config.get("port"), self._solr_config.get("path"), post_solr_docs)
            if len(rows) <= 0:
                has_more_data = False
            else:
                start = start + count

    def get_table_information(self, conn, table):
        columns = []
        sql = 'SELECT `COLUMN_NAME` FROM INFORMATION_SCHEMA.`COLUMNS` WHERE `TABLE_SCHEMA`="%s" AND `TABLE_NAME`="%s"' % (
            self._mysql_config.get("db"), config.table)
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                columns.append(row[0])
            return columns
        except Exception, e:
            self.logger.error("get_table_information sql exception", e)

    def select_table_data(self, conn, table_name, fields, start, count):
        columns = ""
        for index, field in enumerate(fields):
            columns = columns + " %s" % field
            if index != len(fields) - 1:
                columns = columns + ","

        sql = 'SELECT %s FROM %s LIMIT %s, %s' % (columns, table_name, start, count)
        try:
            columns = []
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                columns.append(row)
            return columns
        except Exception, e:
            self.logger.error("select_table_data sql exception", e)

    def detele_all_index(self):
        post_data = {"delete":{"query":"*:*"}}
        self._post_data_to_search_engine(self._solr_config.get("schema"), self._solr_config.get("host"),
                                        self._solr_config.get("port"), self._solr_config.get("path"), post_data)

    # do nothing
    def _find_binlog_file_postion(self):
        cmd = "mysql -u%s -p%s -e 'show master status\G'" % (self._mysql_config.get("user"), self._mysql_config.get("passwd"))
        result = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=os.open("devnull", "w"),
                                  close_fds=True)
        log_file_pos = {}
        for line in result.stdout.readlines():
            if line == 'File':
                log_file_pos["File"] = line
            elif line == 'Position':
                log_file_pos["Position"] = line

    def _binlog_info(self):
        if self._is_binlog_data():
            resume_stream = True
            self.logger.info("Resume from binlog_file: {file}  binlog_pos: {pos}".format(file=self.log_file,
                                                                                     pos=self.log_pos))
        else:
            resume_stream = False

        stream = BinLogStreamReader(connection_settings=self._mysql_config,
                                    server_id=config.mysql_server_id,
                                    only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
                                    only_tables=[config.table],
                                    resume_stream=resume_stream,
                                    blocking=True,
                                    log_file=self.binlog_file,
                                    log_pos=self.binlog_pos)
        for binlog_event in stream:
            self.binlog_file = stream.log_file
            self.binlog_pos = stream.log_pos
            for row in binlog_event.rows:
                # row is a list, every element is a map.
                result = {}
                if isinstance(binlog_event, DeleteRowsEvent):
                    result['delete'] = {"delete":self._load_delete_data(row)}
                elif isinstance(binlog_event, UpdateRowsEvent) or isinstance(binlog_event, WriteRowsEvent):
                    result['update'] = self._load_index_update_data(row)
                else:
                    self.logger.error("not handle event type.")
                    raise TypeError('not handle event type.')
                yield result
        stream.close()
        raise IOError('mysql connection closed')

    def _load_delete_data(self, row):
        list = []
        mysql_main_key = self.mysql_column_solr_index_mapping.keys()[0]
        for row_values in row.values():
            list.append(row_values[mysql_main_key])
        return list

    def _load_index_update_data(self, row):
        list = []
        for values in row.values():
            doc = {}
            for k, v in self.mysql_column_solr_index_mapping.items():
                doc[v] = values[k]
            list.append(doc)
        return list

    def _is_binlog_data(self):
        result = bool(self.binlog_file and self.binlog_pos)
        return result

    def _save_binlog_info(self):
        with open(self._mysql_binlog_info_file, "w+") as f:
            c = ConfigParser.ConfigParser()
            c.read(f)
            if not c.has_section("info"):
                c.add_section("info")
            c.set("info", "binlog_file", self.binlog_file)
            c.set("info", "binlog_pos", self.binlog_pos)
            c.write(f)

    def run(self, first_sync=False):
        '''

        :return:
        '''
        # 第一次同步数据
        if first_sync:
            conn = MySQLdb.connect(**self._mysql_config)
            self._first_sync_data_to_solr(conn)

        # 增量
        docs = self._binlog_info()
        for doc in docs:
            for k, v in doc.items():
                self.logger.info('%s:%s' % (k, v))
                self._post_data_to_search_engine(config.solr_config["schema"],
                                                 config.solr_config["host"],
                                                 config.solr_config["port"],
                                                 config.solr_config["path"],
                                                 v)

if __name__ == "__main__":
    solr = SolrSync()
    solr.run(False)
