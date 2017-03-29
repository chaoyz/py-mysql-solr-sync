#!/usr/local/env python
# coding:utf8
from abc import abstractmethod, ABCMeta

class db_abstract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_index_data(self):
        pass