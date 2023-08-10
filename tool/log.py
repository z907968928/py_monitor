# encoding: utf-8
import time
import sys


def write_log(file_name, *args, **kwargs):
    """
    :param file_name:
    :param message:
    :return:
    """
    if file_name == '':
        file_name = 'monitor.log.wf'
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if './log/' not in file_name:
        file_name = './log/' + file_name
    f = open(file_name, 'a+')
    s = sys.exc_info()
    if s[2]:
        err_line = str(s[2].tb_lineno)
        err_file = s[2].tb_frame.f_code.co_filename
        err = str(err_file) + ':' + str(err_line)
    else:
        s = sys._getframe()
        err = s.f_code.co_filename + ':' + str(s.f_lineno)
    message = ''
    if len(args):
        for i in  args:
            message += str(i).replace('\n', '').replace('\r', '').replace('\t', '') + '\t'
    if kwargs.keys():
        message += pack_log_message(**kwargs)
    print( '{}\t{}\t{}'.format(date_time, err, message), file=f)
    f.close()
    # import logging
    # import logging.handlers
    # logger = logging.getLogger()
    # log = logging.FileHandler(file_name)
    # formatter = logging.Formatter("%(asctime)s %(message)s")
    # log.setFormatter(formatter)
    # logger.addHandler(log)
    # logger.error(message)
    # logger.removeHandler(logger)
    # logger.removeHandler(log)


def pack_log_message(**kwargs):
    log_message = ''
    for log_key, log_desc in kwargs.items():
        log_desc = str(log_desc).replace('\n', '').replace('\r', '')
        log_message = log_message + '[' + str(log_key) + ']:' + str(log_desc) + "\t"
    return log_message
