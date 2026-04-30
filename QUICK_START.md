# 🚀 Быстрый старт UMSFA

## Установка за 3 шага

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Создание первого архива
```bash
# Без пароля
python main.py create my_folder my_archive.ms

# С паролем
python main.py create my_folder my_archive.ms -p "MyPassword123"
```

### 3. Распаковка архива
```bash
python main.py extract my_archive.ms extracted_folder -p "MyPassword123"
```

---

## 📚 Основные команды

### 📦 Архивирование

**Синтаксис:**
```bash
python main.py create <путь_папки> <выход.ms> [опции]
```

**Опции:**
- `-p, --password TEXT` — Пароль для шифрования
- `-i, --interactive` — Интерактивный ввод пароля

**Примеры:**
```bash
# Простое архивирование
python main.py create Documents documents.ms

# С паролем
python main.py create Documents documents.ms -p "secret123"

# Интерактивный ввод
python main.py create Documents documents.ms -i
```

### 📂 Распаковка

**Синтаксис:**
```bash
python main.py extract <архив.ms> <выходная_папка> [опции]
```

**Опции:**
- `-p, --password TEXT` — Пароль для расшифровки
- `-i, --interactive` — Интерактивный ввод пароля

**Примеры:**
```bash
# Распаковка без пароля
python main.py extract documents.ms extracted_docs

# С паролем
python main.py extract documents.ms extracted_docs -p "secret123"
```

### 📋 Информация об архиве

**Синтаксис:**
```bash
python main.py info <архив.ms>
```

**Пример:**
```bash
python main.py info documents.ms
```

**Вывод:**
```
📋 Информация об архиве:
   Имя источника: Documents
   Тип: directory
   Размер (сжато): 5.23 МБ
   Зашифрован: ✅ Да (AES-256)
```

---

## 💻 Использование в Python коде

```python
from umsfa import MSArchiver

# Создание объекта архиватора с паролем
archiver = MSArchiver(password="MyPassword123")

# Архивирование папки
archiver.archive("my_folder", "backup.ms")

# Распаковка
archiver.extract("backup.ms", "restored_folder")

# Получение информации
info = archiver.get_archive_info("backup.ms")
print(f"Зашифрован: {info['encrypted']}")
```

---

## 🔐 Безопасность

| Параметр | Значение |
|----------|----------|
| Алгоритм шифрования | AES-256-CBC |
| Функция ключа | PBKDF2 (SHA-256) |
| Итерации PBKDF2 | 100,000 |
| Размер соли | 16 байт (128 бит) |
| Размер IV | 16 байт (128 бит) |
| Padding | PKCS7 |

---

## ❓ Часто задаваемые вопросы

### Q: Потеря пароля = потеря данных?
**A:** Да. Если вы забудете пароль, восстановить данные не будет возможно. Используйте надежный пароль и храните его в безопасном месте.

### Q: Какой размер файла поддерживается?
**A:** UMSFA поддерживает файлы до 2 ТБ (в зависимости от свободного места на диске).

### Q: Можно ли распаковать .ms архив на другой машине?
**A:** Да, .ms архивы совместимы между машинами с Python 3.7+ и установленными зависимостями.

### Q: Как создать архив интерактивно?
**A:** Используйте флаг `-i`:
```bash
python main.py create my_folder backup.ms -i
```

### Q: Почему распаковка выдает ошибку "not a gzip file"?
**A:** Это означает, что пароль неверный. При расшифровке с неверным ключом получается случайный набор байт.

---

## 🛠️ Примеры реальных сценариев

### Сценарий 1: Резервное копирование конфиденциальных документов
```bash
python main.py create "C:\Users\User\Documents" backup_docs.ms -p "VerySecurePassword123!"
```

### Сценарий 2: Отправка зашифрованной папки коллеге
```bash
python main.py create "project_files" project.ms -p "ProjectPassword123"
# Отправить project.ms по защищённому каналу
# Коллега распаковывает:
python main.py extract project.ms extracted_project -p "ProjectPassword123"
```

### Сценарий 3: Архивирование и хранение в облаке
```bash
# Архивирование с сильным паролем
python main.py create sensitive_data backup.ms -i

# Загрузить backup.ms на облако (Google Drive, OneDrive и т.д.)
# Данные защищены шифрованием AES-256
```

---

## 📞 Поддержка

Для вопросов или проблем обратитесь к документации в `README.md`.

---

**UMSFA v1.0** — Universal MS Format Archiver  
Создано с помощью GitHub Copilot
