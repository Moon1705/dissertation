import time
from module.sniffer import Sniffer
from module.store import DataStore
from module.analytics import Analytics 

def main():
    data_store = DataStore()
    sniff = Sniffer(interface='eth0', store=data_store)
    analytics = Analytics(data_store)
    sniff.start()
    time.sleep(60)
    sniff.stop()


if __name__ == '__main__':
    main()
