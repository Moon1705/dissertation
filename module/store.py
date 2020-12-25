class DataStore:

    def __init__(self) -> None:
        self.__store = dict()

    def write(self, event) -> None:
        ip = event['ip_addr_src']
        event.pop('ip_addr_src')
        if ip not in self.__store.keys():
            self.__store[ip] = {'time_create': datetime.datetime.now(), 'events': []}
        self.__store[ip]['events'].append(event)

    def read_all(self) -> dict:
        return self.__store

    def __check(self) -> None:
        while True:
            if len(self.__store) >= 100:
                self.__store.clear()
            for ip, ip_events in self.__store:
                count_ip_events = len(ip_events['events'])
                if (count_ip_events >= 30) or ((datetime.datetime.now() - ip_events['time_create']).seconds >= 300 and count_ip_events >= 15):
                    self.__analytics.check(self.__store)
