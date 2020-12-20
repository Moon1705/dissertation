class DataStore:

    def __init__(self, store=set()) -> None:
        self.store = store

    def write(self, event) -> None:
        self.store.add(event)

    def read_all(self) -> set:
        return self.store

    def delete_all(self) -> None:
        self.store.clear()

    def check_count_element(self, count) -> bool:
        return True if (len(self.store >= count)) else False

