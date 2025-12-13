from .base import Base

class Record(Base):
    registry = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Додаємо клас у реєстр за його ім'ям
        Record.registry[cls.__name__.lower()] = cls

    def save(self,connection = None, node = None):
        from dioritorm.core.event import Event
        #print("node",node.uuid.value)


        if connection is None:
            print("connection is None")

        self.beforeSave()
        self.onSave(connection)
        if node!=None:
            event = Event()
            event.context = self  # Передаємо контекст події
            event.save(node,connection)
        self.afterSave()

    @classmethod
    def getSchema(cls):
        from dioritorm.core.entity import Entity
        fields_schema = {}

        from .data_field import DataField

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

        return {
            "Entity": temp_instance._type + "_" + cls.__name__,
            "Fields": fields_schema
        }

    def restruct(self):
        from dioritorm.core.Database.databasemanager import DatabaseManger
        schema = self.getSchema()
        dm = DatabaseManger()

        # Основна таблиця
        dm.restruct({
            "Entity": schema["Entity"],
            "Fields": schema["Fields"]
        })

