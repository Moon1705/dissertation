import time
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics 

def main():
    analytics = Analytics()
    data_store = DataStore(analytics)
    sniff = Sniffer(interface='eth0', store=data_store)
    sniff.start()
    time.sleep(30)
    sniff.stop()


if __name__ == '__main__':
    main()
