from enum import Enum


class FilterOperator(Enum):
    EQUALS = "=="
    IN = "IN"
    NOT_EQUALS = "!="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUALS = ">="
    LESS_EQUALS = "<="
    CONTAINS = "LIKE"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"


class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"


class Filter:
    def __init__(self):
        self.conditions = []
        self.logical_operator = LogicalOperator.AND

    def add(self, field, operator, value):
        """
        Додає умову фільтрації

        :param field: Поле для фільтрації
        :param operator: Оператор фільтрації (з FilterOperator)
        :param value: Значення для порівняння
        """
        self.conditions.append({
            "field": field,
            "operator": operator,
            "value": value
        })
        return self

    def and_logic(self):
        """Встановлює логічний оператор AND між умовами"""
        self.logical_operator = LogicalOperator.AND
        return self

    def or_logic(self):
        """Встановлює логічний оператор OR між умовами"""
        self.logical_operator = LogicalOperator.OR
        return self

    def to_sql(self):
        """
        Конвертує фільтр в SQL WHERE умову

        :return: tuple(рядок SQL, параметри)
        """
        if not self.conditions:
            return "", []

        sql_parts = []
        params = []

        for condition in self.conditions:
            field = condition["field"]
            op = condition["operator"]
            value = condition["value"]

            if op == FilterOperator.EQUALS:
                sql_parts.append(f"{field} = %s")
                params.append(value)
            elif op == FilterOperator.IN:
                if not isinstance(value, (list, tuple)) or not value:
                    sql_parts.append("FALSE")  # Ніколи не спрацює, якщо список порожній
                else:
                    placeholders = ', '.join(['%s'] * len(value))
                    sql_parts.append(f"{field} IN ({placeholders})")
                    params.extend(value)
            elif op == FilterOperator.NOT_EQUALS:
                sql_parts.append(f"{field} != %s")
                params.append(value)
            elif op == FilterOperator.GREATER:
                sql_parts.append(f"{field} > %s")
                params.append(value)
            elif op == FilterOperator.LESS:
                sql_parts.append(f"{field} < %s")
                params.append(value)
            elif op == FilterOperator.GREATER_EQUALS:
                sql_parts.append(f"{field} >= %s")
                params.append(value)
            elif op == FilterOperator.LESS_EQUALS:
                sql_parts.append(f"{field} <= %s")
                params.append(value)
            elif op == FilterOperator.CONTAINS:
                sql_parts.append(f"{field} LIKE %s")
                params.append(f"%{value}%")
            elif op == FilterOperator.STARTS_WITH:
                sql_parts.append(f"{field} LIKE %s")
                params.append(f"{value}%")
            elif op == FilterOperator.ENDS_WITH:
                sql_parts.append(f"{field} LIKE %s")
                params.append(f"%{value}")

        logical_op = f" {self.logical_operator.value} "
        return logical_op.join(sql_parts), params
