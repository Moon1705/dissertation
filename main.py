import time
from module.sniff.sniffer import Sniff
from module.store.data_store import DataStore

def main():
    data_store = DataStore()
    sniff = Sniffer(interface='eth0', store=data_store)
    sniff.start()
    time.sleep(100)
    sniff.stop()


if __name__ == '__main__':
    main()
