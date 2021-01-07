import random
import json
import logging


def create_raw_data():
    data=[]
    packet_flags = 575
    max_count_check = 30
    min_count_check = int(max_count_check / 2)
    tcp_flags = ['ratio_tcp_syn', 'ratio_tcp_ack', 'ratio_tcp_fin', 'ratio_tcp_null', 'ratio_tcp_xmas', 'ratio_tcp_maimon', 'ratio_tcp_other']
    for i in range(packet_flags * len(tcp_flags)):
        count_ip_packets = random.randint(min_count_check, max_count_check)
        count_all_packets = random.randint(count_ip_packets, 3 * max_count_check)
        count_udp_packets = random.randint(0, count_ip_packets) if bool(random.getrandbits(1)) else 0
        count_tcp_packets = count_ip_packets - count_udp_packets
        ratio_count = round(count_ip_packets / count_all_packets, 3)
        ratio_udp = round(count_udp_packets / count_ip_packets, 3)
        ratio_tcp = round(count_tcp_packets / count_ip_packets, 3)
        ratio_uniq_ports = round(random.randint(1, count_ip_packets) / count_ip_packets, 3)
        tmp_tcp_flags = tcp_flags.copy()
        one_flag = random.randint(int(count_ip_packets / 2), count_ip_packets)
        ratio_tcp_flags = {tcp_flags[int(i / packet_flags)]: round(one_flag / count_ip_packets, 3)}
        tmp_tcp_flags.pop(int(i / packet_flags))
        max_value = count_ip_packets - one_flag
        for flag in tmp_tcp_flags:
            if flag == 'ratio_tcp_other':
                if round(1.0 - sum(list(ratio_tcp_flags.values())), 3) <= 0.001:
                    ratio_tcp_flags[flag] = 0.0
                else:
                    ratio_tcp_flags[flag] = abs(round(1.0 - sum(list(ratio_tcp_flags.values())), 3)) 
                continue
            if not bool(random.getrandbits(1)):
                ratio_tcp_flags[flag] = 0.0
                continue
            value = max_value - random.randint(0, max_value)
            max_value -= value
            ratio_tcp_flags[flag] = round(value / count_ip_packets, 3)
        ratio = {'ratio_count': ratio_count, 'ratio_udp': ratio_udp, 'ratio_tcp': ratio_tcp, 'ratio_uniq_ports': ratio_uniq_ports}
        ratio.update(ratio_tcp_flags)
        data.append(ratio)
    return data

def check_detection(data):
    for event in data:
        if (event['ratio_tcp_maimon'] > 0.3 or event['ratio_tcp_xmas'] > 0.3 or event['ratio_tcp_null'] > 0.3) and event['ratio_count'] > 0.1 and event['ratio_tcp'] > 0.5:
            event['detection'] = 'bad'
        elif (event['ratio_tcp_syn'] > 0.7 or event['ratio_tcp_ack'] > 0.7 or event['ratio_tcp_fin'] > 0.7) and event['ratio_uniq_ports'] > 0.4 and event['ratio_tcp'] > 0.5 and event['ratio_count'] > 0.1:
            event['detection'] = 'bad'
        elif event['ratio_udp'] > 0.8 and event['ratio_uniq_ports'] > 0.4:
            event['detection'] = 'bad'
        elif event['ratio_count'] > 0.3 and event['ratio_uniq_ports'] > 0.4:
            event['detection'] = 'bad'
        else:
            event['detection'] = 'good'
    return data

def create_json(data, save_data_path):
    with open(save_data_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, sort_keys=True)

def create_data(save_data_path):
    data = check_detection(create_raw_data())
    good = len(list(filter(lambda x: x['detection'] == 'good', data)))
    bad = len(data) - good
    logging.info(f'Data create. Good events: {good} and bad events: {bad}')
    create_json(data, save_data_path)
    logging.info(f'Data save. Path: {save_data_path}')
