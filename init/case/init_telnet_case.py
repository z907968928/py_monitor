# encoding: utf-8
from data_service_monitor.init.init_case import InitCase


class Telnet(InitCase):

    @staticmethod
    def case_type():
        return 'telnet'

    def case_name(self, case):
        return case.get('host', '') + ':' + str(case.get('port', ''))

