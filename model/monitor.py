# encoding: utf-8
import time
from data_service_monitor.core import Model


def add_history(data):
    db = Model.DataBaseHandle('default')
    monitor_key = data.get('monitor_key', '')
    monitor_datetime = data.get('monitor_datetime', '1971-01-01 00:00:00')
    monitor_group = data.get('monitor_group', '')
    is_succ = data.get('is_succ', 1)
    params = data.get('param', '')
    result = data.get('result', '')
    err_msg = data.get('err_msg', '')
    db.insert_db("insert into monitor_history (monitor_key,monitor_datetime,monitor_group,is_succ,param,result,err_msg) values "
                 "(%s,%s,%s,%s,%s,%s,%s)",
                 (monitor_key, monitor_datetime, monitor_group, is_succ, params, result, err_msg))
    add_notice(data)


def add_notice(data):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db = Model.DataBaseHandle('default')
    title = data.get('title', '服务检测')
    content = data.get('desc', '')
    monitor_key = data.get('monitor_key', '')
    is_succ = data.get('is_succ', 1)
    monitor_notice = db.select_db('select id,is_succ,is_show from monitor_notice where monitor_key=%s', (monitor_key))
    if len(monitor_notice) <= 0:
        is_show = 1 if is_succ == 0 else 0
        db.insert_db("insert into monitor_notice (title,content,monitor_key,is_succ,is_show,create_time,update_time) VALUES "
                     "(%s,%s,%s,%s,%s,%s,%s)",
                     (title, content, monitor_key, is_succ, is_show, date_time, date_time))
    else:
        notice_id = monitor_notice[0]['id']
        notice_is_show = monitor_notice[0]['is_show']
        notice_is_succ = monitor_notice[0]['is_succ']
        if is_succ == 0:
            if notice_is_show == 0:
                db.update_db('update monitor_notice set is_show=1, is_succ=0, update_time=%s where id=%s', (date_time, notice_id))
        else:
            if notice_is_succ == 0:
                db.update_db('update monitor_notice set is_show=1, is_succ=1, update_time=%s where id=%s', (date_time, notice_id))
            else:
                if notice_is_show == 1:
                    db.update_db('update monitor_notice set is_show=0, update_time=%s where id=%s',(date_time, notice_id))
