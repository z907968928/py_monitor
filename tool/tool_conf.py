# encoding: utf-8

import sys
import toml
import os
import yaml
import datetime
import time
import json
from string import Template


def read_toml_conf(conf_path, is_template=True):
    conf_data = read_file(conf_path)
    if is_template:
        conf_data = template(conf_data, **const())
    toml_conf = toml.loads(conf_data)
    return toml_conf


def read_yaml_conf(conf_path, is_template=True):
    conf_data = read_file(conf_path)
    if is_template:
        conf_data = template(conf_data, **const())
    conf_data = yaml.safe_load(conf_data)
    return conf_data


def read_file(file_path):
    conf_file = open(file_path, 'rt', encoding='utf-8')
    file_text = conf_file.read()
    conf_file.close()
    return file_text


def template(data, **kwargs):
    not_str = False
    if not isinstance(data, str) or not isinstance(data, bytes):
        data = json.dumps(data)
        not_str = True
    template = Template(data)
    template_data = template.safe_substitute(kwargs)
    if not_str:
        template_data = json.loads(template_data)
    return template_data


def read_conf(conf_path, is_template=True):
    file_path, file_type = os.path.splitext(conf_path)
    if file_type == '.yaml':
        return read_yaml_conf(conf_path, is_template)
    elif file_type == '.yml':
        return read_yaml_conf(conf_path, is_template)
    elif file_type == '.toml':
        return read_toml_conf(conf_path, is_template)
    else:
        return False


def read_conf_dir(conf_dir_path, is_template=True):
    conf_dict = {}
    for parent_dir, dir_name, file_names in os.walk(conf_dir_path):
        for file_name in file_names:
            file_path, file_type = os.path.splitext(file_name)
            conf_dict[file_path] = read_conf(conf_dir_path + '/' + file_name, is_template)
    return conf_dict


def conf_path():
    return sys.path[0] + '/config/'


def const():
    geomesa_start_time = time.time() - 3600
    geomesa_end_time = time.time() - 3600
    geomesa_start = datetime.datetime.fromtimestamp(geomesa_start_time)
    geomesa_end = datetime.datetime.fromtimestamp(geomesa_end_time)

    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    date_yesterday = today - oneday

    const_conf_path = conf_path() + 'const.yaml'
    # const_conf_path = '../config/const.yaml'
    const = read_yaml_conf(const_conf_path, is_template=False)

    CONST = dict(const, **{
        'GEOMESA_START': geomesa_start.strftime("%Y-%m-%dT%H:%M:%S.000000+08:00"),
        'GEOMESA_END': geomesa_end.strftime("%Y-%m-%dT%H:%M:%S.000000+08:00"),
        'START_HOUR': (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        'END_HOUR': (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
        'TODAY': str(today),
        'YESTERDAY': str(date_yesterday),
        'MONTH': date_yesterday.strftime('%Y%m'),
        'TIME_STMAP': int(time.time()),
        'NOW_TIME_STMAP': int(time.time()),
    })
    return CONST
