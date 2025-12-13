from dioritorm.core.Fields.datetime import DateTime
from dioritorm.core.Record import Record


class InfoRecord(Record):
    def __init__(self):
        super().__init__()

 #       self.isPeriodical = False
        self._type = "infrec"

        self.period = DateTime()

        self.resources = []

    # def restruct(self):
    #     if self.isPeriodical:
    #         from app.core.Database.databasemanager import DatabaseManger
    #         schema = self.getSchema()
    #         dm = DatabaseManger()
    #
    #         # Основна таблиця
    #         dm.restruct({
    #             "Entity": schema["Entity"],
    #             "Fields": schema["Fields"]
    #         })
    #
    #
    #
    #         dm.restruct({
    #             "Entity": schema["Entity"],
    #             "Fields": schema["Fields"]
    #         })
    #         pass
    #     else:
    #         super().restruct()
    #     # from app.core.Database.databasemanager import DatabaseManger
    #     # schema = self.getSchema()
    #     # dm = DatabaseManger()
    #     #
    #     # # Основна таблиця
    #     # dm.restruct({
    #     #     "Entity": schema["Entity"],
    #     #     "Fields": schema["Fields"]
    #     # })
