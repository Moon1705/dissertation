import time
from module.sniff.sniffer import Sniff

def main():
    sniff = Sniff()
    sniff.create_redis()
    sniff.start()
    time.sleep(10)
    sniff.stop()


if __name__ == '__main__':
    main()
