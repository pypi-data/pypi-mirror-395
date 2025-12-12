"""
Универсальный анализатор схемы базы данных PostgreSQL
"""

import psycopg2
from typing import Dict, List, Optional, Any
from functools import lru_cache


def analyze_postgres_schema(connection) -> Dict[str, Any]:
    """
    Анализирует полную схему PostgreSQL базы данных
    
    Args:
        connection: psycopg2 connection объект
        
    Returns:
        Словарь со структурой БД в формате:
        {
            "table_name": {
                "columns": {
                    "column_name": {
                        "type": "string",
                        "primary_key": boolean,
                        "nullable": boolean,
                        "foreign_key": {"table": "...", "column": "..."} | null
                    }
                },
                "relationships": {
                    "referenced_by": [...],  # таблицы, которые ссылаются на эту
                    "references_to": [...]   # таблицы, на которые ссылается эта
                }
            }
        }
    """
    cursor = connection.cursor()
    schema = {}
    
    try:
        # Получаем все таблицы в схеме 'public'
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        # Инициализируем структуру для каждой таблицы
        for table in tables:
            schema[table] = {
                "columns": {},
                "relationships": {
                    "referenced_by": [],
                    "references_to": []
                }
            }
        
        # Получаем информацию о столбцах для каждой таблицы
        for table in tables:
            table_structure = get_table_structure(connection, table)
            schema[table]["columns"] = table_structure
        
        # Получаем все внешние ключи
        foreign_keys = find_foreign_keys(connection)
        
        # Заполняем информацию о внешних ключах и связях
        for fk_info in foreign_keys:
            table_name = fk_info["table_name"]
            column_name = fk_info["column_name"]
            ref_table = fk_info["referenced_table"]
            ref_column = fk_info["referenced_column"]
            
            if table_name in schema and column_name in schema[table_name]["columns"]:
                # Обновляем информацию о столбце
                schema[table_name]["columns"][column_name]["foreign_key"] = {
                    "table": ref_table,
                    "column": ref_column
                }
                
                # Обновляем связи
                if ref_table not in schema[table_name]["relationships"]["references_to"]:
                    schema[table_name]["relationships"]["references_to"].append(ref_table)
                
                if table_name not in schema[ref_table]["relationships"]["referenced_by"]:
                    schema[ref_table]["relationships"]["referenced_by"].append(table_name)
        
        # Валидация целостности ссылок
        _validate_references(schema)
        
    finally:
        cursor.close()
    
    return schema


def get_table_structure(connection, table_name: str) -> Dict[str, Any]:
    """
    Получает структуру конкретной таблицы
    
    Args:
        connection: psycopg2 connection объект
        table_name: Имя таблицы
        
    Returns:
        Словарь со структурой столбцов таблицы
    """
    cursor = connection.cursor()
    columns = {}
    
    try:
        # Получаем информацию о столбцах
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                udt_name,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        
        column_info = cursor.fetchall()
        
        # Получаем информацию о первичных ключах
        cursor.execute("""
            SELECT column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = 'public'
            AND tc.table_name = %s
            AND tc.constraint_type = 'PRIMARY KEY';
        """, (table_name,))
        
        primary_keys = {row[0] for row in cursor.fetchall()}
        
        # Формируем структуру столбцов
        for col_name, data_type, udt_name, max_length, is_nullable, default in column_info:
            columns[col_name] = {
                "type": _normalize_postgres_type(data_type, udt_name),
                "primary_key": col_name in primary_keys,
                "nullable": is_nullable == 'YES',
                "foreign_key": None,  # Будет заполнено позже
                "max_length": max_length,
                "default": default
            }
            
    finally:
        cursor.close()
    
    return columns


def find_foreign_keys(connection) -> List[Dict[str, str]]:
    """
    Находит все внешние ключи в базе данных
    
    Args:
        connection: psycopg2 connection объект
        
    Returns:
        Список словарей с информацией о внешних ключах:
        [
            {
                "table_name": "...",
                "column_name": "...",
                "referenced_table": "...",
                "referenced_column": "..."
            },
            ...
        ]
    """
    cursor = connection.cursor()
    foreign_keys = []
    
    try:
        cursor.execute("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM 
                information_schema.table_constraints AS tc
            JOIN 
                information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN 
                information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE 
                tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = 'public'
            ORDER BY tc.table_name, kcu.column_name;
        """)
        
        for table_name, column_name, ref_table, ref_column in cursor.fetchall():
            foreign_keys.append({
                "table_name": table_name,
                "column_name": column_name,
                "referenced_table": ref_table,
                "referenced_column": ref_column
            })
            
    finally:
        cursor.close()
    
    return foreign_keys


def _normalize_postgres_type(data_type: str, udt_name: str) -> str:
    """
    Нормализует типы данных PostgreSQL к стандартным названиям
    
    Args:
        data_type: Базовый тип данных
        udt_name: Имя пользовательского типа
        
    Returns:
        Нормализованное название типа
    """
    type_mapping = {
        'character varying': 'varchar',
        'character': 'char',
        'double precision': 'float',
        'timestamp without time zone': 'timestamp',
        'timestamp with time zone': 'timestamptz',
        'time without time zone': 'time',
        'time with time zone': 'timetz',
        'numeric': 'decimal',
        'boolean': 'bool',
        'integer': 'int',
        'bigint': 'bigint',
        'smallint': 'smallint',
        'text': 'text',
        'date': 'date',
        'uuid': 'uuid',
        'json': 'json',
        'jsonb': 'jsonb',
        'array': 'array'
    }
    
    # Проверяем базовый тип
    if data_type in type_mapping:
        return type_mapping[data_type]
    
    # Проверяем UDT имя
    if udt_name in type_mapping:
        return type_mapping[udt_name]
    
    # Возвращаем исходное значение, если не найдено
    return udt_name or data_type


def _validate_references(schema: Dict[str, Any]) -> None:
    """
    Валидирует целостность ссылок в схеме
    
    Args:
        schema: Схема базы данных
    """
    for table_name, table_info in schema.items():
        # Проверяем, что все ссылающиеся таблицы существуют
        for ref_table in table_info["relationships"]["references_to"]:
            if ref_table not in schema:
                raise ValueError(
                    f"Таблица '{table_name}' ссылается на несуществующую таблицу '{ref_table}'"
                )
        
        # Проверяем, что все ссылающиеся на эту таблицу существуют
        for ref_by_table in table_info["relationships"]["referenced_by"]:
            if ref_by_table not in schema:
                raise ValueError(
                    f"Таблица '{ref_by_table}' ссылается на '{table_name}', но не существует"
                )


# Кэширование для производительности
@lru_cache(maxsize=1)
def _get_cached_schema(connection_id: int) -> Optional[Dict[str, Any]]:
    """
    Кэшированная версия получения схемы (для внутреннего использования)
    """
    # Эта функция будет использоваться с модифицированным connection объектом
    # В реальной реализации нужно будет добавить механизм инвалидации кэша
    return None

