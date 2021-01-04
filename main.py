import threading
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics

def main():
    data_store = DataStore()
    sniffer = threading.Thread(name='sniffer', target=(lambda: Sniffer(interface='eth0', store=data_store)))
    analytics = threading.Thread(name='analytics', target=(lambda: Analytics(data_store)))
    sniffer.start()
    analytics.start()


if __name__ == '__main__':
    main()
