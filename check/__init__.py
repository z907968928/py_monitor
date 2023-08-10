# encoding: utf-8
from .check_telnet import CheckTelnet
from .check_api import CheckApi
from .check_es import CheckEs
from .check_mysql import CheckMysql
from .check_redis import CheckRedis
from .check_cliff import CheckCliff


def factory(case):

    if 'func' not in case or case['func'] == '':
        return False
    func = case['func']
    check_func = {
        'check_telnet': CheckTelnet,
        'check_api': CheckApi,
        'check_es': CheckEs,
        'check_redis': CheckRedis,
        'check_mysql': CheckMysql,
        'check_cliff': CheckCliff,
    }
    if func in check_func:
        return check_func[func](case)
    return False

