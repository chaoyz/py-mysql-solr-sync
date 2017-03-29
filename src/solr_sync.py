#!/usr/local/env python
# encoding:utf8


import config
import logging
import requests
import json
from search_engine_abstract import search_engine_abstract

class SolrSync(search_engine_abstract):

    def __init__(self):
        logging.basicConfig(filename=config.file_path,
                                 level=logging.INFO,
                                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self._solr_config = config.solr_config
        self._mysql_config = config.mysql_config
        self._solr_index_mysql_key_mapping = config.solr_index_mysql_key_mapping

    def post_data_to_search_engine(self, schema, host, port, path, data, headers={'Content-type':'application/json'}, params="commit=true"):
        url = schema + "://" + host + ":" + str(port) + path + "/update/json"
        header_content_type = headers.get("Content-type")
        if header_content_type and header_content_type != "application/json":
            headers["Content-type"] = "application/json"
        if params.find("commit=true"):
            params = params + "&commit=true"
        post_data = json.dumps(data)
        r = requests.post(url=url, data=post_data, headers=headers, params=params)
        return r.json()

if __name__ == "__main__":
    solr = SolrSync()
    data = {
        "add":{
            "doc":{
                "fid":1234,
                "fsid":1234,
                "name":"yctest"
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
