# encoding: utf-8

from .check_api import CheckApi


class CheckEs(CheckApi):

    @staticmethod
    def log_dir():
        return 'es'
