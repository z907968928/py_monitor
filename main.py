# encoding: utf-8
"""
test case for main
"""
import json
import threading
from data_service_monitor import init
from data_service_monitor.init.init_base import cmd
from data_service_monitor.tool.log import write_log
from data_service_monitor.tool._print import _print
from data_service_monitor.check import factory

# import init
# from init.init_base import cmd
# from tool.log import write_log
# from tool._print import _print
# from check import factory
# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.path.append(sys.path[0])


def run(case):
    """
    :param :case
    :return:
    """
    try:
        # monitor check
        if 'func' not in case or not factory(case):
            write_log('monitor.log.wf', err_msg='check fun error')
            return

        # run check case
        func = factory(case)
        func.run()

    except Exception as e:
        write_log('monitor.log.wf', err_msg=str(e))
    sem.release()


if __name__ == '__main__':
    args = cmd()
    # args = base.args
    monitor_type = args.monitor_type

    _print('\033[1;31;40m monitor_type: ' + monitor_type + '\033[0m')

    # 默认all
    cases = []
    if monitor_type == 'all':
        cases = init.all_cases()
    elif init.get_monitor_group_case(monitor_type):
        cases = init.get_monitor_group_case(monitor_type)
    else:
        print ('monitor_type not supported')
        exit(-1)

    f = open('run_conf_defalut.json', 'w')
    f.write(json.dumps(cases, sort_keys=True, indent=2, ensure_ascii=False))
    f.close()
    exit(-1)
    # for case in cases:
    #     run(case)
    #
    # exit(-1)

    # 最大线程数
    max_thread_num = int(args.thread_num)
    sem = threading.Semaphore(max_thread_num)

    # 开始任务
    if monitor_type == 'all':
        for case in cases:
            sem.acquire()
            threading.Thread(target=run, args=(case,)).start()
    else:
        for case in cases:
            # check_func.check_mysql_ret({case_name: case_info})
            func = factory(case['func'])
            if func:
                ret = func(case)
                for i in ret:
                    print (json.dumps(i))
    exit(-1)
