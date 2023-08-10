# encoding: utf-8

import json
import jsonpath
from .check import CheckCase
from data_service_monitor.core import Model
from data_service_monitor.tool import assertions
from data_service_monitor.tool.tool_conf import template



class CheckMysql(CheckCase):

    def __init__(self, case):
        CheckCase.__init__(self, case)
        self.sql = ''

    def check_case(self):
        case = self.case
        db = self.case.get('db', 'default')
        self.sql = self.case.get('sql', '')
        check_db = Model.DataBaseHandle(db)
        result = check_db.select_db(self.sql)
        self.case_result = json.dumps(result)
        if case['value_type'] == 'json' and self.case_result is None:
            result = json.loads(self.case_result)
        self.check_assert()
        return True

    @staticmethod
    def fail_log_key():
        return ['case_name', 'error_msg', 'sql', 'case_result', 'monitor_key']

    @staticmethod
    def fail_web_desc_key():
        return ['error_msg', 'sql', 'case_result']

    @staticmethod
    def log_dir():
        return 'mysql'

    def check_assert(self):
        """
        :desc  校验result结果集
        :return:
        """
        assert_true = self.case.get('assert_true', [])
        case_result = self.case_result
        const = {
            'CASE_RESULT': case_result,
        }

        for rule in assert_true:
            err_desc = rule.get('err_desc', '')
            rule = template(rule, **const)
            # json path
            if '$' in rule.get('actual', ''):
                if isinstance(self.case_result, str):
                    case_result = json.loads(case_result)
                actual = jsonpath.jsonpath(case_result, rule.get('actual'))
                if not actual:
                    raise Exception('未获取到期望值:' + actual)
                rule['actual'] = actual[0]
            is_normal = assertions.RuleVerification().rule[rule.get('assert')](**rule)

            if not is_normal:
                raise Exception(err_desc)
        return True

