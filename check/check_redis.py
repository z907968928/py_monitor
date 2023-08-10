# encoding: utf-8

import json
import jsonpath
from .check import CheckCase
from data_service_monitor.tool import assertions
from data_service_monitor.tool.tool_conf import template
from data_service_monitor.core.Redis import RedisHandle


class CheckRedis(CheckCase):

    def __init__(self, case):
        CheckCase.__init__(self, case)
        self.redis_key = self.case.get('redis_key', '')
        self.redis_host = self.case.get('host', '')
        self.redis_port = self.case.get('port', '')
        self.value_type = self.case.get('value_type', '')
        self.redis_name = self.case.get('redis', 'default')
        self.redis = RedisHandle(self.redis_name).Redis

    def check_case(self):
        # check_redis = self.redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
        self.case_result = self.redis.get(self.redis_key)
        self.check_assert()
        return True

    @staticmethod
    def fail_log_key():
        return ['case_name', 'error_msg', 'redis_key', 'case_result', 'monitor_key']

    @staticmethod
    def fail_web_key():
        return ['error_msg', 'redis_key', 'case_result']

    @staticmethod
    def log_dir():
        return 'redis'

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

        if self.value_type == 'json' and self.case_result is None:
            case_result = json.loads(self.case_result)

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

            if 'eval' in rule:
                for g_key, g_val in rule['eval']:
                    const[g_key] = eval(g_val)

        return True


    # def check_last_assert(self):
