#!/usr/local/env python
# coding:utf8

import json
import requests
import solr_sync
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent

def test_index_doc():
    url ='http://127.0.0.1:8081/solr/fileindex/update/json?commit=true'
    head = {'Content-type':'application/json'}
    list = [{
        'fid':123,
        'fsid':123,
        'name':'yctest'
    }]
    data = json.dumps(list)
    print data
    r = requests.post(url=url, data=data, headers=head)
    print r.status_code
    print r.json()

def test_update_doc():
    url ='http://127.0.0.1:8081/solr/fileindex/update/json?commit=true'
    head = {'Content-type':'application/json'}
    list = [{
        'fid':123,
        'fsid':456,
        'name':'yctest'
    }]
    data = json.dumps(list)
    print data
    r = requests.post(url=url, data=data, headers=head)
    print r.status_code
    print r.json()

def test_delete_doc():
    url ='http://127.0.0.1:8081/solr/fileindex/update/json?commit=true'
    head = {'Content-type':'application/json'}
    # list = [{
    #     'fid':123
    # }]
    map = {
        "delete": {"id":123}
    }
    data = json.dumps(map)
    print data
    r = requests.post(url=url, data=data, headers=head)
    print r.status_code
    print r.json()

def test_index_doc_2():
    url ='http://127.0.0.1:8081/solr/fileindex/update/json?commit=true'
    head = {'Content-type':'application/json'}
    # list = [{
    #     'fid':123
    # }]
    map = {
        "add": {
            "doc":{
                'fid': 123,
                'fsid': 456,
                'name': 'yctest',
                "qweasd":"123qwe"
            }
        }
    }
    data = json.dumps(map)
    print data
    r = requests.post(url=url, data=data, headers=head)
    print r.status_code
    print r.json()

def test_binlog_info():
    binlog_conf = {"host":"127.0.0.1", "port":3306, "user":"ekpapi", "passwd":"ekpapi", "charset": 'utf8', "db":"xserver"}
    stream = BinLogStreamReader(connection_settings=binlog_conf,
                                server_id=2,
                                only_tables=["test"],
                                only_schemas=["xserver"],
                                # only_events=[QueryEvent],
                                only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
                                blocking=True)

    count = 0
    for binlog_event in stream:
        print stream.log_file
        print stream.log_pos
        binlog_event.dump()
        print "rows: %s" % binlog_event.rows
        count += 1
    print count
    stream.close()


if __name__ == "__main__":
    test_index_doc()
    test_update_doc()
    test_delete_doc()
    test_index_doc_2()
    solr = solr_sync.SolrSync()
    solr.detele_all_index()
    solr.start()
    test_binlog_info()
