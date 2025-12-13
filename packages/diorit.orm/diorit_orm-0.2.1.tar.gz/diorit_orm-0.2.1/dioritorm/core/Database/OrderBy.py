from enum import Enum


class OrderDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


class OrderBy:
    def __init__(self):
        self.order_fields = []

    def add(self, field, direction=OrderDirection.ASC):
        """
        Додає поле для сортування

        :param field: Поле для сортування
        :param direction: Напрямок сортування (за замовчуванням ASC)
        """
        self.order_fields.append({
            "field": field,
            "direction": direction
        })
        return self

    def to_sql(self):
        """
        Конвертує параметри сортування в SQL ORDER BY умову

        :return: рядок SQL ORDER BY
        """
        if not self.order_fields:
            return ""

        order_parts = []

        for order in self.order_fields:
            field = order["field"]
            direction = order["direction"].value
            order_parts.append(f"{field} {direction}")

        return ", ".join(order_parts)