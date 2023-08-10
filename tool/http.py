# encoding: utf-8
import requests
import json
from .log import write_log


class RequestTool(object):

    def __init__(self, url, method, data, header, timeout=30, retry=1, **kwargs):
        self.url = url
        self.method = method
        self.data = data
        self.header = self.pack_header(header)
        self.timeout = timeout
        self.data = self.pack_data(data)
        self.response = False
        self.err_msg = ''
        for i in range(retry):
            try:
                response = requests.request(self.method, self.url, params=data, data=data, headers=self.header, timeout=self.timeout, **kwargs)
                if response.status_code != 200:
                    raise Exception('http code not 200')
                else:
                    self.response = response
                    break
                    # reponse.__setattr__('retry', retry-1)
                    # return self.reponse
            except Exception as e:
                self.err_msg = str(e)
                write_log('http.log.wf', url=url, method=method, err_msg=str(e), retry=i-1)

    def pack_header(self, header):
        if self.method == "json":
            if isinstance(header, dict):
                header['Content-Type'] = 'application/json'
            self.method = 'post'
        # else:
        #     header['Content-Type'] = 'application/x-www-form-urlencoded'
        return header

    def pack_data(self, data):
        # if self.method == 'json' and isinstance(data, str) == False:
        if self.method == 'json' and not isinstance(data, str):
            data = json.dumps(data)
        return data

# def request(url, method, data, header, timeout=30, retry=1, **kwargs):
#     header = pack_header(method, header)
#     data = pack_data(method, data)
#     if method == 'json':
#         method = 'post'
#     for i in range(retry):
#         try:
#             reponse = requests.request(method, url, data=data, headers=header, timeout=timeout, **kwargs)
#             if reponse.status_code != 200:
#                 raise Exception('http code not 200')
#             else:
#                 # reponse.__setattr__('retry', retry-1)
#                 return reponse
#         except Exception as e:
#             write_log('http.log.wf', url=url, method=method, err_msg=str(e), retry=i-1)
    # return reponse
    # return reponse

#
# def pack_header(method, header):
#     if method == "json":
#         header = dict(
#             header, **{
#                'Content-Type': 'application/json'
#             }
#         )
#     else:
#         header = dict(
#             header, **{
#                 'Content-Type': 'application/x-www-form-urlencoded'
#             }
#         )
#     return header
#
#
# def pack_data(method, data):
#     if method == 'json' and isinstance(data, str) == False:
#             data = json.dumps(data)
#     return data
#
#
# def get_json(reponse):
#     #获取返回json
#     # print('res.json：\n',reponse.json())
#     return reponse.json()
#
#
# def get_text(reponse):
#     # print('res.text：\n',reponse.text)
#     return reponse.text
#
#
# def get_time(reponse):
#     #获取响应执行时间,单位s
#     time = reponse.elapsed.total_seconds()
#     # print('res.time：\n',reponse.elapsed.total_seconds())
#     return time
#
#
# def get_code(reponse):
#     #获取返回code
#     code = reponse.status_code
#     # print('code：\n',code)
#     return code
