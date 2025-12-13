from dioritorm.core.Sync.apimessage import ApiMessage
from dioritorm.core.constants import NULLLINK
from dioritorm.core.entity import Entity

from dioritorm.core.Database.databasemanager import DatabaseManger
from dioritorm.core.Fields.string import String
from dioritorm.core.Fields.number import Number
from dioritorm.core.Fields.boolean import Boolean
from dioritorm.core.Fields.datetime import DateTime
from dioritorm.core.table_section import TableSection
from dioritorm.core.Database.Filter import Filter, FilterOperator
from dioritorm.core.registry import (
    get_sync_entity,
    get_sync_events,
    get_sync_node,
)


"""Не видаляти. потрібно для визначення дочірнього класу"""
from dioritorm.core.event import Event

class SyncHandler:
    def __init__(self):
        #Це для того аби не видалялися імпорти при рефакторі
        Event()
        for event_cls in get_sync_events():
            event_cls()

        self.apiMessage = ApiMessage()

    def save(self, data, connection=None):
        # data – це вхідний словник (не називаємо його json)
        print("Try to save")
        obj = data.get("object")
        nodeUUID = data.get("node")

        if nodeUUID==None:
            nodeUUID=NULLLINK

        node_cls = get_sync_node()
        if node_cls is None:
            self.apiMessage.result = False
            self.apiMessage.messages.append("Sync node class is not registered.")
            return self.apiMessage

        node = node_cls()
        node.getByUUID(nodeUUID)
        print("node first -",nodeUUID)

        if obj is None:
            print("Warning: ключ 'object' відсутній")
        else:
            pass
            #print(obj + "55")

        className = obj.lower()  # можна використовувати для динамічного створення класу
        print("className",className)
        cls = Entity.registry.get(className)#TODO Перевірити чи не лишнє
        if not cls:
            from dioritorm.core.Record import Record
            cls = Record.registry.get(className)

        items = data.get("items", [])
        if connection==None:
            with DatabaseManger() as connection:
                for item in items:
                    self.saveObject(className,item,connection,node)
        else:
            for item in items:
                print('Try to save object $className');
                self.saveObject(className, item, connection, node)

        return self.apiMessage

    def clearByOwner(self,data,connection):
        pass


    def fillInTableSection(self,tableSection,data):

        dataItems = data.get("items")

        for dataItem in dataItems:
            row = tableSection.rows.add()
            for key, value in dataItem.items():


                field = getattr(row, key, None)

                if field is not None and isinstance(field, String):
                    field.value = value
                elif field is not None and isinstance(field, Number):
                    field.value = value
                elif field is not None and isinstance(field, Boolean):
                    field.value = value
                elif field is not None and isinstance(field, DateTime):
                    #field.value = value
                    field.value = value


                elif field is not None and isinstance(field, Entity):
                    field.uuid.value = value

    def saveObject(self,className,data,connection,node = None):

        cls = Entity.registry.get(className)
        if not cls:
            from dioritorm.core.Record import Record
            cls = Record.registry.get(className)

        if not cls:
            self.apiMessage.result = False
            self.apiMessage.messages.append(f"Клас '{className}' не знайдено.")
            return
            #raise ValueError(f"Клас '{className}' не знайдено.")
        obj = cls()
        obj.create()
        for key, value in data.items():
            # Формуємо ім'я атрибута, наприклад, "code" -> "_code"
            attr_name = "" + key #TODO можливо прибрати підкреслювання
            # Отримаємо поле, якщо воно існує

            print("attr_name",attr_name)

            field = getattr(obj, attr_name, None)

            print("field_type", type(field))
            # Якщо поле існує і є екземпляром класу String, встановлюємо його значення

            if (key=="childReference"):
                child = data.get("childReference")
                for childKey, childVal in child.items():
                    attr_name = childKey
                    self.save(childVal.get("data"),connection)

            if (key=="infoRecord"):
                child = data.get("infoRecord")
                for childKey, childVal in child.items():
                    attr_name = childKey
                    self.save(childVal.get("data"),connection)
                pass

            if field is not None and isinstance(field, String):
                field.value = value
            elif field is not None and isinstance(field, Number):
                field.value = value
            elif field is not None and isinstance(field, Boolean):
                field.value = value
            elif field is not None and isinstance(field, DateTime):
                # if isinstance(value, str):
                #     from datetime import datetime
                #     value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                # if hasattr(value, 'replace'):
                #     value = value.replace(microsecond=0)
                field.value = value
                
            elif field is not None and isinstance(field, Entity):
                field.uuid.value = value
            elif field is not None and isinstance(field, TableSection):
                print("TableSection",field.name)

                self.fillInTableSection(field,value)
                    #print("child.product._uuid",child.product._uuid)

            else:
                print(f"Попередження: Властивість {attr_name} відсутня або не є типу String")
                pass



        obj.save(connection, node)

    def get(self, data):
        cls = get_sync_entity()
        if cls is None:
            self.apiMessage.result = False
            self.apiMessage.messages.append("Sync entity class is not registered.")
            return self.apiMessage

        filter = Filter()
        filter.add("node", FilterOperator.EQUALS, data.get("node"))
        filter.and_logic()
        filter.add("state", FilterOperator.EQUALS, 0)

        # Обробляємо фільтр по entity
        entities_filter = data.get("filter")
        if entities_filter:
            # Отримаємо список імен таблиць з фільтру
            entity_names = [f.get("entity") for f in entities_filter if f.get("entity")]

            # Додаємо умову до фільтру, якщо є entity
            if entity_names:
                print("entity_names", entity_names)

                filter.and_logic()
                filter.add("tableName", FilterOperator.IN, entity_names)


        sync_entities = cls.getList(filter,None,data.get("limit"))

        result = []

        for item in sync_entities:
            className = item.tableName.value

            #print(item.node.uuid.value)
            cls = Entity.registry.get(className.lower())  # Використовуємо нижній регістр
            if not cls:
                self.apiMessage.result = False
                self.apiMessage.messages.append(f"Клас '{className}' не знайдено.")
                return self.apiMessage
                #raise ValueError(
                #    f"Клас '{className}' не знайдено.")  # TODO З уим потрібно буде подумати. Яка поведінка при відсутності класу
            obj = cls()
            obj.create()

            print(item.entityUUID.uuid.value)

            obj.getByUUID(item.entityUUID.uuid.value)
            #obj.uuid.value = "111"
            # Додаємо отриманий об'єкт до списку результатів
            result.append(obj.toDict())


        return result

