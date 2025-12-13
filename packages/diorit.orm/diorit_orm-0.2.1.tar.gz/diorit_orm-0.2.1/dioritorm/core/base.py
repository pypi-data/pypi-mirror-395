import uuid
from .constants import  NAMESPACE

import  json

from dioritorm.core.Fields.string import String
from dioritorm.core.Database.databasemanager import DatabaseManger
import hashlib
from dioritorm.core.Fields.boolean import Boolean
from dioritorm.core.Fields.number import Number
from dioritorm.core.Fields.datetime import DateTime


#from abc import ABC,abstractmethod

class Base:

    def __init__(self):
        self._objectName = String()
        self._objectName.len = 50
        self._objectName.value = self.__class__.__name__
        if not self._objectName:
            raise ValueError("setObjectName must set a valid object name!")
        self._objectUUID = String()
        self._objectUUID.len = 36
        self._objectUUID.value = str(uuid.uuid5(NAMESPACE, self._objectName.value))
        self.isIndexed = True
        self.isUnique = False

        #logging.info(f"Object created: {self._objectName}, UUID: {self._objectUUID}")

    def __del__(self):
       pass

    def beforeCreate(self):
        pass

    def onCreate(self):
        pass

    def afterCreate(self):
        pass

    def create(self):
        from dioritorm.core.event import Event
        self.beforeCreate()
        self.onCreate()
        self.afterCreate()
        event = Event()
        event.create()
        pass

    def beforeSave(self):
        pass

    def onSave(self,connection = None):

        if connection is None:
            connection = DatabaseManger()
            connection.save(self.toDict())
        else:
            connection.save(self.toDict(),connection)#Це треба звести в одну функцыю


    def afterSave(self):
        pass


    @property
    def objectUUID(self):
        return self._objectUUID

    @property
    def objectName(self):
        return self._objectName

    def toDict(self):
        from dioritorm.core.table_section import TableSection
        from dioritorm.core.data_field import DataField
        from dioritorm.core.entity import Entity

        result = {}
        table_sections = {}

        for attr, value in self.__dict__.items():
            if callable(value):  # 🛑 Пропустити методи
                continue
            if isinstance(value, DataField):
                if isinstance(value, DateTime) and value.value:
                    from datetime import datetime
                    if isinstance(value.value, datetime):
                        # Конвертуємо datetime в рядок у потрібному форматі
                        result[attr] = value.value.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        result[attr] = value.value
                else:
                    result[attr] = value.value


            elif isinstance(value, Entity):
                result[attr] = value.uuid.value
            elif isinstance(value, TableSection):
                rows_list = []
                for row in value.rows:
                    row_data = {}
                    for col_name, col_value in row.data.items():
                        if isinstance(col_value, DataField):
                            row_data[col_name] = col_value.value
                        elif isinstance(col_value, Entity):
                            row_data[col_name] = col_value.uuid.value
                        else:
                            row_data[col_name] = col_value
                    rows_list.append(row_data)
                #table_name = value._objectName.value.lower()
                table_name = value.name
                table_sections[table_name] = rows_list
            elif isinstance(value, list):
                continue
            else:
                result[attr] = value

        if table_sections:
            result["TableSections"] = table_sections

        return result

    """    def toDict(self):
        result = {}
        for attr, value in self.__dict__.items():
            from app.core.table_section import TableSection
            if isinstance(value, DataField):
                print("DataField",value.value)
                result[attr] = value.value
            elif isinstance(value, Base):
                print("Base", attr ,value._uuid.value)
                result[attr] = value._uuid.value

            else:
                result[attr] = value
        return result"""

    def toJson(self):
        return json.dumps(self.toDict())

    @staticmethod
    def _map_type(value):
        from dioritorm.core.entity import Entity
        if isinstance(value, String):  # Якщо це Field
            return {
                "type": "VARCHAR",
                "len": value.len,
                "isIndexed": getattr(value, "isIndexed", False),
                "isUnique": getattr(value, "isUnique", False)
            }
        elif isinstance(value, Boolean):  # Якщо це Field
            return {
                "type": "tinyint(1)",
                "isIndexed": getattr(value, "isIndexed", False),
                "isUnique": getattr(value, "isUnique", False)
            }
        elif isinstance(value, Number):  # Якщо це Field
            return {
                "type": "DOUBLE", 
                "isIndexed": getattr(value, "isIndexed", False),
                "isUnique": getattr(value, "isUnique", False)
            }
        elif isinstance(value, DateTime):  # Якщо це Field
            return {
                "type": "DATETIME", 
                "isIndexed": getattr(value, "isIndexed", False),
                "isUnique": getattr(value, "isUnique", False)
            }
        elif isinstance(value, Entity):  # Якщо це Entity (Foreign Key)
            return {
                "type": "VARCHAR",
                "len": 36,
                "isIndexed": getattr(value, "isIndexed", False),
                "isUnique": getattr(value, "isUnique", False)
            }
        else:
            return "BLOB"  # Заглушка для складних типів

    @classmethod
    def getSignature(cls):
        schema_str = json.dumps(cls.getSchema(), sort_keys=True)
        return hashlib.sha256(schema_str.encode()).hexdigest()

    @classmethod
    def getList(cls, filter=None, order_by=None, limit=None, offset=None):
        # Створюємо екземпляр для передачі в handler
        instance = cls()
        connection = DatabaseManger()
        return connection.getList(instance, filter, order_by, limit, offset)