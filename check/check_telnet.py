# encoding: utf-8

from .check import CheckCase
from telnetlib import Telnet


class CheckTelnet(CheckCase):

    def __init__(self, case):
        CheckCase.__init__(self, case)
        self.host = self.case.get('host', '')
        self.port = self.case.get('port', '')
        self.timeout = self.case.get('timeout', 5)

    def check_case(self):
        Telnet(str(self.host), port=int(self.port), timeout=int(self.timeout))
        return True

    @staticmethod
    def fail_log_key():
        return ['host', 'port', 'error_msg', 'monitor_key']

    @staticmethod
    def fail_web_key():
        return ['host', 'port',  'group']

    @staticmethod
    def fail_message_key():
        return ['host', 'port', 'group']

    @staticmethod
    def log_dir():
        return 'telnet'
