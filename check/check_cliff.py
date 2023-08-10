# encoding: utf-8

import json
import redis
import datetime
import jsonpath
from .check_es import CheckEs
from data_service_monitor.tool import tool_conf, assertions
from data_service_monitor.tool.http import RequestTool
from data_service_monitor.tool.tool_conf import template
from data_service_monitor.core.Redis import RedisHandle


class CheckCliff(CheckEs):

    def __init__(self, case):
        CheckEs.__init__(self, case)
        # self.redis_host = self.case.get('redis_host', '')
        # self.redis_port = self.case.get('redis_port', '')
        self.redis_name = self.case.get('redis', 'default')
        self.redis = RedisHandle(self.redis_name).Redis
        self.redis_key = self.case.get('redis_key', '')
        self.last_hour_key = self.case.get('last_hour_key', '')
        self.last_result_info = ''

    def check_case(self):
        today = str(datetime.date.today())
        last_time = self.redis.get(self.last_hour_key)
        if last_time is None:
            raise Exception('获取批次号为空')
        last_data_time = today + ' ' + last_time
        if 'online_its_alarm_movement_month' in self.params:
            last_data_time = datetime.datetime.strptime(last_data_time, '%Y-%m-%d %H:%M:%S') - \
                             datetime.timedelta(minutes=30)
        self.params = tool_conf.template(self.params, LAST_DATE_TIME=last_data_time)

        # get ES result
        request = RequestTool(self.url, self.method, self.params, self.header, self.timeout)
        if not request:
            raise Exception(request.err_msg)

        self.case_result = request.response.text

        last_result_key = self.monitor_key + '_last_result'
        self.last_result_info = self.monitor_redis.get(last_result_key)
        self.check_assert()

        if self.last_result_info and json.loads(self.last_result_info).get('last_time', '') != last_time:
            self.check_cliff()

        new_last_result_info = {
            'last_time': last_time,
            'last_result': self.case_result
        }
        self.monitor_redis.set(last_result_key, json.dumps(new_last_result_info), ex=3600)

        return True

    @staticmethod
    def fail_log_key():
        return ['case_name', 'error_msg', 'params', 'case_result', 'monitor_key', 'last_result_info']

    @staticmethod
    def fail_web_desc_key():
        return ['error_msg', 'case_result', 'last_result_info']

    def check_cliff(self):
        """
        :desc  校验result结果集
        :return:
        """
        assert_true = self.case.get('last_assert_true', [])
        case_result = self.case_result
        last_result = json.loads(self.last_result_info).get('last_result', '')

        for rule in assert_true:
            err_desc = rule.get('err_desc', '')
            const = {
                'LAST_SUBTRACT_NOW_TOTAL': last_result['hits']['total'] - case_result['hits']['total'],
                'TOTAL_EXPECTED': last_result['hits']['total'] * 0.2
            }
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