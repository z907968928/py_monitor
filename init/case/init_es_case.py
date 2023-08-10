# encoding: utf-8
from data_service_monitor.init.case import city_list
from data_service_monitor.init.init_case import InitCase
from data_service_monitor.tool import tool_conf


class Es(InitCase):

    @staticmethod
    def case_type():
        return 'es'

    def pack_case(self):
        final_case = []
        cases = self.cases
        for city_info in city_list:
            for case in cases:
                variable = {
                    'CITY_ID': city_info['city_id'],
                    'CITY_NAME': city_info['city_name']
                }
                case = tool_conf.template(case, **variable)
                final_case.append(case)
        return final_case