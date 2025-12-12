"""
Виджет просмотра и редактирования табличных данных
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, List
from ..core.universal_db import UniversalDB
from .record_form import RecordForm
from .widgets import PaginationWidget, SearchWidget


class TableView(ttk.Frame):
    """Виджет для отображения и редактирования табличных данных"""
    
    def __init__(self, parent, db: UniversalDB, table_name: str):
        super().__init__(parent)
        self.db = db
        self.table_name = table_name
        self.current_page = 1
        self.page_size = 50
        self.current_order_by = None
        self.current_order_direction = "ASC"
        self.search_text = ""
        
        # Данные таблицы
        self.table_data = None
        self.columns = []
        
        # Словарь для хранения соответствия item -> record_id
        self.item_to_record_id = {}
        
        # Настройка UI
        self.setup_ui()
        
        # Загрузка данных
        self.load_data()
    
    def setup_ui(self):
        """Настройка интерфейса виджета"""
        # Заголовок таблицы
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=5)
        
        title_label = ttk.Label(header_frame, text=self.table_name, 
                               font=('Arial', 12, 'bold'))
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Панель инструментов
        self.setup_toolbar(header_frame)
        
        # Виджет поиска
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        self.setup_search(search_frame)
        
        # Таблица
        self.create_table_widget()
        
        # Пагинация
        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(fill=tk.X, padx=5, pady=5)
        self.setup_pagination(pagination_frame)
    
    def setup_toolbar(self, parent):
        """Создает панель инструментов"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(side=tk.RIGHT, padx=10)
        
        # Кнопка "Добавить"
        self.btn_add = ttk.Button(toolbar, text="➕ Добавить", command=self.add_record)
        self.btn_add.pack(side=tk.LEFT, padx=2)
        
        # Кнопка "Обновить"
        self.btn_refresh = ttk.Button(toolbar, text="🔄 Обновить", command=self.refresh_data)
        self.btn_refresh.pack(side=tk.LEFT, padx=2)
        
        # Кнопка "Удалить"
        self.btn_delete = ttk.Button(toolbar, text="🗑️ Удалить", command=self.delete_selected)
        self.btn_delete.pack(side=tk.LEFT, padx=2)
    
    def setup_search(self, parent):
        """Настраивает виджет поиска"""
        self.search_widget = SearchWidget(
            parent,
            on_search=self.on_search,
            on_clear=self.on_search_clear
        )
        self.search_widget.pack(fill=tk.X)
    
    def create_table_widget(self):
        """Создает виджет таблицы (ttk.Treeview)"""
        # Контейнер для таблицы с прокруткой
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вертикальная прокрутка
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Горизонтальная прокрутка
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Таблица
        self.table = ttk.Treeview(
            table_frame,
            columns=(),  # Будет заполнено при загрузке данных
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scrollbar.config(command=self.table.yview)
        h_scrollbar.config(command=self.table.xview)
        
        # Привязка событий
        self.table.bind('<Double-Button-1>', self.on_double_click)
        self.table.bind('<Button-3>', self.show_context_menu)  # Правый клик
        self.table.bind('<Button-1>', self.on_click)
        
        # Контекстное меню
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Редактировать", command=self.edit_selected)
        self.context_menu.add_command(label="Удалить", command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Копировать значение", command=self.copy_value)
    
    def setup_pagination(self, parent):
        """Настраивает пагинацию"""
        self.pagination_widget = PaginationWidget(
            parent,
            on_page_change=self.on_page_change,
            on_page_size_change=self.on_page_size_change
        )
        self.pagination_widget.pack(fill=tk.X)
    
    def load_data(self):
        """Загружает данные из БД с пагинацией"""
        try:
            # Показываем индикатор загрузки
            self.show_loading_indicator()
            
            # Получаем данные
            result = self.db.get_table_data(
                self.table_name,
                page=self.current_page,
                page_size=self.page_size,
                order_by=self.current_order_by,
                order_direction=self.current_order_direction
            )
            
            self.table_data = result["data"]
            self.columns = result["columns"]
            total = result["total"]
            total_pages = result["total_pages"]
            
            # Обновляем таблицу
            self.update_table_display()
            
            # Обновляем пагинацию
            self.pagination_widget.update_info(self.current_page, total_pages, total)
            
            # Скрываем индикатор загрузки
            self.hide_loading_indicator()
            
        except Exception as e:
            self.hide_loading_indicator()
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def update_table_display(self):
        """Обновляет отображение таблицы"""
        # Очищаем таблицу
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Очищаем словарь соответствий
        self.item_to_record_id.clear()
        
        # Настраиваем столбцы
        self.table.config(columns=self.columns)
        
        # Скрываем колонку дерева (#0), так как мы используем только колонки данных
        self.table.column('#0', width=0, stretch=False)
        
        # Настраиваем заголовки
        for col in self.columns:
            self.table.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            # Автоматическая ширина столбца
            self.table.column(col, width=150, minwidth=100)
        
        # Заполняем данными
        for row_data in self.table_data:
            values = [str(row_data.get(col, "")) for col in self.columns]
            item = self.table.insert('', tk.END, values=values)
            
            # Сохраняем ID записи в словаре для быстрого доступа
            pk_column = self.columns[0]  # Предполагаем, что первый столбец - это PK
            record_id = row_data.get(pk_column)
            if record_id is not None:
                # Сохраняем ID в словаре (не используем #0, так как это зарезервированная колонка)
                self.item_to_record_id[item] = record_id
                # Также сохраняем в тегах элемента для удобства
                self.table.item(item, tags=(f"record_{record_id}",))
    
    def refresh_data(self):
        """Обновляет данные таблицы"""
        self.load_data()
    
    def add_record(self):
        """Открывает форму добавления записи"""
        form = RecordForm(self, self.db, self.table_name)
        form.wait_window()  # Ждем закрытия формы
        self.refresh_data()  # Обновляем данные после закрытия
    
    def edit_record(self, record_id: Any):
        """Открывает форму редактирования записи"""
        form = RecordForm(self, self.db, self.table_name, record_id=record_id)
        form.wait_window()  # Ждем закрытия формы
        self.refresh_data()  # Обновляем данные после закрытия
    
    def delete_record(self, record_id: Any):
        """Удаляет запись с подтверждением"""
        result = messagebox.askyesno(
            "Подтверждение",
            f"Вы уверены, что хотите удалить запись с ID {record_id}?",
            icon='warning'
        )
        
        if result:
            try:
                self.db.delete_record(self.table_name, record_id)
                messagebox.showinfo("Успех", "Запись успешно удалена")
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")
    
    def delete_selected(self):
        """Удаляет выбранную запись"""
        selection = self.table.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        
        item = selection[0]
        # Получаем ID из словаря или из первого столбца
        record_id = self.item_to_record_id.get(item)
        if record_id is None:
            # Fallback: получаем из первого столбца
            values = self.table.item(item, 'values')
            if values:
                record_id = values[0]
        
        if record_id:
            self.delete_record(record_id)
    
    def edit_selected(self):
        """Редактирует выбранную запись"""
        selection = self.table.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования")
            return
        
        item = selection[0]
        # Получаем ID из словаря или из первого столбца
        record_id = self.item_to_record_id.get(item)
        if record_id is None:
            # Fallback: получаем из первого столбца
            values = self.table.item(item, 'values')
            if values:
                record_id = values[0]
        
        if record_id:
            self.edit_record(record_id)
    
    def on_click(self, event):
        """Обработчик клика по таблице"""
        # Можно добавить логику выделения строки
        pass
    
    def on_double_click(self, event):
        """Обработчик двойного клика - открывает форму редактирования"""
        self.edit_selected()
    
    def show_context_menu(self, event):
        """Показывает контекстное меню"""
        # Выбираем элемент под курсором
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_value(self):
        """Копирует значение выбранной ячейки"""
        selection = self.table.selection()
        if not selection:
            return
        
        item = selection[0]
        # Получаем координаты клика для определения колонки
        try:
            x = self.table.winfo_pointerx() - self.table.winfo_rootx()
            column = self.table.identify_column(x)
        except:
            return
        
        if column:
            # Колонка #0 - это дерево, колонки данных начинаются с #1
            # Но в нашем случае мы используем только колонки данных
            try:
                col_index = int(column.replace('#', '')) - 1
                # Если это колонка #0 (дерево), пропускаем
                if col_index < 0:
                    return
                if 0 <= col_index < len(self.columns):
                    values = self.table.item(item, 'values')
                    if values and col_index < len(values):
                        self.clipboard_clear()
                        self.clipboard_append(str(values[col_index]))
            except (ValueError, IndexError):
                pass
    
    def sort_by_column(self, column: str):
        """Сортирует таблицу по указанному столбцу"""
        if self.current_order_by == column:
            # Переключаем направление сортировки
            self.current_order_direction = "DESC" if self.current_order_direction == "ASC" else "ASC"
        else:
            self.current_order_by = column
            self.current_order_direction = "ASC"
        
        self.load_data()
    
    def on_page_change(self, page: int):
        """Обработчик изменения страницы"""
        self.current_page = page
        self.load_data()
    
    def on_page_size_change(self, page_size: int):
        """Обработчик изменения размера страницы"""
        self.page_size = page_size
        self.current_page = 1  # Сбрасываем на первую страницу
        self.load_data()
    
    def on_search(self, search_text: str):
        """Обработчик поиска"""
        self.search_text = search_text
        # TODO: Реализовать фильтрацию данных
        # Пока просто обновляем таблицу
        self.current_page = 1
        self.load_data()
    
    def on_search_clear(self):
        """Обработчик очистки поиска"""
        self.search_text = ""
        self.current_page = 1
        self.load_data()
    
    def show_loading_indicator(self):
        """Показывает индикатор загрузки"""
        # Простая реализация - можно улучшить
        self.config(cursor="watch")
        self.update()
    
    def hide_loading_indicator(self):
        """Скрывает индикатор загрузки"""
        self.config(cursor="")

