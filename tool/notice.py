# encoding: utf-8

import sys
import json
import time
import requests
from .log import write_log
from data_service_monitor.init.init_base import case_default_conf
from data_service_monitor.tool import http


def send_webhook(content, webhook_url, **kwargs):
    pack_webhook_notice(content=content, **kwargs)
    """
    :desc 发送webhook
    :param content:
    :param webhook_url:
    :return:
    """
    try:
        webhook_url = webhook_url if webhook_url != '' else case_default_conf().get('webhook_url')
        header = {
            'Content-Type': 'application/json'
        }
        if isinstance(content, dict):
            content = json.dumps(content)
        ret = requests.post(webhook_url, content, headers=header, timeout=10).text
        result = json.loads(ret)
        if 'code' in result and result['code'] != 0:
            raise Exception(ret)
    except Exception as e:
        write_log('monitor.log.wf', error='send web error', webhook=webhook_url, err_msg=str(e))


def send_message(message, phone_list, message_url, **kwargs):
    pack_message_notice(content=message, **kwargs)
    """
    :desc 发送短信
    :param message:
    :param phone_list:
    :return:
    """
    if len(phone_list) <= 0:
        return
    try:
        params = {
            'phone': phone_list,
            'message': message,
        }
        header = {
            'Content-Type': 'application/json'
        }
        params = json.dumps(params)
        ret = requests.post(message_url, params, headers=header, timeout=10)
        result = json.loads(ret.text)
        if result['data']['unSuccess'] is not None:
            raise Exception('send message error : ' + result['data']['error'] + ' [parsms]:' + params)
    except Exception as e:
        write_log('monitor.log.wf', error='send message error', msg_url=message_url, err_msg=str(e))


def send_mail(content, email, **kwargs):
    pack_message_notice(content=content, **kwargs)
    return 1


def pack_content(**kwargs):
    content = ''
    for content_key, content_desc in kwargs.items():
        content += '[' + str(content_key) + ']:' + str(content_desc) + "\n"
    return content


def pack_notice(**kwargs):
    """
    :param title string
    :param sub_title string
    :param content dict
    :return:
    """
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    title = kwargs.get('title', '')
    sub_title = kwargs.get('sub_title', '')
    content = kwargs.get('content', {})
    content = pack_content(**content)
    return date_time, title, sub_title, content

def pack_webhook_notice(**kwargs):
    """
    :param title string
    :param sub_title string
    :param content dict
    :return:
    """
    date_time, title, sub_title, content = pack_notice(**kwargs)
    web_notice_content = {
        'text': title,
        'attachments': [
            {
                'title': '时间',
                'text': date_time,
            },
            {
                'title': sub_title,
                'text': content,
            }
        ]
    }
    return web_notice_content


def pack_message_notice(**kwargs):
    """
    :param title string
    :param sub_title string
    :param content dict
    :return:
    """
    date_time, title, sub_title, content = pack_notice(**kwargs)
    message_notice_content = title + \
                           '\n时间:' + date_time + \
                           '\n名称:' + sub_title + \
                           '\n' + content
    return message_notice_content

def pack_mail_notice(**kwargs):
    """
    :param title string
    :param sub_title string
    :param content dict
    :return:
    """
    date_time, title, sub_title, content = pack_notice(**kwargs)
    message_notice_content = title + \
                           '\n时间:' + date_time + \
                           '\n名称:' + sub_title + \
                           '\n' + content
    return message_notice_content