"""
CLI интерфейс для Universal MS Format Archiver (UMSFA)
"""

import sys
import os
import argparse
from pathlib import Path
from getpass import getpass
from umsfa import MSArchiver

DEFAULT_COMPRESSION_LEVEL = 6


PROTECTED_PATHS = {
    Path('C:/Windows'),
    Path('C:/Program Files'),
    Path('C:/Program Files (x86)'),
    Path('C:/ProgramData'),
    Path('C:/System Volume Information'),
    Path('C:/$Recycle.Bin'),
    Path('C:/PerfLogs'),
}

PROTECTED_ENV_PATHS = {
    'WINDIR',
    'SYSTEMROOT',
    'PROGRAMFILES',
    'PROGRAMFILES(X86)',
    'ALLUSERSPROFILE',
}


def _path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _resolve_existing_base(path_str: str) -> Path:
    path = Path(path_str).expanduser()
    if path.exists():
        return path.resolve()
    if path.parent.exists():
        return (path.parent.resolve() / path.name)
    return path.resolve(strict=False)


def get_protected_roots():
    protected_roots = set()
    for protected in PROTECTED_PATHS:
        try:
            protected_roots.add(protected.resolve())
        except FileNotFoundError:
            protected_roots.add(protected)

    for env_var in PROTECTED_ENV_PATHS:
        env_value = os.environ.get(env_var, '').strip()
        if not env_value:
            continue
        try:
            env_path = Path(env_value).expanduser().resolve()
        except FileNotFoundError:
            env_path = Path(env_value).expanduser()
        protected_roots.add(env_path)

    system_root = os.environ.get('SYSTEMROOT') or os.environ.get('WINDIR')
    if system_root:
        try:
            protected_roots.add((Path(system_root).resolve() / 'System32').resolve())
            protected_roots.add((Path(system_root).resolve() / 'SysWOW64').resolve())
        except FileNotFoundError:
            pass

    return protected_roots


def is_protected_path(path_str: str) -> bool:
    try:
        path = _resolve_existing_base(path_str)
        for protected in get_protected_roots():
            if path == protected or _path_is_relative_to(path, protected):
                return True
        return False
    except Exception:
        return False


def default_archive_name_for_path(path_str: str) -> str:
    source = Path(path_str).resolve()
    if source == Path(source.anchor):
        return 'root_backup.ms'
    return f'{source.name}.ms'


def pick_archive_from_current_directory() -> Path:
    archives = sorted(Path.cwd().glob('*.ms'))
    if not archives:
        raise FileNotFoundError("В текущей папке не найдено ни одного .ms архива")
    if len(archives) > 1:
        names = ', '.join(archive.name for archive in archives)
        raise RuntimeError(
            "В текущей папке найдено несколько .ms архивов. "
            f"Укажите файл явно: {names}"
        )
    return archives[0]


def print_protected_path_error(source_path: str):
    print("Ошибка: архивирование этого пути запрещено.")
    print()
    print(f"Путь: {Path(source_path).resolve()}")
    print("Защита от работы с системными папками Windows.")
    print()
    print("Защищённые пути включают:")
    print("   - C:\\Windows\\*")
    print("   - C:\\Windows\\System32\\*")
    print("   - C:\\Program Files\\*")
    print("   - C:\\ProgramData\\*")
    print("   - Другие системные каталоги")
    print()
    print("Совет: запускайте UMSFA из пользовательских папок:")
    print("   - C:\\Users\\YourName\\Documents\\*")
    print("   - C:\\Users\\YourName\\Desktop\\*")
    print("   - D:\\Projects\\*")


def add_compression_arguments(parser):
    parser.add_argument(
        '-comp',
        '--compress',
        action='store_true',
        help=f'Включить gzip-сжатие при создании архива; по умолчанию уровень {DEFAULT_COMPRESSION_LEVEL}'
    )
    for level in range(1, 10):
        parser.add_argument(
            f'-comp{level}',
            dest='compression_level',
            action='store_const',
            const=level,
            help=f'Включить gzip-сжатие с уровнем {level}'
        )


def resolve_compression_settings(args):
    compression_level = getattr(args, 'compression_level', None)
    use_compression = bool(args.compress or compression_level is not None)
    if not use_compression:
        return False, DEFAULT_COMPRESSION_LEVEL
    return True, compression_level or DEFAULT_COMPRESSION_LEVEL


def main():
    parser = argparse.ArgumentParser(
        description='Universal MS Format Archiver - Архиватор с AES-256 шифрованием',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:

  # Архивирование без пароля
  python main.py create /path/to/folder output.ms

  # Архивирование с паролем
  python main.py create /path/to/folder output.ms -p "mypassword"

  # Архивирование со сжатием и паролем
  python main.py create /path/to/folder output.ms -comp -p "mypassword"

  # Архивирование с максимальным уровнем сжатия
  python main.py create /path/to/folder output.ms -comp9 -p "mypassword"

  # Интерактивный ввод пароля
  python main.py create /path/to/folder output.ms -i

  # Архивирование текущей папки с именем по умолчанию
  python main.py create -p "mypassword"

  # Распаковка архива
  python main.py extract output.ms /path/to/extract -p "mypassword"

  # Распаковка единственного .ms архива из текущей папки
  python main.py extract -p "mypassword"

  # Информация об архиве
  python main.py info output.ms
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Команда')
    
    # Команда архивирования
    create_parser = subparsers.add_parser('create', aliases=['c'], help='Создать архив')
    create_parser.add_argument('source', nargs='?', default='.', help='Путь к файлу или папке; по умолчанию текущая папка')
    create_parser.add_argument('output', nargs='?', help='Путь к выходному .ms файлу; по умолчанию <текущая_папка>.ms')
    add_compression_arguments(create_parser)
    create_parser.add_argument('-p', '--password', help='Пароль для шифрования')
    create_parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный ввод пароля')
    
    # Команда распаковки
    extract_parser = subparsers.add_parser('extract', aliases=['x', 'e'], help='Распаковать архив')
    extract_parser.add_argument('archive', nargs='?', help='Путь к .ms архиву; по умолчанию единственный .ms файл в текущей папке')
    extract_parser.add_argument('output', nargs='?', help='Директория для распаковки; по умолчанию <имя_архива>')
    extract_parser.add_argument('-p', '--password', help='Пароль для расшифровки')
    extract_parser.add_argument('-i', '--interactive', action='store_true', help='Интерактивный ввод пароля')
    
    # Команда информации
    info_parser = subparsers.add_parser('info', aliases=['i'], help='Информация об архиве')
    info_parser.add_argument('archive', help='Путь к .ms архиву')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Обработка команды архивирования
    if args.command in ('create', 'c'):
        source_path = args.source
        output_path = args.output or default_archive_name_for_path(source_path)

        # Проверка защиты системных папок
        if is_protected_path(source_path):
            print_protected_path_error(source_path)
            return

        password = None

        if args.interactive:
            password = getpass("Введите пароль: ")
            confirm = getpass("Подтвердите пароль: ")
            if password != confirm:
                print("Ошибка: пароли не совпадают.")
                return
        elif args.password:
            password = args.password

        use_compression, compression_level = resolve_compression_settings(args)
        archiver = MSArchiver(
            password=password,
            use_compression=use_compression,
            compression_level=compression_level
        )
        success = archiver.archive(source_path, output_path)
        
        if not success:
            sys.exit(1)
    
    # Обработка команды распаковки
    elif args.command in ('extract', 'x', 'e'):
        try:
            archive_path = args.archive or str(pick_archive_from_current_directory())
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"Ошибка: {exc}")
            sys.exit(1)

        password = None

        if args.interactive:
            password = getpass("Введите пароль для распаковки: ")
        elif args.password:
            password = args.password

        output_path = args.output or Path(archive_path).stem
        archiver = MSArchiver(password=password)
        success = archiver.extract(archive_path, str(output_path))
        
        if not success:
            sys.exit(1)
    
    # Обработка команды информации
    elif args.command in ('info', 'i'):
        archiver = MSArchiver()
        info = archiver.get_archive_info(args.archive)
        
        if info is None:
            print("Ошибка: некорректный файл архива.")
            sys.exit(1)
        
        print("\nИнформация об архиве:")
        print(f"   Имя источника: {info['source_name']}")
        print(f"   Тип: {info['source_type']}")
        print(f"   Размер (сжато): {info['original_size'] / 1024 / 1024:.2f} МБ")
        if info.get('compressed', True):
            level = info.get('compression_level')
            level_suffix = f", уровень {level}" if level else ""
            print(f"   Сжатие: Да (gzip{level_suffix})")
        else:
            print("   Сжатие: Нет")
        print(f"   Зашифрован: {'Да (AES-256)' if info['encrypted'] else 'Нет'}")
        print()


if __name__ == '__main__':
    main()
