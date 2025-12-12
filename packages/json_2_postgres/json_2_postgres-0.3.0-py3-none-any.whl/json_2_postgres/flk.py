# json_2_postgres/flk.py
import json
import logging
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict
from typing import Any, Dict, List, Optional, Tuple, Union

import jsonschema

from .table_to_dict import (
    # _constraint_contains_excluded_columns,
    # _fetch_columns,
    # _fetch_constraints,
    # _fetch_sequence_params,
    # _fetch_table_comment,
    # _sequence_related_to_excluded_columns,
    _table_structure_to_dict,
)

logger = logging.getLogger("json_2_postgres")


class FLKReceiptPayload(TypedDict):
    """Payload квитанции ФЛК."""

    parent_msg_id: Optional[str]
    read_check: bool
    schema_check: bool
    data_and_structure_check: bool
    structure_check: bool
    proto_check: bool
    flk_success: bool
    timestamp: str
    statistics: Optional[Dict[str, Any]]
    error_details: Optional[str]
    comments: List[str]


class FLKReceipt(TypedDict):
    """Квитанция форматно-логического контроля."""

    protocol_version: float
    id: str
    timestamp: str
    system_id: str
    note: str
    msg_type: str
    payload: FLKReceiptPayload


class FLKValidator:
    """
    Валидатор для форматно-логического контроля JSON классификаторов.

    Обеспечивает проверку:
    - Чтения и парсинга JSON данных
    - Соответствия JSON схеме
    - Согласованности структуры и данных
    - Совместимости с существующими таблицами БД
    """

    def __init__(self):
        """
        Инициализирует валидатор со схемами для известных классификаторов.

        Attributes:
            classifier_schemas (Dict[str, Dict]): Словарь схем для конкретных классификаторов
            generic_schemas (Dict): Общая схема для неизвестных классификаторов
        """
        self.classifier_schemas = {
            "division": self._get_divisions_schema(),
            # Добавляем новые классификаторы по мере появления
        }
        self.generic_schema = self._get_generic_schema()

    def _get_divisions_schema(self):
        """Схема для классификатора подразделений."""
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["data", "structure"],
            "properties": {
                # Мета-поля
                "protocol_version": {"type": ["number", "null"]},
                "id": {"type": ["string", "null"], "format": "uuid"},
                "timestamp": {"type": ["string", "null"], "format": "date-time"},
                "system_id": {"type": ["string", "null"]},
                "note": {"type": ["string", "null"]},
                "msg_type": {"type": ["string", "null"]},
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "name"],
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "name_short": {"type": ["string", "null"]},
                            "id_parent": {"type": ["integer", "null"]},
                            "parent_id": {"type": ["integer", "null"]},
                            "id_type": {"type": "integer"},
                            "code": {"type": ["string", "null"]},
                            "all_children_ids": {"type": ["array", "null"], "items": {"type": ["integer", "null"]}},
                            "is_active": {"type": ["boolean", "null"]},
                        },
                    },
                },
                "structure": {
                    "type": "object",
                    "required": ["table", "columns", "constraints", "sequences"],
                    "properties": {
                        "table": {"type": "string"},
                        "comment": {"type": ["string", "null"]},
                        "columns": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "type", "nullable", "default", "comment"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "nullable": {"type": "boolean"},
                                    "default": {"type": ["string", "null"]},
                                    "comment": {"type": ["string", "null"]},
                                },
                            },
                        },
                        "constraints": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["constraint_type", "constraint_name"],
                                "properties": {
                                    "constraint_type": {"type": "string"},
                                    "constraint_name": {"type": "string"},
                                    "column": {"type": ["string", "null"]},
                                    "foreign_table": {"type": ["string", "null"]},
                                    "foreign_table_schema": {"type": ["string", "null"]},
                                    "foreign_column": {"type": ["string", "null"]},
                                    "check_clause": {"type": ["string", "null"]},
                                },
                            },
                        },
                        "sequences": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "name",
                                    "data_type",
                                    "increment",
                                    "minvalue",
                                    "maxvalue",
                                    "start",
                                    "cycle",
                                    "current_value",
                                ],
                                "properties": {
                                    "name": {"type": "string"},
                                    "data_type": {"type": "string"},
                                    "increment": {"type": "string"},
                                    "minvalue": {"type": "string"},
                                    "maxvalue": {"type": "string"},
                                    "start": {"type": "string"},
                                    "cycle": {"type": "boolean"},
                                    "current_value": {"type": ["integer", "null"]},
                                },
                            },
                        },
                    },
                },
            },
        }

    def _get_generic_schema(self):
        """Общая схема для неизвестных классификаторов."""
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["data", "structure"],
            "properties": {
                # Мета-поля
                "protocol_version": {"type": ["number", "null"]},
                "id": {"type": ["string", "null"], "format": "uuid"},
                "timestamp": {"type": ["string", "null"], "format": "date-time"},
                "system_id": {"type": ["string", "null"]},
                "note": {"type": ["string", "null"]},
                "msg_type": {"type": ["string", "null"]},
                # Основные данные
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "minProperties": 1,
                        "additionalProperties": {  # могут быть любые поля
                            "anyOf": [
                                {"type": "string"},
                                {"type": "integer"},
                                {"type": "null"},
                                {"type": "boolean"},
                                {"type": "number"},
                                {"type": "array", "items": {"type": "integer"}},
                            ]
                        },
                    },
                },
                "structure": {
                    "type": "object",
                    "required": ["table", "columns", "constraints", "sequences"],
                    "properties": {
                        "table": {"type": "string"},
                        "comment": {"type": ["string", "null"]},
                        "columns": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["name", "type", "nullable", "default", "comment"],
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"type": "string"},
                                    "nullable": {"type": "boolean"},
                                    "default": {"type": ["string", "null"]},
                                    "comment": {"type": ["string", "null"]},
                                },
                            },
                        },
                        "constraints": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["constraint_type", "constraint_name"],
                                "properties": {
                                    "constraint_type": {"type": "string"},
                                    "constraint_name": {"type": "string"},
                                    "column": {"type": ["string", "null"]},
                                    "foreign_table": {"type": ["string", "null"]},
                                    "foreign_table_schema": {"type": ["string", "null"]},
                                    "foreign_column": {"type": ["string", "null"]},
                                    "check_clause": {"type": ["string", "null"]},
                                },
                            },
                        },
                        "sequences": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": [
                                    "name",
                                    "data_type",
                                    "increment",
                                    "minvalue",
                                    "maxvalue",
                                    "start",
                                    "cycle",
                                    "current_value",
                                ],
                                "properties": {
                                    "name": {"type": "string"},
                                    "data_type": {"type": "string"},
                                    "increment": {"type": "string"},
                                    "minvalue": {"type": "string"},
                                    "maxvalue": {"type": "string"},
                                    "start": {"type": "string"},
                                    "cycle": {"type": "boolean"},
                                    "current_value": {"type": ["integer", "null"]},
                                },
                            },
                        },
                    },
                },
            },
        }

    def validate_classifier(
        self,
        json_data: Union[str, Dict, Path],
        connection: Optional[Any] = None,
        schema_name: str = "classification",
        table_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """ФЛК с поддержкой дополнительных полей."""
        receipt_data = {
            "read_check": False,
            "schema_check": False,
            "data_and_structure_check": False,
            "structure_check": False,
            "proto_check": True,
            "flk_success": False,
            "statistics": self._get_base_statistics(),
            "error_details": None,
            "comments": [],
        }

        try:
            # 1. Проверка чтения данных
            logger.debug("Проверка чтения данных")
            parsed_data = self._check_readable(json_data)
            if not parsed_data:
                receipt_data["error_details"] = "Ошибка чтения данных"
                receipt_data["comments"].append("Не удалось прочитать или распарсить JSON данные")
                logger.error("Ошибка чтения данных")
                return self._build_flk_response(receipt_data)

            receipt_data["read_check"] = True
            receipt_data["comments"].append("JSON данные успешно прочитаны")
            receipt_data["statistics"] = self._get_base_statistics(parsed_data)

            # 2. Проверка JSON схемы (гибкая)
            logger.debug("Проверка JSON схемы")
            schema_ok, schema_comments = self._check_json_schema(parsed_data)
            receipt_data["schema_check"] = schema_ok
            receipt_data["comments"].extend(schema_comments)

            if not schema_ok:
                receipt_data["error_details"] = "Несоответствие JSON схеме классификатора"
                logger.error("Ошибка JSON схемы")
                return self._build_flk_response(receipt_data, parsed_data)

            # 3. Проверка соответствия структуры и данных
            logger.debug("Проверка соответствия структуры и данных")
            structure_ok, structure_comments = self._check_structure_data_consistency(parsed_data)
            receipt_data["data_and_structure_check"] = structure_ok
            receipt_data["comments"].extend(structure_comments)

            if not structure_ok:
                receipt_data["error_details"] = "Несоответствие структуры и данных"
                logger.error("Ошибка соответствия структуры и данных")
                return self._build_flk_response(receipt_data, parsed_data)

            # 4.Проверка существования таблицы и совместимости
            table_name = table_name if table_name else parsed_data["structure"]["table"]
            table_name_from_json = parsed_data["structure"]["table"]

            logger.debug(f"Имя таблицы для проверки из базы: '{table_name}' (из JSON: '{table_name_from_json}')")

            if connection:
                # Проверяем существование таблицы
                table_exists = self._table_exists(connection, table_name, schema_name)

                if table_exists:
                    receipt_data["comments"].append(f"Таблица {schema_name}.{table_name} существует в БД")
                    logger.debug(f"Таблица {schema_name}.{table_name} существует")

                    # Если таблица существует, можно проверить совместимость
                    target_structure = self._get_table_structure(connection, table_name, schema_name)
                    if target_structure:
                        receipt_data["comments"].append(f"Структура таблицы {table_name} успешно получена из БД")
                        compatibility_ok, compatibility_comments = self._check_structure_compatibility(
                            parsed_data["structure"], target_structure
                        )
                        receipt_data["structure_check"] = compatibility_ok
                        receipt_data["comments"].extend(compatibility_comments)

                        if not compatibility_ok:
                            receipt_data["error_details"] = "Несовместимость с целевой структурой"
                            logger.error("Ошибка совместимости структур")
                    else:
                        receipt_data["structure_check"] = False
                        receipt_data["comments"].append(
                            "Таблица существует, но проверка совместимости не выполнялась -отсутствует target_structure"
                        )
                else:
                    receipt_data["comments"].append(
                        f"Таблица {schema_name}.{table_name} не существует в БД - будет создана при импорте"
                    )
                    receipt_data["structure_check"] = True
                    logger.debug(f"Таблица {schema_name}.{table_name} не существует")
            else:
                receipt_data["structure_check"] = False
                receipt_data["comments"].append(
                    "Проверка существования таблицы не выполнялась (отсутствует connection)"
                )
                logger.debug("Проверка существования таблицы пропущена")

            # Определяем общий успех ФЛК
            # Основные проверки (чтение, схема, данные) должны быть успешными
            basic_checks_ok = all(
                [
                    receipt_data["read_check"],
                    receipt_data["schema_check"],
                    receipt_data["data_and_structure_check"],
                    receipt_data["structure_check"],
                ]
            )

            receipt_data["flk_success"] = basic_checks_ok

            if receipt_data["flk_success"]:
                receipt_data["statistics"] = {
                    "table_name": table_name,
                    "columns_count": len(parsed_data["structure"]["columns"]),
                    "records_count": len(parsed_data["data"]),
                    "table_exists": connection and self._table_exists(connection, table_name, schema_name)
                    if connection
                    else None,
                }

                receipt_data["comments"].append("Все проверки ФЛК пройдены успешно")
                logger.info(f"ФЛК пройден успешно: {table_name} - {len(parsed_data['data'])} записей")
            else:
                receipt_data["comments"].append("ФЛК не пройден")
                logger.warning(f"ФЛК не пройден для таблицы {table_name}")

            return self._build_flk_response(receipt_data, parsed_data)

        except Exception as e:
            receipt_data["error_details"] = f"Непредвиденная ошибка ФЛК: {str(e)}"
            receipt_data["comments"].append(f"Системная ошибка: {str(e)}")
            logger.error(f"Непредвиденная ошибка ФЛК: {str(e)}", exc_info=True)
            return self._build_flk_response(receipt_data)

    def _table_exists(self, connection, table_name: str, schema_name: str = "classification") -> bool:
        """Проверяет существование таблицы в БД."""
        try:
            logger.debug(f"Проверка существования таблицы: {schema_name}.{table_name}")

            with connection.cursor() as cursor:
                query = """
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables
                        WHERE table_schema = %s
                        AND table_name = %s
                    );
                """
                cursor.execute(query, (schema_name, table_name))
                result = cursor.fetchone()
                exists = result[0]

                if exists:
                    logger.debug(f"Таблица {schema_name}.{table_name} существует")
                else:
                    logger.debug(f"Таблица {schema_name}.{table_name} не найдена")

                return exists

        except Exception as e:
            logger.error(f"Ошибка при проверке существования таблицы {schema_name}.{table_name}: {str(e)}")
            return False

    def _get_table_structure(
        self, connection: Any, table_name: str, schema_name: str = "classification"
    ) -> Optional[Dict[str, Any]]:
        """Получение структуры таблицы используя функцию экспорта."""
        try:
            logger.debug(f"Получение структуры таблицы {schema_name}.{table_name} из БД")

            structure = _table_structure_to_dict(
                connection=connection, table_name=table_name, schema_name=schema_name, excluded_columns=None
            )

            if structure:
                logger.debug(f"Структура таблицы {table_name} успешно получена")
                logger.debug(
                    f"Получено колонок: {len(structure['columns'])}, "
                    f"ограничений: {len(structure['constraints'])}, "
                    f"последовательностей: {len(structure['sequences'])}"
                )
                return structure

            logger.warning(f"Не удалось получить структуру таблицы {table_name}")
            return None

        except Exception as e:
            logger.error(f"Ошибка при получении структуры таблицы {table_name}: {str(e)}", exc_info=True)
            return None

    def _get_base_statistics(self, parsed_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Возвращает базовую статистику даже при ошибках."""
        base_stats = {"table_name": "unknown", "columns_count": 0, "records_count": 0, "table_exists": None}
        if not parsed_data:
            return base_stats

        try:
            return {
                "table_name": parsed_data["structure"]["table"]
                if parsed_data and "structure" in parsed_data
                else "unknown",
                "columns_count": len(parsed_data["structure"]["columns"])
                if parsed_data and "structure" in parsed_data
                else 0,
                "records_count": len(parsed_data["data"]) if parsed_data and "data" in parsed_data else 0,
                "table_exists": None,
            }
        except Exception:
            return base_stats

    def _check_readable(self, json_data: Union[str, Dict, Path]) -> Optional[Dict]:
        """Проверка возможности чтения данных."""
        try:
            if isinstance(json_data, Path) or (isinstance(json_data, str) and "/" in json_data):
                path = Path(json_data)
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            elif isinstance(json_data, str):
                logger.debug("Чтение JSON строки")
                return json.loads(json_data)
            else:
                logger.debug("Использование готового словаря")
                return json_data
        except Exception as e:
            logger.error(f"Ошибка чтения данных: {str(e)}")
            return None

    def _check_json_schema(self, data: Dict) -> Tuple[bool, List[str]]:
        """Гибкая проверка JSON схемы."""
        comments = []
        try:
            table_name = data["structure"]["table"]  # будет меняться источник названия
            schema = self.classifier_schemas.get(table_name, self.generic_schema)

            jsonschema.validate(instance=data, schema=schema)

            if table_name in self.classifier_schemas:
                comments.append(f"JSON схема соответствует формату классификатора '{table_name}'")
                logger.debug(f"Использована специфичная схема для {table_name}")
            else:
                comments.append(f"JSON схема прошла общую проверку (неизвестный классификатор '{table_name}')")
                logger.debug(f"Использована общая схема для неизвестного классификатора {table_name}")

            return True, comments

        except jsonschema.ValidationError as e:
            comments.append(f"Ошибка валидации JSON схемы: {e.message}")
            logger.debug(f"Ошибка валидации схемы для {data['structure']['table']}: {e.message}")
            return False, comments

    def _check_structure_data_consistency(self, data: Dict) -> Tuple[bool, List[str]]:
        """Проверка соответствия данных и структуры в json."""
        comments = []
        try:
            structure = data["structure"]
            table_data = data["data"]

            expected_columns = {col["name"] for col in structure["columns"]}
            required_columns = {col["name"] for col in structure["columns"] if not col.get("nullable", True)}

            if not table_data:
                comments.append("Таблица не содержит данных")
                return True, comments

            # Быстрая проверка: если все записи имеют одинаковый набор колонок
            first_columns = set(table_data[0].keys())
            all_same_structure = all(set(record.keys()) == first_columns for record in table_data)

            if all_same_structure:
                # Все записи идентичны по структуре - проверяем только первую
                actual_columns = first_columns

                # Лишние колонки
                extra_columns = actual_columns - expected_columns
                if extra_columns:
                    comments.append(f"Обнаружены лишние колонки: {extra_columns}")
                    logger.debug(f"Лишние колонки в данных: {extra_columns}")
                    return False, comments

                # Обязательные колонки
                missing_columns = required_columns - actual_columns
                if missing_columns:
                    comments.append(f"Отсутствуют обязательные колонки: {missing_columns}")
                    return False, comments

            else:
                # Записи имеют разную структуру - проверяем все
                all_extra_columns = set()
                problem_records = 0

                for i, record in enumerate(table_data):
                    actual_columns = set(record.keys())

                    # Быстрая проверка лишних колонок
                    if not actual_columns.issubset(expected_columns):
                        record_extra = actual_columns - expected_columns
                        all_extra_columns.update(record_extra)
                        problem_records += 1
                        if problem_records <= 3:  # Логируем только первые 3 ошибки
                            comments.append(f"Запись {i}: лишние колонки {record_extra}")

                    # Быстрая проверка обязательных колонок
                    if not required_columns.issubset(actual_columns):
                        record_missing = required_columns - actual_columns
                        problem_records += 1
                        if problem_records <= 3:
                            comments.append(f"Запись {i}: отсутствуют {record_missing}")

                if all_extra_columns:
                    comments.insert(0, f"Обнаружены лишние колонки: {all_extra_columns} (в {problem_records} записях)")
                    return False, comments

            # Проверка типов данных (выборочно)
            sample_size = min(50, len(table_data))  # Проверяем не более 50 записей
            type_errors = self._validate_data_types(structure, table_data[:sample_size])
            if type_errors:
                comments.extend(type_errors[:5])  # Ограничиваем вывод ошибок
                logger.debug(f"Ошибки типов данных: {type_errors[:5]}")
                if len(type_errors) > 5:
                    comments.append(f"... и еще {len(type_errors) - 5} ошибок типов")
                    logger.debug(f"... и еще {len(type_errors) - 5} ошибок типов")
                return False, comments

            comments.append(f"Структура и данные согласованы (проверено {len(table_data)} записей)")
            return True, comments

        except Exception as e:
            comments.append(f"Ошибка проверки согласованности данных со структурой json: {str(e)}")
            logger.error(f"Ошибка проверки согласованности данных со структурой json: {str(e)}")
            return False, comments

    def _validate_data_types(self, structure: Dict, data: List[Dict]) -> List[str]:
        """Базовая проверка типов данных."""
        errors = []
        column_types = {col["name"]: col["type"] for col in structure["columns"]}

        for i, record in enumerate(data):
            for col_name, value in record.items():
                if col_name in column_types:
                    type_error = self._validate_single_value(value, column_types[col_name])
                    if type_error:
                        errors.append(f"Запись {i}, колонка '{col_name}': {type_error}")
                        if len(errors) >= 3:
                            return errors

        return errors

    def _validate_single_value(self, value: Any, expected_type: str) -> Optional[str]:
        """Валидация одного значения для текущего формата экспорта типов."""
        if value is None:
            return None

        try:
            expected_lower = expected_type.lower()

            # 1. МАССИВЫ
            if expected_lower == "array":
                if not isinstance(value, list):
                    return f"ожидается массив, получен {type(value).__name__}"
                return None
            # 2. СТРОКОВЫЕ ТИПЫ
            if any(t in expected_lower for t in ["varchar", "character varying", "text", "char"]):
                if not isinstance(value, str):
                    return f"ожидается строка, получен {type(value).__name__}"
            # 3. ЦЕЛОЧИСЛЕННЫЕ
            elif any(t in expected_lower for t in ["integer", "int", "serial"]):
                if not isinstance(value, int):
                    return f"ожидается целое число, получен {type(value).__name__}"
            # 4. ДРОБНЫЕ ЧИСЛА
            elif any(t in expected_lower for t in ["numeric", "decimal", "real", "double", "float"]):
                if not isinstance(value, (int, float)):
                    return f"ожидается число, получен {type(value).__name__}"
            # 5. БУЛЕВЫ
            elif "boolean" in expected_lower or "bool" in expected_lower:
                if not isinstance(value, bool):
                    return f"ожидается булево значение, получен {type(value).__name__}"
            # 6. USER-DEFINED типы (enum и другие) - проверяем как строки
            elif "user-defined" in expected_lower or expected_lower in ["enum"]:
                if not isinstance(value, str):
                    return f"ожидается строковое значение, получен {type(value).__name__}"
            # 7. ДАТА/ВРЕМЯ (могут приходить как строки)
            elif any(t in expected_lower for t in ["date", "timestamp", "time"]):
                if not isinstance(value, str):
                    return f"ожидается строковое значение даты/времени, получен {type(value).__name__}"
            # 8. JSON (могут быть объекты или массивы)
            elif any(t in expected_lower for t in ["json", "jsonb"]):
                if not isinstance(value, (dict, list, str, int, float, bool)) and value is not None:
                    return f"ожидается JSON-совместимое значение, получен {type(value).__name__}"
            # 9. UUID
            elif "uuid" in expected_lower:
                if not isinstance(value, str):
                    return f"ожидается UUID строка, получен {type(value).__name__}"
            # 10. ДЛЯ НЕИЗВЕСТНЫХ ТИПОВ
            # Разрешаем основные JSON-совместимые типы
            elif not isinstance(value, (str, int, float, bool, list, dict)) and value is not None:
                return f"неподдерживаемый тип значения: {type(value).__name__} для типа {expected_type}"

            return None

        except Exception as e:
            return f"ошибка валидации типа: {str(e)}"

    def _check_structure_compatibility(self, source: Dict, target: Dict) -> Tuple[bool, List[str]]:
        """
        Строгая проверка совместимости структур с точным сравнением и полным сбором ошибок.

        Args:
            source: Структура из JSON (импортируемые данные)
            target: Структура из БД (целевая таблица)

        Returns:
            (успех, список комментариев)
        """
        comments = []
        all_issues = []

        try:
            source_columns = {col["name"]: col for col in source["columns"]}
            target_columns = {col["name"]: col for col in target["columns"]}

            # Сравнение набора колонок по именам
            source_column_names = set(source_columns.keys())
            target_column_names = set(target_columns.keys())
            logger.debug(f"Колонок в JSON: {len(source_column_names)}, в БД: {len(target_column_names)}")

            if source_column_names != target_column_names:
                missing_in_source = target_column_names - source_column_names
                extra_in_source = source_column_names - target_column_names

                if missing_in_source:
                    issue_msg = f"Отсутствуют колонки в JSON: {sorted(missing_in_source)}"
                    all_issues.append(issue_msg)
                    logger.debug(issue_msg)
                if extra_in_source:
                    issue_msg = f"Лишние колонки в JSON: {sorted(extra_in_source)}"
                    all_issues.append(issue_msg)
                    logger.debug(issue_msg)
            else:
                comments.append("Набор колонок совпадает")
                logger.debug("Набор колонок совпадает")

            # Сравнение параметров колонок (для общих колонок из пересечения множеств)
            common_columns = source_column_names & target_column_names
            column_params_ok = True
            for col_name in common_columns:
                source_col = source_columns[col_name]
                target_col = target_columns[col_name]

                # Сравнение типов (точное)
                if source_col["type"] != target_col["type"]:
                    issue_msg = (
                        f"Различие в TYPE для '{col_name}': JSON='{source_col['type']}', БД='{target_col['type']}'"  # noqa: E501
                    )
                    all_issues.append(issue_msg)
                    column_params_ok = False
                    logger.debug(issue_msg)

                # Сравнение NULLABLE (точное)
                if source_col.get("nullable") != target_col.get("nullable"):
                    source_nullable = "NULLABLE" if source_col.get("nullable", True) else "NOT NULL"
                    target_nullable = "NULLABLE" if target_col.get("nullable", True) else "NOT NULL"
                    issue_msg = f"Различие в NULLABLE для '{col_name}': JSON={source_nullable}, БД={target_nullable}"
                    all_issues.append(issue_msg)
                    column_params_ok = False
                    logger.debug(issue_msg)

                # Сравнение DEFAULT (с нормализацией по имени таблицы из базы даже если имя в json другое)
                source_default = self._normalize_default(source_col.get("default"), source["table"], target["table"])
                target_default = target_col.get("default")

                if source_default != target_default:
                    issue_msg = f"Различие в DEFAULT для '{col_name}': JSON='{source_default}', БД='{target_default}'"
                    all_issues.append(issue_msg)
                    column_params_ok = False
                    logger.debug(issue_msg)

            if column_params_ok and common_columns:
                comments.append("Все параметры колонок совпадают")

            # Сравнение ограничений (строгое)
            constraints_issues = self._compare_constraints_strict(
                source["constraints"], target["constraints"], source["table"], target["table"]
            )
            all_issues.extend(constraints_issues)

            if not constraints_issues and (source["constraints"] or target["constraints"]):
                comments.append(f"Ограничения совпадают: {len(source['constraints'])} шт.")
                logger.debug(f"Ограничения совпадают: {len(source['constraints'])} шт.")

            # Сравнение последовательностей
            sequences_issues = self._compare_sequences_strict(
                source["sequences"], target["sequences"], source["table"], target["table"]
            )
            all_issues.extend(sequences_issues)

            has_source_seqs = bool(source.get("sequences"))
            has_target_seqs = bool(target.get("sequences"))

            if not sequences_issues:
                if has_source_seqs and has_target_seqs:
                    comments.append(f"Последовательности совпадают: {len(source['sequences'])} шт.")
                    logger.debug(f"Последовательности совпадают: {len(source['sequences'])} шт.")
                elif not has_source_seqs and not has_target_seqs:
                    comments.append("Последовательностей нет в обоих источниках")
                    logger.debug("Последовательностей нет в обоих источниках")

            # Формируем итоговый результат
            if all_issues:
                comments.extend(all_issues)
                comments.append("Для импорта необходимо точное соответствие структур")
                logger.warning(f"Обнаружены различия в структурах: {len(all_issues)} issues")
                return False, comments

            comments.append("Структуры полностью идентичны")
            logger.debug("Структуры полностью идентичны")
            return True, comments

        except Exception as e:
            error_msg = f"Ошибка проверки совместимости структур: {str(e)}"
            comments.append(f"{error_msg}")
            logger.error(error_msg, exc_info=True)
            return False, comments

    def _normalize_default(
        self, default_value: Optional[str], source_table: str, target_table: str, schema_name: str = "classification"
    ) -> Optional[str]:
        """Нормализация DEFAULT значений в колонках(если это последовательность) по названию таблицы в базе."""
        if not default_value:
            logger.debug(f"DEFAULT значение пустое или None, возвращаем как есть: '{default_value}'")
            return default_value

        # Нормализация nextval для последовательностей
        # Пример: nextval('old_table_id_seq'::regclass) -> nextval('new_table_id_seq'::regclass)
        pattern = r"(nextval\(')([^']+)(\..+::regclass\))"

        if "nextval" in default_value:
            try:
                logger.debug(
                    f"Обнаружен nextval в DEFAULT значении последовательности, начинаем нормализацию: '{default_value}'"
                )
                normalized = re.sub(pattern, rf"\1{schema_name}\3", default_value)
                if source_table != target_table:
                    normalized = normalized.replace(source_table, target_table)
                    logger.debug(f"После замены таблицы '{source_table}' -> '{target_table}': '{normalized}'")
                else:
                    logger.debug("Имена таблиц совпадают, замена не требуется")

                return normalized

            except Exception as e:
                logger.warning(f"Ошибка нормализации DEFAULT '{default_value}': {e}")
                return default_value

        logger.debug(f"DEFAULT не содержит nextval, возвращаем без изменений: '{default_value}'")
        return default_value

    def _compare_constraints_strict(
        self, source_constraints: List[Dict], target_constraints: List[Dict], source_table: str, target_table: str
    ) -> List[str]:
        """Строгое сравнение ограничений."""
        issues = []

        logger.debug(f"Сравнение ограничений: JSON таблица='{source_table}' -> БД таблица='{target_table}'")
        logger.debug(f"Ограничений в JSON: {len(source_constraints)}, в БД: {len(target_constraints)}")

        def normalize_constraints(constraints, target_table_name, source_type: str):
            """Нормализуем ограничения, удаляя их constraint_name и учитывая имя таблицы в базе."""
            normalized = []

            for i, constr in enumerate(constraints):
                norm_constr = constr.copy()

                original_name = norm_constr.pop("constraint_name", None)
                logger.debug(f"[{i}] Удалено имя ограничения: '{original_name}'")

                if norm_constr["constraint_type"] in ["PRIMARY KEY", "UNIQUE"]:
                    old_foreign_table = norm_constr.get("foreign_table")
                    norm_constr["foreign_table"] = target_table_name
                    logger.debug(
                        f"[{i}] {norm_constr['constraint_type']}: foreign_table '{old_foreign_table}' -> '{target_table_name}'"  # noqa: E501
                    )

                elif norm_constr["constraint_type"] == "FOREIGN KEY":
                    foreign_table = norm_constr.get("foreign_table")
                    if foreign_table == source_table:  # self-reference
                        norm_constr["foreign_table"] = target_table_name
                        logger.debug(f"[{i}] FK self-reference: '{foreign_table}' -> '{target_table_name}'")
                    else:
                        logger.debug(f"[{i}] FK на внешнюю таблицу: '{foreign_table}' (оставляем как есть)")

                normalized.append(norm_constr)
                logger.debug(f"[{i}] Нормализованное ограничение: {norm_constr}")

            logger.debug(f"Нормализация {source_type} завершена: {len(normalized)} ограничений")
            return normalized

        source_norm = normalize_constraints(source_constraints, target_table, "JSON")
        target_norm = normalize_constraints(target_constraints, target_table, "БД")

        # Сравниваем через преобразование в словари
        def constraints_to_dict(constraints):
            dict_result = {}
            for c in constraints:
                # Для ограничений без колонки (например, CHECK) используем специальный ключ
                column_key = c.get("column", "NO_COLUMN")
                key = f"{c['constraint_type']}_{column_key}"
                dict_result[key] = c
            return dict_result

        source_dict = constraints_to_dict(source_norm)
        target_dict = constraints_to_dict(target_norm)

        logger.debug(f"Ключи ограничений JSON: {sorted(source_dict.keys())}")
        logger.debug(f"Ключи ограничений БД: {sorted(target_dict.keys())}")

        if source_dict != target_dict:
            logger.warning("Обнаружены различия в ограничениях")

            missing_in_source = set(target_dict.keys()) - set(source_dict.keys())
            extra_in_source = set(source_dict.keys()) - set(target_dict.keys())

            logger.debug(f"Отсутствует в JSON: {len(missing_in_source)} ограничений")
            logger.debug(f"Лишние в JSON: {len(extra_in_source)} ограничений")

            for key in missing_in_source:
                constr = target_dict[key]
                column = constr.get("column", "NO_COLUMN")
                issue_msg = f"Отсутствует ограничение в JSON: {constr['constraint_type']} для '{column}'"
                issues.append(issue_msg)
                logger.debug(issue_msg)

            for key in extra_in_source:
                constr = source_dict[key]
                column = constr.get("column", "NO_COLUMN")
                issue_msg = f"Лишнее ограничение в JSON: {constr['constraint_type']} для '{column}'"
                issues.append(issue_msg)
                logger.debug(issue_msg)
        else:
            logger.debug("Все ограничения совпадают")

        logger.debug(f"Сравнение ограничений завершено: найдено {len(issues)} проблем")
        return issues

    def _compare_sequences_strict(
        self, source_sequences: List[Dict], target_sequences: List[Dict], source_table: str, target_table: str
    ) -> List[str]:
        """Строгое сравнение последовательностей."""
        issues = []

        logger.debug(f"Сравнение последовательностей: JSON таблица='{source_table}' -> БД таблица='{target_table}'")

        def normalize_source_sequences(sequences, source_tbl, target_tbl):
            """Нормализация имен последовательностей в JSON."""
            normalized = []
            for seq in sequences:
                norm_seq = seq.copy()
                seq_name = norm_seq.get("name", "")

                if source_tbl in seq_name:
                    old_name = seq_name
                    norm_seq["name"] = seq_name.replace(source_tbl, target_tbl)
                    logger.debug(f"Нормализация: '{old_name}' -> '{norm_seq['name']}'")
                else:
                    logger.debug(f"Имя последовательности не требует нормализации: '{seq_name}'")

                normalized.append(norm_seq)
            return sorted(normalized, key=lambda x: x["name"])

        def normalize_target_sequences(sequences):
            """Последовательности из БД сортируем по имени."""
            return sorted(sequences or [], key=lambda x: x["name"])

        source_norm = normalize_source_sequences(source_sequences or [], source_table, target_table)
        target_norm = normalize_target_sequences(target_sequences)

        logger.debug(f"Последовательностей в JSON: {len(source_norm)}, в БД: {len(target_norm)}")

        if source_norm and not target_norm:
            issues.append("В JSON есть последовательности, а в БД отсутствуют")
            return issues

        if not source_norm and target_norm:
            issues.append(f"В JSON нет последовательностей, а в БД есть: {len(target_norm)} шт.")
            return issues

        if not source_norm and not target_norm:
            logger.debug("Последовательностей нет в обоих источниках")
            return issues

        if len(source_norm) != len(target_norm):
            issues.append(f"Разное количество последовательностей: JSON={len(source_norm)}, БД={len(target_norm)}")

        min_len = min(len(source_norm), len(target_norm))

        for index in range(min_len):
            source_seq = source_norm[index]
            target_seq = target_norm[index]

            logger.debug(
                f"Сравнение последовательности [{index}]: '{source_seq.get('name')}' vs '{target_seq.get('name')}'"
            )

            if source_seq.get("name") != target_seq.get("name"):
                issues.append(
                    f"Различие в имени последовательности: JSON='{source_seq.get('name')}', БД='{target_seq.get('name')}'"  # noqa: E501
                )

            params_to_check = ["data_type", "increment", "minvalue", "maxvalue", "start", "cycle"]

            for param in params_to_check:
                source_val = source_seq.get(param)
                target_val = target_seq.get(param)

                if source_val != target_val:
                    issues.append(
                        f"Различие в параметре '{param}' последовательности: JSON='{source_val}', БД='{target_val}'"
                    )

        logger.debug(f"Сравнение последовательностей завершено: найдено {len(issues)} проблем")
        return issues

    def _build_flk_response(
        self, receipt_data: Dict[str, Any], validated_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Формирует итоговый ответ ФЛК."""
        system_id = "unknown_system"
        protocol_version = 0.1
        note = "ФЛК классификатора"
        parent_msg_id = "5e399b36-b937-456c-9091-0ffc237f75b1"
        msg_type = "02"

        if validated_data:
            system_id = validated_data.get("system_id", "unknown_system")
            protocol_version = validated_data.get("protocol_version", 0.1)
            note = validated_data.get("note", "ФЛК классификатора")
            parent_msg_id = validated_data.get("message_id", "5e399b36-b937-456c-9091-0ffc237f75b1")
            msg_type = validated_data.get("msg_type", "02")

        receipt: FLKReceipt = {
            "protocol_version": protocol_version,
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),  # noqa: DTZ005
            "system_id": system_id,
            "note": note,
            "msg_type": msg_type,
            "payload": {
                "parent_msg_id": parent_msg_id,
                "read_check": receipt_data["read_check"],
                "schema_check": receipt_data["schema_check"],
                "data_and_structure_check": receipt_data["data_and_structure_check"],
                "structure_check": receipt_data["structure_check"],
                "proto_check": receipt_data["proto_check"],
                "flk_success": receipt_data["flk_success"],
                "timestamp": datetime.now().isoformat(),  # noqa: DTZ005
                "statistics": receipt_data["statistics"],
                "error_details": receipt_data["error_details"],
                "comments": receipt_data["comments"],
            },
        }

        response = {"receipt": receipt}

        if validated_data and receipt_data["flk_success"]:
            response["validated_data"] = validated_data

        logger.debug(f"ФЛК завершен: успех={receipt_data['flk_success']}, ошибка={receipt_data['error_details']}")
        return response
