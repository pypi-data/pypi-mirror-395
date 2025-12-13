from dioritorm.core.entity import Entity


class TableSectionRecord(Entity):
    def __init__(self):
        super().__init__()

        self._type = "ts"

