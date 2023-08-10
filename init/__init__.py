# encoding: utf-8
from .case.init_api_case import Api
from .case.init_mysql_case import Mysql
from .case.init_redis_case import Redis
from .case.init_telnet_case import Telnet
from .case.init_es_case import Es


def all_cases():
    """
    :desc 所有case
    :return:
    """
    print(Es().__getattribute__('case_base_conf'))
    exit(-1)
    cases = Es().all_case + \
            Api().all_case+ \
            Mysql().all_case + \
            Telnet().all_case + \
            Redis().all_case
    # cases = Es().all_case
    return cases


def get_monitor_group_case(group):
    """
    :desc 根据分类获取case
    :param group:
    :return:
    """
    monitor_group = {
        'api': Api().all_case,
        'es': Es().all_case,
        'telnet': Telnet().all_case,
        'mysql': Mysql().all_case,
        'redis': Redis().all_case,
    }
    if group not in monitor_group:
        return False
    return monitor_group[group]()