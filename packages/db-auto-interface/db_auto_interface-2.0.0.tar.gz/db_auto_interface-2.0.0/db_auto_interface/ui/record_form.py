"""
Динамические формы редактирования записей
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, List
from ..core.universal_db import UniversalDB
import traceback


class RecordForm(tk.Toplevel):
    """Окно формы для добавления/редактирования записи"""
    
    def __init__(self, parent, db: UniversalDB, table_name: str, record_id: Optional[Any] = None):
        """
        Инициализация формы
        
        Args:
            parent: Родительское окно
            db: Объект UniversalDB
            table_name: Имя таблицы
            record_id: ID записи для редактирования (None для новой записи)
        """
        super().__init__(parent)
        
        self.db = db
        self.table_name = table_name
        self.record_id = record_id
        self.is_edit_mode = record_id is not None
        
        # Схема таблицы
        self.schema = None
        self.table_structure = None
        
        # Поля формы
        self.form_fields = {}
        self.form_widgets = {}
        
        # Настройка окна
        title = f"Редактирование: {table_name}" if self.is_edit_mode else f"Добавление: {table_name}"
        self.title(title)
        self.geometry("600x500")
        self.resizable(True, True)
        
        # Загружаем структуру таблицы
        self.load_table_structure()
        
        # Настройка UI
        self.setup_ui()
        
        # Загружаем данные для редактирования
        if self.is_edit_mode:
            self.load_record_data()
        
        # Фокус на первое поле
        if self.form_widgets:
            first_widget = list(self.form_widgets.values())[0]
            if isinstance(first_widget, (ttk.Entry, ttk.Combobox, tk.Text)):
                first_widget.focus()
    
    def load_table_structure(self):
        """Загружает структуру таблицы"""
        try:
            schema = self.db.get_schema()
            if self.table_name in schema:
                self.schema = schema
                self.table_structure = schema[self.table_name]["columns"]
            else:
                messagebox.showerror("Ошибка", f"Таблица {self.table_name} не найдена в схеме")
                self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить структуру таблицы: {str(e)}")
            self.destroy()
    
    def setup_ui(self):
        """Настройка интерфейса формы"""
        # Основной контейнер с прокруткой
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Создаем поля формы
        self.create_form_fields(scrollable_frame)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_save = ttk.Button(button_frame, text="Сохранить", command=self.save_record)
        self.btn_save.pack(side=tk.RIGHT, padx=5)
        
        self.btn_cancel = ttk.Button(button_frame, text="Отмена", command=self.destroy)
        self.btn_cancel.pack(side=tk.RIGHT, padx=5)
        
        # Привязка горячих клавиш
        self.bind('<Return>', lambda e: self.save_record())
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Control-s>', lambda e: self.save_record())
    
    def create_form_fields(self, parent):
        """Динамически создает поля формы на основе структуры таблицы"""
        if not self.table_structure:
            return
        
        row = 0
        for column_name, column_info in self.table_structure.items():
            # Пропускаем первичный ключ при добавлении (автоинкремент)
            if column_info.get("primary_key") and not self.is_edit_mode:
                continue
            
            # Метка поля
            label = ttk.Label(parent, text=column_name + ("" if column_info.get("nullable") else " *"))
            label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Индикация обязательных полей
            if not column_info.get("nullable"):
                label.config(foreground="red")
            
            # Создаем виджет в зависимости от типа поля
            widget = self.create_field_widget(parent, column_name, column_info)
            widget.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5)
            
            # Сохраняем виджет
            self.form_widgets[column_name] = widget
            self.form_fields[column_name] = column_info
            
            # Подсказка (tooltip)
            self.create_tooltip(widget, column_info)
            
            row += 1
        
        # Настройка растягивания столбцов
        parent.columnconfigure(1, weight=1)
    
    def create_field_widget(self, parent, column_name: str, column_info: Dict[str, Any]) -> tk.Widget:
        """
        Создает виджет для поля в зависимости от его типа
        
        Args:
            parent: Родительский виджет
            column_name: Имя столбца
            column_info: Информация о столбце
        
        Returns:
            Виджет для ввода данных
        """
        data_type = column_info.get("type", "").lower()
        is_foreign_key = column_info.get("foreign_key") is not None
        is_primary_key = column_info.get("primary_key", False)
        
        # Внешний ключ - комбобокс
        if is_foreign_key and not is_primary_key:
            return self.create_foreign_key_combo(parent, column_info)
        
        # Boolean - чекбокс
        if data_type in ['bool', 'boolean']:
            var = tk.BooleanVar()
            widget = ttk.Checkbutton(parent, variable=var)
            # Сохраняем и виджет, и переменную
            self.form_widgets[column_name] = widget
            setattr(widget, '_var', var)  # Сохраняем переменную в виджете
            return widget
        
        # Числовые типы - Spinbox
        if data_type in ['int', 'integer', 'bigint', 'smallint', 'decimal', 'numeric', 'float', 'double precision']:
            widget = ttk.Spinbox(parent, from_=-999999, to=999999, width=30)
            return widget
        
        # Большие тексты - Text
        max_length = column_info.get("max_length")
        if data_type in ['text'] or (max_length is not None and max_length > 255):
            widget = tk.Text(parent, height=5, width=40, wrap=tk.WORD)
            return widget
        
        # Строки - Entry
        widget = ttk.Entry(parent, width=40)
        max_length = column_info.get("max_length")
        if max_length is not None and max_length > 0:
            # Можно добавить валидацию длины
            pass
        return widget
    
    def create_foreign_key_combo(self, parent, column_info: Dict[str, Any]) -> ttk.Combobox:
        """Создает комбобокс для внешнего ключа"""
        fk_info = column_info.get("foreign_key")
        if not fk_info:
            # Если нет информации о FK, создаем обычное поле
            print(f"[DEBUG] Нет информации о внешнем ключе для {column_info}")
            return ttk.Entry(parent, width=40)
        
        fk_table = fk_info["table"]
        fk_column = fk_info["column"]
        is_nullable = column_info.get("nullable", True)
        
        print(f"[DEBUG] Создание комбобокса для FK: {fk_table}.{fk_column}, nullable={is_nullable}")
        
        try:
            # Получаем опции для комбобокса
            options = self.db.get_foreign_key_options(fk_table, fk_column)
            print(f"[DEBUG] Получено {len(options)} опций для {fk_table}.{fk_column}")
            
            # Формируем список значений для комбобокса
            values = []
            value_map = {}
            reverse_map = {}  # Для быстрого поиска по значению
            
            # Проверяем, есть ли опции
            if not options:
                print(f"[WARNING] Нет опций для внешнего ключа {fk_table}.{fk_column}")
                # Если нет опций и поле не nullable, создаем обычное поле
                if not is_nullable:
                    print(f"[WARNING] Поле {column_info} не nullable, но нет опций. Создаем обычное поле.")
                    return ttk.Entry(parent, width=40)
                # Если nullable, добавляем только опцию "(Не выбрано)"
                values.append("(Не выбрано)")
                value_map["(Не выбрано)"] = None
                reverse_map[None] = "(Не выбрано)"
            else:
                # Добавляем опцию "Не выбрано" если поле nullable
                if is_nullable:
                    values.append("(Не выбрано)")
                    value_map["(Не выбрано)"] = None
                    reverse_map[None] = "(Не выбрано)"
                
                # Добавляем опции из БД
                for value, display in options:
                    display_text = f"{display} (ID: {value})"
                    values.append(display_text)
                    value_map[display_text] = value
                    reverse_map[value] = display_text
                    reverse_map[str(value)] = display_text  # Для строковых ID
            
            widget = ttk.Combobox(parent, values=values, state="readonly", width=37)
            widget.value_map = value_map  # Сохраняем маппинг для получения значения
            widget.reverse_map = reverse_map  # Для поиска по значению при загрузке
            widget.fk_table = fk_table  # Сохраняем информацию о связанной таблице
            widget.is_nullable = is_nullable
            
            # Добавляем поиск (autocomplete)
            def on_key_release(event):
                typed = widget.get().lower()
                if typed:
                    filtered = [v for v in values if typed in v.lower()]
                    widget['values'] = filtered if filtered else values
                else:
                    widget['values'] = values
            
            # Разрешаем редактирование для поиска
            widget.config(state="normal")
            widget.bind('<KeyRelease>', on_key_release)
            widget.bind('<FocusOut>', lambda e: widget.config(state="readonly"))
            widget.bind('<Button-1>', lambda e: widget.config(state="normal"))
            
            print(f"[DEBUG] Комбобокс создан успешно с {len(values)} опциями")
            return widget
        except Exception as e:
            # В случае ошибки создаем обычное поле
            print(f"[ERROR] Ошибка создания комбобокса для FK {fk_table}.{fk_column}: {e}")
            import traceback
            traceback.print_exc()
            return ttk.Entry(parent, width=40)
    
    def create_tooltip(self, widget, column_info: Dict[str, Any]):
        """Создает подсказку для виджета"""
        tooltip_text = f"Тип: {column_info.get('type', 'unknown')}"
        if column_info.get("max_length"):
            tooltip_text += f", Макс. длина: {column_info.get('max_length')}"
        if column_info.get("default"):
            tooltip_text += f", По умолчанию: {column_info.get('default')}"
        
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ttk.Label(tooltip, text=tooltip_text, background="lightyellow",
                            relief=tk.SOLID, borderwidth=1, padding=5)
            label.pack()
            tooltip.after(3000, tooltip.destroy)
        
        widget.bind('<Enter>', show_tooltip)
    
    def load_record_data(self):
        """Загружает данные записи для редактирования"""
        if not self.record_id:
            return
        
        try:
            # Получаем первичный ключ
            pk_column = self.db._get_primary_key(self.table_name)
            if not pk_column:
                messagebox.showerror("Ошибка", "Не удалось определить первичный ключ")
                return
            
            # Получаем данные записи
            query = f'SELECT * FROM "{self.table_name}" WHERE "{pk_column}" = %s'
            cursor = self.db.conn.cursor()
            cursor.execute(query, (self.record_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if not row:
                messagebox.showerror("Ошибка", "Запись не найдена")
                self.destroy()
                return
            
            # Получаем названия столбцов
            columns = list(self.table_structure.keys())
            
            # Заполняем поля формы
            for i, column_name in enumerate(columns):
                if column_name in self.form_widgets:
                    value = row[i] if i < len(row) else None
                    self.set_field_value(column_name, value)
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.destroy()
    
    def set_field_value(self, column_name: str, value: Any):
        """Устанавливает значение поля формы"""
        if column_name not in self.form_widgets:
            print(f"[DEBUG] Виджет для {column_name} не найден")
            return
        
        widget = self.form_widgets[column_name]
        
        print(f"[DEBUG] Установка значения для {column_name}: {value} (type: {type(value)})")
        
        # Обрабатываем разные типы виджетов
        if isinstance(widget, ttk.Combobox):
            # Для комбобокса ищем значение через reverse_map
            if hasattr(widget, 'reverse_map'):
                # Пробуем найти по значению
                display_text = None
                if value is None:
                    if hasattr(widget, 'is_nullable') and widget.is_nullable:
                        display_text = "(Не выбрано)"
                        widget.set(display_text)
                        print(f"[DEBUG] Установлено NULL значение для nullable поля")
                        return
                    else:
                        print(f"[WARNING] Попытка установить NULL для non-nullable поля {column_name}")
                        return
                else:
                    # Пробуем найти по разным вариантам значения
                    search_keys = [value]
                    if isinstance(value, str) and value.isdigit():
                        search_keys.append(int(value))
                    if isinstance(value, (int, float)):
                        search_keys.append(str(value))
                    
                    for key in search_keys:
                        if key is not None and key in widget.reverse_map:
                            display_text = widget.reverse_map[key]
                            break
                
                if display_text:
                    widget.set(display_text)
                    print(f"[DEBUG] Установлено значение комбобокса: {display_text}")
                else:
                    # Если не нашли, пробуем найти по частичному совпадению
                    value_str = str(value)
                    for option in widget['values']:
                        if value_str in option or option.endswith(f"(ID: {value_str})"):
                            widget.set(option)
                            print(f"[DEBUG] Установлено значение комбобокса по совпадению: {option}")
                            break
                    else:
                        print(f"[WARNING] Не удалось найти значение {value} в опциях комбобокса")
            else:
                # Старый способ поиска
                for option in widget['values']:
                    if str(value) in option:
                        widget.set(option)
                        break
            return
        
        if value is None:
            return
        elif isinstance(widget, ttk.Checkbutton):
            # Для чекбокса используем переменную
            var = widget
            var.set(bool(value))
        elif isinstance(widget, tk.Text):
            widget.delete('1.0', tk.END)
            widget.insert('1.0', str(value))
        else:
            # Для Entry, Spinbox и других
            widget.delete(0, tk.END)
            widget.insert(0, str(value))
    
    def validate_form(self) -> bool:
        """Валидация введенных данных"""
        errors = []
        
        for column_name, column_info in self.form_fields.items():
            widget = self.form_widgets.get(column_name)
            if not widget:
                continue
            
            value = self.get_field_value(column_name)
            
            # Проверка обязательных полей
            if not column_info.get("nullable", True):
                if value is None or (isinstance(value, str) and not value.strip()):
                    errors.append(f"Поле '{column_name}' обязательно для заполнения")
                    continue
            
            # Валидация внешних ключей
            if column_info.get("foreign_key") and value is not None:
                fk_info = column_info.get("foreign_key")
                fk_table = fk_info["table"]
                fk_column = fk_info["column"]
                
                # Проверяем, что значение существует в связанной таблице
                try:
                    pk_column = self.db._get_primary_key(fk_table)
                    if not pk_column:
                        pk_column = fk_column
                    
                    query = f'SELECT COUNT(*) FROM "{fk_table}" WHERE "{pk_column}" = %s'
                    cursor = self.db.conn.cursor()
                    cursor.execute(query, (value,))
                    count = cursor.fetchone()[0]
                    cursor.close()
                    
                    if count == 0:
                        errors.append(f"Поле '{column_name}': выбранное значение не существует в таблице '{fk_table}'")
                except Exception as e:
                    print(f"[WARNING] Ошибка валидации внешнего ключа {column_name}: {e}")
                    # Не блокируем сохранение, но предупреждаем
                    errors.append(f"Поле '{column_name}': не удалось проверить значение ({str(e)})")
            
            # Валидация типов данных
            if value is not None and value != "":
                data_type = column_info.get("type", "").lower()
                
                # Валидация числовых типов
                if data_type in ['int', 'integer', 'bigint', 'smallint']:
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        errors.append(f"Поле '{column_name}' должно быть целым числом")
                
                elif data_type in ['decimal', 'numeric', 'float', 'double precision']:
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        errors.append(f"Поле '{column_name}' должно быть числом")
        
        if errors:
            messagebox.showerror("Ошибки валидации", "\n".join(errors))
            return False
        
        return True
    
    def get_field_value(self, column_name: str) -> Any:
        """Получает значение поля формы"""
        widget = self.form_widgets.get(column_name)
        if not widget:
            print(f"[DEBUG] Виджет для {column_name} не найден")
            return None
        
        # Обрабатываем разные типы виджетов
        if isinstance(widget, ttk.Combobox):
            selected = widget.get()
            print(f"[DEBUG] Получение значения из комбобокса {column_name}: '{selected}'")
            
            if not selected or selected == "(Не выбрано)":
                # Проверяем, может ли поле быть NULL
                column_info = self.form_fields.get(column_name, {})
                if column_info.get("nullable", True):
                    print(f"[DEBUG] Возвращаем None для nullable поля {column_name}")
                    return None
                else:
                    print(f"[WARNING] Поле {column_name} не может быть NULL, но значение не выбрано")
                    return None
            
            if hasattr(widget, 'value_map') and selected in widget.value_map:
                value = widget.value_map[selected]
                print(f"[DEBUG] Значение из value_map: {value}")
                return value
            
            # Пытаемся извлечь значение из строки "Display (ID: Value)"
            if 'ID:' in selected:
                try:
                    # Формат: "Display (ID: 123)"
                    value_str = selected.split('ID:')[1].strip().rstrip(')')
                    print(f"[DEBUG] Извлечено значение из строки: {value_str}")
                    # Пробуем преобразовать в число, если возможно
                    try:
                        return int(value_str)
                    except ValueError:
                        return value_str
                except:
                    pass
            
            # Пытаемся извлечь значение из строки "Display (Value)"
            if '(' in selected and ')' in selected:
                try:
                    value_str = selected.split('(')[1].rstrip(')')
                    print(f"[DEBUG] Извлечено значение из скобок: {value_str}")
                    try:
                        return int(value_str)
                    except ValueError:
                        return value_str
                except:
                    pass
            
            print(f"[WARNING] Не удалось извлечь значение из '{selected}', возвращаем как есть")
            return selected
        
        elif isinstance(widget, ttk.Checkbutton):
            # Для чекбокса возвращаем значение переменной
            if hasattr(widget, '_var'):
                return widget._var.get()
            else:
                var_name = widget.cget('variable')
                if var_name:
                    var = widget.nametowidget(var_name) if '.' in var_name else self.nametowidget(var_name)
                    return var.get()
                return False
        
        elif isinstance(widget, tk.Text):
            return widget.get('1.0', tk.END).strip()
        
        else:
            # Для Entry, Spinbox и других
            value = widget.get()
            return value.strip() if isinstance(value, str) else value
    
    def save_record(self):
        """Сохраняет данные (insert или update)"""
        if not self.validate_form():
            return
        
        try:
            # Собираем данные из формы
            data = {}
            for column_name in self.form_fields.keys():
                if column_name in self.form_widgets:
                    value = self.get_field_value(column_name)
                    if value is not None and value != "":
                        data[column_name] = value
            
            # Сохраняем запись
            if self.is_edit_mode:
                self.db.update_record(self.table_name, self.record_id, data)
                messagebox.showinfo("Успех", "Запись успешно обновлена")
            else:
                self.db.insert_record(self.table_name, data)
                messagebox.showinfo("Успех", "Запись успешно добавлена")
            
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {str(e)}")

