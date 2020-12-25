import datetime
from functools import reduce

class Analytics:

    def __init__(self, store) -> None:
        self.__store = store
        self.__check(30)

    def __check(self, count_max_events) -> None:
        while True:
            if len(self.__store) >= 100:
                self.__store.clear()
            for ip, ip_events in self.__store:
                count_ip_events = len(ip_events['events'])
                if (count_ip_events >= count_max_events) or ((datetime.datetime.now() - ip_events['time_create']).seconds >= 300 and count_ip_events >= int(0.5 * count_max_events)):
                    self.preprocessing(self.__store)

    def preprocessing(self, store) -> None:
        count_all_events = reduce(lambda a, x: a + len(x['events']), store.values(), 0)
        for ip, ip_events in store.items():
            count_ip_events = len(ip_events['events'])
            ratio_count = count_ip_events / count_all_events 
            ratio_udp = self.__take_count_flag_events(ip_events, 'None') / count_all_events
            ratio_tcp = 1.0 - ratio_udp
            ratio_tcp_syn = self.__take_count_flag_events(ip_events, '2') / count_ip_events
            ratio_tcp_ack = self.__take_count_flag_events(ip_events, '16') / count_ip_events
            ratio_tcp_fin = self.__take_count_flag_events(ip_events, '1') / count_ip_events
            ratio_tcp_null = self.__take_count_flag_events(ip_events, '0') / count_ip_events
            ratio_tcp_xmas = self.__take_count_flag_events(ip_events, '41') / count_ip_events
            ratio_tcp_maimon = self.__take_count_flag_events(ip_events, '17') / count_ip_events
            ratio_tcp_other = 1.0 - ratio_tcp_syn - ratio_tcp_ack - ratio_tcp_fin - ratio_tcp_null - ratio_tcp_xmas - ratio_tcp_maimon - ratio_udp
            ratio_uniq_ports = len(set(map(lambda x: x['port_dst'], ip_events['events']))) / count_ip_events
            event_info = {"ip_source": ip, "count": ratio_count, "tcp": ratio_tcp, "udp": ratio_udp, "tcp_syn": ratio_tcp_syn, "tcp_ack": ratio_tcp_ack, "tcp_fin": ratio_tcp_fin, "tcp_null": ratio_tcp_null, "tcp_xmas": ratio_tcp_xmas, "tcp_maimon": ratio_tcp_maimon, "tcp_other": ratio_tcp_other, "uniq_ports": ratio_uniq_ports}
            print(event_info)

    def __take_count_flag_events(self, ip_events, flag) -> int:
        return len(list(filter(lambda x: x['transport_protocol_flag'] == flag, ip_events['events'])))


