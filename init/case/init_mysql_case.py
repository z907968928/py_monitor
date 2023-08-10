# encoding: utf-8

from data_service_monitor.init.init_case import InitCase


class Mysql(InitCase):

    @staticmethod
    def case_type():
        return 'mysql'

