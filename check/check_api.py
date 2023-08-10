# encoding: utf-8

import json
import jsonpath
from .check import CheckCase
from data_service_monitor.tool.http import RequestTool
from data_service_monitor.tool import assertions


class CheckApi(CheckCase):

    def __init__(self, case):
        CheckCase.__init__(self, case)
        self.host = self.case.get('host', '')
        self.uri = self.case.get('uri', '')
        self.url = self.host + self.uri
        self.method = self.case.get('method', 'post')
        self.header = self.case.get('header', {})
        self.timeout = self.case.get('timeout', 5)
        self.params = self.case.get('params', '')

    def check_case(self):
        # get api result
        request = RequestTool(self.url, self.method, self.params, self.header, self.timeout)
        if not request.response:
            raise Exception(request.err_msg)

        self.case_result = request.response.text
        self.check_assert()
        return True


    @staticmethod
    def fail_log_key():
        return ['case_name', 'error_msg', 'params', 'case_result', 'monitor_key']

    @staticmethod
    def fail_webhook_content_key():
        return ['case_name', 'error_msg', 'params', 'case_result', 'monitor_key']

    def check_assert(self):
        """
        :desc  校验result结果集
        :return:
        """
        assert_true = self.case.get('assert_true', [])
        case_result = self.case_result
        for rule in assert_true:
            err_desc = rule.get('err_desc', '')
            # json path
            if '$.' in rule.get('actual', ''):
                case_result = json.loads(case_result)
                actual = jsonpath.jsonpath(case_result, rule.get('actual'))
                if not actual:
                    raise Exception('未获取到期望值:' + actual)
                rule['actual'] = actual[0]
            is_normal = assertions.RuleVerification().rule[rule.get('assert')](**rule)
            if not is_normal:
                raise Exception(err_desc)
        return True

