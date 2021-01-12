import logging
import datetime
from functools import reduce
from collections import OrderedDict

class Analytics:

    def __init__(self, store, count_max_events, check_time, model) -> None:
        logging.info('Create object Analytics')
        self.__store = store.read_all()
        self.__model = model
        self.__check(count_max_events, check_time)

    def __check(self, count_max_events, check_time) -> None:
        while True:
            if len(self.__store) >= 100:
                self.__store.clear()
            ips = list(self.__store.keys())
            for ip in ips:
                count_ip_events = len(self.__store[ip]['events'])
                if (count_ip_events >= count_max_events) or ((datetime.datetime.now() - self.__store[ip]['time_create']).seconds >= check_time and count_ip_events >= int(0.5 * count_max_events)):
                    self.__preprocessing(ip)
                    self.__store.pop(ip)

    def __preprocessing(self, ip) -> None:
        count_all_events = reduce(lambda a, x: a + len(x['events']), self.__store.values(), 0)
        count_ip_events = len(self.__store[ip]['events'])
        ratio_count = count_ip_events / count_all_events 
        ratio_udp = self.__take_count_flag_events(ip, 'None') / count_ip_events
        ratio_tcp = 1.0 - ratio_udp
        ratio_tcp_syn = self.__take_count_flag_events(ip, '2') / count_ip_events
        ratio_tcp_ack = self.__take_count_flag_events(ip, '16') / count_ip_events
        ratio_tcp_fin = self.__take_count_flag_events(ip, '1') / count_ip_events
        ratio_tcp_null = self.__take_count_flag_events(ip, '0') / count_ip_events
        ratio_tcp_xmas = self.__take_count_flag_events(ip, '41') / count_ip_events
        ratio_tcp_maimon = self.__take_count_flag_events(ip, '17') / count_ip_events
        ratio_tcp_other = 1.0 - ratio_tcp_syn - ratio_tcp_ack - ratio_tcp_fin - ratio_tcp_null - ratio_tcp_xmas - ratio_tcp_maimon - ratio_udp
        ratio_uniq_ports = len(set(map(lambda x: x['port_dst'], self.__store[ip]['events']))) / count_ip_events
        event_info = {"count": ratio_count, "tcp": ratio_tcp, "udp": ratio_udp, "tcp_syn": ratio_tcp_syn, "tcp_ack": ratio_tcp_ack, "tcp_fin": ratio_tcp_fin, "tcp_null": ratio_tcp_null, "tcp_xmas": ratio_tcp_xmas, "tcp_maimon": ratio_tcp_maimon, "tcp_other": ratio_tcp_other, "uniq_ports": ratio_uniq_ports}
        if not self.__model.check_event(list(dict(OrderedDict(sorted(event_info.items()))).values())):
            logging.info(f'Bad event: {ip} - {event_info}')

    def __take_count_flag_events(self, ip, flag) -> int:
        return len(list(filter(lambda x: x['transport_protocol_flag'] == flag, self.__store[ip]['events'])))


