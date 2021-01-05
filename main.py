import threading
import configparser
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics
from module.model import Model

def main(config):
    data_store = DataStore()
    sniffer = threading.Thread(name='sniffer', target=(lambda: Sniffer(config['SNIFFER']['interface'], data_store)))
    analytics = threading.Thread(name='analytics', target=(lambda: Analytics(data_store, int(config['ANALYTIC']['count_event_analysis']), int(config['ANALYTIC']['check_time']), Model(config['MODEL']['model_path'], config['MODEL']['load_data_path'], True if config['MODEL']['create_model'] == 'yes' else False))))
    sniffer.start()
    analytics.start()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("settings.conf")
    main(config)
