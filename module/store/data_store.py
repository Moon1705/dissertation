import sys

class DataStore:

    def __init__(self, store=set()) -> None:
        self.__store = store

    def write(self, event) -> None:
        self.__store.add(event)

    def read_all(self) -> set:
        return self.__store

    def delete_all(self) -> None:
        self.__store.clear()

    def check_count_element(self, count) -> bool:
        return True if (len(self.__store >= count)) else False

    def size(self) -> str:
        size_store = sys.getsizeof(self.__store)
        if size_store < 1024:
            return f"{size_store} B"
        elif 1024 <= size_store < (1024 * 1024):
            return f"{round(size_store / 1024, 2)} Kb"
        else:
            return f"{round(size_store / (1024 * 1024), 2)} Mb"
    
    def length(self) -> int:
        return len(self.__store)

