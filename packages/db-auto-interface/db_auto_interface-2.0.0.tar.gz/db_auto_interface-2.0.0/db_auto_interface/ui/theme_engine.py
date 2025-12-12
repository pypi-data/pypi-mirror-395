"""
Система уникальных интерфейсных паттернов (тем)
Предоставляет различные визуальные стили для разных пользователей
"""

import tkinter as tk
from tkinter import ttk
import hashlib
import os
import getpass
from typing import Dict, Any, Optional, List


class ThemePattern:
    """Базовый класс для паттерна темы"""
    
    def __init__(self, name: str, display_name: str):
        self.name = name
        self.display_name = display_name
        self.colors = {}
        self.fonts = {}
        self.styles = {}
        
    def apply(self, root: tk.Tk) -> None:
        """Применяет паттерн к корневому окну"""
        raise NotImplementedError("Subclass must implement apply method")


class MinimalistTheme(ThemePattern):
    """Pattern1: Современный минимализм (светлая тема, скругленные углы)"""
    
    def __init__(self):
        super().__init__("minimalist", "Современный минимализм")
        self.colors = {
            'bg': '#FFFFFF',
            'fg': '#2C3E50',
            'select_bg': '#3498DB',
            'select_fg': '#FFFFFF',
            'entry_bg': '#F8F9FA',
            'entry_fg': '#212529',
            'button_bg': '#3498DB',
            'button_fg': '#FFFFFF',
            'button_active': '#2980B9',
            'accent': '#3498DB',
            'border': '#E1E8ED',
            'hover': '#ECF0F1'
        }
        self.fonts = {
            'default': ('Segoe UI', 10),
            'heading': ('Segoe UI', 12, 'bold'),
            'small': ('Segoe UI', 9)
        }
    
    def apply(self, root: tk.Tk) -> None:
        style = ttk.Style()
        style.theme_use('clam')
        
        # Фон окна
        root.configure(bg=self.colors['bg'])
        
        # Стили для кнопок
        style.configure('TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        style.map('TButton',
                 background=[('active', self.colors['button_active']),
                           ('pressed', self.colors['button_active'])],
                 foreground=[('active', self.colors['button_fg'])])
        
        # Стили для рамок
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['default'])
        style.configure('TLabelFrame', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])
        
        # Стили для полей ввода
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'],
                       borderwidth=1,
                       relief='flat')
        style.map('TEntry',
                 fieldbackground=[('focus', '#FFFFFF')],
                 bordercolor=[('focus', self.colors['accent'])])
        
        # Стили для Treeview
        style.configure('Treeview',
                       background='#FFFFFF',
                       foreground=self.colors['fg'],
                       fieldbackground='#FFFFFF',
                       borderwidth=1)
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground='#FFFFFF',
                       font=self.fonts['small'])
        style.map('Treeview',
                 background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])
        
        # Стили для Scrollbar
        style.configure('TScrollbar',
                       background=self.colors['border'],
                       troughcolor=self.colors['bg'],
                       borderwidth=0,
                       arrowcolor=self.colors['fg'],
                       width=12)
        
        # Стили для Notebook
        style.configure('TNotebook',
                       background=self.colors['bg'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=self.colors['border'],
                       foreground=self.colors['fg'],
                       padding=(12, 6))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', '#FFFFFF'),
                           ('!selected', self.colors['fg'])])

class DarkTheme(ThemePattern):
    """Pattern2: Темная тема (dark mode, контрастные акценты)"""
    
    def __init__(self):
        super().__init__("dark", "Темная тема")
        self.colors = {
            'bg': '#1E1E1E',
            'fg': '#D4D4D4',
            'select_bg': '#007ACC',
            'select_fg': '#FFFFFF',
            'entry_bg': '#252526',
            'entry_fg': '#CCCCCC',
            'button_bg': '#0E639C',
            'button_fg': '#FFFFFF',
            'button_active': '#1177BB',
            'accent': '#007ACC',
            'border': '#3E3E42',
            'hover': '#2D2D30'
        }
        self.fonts = {
            'default': ('Consolas', 10),
            'heading': ('Consolas', 12, 'bold'),
            'small': ('Consolas', 9)
        }
    
    def apply(self, root: tk.Tk) -> None:
        style = ttk.Style()
        style.theme_use('clam')
        
        root.configure(bg=self.colors['bg'])
        
        style.configure('TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        style.map('TButton',
                 background=[('active', self.colors['button_active'])],
                 foreground=[('active', self.colors['button_fg'])])
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['default'])
        style.configure('TLabelFrame', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'])
        
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'],
                       borderwidth=1,
                       relief='flat')
        style.map('TEntry',
                 bordercolor=[('focus', self.colors['accent'])])
        
        style.configure('Treeview',
                       background=self.colors['entry_bg'],
                       foreground=self.colors['fg'],
                       fieldbackground=self.colors['entry_bg'],
                       borderwidth=1)
        style.configure('Treeview.Heading',
                       background=self.colors['border'],
                       foreground=self.colors['fg'],
                       font=self.fonts['small'])
        style.map('Treeview',
                 background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])
        
        style.configure('TScrollbar',
                       background=self.colors['border'],
                       troughcolor=self.colors['bg'],
                       borderwidth=0,
                       arrowcolor=self.colors['fg'],
                       width=12)
        
        style.configure('TNotebook',
                       background=self.colors['bg'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=self.colors['border'],
                       foreground=self.colors['fg'],
                       padding=(12, 6))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', '#FFFFFF')])


class ClassicTheme(ThemePattern):
    """Pattern3: Классический (деловой стиль, синие акценты)"""
    
    def __init__(self):
        super().__init__("classic", "Классический")
        self.colors = {
            'bg': '#F0F0F0',
            'fg': '#000080',
            'select_bg': '#0066CC',
            'select_fg': '#FFFFFF',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#000000',
            'button_bg': '#0066CC',
            'button_fg': '#FFFFFF',
            'button_active': '#0052A3',
            'accent': '#0066CC',
            'border': '#CCCCCC',
            'hover': '#E6E6E6'
        }
        self.fonts = {
            'default': ('Arial', 10),
            'heading': ('Arial', 12, 'bold'),
            'small': ('Arial', 9)
        }
    
    def apply(self, root: tk.Tk) -> None:
        style = ttk.Style()
        style.theme_use('clam')
        
        root.configure(bg=self.colors['bg'])
        
        style.configure('TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       borderwidth=2,
                       relief='raised',
                       padding=(12, 6))
        style.map('TButton',
                 background=[('active', self.colors['button_active']),
                           ('pressed', self.colors['button_active'])],
                 relief=[('pressed', 'sunken')])
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['default'])
        style.configure('TLabelFrame', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       borderwidth=2,
                       relief='groove')
        
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'],
                       borderwidth=2,
                       relief='sunken')
        style.map('TEntry',
                 bordercolor=[('focus', self.colors['accent'])])
        
        style.configure('Treeview',
                       background='#FFFFFF',
                       foreground='#000000',
                       fieldbackground='#FFFFFF',
                       borderwidth=2,
                       relief='solid')
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground='#FFFFFF',
                       font=self.fonts['heading'],
                       relief='raised')
        style.map('Treeview',
                 background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])
        
        style.configure('TScrollbar',
                       background=self.colors['border'],
                       troughcolor=self.colors['bg'],
                       borderwidth=1,
                       arrowcolor=self.colors['fg'],
                       width=15)
        
        style.configure('TNotebook',
                       background=self.colors['bg'],
                       borderwidth=2)
        style.configure('TNotebook.Tab',
                       background=self.colors['hover'],
                       foreground=self.colors['fg'],
                       padding=(15, 8),
                       borderwidth=1)
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', '#FFFFFF')])


class ContrastTheme(ThemePattern):
    """Pattern4: Контрастный (яркие цвета, четкие границы)"""
    
    def __init__(self):
        super().__init__("contrast", "Контрастный")
        self.colors = {
            'bg': '#FFFFFF',
            'fg': '#000000',
            'select_bg': '#FF6B00',
            'select_fg': '#FFFFFF',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#000000',
            'button_bg': '#FF6B00',
            'button_fg': '#FFFFFF',
            'button_active': '#FF4500',
            'accent': '#FF6B00',
            'border': '#000000',
            'hover': '#FFF4E6'
        }
        self.fonts = {
            'default': ('Verdana', 11, 'bold'),
            'heading': ('Verdana', 13, 'bold'),
            'small': ('Verdana', 10, 'bold')
        }
    
    def apply(self, root: tk.Tk) -> None:
        style = ttk.Style()
        style.theme_use('clam')
        
        root.configure(bg=self.colors['bg'])
        
        style.configure('TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       borderwidth=3,
                       relief='solid',
                       padding=(15, 10),
                       font=self.fonts['default'])
        style.map('TButton',
                 background=[('active', self.colors['button_active'])],
                 foreground=[('active', self.colors['button_fg'])],
                 borderwidth=[('active', 3)])
        
        style.configure('TFrame', 
                       background=self.colors['bg'],
                       borderwidth=2,
                       relief='solid')
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['default'])
        style.configure('TLabelFrame', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       borderwidth=3,
                       relief='solid')
        
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'],
                       borderwidth=3,
                       relief='solid',
                       font=self.fonts['default'])
        style.map('TEntry',
                 bordercolor=[('focus', self.colors['accent'])],
                 borderwidth=[('focus', 4)])
        
        style.configure('Treeview',
                       background='#FFFFFF',
                       foreground='#000000',
                       fieldbackground='#FFFFFF',
                       borderwidth=2,
                       relief='solid')
        style.configure('Treeview.Heading',
                       background=self.colors['accent'],
                       foreground='#FFFFFF',
                       font=self.fonts['heading'],
                       relief='solid',
                       borderwidth=2)
        style.map('Treeview',
                 background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])
        
        style.configure('TScrollbar',
                       background=self.colors['border'],
                       troughcolor=self.colors['bg'],
                       borderwidth=2,
                       arrowcolor=self.colors['fg'],
                       width=16)
        
        style.configure('TNotebook',
                       background=self.colors['bg'],
                       borderwidth=3)
        style.configure('TNotebook.Tab',
                       background=self.colors['hover'],
                       foreground=self.colors['fg'],
                       padding=(15, 10),
                       borderwidth=2,
                       font=self.fonts['default'])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', '#FFFFFF')])


class SimpleTheme(ThemePattern):
    """Pattern5: Упрощенный (максимально простой, для слабых ПК)"""
    
    def __init__(self):
        super().__init__("simple", "Упрощенный")
        self.colors = {
            'bg': '#C0C0C0',
            'fg': '#000000',
            'select_bg': '#000080',
            'select_fg': '#FFFFFF',
            'entry_bg': '#FFFFFF',
            'entry_fg': '#000000',
            'button_bg': '#C0C0C0',
            'button_fg': '#000000',
            'button_active': '#A0A0A0',
            'accent': '#000080',
            'border': '#808080',
            'hover': '#D4D4D4'
        }
        self.fonts = {
            'default': ('MS Sans Serif', 8),
            'heading': ('MS Sans Serif', 8, 'bold'),
            'small': ('MS Sans Serif', 8)
        }
    
    def apply(self, root: tk.Tk) -> None:
        style = ttk.Style()
        style.theme_use('classic')  # Используем классическую тему Windows
        
        root.configure(bg=self.colors['bg'])
        
        # Минимальные настройки для производительности
        style.configure('TButton',
                       padding=(8, 4))
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['default'])
        
        style.configure('TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'])
        
        style.configure('Treeview',
                       background='#FFFFFF',
                       foreground='#000000',
                       fieldbackground='#FFFFFF')
        style.configure('Treeview.Heading',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=self.fonts['small'])
        style.map('Treeview',
                 background=[('selected', self.colors['select_bg'])],
                 foreground=[('selected', self.colors['select_fg'])])


class ThemeEngine:
    """Движок управления темами"""
    
    # Регистр доступных паттернов
    PATTERNS = {
        'minimalist': MinimalistTheme,
        'dark': DarkTheme,
        'classic': ClassicTheme,
        'contrast': ContrastTheme,
        'simple': SimpleTheme
    }
    
    def __init__(self):
        self.current_pattern: Optional[ThemePattern] = None
        self.current_pattern_name: Optional[str] = None
    
    @classmethod
    def get_available_patterns(cls) -> List[str]:
        """Возвращает список доступных паттернов"""
        return list(cls.PATTERNS.keys())
    
    @classmethod
    def get_pattern_display_name(cls, pattern_name: str) -> str:
        """Возвращает отображаемое имя паттерна"""
        if pattern_name in cls.PATTERNS:
            pattern = cls.PATTERNS[pattern_name]()
            return pattern.display_name
        return pattern_name
    
    def select_pattern(self, pattern_name: str, root: tk.Tk) -> bool:
        """
        Выбирает и применяет паттерн
        
        Args:
            pattern_name: Имя паттерна
            root: Корневое окно приложения
            
        Returns:
            True если паттерн успешно применен
        """
        if pattern_name not in self.PATTERNS:
            return False
        
        self.current_pattern = self.PATTERNS[pattern_name]()
        self.current_pattern_name = pattern_name
        self.current_pattern.apply(root)
        
        return True
    
    def get_current_pattern(self) -> Optional[ThemePattern]:
        """Возвращает текущий паттерн"""
        return self.current_pattern
    
    def get_current_pattern_name(self) -> Optional[str]:
        """Возвращает имя текущего паттерна"""
        return self.current_pattern_name
    
    @staticmethod
    def select_pattern_by_username(username: Optional[str] = None) -> str:
        """
        Выбирает паттерн на основе имени пользователя системы
        
        Args:
            username: Имя пользователя (если None, берется из системы)
            
        Returns:
            Имя паттерна
        """
        if username is None:
            username = getpass.getuser()
        
        patterns = list(ThemeEngine.PATTERNS.keys())
        hash_value = int(hashlib.md5(username.encode()).hexdigest(), 16)
        pattern_index = hash_value % len(patterns)
        
        return patterns[pattern_index]
    
    @staticmethod
    def select_pattern_by_student_id(student_id: str) -> str:
        """
        Выбирает паттерн на основе хэша ID студента
        
        Args:
            student_id: ID студента
            
        Returns:
            Имя паттерна
        """
        patterns = list(ThemeEngine.PATTERNS.keys())
        hash_value = int(hashlib.md5(student_id.encode()).hexdigest(), 16)
        pattern_index = hash_value % len(patterns)
        
        return patterns[pattern_index]
    
    @staticmethod
    def select_pattern_deterministic(seed: str) -> str:
        """
        Детерминированный выбор паттерна на основе seed
        
        Args:
            seed: Строка-ключ для генерации
            
        Returns:
            Имя паттерна
        """
        patterns = list(ThemeEngine.PATTERNS.keys())
        hash_value = int(hashlib.md5(seed.encode()).hexdigest(), 16)
        pattern_index = hash_value % len(patterns)
        
        return patterns[pattern_index]


def apply_theme(pattern_name: str, root_window: tk.Tk) -> bool:
    """
    Применяет выбранный паттерн ко всему Tkinter приложению
    
    Args:
        pattern_name: Имя паттерна (minimalist, dark, classic, contrast, simple)
        root_window: Корневое окно приложения
        
    Returns:
        True если тема успешно применена
        
    Example:
        >>> import tkinter as tk
        >>> root = tk.Tk()
        >>> apply_theme('dark', root)
        True
    """
    engine = ThemeEngine()
    return engine.select_pattern(pattern_name, root_window)
