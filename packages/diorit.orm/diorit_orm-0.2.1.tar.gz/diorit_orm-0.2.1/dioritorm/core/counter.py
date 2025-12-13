from dioritorm.core.Database.Filter import Filter, FilterOperator
from dioritorm.core.Fields.string import String
from dioritorm.core.entity import Entity


class Counter(Entity):
    def __init__(self):
        super().__init__()
        self._type = 'count'

        self.entityName: String = String()
        self.entityName.len = 50
        self.entityName.value = ''

        self.lastNumber: String = String()
        self.lastNumber.len = 11
        self.lastNumber.value = ''

    def create_new_instance(self):
        return Counter()

    @classmethod
    def getCounterData(cls, entityName: String):
        counter = cls()
        counter.lastNumber.value = '0'

        filter = Filter().add("entityName", FilterOperator.CONTAINS, entityName.value)
        listRes = counter.getList(filter=filter, limit=1)

        if len(listRes) > 0:
            counter = listRes[0]

        return counter