from dioritorm.core.data_field import DataField


class Number(DataField):

    def __init__(self):
        super().__init__()
        self._value = 0  # Значення за замовчуванням
        self._min = None  # Мінімальне значення
        self._max = None  # Максимальне значення
        self._decimal_places = None  # Кількість знаків після коми

    @DataField.value.setter
    def value(self, val):
        #val = float(val.replace(",", "."))

        if not isinstance(val, (int, float)):
            raise ValueError("The 'value' property must be an integer or float.")
        if self._min is not None and val < self._min:
            raise ValueError(f"The value must be greater than or equal to {self._min}.")
        if self._max is not None and val > self._max:
            raise ValueError(f"The value must be less than or equal to {self._max}.")
        if self._decimal_places is not None:
            # Округлення до заданої кількості знаків після коми
            val = round(val, self._decimal_places)
        # DataField.value.fset(self, val[:self._len]) #TODO  тут якась проблема
        DataField.value.fset(self, val)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError("The 'min' property must be an integer or float.")
        self._min = val

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, val):
        if not isinstance(val, (int, float)):
            raise ValueError("The 'max' property must be an integer or float.")
        self._max = val

    @property
    def decimal_places(self):
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, val):
        if not isinstance(val, int) or val < 0:
            raise ValueError("The 'decimal_places' property must be a non-negative integer.")
        self._decimal_places = val
