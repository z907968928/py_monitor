# encoding: utf-8

import time
import json


def check_time_slot(time_slot):
    """
    :desc 校验是否在时间段内
    :param time_slot:
    :return:
    """
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    for time_slot in time_slot:
        start_time = time_slot['start_time'] if 'start_time' in time_slot else ''
        end_time = time_slot['end_time'] if 'end_time' in time_slot else ''
        if start_time <= now_localtime <= end_time:
            return True
    return False


def pack_history_param(**kwargs):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    monitor_key = kwargs.get('monitor_key')
    params = kwargs.get('params', '')
    if not isinstance(params, str):
        params = json.dumps(params)
    group = kwargs.get('group', '')
    case_desc = kwargs.get('desc', '')
    check_is_succ = 1 if kwargs.get('check_is_succ') else 0
    result = kwargs.get('case_result', '')
    err_msg = kwargs.get('error_msg', '')
    # case_name = kwargs.get('case_name', '')
    monitor_his_param = {
        'monitor_key': monitor_key,
        'monitor_datetime': date_time,
        'monitor_group': group,
        # 'case_name': case_name,
        'is_succ': check_is_succ,  # 1正常 0失败
        'param': str(params),
        'result': result,
        'err_msg': err_msg,
        'desc': case_desc,
    }
    return monitor_his_param