import copy
import logging
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as PgConnection
from psycopg2.extras import execute_values

logger = logging.getLogger("json_2_postgres")


def _fetch_sequence_params(cursor, table_name: str, schema_name: str = "public"):
    """
    Получает параметры последовательностей, связанных с таблицей, включая текущее значение.

    :param cursor: Объект курсора для выполнения SQL-запросов.
    :param table_name: Имя таблицы для поиска связанных последовательностей.
    :param schema_name: Имя схемы (по умолчанию "public").
    :return: Список словарей с параметрами последовательностей.
    """
    try:
        # Находим все связанные последовательности
        cursor.execute(
            """
            SELECT
                s.sequence_name,
                s.data_type,
                s.start_value,
                s.minimum_value,
                s.maximum_value,
                s.increment,
                s.cycle_option,
                s.sequence_schema
            FROM
                information_schema.sequences s
            WHERE
                s.sequence_schema = %s
                AND EXISTS (
                    SELECT 1
                    FROM information_schema.columns c
                    WHERE
                        c.table_schema = %s
                        AND c.table_name = %s
                        AND c.column_default = CONCAT(
                            'nextval(''',
                            s.sequence_schema, '.', s.sequence_name,
                            '''::regclass)'
                        )
                )
        """,
            (schema_name, schema_name, table_name),
        )

        sequences_data = cursor.fetchall()
        logger.debug("Найдено связанных последовательностей: %d", len(sequences_data))

        sequences = []
        for row in sequences_data:
            seq_name = row[0]
            seq_schema = row[7]

            # Получаем текущее значение только нужной последовательности.
            cursor.execute(f"SELECT last_value FROM {seq_schema}.{seq_name}")
            current_val = cursor.fetchone()[0]

            sequences.append(
                {
                    "name": seq_name,
                    "data_type": row[1],
                    "increment": row[5],
                    "minvalue": row[3],
                    "maxvalue": row[4],
                    "start": row[2],
                    "cycle": row[6] == "YES",
                    "current_value": current_val if current_val is not None else row[2],
                }
            )
        logger.debug("Успешно обработано последовательностей: %d", len(sequences))
        return sequences

    except Exception as e:
        logger.error(
            "Ошибка при извлечении последовательностей для %s.%s: %s", schema_name, table_name, str(e), exc_info=True
        )
        return []


def _fetch_columns(cursor, table_name: str, schema_name: str = "public") -> List[Dict[str, Union[str, int, bool]]]:
    """
    Получение столбцов таблицы с учётом схемы.

    :param cursor: Курсор для работы с БД.
    :param table_name: Имя таблицы, для которой нужно получить информацию о столбцах.
    :param schema_name: Имя схемы (по умолчанию 'public').
    :return: Список словарей с информацией о столбцах.
    """
    logger.debug("Получение информации о колонках")
    cursor.execute(
        """
        SELECT
            c.column_name,
            c.data_type,
            c.character_maximum_length,  -- Длина для VARCHAR и CHAR
            c.is_nullable,
            c.column_default,
            c.udt_name,
            pg_catalog.col_description(
                format('%%I.%%I', c.table_schema, c.table_name)::regclass::oid,
                c.ordinal_position
            ) AS column_comment
        FROM
            information_schema.columns c
        WHERE
            c.table_name = %s AND c.table_schema = %s
        ORDER BY
            c.ordinal_position;
        """,
        (table_name, schema_name),
    )
    columns = cursor.fetchall()

    if not columns:
        raise ValueError(f"Не найдены столбцы для таблицы: {table_name} в схеме {schema_name}")

    logger.debug("Найдено колонок: %d", len(columns))
    return [
        {
            "name": col[0],
            "type": (col[5] if col[1] == "USER-DEFINED" else f"{col[1]}({col[2]})" if col[2] else col[1]),
            "nullable": col[3] == "YES",
            "default": col[4],
            "comment": col[6],
        }
        for col in columns
    ]


def _fetch_table_comment(cursor, table_name: str, schema_name: str = "public") -> str:
    """
    Получение комментария к таблице с учетом схемы.

    :param cursor: Курсор для работы с БД.
    :param table_name: Имя таблицы, для которой необходимо получить комментарий.
    :param schema_name: Имя схемы (по умолчанию 'public').
    :return: Строка - комментарий к таблице.
    """
    cursor.execute(
        """
        SELECT
            obj_description(format('%%I.%%I', %s, %s)::regclass) AS table_comment;
        """,
        (schema_name, table_name),
    )
    result = cursor.fetchone()
    table_comment = result[0] if result else None

    if table_comment:
        logger.debug("Найден комментарий таблицы: '%s'", table_comment)
    else:
        logger.debug("Комментарий таблицы не найден")

    return table_comment


def _fetch_constraints(cursor, table_name: str, schema_name: str = "public") -> List[Dict[str, str]]:
    """
    Получение ограничений для таблицы.

    :param cursor: Курсор для работы с бд.
    :param  table_name: Имя таблицы.
    :param schema_name: Имя схемы (по умолчанию "public").
    :return: Список словарей с ограничениями.
    """
    cursor.execute(
        """
        SELECT
            tc.constraint_type,
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column,
            ch.check_clause,
            tc.constraint_name,
            ccu.table_schema AS foreign_table_schema
        FROM
            information_schema.table_constraints AS tc
        LEFT JOIN
            information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_name = kcu.table_name
            AND tc.table_schema = kcu.table_schema
        LEFT JOIN
            information_schema.constraint_column_usage AS ccu
            ON tc.constraint_name = ccu.constraint_name
        LEFT JOIN
            information_schema.check_constraints AS ch
            ON tc.constraint_name = ch.constraint_name
        WHERE
            tc.table_name = %s
            AND tc.table_schema = %s;
        """,
        (table_name, schema_name),
    )
    constraints = cursor.fetchall()
    logger.debug("Найдено ограничений: %d", len(constraints))

    result = [
        {
            "constraint_type": constraint[0],
            "column": constraint[1],
            "foreign_table": constraint[2],
            "foreign_column": constraint[3],
            "check_clause": constraint[4],
            "constraint_name": constraint[5],
            "foreign_table_schema": constraint[6],
        }
        for constraint in constraints
    ]
    if result:
        constraint_types = [c["constraint_type"] for c in result if c["constraint_type"]]
        logger.debug("Типы ограничений: %s", list(set(constraint_types)))

    return result


def _sequence_related_to_excluded_columns(
    sequence: Dict[str, Any], all_columns: List[Dict[str, Any]], excluded_columns: List[str]
) -> bool:
    """
    Проверяет, связана ли последовательность с исключенной колонкой.

    :param sequence: Информация о последовательности.
    :param all_columns: Все колонки таблицы.
    :param excluded_columns: Список исключаемых колонок.
    :return: True если последовательность связана с исключенной колонкой.
    """
    # Находим колонку, которая использует эту последовательность
    for column in all_columns:
        column_default = column.get("default", "")
        if (
            isinstance(column_default, str)
            and sequence["name"] in column_default
            and column["name"] in excluded_columns
        ):
            logger.debug(
                "Последовательность '%s' связана с исключенной колонкой '%s'", sequence.get("name"), column["name"]
            )
            return True
    return False


def _constraint_contains_excluded_columns(constraint: Dict[str, Any], excluded_columns: List[str]) -> bool:
    """
    Проверяет, содержит ли constraint исключенные колонки.

    :param constraint: Словарь с информацией о constraint.
    :param excluded_columns: Список исключаемых колонок.
    :return: True если constraint содержит исключенные колонки.
    """
    constraint_name = constraint.get("constraint_name", "unknown")
    constraint_column = constraint.get("column")
    # Для PRIMARY KEY, UNIQUE, FOREIGN KEY проверяем column
    if constraint_column in excluded_columns:
        logger.debug("Ограничение '%s' содержит исключенную колонку '%s'", constraint_name, constraint_column)
        return True

    # Для CHECK constraints проверяем, ссылается ли он на исключенные колонки
    if constraint.get("constraint_type") == "CHECK" and constraint.get("check_clause"):
        check_clause = constraint["check_clause"] or ""
        for excluded_col in excluded_columns:
            if excluded_col in check_clause:
                logger.debug(
                    "CHECK ограничение '%s' ссылается на исключенную колонку '%s'", constraint_name, excluded_col
                )
                return True
    logger.debug("Ограничение '%s' не содержит исключенных колонок", constraint_name)
    return False


def _table_structure_to_dict(
    connection, table_name: str, schema_name: str = "public", excluded_columns: Optional[List[str]] = None
) -> Dict[str, Union[str, List[Dict[str, Union[str, bool, int]]]]]:
    """
    Экспортирует структуру таблицы из базы данных в словарь.

    :param connection: Объект соединения с базой данных psycopg2.
    :param table_name: Имя таблицы для экспорта.
    :param schema_name: Имя схемы (по умолчанию 'public').
    :param excluded_columns: Список колонок для исключения.
    :returns: Словарь, содержащий информацию о таблице, столбцах, первичных и внешних ключах, и последовательностях.
    """
    logger.debug("Получение структуры таблицы %s", table_name)
    excluded_columns = excluded_columns or []

    with connection.cursor() as cursor:
        columns = _fetch_columns(cursor, table_name, schema_name)

        filtered_columns = [col for col in columns if col["name"] not in excluded_columns]
        logger.debug("Отфильтровано колонок: %d из %d", len(filtered_columns), len(columns))

        table_comment = _fetch_table_comment(cursor, table_name, schema_name)
        constraints = _fetch_constraints(cursor, table_name, schema_name)

        filtered_constraints = [
            con for con in constraints if not _constraint_contains_excluded_columns(con, excluded_columns)
        ]
        logger.debug("Отфильтровано ограничений: %d из %d", len(filtered_constraints), len(constraints))

        sequences = _fetch_sequence_params(cursor, table_name, schema_name)

        filtered_sequences = [
            seq for seq in sequences if not _sequence_related_to_excluded_columns(seq, columns, excluded_columns)
        ]
        logger.debug("Отфильтровано последовательностей: %d из %d", len(filtered_sequences), len(sequences))

        table_structure = {
            "table": table_name,
            "comment": table_comment,
            "columns": filtered_columns,
            "constraints": filtered_constraints,
            "sequences": filtered_sequences,
        }

    logger.debug("Структура таблицы экспортирована")
    return table_structure


def _create_sequences(
    cursor,
    sequences: List[Dict[str, Union[str, int, None]]],
    table_name: str,
    old_table_name: str,
    schema_name: str = "public",
) -> None:
    """
    Создает последовательности в базе данных, учитывая все возможные параметры, включая текущее значение.

    :param cursor: Объект курсора для выполнения SQL-запросов.
    :param sequences: Список словарей, содержащих параметры последовательностей.
    :param table_name: Новое имя таблицы, заменяет старое имя в параметрах.
    :param old_table_name: Старое имя таблицы, которое будет заменено.
    :param schema_name: Имя схемы, в которой создается последовательность.
    """
    if not sequences:
        return
    for seq in sequences:
        seq_base_name = seq["name"].replace(old_table_name, table_name)
        full_seq_name = f"{schema_name}.{seq_base_name}"
        data_type = seq.get("data_type", "bigint")
        increment = seq.get("increment", 1)
        minvalue = seq.get("minvalue", "NO MINVALUE")
        maxvalue = seq.get("maxvalue", "NO MAXVALUE")
        start = seq.get("start", None)
        cycle = "CYCLE" if seq.get("cycle", False) else "NO CYCLE"
        current_value = seq.get("current_value", 1)

        # Формирование SQL-запроса
        create_sequence_sql = sql.SQL(
            """
            CREATE SEQUENCE IF NOT EXISTS {seq_name}
            AS {data_type}
            INCREMENT BY {increment}
            MINVALUE {minvalue}
            MAXVALUE {maxvalue}
            {start}
            {cycle};

            -- Set the current value of the sequence
           SELECT setval(%s, %s, true);
        """
        ).format(
            seq_name=sql.Identifier(schema_name, seq_base_name),
            data_type=sql.SQL(data_type),
            increment=sql.SQL(increment),
            minvalue=sql.SQL(minvalue),
            maxvalue=sql.SQL(maxvalue),
            start=sql.SQL(f"START WITH {start}") if start is not None else sql.SQL(""),
            cycle=sql.SQL(cycle),
        )

        try:
            cursor.execute(
                create_sequence_sql,
                (
                    full_seq_name,
                    current_value,
                ),
            )
            logger.debug("Последовательность %s успешно создана", full_seq_name)
        except Exception as e:
            logger.error("Ошибка создания последовательности %s: %s", full_seq_name, str(e), exc_info=True)
            raise
    logger.debug("Все последовательности созданы успешно")


def _create_table(
    cursor,
    old_table_name: str,
    new_table_name: str,
    columns: List[Dict[str, str]],
    table_comment: str = None,
    schema_name: str = "public",
) -> None:
    """
    Создает таблицу на основе предоставленных данных.

    :param cursor: Объект курсора для выполнения SQL-запросов.
    :param old_table_name: Старое имя таблицы.
    :param new_table_name: Имя таблицы.
    :param columns: Список словарей, описывающих столбцы таблицы.
    :param table_comment: Комментарий к таблице.
    :param schema_name: Имя схемы в которой создается таблица, по умолчанию "public"
    """
    full_table_name = f"{schema_name}.{new_table_name}"
    logger.debug("Создание таблицы %s с %d колонками", full_table_name, len(columns))

    column_defs = []
    for col in columns:
        col_type = col["type"]
        col_name = sql.Identifier(col["name"])
        col_def_parts = [col_name, sql.SQL(col_type)]

        if not col.get("nullable", True):
            col_def_parts.append(sql.SQL("NOT NULL"))

        if col.get("default"):
            pattern = r"(nextval\(')([^']+)(\..+::regclass)"
            default_value = sql.SQL(
                re.sub(pattern, rf"\1{schema_name}\3", col["default"]).replace(old_table_name, new_table_name)
            )
            col_def_parts.extend([sql.SQL("DEFAULT"), default_value])

        col_def = sql.SQL(" ").join(col_def_parts)
        column_defs.append(col_def)

    columns_sql = sql.SQL(",\n").join(column_defs)

    create_table_sql = sql.SQL(
        """
        CREATE TABLE {table_name} (
            {columns}
        );
    """
    ).format(
        table_name=sql.Identifier(schema_name, new_table_name),
        columns=columns_sql,
    )

    try:
        cursor.execute(create_table_sql)
        logger.debug("Таблица %s успешно создана", full_table_name)
    except Exception as e:
        logger.error("Ошибка создания таблицы %s: %s", full_table_name, str(e), exc_info=True)
        raise

    if table_comment:
        comment_sql = sql.SQL("COMMENT ON TABLE {table} IS %s;").format(
            table=sql.Identifier(schema_name, new_table_name),
        )
        cursor.execute(comment_sql, (table_comment,))

    # Комментарии к столбцам
    for col in columns:
        if "comment" in col and col["comment"]:
            comment_col_sql = sql.SQL("COMMENT ON COLUMN {table}.{column} IS %s;").format(
                table=sql.Identifier(schema_name, new_table_name),
                column=sql.Identifier(col["name"]),
            )
            cursor.execute(comment_col_sql, (col["comment"],))
    logger.debug("Таблица %s полностью создана", full_table_name)


def _create_constraints(
    cursor,
    old_table_name: str,
    new_table_name: str,
    constraints: List[Dict[str, str]],
    foreign_tables_mapping: Union[Dict[Tuple[str, str], Tuple[str, str]], None],
    columns_names: Set[str],
    schema_name: str = "public",
) -> None:
    """
    Создает все ограничения для таблицы.

    :param cursor: Объект курсора для выполнения SQL-запросов.
    :param new_table_name: Имя таблицы.
    :param constraints: Список словарей, описывающих ограничения.
    :param foreign_tables_mapping: Словарь соответствия имен связанных таблиц и схем в словаре и в базе данных состоит
    из кортежей с парой значений ("имя_схемы", "имя_таблицы") ключи имена в словаре, значения в имена базе.
    :param columns_names: Имена столбцов таблицы для их оборачивания в кавычки.
    :param schema_name: Имя схемы, по умолчанию "public".
    """
    logger.debug(
        "Создание ограничений для таблицы %s.%s (%d ограничений)", schema_name, new_table_name, len(constraints)
    )

    def replace_match(match: re.Match) -> str:
        """Оборачивает в кавычки слово если оно соответствует названию столбца."""
        word = match.group(0)
        result = f'"{word}"' if word in columns_names else word
        logger.debug("Замена в CHECK: '%s' -> '%s'", word, result)
        return result

    primary_key_columns = []
    for constraint in constraints:
        if constraint["constraint_type"] == "PRIMARY KEY" and constraint["column"] not in primary_key_columns:
            primary_key_columns.append(constraint["column"])

    if primary_key_columns:
        primary_key_sql = sql.SQL(
            """
               ALTER TABLE {table}
               ADD CONSTRAINT {constraint_name}
               PRIMARY KEY ({columns});
           """
        ).format(
            table=sql.Identifier(schema_name, new_table_name),
            constraint_name=sql.Identifier(f"{new_table_name}_pkey"),
            columns=sql.SQL(", ").join(map(sql.Identifier, primary_key_columns)),
        )
        try:
            cursor.execute(primary_key_sql)
            logger.debug("PRIMARY KEY создан: %s_pkey", new_table_name)
        except Exception as e:
            logger.error("Ошибка создания PRIMARY KEY для %s: %s", new_table_name, str(e), exc_info=True)
            raise
    else:
        logger.debug("PRIMARY KEY не найден в ограничениях")

    for constraint in constraints:
        constraint_name = constraint.get("constraint_name", "unknown")
        constraint_type = constraint.get("constraint_type", "unknown")
        if constraint["constraint_type"] == "FOREIGN KEY":
            foreign_table_name = (
                foreign_tables_mapping.get(
                    (
                        constraint["foreign_table_schema"],
                        constraint["foreign_table"],
                    ),
                    (
                        constraint["foreign_table_schema"],
                        constraint["foreign_table"],
                    ),
                )
                if foreign_tables_mapping
                else (
                    constraint["foreign_table_schema"],
                    constraint["foreign_table"],
                )
            )
            constraint_sql = sql.SQL(
                """
                ALTER TABLE {table}
                ADD CONSTRAINT {constraint_name}
                FOREIGN KEY ({column})
                REFERENCES {foreign_table} ({foreign_column});
            """
            ).format(
                table=sql.Identifier(schema_name, new_table_name),
                constraint_name=sql.Identifier(f"{new_table_name}_{constraint['column']}_fkey"),
                column=sql.Identifier(constraint["column"]),
                foreign_table=sql.Identifier(foreign_table_name[0], foreign_table_name[1]),
                foreign_column=sql.Identifier(constraint["foreign_column"]),
            )

        elif constraint["constraint_type"] == "UNIQUE":
            constraint_sql = sql.SQL(
                """
                ALTER TABLE {table}
                ADD CONSTRAINT {constraint_name}
                UNIQUE ({column});
            """
            ).format(
                table=sql.Identifier(schema_name, new_table_name),
                constraint_name=sql.Identifier(f"uq_{new_table_name}_{constraint['column']}"),
                column=sql.Identifier(constraint["column"]),
            )

        elif constraint["constraint_type"] == "CHECK":
            if constraint["check_clause"].find("IS NOT NULL") != -1:
                continue  # NOT NULL задается через свойства столбцов. Поэтому если попадается такое ограничение мы его
                # пропускаем
            logger.debug("Создание CHECK ограничения: %s", constraint_name)
            check_clause = constraint["check_clause"].replace(old_table_name, new_table_name)

            pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")
            check_clause = pattern.sub(replace_match, check_clause)
            check_clause = check_clause.replace('""', '"')

            logger.debug("CHECK условие: %s", check_clause)

            constraint_sql = sql.SQL(
                """
                ALTER TABLE {table}
                ADD CONSTRAINT {constraint_name}
                CHECK ({check_clause});
            """
            ).format(
                table=sql.Identifier(schema_name, new_table_name),
                constraint_name=sql.Identifier(constraint["constraint_name"].replace(old_table_name, new_table_name)),
                check_clause=sql.SQL(check_clause),
            )
        else:
            logger.debug("Неизвестный тип ограничения: %s", constraint_type)
            continue
        try:
            cursor.execute(constraint_sql)
            logger.debug("Ограничение создано: %s", constraint_name)
        except Exception as e:
            logger.error("Ошибка создания ограничения %s: %s", constraint_name, str(e), exc_info=True)
            raise
    logger.debug("Создание ограничений завершено")


def _create_table_from_dict(
    connection,
    table_structure: Dict[str, Union[str, List[str], List[Dict[str, str]]]],
    new_table_name: Union[str, None] = None,
    foreign_tables_mapping: Union[Dict[Tuple[str, str], Tuple[str, str]], None] = None,
    schema_name="public",
) -> None:
    """
    Создает таблицу в базе данных PostgreSQL на основе структуры, описанной в словаре.

    :param connection: Объект соединения с базой данных psycopg2.
    :param table_structure: Словарь содержащий структуру таблицы.
    :param new_table_name: Имя таблицы в базе данных.
    :param foreign_tables_mapping: Словарь соответствия имен связанных таблиц и схем в словаре и в базе данных состоит
    из кортежей с парой значений ("имя_схемы", "имя_таблицы") ключи имена в словаре, значения в имена базе.
    :param schema_name: Имя схемы (по умолчанию 'public').
    """
    table_name = new_table_name if new_table_name else table_structure["table"]
    table_comment = table_structure.get("comment")
    columns = table_structure.get("columns", [])
    columns_names = {column["name"] for column in columns}
    constraints = table_structure.get("constraints", [])
    sequences = table_structure.get("sequences", [])

    full_table_name = f"{schema_name}.{table_name}"
    logger.debug("Начало создания таблицы %s из словаря", full_table_name)
    logger.debug(
        "Структура таблицы: %d колонок, %d ограничений, %d последовательностей",
        len(columns),
        len(constraints),
        len(sequences),
    )

    try:
        with connection.cursor() as cursor:
            _create_sequences(
                cursor,
                sequences=sequences,
                table_name=table_name,
                old_table_name=table_structure["table"],
                schema_name=schema_name,
            )

            _create_table(
                cursor,
                old_table_name=table_structure["table"],
                new_table_name=table_name,
                columns=columns,
                table_comment=table_comment,
                schema_name=schema_name,
            )

            _create_constraints(
                cursor,
                table_structure["table"],
                table_name,
                constraints,
                foreign_tables_mapping,
                columns_names,
                schema_name=schema_name,
            )
            logger.debug("Таблица %s успешно создана из словаря", full_table_name)
    except Exception as e:
        logger.error("Ошибка создания таблицы %s из словаря: %s", full_table_name, str(e), exc_info=True)
        raise


def _get_column_cast_expression(column_meta: Dict[str, Any]) -> sql.Composable:
    """Генерирует выражение для приведения типа колонки."""
    col_name = column_meta["name"]
    col_type = column_meta["type"].lower()

    if col_type in ("integer", "int", "int4", "serial"):
        logger.debug("Приведение к INTEGER: %s", col_name)
        return sql.SQL("t.{}::integer").format(sql.Identifier(col_name))

    if col_type in ("bigint", "int8", "bigserial"):
        logger.debug("Приведение к BIGINT: %s", col_name)
        return sql.SQL("t.{}::bigint").format(sql.Identifier(col_name))

    if col_type in ("smallint", "int2", "smallserial"):
        logger.debug("Приведение к SMALLINT: %s", col_name)
        return sql.SQL("t.{}::smallint").format(sql.Identifier(col_name))

    if "character varying" in col_type or col_type in ("text", "varchar", "char", "bpchar"):
        logger.debug("Приведение к TEXT: %s", col_name)
        return sql.SQL("t.{}::text").format(sql.Identifier(col_name))

    if col_type in {"boolean", "bool"}:
        logger.debug("Приведение к BOOLEAN с преобразованием строк: %s", col_name)
        return sql.SQL("""
            CASE
                WHEN t.{col}::text IN ('true', 't', 'yes', 'y', '1', 'on') THEN true
                WHEN t.{col}::text IN ('false', 'f', 'no', 'n', '0', 'off') THEN false
                ELSE NULL
            END
        """).format(col=sql.Identifier(col_name))

    if col_type in ("numeric", "decimal", "real", "double precision", "float", "float4", "float8"):
        logger.debug("Приведение к NUMERIC: %s", col_name)
        return sql.SQL("t.{}::numeric").format(sql.Identifier(col_name))

    if col_type in ("timestamp", "timestamptz", "timestamp without time zone", "timestamp with time zone"):
        logger.debug("Приведение к TIMESTAMP: %s", col_name)
        return sql.SQL("t.{}::timestamp").format(sql.Identifier(col_name))

    if col_type == "date":
        logger.debug("Приведение к DATE: %s", col_name)
        return sql.SQL("t.{}::date").format(sql.Identifier(col_name))

    if col_type == "time" or "time without time zone" in col_type or "time with time zone" in col_type:
        logger.debug("Приведение к TIME: %s", col_name)
        return sql.SQL("t.{}::time").format(sql.Identifier(col_name))

    if col_type in {"json", "jsonb"}:
        logger.debug("Приведение к JSONB: %s", col_name)
        return sql.SQL("t.{}::jsonb").format(sql.Identifier(col_name))

    if col_type == "uuid":
        logger.debug("Приведение к UUID с проверкой NULL: %s", col_name)
        return sql.SQL("""
            CASE
                WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE t.{col}::uuid
            END
        """).format(col=sql.Identifier(col_name))

    if col_type == "ltree":
        logger.debug("Приведение к LTREE: %s", col_name)
        return sql.SQL("t.{}::ltree").format(sql.Identifier(col_name))

    if col_type == "bytea":
        logger.debug("Приведение к BYTEA с декодированием: %s", col_name)
        return sql.SQL("decode(t.{col}, 'escape')").format(col=sql.Identifier(col_name))

    if "[]" in col_type or col_type == "array":
        default_value = str(column_meta.get("default", "")).upper()
        logger.debug("Обработка массива %s, default: %s", col_name, default_value)

        if "INTEGER[]" in default_value or "INT[]" in default_value or "INT4[]" in default_value:
            logger.debug("Приведение к INTEGER[]: %s", col_name)
            return sql.SQL("""
                CASE WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE string_to_array(t.{col}, ',')::integer[]
                END
            """).format(col=sql.Identifier(col_name))

        if "BIGINT[]" in default_value or "INT8[]" in default_value:
            logger.debug("Приведение к BIGINT[]: %s", col_name)
            return sql.SQL("""
                CASE WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE string_to_array(t.{col}, ',')::bigint[]
                END
            """).format(col=sql.Identifier(col_name))

        if "TEXT[]" in default_value or "VARCHAR[]" in default_value or "CHARACTER VARYING[]" in default_value:
            logger.debug("Приведение к TEXT[]: %s", col_name)
            return sql.SQL("""
                CASE WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE string_to_array(t.{col}, ',')
                END
            """).format(col=sql.Identifier(col_name))

        if "UUID[]" in default_value:
            logger.debug("Приведение к UUID[]: %s", col_name)
            return sql.SQL("""
                CASE WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE string_to_array(t.{col}, ',')::uuid[]
                END
            """).format(col=sql.Identifier(col_name))

        # По умолчанию считаем integer[] ('ARRAY[]::integer[]')
        logger.debug("Приведение к INTEGER[] (по умолчанию): %s", col_name)
        return sql.SQL("""
                CASE WHEN t.{col} IS NULL OR t.{col} = '' THEN NULL
                ELSE string_to_array(t.{col}, ',')::integer[]
                END
            """).format(col=sql.Identifier(col_name))
    logger.debug("Использование типа как есть (без приведения): %s", col_name)
    return sql.SQL("t.{}").format(sql.Identifier(col_name))


def _compare_table_structure(
    connection,
    table_structure: Dict[str, Union[str, List[Dict[str, Union[str, bool, int, None]]]]],
    table_name: str,
    foreign_tables_mapping: Union[Dict[Tuple[str, str], Tuple[str, str]], None] = None,
    schema_name: str = "public",
    excluded_columns: Optional[List[str]] = None,
) -> bool:
    """
    Сравнивает структуру таблицы из базы данных с переданной структурой таблицы.

    :param connection: Объект соединения с базой данных psycopg2.
    :param table_structure: Словарь содержащий структуру таблицы.
    :param table_name: Имя таблицы в базе данных с которой осуществляется сравнение.
    :param foreign_tables_mapping: Словарь соответствия имен связанных таблиц и схем в словаре и в базе данных состоит
    из кортежей с парой значений ("имя_схемы", "имя_таблицы") ключи имена в словаре, значения в имена базе.
    :param schema_name: Имя схемы (по умолчанию 'public').
    :param excluded_columns: Список колонок для исключения при сравнении.
    :return: True если основные параметры таблиц совпадают. False если различаются.
    """
    excluded_columns = excluded_columns or []

    logger.debug("Начало сравнения структуры таблицы из базы со структурой из json")
    logger.debug("Исключаемые колонки: %s", excluded_columns)

    table_from_db = _table_structure_to_dict(
        connection, table_name=table_name, schema_name=schema_name, excluded_columns=excluded_columns
    )
    old_table_name = table_structure["table"]
    # Сравнение столбцов
    structure_columns = {col["name"]: col for col in table_structure["columns"]}
    db_columns = {col["name"]: col for col in table_from_db["columns"]}

    logger.debug("Сравнение колонок: эталон %d, БД %d", len(structure_columns), len(db_columns))

    if structure_columns.keys() != db_columns.keys():
        logger.warning(
            "Различие в наборе колонок: json %s, БД %s", set(structure_columns.keys()), set(db_columns.keys())
        )
        return False

    pattern = r"(nextval\(')([^']+)(\..+::regclass)"
    for column_name, structure_column in structure_columns.items():
        db_column = db_columns[column_name]

        if (
            structure_column["default"]
            and re.sub(pattern, rf"\1{schema_name}\3", structure_column["default"]).replace(old_table_name, table_name)
            != db_column["default"]
        ):
            logger.warning("Различие в DEFAULT для колонки %s", column_name)
            return False

        if structure_column["nullable"] != db_column["nullable"]:
            logger.warning(
                "Различие в NULLABLE для колонки %s: эталон %s, БД %s",
                column_name,
                structure_column["nullable"],
                db_column["nullable"],
            )
            return False

        if structure_column["type"] != db_column["type"]:
            logger.warning(
                "Различие в TYPE для колонки %s: эталон '%s', БД '%s'",
                column_name,
                structure_column["type"],
                db_column["type"],
            )
            return False
    logger.debug("Все параметры колонок совпадают")

    # Изменяем имя таблиц в constraints на новые и удаляем имя ограничения
    logger.debug("Сравнение ограничений")
    constraints_structure = copy.deepcopy(table_structure["constraints"])
    for constraint in constraints_structure:
        if constraint["constraint_type"] == "PRIMARY KEY" or constraint["constraint_type"] == "UNIQUE":
            constraint["foreign_table"] = table_name
        if constraint["constraint_type"] == "FOREIGN KEY":
            constraint["foreign_table_schema"], constraint["foreign_table"] = (
                foreign_tables_mapping.get(
                    (
                        constraint["foreign_table_schema"],
                        constraint["foreign_table"],
                    ),
                    (
                        constraint["foreign_table_schema"],
                        constraint["foreign_table"],
                    ),
                )
                if foreign_tables_mapping
                else (
                    constraint["foreign_table_schema"],
                    constraint["foreign_table"],
                )
            )
        constraint.pop("constraint_name")
    constraints_db = table_from_db["constraints"]
    for constraint in constraints_db:
        constraint.pop("constraint_name")

    # Преобразуем списки ограничений в словари для удобства сравнения
    def constraints_to_dict(
        constraints: List[Dict[str, str]],
    ) -> Dict[str, Dict[str, str]]:
        return {f"{c['constraint_type']}_{c['column']}": c for c in constraints}

    constraints_structure = constraints_to_dict(constraints_structure)
    constraints_db = constraints_to_dict(constraints_db)

    if constraints_structure != constraints_db:
        logger.warning("Различие в ограничениях")
        logger.debug("Ограничения json: %s", list(constraints_structure.keys()))
        logger.debug("Ограничения БД: %s", list(constraints_db.keys()))
        return False

    logger.debug("Все ограничения совпадают")

    # Проверка на совпадение последовательностей
    logger.debug("Сравнение последовательностей")
    seq_structure = table_structure["sequences"]
    if seq_structure:
        for seq in seq_structure:
            seq["name"] = seq["name"].replace(old_table_name, table_name)
        seq_structure = sorted(seq_structure, key=lambda x: x["name"])
        seq_db = sorted(table_from_db["sequences"], key=lambda x: x["name"])

        if len(seq_structure) != len(seq_db):
            logger.warning("Разное количество последовательностей: эталон %d, БД %d", len(seq_structure), len(seq_db))
            return False

        for index in range(len(seq_db)):
            if seq_db[index]["name"] != seq_structure[index]["name"]:
                logger.warning(
                    "Различие в имени последовательности: json '%s', БД '%s'",
                    seq_db[index]["name"],
                    seq_structure[index]["name"],
                )
                return False

            if seq_db[index]["cycle"] != seq_structure[index]["cycle"]:
                logger.warning(
                    "Различие в cycle последовательности: json '%s', БД '%s'",
                    seq_db[index]["cycle"],
                    seq_structure[index]["cycle"],
                )
                return False

            if seq_db[index]["data_type"] != seq_structure[index]["data_type"]:
                logger.warning(
                    "Различие в типе данных последовательности: json '%s', БД '%s'",
                    seq_db[index]["data_type"],
                    seq_structure[index]["data_type"],
                )
                return False

            if seq_db[index]["increment"] != seq_structure[index]["increment"]:
                logger.warning(
                    "Различие в шаге изменения счетчика последовательности: json '%s', БД '%s'",
                    seq_db[index]["increment"],
                    seq_structure[index]["increment"],
                )
                return False

            if seq_db[index]["maxvalue"] != seq_structure[index]["maxvalue"]:
                logger.warning(
                    "Различие в max значении счетчика последовательности: json '%s', БД '%s'",
                    seq_db[index]["maxvalue"],
                    seq_structure[index]["maxvalue"],
                )
                return False

            if seq_db[index]["minvalue"] != seq_structure[index]["minvalue"]:
                logger.warning(
                    "Различие в min значении счетчика последовательности: json '%s', БД '%s'",
                    seq_db[index]["minvalue"],
                    seq_structure[index]["minvalue"],
                )
                return False

            if seq_db[index]["start"] != seq_structure[index]["start"]:
                logger.warning(
                    "Различие в начальном значении счетчика последовательности: json '%s', БД '%s'",
                    seq_db[index]["start"],
                    seq_structure[index]["start"],
                )
                return False
    else:
        seq_db = table_from_db["sequences"]
        if seq_db:
            logger.warning("В json нет последовательностей, а в БД есть: %d", len(seq_db))
            return False

    logger.debug("Структуры таблиц полностью совпадают")
    return True


def _export_table_data(
    connection, table_name: str, schema_name: str = "public", excluded_columns: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Экспортирует данные таблицы в виде списка словарей.

    :param connection: Объект соединения с базой данных psycopg2.
    :param table_name: Имя таблицы в базе данных данные из которой необходимо экспортировать.
    :param schema_name: Имя схемы (по умолчанию "public").
    :param excluded_columns: Список колонок для исключения.
    :return: Список словарей содержащий данные таблицы.
    """
    excluded_columns = excluded_columns or []
    full_table_name = f"{schema_name}.{table_name}"

    logger.debug("Начало экспорта данных таблицы %s", full_table_name)
    logger.debug("Исключаемые колонки: %s", excluded_columns)

    with connection.cursor() as cursor:
        # Если есть исключаемые колонки, формируем запрос с явным указанием колонок
        if excluded_columns:
            cursor.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
                """,
                (table_name, schema_name),
            )
            all_columns = [row[0] for row in cursor.fetchall()]
            logger.debug("Все колонки таблицы: %s", all_columns)

            # Фильтруем исключенные колонки
            selected_columns = [col for col in all_columns if col not in excluded_columns]

            logger.debug("Выбрано колонок для экспорта: %d из %d", len(selected_columns), len(all_columns))
            logger.debug("Экспортируемые колонки: %s", selected_columns)
            logger.debug("Исключенные колонки: %s", excluded_columns)

            if selected_columns:
                columns_sql = sql.SQL(", ").join([sql.Identifier(col) for col in selected_columns])
                query = sql.SQL("SELECT {columns} FROM {table};").format(
                    columns=columns_sql, table=sql.Identifier(schema_name, table_name)
                )
                logger.debug("SQL запрос с фильтрацией колонок")
            else:
                logger.warning("Все колонки исключены из экспорта, возвращаем пустой список")
                return []

        else:
            logger.debug("Экспорт всех колонок таблицы, исключаемые отсутствуют")
            query = sql.SQL("SELECT * FROM {table};").format(table=sql.Identifier(schema_name, table_name))

        cursor.execute(query)
        rows: List[tuple] = cursor.fetchall()

        # Получение названий столбцов
        column_names: List[str] = [desc[0] for desc in cursor.description]
        logger.debug("Получено колонок: %s", column_names)
        logger.debug("Получено строк: %d", len(rows))

        # Преобразование данных в список словарей
        logger.debug("Преобразование данных в словари")
        data: List[Dict[str, Any]] = []
        for row in rows:
            row_dict: Dict[str, Any] = {column_names[i]: row[i] for i in range(len(column_names))}
            data.append(row_dict)

        logger.debug("Экспорт данных завершен: %d строк", len(data))
        return data


def _get_metadata_mock(table_name: str, operation: str = "export") -> Dict[str, Any]:
    """
    Заглушка для получения мета-данных классификатора.

    В будущем будет заменена на реальную логику получения данных из таблицы классификаторов.
    :param table_name: Имя таблицы классификатора
    :param operation: Тип операции (export/import)
    :return: Словарь с мета-данными
    """
    metadata = {
        "protocol_version": 1.0,
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),  # noqa: DTZ005
        "system_id": str(uuid.uuid4()),
        "note": f"Классификатор {table_name}",
        "msg_type": "02",
    }

    logger.debug(f"Сгенерированы мета-данные для {table_name}: {metadata}")
    return metadata


def _export_with_connection(
    connection: PgConnection, table_name: str, schema_name: str, excluded_columns: List[str]
) -> Dict[str, Any]:
    """Внутренняя функция для экспорта с использованием подключения."""
    metadata = _get_metadata_mock(table_name, "export")
    table = {
        "protocol_version": metadata["protocol_version"],
        "id": metadata["id"],
        "timestamp": metadata["timestamp"],
        "system_id": metadata["system_id"],
        "note": metadata["note"],
        "msg_type": metadata["msg_type"],
        "structure": _table_structure_to_dict(connection, table_name, schema_name, excluded_columns),
        "data": _export_table_data(connection, table_name, schema_name, excluded_columns),
    }
    return table


def export_table_to_dict(
    table_name: str,
    schema_name: str = "public",
    connection: Optional[Any] = None,
    dbname: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    excluded_columns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Преобразует таблицу в словарь со структурой и данными.

    :param table_name: Имя таблицы в базе данных.
    :param dbname: Имя базы данных.
    :param connection: Существующее подключение.
    :param user: Пользователь БД.
    :param password: Пароль пользователя.
    :param host: Адрес сервера баз данных.
    :param port: Порт сервера баз данных.
    :param schema_name: Имя схемы (по умолчанию "public").
    :param excluded_columns: Список колонок для исключения.
    :return: Словарь со структурой и данными таблицы.
    """
    excluded_columns = excluded_columns or []

    if connection is None:
        logger.debug("Создание нового подключения к БД")
        required_params = [dbname, user, password, host, port]
        if any(param is None for param in required_params):
            raise ValueError(
                "Все параметры подключения (dbname, user, password, host, port) "
                "должны быть указаны когда connection не предоставлен"
            )

        with psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as new_connection:
            logger.debug("Подключение к БД установлено")
            result = _export_with_connection(new_connection, table_name, schema_name, excluded_columns)
    else:
        logger.info("Использование существующего подключения")
        result = _export_with_connection(connection, table_name, schema_name, excluded_columns)

    logger.debug("Экспорт завершен успешно")
    return result


def _table_exists(connection, table_name, schema_name: str = "public"):
    """
    Проверяет, существует ли таблица с именем table_name в базе данных conn.

    :param connection: Подключение к базе данных psycopg2
    :param table_name: Имя таблицы (строка)
    :param schema_name: Имя схемы (по умолчанию "public").
    :return: True, если таблица существует, иначе False
    """
    full_table_name = f"{schema_name}.{table_name}"

    logger.debug("Проверка существования таблицы: %s", full_table_name)

    with connection.cursor() as cursor:
        query = sql.SQL(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = %s
            );
        """
        )
        logger.debug("Выполнение SQL запроса для проверки таблицы")
        cursor.execute(
            query,
            (
                schema_name,
                table_name,
            ),
        )
        result = cursor.fetchone()
        exists = result[0]

        if exists:
            logger.debug("Таблица %s существует", full_table_name)
        else:
            logger.debug("Таблица %s не найдена, переходим к созданию", full_table_name)

        return exists


def _collect_import_stats(results: List, primary_keys: List[str]) -> Dict[str, Any]:
    """Собирает статистику импорта из результатов запроса."""
    logger.debug("Сбор статистики импорта: %d результатов, первичные ключи: %s", len(results), primary_keys)
    detailed_stats = {
        "total_processed": len(results),
        "inserted": 0,
        "updated": 0,
        "inserted_records": [],
        "updated_records": [],
    }

    for row in results:
        pk_values = row[: len(primary_keys)]
        new_values_json = row[len(primary_keys)]
        old_values_json = row[len(primary_keys) + 1] if row[len(primary_keys) + 1] else {}
        operation = row[len(primary_keys) + 2]

        pk_dict = dict(zip(primary_keys, pk_values))
        new_values = dict(new_values_json) if new_values_json else {}
        old_values = dict(old_values_json) if old_values_json else {}

        if operation == "inserted":
            detailed_stats["inserted"] += 1
            detailed_stats["inserted_records"].append({"primary_key": pk_dict, "new_values": new_values})

        elif operation == "updated":
            detailed_stats["updated"] += 1

            changes = {}
            for key in new_values.keys():  # noqa: SIM118
                old_val = old_values.get(key)
                new_val = new_values.get(key)
                if old_val != new_val:
                    changes[key] = {"old_value": old_val, "new_value": new_val}

            detailed_stats["updated_records"].append(
                {"primary_key": pk_dict, "changes": changes, "old_values": old_values, "new_values": new_values}
            )

    logger.debug("Итоговая статистика импорта:")
    logger.debug("Всего обработано: %d", detailed_stats["total_processed"])
    logger.debug("Вставлено новых: %d", detailed_stats["inserted"])
    logger.debug("Обновлено существующих: %d", detailed_stats["updated"])

    return detailed_stats


def _format_stats_response(detailed_stats: Dict[str, Any], primary_keys: List[str]) -> Dict[str, Any]:
    """Форматирует детальную статистику для ответа API."""
    stats_response = {
        "total_processed": detailed_stats["total_processed"],
        "inserted": detailed_stats["inserted"],
        "updated": detailed_stats["updated"],
        "inserted_data": [
            {"primary_key": record["primary_key"], **record["new_values"]}
            for record in detailed_stats["inserted_records"]
        ],
        "updated_data": [
            {"primary_key": record["primary_key"], "changes": record["changes"]}
            for record in detailed_stats["updated_records"]
        ],
    }

    MAX_DETAILED_RECORDS = 100
    if len(stats_response["inserted_data"]) > MAX_DETAILED_RECORDS:
        stats_response["inserted_data"] = stats_response["inserted_data"][:MAX_DETAILED_RECORDS]
        stats_response["_note_inserted"] = (
            f"Показаны первые {MAX_DETAILED_RECORDS} из {detailed_stats['inserted']} записей"  # noqa: E501
        )

    if len(stats_response["updated_data"]) > MAX_DETAILED_RECORDS:
        stats_response["updated_data"] = stats_response["updated_data"][:MAX_DETAILED_RECORDS]
        stats_response["_note_updated"] = (
            f"Показаны первые {MAX_DETAILED_RECORDS} из {detailed_stats['updated']} записей"  # noqa: E501
        )

    return stats_response


def _build_upsert_query_with_stats(
    schema_name: str,
    table_name: str,
    temp_table_name: str,
    json_columns: List[str],
    primary_keys: List[str],
    cast_expressions: List[sql.Composable],
) -> sql.Composable:
    """Создает UPSERT запрос с возвратом статистики."""
    return sql.SQL("""
        WITH typed_temp_table AS (
            -- Приводим типы во временной таблице
            SELECT {cast_expressions}
            FROM {temp_table} t
        ),
        old_data AS (
            -- Теперь JOIN работает без проблем с типами
            SELECT
                {pk_columns},
                to_jsonb({main_table}.*) as old_values
            FROM typed_temp_table ttt
            LEFT JOIN {main_table} ON {join_conditions}
            WHERE {main_table}.{pk1} IS NOT NULL
        ),
        upsert_data AS (
            INSERT INTO {main_table} ({columns})
            SELECT *
            FROM typed_temp_table
            ON CONFLICT ({pk}) DO UPDATE SET
            {update_set}
            RETURNING *
        ),
        result_data AS (
            SELECT
                {pk_columns_ud},
                to_jsonb(ud.*) as new_values,
                od.old_values as old_values,
                CASE
                    WHEN od.old_values IS NULL THEN 'inserted'
                    WHEN od.old_values IS NOT NULL AND od.old_values != to_jsonb(ud.*) THEN 'updated'
                    ELSE 'unchanged'
                END as operation
            FROM upsert_data ud
            LEFT JOIN old_data od ON {join_conditions_ud_od}
        )
        SELECT * FROM result_data
    """).format(
        main_table=sql.Identifier(schema_name, table_name),
        temp_table=sql.Identifier(temp_table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, json_columns)),
        cast_expressions=sql.SQL(", ").join(cast_expressions),
        pk=sql.SQL(", ").join(map(sql.Identifier, primary_keys)),
        pk1=sql.Identifier(primary_keys[0]),
        update_set=sql.SQL(", ").join(
            [
                sql.SQL("{column} = EXCLUDED.{column}").format(column=sql.Identifier(column))
                for column in json_columns
                if column not in primary_keys
            ]
        ),
        pk_columns=sql.SQL(", ").join([sql.SQL("ttt.{}").format(sql.Identifier(pk)) for pk in primary_keys]),
        pk_columns_ud=sql.SQL(", ").join([sql.SQL("ud.{}").format(sql.Identifier(pk)) for pk in primary_keys]),
        join_conditions=sql.SQL(" AND ").join(
            [
                sql.SQL("ttt.{pk} = {main_table}.{pk}").format(
                    pk=sql.Identifier(pk), main_table=sql.Identifier(schema_name, table_name)
                )
                for pk in primary_keys
            ]
        ),
        join_conditions_ud_od=sql.SQL(" AND ").join(
            [sql.SQL("ud.{pk} = od.{pk}").format(pk=sql.Identifier(pk)) for pk in primary_keys]
        ),
    )


def _build_simple_upsert_query(
    schema_name: str,
    table_name: str,
    temp_table_name: str,
    json_columns: List[str],
    primary_keys: List[str],
    cast_expressions: List[sql.Composable],
) -> sql.Composable:
    """Создает простой UPSERT запрос (для обратной совместимости без сбора статистики)."""
    return sql.SQL("""
        INSERT INTO {main_table} ({columns})
        SELECT {cast_expressions}
        FROM {temp_table} t
        ON CONFLICT ({pk}) DO UPDATE SET
        {update_set}
    """).format(
        main_table=sql.Identifier(schema_name, table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, json_columns)),
        temp_table=sql.Identifier(temp_table_name),
        cast_expressions=sql.SQL(", ").join(cast_expressions),
        pk=sql.SQL(", ").join(map(sql.Identifier, primary_keys)),
        update_set=sql.SQL(", ").join(
            [
                sql.SQL("{column} = EXCLUDED.{column}").format(column=sql.Identifier(column))
                for column in json_columns
                if column not in primary_keys
            ]
        ),
    )


def _validate_primary_keys(primary_keys: List[str], excluded_columns: List[str], schema_name: str, table_name: str):
    """Валидирует структуру импортруемрго json по первичным ключам."""
    if not primary_keys:
        raise ValueError(
            f"Таблица {schema_name}.{table_name} не имеет первичного ключа. "
            f"Импорт данных возможен только в таблицы с первичным ключом для обеспечения "
            f"корректной работы UPSERT (вставка и обновление)."
        )

    for pk in primary_keys:
        if pk in excluded_columns:
            raise ValueError(
                f"Первичный ключ '{pk}' не может быть исключаемой колонкой. Исключаемые колонки: {excluded_columns}"
            )


def _create_temp_table(cursor, table_name: str, json_columns: List[str]) -> str:
    """Создает временную таблицу."""
    temp_table_name = f"temp_{table_name}_{uuid.uuid4().hex[:8]}"

    logger.debug("Создание временной таблицы для импорта")
    logger.debug("Исходная таблица: %s", table_name)
    logger.debug("Временная таблица: %s", temp_table_name)
    logger.debug("Колонки для импорта: %s", json_columns)
    logger.debug("Количество колонок: %d", len(json_columns))

    create_temp_query = sql.SQL("""
        CREATE TEMPORARY TABLE {temp_table} ({columns})
    """).format(
        temp_table=sql.Identifier(temp_table_name),
        columns=sql.SQL(", ").join([sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in json_columns]),
    )
    try:
        cursor.execute(create_temp_query)
        logger.debug("Временная таблица %s успешно создана", temp_table_name)
        return temp_table_name

    except Exception as e:
        logger.error("Ошибка создания временной таблицы %s: %s", temp_table_name, str(e), exc_info=True)
        raise


def _populate_temp_table(cursor, temp_table_name: str, json_columns: List[str], table_data: List[Dict[str, Any]]):
    """Заполняет временную таблицу данными."""
    logger.debug("Начало заполнения временной таблицы %s данными", temp_table_name)
    logger.debug("Данные для импорта: %d записей, %d колонок", len(table_data), len(json_columns))

    if not table_data:
        logger.debug("Нет данных для заполнения временной таблицы")
        return

    insert_temp_query = sql.SQL("INSERT INTO {temp_table} ({columns}) VALUES %s").format(
        temp_table=sql.Identifier(temp_table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, json_columns)),
    )

    values = []
    for data in table_data:
        row_values = []
        for col in json_columns:
            value = data.get(col)
            if isinstance(value, list):
                row_values.append(",".join(map(str, value)))
            else:
                row_values.append(str(value) if value is not None else None)
        values.append(tuple(row_values))

    if values:
        logger.debug("Пример первой строки данных: %s", values[0])
        logger.debug("Пример последней строки данных: %s", values[-1])

    logger.debug("Вставка %d записей во временную таблицу", len(values))

    try:
        execute_values(cursor, insert_temp_query, values)
        logger.debug("Временная таблица %s успешно заполнена %d записями", temp_table_name, len(values))

    except Exception as e:
        logger.error("Ошибка заполнения временной таблицы %s: %s", temp_table_name, str(e), exc_info=True)
        raise


def _import_table_data(
    connection,
    table_name: str,
    table_data: List[Dict[str, Any]],
    table_structure: Dict[str, Any],
    foreign_tables_mapping: Union[Dict[Tuple[str, str], Tuple[str, str]], None] = None,
    schema_name: str = "public",
    excluded_columns: Optional[List[str]] = None,
    return_stats: bool = False,
) -> Union[None, Dict[str, Any]]:
    """
    Импортирует данные из списка словарей в таблицу при этом заменяя старые данные новыми.

    :param connection: Объект соединения с базой данных psycopg2.
    :param table_name: Имя таблицы в базе данных в которую осуществляется импорт.
    :param table_data: Данные для импорта.
    :param table_structure: Метаданные о структуре таблицы.
    :param schema_name: Имя схемы (по умолчанию "public").
    :param excluded_columns: Список колонок для исключения.
    :param return_stats: Если True, возвращает статистику.
    :return: Если return_stats=True, возвращает словарь со статистикой.
    :raises ValueError: Если в таблице нет первичного ключа.
    """
    excluded_columns = excluded_columns or []
    full_table_name = f"{schema_name}.{table_name}"

    logger.debug("Начало импорта данных в таблицу %s", full_table_name)
    logger.debug("Данные для импорта: %d записей", len(table_data))
    logger.debug("Исключаемые колонки: %s", excluded_columns)
    logger.debug("Возврат статистики: %s", return_stats)

    if foreign_tables_mapping is None:
        foreign_tables_mapping = {}

    with connection.cursor() as cursor:
        constraints = _fetch_constraints(cursor, table_name, schema_name=schema_name)
        logger.debug("Найдено ограничений: %d", len(constraints))

        primary_keys = [
            constraint["column"] for constraint in constraints if constraint["constraint_type"] == "PRIMARY KEY"
        ]
        logger.debug("Найдены первичные ключи: %s", primary_keys)

        _validate_primary_keys(primary_keys, excluded_columns, schema_name, table_name)
        logger.debug("Проверка первичных ключей пройдена")

        json_columns = [column["name"] for column in table_structure["columns"]]

        has_self_referencing_fk = any(
            constraint["constraint_type"] == "FOREIGN KEY"
            and constraint["foreign_table_schema"] == schema_name
            and constraint["foreign_table"] == table_name
            for constraint in constraints
        )

        if has_self_referencing_fk:
            logger.debug("Обнаружен self-referencing FOREIGN KEY, откладываем проверки на конец функции")
            cursor.execute("SET CONSTRAINTS ALL DEFERRED")

        temp_table_name = _create_temp_table(cursor, table_name, json_columns)

        _populate_temp_table(cursor, temp_table_name, json_columns, table_data)

        cast_expressions = []
        for column in json_columns:
            col_meta = next((col for col in table_structure["columns"] if col["name"] == column), None)

            if col_meta:
                cast_expr = _get_column_cast_expression(col_meta)
                cast_expressions.append(cast_expr)
            else:
                continue

        if return_stats:
            logger.debug("Сбор статистики импорта включен")
            upsert_query = _build_upsert_query_with_stats(
                schema_name, table_name, temp_table_name, json_columns, primary_keys, cast_expressions
            )
            logger.debug("Выполнение UPSERT запроса со статистикой")
            cursor.execute(upsert_query)
            results = cursor.fetchall()
            detailed_stats = _collect_import_stats(results, primary_keys)
            stats_response = _format_stats_response(detailed_stats, primary_keys)

        else:
            logger.debug("Сбор статистики импорта отключен")
            upsert_query = _build_simple_upsert_query(
                schema_name, table_name, temp_table_name, json_columns, primary_keys, cast_expressions
            )
            cursor.execute(upsert_query)
            logger.debug("UPSERT запрос без статистики выполнен успешно")

        if has_self_referencing_fk:
            logger.debug("Восстановление проверок ограничений")
            cursor.execute("SET CONSTRAINTS ALL IMMEDIATE")

        _validate_foreign_keys(table_name, schema_name, cursor, constraints)
        logger.debug("Валидация внешних ключей self-referencing пройдена")

        _update_sequences(table_data, table_structure, schema_name, cursor, primary_keys)
        logger.debug("Последовательности обновлены")

        _drop_temp_table(cursor, temp_table_name)
        logger.debug("Временная таблица удалена")

        if return_stats:
            logger.debug("Импорт данных в %s завершен успешно, возвращаем статистику", full_table_name)
            return stats_response

        logger.debug("Импорт данных в %s завершен успешно", full_table_name)
        return None


def _update_sequences(
    table_data: List[Dict[str, Any]],
    table_structure: Dict[str, Any],
    schema_name: str,
    cursor: Any,
    primary_keys: List[str],
) -> None:
    """
    Обновляет значения последовательностей (sequences) для таблицы после импорта данных.

    Функция находит максимальное значение первичного ключа в импортируемых данных
    и обновляет связанные последовательности, чтобы избежать конфликтов при будущих вставках.
    """
    if table_structure.get("sequences") and table_data:
        max_id = 0
        for data in table_data:
            data_id = data.get(primary_keys[0])
            if data_id is not None and data_id > max_id:
                max_id = data_id
        if max_id > 0:
            for sequence in table_structure["sequences"]:
                sequence_name = sequence["name"]

                if "." not in sequence_name:
                    sequence_name = f"{schema_name}.{sequence_name}"

                try:
                    update_seq_query = sql.SQL("SELECT setval({}, {}, false)").format(
                        sql.Literal(sequence_name), sql.Literal(max_id + 1)
                    )
                    cursor.execute(update_seq_query)
                except Exception:
                    pass


def _drop_temp_table(cursor: Any, temp_table_name: str) -> None:
    """Удаляет временную таблицу из базы данных."""
    drop_query = sql.SQL("DROP TABLE {temp_table}").format(temp_table=sql.Identifier(temp_table_name))
    cursor.execute(drop_query)


def _validate_foreign_keys(table_name: str, schema_name: str, cursor: Any, constraints: List[Dict[str, Any]]):
    """
    Проверяет целостность self-referencing foreign key constraints.

    Валидирует, что все внешние ключи, ссылающиеся на ту же таблицу, указывают
    на существующие записи. Это важно для иерархических данных и самоссылающихся таблиц.
    """
    for constraint in constraints:
        if (
            constraint["constraint_type"] == "FOREIGN KEY"
            and constraint["column"] is not None
            and constraint["foreign_column"] is not None
            and constraint["foreign_table"] == table_name
        ):
            check_fk_query = sql.SQL("""
                        SELECT COUNT(*)
                        FROM {main_table} t
                        LEFT JOIN {main_table} p ON t.{fk_column} = p.{pk_column}
                        WHERE t.{fk_column} IS NOT NULL
                        AND p.{pk_column} IS NULL
                    """).format(
                main_table=sql.Identifier(schema_name, table_name),
                fk_column=sql.Identifier(constraint["column"]),
                pk_column=sql.Identifier(constraint["foreign_column"]),
            )

            cursor.execute(check_fk_query)
            invalid_count = cursor.fetchone()[0]

            if invalid_count > 0:
                raise ValueError(f"Найдено {invalid_count} записей с некорректными ссылками на родителя")


def _import_with_connection(
    connection: Any,
    table_structure: Dict[str, Any],
    table_data: List[Dict[str, Any]],
    table_name: str,
    foreign_tables_mapping: Optional[Dict[Tuple[str, str], Tuple[str, str]]],
    schema_name: str,
    excluded_columns: Optional[List[str]] = None,
    return_stats: bool = False,
) -> Union[None, Dict[str, Any]]:
    """Внутренняя функция для импорта с использованием подключения."""
    excluded_columns = excluded_columns or []
    full_table_name = f"{schema_name}.{table_name}"

    logger.debug("Начало импорта с подключением для таблицы %s", full_table_name)
    logger.debug("Данные: %d записей, структура: %d колонок", len(table_data), len(table_structure.get("columns", [])))
    logger.debug("Исключаемые колонки: %s", excluded_columns)
    logger.debug("Возврат статистики: %s", return_stats)

    if not _table_exists(connection, table_name=table_name, schema_name=schema_name):
        _create_table_from_dict(
            connection,
            table_structure=table_structure,
            new_table_name=table_name,
            foreign_tables_mapping=foreign_tables_mapping,
            schema_name=schema_name,
        )
    else:
        if not _compare_table_structure(
            connection,
            table_structure=table_structure,
            table_name=table_name,
            foreign_tables_mapping=foreign_tables_mapping,
            schema_name=schema_name,
            excluded_columns=excluded_columns,
        ):
            raise ValueError("Структура таблицы в базе данных не совпадает с переданной")

        if return_stats:
            return _import_table_data(
                connection,
                table_name=table_name,
                table_data=table_data,
                table_structure=table_structure,
                foreign_tables_mapping=foreign_tables_mapping,
                schema_name=schema_name,
                excluded_columns=excluded_columns,
                return_stats=return_stats,
            )
        _import_table_data(
            connection,
            table_name=table_name,
            table_data=table_data,
            table_structure=table_structure,
            foreign_tables_mapping=foreign_tables_mapping,
            schema_name=schema_name,
            excluded_columns=excluded_columns,
        )
        return None
    return None


def import_table_from_dict(
    table: Dict[str, Any],
    table_name: str,
    dbname: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    foreign_tables_mapping: Optional[Dict[Tuple[str, str], Tuple[str, str]]] = None,
    schema_name: str = "public",
    connection: Optional[Any] = None,
    excluded_columns: Optional[List[str]] = None,
    return_stats: bool = False,
) -> Union[None, Dict[str, Any]]:
    """
    Импортирует данные из словаря в базу данных.

    :param table: Структура таблицы и данные для импорта в виде словаря.
    :param table_name: Имя таблицы в базе данных.
    :param dbname: Имя базы данных.
    :param user: Пользователь БД.
    :param password: Пароль пользователя.
    :param host: Адрес сервера баз данных.
    :param port: Порт сервера баз данных.
    :param foreign_tables_mapping: Словарь соответствия имен связанных таблиц и схем в словаре и в базе данных состоит
    из кортежей с парой значений ("имя_схемы", "имя_таблицы") ключи имена в словаре, значения в имена базе.
    :param schema_name: Имя схемы (по умолчанию 'public').
    :param excluded_columns: Список колонок для исключения при сравнении.
    :param return_stats: Если True, возвращает статистику.
    :return: Если return_stats=True, возвращает словарь со статистикой.
    """
    excluded_columns = excluded_columns or []

    if connection is None and any(param is None for param in [dbname, user, password, host, port]):
        raise ValueError("Все параметры подключения должны быть указаны когда connection не предоставлен")

    table_structure = table["structure"]
    table_data = table["data"]

    if connection is not None:
        return _import_with_connection(
            connection,
            table_structure,
            table_data,
            table_name,
            foreign_tables_mapping,
            schema_name,
            excluded_columns,
            return_stats=return_stats,
        )
    with psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as new_connection:
        return _import_with_connection(
            new_connection,
            table_structure,
            table_data,
            table_name,
            foreign_tables_mapping,
            schema_name,
            excluded_columns,
            return_stats=return_stats,
        )
