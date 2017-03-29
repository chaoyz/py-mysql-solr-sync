#!/usr/local/env python
# coding:utf8

import requests
import json

from src import solr_sync

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

if __name__ == "__main__":
    test_index_doc()
    test_update_doc()
    test_delete_doc()
    test_index_doc_2()