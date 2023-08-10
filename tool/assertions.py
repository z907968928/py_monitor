# encoding: utf-8

# import pytest
import datetime
import time
import jsonpath


class RuleVerification(object):

    def __init__(self):
        self.rule = {
            '==': self._eq_status_code,
            "=": self._eq,
            "!=": self._neq,
            ">": self._gt,
            ">=": self._gte,
            "<": self._lt,
            "<=": self._lte,
            "in": self._in,
            "notIn": self._not_in,
            "isInstance": self._is_instance,
            "notIsInstance": self._not_is_instance,
            "empty": self._empty,
            "notEmpty": self._not_empty,
            "datetimeToTimeStmapLt": self._datetime_to_timestmap_lt,
            "datetimeToTimeStmapLe": self._datetime_to_timestmap_le,
            "datetimeToTimeStmapGt": self._datetime_to_timestmap_gt,
            "datetimeToTimeStmapGe": self._datetime_to_timestmap_ge,
            "lenLt": self._len_lt,
            "lenLe": self._len_le,
            "lenGt": self._len_gt,
            "lenGe": self._len_ge,
        }
        # return self.rule[check_rule]
        # for k, v in kwargs:
        #     self.__setattr__(k, v)

    @staticmethod
    def _eq_status_code(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # assert int(actual) == int(expected)
        return int(actual) == int(expected)

    @staticmethod
    def _eq(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual == expected, desc)
        return actual == expected

    @staticmethod
    def _neq(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual != expected, desc)
        return actual != expected

    @staticmethod
    def _gt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual > expected, desc)
        return actual > expected

    @staticmethod
    def _gte(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual >= expected, desc)
        return actual >= expected

    @staticmethod
    def _lt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual < expected, desc)
        return actual < expected

    @staticmethod
    def _lte(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual <= expected, desc)
        return actual >= expected

    @staticmethod
    def _in(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual in expected, desc)
        return actual in expected

    @staticmethod
    def _not_in(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(actual not in expected, desc)
        return actual in expected

    @staticmethod
    def _is_instance(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(isinstance(actual, expected), desc)
        return isinstance(actual, expected) == True

    @staticmethod
    def _not_is_instance(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(isinstance(actual, expected) == False, desc)
        return isinstance(actual, expected) == False

    @staticmethod
    def _empty(actual, **kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        # pytest.assume(len(actual) == 0, desc)
        return len(actual) == 0

    @staticmethod
    def _not_empty(**kwargs):
        actual = kwargs.get('actual')
        # pytest.assume(len(actual), desc)
        return len(actual) > 0

    @staticmethod
    def _datetime_to_timestmap_lt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        date_format = kwargs.get('date_format', '%Y-%m-%d %H:%M:%S')
        actual_time_stmap = int(time.mktime(time.strptime(actual, date_format)))
        time_stmap = int(time.time())
        # pytest.assume(time_stmap-actual_time_stmap <= expected, desc)
        return time_stmap-actual_time_stmap < expected

    @staticmethod
    def _datetime_to_timestmap_le(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        date_format = kwargs.get('date_format', '%Y-%m-%d %H:%M:%S')
        actual_time_stmap = int(time.mktime(time.strptime(actual, date_format)))
        time_stmap = int(time.time())
        # pytest.assume(time_stmap-actual_time_stmap <= expected, desc)
        return time_stmap-actual_time_stmap <= expected

    @staticmethod
    def _datetime_to_timestmap_gt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        date_format = kwargs.get('date_format', '%Y-%m-%d %H:%M:%S')
        actual_time_stmap = int(time.mktime(time.strptime(actual, date_format)))
        time_stmap = int(time.time())
        # pytest.assume(time_stmap-actual_time_stmap <= expected, desc)
        return time_stmap-actual_time_stmap > expected

    @staticmethod
    def _datetime_to_timestmap_ge(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        date_format = kwargs.get('date_format', '%Y-%m-%d %H:%M:%S')
        actual_time_stmap = int(time.mktime(time.strptime(actual, date_format)))
        time_stmap = int(time.time())
        # pytest.assume(time_stmap-actual_time_stmap <= expected, desc)
        return time_stmap - actual_time_stmap >= expected

    @staticmethod
    def _len_lt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        return len(actual) < expected

    @staticmethod
    def _len_le(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        return len(actual) <= expected

    @staticmethod
    def _len_gt(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        return len(actual) > expected

    @staticmethod
    def _len_ge(**kwargs):
        actual = kwargs.get('actual')
        expected = kwargs.get('expected')
        return len(actual) >= expected


# pytest.main()
def test():
    a = RuleVerification().rule
    print (a['==']('1', '2', 'test'))