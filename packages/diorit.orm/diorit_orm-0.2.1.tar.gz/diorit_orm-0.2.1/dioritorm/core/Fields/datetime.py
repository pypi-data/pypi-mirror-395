from datetime import datetime
from dioritorm.core.data_field import DataField


class DateTime(DataField):

    def __init__(self):
        super().__init__()
        self._value = None  # Значення дати/часу
        self._format = "%Y-%m-%d %H:%M:%S"  # Формат за замовчуванням

    @DataField.value.setter
    def value(self, val):
        if val is None:
            return

        if isinstance(val, str):
            # Якщо передано рядок, намагаємося розпарсити його у datetime
            try:
                val = datetime.strptime(val, self._format)
            except ValueError:
                raise ValueError(f"The 'value' property must match the format '{self._format}'.")
        elif not isinstance(val, datetime):
            raise ValueError("The 'value' property must be a datetime object or a properly formatted string.")


        DataField.value.fset(self, val)




    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, val):
        if not isinstance(val, str):
            raise ValueError("The 'format' property must be a string.")
        self._format = val
