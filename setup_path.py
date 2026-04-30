"""
Скрипт для установки UMSFA в PATH

Использование:
    python setup_path.py --add       # Добавить UMSFA в PATH
    python setup_path.py --remove    # Удалить UMSFA из PATH
    python setup_path.py --check     # Проверить статус
"""

import os
import sys
import winreg
from pathlib import Path


class UMSFASetup:
    """Класс для управления UMSFA в PATH"""
    
    def __init__(self):
        self.umsfa_dir = Path(__file__).parent.resolve()
        self.user_registry_path = r"Environment"
        self.system_registry_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        
    def is_windows(self):
        """Проверка операционной системы"""
        return sys.platform.startswith('win')
    
    def get_path(self, scope='user'):
        """Получение переменной PATH из реестра"""
        try:
            root, registry_path = self._get_registry_target(scope)
            key = winreg.OpenKey(root, registry_path)
            path, _ = winreg.QueryValueEx(key, 'Path')
            winreg.CloseKey(key)
            return path
        except FileNotFoundError:
            return ''
        except Exception as e:
            print(f"Ошибка при чтении PATH: {e}")
            return None
    
    def set_path(self, new_path, scope='user'):
        """Установка переменной PATH в реестр"""
        try:
            root, registry_path = self._get_registry_target(scope)
            key = winreg.CreateKeyEx(
                root,
                registry_path,
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(key)
            return True
        except PermissionError:
            if scope == 'system':
                print("Ошибка: для изменения системного PATH требуются права администратора.")
                print("   Запустите PowerShell от имени администратора или используйте --scope user")
            else:
                print("Ошибка: не удалось изменить пользовательский PATH.")
                print("   Если это обычный Windows-сеанс, проверьте права записи в HKCU\\Environment.")
            return False
        except Exception as e:
            print(f"Ошибка при установке PATH: {e}")
            return False

    def _get_registry_target(self, scope):
        normalized_scope = scope.lower()
        if normalized_scope == 'system':
            return winreg.HKEY_LOCAL_MACHINE, self.system_registry_path
        return winreg.HKEY_CURRENT_USER, self.user_registry_path
    
    def is_admin(self):
        """Проверка наличия прав администратора"""
        try:
            return os.getuid() == 0  # Linux/macOS
        except AttributeError:
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
    
    def add_to_path(self, scope='user'):
        """Добавление UMSFA в PATH"""
        if not self.is_windows():
            print("Предупреждение: эта функция работает только на Windows.")
            print("   Для Linux/macOS: добавьте строку в ~/.bashrc или ~/.zshrc:")
            print(f"   export PATH=\"$PATH:{self.umsfa_dir}\"")
            return False
        
        if scope == 'system' and not self.is_admin():
            print("Ошибка: для системного PATH требуются права администратора.")
            print("   Используйте PowerShell от имени администратора или выполните:")
            print(f"   python setup_path.py --add --scope user")
            return False
        
        current_path = self.get_path(scope)
        if current_path is None:
            return False
        
        paths = self._split_path_entries(current_path)
        umsfa_dir_str = str(self.umsfa_dir)

        if any(self._paths_equal(path, umsfa_dir_str) for path in paths):
            print(f"UMSFA уже есть в {scope} PATH: {self.umsfa_dir}")
            return True
        
        paths.append(umsfa_dir_str)
        new_path = ";".join(paths)
        
        if self.set_path(new_path, scope):
            print(f"UMSFA успешно добавлен в {scope} PATH.")
            print(f"   Путь: {self.umsfa_dir}")
            print()
            print("Нужно открыть новый PowerShell/cmd, чтобы PATH обновился:")
            print("   1. Закройте текущую командную строку/PowerShell")
            print("   2. Откройте новую командную строку/PowerShell")
            print("   3. Введите: UMSFA --help")
            print()
            return True
        
        return False
    
    def remove_from_path(self, scope='user'):
        """Удаление UMSFA из PATH"""
        if not self.is_windows():
            print("Предупреждение: эта функция работает только на Windows.")
            print("   Для Linux/macOS: удалите строку из ~/.bashrc или ~/.zshrc")
            return False
        
        if scope == 'system' and not self.is_admin():
            print("Ошибка: для изменения системного PATH требуются права администратора.")
            return False
        
        current_path = self.get_path(scope)
        if current_path is None:
            return False
        
        paths = self._split_path_entries(current_path)
        filtered_paths = [
            path for path in paths
            if not self._paths_equal(path, str(self.umsfa_dir))
        ]

        if len(filtered_paths) == len(paths):
            print(f"UMSFA уже отсутствует в {scope} PATH.")
            return True
        
        new_path = ";".join(filtered_paths)
        
        if self.set_path(new_path, scope):
            print(f"UMSFA успешно удален из {scope} PATH.")
            print()
            print("Нужно открыть новый PowerShell/cmd, чтобы PATH обновился:")
            print("   1. Закройте текущую командную строку/PowerShell")
            print("   2. Откройте новую командную строку/PowerShell")
            return True
        
        return False
    
    def check_status(self):
        """Проверка статуса UMSFA в PATH"""
        print("Статус UMSFA")
        print("=" * 60)
        print()
        
        print(f"Директория UMSFA: {self.umsfa_dir}")
        print()
        
        if self.is_windows():
            for scope in ('user', 'system'):
                current_path = self.get_path(scope)
                if current_path is None:
                    return

                scope_label = 'пользовательский' if scope == 'user' else 'системный'
                if any(
                    self._paths_equal(path, str(self.umsfa_dir))
                    for path in self._split_path_entries(current_path)
                ):
                    print(f"Статус: UMSFA добавлен в {scope_label} PATH")
                else:
                    print(f"Статус: UMSFA НЕ в {scope_label} PATH")

            print()
            print("Вы можете использовать команды из любой папки:")
            print("   UMSFA create -p \"password\"")
            print("   UMSFA extract -p \"password\"")
            print("   UMSFA info archive.ms")
            print()
            print("Для установки без прав администратора:")
            print("   python setup_path.py --add --scope user")
        else:
            # Linux/macOS
            shell_rc = Path.home() / ".bashrc"
            if not shell_rc.exists():
                shell_rc = Path.home() / ".zshrc"
            
            if shell_rc.exists():
                content = shell_rc.read_text()
                if str(self.umsfa_dir) in content:
                    print("Статус: UMSFA добавлен в PATH (Linux/macOS)")
                else:
                    print("Статус: UMSFA НЕ в PATH (Linux/macOS)")
                    print()
                    print("Для добавления добавьте в ~/.bashrc или ~/.zshrc:")
                    print(f"   export PATH=\"$PATH:{self.umsfa_dir}\"")
            else:
                print("Предупреждение: не удалось определить shell конфигурацию.")
        
        print()

    @staticmethod
    def _split_path_entries(path_value):
        return [part for part in path_value.split(";") if part.strip()]

    @staticmethod
    def _paths_equal(left, right):
        return os.path.normcase(os.path.normpath(left)) == os.path.normcase(os.path.normpath(right))


def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='UMSFA - Setup PATH Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:

  # Проверить статус
  python setup_path.py --check

  # Добавить UMSFA в PATH для текущего пользователя
  python setup_path.py --add --scope user

  # Удалить UMSFA из PATH для текущего пользователя
  python setup_path.py --remove --scope user
        '''
    )
    
    parser.add_argument(
        '--add',
        action='store_true',
        help='Добавить UMSFA в PATH'
    )
    parser.add_argument(
        '--remove',
        action='store_true',
        help='Удалить UMSFA из PATH'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Проверить статус UMSFA в PATH'
    )
    parser.add_argument(
        '--scope',
        choices=['user', 'system'],
        default='user',
        help='Куда добавлять PATH на Windows: user (по умолчанию) или system'
    )
    
    args = parser.parse_args()
    
    setup = UMSFASetup()
    
    if args.add:
        if setup.add_to_path(args.scope):
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.remove:
        if setup.remove_from_path(args.scope):
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.check:
        setup.check_status()
        sys.exit(0)
    else:
        parser.print_help()
        print()
        print("Используйте --check для проверки статуса.")
        sys.exit(1)


if __name__ == '__main__':
    main()
