class DataStore:

    def __init__(self, analytics) -> None:
        self.__store = dict()
        self.__count_events = 0
        self.__analytics = analytics

    def write(self, event) -> None:
        ip = event['ip_addr_src']
        event.pop('ip_addr_src')
        if ip not in self.__store.keys():
            self.__store[ip] = []
        self.__store[ip].append(event)
        self.__count_events += 1
        self.__check(self.__analytics)

    def __delete_all(self) -> None:
        self.__store.clear()
        self.__count_events = 0

    def read_all(self) -> dict:
        return self.__store

    def __check(self, analytics) -> None:
        if self.__count_events >= 30:
            analytics.check(self.__store)
            self.__delete_all()


