# encoding: utf-8
import argparse
from data_service_monitor.tool import tool_conf


def cmd():
    conf_dict = tool_conf.read_conf(tool_conf.conf_path() + '/cmd.yaml')
    arg_parser = argparse.ArgumentParser()
    for args_key, args_info in conf_dict.items():
        arg_parser.add_argument(
            args_key,
            default=args_info['default'] if 'default' in args_info else '',
            nargs=args_info['nargs'] if 'nargs' in args_info else '',
            help=args_info['help'] if 'help' in args_info else ''
        )
    return arg_parser.parse_args()
    # return args


def database_conf():
    return tool_conf.read_conf(tool_conf.conf_path() + '/databases.yaml')


def redis_conf():
    return tool_conf.read_conf(tool_conf.conf_path() + '/redis.yaml')


def case_default_conf():
    return tool_conf.read_conf(tool_conf.conf_path() + '/case_default.yaml')
