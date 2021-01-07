import datetime
import logging


class DataStore:

    def __init__(self) -> None:
        logging.info('Create object Datastore')
        self.__store = dict()

    def write(self, event) -> None:
        ip = event['ip_addr_src']
        event.pop('ip_addr_src')
        if ip not in self.__store.keys():
            self.__store[ip] = {'time_create': datetime.datetime.now(), 'events': []}
        self.__store[ip]['events'].append(event)

    def read_all(self) -> dict:
        return self.__store

