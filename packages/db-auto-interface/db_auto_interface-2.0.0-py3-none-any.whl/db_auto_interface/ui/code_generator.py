"""
Генератор исходного кода интерфейса
Генерирует Python код созданного интерфейса на основе текущего состояния приложения
"""

import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
import inspect
import tkinter as tk
from tkinter import ttk


class InterfaceCodeGenerator:
    """Генератор кода интерфейса"""
    
    def __init__(self, app_instance: Any = None):
        """
        Инициализация генератора
        
        Args:
            app_instance: Экземпляр приложения DBAutoInterface
        """
        self.app = app_instance
        self.generated_code = []
        self.indent_level = 0
        self.indent_string = "    "  # 4 пробела
    
    def generate(self, include_comments: bool = True, 
                 include_docstrings: bool = True) -> str:
        """
        Генерирует полный Python код интерфейса
        
        Args:
            include_comments: Включать ли комментарии в код
            include_docstrings: Включать ли docstrings
            
        Returns:
            Строка с Python кодом
        """
        self.generated_code = []
        
        # Заголовок файла
        self._add_header(include_comments)
        
        # Импорты
        self._add_imports()
        
        # Класс главного окна
        self._add_main_window_class(include_docstrings)
        
        # Классы виджетов
        self._add_widget_classes(include_docstrings)
        
        # Главная функция
        self._add_main_function()
        
        return "\n".join(self.generated_code)
    
    def _add_header(self, include_comments: bool):
        """Добавляет заголовок файла"""
        if include_comments:
            self._add_line('"""')
            self._add_line('Сгенерированный код интерфейса DB Auto Interface')
            self._add_line('')
            self._add_line(f'Сгенерировано: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            self._add_line('Автоматически создано системой db_auto_interface')
            self._add_line('')
            self._add_line('ВНИМАНИЕ: Этот файл был автоматически сгенерирован.')
            self._add_line('Любые изменения могут быть перезаписаны при повторной генерации.')
            self._add_line('"""')
            self._add_line('')
            self._add_line('# -*- coding: utf-8 -*-')
            self._add_line('')
            self._add_line(f'# Generated at: {datetime.now().isoformat()}')
            self._add_line('')
    
    def _add_imports(self):
        """Добавляет импорты"""
        self._add_line('import tkinter as tk')
        self._add_line('from tkinter import ttk, messagebox')
        self._add_line('from typing import Optional, Dict, Any, List')
        self._add_line('')
        self._add_line('# Импорт библиотеки db_auto_interface')
        self._add_line('try:')
        self._indent()
        self._add_line('from db_auto_interface import UniversalDB, DBAutoInterface')
        self._dedent()
        self._add_line('except ImportError:')
        self._indent()
        self._add_line('print("Ошибка: библиотека db_auto_interface не установлена")')
        self._add_line('print("Установите: pip install db-auto-interface")')
        self._add_line('sys.exit(1)')
        self._add_line('')
    
    def _add_main_window_class(self, include_docstrings: bool):
        """Добавляет класс главного окна"""
        self._add_line('')
        self._add_line('')
        self._add_line('class GeneratedDBInterface(tk.Tk):')
        if include_docstrings:
            self._indent()
            self._add_line('"""')
            self._add_line('Сгенерированное главное окно приложения')
            self._add_line('Автоматически создано на основе текущего интерфейса')
            self._add_line('"""')
            self._dedent()
        
        # Метод __init__
        self._add_line('')
        self._indent()
        self._add_line('def __init__(self, connection_params: Dict[str, Any]):')
        if include_docstrings:
            self._indent()
            self._add_line('"""')
            self._add_line('Инициализация главного окна')
            self._add_line('')
            self._add_line('Args:')
            self._add_line('    connection_params: Параметры подключения к БД')
            self._add_line('"""')
            self._dedent()
        
        self._indent()
        self._add_line('super().__init__()')
        self._add_line('')
        
        # Параметры подключения
        if self.app and hasattr(self.app, 'db'):
            self._add_line('# Параметры подключения к БД')
            self._add_line('self.db = UniversalDB()')
            self._add_line('if not self.db.connect(connection_params):')
            self._indent()
            self._add_line('messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")')
            self._add_line('self.destroy()')
            self._add_line('return')
            self._dedent()
            self._add_line('')
        
        # Настройка окна
        self._add_line('# Настройка окна')
        if self.app:
            title = self.app.title() if hasattr(self.app, 'title') else "DB Auto Interface"
            geometry = self.app.geometry() if hasattr(self.app, 'geometry') else "1200x800"
            self._add_line(f'self.title("{title}")')
            self._add_line(f'self.geometry("{geometry}")')
        else:
            self._add_line('self.title("DB Auto Interface - Сгенерированный интерфейс")')
            self._add_line('self.geometry("1200x800")')
        self._add_line('self.minsize(800, 600)')
        self._add_line('')
        
        # Создание UI
        self._add_line('# Создание интерфейса')
        self._add_line('self.setup_ui()')
        self._add_line('')
        
        # Загрузка данных
        self._add_line('# Загрузка схемы БД')
        self._add_line('self.schema = None')
        self._add_line('self.navigation_map = None')
        self._add_line('self.current_table = None')
        self._add_line('self.load_schema()')
        
        self._dedent()
        
        # Метод setup_ui
        self._add_line('')
        self._add_line('    def setup_ui(self):')
        if include_docstrings:
            self._indent()
            self._add_line('"""Настройка интерфейса приложения"""')
            self._dedent()
        self._indent()
        self._add_line('# Основной контейнер')
        self._add_line('main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)')
        self._add_line('main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)')
        self._add_line('')
        self._add_line('# Левая панель с деревом таблиц')
        self._add_line('left_frame = ttk.Frame(main_container)')
        self._add_line('main_container.add(left_frame, weight=1)')
        self._add_line('')
        self._add_line('left_header = ttk.Label(left_frame, text="Таблицы", font=(\'Arial\', 10, \'bold\'))')
        self._add_line('left_header.pack(pady=5)')
        self._add_line('')
        self._add_line('# Правая панель с данными')
        self._add_line('right_frame = ttk.Frame(main_container)')
        self._add_line('main_container.add(right_frame, weight=3)')
        self._add_line('')
        self._add_line('self.table_container = ttk.Frame(right_frame)')
        self._add_line('self.table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)')
        self._add_line('')
        self._add_line('# Статус бар')
        self._add_line('self.status_bar = ttk.Label(self, text="Готово", relief=tk.SUNKEN)')
        self._add_line('self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)')
        self._dedent()
        
        # Метод load_schema
        self._add_line('')
        self._add_line('    def load_schema(self):')
        if include_docstrings:
            self._indent()
            self._add_line('"""Загружает схему базы данных"""')
            self._dedent()
        self._indent()
        self._add_line('try:')
        self._indent()
        self._add_line('self.status_bar.config(text="Загрузка схемы...")')
        self._add_line('self.schema = self.db.get_schema()')
        self._add_line('# TODO: Построить navigation_map при наличии модуля navigation')
        self._add_line('self.status_bar.config(text="Схема загружена")')
        self._dedent()
        self._add_line('except Exception as e:')
        self._indent()
        self._add_line('messagebox.showerror("Ошибка", f"Не удалось загрузить схему: {str(e)}")')
        self._add_line('self.status_bar.config(text="Ошибка загрузки схемы")')
        self._dedent()
        self._dedent()
        
        # Метод run
        self._add_line('')
        self._add_line('    def run(self):')
        if include_docstrings:
            self._indent()
            self._add_line('"""Запуск приложения"""')
            self._dedent()
        self._indent()
        self._add_line('try:')
        self._indent()
        self._add_line('self.mainloop()')
        self._dedent()
        self._add_line('finally:')
        self._indent()
        self._add_line('if hasattr(self, \'db\') and self.db:')
        self._indent()
        self._add_line('self.db.close()')
        self._dedent()
        self._dedent()
        self._dedent()
    
    def _add_widget_classes(self, include_docstrings: bool):
        """Добавляет классы виджетов (заглушки)"""
        self._add_line('')
        self._add_line('')
        self._add_line('# Дополнительные классы виджетов могут быть добавлены здесь')
        self._add_line('# при необходимости расширения функциональности')
    
    def _add_main_function(self):
        """Добавляет главную функцию"""
        self._add_line('')
        self._add_line('')
        self._add_line('def main():')
        self._indent()
        self._add_line('"""Главная функция запуска приложения"""')
        self._add_line('# Параметры подключения')
        self._add_line('connection_params = {')
        self._indent()
        self._add_line("'host': os.getenv('DB_HOST', 'localhost'),")
        self._add_line("'database': os.getenv('DB_NAME', 'test_db'),")
        self._add_line("'user': os.getenv('DB_USER', 'postgres'),")
        self._add_line("'password': os.getenv('DB_PASSWORD', 'password'),")
        self._add_line("'port': int(os.getenv('DB_PORT', '5432'))")
        self._dedent()
        self._add_line('}')
        self._add_line('')
        self._add_line('# Создание и запуск приложения')
        self._add_line('app = GeneratedDBInterface(connection_params)')
        self._add_line('app.run()')
        self._dedent()
        self._add_line('')
        self._add_line('')
        self._add_line("if __name__ == '__main__':")
        self._indent()
        self._add_line('import os')
        self._add_line('main()')
        self._dedent()
    
    def _add_line(self, line: str):
        """Добавляет строку кода с учетом отступа"""
        if line.strip():
            self.generated_code.append(self.indent_string * self.indent_level + line)
        else:
            self.generated_code.append("")
    
    def _indent(self):
        """Увеличивает уровень отступа"""
        self.indent_level += 1
    
    def _dedent(self):
        """Уменьшает уровень отступа"""
        if self.indent_level > 0:
            self.indent_level -= 1
    
    def generate_readme(self) -> str:
        """
        Генерирует README отчет о структуре интерфейса
        
        Returns:
            Строка с README форматом
        """
        lines = []
        lines.append("# Генерация кода интерфейса")
        lines.append("")
        lines.append(f"**Дата генерации:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("## Структура интерфейса")
        lines.append("")
        lines.append("### Главное окно")
        lines.append("")
        lines.append("- `GeneratedDBInterface` - основной класс приложения")
        lines.append("  - Наследуется от `tk.Tk`")
        lines.append("  - Управляет подключением к БД")
        lines.append("  - Создает основной интерфейс")
        lines.append("")
        lines.append("### Основные методы")
        lines.append("")
        lines.append("1. `__init__()` - инициализация окна и подключения")
        lines.append("2. `setup_ui()` - создание элементов интерфейса")
        lines.append("3. `load_schema()` - загрузка схемы БД")
        lines.append("4. `run()` - запуск приложения")
        lines.append("")
        lines.append("## Использование")
        lines.append("")
        lines.append("```python")
        lines.append("from generated_interface import GeneratedDBInterface")
        lines.append("")
        lines.append("app = GeneratedDBInterface({")
        lines.append("    'host': 'localhost',")
        lines.append("    'database': 'my_db',")
        lines.append("    'user': 'postgres',")
        lines.append("    'password': 'password'")
        lines.append("})")
        lines.append("app.run()")
        lines.append("```")
        lines.append("")
        lines.append("## Примечания")
        lines.append("")
        lines.append("- Код был автоматически сгенерирован")
        lines.append("- Для расширения функциональности рекомендуется наследование")
        lines.append("- Все изменения могут быть потеряны при повторной генерации")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_uml_diagram(self) -> str:
        """
        Генерирует текстовую UML-диаграмму структуры
        
        Returns:
            Строка с диаграммой в формате PlantUML/Mermaid
        """
        lines = []
        lines.append("@startuml")
        lines.append("class GeneratedDBInterface {")
        lines.append("  - db: UniversalDB")
        lines.append("  - schema: Dict")
        lines.append("  - navigation_map: Dict")
        lines.append("  - current_table: str")
        lines.append("  - table_container: Frame")
        lines.append("  - status_bar: Label")
        lines.append("  --")
        lines.append("  + __init__(connection_params)")
        lines.append("  + setup_ui()")
        lines.append("  + load_schema()")
        lines.append("  + run()")
        lines.append("}")
        lines.append("")
        lines.append("class UniversalDB {")
        lines.append("  + connect(params)")
        lines.append("  + get_schema()")
        lines.append("  + close()")
        lines.append("}")
        lines.append("")
        lines.append("GeneratedDBInterface --> UniversalDB : uses")
        lines.append("@enduml")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("```mermaid")
        lines.append("classDiagram")
        lines.append("    class GeneratedDBInterface {")
        lines.append("        +UniversalDB db")
        lines.append("        +Dict schema")
        lines.append("        +__init__(connection_params)")
        lines.append("        +setup_ui()")
        lines.append("        +load_schema()")
        lines.append("        +run()")
        lines.append("    }")
        lines.append("    class UniversalDB {")
        lines.append("        +connect(params)")
        lines.append("        +get_schema()")
        lines.append("        +close()")
        lines.append("    }")
        lines.append("    GeneratedDBInterface --> UniversalDB")
        lines.append("```")
        lines.append("")
        
        return "\n".join(lines)
    
    def save_to_file(self, filepath: str, include_comments: bool = True, 
                    include_docstrings: bool = True) -> bool:
        """
        Сохраняет сгенерированный код в файл
        
        Args:
            filepath: Путь к файлу для сохранения
            include_comments: Включать комментарии
            include_docstrings: Включать docstrings
            
        Returns:
            True если успешно сохранено
        """
        try:
            code = self.generate(include_comments, include_docstrings)
            
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', 
                       exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def generate_interface_code(output_file: str, app_instance: Any = None,
                           include_comments: bool = True,
                           include_docstrings: bool = True) -> bool:
    """
    Утилитная функция для генерации кода интерфейса
    
    Args:
        output_file: Путь к выходному файлу
        app_instance: Экземпляр приложения (опционально)
        include_comments: Включать комментарии
        include_docstrings: Включать docstrings
        
    Returns:
        True если успешно сгенерировано
    """
    generator = InterfaceCodeGenerator(app_instance)
    return generator.save_to_file(output_file, include_comments, include_docstrings)
