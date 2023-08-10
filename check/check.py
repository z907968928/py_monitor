# encoding: utf-8

import jsonpath
from data_service_monitor.core.Redis import monitor_redis
from data_service_monitor.model import monitor as db_monitor
from data_service_monitor.tool import (
    check_time_slot,
    pack_history_param,
    _print
)
from  data_service_monitor.tool.log import write_log
from data_service_monitor.tool.notice import *
from data_service_monitor.init.init_base import cmd

class CheckCase(object):
    """
    :desc ip:port telnet 监控
    """

    def __init__(self, case):
        self.case = case
        # for key, info in case.items():
        #     self.__setattr__(key, info)
        self.case_name = case.get('name', '')
        self.case_type = case.get('type', '')
        self.monitor_key = case.get('monitor_key', '')
        self.warning_title = case.get('warning_title', '')
        self.level = case.get('level', '')
        self.title = self.level + '_' + self.warning_title
        self.sub_title = self.case.get('desc', '')
        self.group = self.case.get('group', '')
        self.check_is_succ = False
        self.error_msg = ''
        self.send_mail = False,
        self.send_webhook = False,
        self.send_message = False,
        self.webhook_content = ''
        self.message_content = ''
        self.mail_content = ''
        self.monitor_redis = monitor_redis()

    def get_attr(self, attr):
        attr_dict = {}
        for key in attr:
            attr_dict[key] = getattr(self, key, '')
        return attr_dict

    @staticmethod
    def log_dir():
        return 'api'

    @staticmethod
    def fail_log_key():
        return ['case_name', 'error_msg', 'monitor_key']

    @staticmethod
    def succ_webhook_content_key():
        return ['monitor_key', 'group']

    @staticmethod
    def fail_webhook_content_key():
        return ['error_msg', 'monitor_key']

    def webhook_waring_key(self):
        return self.monitor_key + '_webhook_warning'

    @staticmethod
    def succ_message_content_key():
        return ['monitor_key']

    @staticmethod
    def fail_message_content_key():
        return ['error_msg', 'monitor_key']

    def message_waring_key(self):
        return self.monitor_key + '_message_warning'

    @staticmethod
    def succ_mail_content_key():
        return ['monitor_key']

    @staticmethod
    def fail_mail_content_key():
        return ['error_msg', 'monitor_key']

    def mail_waring_key(self):
        return self.monitor_key + '_mail_warning'

    @staticmethod
    def history_param_key():
        return ['monitor_key', 'group', 'case_name', 'check_is_succ', 'params', 'case_result', 'error_msg']

    def succ(self):
        self.recovery()
        return

    def fail(self):
        # write log
        fail_log_dict = self.get_attr(self.fail_log_key())
        wf_log_path = self.log_dir() + '/' + getattr(self, 'case_name') + '.log.wf'
        write_log(wf_log_path, **fail_log_dict)

        # pack notice
        webhook_warning_interval = self.case.get('webhook_interval', False)
        if self.case.get('send_webhook', False) and \
                webhook_warning_interval and \
                self.monitor_redis.set(self.webhook_waring_key(), 1, nx=True, ex=int(webhook_warning_interval)):
            self.webhook_content = self.get_attr(self.fail_webhook_content_key())
            self.send_webhook = True

        message_warning_interval = self.case.get('message_interval', False)
        if self.case.get('send_message', False) and \
                message_warning_interval and \
                self.monitor_redis.set(self.message_waring_key(), 1, nx=True, ex=int(message_warning_interval)):
            self.message_content = self.get_attr(self.fail_message_content_key())
            self.send_message = True

        email_warning_interval = self.case.get('email_interval', False)
        if self.case.get('send_email', False) and \
                email_warning_interval and \
                self.monitor_redis.set(self.mail_waring_key(), 1, nx=True, ex=int(email_warning_interval)):
            self.mail_content = self.get_attr(self.fail_mail_content_key())
            self.send_mail = True,
        return

    def recovery(self):
        # pack notice
        self.title = self.title + '_恢复'
        if self.monitor_redis.get(self.webhook_waring_key()):
            self.webhook_content = self.get_attr(self.succ_webhook_content_key())
            self.monitor_redis.delete(self.webhook_waring_key())
        self.message_content = self.get_attr(self.succ_webhook_content_key())
        self.mail_content = self.get_attr(self.succ_webhook_content_key())

    def send_notice(self):
        if self.send_webhook:
            webhook_url = self.case.get('webhook_url', False)
            if webhook_url and self.webhook_content != '':
                send_webhook(self.webhook_content, webhook_url, title=self.title,sub_title=self.sub_title)

        if self.send_message:
            message_url = self.case.get('message_url', False)
            phone_list = self.case.get('phone', False)
            if message_url and self.mail_content != '' and phone_list:
                send_message(self.message_content, phone_list, message_url, title=self.title, sub_title=self.sub_title)

        if self.send_mail:
            email = self.case.get('email', False)
            if email:
                send_mail(self.mail_content, email, title=self.title,sub_title=self.sub_title)

    def feedback(self):
        if self.check_is_succ:
            self.succ()
        else:
            self.fail()
        self.send_notice()

    def save_history(self):
        history_param_dict = self.get_attr(self.history_param_key())
        monitor_history_data = pack_history_param(**history_param_dict)
        db_monitor.add_history(monitor_history_data)

    def run(self):
        monitor_time_slot = self.case.get('time_slot', False)
        monitor_interval = self.case.get('monitor_interval', False)
        is_test = cmd().is_test
        if not is_test:
            if not monitor_time_slot \
                    or not check_time_slot(monitor_time_slot) or \
                    not monitor_interval or \
                    self.monitor_redis.set(self.monitor_key, 1, nx=True, ex=monitor_interval) is None:
                return
        try:
            check_is_succ = self.check_case()
            if not check_is_succ:
                raise Exception('check case fail')
            self.check_is_succ = True
            _print.succ('check_' + self.case_type, self.case_name)
        except Exception as e:
            self.check_is_succ = False
            self.error_msg = str(e)
            _print.fail('check_' + self.case_type, self.case_name)

        if not is_test:
            self.feedback()
            self.save_history()
        return

    def check_case(self):
        return
