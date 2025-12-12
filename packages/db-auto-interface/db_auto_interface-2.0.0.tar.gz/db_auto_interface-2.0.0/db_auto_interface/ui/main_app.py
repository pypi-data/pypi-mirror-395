"""
Главное tkinter приложение для работы с базой данных
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
from ..core.universal_db import UniversalDB
from ..core.navigation import build_navigation_map
from .table_view import TableView
from .widgets import NavigationTree, StatusBar


class DBAutoInterface(tk.Tk):
    """Главное окно desktop приложения для работы с БД"""
    
    def __init__(self, db_connection: Optional[UniversalDB] = None, 
                 connection_params: Optional[Dict[str, Any]] = None):
        """
        Инициализация приложения
        
        Args:
            db_connection: Готовый объект UniversalDB (опционально)
            connection_params: Параметры подключения (если db_connection не передан)
        """
        super().__init__()
        
        # Инициализация подключения к БД
        if db_connection:
            self.db = db_connection
        elif connection_params:
            self.db = UniversalDB()
            if not self.db.connect(connection_params):
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
                self.destroy()
                return
        else:
            raise ValueError("Необходимо указать либо db_connection, либо connection_params")
        
        # Кэш схемы и навигации
        self.schema = None
        self.navigation_map = None
        self.current_table = None
        
        # Настройка окна
        self.title("DB Auto Interface - Универсальный интерфейс для работы с БД")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Настройка UI
        self.setup_ui()
        
        # Загрузка данных
        self.load_schema()
        
        # Привязка горячих клавиш
        self.bind('<Control-s>', lambda e: self.save_current())
        self.bind('<Control-f>', lambda e: self.focus_search())
        self.bind('<F5>', lambda e: self.refresh_current_table())
        self.bind('<Control-q>', lambda e: self.quit())
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Создание меню
        self.create_menu()
        
        # Основной контейнер
        main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель: дерево таблиц
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=1)
        
        # Заголовок левой панели
        left_header = ttk.Label(left_frame, text="Таблицы", font=('Arial', 10, 'bold'))
        left_header.pack(pady=5)
        
        # Дерево таблиц
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_tree = ttk.Scrollbar(tree_frame)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.table_tree = NavigationTree(tree_frame, self.on_table_select)
        self.table_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.config(command=self.table_tree.yview)
        self.table_tree.config(yscrollcommand=scrollbar_tree.set)
        
        # Правая панель: область данных таблицы
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=3)
        
        # Контейнер для таблицы
        self.table_container = ttk.Frame(right_frame)
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Статус бар
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Обновить схему", command=self.load_schema, accelerator="Ctrl+R")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit, accelerator="Ctrl+Q")
        
        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить таблицу", command=self.refresh_current_table, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_command(label="Показать точки входа", command=self.show_entry_points)
        view_menu.add_command(label="Показать навигацию", command=self.show_navigation)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        help_menu.add_command(label="Горячие клавиши", command=self.show_shortcuts)
    
    def load_schema(self):
        """Загружает схему базы данных"""
        try:
            self.status_bar.update_status("Загрузка схемы...")
            self.schema = self.db.get_schema()
            self.navigation_map = build_navigation_map(self.schema)
            
            # Обновляем дерево таблиц
            self.table_tree.load_tables(self.schema, self.navigation_map)
            
            self.status_bar.update_status("Схема загружена")
            
            if not self.schema:
                messagebox.showwarning("Предупреждение", "База данных пуста или не содержит таблиц")
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить схему: {str(e)}")
            self.status_bar.update_status("Ошибка загрузки схемы")
    
    def load_table_list(self):
        """Загружает список таблиц в дерево (устаревший метод, используйте load_schema)"""
        self.load_schema()
    
    def show_table_data(self, table_name: str):
        """Отображает данные таблицы"""
        try:
            self.status_bar.update_status(f"Загрузка данных таблицы {table_name}...")
            
            # Удаляем предыдущий виджет таблицы
            for widget in self.table_container.winfo_children():
                widget.destroy()
            
            # Создаем новый виджет таблицы
            table_view = TableView(self.table_container, self.db, table_name)
            table_view.pack(fill=tk.BOTH, expand=True)
            
            self.current_table = table_name
            self.status_bar.update_table_info(table_name)
            self.status_bar.update_status("Готово")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные таблицы: {str(e)}")
            self.status_bar.update_status("Ошибка загрузки данных")
    
    def on_table_select(self, table_name: str):
        """Обработчик выбора таблицы"""
        if table_name and table_name in self.schema:
            self.show_table_data(table_name)
    
    def refresh_current_table(self):
        """Обновляет текущую таблицу"""
        if self.current_table:
            self.show_table_data(self.current_table)
    
    def save_current(self):
        """Сохраняет текущие изменения (заглушка)"""
        self.status_bar.update_status("Сохранение...")
        # Реальная логика сохранения будет в TableView
    
    def focus_search(self):
        """Фокусирует поле поиска (заглушка)"""
        # Реальная логика будет в TableView
        pass
    
    def show_entry_points(self):
        """Показывает точки входа в БД"""
        if not self.navigation_map:
            messagebox.showinfo("Информация", "Схема не загружена")
            return
        
        entry_points = [table for table, info in self.navigation_map.items() 
                       if info.get("type") == "entry"]
        
        if entry_points:
            msg = "Точки входа в базу данных:\n\n" + "\n".join(f"• {table}" for table in entry_points)
            messagebox.showinfo("Точки входа", msg)
        else:
            messagebox.showinfo("Информация", "Точек входа не найдено (возможны циклические зависимости)")
    
    def show_navigation(self):
        """Показывает карту навигации"""
        if not self.navigation_map:
            messagebox.showinfo("Информация", "Схема не загружена")
            return
        
        nav_text = "Карта навигации:\n\n"
        for table, info in sorted(self.navigation_map.items()):
            nav_type = info.get("type", "bridge")
            depth = info.get("depth", -1)
            next_tables = info.get("next", [])
            
            nav_text += f"{table} ({nav_type}, глубина: {depth})\n"
            if next_tables:
                nav_text += "  → " + ", ".join(next_tables) + "\n"
            nav_text += "\n"
        
        # Создаем окно для отображения навигации
        nav_window = tk.Toplevel(self)
        nav_window.title("Карта навигации")
        nav_window.geometry("600x500")
        
        text_widget = tk.Text(nav_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', nav_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(nav_window, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
    
    def show_about(self):
        """Показывает информацию о программе"""
        about_text = """DB Auto Interface v1.0.0

Универсальный интерфейс для работы с базами данных PostgreSQL.

Возможности:
• Автоматический анализ схемы БД
• Навигация между связанными таблицами
• CRUD операции с данными
• Динамические формы редактирования
• Пагинация и поиск

Использует только стандартные библиотеки Python + psycopg2.
"""
        messagebox.showinfo("О программе", about_text)
    
    def show_shortcuts(self):
        """Показывает список горячих клавиш"""
        shortcuts_text = """Горячие клавиши:

Ctrl+S - Сохранить изменения
Ctrl+F - Поиск
F5 - Обновить таблицу
Ctrl+R - Обновить схему
Ctrl+Q - Выход
"""
        messagebox.showinfo("Горячие клавиши", shortcuts_text)
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.quit()
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            if hasattr(self, 'db') and self.db:
                self.db.close()
            self.destroy()
    
    def run(self):
        """Запуск приложения"""
        try:
            self.mainloop()
        finally:
            # Закрываем подключение при выходе
            if hasattr(self, 'db') and self.db:
                self.db.close()


def main():
    """
    Точка входа для консольной команды db-auto-interface
    """
    import sys
    
    # Параметры подключения из аргументов командной строки или переменных окружения
    import os
    
    connection_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'test_db'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': int(os.getenv('DB_PORT', '5432'))
    }
    
    # Парсинг аргументов командной строки (простой вариант)
    if len(sys.argv) > 1:
        print("Использование: db-auto-interface")
        print("\nИли установите переменные окружения:")
        print("  DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT")
        print("\nИли используйте в коде:")
        print("  from db_auto_interface import DBAutoInterface")
        print("  app = DBAutoInterface(connection_params={...})")
        print("  app.run()")
        sys.exit(1)
    
    try:
        app = DBAutoInterface(connection_params=connection_params)
        app.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

