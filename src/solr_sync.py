#!/usr/local/env python
# encoding:utf8

import config
import logging
import requests
import json
import MySQLdb
import subprocess
import os


class SolrSync(object):
    def __init__(self):
        logging.basicConfig(filename=config.file_path,
                            level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self._solr_config = config.solr_config
        self._mysql_config = config.mysql_config
        self.mysql_column_solr_index_mapping = config.mysql_column_solr_index_mapping

    def post_data_to_search_engine(self, schema, host, port, path, data, headers={'Content-type': 'application/json'}):
        url = schema + "://" + host + ":" + str(port) + path + "/update?commit=true"
        header_content_type = headers.get("Content-type")
        if header_content_type and header_content_type != "application/json":
            headers["Content-type"] = "application/json"
        post_data = json.dumps(data)
        r = requests.post(url, post_data, headers=headers)
        return r.json()

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
            self.post_data_to_search_engine(self._solr_config.get("schema"), self._solr_config.get("host"),
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
        self.post_data_to_search_engine(self._solr_config.get("schema"), self._solr_config.get("host"),
                                        self._solr_config.get("port"), self._solr_config.get("path"), post_data)

    def start(self):
        conn = MySQLdb.connect(**self._mysql_config)
        self._first_sync_data_to_solr(conn)

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



    def binlog_listener(self):
        pass



if __name__ == "__main__":
    solr = SolrSync()
    data = {
        "add": {
            "doc": {
                "fid": 1234,
                "fsid": 1234,
                "name": "yctest"
            }
        }
        # "delete":{"id":1234}
    }
    result = solr.post_data_to_search_engine(config.solr_config["schema"],
                                             config.solr_config["host"],
                                             config.solr_config["port"],
                                             config.solr_config["path"],
                                             data)
    print result
