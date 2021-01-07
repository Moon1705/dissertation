import threading
import json
import logging
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics
from module.model import Model


def main(config):
    data_store = DataStore()
    try:
        sniffer = threading.Thread(name='sniffer', target=(lambda: Sniffer(config['SNIFFER']['interface'], config['SNIFFER']['excluded_ips'], data_store)))
        analytics = threading.Thread(name='analytics', target=(lambda: Analytics(data_store, config['ANALYTIC']['count_event_analysis'], config['ANALYTIC']['check_time'], Model(config['MODEL']['model_path'], config['MODEL']['load_data_path'], config['MODEL']['create_model']))))
        sniffer.start()
        analytics.start()
    except Exception:
        logging.exception('Problems in threads')
        logging.info('Program stop')
        exit()


if __name__ == '__main__':
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s', filename = 'log/runtime_log.txt', level=logging.DEBUG)
    logging.info('Program start')
    try:
        with open('config/settings.conf', 'r', encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error('Config settings file not found')
        loggin.info('Program stop')
        exit()
    try:
        main(config)
    except KeyboardInterrupt:
        logging.info('Program was stopped by user request')
        exit()
