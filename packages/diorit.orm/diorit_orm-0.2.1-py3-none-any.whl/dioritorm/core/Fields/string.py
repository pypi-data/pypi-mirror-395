from dioritorm.core.data_field import DataField

class String(DataField):

    def __init__(self, owner = None):
        super().__init__(owner)
        self._len = 10
        self._value = ""

    @DataField.value.setter
    def value(self,val):
        # print("---val---")
        # print(val)
        if val is None:
            val = ""
        if not isinstance(val, str):
            raise ValueError("The 'value' property must be a string value.")
        DataField.value.fset(self, val[:self._len]) #Встановлюємо значення в межах заданої довжини

    @property
    def len(self):
         return self._len

    @len.setter
    def len(self,val):
        if not isinstance(val, int):
            raise ValueError("The 'value' property must be a integer value.")
        self._len = val


