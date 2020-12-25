from functools import reduce

class Analytics:

    def __init__(self) -> None:
        pass

    def check(self, store) -> None:
        count_all_events = reduce(lambda a, x: a + len(x), store.values(), 0)
        for ip, events in store.items():
            count_ip_events = len(events)
            ratio_count = count_ip_events / count_all_events 
            ratio_udp = self.__take_count_flag_events(events, 'None') / count_all_events
            ratio_tcp = 1.0 - ratio_udp
            ratio_tcp_syn = self.__take_count_flag_events(events, '2') / count_ip_events
            ratio_tcp_ack = self.__take_count_flag_events(events, '16') / count_ip_events
            ratio_tcp_fin = self.__take_count_flag_events(events, '1') / count_ip_events
            ratio_tcp_null = self.__take_count_flag_events(events, '0') / count_ip_events
            ratio_tcp_xmas = self.__take_count_flag_events(events, '41') / count_ip_events
            ratio_tcp_maimon = self.__take_count_flag_events(events, '17') / count_ip_events
            ratio_tcp_other = 1.0 - ratio_tcp_syn - ratio_tcp_ack - ratio_tcp_fin - ratio_tcp_null - ratio_tcp_xmas - ratio_tcp_maimon
            ratio_uniq_ports = len(set(map(lambda x: x['port_dst'], events))) / count_ip_events
            event_info = {"ip_source": ip, "count": ratio_count, "tcp": ratio_tcp, "udp": ratio_udp, "tcp_syn": ratio_tcp_syn, "tcp_ack": ratio_tcp_ack, "tcp_fin": ratio_tcp_fin, "tcp_null": ratio_tcp_null, "tcp_xmas": ratio_tcp_xmas, "tcp_maimon": ratio_tcp_maimon, "tcp_other": ratio_tcp_other, "uniq_ports": ratio_uniq_ports}
            print(event_info)

    def __take_count_flag_events(self, events, flag) -> int:
        return len(list(filter(lambda x: x['transport_protocol_flag'] == flag, events)))


