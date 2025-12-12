"""
Система навигации между таблицами базы данных
"""

from typing import Dict, List, Any, Set, Tuple
from collections import deque


def find_entry_points(schema: Dict[str, Any]) -> List[str]:
    """
    Находит таблицы без входящих ссылок (точки входа)
    
    Алгоритм: таблицы, которые НЕ упоминаются в foreign_key других таблиц
    
    Args:
        schema: Схема базы данных
    
    Returns:
        Список имен таблиц, которые являются точками входа
    """
    entry_points = []
    
    # Собираем все таблицы, на которые есть ссылки
    referenced_tables = set()
    for table_name, table_info in schema.items():
        for ref_table in table_info["relationships"]["references_to"]:
            referenced_tables.add(ref_table)
    
    # Точки входа - это таблицы, на которые никто не ссылается
    for table_name in schema.keys():
        if table_name not in referenced_tables:
            entry_points.append(table_name)
    
    # Если все таблицы связаны (циклические зависимости),
    # выбираем таблицы с наименьшим количеством входящих ссылок
    if not entry_points:
        min_references = float('inf')
        for table_name, table_info in schema.items():
            ref_count = len(table_info["relationships"]["referenced_by"])
            if ref_count < min_references:
                min_references = ref_count
                entry_points = [table_name]
            elif ref_count == min_references:
                entry_points.append(table_name)
    
    return entry_points


def build_navigation_map(schema: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Строит карту переходов между таблицами используя BFS от точек входа
    
    Args:
        schema: Схема базы данных
    
    Returns:
        Словарь с информацией о навигации:
        {
            "table_name": {
                "type": "entry|bridge",  # тип таблицы
                "next": [...],  # список таблиц, на которые можно перейти
                "depth": int  # глубина в дереве навигации
            },
            ...
        }
    """
    entry_points = find_entry_points(schema)
    navigation_map = {}
    visited = set()
    queue = deque()
    
    # Инициализируем все таблицы
    for table_name in schema.keys():
        navigation_map[table_name] = {
            "type": "bridge",
            "next": [],
            "depth": -1  # -1 означает, что еще не обработана
        }
    
    # Помечаем точки входа
    for entry_point in entry_points:
        navigation_map[entry_point]["type"] = "entry"
        navigation_map[entry_point]["depth"] = 0
        queue.append((entry_point, 0))
        visited.add(entry_point)
    
    # BFS обход
    while queue:
        current_table, depth = queue.popleft()
        
        # Находим все таблицы, которые ссылаются на текущую
        # (это таблицы, на которые можно перейти из текущей)
        for table_name, table_info in schema.items():
            if current_table in table_info["relationships"]["references_to"]:
                if table_name not in visited:
                    visited.add(table_name)
                    navigation_map[current_table]["next"].append(table_name)
                    navigation_map[table_name]["depth"] = depth + 1
                    queue.append((table_name, depth + 1))
                elif table_name in navigation_map[current_table]["next"]:
                    # Уже добавлена, пропускаем
                    pass
                else:
                    # Таблица уже обработана, но добавляем связь
                    navigation_map[current_table]["next"].append(table_name)
    
    # Обрабатываем самоссылающиеся таблицы
    for table_name, table_info in schema.items():
        if table_name in table_info["relationships"]["references_to"]:
            # Таблица ссылается сама на себя
            if table_name not in navigation_map[table_name]["next"]:
                navigation_map[table_name]["next"].append(table_name)
    
    return navigation_map


def generate_filling_sequence(navigation_map: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Генерирует последовательность заполнения таблиц
    
    Args:
        navigation_map: Карта навигации между таблицами
    
    Returns:
        Список словарей с информацией о шагах:
        [
            {
                "step": 1,
                "table": "users",
                "action": "create",
                "depends_on": []
            },
            ...
        ]
    """
    sequence = []
    step = 1
    
    # Сортируем таблицы по глубине
    sorted_tables = sorted(
        navigation_map.items(),
        key=lambda x: (x[1]["depth"], x[0])
    )
    
    for table_name, nav_info in sorted_tables:
        # Определяем зависимости
        depends_on = []
        
        # Находим таблицы, на которые ссылается текущая
        # (нужно заполнить их раньше)
        # Это нужно получать из схемы, но для упрощения используем navigation_map
        # В реальности нужно проверять foreign keys
        
        sequence.append({
            "step": step,
            "table": table_name,
            "action": "create",
            "depends_on": depends_on,
            "depth": nav_info["depth"],
            "type": nav_info["type"]
        })
        step += 1
    
    return sequence


def detect_cycles(schema: Dict[str, Any]) -> List[List[str]]:
    """
    Обнаруживает циклические зависимости между таблицами
    
    Args:
        schema: Схема базы данных
    
    Returns:
        Список циклов, каждый цикл - это список имен таблиц
    """
    cycles = []
    visited = set()
    rec_stack = set()
    path = []
    
    def dfs(table_name: str, parent: str = None) -> bool:
        """Поиск циклов с помощью DFS"""
        visited.add(table_name)
        rec_stack.add(table_name)
        path.append(table_name)
        
        # Проверяем все таблицы, на которые ссылается текущая
        if table_name in schema:
            ref_tables = schema[table_name]["relationships"]["references_to"]
            
            for ref_table in ref_tables:
                if ref_table not in visited:
                    if dfs(ref_table, table_name):
                        return True
                elif ref_table in rec_stack:
                    # Найден цикл
                    cycle_start = path.index(ref_table)
                    cycle = path[cycle_start:] + [ref_table]
                    cycles.append(cycle.copy())
                    return True
        
        rec_stack.remove(table_name)
        path.pop()
        return False
    
    # Проверяем все таблицы
    for table_name in schema.keys():
        if table_name not in visited:
            dfs(table_name)
    
    # Удаляем дубликаты циклов
    unique_cycles = []
    for cycle in cycles:
        # Нормализуем цикл (начинаем с минимального элемента)
        min_idx = cycle.index(min(cycle))
        normalized = cycle[min_idx:] + cycle[:min_idx]
        if normalized not in unique_cycles:
            unique_cycles.append(normalized)
    
    return unique_cycles


def get_table_dependencies(schema: Dict[str, Any], table_name: str) -> List[str]:
    """
    Получает список таблиц, от которых зависит указанная таблица
    
    Args:
        schema: Схема базы данных
        table_name: Имя таблицы
    
    Returns:
        Список имен таблиц, от которых зависит указанная таблица
    """
    if table_name not in schema:
        return []
    
    return schema[table_name]["relationships"]["references_to"].copy()


def get_referencing_tables(schema: Dict[str, Any], table_name: str) -> List[str]:
    """
    Получает список таблиц, которые ссылаются на указанную таблицу
    
    Args:
        schema: Схема базы данных
        table_name: Имя таблицы
    
    Returns:
        Список имен таблиц, которые ссылаются на указанную таблицу
    """
    if table_name not in schema:
        return []
    
    return schema[table_name]["relationships"]["referenced_by"].copy()

