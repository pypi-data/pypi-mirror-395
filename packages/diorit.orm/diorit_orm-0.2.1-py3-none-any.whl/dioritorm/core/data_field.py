import hashlib

#from .base import Base


class DataField:
    def __init__(self, owner = None):
        #super().__init__()
        self._required = False
        self._name = ""
        self._synonym = ""
        self._value = None
        self.isIndexed = False
        self.isUnique = False

        self._owner = owner


    def setObjectName(self):
        self._objectName="DataField"


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        if self._owner != None:
            self._owner.notifyChange()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,val):
        self._name = val

    @property
    def synonym(self):
        return self._synonym

    @synonym.setter
    def synonym(self,val):
        self._synonym = val

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self,val):
        if not isinstance(val, bool):
            raise ValueError("The 'required' property must be a boolean value.")
        self._required=val

