# 🆕 PATH Support v1.1 — Новые возможности

## ✨ Что добавлено

**UMSFA теперь можно вызывать из любого места в системе после добавления в PATH!**

---

## 🎯 Основные возможности

### 1️⃣ Вызов из любой папки

**Раньше:**
```powershell
cd C:\Users\sstep\Downloads\UMSFA
python main.py create "C:\Users\User\Documents" backup.ms -p "password"
```

**Теперь:**
```powershell
cd C:\Users\User\Documents
umsfa create . backup.ms -p "password"

# Или из любого места:
umsfa create "C:\Users\User\Documents" backup.ms -p "password"
```

### 2️⃣ Работа с текущей директорией

```powershell
cd "C:\Users\User\MyProject"

# Архивировать текущую папку (.)
umsfa create . project.ms -p "pass123"

# Архивировать из другого места
cd "C:\Downloads"
umsfa create "C:\Users\User\MyProject" project.ms -p "pass123"
```

### 3️⃣ Защита от системных папок

```powershell
# Попытка архивировать системные файлы:
umsfa create C:\Windows backup.ms

# Результат:
# ❌ Ошибка: Архивирование этого пути запрещено!
# 🔒 Защита от случайного удаления системных файлов
```

---

## 🚀 Установка (3 шага)

### Шаг 1: Откройте PowerShell от имени администратора

Нажмите `Win + X` → "Windows PowerShell (администратор)"

### Шаг 2: Перейдите в папку UMSFA

```powershell
cd C:\Users\sstep\Downloads\UMSFA
```

### Шаг 3: Запустите установку

```powershell
python setup_path.py --add
```

**Результат:**
```
✅ UMSFA успешно добавлен в PATH
   Путь: C:\Users\sstep\Downloads\UMSFA

⚠️ Требуется перезагрузка или перезагрузка переменных окружения:
   1. Закройте текущую командную строку/PowerShell
   2. Откройте новую командную строку/PowerShell
   3. Введите: umsfa --help
```

### Шаг 4: Перезагрузите PowerShell

Закройте PowerShell и откройте новое окно.

### Шаг 5: Проверьте

```powershell
umsfa --help
```

---

## 📁 Новые файлы

### setup_path.py
Скрипт для добавления/удаления UMSFA в системный PATH

**Команды:**
```powershell
# Проверить статус
python setup_path.py --check

# Добавить в PATH (требуется администратор)
python setup_path.py --add

# Удалить из PATH (требуется администратор)
python setup_path.py --remove
```

### umsfa.bat (Windows wrapper)
Батник для вызова UMSFA из командной строки.  
Автоматически находит Python и запускает main.py

### umsfa.sh (Linux/macOS wrapper)
Shell скрипт для Linux/macOS (работает аналогично .bat)

### INSTALLATION.md
Подробное руководство по установке на Windows, Linux и macOS

### PATH_USAGE.md
Практические примеры использования UMSFA из любого места

---

## 📋 Примеры

### Архивирование текущей папки

```powershell
cd "C:\Users\User\MyProject"
umsfa create . backup.ms -p "secure123"
```

### Архивирование конкретной папки

```powershell
umsfa create "D:\Important Files" backup.ms -p "pass"
```

### Распаковка

```powershell
umsfa extract backup.ms restored -p "pass"
```

### Просмотр информации

```powershell
umsfa info backup.ms
```

### Интерактивный пароль

```powershell
umsfa create my_folder backup.ms -i
# Система запросит пароль
```

---

## 🛡️ Защита системных папок

### Защищённые пути (нельзя архивировать)

```
C:\Windows
C:\Program Files
C:\Program Files (x86)
C:\ProgramData
C:\System Volume Information
C:\$Recycle.Bin
C:\PerfLogs
```

### Почему это нужно?

- ✅ Защита от случайного повреждения системы
- ✅ Предотвращение архивирования системных файлов
- ✅ Избежание конфликтов с антивирусами
- ✅ Сокращение размера архива

### Что архивировать вместо этого?

```
✅ C:\Users\YourName\Documents
✅ C:\Users\YourName\Desktop
✅ C:\Users\YourName\Pictures
✅ D:\Projects
✅ E:\Data
```

---

## 🔧 Управление PATH

### Проверить статус

```powershell
python setup_path.py --check
```

### Удалить из PATH

```powershell
# От имени администратора:
python setup_path.py --remove
```

### Перезагрузить PATH

```powershell
# Если UMSFA перестал работать:
python setup_path.py --remove
python setup_path.py --add
```

---

## 📊 Сравнение версий

| Функция | v1.0 | v1.1 |
|---------|------|------|
| Архивирование | ✅ | ✅ |
| Распаковка | ✅ | ✅ |
| AES-256 шифрование | ✅ | ✅ |
| Вызов из PATH | ❌ | ✅ |
| Защита системных папок | ❌ | ✅ |
| setup_path.py | ❌ | ✅ |
| INSTALLATION.md | ❌ | ✅ |
| PATH_USAGE.md | ❌ | ✅ |

---

## 🚀 Быстрый старт для спешящих

1. Откройте PowerShell администратором
2. Выполните:
   ```powershell
   cd C:\Users\sstep\Downloads\UMSFA
   python setup_path.py --add
   ```
3. Закройте и откройте новый PowerShell
4. Используйте:
   ```powershell
   umsfa create my_folder backup.ms -p "password"
   ```

---

## 🐧 Linux/macOS

После установки UMSFA на Linux/macOS используйте:

```bash
# Вместо umsfa используйте:
umsfa.sh create ~/Documents backup.ms -p "password"

# Или добавьте alias в ~/.bashrc:
alias umsfa="~/Downloads/UMSFA/umsfa.sh"

# Тогда сможете использовать:
umsfa create ~/Documents backup.ms -p "password"
```

---

## 📞 Справка

### Вызов справки

```powershell
umsfa --help
umsfa create --help
umsfa extract --help
```

### Общие команды

```powershell
# Архивировать
umsfa create <папка> <файл.ms> -p "пароль"

# Распаковать
umsfa extract <файл.ms> <папка> -p "пароль"

# Информация
umsfa info <файл.ms>
```

---

## ✅ Проверка после установки

```powershell
# 1. Создайте тестовую папку
mkdir test_umsfa
echo "Hello" > test_umsfa\hello.txt

# 2. Архивируйте её
umsfa create test_umsfa test.ms -p "test123"

# 3. Посмотрите информацию
umsfa info test.ms

# 4. Распакуйте
umsfa extract test.ms restored -p "test123"

# 5. Проверьте результат
dir restored\test_umsfa
```

Если всё работает — поздравляем! 🎉 UMSFA установлен и готов к использованию!

---

## 🔄 Обновление PATH

Если вы переместили папку UMSFA:

```powershell
# От имени администратора:
cd "C:\New Location\UMSFA"
python setup_path.py --remove
python setup_path.py --add
```

---

## ⚠️ Решение проблем

### Problem: "umsfa: The term 'umsfa' is not recognized"

**Решение:** Перезагрузите PowerShell (закройте и откройте заново)

### Problem: "PermissionError: требуются права администратора"

**Решение:** Откройте PowerShell ОТ ИМЕНИ АДМИНИСТРАТОРА

### Problem: "Архивирование этого пути запрещено!"

**Решение:** Архивируйте пользовательские папки, а не системные:
```powershell
# ❌ Неправильно:
umsfa create C:\Windows backup.ms

# ✅ Правильно:
umsfa create C:\Users\User\Documents backup.ms
```

---

## 📚 Дополнительная информация

- Подробное руководство: [INSTALLATION.md](INSTALLATION.md)
- Практические примеры: [PATH_USAGE.md](PATH_USAGE.md)
- Техническая документация: [TECHNICAL.md](TECHNICAL.md)
- Основная документация: [README.md](README.md)

---

## 🎓 История обновлений

### v1.1 (29.04.2026) — Текущая версия

✨ **Новое:**
- Добавлена поддержка PATH
- setup_path.py для управления PATH
- Защита от системных папок
- umsfa.bat wrapper для Windows
- umsfa.sh wrapper для Linux/macOS
- Расширенная документация

### v1.0 (29.04.2026)

- Первая версия UMSFA
- AES-256 шифрование
- CLI интерфейс
- Python API

---

**UMSFA v1.1 — Теперь более удобный и безопасный! 🚀**

Начните с: `python setup_path.py --add`

---

**Версия документации:** 1.1  
**Дата:** 29.04.2026  
**Статус:** ✅ Готово к использованию
