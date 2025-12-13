from dioritorm.core.Fields.boolean import Boolean
from dioritorm.core.Fields.string import String
from dioritorm.core.entity import Entity
from dioritorm.core.counter import Counter

class Reference(Entity):
    def __init__(self):
        super().__init__()
        self.deleted = Boolean()
        self.deleted.value = False
        self._type = "ref"
        self.code = String() #This field is required
        self.code.len = 11
        self.name = String() #This field is required
        self.name.len = 50



    def refreshCounter(self, counter: Counter):
        counter.entityName.value = self.objectName.value
        counter.lastNumber.value = self.code.value
        counter.save()

    def beforeSave(self):
        if self.code.value == '':
            counter = Counter.getCounterData(self.objectName)
            self.code.value = str(int(counter.lastNumber.value) + 1)
            self.refreshCounter(counter)

    def markAsDeleted(self, is_deleted=True, connection=None, node=None):
        # Added helper to toggle logical deletion flag and persist the change.
        self.deleted.value = bool(is_deleted)
        self.save(connection, node)
