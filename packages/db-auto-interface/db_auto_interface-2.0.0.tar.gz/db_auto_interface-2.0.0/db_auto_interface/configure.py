"""
Утилита настройки интерфейса DB Auto Interface
Позволяет настроить темы, конфигурацию и генерацию кода
"""

import sys
import os
import json
import argparse
from typing import Optional, Dict, Any
from pathlib import Path


class ConfigManager:
    """Менеджер конфигурации"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Инициализация менеджера конфигурации
        
        Args:
            config_path: Путь к файлу конфигурации
        """
        if config_path is None:
            # Путь по умолчанию
            config_path = os.path.join(
                os.path.dirname(__file__),
                'themes_config.json'
            )
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Возвращает конфигурацию по умолчанию"""
        return {
            "available_patterns": [
                "minimalist",
                "dark",
                "classic",
                "contrast",
                "simple"
            ],
            "pattern_descriptions": {
                "minimalist": "Современный минимализм - светлая тема с скругленными углами",
                "dark": "Темная тема - dark mode с контрастными акцентами",
                "classic": "Классический - деловой стиль с синими акцентами",
                "contrast": "Контрастный - яркие цвета с четкими границами",
                "simple": "Упрощенный - максимально простой для слабых ПК"
            },
            "user_mappings": {},
            "auto_selection": {
                "enabled": True,
                "method": "username",
                "fallback": "minimalist"
            },
            "code_generation": {
                "enabled": True,
                "auto_generate": False,
                "default_output": "generated_interface.py",
                "include_comments": True,
                "include_docstrings": True
            }
        }
    
    def save_config(self) -> bool:
        """Сохраняет конфигурацию в файл"""
        try:
            # Создаем директорию если не существует
            os.makedirs(os.path.dirname(self.config_path) if os.path.dirname(self.config_path) else '.', 
                       exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False
    
    def set_pattern(self, pattern: str) -> bool:
        """
        Устанавливает паттерн по умолчанию
        
        Args:
            pattern: Имя паттерна
            
        Returns:
            True если успешно установлено
        """
        if pattern not in self.config.get("available_patterns", []):
            print(f"Ошибка: паттерн '{pattern}' не найден")
            print(f"Доступные паттерны: {', '.join(self.config.get('available_patterns', []))}")
            return False
        
        # Обновляем fallback в auto_selection
        if "auto_selection" not in self.config:
            self.config["auto_selection"] = {}
        
        self.config["auto_selection"]["fallback"] = pattern
        self.config["auto_selection"]["enabled"] = False  # Отключаем авто-выбор
        
        return True
    
    def enable_code_generation(self, enabled: bool = True):
        """Включает/выключает генерацию кода"""
        if "code_generation" not in self.config:
            self.config["code_generation"] = {}
        
        self.config["code_generation"]["enabled"] = enabled
    
    def set_code_output(self, output_file: str):
        """Устанавливает путь к выходному файлу генерации кода"""
        if "code_generation" not in self.config:
            self.config["code_generation"] = {}
        
        self.config["code_generation"]["default_output"] = output_file
    
    def add_user_mapping(self, username: str, pattern: str) -> bool:
        """
        Добавляет привязку пользователя к паттерну
        
        Args:
            username: Имя пользователя
            pattern: Имя паттерна
            
        Returns:
            True если успешно добавлено
        """
        if pattern not in self.config.get("available_patterns", []):
            print(f"Ошибка: паттерн '{pattern}' не найден")
            return False
        
        if "user_mappings" not in self.config:
            self.config["user_mappings"] = {}
        
        self.config["user_mappings"][username] = pattern
        return True
    
    def remove_user_mapping(self, username: str):
        """Удаляет привязку пользователя"""
        if "user_mappings" in self.config:
            self.config["user_mappings"].pop(username, None)
    
    def list_patterns(self):
        """Выводит список доступных паттернов"""
        patterns = self.config.get("available_patterns", [])
        descriptions = self.config.get("pattern_descriptions", {})
        
        print("Доступные паттерны:")
        print("=" * 50)
        for pattern in patterns:
            desc = descriptions.get(pattern, "Описание недоступно")
            print(f"  {pattern:15} - {desc}")
        print()
    
    def show_config(self):
        """Выводит текущую конфигурацию"""
        print("Текущая конфигурация:")
        print("=" * 50)
        print(json.dumps(self.config, indent=2, ensure_ascii=False))
        print()


def main():
    """Главная функция утилиты настройки"""
    parser = argparse.ArgumentParser(
        description='Утилита настройки DB Auto Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  
  # Установить тему по умолчанию
  python -m db_auto_interface.configure --pattern dark
  
  # Включить генерацию кода
  python -m db_auto_interface.configure --generate-code
  
  # Установить путь для генерации кода
  python -m db_auto_interface.configure --code-output my_interface.py
  
  # Добавить привязку пользователя
  python -m db_auto_interface.configure --user student1 --pattern minimalist
  
  # Показать список паттернов
  python -m db_auto_interface.configure --list-patterns
  
  # Показать текущую конфигурацию
  python -m db_auto_interface.configure --show-config
        """
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        help='Установить паттерн темы по умолчанию'
    )
    
    parser.add_argument(
        '--generate-code',
        action='store_true',
        help='Включить автоматическую генерацию кода'
    )
    
    parser.add_argument(
        '--no-generate-code',
        action='store_true',
        help='Выключить генерацию кода'
    )
    
    parser.add_argument(
        '--code-output',
        type=str,
        help='Установить путь к выходному файлу для генерации кода'
    )
    
    parser.add_argument(
        '--user',
        type=str,
        help='Имя пользователя для привязки к паттерну (используйте с --pattern)'
    )
    
    parser.add_argument(
        '--list-patterns',
        action='store_true',
        help='Показать список доступных паттернов'
    )
    
    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Показать текущую конфигурацию'
    )
    
    parser.add_argument(
        '--config-path',
        type=str,
        help='Путь к файлу конфигурации'
    )
    
    args = parser.parse_args()
    
    # Создаем менеджер конфигурации
    config_manager = ConfigManager(args.config_path)
    
    # Обработка аргументов
    if args.list_patterns:
        config_manager.list_patterns()
        return
    
    if args.show_config:
        config_manager.show_config()
        return
    
    # Флаг для отслеживания изменений
    changed = False
    
    if args.pattern:
        if args.user:
            # Привязка пользователя к паттерну
            if config_manager.add_user_mapping(args.user, args.pattern):
                print(f"Привязка добавлена: пользователь '{args.user}' -> паттерн '{args.pattern}'")
                changed = True
        else:
            # Установка паттерна по умолчанию
            if config_manager.set_pattern(args.pattern):
                print(f"Паттерн по умолчанию установлен: {args.pattern}")
                changed = True
    
    if args.generate_code:
        config_manager.enable_code_generation(True)
        print("Генерация кода включена")
        changed = True
    
    if args.no_generate_code:
        config_manager.enable_code_generation(False)
        print("Генерация кода выключена")
        changed = True
    
    if args.code_output:
        config_manager.set_code_output(args.code_output)
        print(f"Путь для генерации кода установлен: {args.code_output}")
        changed = True
    
    # Сохраняем конфигурацию если были изменения
    if changed:
        if config_manager.save_config():
            print(f"Конфигурация сохранена в: {config_manager.config_path}")
        else:
            print("Ошибка при сохранении конфигурации")
            sys.exit(1)
    elif not args.list_patterns and not args.show_config:
        # Если не было аргументов, показываем помощь
        parser.print_help()


if __name__ == "__main__":
    main()
