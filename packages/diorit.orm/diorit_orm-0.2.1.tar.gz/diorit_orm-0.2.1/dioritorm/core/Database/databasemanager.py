#from app.core.base import Base
from dioritorm.core.constants import *
from .mysqlhandler import MySQLHandler
from .sqllitehandler import SQLiteHandler

class DatabaseManger:

    def __init__(self):
        super().__init__()
        self.databaseType = DATABASE_TYPE
        self.handlers = {
            "mysql":MySQLHandler(),
            "sqllite":SQLiteHandler()
        }

    def _getHandler(self):
        if self.databaseType not in self.handlers:
            raise ValueError(f"Unsupported database type: {self.databaseType}")
        return self.handlers[self.databaseType]

    def save(self,data,connection = None):
        handler = self._getHandler()
        #handler.save(table_name, json_data)
        handler.save(data,connection)

    def getByUUID(self,entity,ref):
        handler = self._getHandler()
        handler.getByUUID(entity,ref)

    def delete(self,entity,filter=None):
        handler = self._getHandler()
        handler.delete(entity,filter)  # Changed: forward entity and optional Filter to handler-level delete logic.


    def getList(self,entity,filter=None, orderBy=None, limit=None, offset=None):
        handler = self._getHandler()
        return handler.getList(entity,filter,orderBy,limit,offset)

    def close(self):
        handler = self._getHandler()
        handler.close()

    def restruct(self,schema):
        handler = self._getHandler()
        handler.restruct(schema)
        pass

    def __enter__(self):
        handler = self._getHandler()
        return  handler

    def __exit__(self, exc_type, exc_value, traceback):
        handler = self._getHandler()
        if exc_type:
            handler.connect().rollback()
        else:
            handler.connect().commit()
        handler.close()
