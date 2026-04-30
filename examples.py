"""
Примеры использования Universal MS Format Archiver (UMSFA)

Этот файл содержит примеры кода для архивирования и распаковки
данных с использованием криптографии AES-256.
"""

from umsfa import MSArchiver
import os

# ============================================================================
# Пример 1: Простое архивирование без пароля
# ============================================================================
print("=" * 60)
print("Пример 1: Архивирование без пароля")
print("=" * 60)

archiver_no_pass = MSArchiver()
archiver_no_pass.archive('test_folder', 'my_archive_simple.ms')
print()

# ============================================================================
# Пример 2: Архивирование с защитой паролем
# ============================================================================
print("=" * 60)
print("Пример 2: Архивирование с паролем (AES-256)")
print("=" * 60)

archiver_encrypted = MSArchiver(password="MySecurePassword123!")
archiver_encrypted.archive('test_folder', 'my_archive_encrypted.ms')
print()

# ============================================================================
# Пример 3: Получение информации об архиве
# ============================================================================
print("=" * 60)
print("Пример 3: Информация об архивах")
print("=" * 60)

archiver = MSArchiver()

info1 = archiver.get_archive_info('my_archive_simple.ms')
if info1:
    print("Архив без пароля:")
    for key, value in info1.items():
        if key not in ('salt', 'iv'):  # Скрываем техническую информацию
            print(f"  {key}: {value}")
    print()

info2 = archiver.get_archive_info('my_archive_encrypted.ms')
if info2:
    print("Архив с паролем:")
    for key, value in info2.items():
        if key not in ('salt', 'iv'):
            print(f"  {key}: {value}")
    print()

# ============================================================================
# Пример 4: Распаковка с проверкой пароля
# ============================================================================
print("=" * 60)
print("Пример 4: Распаковка зашифрованного архива")
print("=" * 60)

archiver_decrypt = MSArchiver(password="MySecurePassword123!")
archiver_decrypt.extract('my_archive_encrypted.ms', 'extracted_with_password')
print()

# ============================================================================
# Пример 5: Интеграция в приложение
# ============================================================================
print("=" * 60)
print("Пример 5: Использование в приложении")
print("=" * 60)

def backup_folder(folder_path, output_file, password=None):
    """
    Функция резервного копирования папки
    
    Args:
        folder_path: Путь к папке
        output_file: Путь к выходному файлу .ms
        password: Пароль для шифрования (опционально)
    
    Returns:
        bool: True если успешно, False иначе
    """
    try:
        if not os.path.exists(folder_path):
            print(f"❌ Папка {folder_path} не найдена")
            return False
        
        archiver = MSArchiver(password=password)
        success = archiver.archive(folder_path, output_file)
        
        if success:
            size = os.path.getsize(output_file) / 1024 / 1024
            print(f"✅ Резервная копия создана: {output_file} ({size:.2f} МБ)")
        
        return success
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def restore_from_backup(backup_file, output_dir, password=None):
    """
    Функция восстановления из резервной копии
    
    Args:
        backup_file: Путь к архиву .ms
        output_dir: Директория для восстановления
        password: Пароль для расшифровки
    
    Returns:
        bool: True если успешно, False иначе
    """
    try:
        if not os.path.exists(backup_file):
            print(f"❌ Архив {backup_file} не найден")
            return False
        
        archiver = MSArchiver(password=password)
        success = archiver.extract(backup_file, output_dir)
        
        if success:
            print(f"✅ Восстановление завершено в: {output_dir}")
        
        return success
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


# Использование функций
print("\nСоздание резервной копии...")
backup_folder('test_folder', 'backup_example.ms', password='SecurePass123!')

print("\nВосстановление из резервной копии...")
restore_from_backup('backup_example.ms', 'restored_folder', password='SecurePass123!')

# ============================================================================
# Пример 6: Обработка ошибок
# ============================================================================
print("\n" + "=" * 60)
print("Пример 6: Обработка ошибок")
print("=" * 60)

archiver_error = MSArchiver(password="WrongPassword")

# Попытка распаковать с неверным паролем
print("\nПопытка распаковать архив с неверным паролем...")
success = archiver_error.extract('my_archive_encrypted.ms', 'wrong_extract')

if not success:
    print("⚠️ Распаковка не удалась (как и ожидалось)")

# ============================================================================
# Пример 7: Архивирование отдельного файла
# ============================================================================
print("\n" + "=" * 60)
print("Пример 7: Архивирование отдельного файла")
print("=" * 60)

# Создание тестового файла
with open('single_file.txt', 'w') as f:
    f.write("Это тестовый файл для архивирования\n")

archiver_file = MSArchiver(password="FilePassword123")
archiver_file.archive('single_file.txt', 'single_file_archive.ms')

print("\nИнформация о файловом архиве:")
info = archiver_file.get_archive_info('single_file_archive.ms')
if info:
    for key, value in info.items():
        if key not in ('salt', 'iv'):
            print(f"  {key}: {value}")

print("\n" + "=" * 60)
print("✅ Все примеры выполнены успешно!")
print("=" * 60)
