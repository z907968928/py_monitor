# encoding: utf-8
import sys
import time


def _print(content):
    sys.stdout.write('{}\n'.format(content))


def succ(title, content):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _print('\033[1;34;40m ===={}  {} \033[1;32;40m {} OK!  \033[1;34;40m ====\033[0m' . format(title, date_time, content))


def fail(title, content):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    _print('\033[1;34;40m ===={}  {} \033[1;31;40m {} FAIL1! \033[1;34;40m ==== \033[0m'. format(title, date_time, content))
