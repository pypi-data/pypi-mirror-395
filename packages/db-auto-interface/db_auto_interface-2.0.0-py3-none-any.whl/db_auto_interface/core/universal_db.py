"""
Универсальный класс для работы с базой данных
"""

import psycopg2
from typing import Dict, List, Optional, Any, Tuple
from .db_schema import analyze_postgres_schema, get_table_structure


class UniversalDB:
    """
    Универсальный класс для работы с базой данных PostgreSQL
    """
    
    def __init__(self, db_type: str = "postgresql", connection_string: Optional[str] = None):
        """
        Инициализация класса
        
        Args:
            db_type: Тип базы данных (пока поддерживается только postgresql)
            connection_string: Строка подключения (опционально)
        """
        self.db_type = db_type
        self.connection_string = connection_string
        self.conn = None
        self._schema_cache = None
        self._primary_keys_cache = {}
    
    def connect(self, connection_params: Dict[str, Any]) -> bool:
        """
        Универсальное подключение к базе данных
        
        Args:
            connection_params: Словарь с параметрами подключения:
                - host: адрес сервера
                - database: имя базы данных
                - user: имя пользователя
                - password: пароль
                - port: порт (опционально, по умолчанию 5432)
        
        Returns:
            True если подключение успешно, False в противном случае
        """
        try:
            if self.db_type == "postgresql":
                port = connection_params.get('port', 5432)
                self.conn = psycopg2.connect(
                    host=connection_params.get('host', 'localhost'),
                    database=connection_params.get('database'),
                    user=connection_params.get('user'),
                    password=connection_params.get('password'),
                    port=port
                )
                self.conn.autocommit = False  # Используем транзакции
                return True
            else:
                raise ValueError(f"Неподдерживаемый тип БД: {self.db_type}")
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            return False
    
    def get_schema(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Получает полную схему базы данных через db_schema.py
        
        Args:
            force_refresh: Принудительно обновить кэш схемы
        
        Returns:
            Словарь со схемой БД
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        # Используем кэш, если схема уже была получена
        if self._schema_cache is None or force_refresh:
            self._schema_cache = analyze_postgres_schema(self.conn)
            # Очищаем кэш первичных ключей при обновлении схемы
            self._primary_keys_cache = {}
        
        return self._schema_cache
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Any:
        """
        Выполняет SQL запрос с параметрами
        
        Args:
            query: SQL запрос
            params: Параметры для запроса (кортеж)
        
        Returns:
            Для SELECT запросов - список кортежей с результатами
            Для других запросов - True при успехе, False при ошибке
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                # Для SELECT запросов возвращаем результат
                if cursor.description:
                    result = cursor.fetchall()
                    return result
                
                # Для других запросов коммитим транзакцию
                self.conn.commit()
                return True
                
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка выполнения запроса: {e}")
            raise
    
    def get_table_data(self, table_name: str, page: int = 1, page_size: int = 50, 
                      order_by: Optional[str] = None, order_direction: str = "ASC") -> Dict[str, Any]:
        """
        Получает данные таблицы с пагинацией
        
        Args:
            table_name: Имя таблицы
            page: Номер страницы (начиная с 1)
            page_size: Размер страницы
            order_by: Столбец для сортировки (опционально)
            order_direction: Направление сортировки (ASC/DESC)
        
        Returns:
            Словарь с данными:
            {
                "data": [...],  # список словарей с записями
                "columns": [...],  # список названий столбцов
                "total": int,  # общее количество записей
                "page": int,  # текущая страница
                "page_size": int,  # размер страницы
                "total_pages": int  # общее количество страниц
            }
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        try:
            cursor = self.conn.cursor()
            
            # Получаем общее количество записей
            count_query = f'SELECT COUNT(*) FROM "{table_name}"'
            cursor.execute(count_query)
            total = cursor.fetchone()[0]
            
            # Формируем запрос с пагинацией
            offset = (page - 1) * page_size
            query = f'SELECT * FROM "{table_name}"'
            
            if order_by:
                query += f' ORDER BY "{order_by}" {order_direction}'
            
            query += f' LIMIT {page_size} OFFSET {offset}'
            
            cursor.execute(query)
            
            # Получаем названия столбцов
            columns = [desc[0] for desc in cursor.description]
            
            # Получаем данные
            rows = cursor.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
            
            cursor.close()
            
            total_pages = (total + page_size - 1) // page_size if total > 0 else 1
            
            return {
                "data": data,
                "columns": columns,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
            
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Ошибка получения данных таблицы: {e}")
    
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        Вставляет новую запись в таблицу
        
        Args:
            table_name: Имя таблицы
            data: Словарь с данными {column_name: value}
        
        Returns:
            True при успехе, False при ошибке
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        if not data:
            raise ValueError("Данные для вставки не могут быть пустыми")
        
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ", ".join(["%s"] * len(values))
            columns_str = ", ".join([f'"{col}"' for col in columns])
            
            query = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'
            
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                self.conn.commit()
                
                # Инвалидируем кэш схемы при изменении данных
                self._schema_cache = None
                
                return True
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Ошибка вставки записи: {e}")
    
    def update_record(self, table_name: str, record_id: Any, data: Dict[str, Any]) -> bool:
        """
        Обновляет запись в таблице
        
        Args:
            table_name: Имя таблицы
            record_id: Значение первичного ключа записи
            data: Словарь с данными для обновления {column_name: value}
        
        Returns:
            True при успехе, False при ошибке
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        if not data:
            raise ValueError("Данные для обновления не могут быть пустыми")
        
        try:
            # Автоматически определяем первичный ключ
            primary_key = self._get_primary_key(table_name)
            if not primary_key:
                raise ValueError(f"Не удалось определить первичный ключ для таблицы {table_name}")
            
            # Формируем SET часть запроса
            set_parts = [f'"{col}" = %s' for col in data.keys()]
            set_clause = ", ".join(set_parts)
            values = list(data.values())
            values.append(record_id)
            
            query = f'UPDATE "{table_name}" SET {set_clause} WHERE "{primary_key}" = %s'
            
            with self.conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                self.conn.commit()
                
                # Инвалидируем кэш схемы при изменении данных
                self._schema_cache = None
                
                return True
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Ошибка обновления записи: {e}")
    
    def delete_record(self, table_name: str, record_id: Any) -> bool:
        """
        Удаляет запись из таблицы
        
        Args:
            table_name: Имя таблицы
            record_id: Значение первичного ключа записи
        
        Returns:
            True при успехе, False при ошибке
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        try:
            # Автоматически определяем первичный ключ
            primary_key = self._get_primary_key(table_name)
            if not primary_key:
                raise ValueError(f"Не удалось определить первичный ключ для таблицы {table_name}")
            
            query = f'DELETE FROM "{table_name}" WHERE "{primary_key}" = %s'
            
            with self.conn.cursor() as cursor:
                cursor.execute(query, (record_id,))
                self.conn.commit()
                
                # Инвалидируем кэш схемы при изменении данных
                self._schema_cache = None
                
                return True
                
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Ошибка удаления записи: {e}")
    
    def get_foreign_key_options(self, fk_table: str, fk_column: str) -> List[Tuple[Any, str]]:
        """
        Получает значения для комбобоксов внешних ключей
        
        Args:
            fk_table: Таблица, на которую ссылается внешний ключ
            fk_column: Столбец, на который ссылается внешний ключ
        
        Returns:
            Список кортежей (value, display_text) для комбобокса
        """
        if not self.conn:
            raise ConnectionError("Нет подключения к базе данных")
        
        try:
            # Получаем первичный ключ целевой таблицы
            pk_column = self._get_primary_key(fk_table)
            if not pk_column:
                # Если нет PK, используем указанный столбец
                pk_column = fk_column
            
            # Получаем все записи из целевой таблицы
            # Пытаемся найти текстовое поле для отображения
            schema = self.get_schema()
            if fk_table in schema:
                columns = schema[fk_table]["columns"]
                # Ищем текстовое поле (name, title, description и т.д.)
                display_column = None
                for col_name in columns:
                    if col_name.lower() in ['name', 'title', 'название', 'имя', 'описание', 'description']:
                        display_column = col_name
                        break
                
                if display_column:
                    query = f'SELECT "{pk_column}", "{display_column}" FROM "{fk_table}" ORDER BY "{display_column}"'
                else:
                    # Если не нашли текстовое поле, используем PK
                    query = f'SELECT "{pk_column}" FROM "{fk_table}" ORDER BY "{pk_column}"'
                    display_column = pk_column
            else:
                query = f'SELECT "{pk_column}" FROM "{fk_table}" ORDER BY "{pk_column}"'
                display_column = pk_column
            
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            # Формируем список опций
            if not results:
                # Если нет записей, возвращаем пустой список
                print(f"[WARNING] Нет записей в таблице {fk_table} для внешнего ключа")
                return []
            
            # Проверяем количество столбцов в результате
            num_columns = len(results[0]) if results else 0
            if num_columns > 1:
                # Есть отдельное поле для отображения
                return [(row[0], str(row[1])) for row in results]
            else:
                # Используем PK как значение и отображение
                return [(row[0], str(row[0])) for row in results]
                
        except Exception as e:
            import traceback
            print(f"[ERROR] Ошибка получения опций внешнего ключа {fk_table}.{fk_column}: {e}")
            traceback.print_exc()
            raise Exception(f"Ошибка получения опций внешнего ключа: {e}")
    
    def _get_primary_key(self, table_name: str) -> Optional[str]:
        """
        Автоматически определяет первичный ключ таблицы
        
        Args:
            table_name: Имя таблицы
        
        Returns:
            Имя столбца первичного ключа или None
        """
        # Используем кэш
        if table_name in self._primary_keys_cache:
            return self._primary_keys_cache[table_name]
        
        try:
            schema = self.get_schema()
            if table_name in schema:
                columns = schema[table_name]["columns"]
                for col_name, col_info in columns.items():
                    if col_info.get("primary_key", False):
                        self._primary_keys_cache[table_name] = col_name
                        return col_name
            
            # Если не нашли в схеме, запрашиваем напрямую
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_schema = 'public'
                AND tc.table_name = %s
                AND tc.constraint_type = 'PRIMARY KEY'
                LIMIT 1;
            """, (table_name,))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                pk = result[0]
                self._primary_keys_cache[table_name] = pk
                return pk
            
            return None
            
        except Exception as e:
            print(f"Ошибка определения первичного ключа: {e}")
            return None
    
    def close(self) -> None:
        """Закрывает подключение к базе данных"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self._schema_cache = None
            self._primary_keys_cache = {}

