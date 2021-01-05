import threading
import json
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics
from module.model import Model

def main(config):
    data_store = DataStore()
    sniffer = threading.Thread(name='sniffer', target=(lambda: Sniffer(config['SNIFFER']['interface'], config['SNIFFER']['excluded_ips'], data_store)))
    analytics = threading.Thread(name='analytics', target=(lambda: Analytics(data_store, config['ANALYTIC']['count_event_analysis'], config['ANALYTIC']['check_time'], Model(config['MODEL']['model_path'], config['MODEL']['load_data_path'], config['MODEL']['create_model']))))
    sniffer.start()
    analytics.start()


if __name__ == '__main__':
    with open('settings.conf', 'r', encoding='utf-8') as file:
        config = json.load(file)
    main(config)
