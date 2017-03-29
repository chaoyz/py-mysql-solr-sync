#!/usr/local/env python
# coding:utf8
from abc import abstractmethod, ABCMeta

class search_engine_abstract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def post_data_to_search_engine(self, *p, **kwargs):
        pass

