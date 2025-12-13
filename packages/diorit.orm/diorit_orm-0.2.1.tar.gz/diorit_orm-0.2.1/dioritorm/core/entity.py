import uuid

from .base import Base
from .constants import NULLLINK

from dioritorm.core.Fields.string import String
from dioritorm.core.Database.databasemanager import DatabaseManger
from .event import Event


class Entity(Base):
    registry = {}  # глобальний реєстр для всіх підкласів

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Додаємо клас у реєстр за його ім'ям
        Entity.registry[cls.__name__.lower()] = cls
        #pprint(Entity.registry)

    def __init__(self):
        super().__init__()
        self._type = ""
        self.uuid = String()
        self.uuid.len = 36
        self.uuid.value = NULLLINK
        self.uuid.isIndexed = True
        self.uuid.isUnique = True

        self._callBacks = list()


    def addCallback(self, func):
        self._callBacks.append(func)

    def notifyChange(self):
        for func in self._callBacks:
            func()

    #@property
    def ref(self):
        return self.uuid.value


    def getByUUID(self,uuid):
        connection = DatabaseManger()
        return connection.getByUUID(self, uuid)


    def save(self,connection = None, node = None):



        if self.uuid.value == "00000000-0000-0000-0000-000000000000":
            self.uuid.value= str(uuid.uuid4())


        self.beforeSave()
        self.onSave(connection)
        event = Event()
        event.context = self  # Передаємо контекст події
        event.save(node,connection)
        self.afterSave()

    def restruct(self):
        schema = self.getSchema()
        dm = DatabaseManger()

        # Основна таблиця
        dm.restruct({
            "Entity": schema["Entity"],
            "Fields": schema["Fields"]
        })

        # Табличні частини
        if "TableSections" in schema:
            for section_schema in schema["TableSections"].values():
                dm.restruct(section_schema)


    """@classmethod
    def _map_type(cls, value):
        # Простий приклад мапінгу типів, можна налаштувати під свої потреби
        return type(value).__name__"""

    @classmethod
    def getSchema(cls):
        fields_schema = {}

        from .data_field import DataField
        from dioritorm.core.table_section import TableSection

        try:
            temp_instance = cls()
            if hasattr(temp_instance, "create"):
                temp_instance.create()
        except Exception as e:
            print("Не вдалося створити екземпляр класу:", e)
            return {"Entity": cls.__name__, "Fields": fields_schema}

        for attr, value in temp_instance.__dict__.items():
            if attr in ["_objectName", "_objectUUID"]:
                continue

            if isinstance(value, (DataField, Entity, cls)):
                fields_schema[attr] = cls._map_type(value)

        table_sections = {}
        for attr, value in temp_instance.__dict__.items():
            if isinstance(value, TableSection):
                section_fields = {
                    "uuid": {"type": "VARCHAR", "len": 36, "isIndexed": True},
                    "owner": {"type": "VARCHAR", "len": 36, "isIndexed": True}
                }

                for col in value.columns:
                    try:
                        section_fields[col.name] = cls._map_type(col.type())
                        if isinstance(col.type(), String):
                            section_fields[col.name]["len"] = col._len if hasattr(col,'_len') and col._len is not None else col.type().len
                    except Exception as e:
                        print(f"Помилка при обробці поля '{col.name}' табличної частини '{attr}':", e)

                section_table_name = value._objectName.value
                table_sections[section_table_name] = {
                    "Entity": section_table_name,
                    "Fields": section_fields
                }

        return {
            "Entity": temp_instance._type + "_" + cls.__name__,
            "Fields": fields_schema,
            "TableSections": table_sections
        }




