# encoding: utf-8

import hashlib
from .init_base import case_default_conf
from data_service_monitor.tool import tool_conf
from data_service_monitor.tool.log import write_log


class InitCase(object):

    def __init__(self):
        try:

            # self.__setattr__('case_base_conf', self.case_base())
            self.type = self.case_type()
            self.case_conf_path = self.case_path()
            self.case_base_conf_path = self.case_base_path()
            self.case_base_conf = self.case_base()
            self.cases = self.get_case()
            self.all_case = self.pack_case()
        except Exception as e:
            write_log('monitor.log.wf', error='pack case error', err_msg=str(e))

    @staticmethod
    def case_type():
        return 'api'

    def case_name(self, case):
        return case.get('name', '')

    def case_base_path(self):
        return tool_conf.conf_path() + 'base/' + self.type + '_base.yaml'

    def case_path(self):
        return tool_conf.conf_path() + 'case/' + self.type

    def case_base(self):
        base_case_conf = tool_conf.read_conf(self.case_base_conf_path)
        return base_case_conf

    def get_case(self):
        case_dict = tool_conf.read_conf_dir(self.case_conf_path)
        case_list = []
        for file_name, cases in case_dict.items():
            for case in cases:
                case = dict(
                    self.case_base_conf, **case
                )
                case = self.check_case_conf(case, file_name)
                case_list.append(case)
        return case_list

    def pack_case(self):
        return self.cases

    def check_case_conf(self, case, group=''):
        case_default = case_default_conf()
        case = dict(case_default, **case)

        monitor_key = case.get('monitor_key', '')
        monitor_key_prefix = case.get('monitor_key_prefix', '')

        if monitor_key_prefix == '':
            monitor_key_prefix = case_default['monitor_key_prefix']

        if monitor_key == '':
                # monitor_key = monitor_key_prefix + case['group']
                monitor_key = monitor_key_prefix + hashlib.md5(str(case)).hexdigest()
        else:
            if monitor_key_prefix not in monitor_key:
                monitor_key = monitor_key_prefix + monitor_key

        case['monitor_key'] = monitor_key
        case['monitor_key_prefix'] = monitor_key_prefix

        case_group = case.get('group', '')
        if case_group == '':
            case['group'] = group

        case_type = case.get('type', '')
        if case_type == '':
            case['type'] = self.type

        case['name'] = self.case_name(case)
        return case
