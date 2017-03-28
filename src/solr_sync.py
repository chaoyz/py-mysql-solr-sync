#!/usr/local/env python
# encoding:utf8


from pymysqlreplication import BinLogStreamReader
import config
import logging

class SolrSync(object):

    def __init__(self):
        logging.basicConfig(filename=config.file_path,
                                 level=logging.INFO,
                                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        self.logger = logging.getLogger(__name__)
        self._solr_config = config.solr_config
        self._mysql_config = config.mysql_config
        self._solr_index_mysql_key_mapping = config.solr_index_mysql_key_mapping

    def _post_data_to_solr(self, url, data, operation):
        '''
        use json data post to solr
        :param url:
        :param data:
        :param operation:
        :return:
        '''
        if operation == 'index':
            url = url + '/'
            pass
        elif operation == 'delete':
            pass
        elif operation == 'update':
            pass
        elif operation == 'select':
            pass

    def _full_sync(self):
        pass

    def _index_data(self):
        pass

    def _delete_data(self):
        pass

    def _update_data(self):
        pass
