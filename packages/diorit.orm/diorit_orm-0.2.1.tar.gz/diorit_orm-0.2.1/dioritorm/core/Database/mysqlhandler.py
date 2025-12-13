from .databasehandler import DatabaseHandler
import mysql.connector
from mysql.connector import Error
from dioritorm.core.constants import DATABASE_PATH, DATABASE_USER, DATABASE_PWD, DATABASE_NAME, NULLLINK


#from ..core.table_section import TableSection


class MySQLHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        self._connection = None
        self._cursor = None
        self.init()
        #self.get()

    def init(self):
        try:
            # Підключення до бази даних
            self._connection = mysql.connector.connect(
                host=DATABASE_PATH,        # або IP-адреса сервера
                user=DATABASE_USER,        # ваш логін
                password=DATABASE_PWD,      # ваш пароль
                database=DATABASE_NAME      # назва бази даних
            )
        except Error as e:
            print("Сталася помилка при роботі з MySQL:", e)


    def connect(self):
        return self._connection



    def close(self):
        return self._connection.close()

    def getByUUID(self, entity, entity_ref):
        from dioritorm.core.entity import Entity
        from dioritorm.core.data_field import DataField
        from dioritorm.core.table_section import TableSection
        print("Отримую дані обєкта")
        try:
            if not self._connection or not self._connection.is_connected():
                self.init()

            if not entity:
                return None

            # Перевіряємо чи entity_ref це об'єкт Entity
            if not isinstance(entity, Entity):
                print("Ідентифікатор UUID без типу об'єкта.")
                return None

            # Формуємо ім'я таблиці на основі типу та імені об'єкта
            table_name = f"{entity._type}_{entity._objectName.value.lower()}"

            self._cursor = self._connection.cursor(dictionary=True)  # Повертати результати як словники

            fields = []
            joins = []

            for name, value in entity.__dict__.items():
                if not name.startswith('_'):
                    if isinstance(value, Entity):
                        from dioritorm.core.reference import Reference
                        from dioritorm.core.document import Document
                        if isinstance(value, Reference):
                            fields.append(f"{table_name}.{name} as {name}")
                            fields.append(f"{name}.name as {name}_name")
                            joins.append(f"LEFT JOIN {value._type}_{value._objectName.value.lower()} as {name} ON {name}.uuid={table_name}.{name}")
                        elif isinstance(value, Document):
                            fields.append(f"{table_name}.{name} as {name}")
                            fields.append(f"{name}.number as {name}_number")
                            fields.append(f"{name}.datedoc as {name}_datedoc")
                            joins.append(f"LEFT JOIN {value._type}_{value._objectName.value.lower()} as {name} ON {name}.uuid={table_name}.{name}")
                    elif isinstance(value, DataField):
                        fields.append(f"{table_name}.{name} as {name}")

            # Запит для отримання об'єкту за UUID

            query = f"SELECT {','.join(map(str, fields))} FROM {table_name} {' '.join(map(str, joins))} WHERE {table_name}.uuid = %s"
            print(query)
            self._cursor.execute(query, (entity_ref,))
            record = self._cursor.fetchone()

            if record:
                print("Заповнюємо всі поля з record")
                # Заповнюємо всі поля з record
                for field_name, field_value in record.items():
                    if field_name == 'TableSections':
                        continue  # TableSections обробляємо окремо
                    if hasattr(entity, field_name):
                        field = getattr(entity, field_name)
                        if isinstance(field, DataField):  # якщо це DataField
                            if field_value is not None:
                                field.value = field_value
                        elif isinstance(field, Entity):
                            if field_value is not None:
                                field.uuid.value = field_value
                            else:
                                field.uuid.value = NULLLINK
                            if isinstance(field, Reference):
                                if record[f'{field_name}_name'] is not None:
                                    field.name.value = record[f'{field_name}_name']
                            elif isinstance(field, Document):
                                if record[f'{field_name}_number'] is not None:
                                    field.number.value = record[f'{field_name}_number']
                                if record[f'{field_name}_datedoc'] is not None:
                                    field.datedoc.value = record[f'{field_name}_datedoc']
                        else:  # якщо це звичайний атрибут
                            setattr(entity, field_name, field_value)
                # Знаходимо всі табличні частини в об'єкті
                for attr_name in dir(entity):
                    # Розглядаємо тільки атрибути з підкресленням
                    try:
                        attr_value = getattr(entity, attr_name)
                        # Перевіряємо, чи це TableSection
                        if isinstance(attr_value, TableSection):
                            print(f"Знайдено табличну частину: {attr_name}")

                            # Отримуємо ім'я таблиці з табличної частини
                            ts_name = attr_value._objectName.value
                            ts_name_sql = attr_value._objectName.value

                            # Запит для отримання записів з табличної частини
                            fields = []
                            joins = []
                            for col in attr_value.columns:
                                a = col.type()
                                if isinstance(a, Reference):
                                    fields.append(f"{ts_name_sql}.{col.name} as {col.name}")
                                    fields.append(f"{col.name}.name as {col.name}_name")
                                    joins.append(
                                        f"LEFT JOIN {a._type}_{a._objectName.value}  as {col.name} ON {col.name}.uuid={ts_name_sql}.{col.name}")
                                elif isinstance(a, Document):
                                    fields.append(f"{ts_name_sql}.{col.name} as {col.name}")
                                    fields.append(f"{col.name}.number as {col.name}_number")
                                    fields.append(f"{col.name}.datedoc as {col.name}_datedoc")
                                    joins.append(
                                        f"LEFT JOIN {a._type}_{a._objectName.value} as {col.name} ON {col.name}.uuid={ts_name_sql}.{col.name}")
                                elif isinstance(a, DataField):
                                    fields.append(f"{ts_name_sql}.{col.name} as {col.name}")
                            ts_query = f"SELECT {','.join(map(str, fields))} FROM {ts_name_sql} {' '.join(map(str, joins))} WHERE {ts_name_sql}.owner = %s"

                            self._cursor.execute(ts_query, (entity_ref,))
                            ts_records = self._cursor.fetchall()

                            print(f"Знайдено {len(ts_records)} записів для табличної частини {ts_name}")
                            # Додаємо нові рядки з даних з бази
                            for ts_record in ts_records:
                                # Додаємо новий рядок
                                row = attr_value.rows.add()

                                # Заповнюємо дані рядка
                                for col_name, col_value in ts_record.items():
                                    if col_name not in ('owner', 'uuid'):
                                        # Перевіряємо, чи доступно поле через row.data
                                        if hasattr(row, 'data') and isinstance(row.data, dict):
                                            if col_name in row.data:
                                                col_obj = row.data[col_name]
                                                if hasattr(col_obj, 'value'):  # DataField
                                                    col_obj.value = col_value
                                                elif hasattr(col_obj, 'uuid') and hasattr(col_obj.uuid,
                                                                                          'value'):  # Entity
                                                    if col_value is not None:
                                                        col_obj.uuid.value = col_value
                                                    else:
                                                        col_obj.uuid.value = NULLLINK
                                                    if isinstance(col_obj, Reference):
                                                        if ts_record[f'{col_name}_name'] is not None:
                                                            col_obj.name.value = ts_record[f'{col_name}_name']
                                                    elif isinstance(col_obj, Document):
                                                        if ts_record[f'{col_name}_number'] is not None:
                                                            col_obj.number.value = ts_record[f'{col_name}_number']
                                                        elif ts_record[f'{col_name}_datedoc'] is not None:
                                                            col_obj.datedoc.value = ts_record[f'{col_name}_datedoc']
                                                else:
                                                    row.data[col_name] = col_value
                                        # Або перевіряємо як атрибут рядка
                                        elif hasattr(row, col_name):
                                            col_field = getattr(row, col_name)
                                            if hasattr(col_field, 'value'):  # DataField
                                                col_field.value = col_value
                                            elif hasattr(col_field, 'uuid') and hasattr(col_field.uuid,
                                                                                        'value'):  # Entity
                                                col_field.uuid.value = col_value
                                            else:
                                                setattr(row, col_name, col_value)
                    except Exception as e:
                        print(f"Помилка при обробці атрибуту {attr_name}: {e}")
                        continue

                return entity
            else:
                return None

        except Exception as e:
            print(f"Сталася помилка при отриманні даних з бази: {e}")
            import traceback
            traceback.print_exc()
            return None

        finally:
            if self._cursor is not None:
                self._cursor.close()
                self._cursor = None

    def save(self, data, connection=None):
        import uuid

        auto_commit = False
        if connection is None:
            connection = self.connect()
            auto_commit = True
        else:
            connection = connection.connect()

        table_name = f"{data['_type'].lower()}_{data['_objectName'].lower()}"
        data_to_save = {k: v for k, v in data.items() if
                        k not in ["_objectName", "_objectUUID", "isIndexed", "isUnique", "_type", "TableSections"]}

        cursor = connection.cursor()
        
        # Формуємо колонки та значення для INSERT
        columns = ", ".join(data_to_save.keys())
        placeholders = ", ".join(["%s"] * len(data_to_save))
        
        # Формуємо частину ON DUPLICATE KEY UPDATE
        update_parts = []
        for key in data_to_save.keys():
            if key != "uuid":  # Не оновлюємо _uuid
                update_parts.append(f"{key}=VALUES({key})")
        
        update_clause = ", ".join(update_parts)
        
        # Єдиний INSERT ... ON DUPLICATE KEY UPDATE запит
        query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {update_clause}
        """
        
        cursor.execute(query, tuple(data_to_save.values()))
        
        # Обробка табличних частин залишається без змін
        if "TableSections" in data:
            main_uuid = data_to_save["uuid"]
            for ts_name, rows in data["TableSections"].items():
                # Видалити всі старі записи

                del_query = f"DELETE FROM ts_{data['_objectName']}{ts_name} WHERE owner = %s" #TODO: Тут переробити з назвою таблиці.Можливо перепісити на клас
                print("del_query")
                print(del_query)
                print("del_query")
                cursor.execute(del_query, (main_uuid,))

                # Вставити нові записи
                for row in rows:
                    row["uuid"] = str(uuid.uuid4())
                    row["owner"] = main_uuid
                    columns = ", ".join(row.keys())
                    placeholders = ", ".join(["%s"] * len(row))
                    insert_query = f"INSERT INTO ts_{data['_objectName']}{ts_name} ({columns}) VALUES ({placeholders})"#TODO: Тут переробити з назвою таблиці.Можливо перепісити на клас
                    cursor.execute(insert_query, tuple(row.values()))

        if auto_commit:
            connection.commit()

        cursor.close()


    def commit(self):
        pass

    def rollback(self):
        pass

    def delete(self, entity, filter=None):
        # Changed: implement conditional delete analogous to getList for MySQL backend.
        from dioritorm.core.entity import Entity

        if not self._connection or not self._connection.is_connected():
            self.init()

        if not isinstance(entity, Entity):
            raise ValueError("delete requires an Entity instance.")

        if filter is None or not getattr(filter, "conditions", None):
            raise ValueError("delete requires a non-empty Filter to avoid wiping entire tables.")

        table_name = f"{entity._type}_{entity._objectName.value.lower()}"
        where_sql, params = filter.to_sql()
        if not where_sql:
            raise ValueError("delete requires Filter to produce SQL clauses.")

        cursor = self._connection.cursor()
        try:
            query = f"DELETE FROM {table_name} WHERE {where_sql}"
            cursor.execute(query, params)
            self._connection.commit()
        except Error as e:
            self._connection.rollback()
            raise
        finally:
            cursor.close()

    def restruct(self, schema):
        table_name = schema["Entity"].lower()
        desired_fields = schema["Fields"]

        # if not self._connection or not self._connection.is_connected():
        #     self.init()

        # Налагоджувальне повідомлення про поля та їх атрибути
        print(f"Обробка таблиці {table_name}")
        for field_name, field_def in desired_fields.items():
            if isinstance(field_def, dict):
                isIndexed = field_def.get("isIndexed", False)
                isUnique = field_def.get("isUnique", False)
                isUnic = field_def.get("isUnic", False)
                print(f"Поле {field_name}: isIndexed={isIndexed}, isUnique={isUnique}, isUnic={isUnic}")

        # Допоміжна функція для отримання визначення стовпця
        def get_column_definition(col, definition):
            if isinstance(definition, dict):
                col_type = definition.get("type")
                length = definition.get("len")
                if length:
                    return f"{col_type}({length})"
                else:
                    return col_type
            else:
                return definition

        # Перевірка, чи існує таблиця
        check_query = """
            SELECT COUNT(*)
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s
        """
        self._cursor = self._connection.cursor()
        self._cursor.execute(check_query, (DATABASE_NAME, table_name))
        table_exists = self._cursor.fetchone()[0] > 0
        self._cursor.close()

        if not table_exists:
            # Створення таблиці
            columns_definitions = []
            for col, definition in desired_fields.items():
                col_def = f"{col} {get_column_definition(col, definition)}"
                columns_definitions.append(col_def)
            create_stmt = f"CREATE TABLE {table_name} ({', '.join(columns_definitions)})"
            self._cursor = self._connection.cursor()
            try:
                self._cursor.execute(create_stmt)
                self._connection.commit()
                print(f"Таблиця {table_name} створена.")
            except Error as e:
                print("Помилка при створенні таблиці:", e)
            finally:
                self._cursor.close()

            # Додавання індексів (тільки для полів, де isIndexed=True)
            for col, definition in desired_fields.items():
                if isinstance(definition, dict) and definition.get("isIndexed"):
                    idx_name = f"idx_{col}"
                    add_idx_stmt = f"ALTER TABLE {table_name} ADD INDEX {idx_name} ({col})"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(add_idx_stmt)
                        self._connection.commit()
                        print(f"Додано індекс {idx_name} для стовпця {col}.")
                    except Error as e:
                        print("Помилка при додаванні індексу:", e)
                    finally:
                        self._cursor.close()

            # Збираємо унікальні поля та створюємо лише один об'єднаний унікальний індекс
            unic_fields = []
            for col, definition in desired_fields.items():
                if isinstance(definition, dict) and (definition.get("isUnique") or definition.get("isUnic")):
                    unic_fields.append(col)

            if unic_fields:
                combined_idx_name = f"combined_uniq_idx_{table_name}"
                fields_str = ", ".join(unic_fields)
                add_combined_idx_stmt = f"ALTER TABLE {table_name.lower()} ADD UNIQUE INDEX {combined_idx_name} ({fields_str})"
                self._cursor = self._connection.cursor()
                try:
                    self._cursor.execute(add_combined_idx_stmt)
                    self._connection.commit()
                    print(f"Додано об'єднаний унікальний індекс {combined_idx_name} для полів: {fields_str}.")
                except Error as e:
                    print(f"Помилка при додаванні об'єднаного унікального індексу: {e}")
                finally:
                    self._cursor.close()
        else:
            # Таблиця існує: перевірка колонок
            columns_query = """
                SELECT column_name, column_type 
                FROM information_schema.columns 
                WHERE table_schema = %s AND table_name = %s
            """
            self._cursor = self._connection.cursor()
            self._cursor.execute(columns_query, (DATABASE_NAME, table_name))
            existing_columns = {row[0]: row[1] for row in self._cursor.fetchall()}
            self._cursor.close()

            alterations = []
            # Перевірка та модифікація колонок
            for col, definition in desired_fields.items():
                desired_def = get_column_definition(col, definition)
                if col not in existing_columns:
                    alterations.append(f"ADD COLUMN {col} {desired_def}")
                else:
                    if existing_columns[col].upper() != desired_def.upper():
                        alterations.append(f"MODIFY COLUMN {col} {desired_def}")

            # Видалення зайвих колонок
            extra_columns = set(existing_columns.keys()) - set(desired_fields.keys())
            for col in extra_columns:
                alterations.append(f"DROP COLUMN {col}")

            if alterations:
                alter_stmt = f"ALTER TABLE {table_name} " + ", ".join(alterations)
                self._cursor = self._connection.cursor()
                try:
                    self._cursor.execute(alter_stmt)
                    self._connection.commit()
                    print(f"Таблиця {table_name} оновлена. Зміни: {alterations}")
                except Error as e:
                    print("Помилка при оновленні таблиці:", e)
                finally:
                    self._cursor.close()
            else:
                print(f"Таблиця {table_name} вже відповідає заданій схемі колонок.")

            # Перевірка індексів
            self._cursor = self._connection.cursor()
            self._cursor.execute(f"SHOW INDEX FROM {table_name} WHERE Key_name <> 'PRIMARY'")
            index_info = self._cursor.fetchall()
            self._cursor.close()

            # Виводимо інформацію про існуючі індекси для налагодження
            print(f"Існуючі індекси для таблиці {table_name}:")
            for idx in index_info:
                print(f"  Індекс: {idx[2]}, Колонка: {idx[4]}, Унікальний: {idx[1] == 0}")

            # Формуємо словник існуючих індексів: {column_name: [(index_name, is_unique)]}
            existing_indexes = {}
            for row in index_info:
                col_name = row[4]
                idx_name = row[2]
                is_unique = row[1] == 0  # non_unique = 0 означає, що індекс унікальний

                if col_name not in existing_indexes:
                    existing_indexes[col_name] = []
                existing_indexes[col_name].append((idx_name, is_unique))

            # Дії з індексами
            index_alterations = []

            # Перевірка звичайних індексів
            for col, definition in desired_fields.items():
                if isinstance(definition, dict) and "isIndexed" in definition:
                    desired_index = definition["isIndexed"]
                    idx_name = f"idx_{col}"

                    # Визначаємо, чи існує звичайний індекс для цієї колонки
                    has_regular_index = any(name == idx_name and not is_unique
                                            for name, is_unique in existing_indexes.get(col, []))

                    if desired_index and not has_regular_index:
                        # Додаємо звичайний індекс
                        index_alterations.append(("ADD", col, idx_name, False))
                    elif not desired_index and has_regular_index:
                        # Видаляємо звичайний індекс
                        index_alterations.append(("DROP", col, idx_name, False))

            # Виконання змін індексів
            for action, col, idx_name, is_unique in index_alterations:
                if action == "ADD":
                    unique_clause = "UNIQUE " if is_unique else ""
                    stmt = f"ALTER TABLE {table_name} ADD {unique_clause}INDEX {idx_name} ({col})"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(stmt)
                        self._connection.commit()
                        unique_text = "унікальний " if is_unique else ""
                        print(f"Додано {unique_text}індекс {idx_name} для стовпця {col}.")
                    except Error as e:
                        print(f"Помилка при додаванні індексу {idx_name} для {col}: {e}")
                    finally:
                        self._cursor.close()
                elif action == "DROP":
                    stmt = f"ALTER TABLE {table_name} DROP INDEX {idx_name}"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(stmt)
                        self._connection.commit()
                        unique_text = "унікальний " if is_unique else ""
                        print(f"{unique_text}Індекс {idx_name} для стовпця {col} видалено.")
                    except Error as e:
                        print(f"Помилка при видаленні індексу {idx_name}: {e}")
                    finally:
                        self._cursor.close()

            # Збираємо всі унікальні поля для об'єднаного індексу
            unic_fields = []
            for col, definition in desired_fields.items():
                if isinstance(definition, dict) and (definition.get("isUnique") or definition.get("isUnic")):
                    unic_fields.append(col)

            combined_idx_name = f"combined_uniq_idx_{table_name}"

            # Перевіряємо наявність цього індексу
            has_combined_index = any(idx[2] == combined_idx_name for idx in index_info)

            # Перевіряємо, чи є окремі унікальні індекси, які потрібно видалити
            for col in unic_fields:
                uni_idx_name = f"uniq_{col}"
                if any(idx[2] == uni_idx_name for idx in index_info):
                    # Видаляємо окремий унікальний індекс
                    drop_stmt = f"ALTER TABLE {table_name} DROP INDEX {uni_idx_name}"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(drop_stmt)
                        self._connection.commit()
                        print(f"Видалено окремий унікальний індекс {uni_idx_name} для стовпця {col}.")
                    except Error as e:
                        print(f"Помилка при видаленні окремого унікального індексу {uni_idx_name}: {e}")
                    finally:
                        self._cursor.close()

            # Якщо є унікальні поля і потрібно оновити комбінований індекс
            if unic_fields:
                print(f"Унікальні поля для об'єднаного індексу: {unic_fields}")

                # Видаляємо старий індекс, якщо існує
                if has_combined_index:
                    drop_stmt = f"ALTER TABLE {table_name} DROP INDEX {combined_idx_name}"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(drop_stmt)
                        self._connection.commit()
                        print(f"Видалено старий об'єднаний індекс {combined_idx_name}.")
                    except Error as e:
                        print(f"Помилка при видаленні об'єднаного індексу: {e}")
                    finally:
                        self._cursor.close()

                # Створюємо новий індекс тільки якщо є унікальні поля
                if unic_fields:
                    fields_str = ", ".join(unic_fields)
                    add_stmt = f"ALTER TABLE {table_name} ADD UNIQUE INDEX {combined_idx_name} ({fields_str})"
                    self._cursor = self._connection.cursor()
                    try:
                        self._cursor.execute(add_stmt)
                        self._connection.commit()
                        print(f"Створено об'єднаний унікальний індекс {combined_idx_name} для полів: {fields_str}.")
                    except Error as e:
                        print(f"Помилка при додаванні об'єднаного унікального індексу: {e}")
                    finally:
                        self._cursor.close()
            elif has_combined_index:
                # Якщо вже немає унікальних полів, але індекс існує - видаляємо його
                drop_stmt = f"ALTER TABLE {table_name} DROP INDEX {combined_idx_name}"
                self._cursor = self._connection.cursor()
                try:
                    self._cursor.execute(drop_stmt)
                    self._connection.commit()
                    print(
                        f"Видалено об'єднаний унікальний індекс {combined_idx_name}, оскільки немає унікальних полів.")
                except Error as e:
                    print(f"Помилка при видаленні об'єднаного індексу: {e}")
                finally:
                    self._cursor.close()


    def getList(self, entity, filter=None, orderBy=None, limit=None, offset=None):
        #testing
        from dioritorm.core.entity import Entity
        from dioritorm.core.data_field import DataField
        from dioritorm.core.table_section import TableSection
        try:
            if not self._connection or not self._connection.is_connected():
                self.init()

            # Отримуємо клас сутності
            entity_class = entity.__class__

            # Формуємо ім'я таблиці на основі типу та імені об'єкта
            table_name = f"{entity._type}_{entity._objectName.value.lower()}"
            # Запит для отримання об'єкту за UUID
            self._cursor = self._connection.cursor(dictionary=True)  # Повертати результати як словники

            # Базовий SQL запит

            fields = []
            joins = []
            entity.create()
            for name, value in entity.__dict__.items():
                if not name.startswith('_'):
                    if isinstance(value, Entity):
                        from dioritorm.core.reference import Reference
                        from dioritorm.core.document import Document
                        if isinstance(value, Reference):
                            fields.append(f"{table_name}.{name} as {name}")
                            fields.append(f"{name}.name as {name}_name")
                            joins.append(f"LEFT JOIN {value._type}_{value._objectName.value.lower()} as {name} ON {name}.uuid={table_name}.{name}")
                        elif isinstance(value, Document):
                            fields.append(f"{table_name}.{name} as {name}")
                            fields.append(f"{name}.number as {name}_number")
                            fields.append(f"{name}.datedoc as {name}_datedoc")
                            joins.append(f"LEFT JOIN {value._type}_{value._objectName.value.lower()} as {name} ON {name}.uuid={table_name}.{name}")
                        fields.append(f"{table_name}.{name} as {name}") #Тут додав
                    elif isinstance(value, DataField):
                        fields.append(f"{table_name}.{name} as {name}")

            query = f"SELECT {','.join(map(str, fields))} FROM {table_name} {' '.join(map(str, joins))}"
            print(query)
            params = []
            # Додаємо умови фільтрації, якщо вони є
            if filter and filter.conditions:
                where_clause, where_params = filter.to_sql()
                query += f" WHERE {where_clause}"
                params.extend(where_params)

            # Додаємо сортування, якщо воно вказане
            if orderBy and orderBy.order_fields:
                query += f" ORDER BY {orderBy.to_sql()}"

            # Додаємо обмеження кількості записів, якщо вказано
            if limit is not None:
                query += f" LIMIT {limit}"

                # Додаємо зміщення, якщо вказано
                if offset is not None:
                    query += f" OFFSET {offset}"

            # Виконуємо запит

            #print("PARAMS:", params)
            #print("PARAM TYPES:", [type(p) for p in params])
            self._cursor.execute(query, params)
            records = self._cursor.fetchall()
            # Обробляємо результати
            results = []
            for record in records:
                # Створюємо новий об'єкт відповідного класу
                obj = entity_class()
                obj.create()
                # Заповнюємо всі поля з record
                for field_name, field_value in record.items():
                    if field_name == 'TableSections':
                        continue  # TableSections обробляємо окремо
                    if hasattr(obj, field_name):
                        field = getattr(obj, field_name)
                        if isinstance(field, DataField):  # якщо це DataField
                            field.value = field_value
                        elif isinstance(field, Entity):
                            if field_value is not None:
                                field.uuid.value = field_value
                            else:
                                field.uuid.value = NULLLINK
                            if isinstance(field, Reference):
                                if record[f'{field_name}_name'] is not None:
                                    field.name.value = record[f'{field_name}_name']
                            elif isinstance(field, Document):
                                if record[f'{field_name}_number'] is not None:
                                    field.number.value = record[f'{field_name}_number']
                                if record[f'{field_name}_datedoc'] is not None:
                                    field.datedoc.value = record[f'{field_name}_datedoc']
                        elif isinstance(field, TableSection):
                            print("TableSection:", "have TableSections")
                        else:  # якщо це звичайний атрибут
                            setattr(obj, field_name, field_value)

                # Обробляємо табличні частини
                if hasattr(entity, 'TableSections'):
                     if entity.TableSections.count()>0:
                        for ts_name, ts_info in entity.TableSections.items():
                            ts_query = f"SELECT * FROM {ts_name} WHERE _owner = %s"
                            self._cursor.execute(ts_query, (record['uuid'],))
                            ts_records = self._cursor.fetchall()

                            # Заповнюємо табличну частину, якщо вона є
                            if hasattr(obj, ts_name):
                                table_section = getattr(obj, ts_name)
                                for ts_record in ts_records:
                                    row = table_section.rows.add()
                                    for col_name, col_value in ts_record.items():
                                        if col_name != 'owner' and col_name != 'uuid':
                                            if hasattr(row, col_name):
                                                field = getattr(row, col_name)
                                                if hasattr(field, 'value'):  # якщо це DataField
                                                    field.value = col_value
                                                else:  # якщо це звичайний атрибут
                                                    setattr(row, col_name, col_value)

                results.append(obj)

            return results

        except Error as e:
            print(f"Помилка при отриманні списку об'єктів: {e}")
            return []

        finally:
            if self._cursor:
                self._cursor.close()
                self._cursor = None
