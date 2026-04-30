# Universal MS Format Archiver (UMSFA) 🗂️

Мощный локальный архиватор с поддержкой AES-256 шифрования для архивирования папок и файлов в новый формат `.ms`.

## 🎯 Возможности

- ✅ **Архивирование папок и файлов** в формат `.ms`
- 🔐 **AES-256 шифрование** для защиты данных
- 🔑 **Защита паролем** с использованием PBKDF2
- 📦 **Опциональное gzip-сжатие** по флагу `-comp`
- 💾 **Метаданные** о структуре архива
- 📊 **Информация об архиве** без распаковки
- 🖥️ **Удобный CLI интерфейс**

## 📦 Установка

### Требования
- Python 3.7+
- pip

### Подготовка

```bash
cd UMSFA
pip install -r requirements.txt
```

## 🚀 Использование

### Архивирование без пароля

```bash
python main.py create /path/to/folder output.ms
```

### Архивирование с паролем

```bash
python main.py create /path/to/folder output.ms -p "mypassword"
```

### Архивирование со сжатием

```bash
python main.py create /path/to/folder output.ms -comp -p "mypassword"
```

### Архивирование с уровнем сжатия

```bash
python main.py create /path/to/folder output.ms -comp1 -p "mypassword"  # быстрее
python main.py create /path/to/folder output.ms -comp9 -p "mypassword"  # сильнее сжимает
```

### Интерактивный ввод пароля

```bash
python main.py create /path/to/folder output.ms -i
```

### Распаковка архива

```bash
python main.py extract output.ms /path/to/extract -p "mypassword"
```

### Информация об архиве

```bash
python main.py info output.ms
```

### ⚡ Использование из PATH (Windows)

После добавления UMSFA в PATH вы можете вызывать его из любого места:

```powershell
# Архивировать текущую папку; имя архива будет project.ms
umsfa create -p "password"

# Архивировать текущую папку с явным именем архива
umsfa create . backup.ms -p "password"

# Архивировать с абсолютным путём
umsfa create "C:\Users\User\Documents" docs.ms -p "password"

# Распаковать единственный .ms архив из текущей папки
umsfa extract -p "password"

# Распаковать с явным путём
umsfa extract backup.ms restored -p "password"

# Информация
umsfa info backup.ms
```

**Для установки в PATH:** см. [INSTALLATION.md](INSTALLATION.md)

## 🏗️ Архитектура .ms формата

```
[MAGIC: 8 байт]              # "UMSFA1.0"
[METADATA_SIZE: 4 байта]     # Размер JSON метаданных
[METADATA: JSON]             # Информация об архиве
[ENCRYPTED_TAR_DATA]         # Шифрованные данные tar.gz
```

### Метаданные

```json
{
  "source_name": "folder_name",
  "source_type": "directory",
  "original_size": 1048576,
  "encrypted": true,
  "salt": "hex_string",
  "iv": "hex_string"
}
```

## 🔐 Безопасность

- **Алгоритм шифрования:** AES-256-CBC
- **Функция получения ключа:** PBKDF2 (SHA-256, 100000 итераций)
- **Размер соли:** 16 байт (128 бит)
- **Размер IV:** 16 байт (128 бит)
- **Padding:** PKCS7

### 🛡️ Защита системных папок

UMSFA имеет встроенную защиту от архивирования системных папок Windows:

```
❌ НЕЛЬЗЯ архивировать:
  - C:\Windows\*
  - C:\Program Files\*
  - C:\ProgramData\*
  - System Volume Information\
  - $Recycle.Bin\
  
✅ МОЖНО архивировать:
  - C:\Users\YourName\Documents\*
  - C:\Users\YourName\Desktop\*
  - D:\Projects\*
  - E:\Data\*
```

Эта защита предотвращает случайное повреждение системы.

## 📝 Примеры кода

### Использование в Python коде

```python
from umsfa import MSArchiver

# Архивирование
archiver = MSArchiver(password="secure_password")
archiver.archive("my_folder", "my_archive.ms")

# Распаковка
archiver.extract("my_archive.ms", "extracted_folder")

# Информация
info = archiver.get_archive_info("my_archive.ms")
print(f"Размер: {info['original_size']} байт")
print(f"Зашифрован: {info['encrypted']}")
```

## 🎓 Структура проекта

```
UMSFA/
├── umsfa.py          # Основная логика архиватора
├── main.py           # CLI интерфейс
├── requirements.txt  # Зависимости
└── README.md         # Документация
```

## 📊 Производительность

- Поддержка больших файлов (тестировано до 10 ГБ)
- Gzip-сжатие по флагу `-comp`
- Потоковое шифрование для экономии памяти

## 🔧 Настройка параметров шифрования

Все параметры находятся в классе `MSArchiver`:

```python
SALT_SIZE = 16              # Размер соли (байт)
IV_SIZE = 16                # Размер инициализирующего вектора
KEY_SIZE = 32               # Размер ключа AES-256
ITERATIONS = 100000         # Итерации PBKDF2
```

## ⚠️ Важные замечания

1. **Потеря пароля = потеря данных** - убедитесь, что помните пароль
2. **Совместимость:** Используйте одну версию UMSFA для архивирования и распаковки
3. **Производительность:** На слабых машинах расшифровка может занять время

## 📄 Лицензия

MIT

## 👤 Автор

Создано с помощью GitHub Copilot

---

**Версия:** 1.0  
**Последнее обновление:** 2026-04-29
