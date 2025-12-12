"""
db_auto_interface - Универсальная библиотека для автоматического интерфейса работы с БД

Автоматический генератор desktop интерфейса для PostgreSQL баз данных.
Создает полнофункциональный GUI для работы с любыми таблицами БД без написания кода.
"""

from .core.universal_db import UniversalDB
from .ui.main_app import DBAutoInterface

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = ['UniversalDB', 'DBAutoInterface', '__version__']

