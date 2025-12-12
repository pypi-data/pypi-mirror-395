"""
Дополнительные виджеты для интерфейса
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, List, Tuple


class PaginationWidget(ttk.Frame):
    """Виджет пагинации для таблиц"""
    
    def __init__(self, parent, on_page_change: Callable[[int], None], 
                 on_page_size_change: Optional[Callable[[int], None]] = None):
        super().__init__(parent)
        self.on_page_change = on_page_change
        self.on_page_size_change = on_page_size_change
        
        self.current_page = 1
        self.total_pages = 1
        self.page_size = 50
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса виджета"""
        # Кнопка "Назад"
        self.btn_prev = ttk.Button(self, text="◀ Назад", command=self.prev_page)
        self.btn_prev.pack(side=tk.LEFT, padx=2)
        
        # Информация о странице
        self.page_label = ttk.Label(self, text="Страница 1 из 1")
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        # Поле ввода номера страницы
        self.page_entry = ttk.Entry(self, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=2)
        self.page_entry.bind('<Return>', self.go_to_page)
        
        # Кнопка "Вперед"
        self.btn_next = ttk.Button(self, text="Вперед ▶", command=self.next_page)
        self.btn_next.pack(side=tk.LEFT, padx=2)
        
        # Разделитель
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Выбор размера страницы
        ttk.Label(self, text="Записей на странице:").pack(side=tk.LEFT, padx=2)
        self.page_size_var = tk.StringVar(value="50")
        self.page_size_combo = ttk.Combobox(
            self, 
            textvariable=self.page_size_var,
            values=["10", "25", "50", "100"],
            width=5,
            state="readonly"
        )
        self.page_size_combo.pack(side=tk.LEFT, padx=2)
        self.page_size_combo.bind('<<ComboboxSelected>>', self.on_page_size_selected)
    
    def update_info(self, current_page: int, total_pages: int, total: int = 0):
        """Обновляет информацию о пагинации"""
        self.current_page = current_page
        self.total_pages = total_pages
        
        if total > 0:
            self.page_label.config(
                text=f"Страница {current_page} из {total_pages} (Всего: {total})"
            )
        else:
            self.page_label.config(text=f"Страница {current_page} из {total_pages}")
        
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, str(current_page))
        
        # Обновляем состояние кнопок
        self.btn_prev.config(state=tk.NORMAL if current_page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if current_page < total_pages else tk.DISABLED)
    
    def prev_page(self):
        """Переход на предыдущую страницу"""
        if self.current_page > 1:
            self.on_page_change(self.current_page - 1)
    
    def next_page(self):
        """Переход на следующую страницу"""
        if self.current_page < self.total_pages:
            self.on_page_change(self.current_page + 1)
    
    def go_to_page(self, event=None):
        """Переход на указанную страницу"""
        try:
            page = int(self.page_entry.get())
            if 1 <= page <= self.total_pages:
                self.on_page_change(page)
            else:
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, str(self.current_page))
        except ValueError:
            self.page_entry.delete(0, tk.END)
            self.page_entry.insert(0, str(self.current_page))
    
    def on_page_size_selected(self, event=None):
        """Обработка изменения размера страницы"""
        try:
            new_size = int(self.page_size_var.get())
            if new_size != self.page_size:
                self.page_size = new_size
                if self.on_page_size_change:
                    self.on_page_size_change(new_size)
        except ValueError:
            pass


class SearchWidget(ttk.Frame):
    """Виджет поиска и фильтрации"""
    
    def __init__(self, parent, on_search: Callable[[str], None], 
                 on_clear: Optional[Callable[[], None]] = None):
        super().__init__(parent)
        self.on_search = on_search
        self.on_clear = on_clear
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса виджета"""
        # Метка
        ttk.Label(self, text="Поиск:").pack(side=tk.LEFT, padx=5)
        
        # Поле поиска
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<KeyRelease>', self.on_search_changed)
        self.search_entry.bind('<Return>', self.on_search_enter)
        
        # Кнопка поиска
        self.btn_search = ttk.Button(self, text="Найти", command=self.do_search)
        self.btn_search.pack(side=tk.LEFT, padx=2)
        
        # Кнопка очистки
        self.btn_clear = ttk.Button(self, text="Очистить", command=self.clear_search)
        self.btn_clear.pack(side=tk.LEFT, padx=2)
    
    def on_search_changed(self, event=None):
        """Обработка изменения текста поиска"""
        # Можно добавить задержку для поиска в реальном времени
        pass
    
    def on_search_enter(self, event=None):
        """Обработка нажатия Enter в поле поиска"""
        self.do_search()
    
    def do_search(self):
        """Выполняет поиск"""
        search_text = self.search_var.get().strip()
        self.on_search(search_text)
    
    def clear_search(self):
        """Очищает поиск"""
        self.search_var.set("")
        if self.on_clear:
            self.on_clear()
        else:
            self.on_search("")


class NavigationTree(ttk.Treeview):
    """Дерево таблиц с группировкой по связям"""
    
    def __init__(self, parent, on_table_select: Callable[[str], None]):
        super().__init__(parent, show='tree')
        self.on_table_select = on_table_select
        
        # Настройка стилей
        self.heading('#0', text='Таблицы базы данных')
        
        # Привязка событий
        self.bind('<<TreeviewSelect>>', self.on_select)
        self.bind('<Double-Button-1>', self.on_double_click)
    
    def load_tables(self, schema: dict, navigation_map: Optional[dict] = None):
        """Загружает таблицы в дерево"""
        # Очищаем дерево
        for item in self.get_children():
            self.delete(item)
        
        # Группируем по типам
        entry_tables = []
        bridge_tables = []
        
        if navigation_map:
            for table_name, nav_info in navigation_map.items():
                if nav_info.get("type") == "entry":
                    entry_tables.append((table_name, nav_info.get("depth", 0)))
                else:
                    bridge_tables.append((table_name, nav_info.get("depth", 0)))
            
            # Сортируем по глубине
            entry_tables.sort(key=lambda x: (x[1], x[0]))
            bridge_tables.sort(key=lambda x: (x[1], x[0]))
        else:
            # Если нет navigation_map, просто добавляем все таблицы
            for table_name in schema.keys():
                entry_tables.append((table_name, 0))
        
        # Добавляем точки входа
        if entry_tables:
            entry_node = self.insert('', 'end', text='Точки входа', open=True)
            for table_name, depth in entry_tables:
                self.insert(entry_node, 'end', text=table_name, tags=('entry',))
        
        # Добавляем связующие таблицы
        if bridge_tables:
            bridge_node = self.insert('', 'end', text='Связующие таблицы', open=True)
            for table_name, depth in bridge_tables:
                self.insert(bridge_node, 'end', text=table_name, tags=('bridge',))
        
        # Настраиваем теги для разных типов
        self.tag_configure('entry', foreground='green')
        self.tag_configure('bridge', foreground='blue')
    
    def on_select(self, event):
        """Обработка выбора элемента"""
        selection = self.selection()
        if selection:
            item = selection[0]
            text = self.item(item, 'text')
            # Проверяем, что это не группа
            if text not in ['Точки входа', 'Связующие таблицы']:
                self.on_table_select(text)
    
    def on_double_click(self, event):
        """Обработка двойного клика"""
        self.on_select(event)


class StatusBar(ttk.Frame):
    """Строка состояния с информацией о текущей таблице"""
    
    def __init__(self, parent):
        super().__init__(parent, relief=tk.SUNKEN, borderwidth=1)
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса статус-бара"""
        # Информация о текущей таблице
        self.table_label = ttk.Label(self, text="Таблица: -")
        self.table_label.pack(side=tk.LEFT, padx=5)
        
        # Разделитель
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Количество записей
        self.records_label = ttk.Label(self, text="Записей: -")
        self.records_label.pack(side=tk.LEFT, padx=5)
        
        # Разделитель
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Статус операции
        self.status_label = ttk.Label(self, text="Готово")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Растягиваемый элемент
        ttk.Label(self, text="").pack(side=tk.RIGHT, padx=5)
    
    def update_table_info(self, table_name: str, record_count: int = 0):
        """Обновляет информацию о таблице"""
        self.table_label.config(text=f"Таблица: {table_name}")
        if record_count >= 0:
            self.records_label.config(text=f"Записей: {record_count}")
    
    def update_status(self, status: str):
        """Обновляет статус операции"""
        self.status_label.config(text=status)
    
    def clear(self):
        """Очищает статус-бар"""
        self.table_label.config(text="Таблица: -")
        self.records_label.config(text="Записей: -")
        self.status_label.config(text="Готово")

