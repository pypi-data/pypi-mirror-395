from dioritorm.core.data_field import DataField

class Boolean(DataField):

    def __init__(self):
        super().__init__()
        self._value = False

    @DataField.value.setter
    def value(self,val):
        #TODO: Тимчасвий перетворювач з числа в логічний тип
        """
        Потрібно додати якщо передається тектовий true чи false
        """
        if val==0:
            val = False
        else:
            val = True

        if not isinstance(val, bool):
            return
            #raise ValueError("The 'value' property must be a boolean value.")
        DataField.value.fset(self, val)