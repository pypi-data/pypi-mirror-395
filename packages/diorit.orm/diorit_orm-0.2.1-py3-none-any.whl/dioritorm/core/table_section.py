from typing import Any,  List, Optional, Type
from dioritorm.core.data_field import DataField
from dioritorm.core.Fields.string import String
from dioritorm.core.entity import Entity

class TableSection:
    def __init__(self, name: str, owner: Any):
        self._ownerName = ""
        if isinstance(owner,Entity):
            self._ownerName = owner.objectName.value
        self._type = "ts_"
        self._objectName = String()
        self._objectName.len = 50
        self._objectName.value =  self._type+self._ownerName+name
        self._name = name;
        #print("self._objectName.value",self._objectName.value)

        self._owner = owner
        self._columns = Columns(owner=self)
        self._rows = Rows(owner=self)
        self._rows.set_columns(self._columns)
        self._current_row: Optional[Row] = None

    def add_column(self, name: str, col_type: Type[Any]) -> "Column":
        return self._columns.add(name, col_type)

    def add_row(self) -> "Row":
        row = self._rows.add()
        self._current_row = row
        return row
    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> "Columns":
        return self._columns

    @property
    def rows(self) -> "Rows":
        return self._rows

    @property
    def current_row(self) -> Optional["Row"]:
        return self._current_row

    def __repr__(self) -> str:
        return f"TableSection(name={self._objectName.value!r}, columns={self._columns}, rows={self._rows})"


class Column:
    def __init__(self, owner: "Columns", name: str, col_type: Type[Any],len=None):
        self._len = None
        self._owner = owner
        self._name = name
        self._type = col_type
        #if isinstance(col_type(),String):
        self._len = len

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> Type[Any]:
        return self._type

    @property
    def len(self):
        return self._len

    def __repr__(self) -> str:
        return f"Column(name={self._name!r}, type={self._type.__name__})"


class Columns:
    def __init__(self, owner: TableSection):
        self._owner = owner
        self._columns: List[Column] = []

    def add(self, name: str, col_type: Type[Any],len = None) -> Column:
        col = Column(owner=self, name=name, col_type=col_type,len=len)
        self._columns.append(col)
        return col

    def __iter__(self):
        return iter(self._columns)

    def __len__(self) -> int:
        return len(self._columns)

    def __getitem__(self, index: int) -> Column:
        return self._columns[index]

    def __repr__(self) -> str:
        return repr(self._columns)


class Row:
    def __init__(self, owner: "Rows"):
        # Встановлюємо ці атрибути через object.__setattr__,
        # щоб не зацікавити власний __setattr__
        object.__setattr__(self, "_owner", owner)
        object.__setattr__(self, "data", {})

    def __getattr__(self, name: str) -> Any:
        # Якщо звертаються до row.<column>, і таке поле є в data — повертаємо його
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"{self.__class__.__name__!r} has no attribute {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        # Якщо в data уже є ключ name — пишемо туди, інакше створюємо звичайний атрибут
        if "data" in self.__dict__ and name in self.data:
            self.data[name] = value
        else:
            object.__setattr__(self, name, value)

    def delete(self) -> None:
        self._owner.remove(self)

    def __repr__(self) -> str:
        return f"Row({self.data})"


class Rows:
    def __init__(self, owner: TableSection):
        self._owner = owner
        self._columns: Optional[Columns] = None
        self._rows: List[Row] = []

    def set_columns(self, columns: Columns) -> None:
        self._columns = columns

    def add(self) -> Row:
        """
        Створює новий Row і для кожної колонки:
          - якщо type — підклас DataField, створює екземпляр і зберігає його в data
          - якщо type — підклас Entity, створює екземпляр, викликає .create(), і зберігає його
          - інакше зберігає None
        """
        row = Row(owner=self)
        if self._columns:
            for col in self._columns:
                col_cls = col.type
                if isinstance(col_cls, type) and issubclass(col_cls, DataField):
                    # створюємо нове поле, наприклад String(), Boolean()…

                    if issubclass(col_cls, String):
                        field = col_cls()
                        field.len = col.len
                        row.data[col.name] = field
                        pass
                    else:
                        field = col_cls()
                        row.data[col.name] = field
                elif isinstance(col_cls, type) and issubclass(col_cls, Entity):
                    # створюємо під-об’єкт, ініціалізуємо його .create()
                    ent = col_cls()
                    ent.create()
                    row.data[col.name] = ent
                else:
                    # прості типи (str,int тощо) — або None, або дефолт col_cls()
                    try:
                        row.data[col.name] = col_cls()
                    except Exception:
                        row.data[col.name] = None

        self._rows.append(row)
        return row

    def remove(self, row: Row) -> None:
        if row in self._rows:
            self._rows.remove(row)

    def __iter__(self):
        return iter(self._rows)

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, index: int) -> Row:
        return self._rows[index]

    def __repr__(self) -> str:
        return repr(self._rows)