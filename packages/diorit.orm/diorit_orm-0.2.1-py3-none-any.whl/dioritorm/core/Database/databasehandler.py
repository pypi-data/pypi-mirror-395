from abc import ABC, abstractmethod
#from app.core.base import Base

class DatabaseHandler:
    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        pass

    def close(self):
        raise NotImplementedError

    def save(self,data):
        raise NotImplementedError

    def delete(self, entity, filter=None):
        # Changed: allow handlers to receive optional Filter for conditional deletes.
        raise NotImplementedError

    def get(self, entity_ref):
        raise NotImplementedError

    def getList(self,entity):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()
