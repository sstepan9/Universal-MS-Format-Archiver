# 🚀 UMSFA v1.1 — Готово! Инструкции по использованию PATH

## ⚡ Первые шаги (5 минут)

### Для нетерпеливых: Базовые команды

После добавления в PATH:

```powershell
# Архивировать текущую папку
umsfa create . backup.ms -p "password123"

# Распаковать
umsfa extract backup.ms restored -p "password123"

# Информация об архиве
umsfa info backup.ms
```

---

## 📌 Установка PATH (3 шага)

### 1. Откройте PowerShell от имени администратора

Нажмите `Win + X` → выберите "Windows PowerShell (администратор)"

### 2. Перейдите в папку UMSFA

```powershell
cd C:\Users\sstep\Downloads\UMSFA
```

### 3. Запустите установку

```powershell
python setup_path.py --add
```

Вы должны увидеть:
```
✅ UMSFA успешно добавлен в PATH
   Путь: C:\Users\sstep\Downloads\UMSFA

⚠️ Требуется перезагрузка или перезагрузка переменных окружения:
   1. Закройте текущую командную строку/PowerShell
   2. Откройте новую командную строку/PowerShell
   3. Введите: umsfa --help
```

### 4. Закройте PowerShell и откройте новое окно

### 5. Проверьте

```powershell
umsfa --help
```

---

## 🎯 Первые команды

### Создание архива

```powershell
# Архивировать папку с паролем
umsfa create "C:\Users\User\Documents" backup.ms -p "MySecurePassword123!"

# Архивировать текущую папку
cd "C:\My Project"
umsfa create . project.ms -p "pass123"

# Архивировать без пароля
umsfa create "C:\Users\User\Desktop" desktop.ms
```

### Распаковка

```powershell
# Распаковать архив
umsfa extract backup.ms restored_folder -p "MySecurePassword123!"

# Распаковать в текущую папку
umsfa extract backup.ms . -p "pass123"
```

### Информация об архиве

```powershell
# Посмотреть информацию
umsfa info backup.ms
```

---

## 📖 Документация

### 🔥 Начните отсюда!

| Документ | Содержание |
|----------|-----------|
| **WHATS_NEW.md** | ✨ Что нового в v1.1 (PATH Support) |
| **QUICK_START.md** | ⚡ Быстрый старт за 5 минут |
| **INSTALLATION.md** | 🔧 Подробная инструкция по установке |

### 📚 Дополнительно

| Документ | Содержание |
|----------|-----------|
| **PATH_USAGE.md** | 🚀 Практические примеры использования из PATH |
| **README.md** | 📖 Основная документация |
| **TECHNICAL.md** | 🔬 Техническая документация |
| **INDEX.md** | 🗺️ Полная навигация по документам |

---

## 🛡️ Защита системных папок

### ✅ Работает

```powershell
umsfa create "C:\Users\User\Documents" backup.ms -p "pass"     # ✅
umsfa create "D:\Projects" backup.ms -p "pass"                  # ✅
umsfa create "C:\Users\User\Desktop" backup.ms -p "pass"        # ✅
```

### ❌ Не работает (защита)

```powershell
umsfa create "C:\Windows" backup.ms -p "pass"                   # ❌
umsfa create "C:\Program Files" backup.ms -p "pass"             # ❌
umsfa create "C:\ProgramData" backup.ms -p "pass"               # ❌
```

**Результат:**
```
❌ Ошибка: Архивирование этого пути запрещено!

🔒 Защита от случайного удаления системных файлов

Защищённые пути:
   - C:\Windows\*
   - C:\Program Files\*
   - C:\ProgramData\*
   - Системные папки Windows
```

---

## 🎓 Практические примеры

### Пример 1: Резервная копия документов

```powershell
cd "C:\Users\User\Documents"

# Архивировать текущую папку
umsfa create . "docs_backup_$(Get-Date -Format 'yyyy-MM-dd').ms" -p "MyPassword"

# Результат: docs_backup_2026-04-29.ms
```

### Пример 2: Архивирование проекта

```powershell
cd "D:\MyProject"

# Архивировать всё
umsfa create . "backup.ms" -i

# Система запросит пароль и подтверждение
```

### Пример 3: Быстрая проверка

```powershell
# Создать, проверить и распаковать
umsfa create "C:\Users\User\Documents" test.ms -p "pass"
umsfa info test.ms
umsfa extract test.ms test_extract -p "pass"
```

### Пример 4: Массовое архивирование

```powershell
# Архивировать несколько папок
$folders = @(
    "C:\Users\User\Documents",
    "C:\Users\User\Desktop",
    "C:\Users\User\Pictures"
)

foreach ($folder in $folders) {
    $name = Split-Path $folder -Leaf
    Write-Host "Архивирование: $name"
    umsfa create "$folder" "$name.ms" -p "password"
}
```

---

## ❓ Часто задаваемые вопросы

### Q: Как проверить что UMSFA установлен?

```powershell
umsfa --help
```

### Q: Какой пароль использовать?

**Рекомендация:** Используйте сложные пароли:
- `MyP@ssw0rd!2024!` ✅ Хорошо
- `password123` ❌ Слабо

### Q: Что если я забыл пароль?

К сожалению, архив будет недоступен. Пароли невозможно восстановить.  
**Совет:** Храните пароли в менеджере паролей (KeePass, LastPass и т.д.)

### Q: Могу ли я удалить исходные файлы после архивирования?

Да, но сначала проверьте архив:
```powershell
umsfa info backup.ms
umsfa extract backup.ms test -p "pass"
# Если всё ОК, удаляйте исходные файлы
```

### Q: Как архивировать текущую папку?

Используйте точку (`.`) вместо пути:
```powershell
cd "C:\My Folder"
umsfa create . backup.ms -p "pass"
```

### Q: Что если UMSFA не находится?

Перезагрузите PowerShell:
1. Закройте текущее окно
2. Откройте новое окно PowerShell
3. Попробуйте заново: `umsfa --help`

---

## 🔧 Управление PATH

### Проверить статус

```powershell
python setup_path.py --check
```

### Удалить из PATH

```powershell
# От имени администратора
cd C:\Users\sstep\Downloads\UMSFA
python setup_path.py --remove
```

### Переустановить

```powershell
# От имени администратора
cd C:\Users\sstep\Downloads\UMSFA
python setup_path.py --remove
python setup_path.py --add
```

---

## 📊 Быстрый тест

Выполните этот тест для проверки функциональности:

```powershell
# 1. Создайте тестовую папку
mkdir test_umsfa_demo
echo "Hello World" > test_umsfa_demo\test.txt

# 2. Архивируйте её
umsfa create test_umsfa_demo demo.ms -p "test123"

# 3. Посмотрите информацию
umsfa info demo.ms

# 4. Распакуйте
umsfa extract demo.ms demo_restored -p "test123"

# 5. Проверьте результат
cat demo_restored\test_umsfa_demo\test.txt

# Если увидели "Hello World", всё работает! ✅

# 6. Очистите
Remove-Item test_umsfa_demo -Recurse
Remove-Item demo_restored -Recurse
Remove-Item demo.ms
```

---

## 🆘 Решение проблем

### Problem: "The term 'umsfa' is not recognized"

**Причина:** PATH не был обновлён

**Решение:**
```powershell
# Закройте PowerShell полностью
# Откройте новое окно PowerShell
# Попробуйте: umsfa --help
```

### Problem: "PermissionError: требуются права администратора"

**Причина:** Запустили без прав администратора

**Решение:**
- Нажмите `Win + X` → "Windows PowerShell (администратор)"

### Problem: "python: The term 'python' is not recognized"

**Причина:** Python не в PATH

**Решение:**
- Переустановите Python с отметкой "Add Python to PATH"

### Problem: "Архивирование этого пути запрещено!"

**Причина:** Попытка архивировать системную папку

**Решение:**
```powershell
# Архивируйте пользовательские папки:
umsfa create "C:\Users\YourName\Documents" backup.ms -p "pass"

# Не системные:
umsfa create "C:\Windows" backup.ms  # ❌ Запрещено
```

---

## 📞 Справка и помощь

### Общая справка

```powershell
umsfa --help
```

### Справка по команде

```powershell
umsfa create --help
umsfa extract --help
umsfa info --help
```

### Посмотрите документацию

- [INSTALLATION.md](INSTALLATION.md) — Подробная установка
- [PATH_USAGE.md](PATH_USAGE.md) — Примеры использования
- [README.md](README.md) — Основная документация

---

## ✅ Финальный чек-лист

- [ ] PowerShell открыт от имени администратора
- [ ] Я в папке `C:\Users\sstep\Downloads\UMSFA`
- [ ] Я выполнил: `python setup_path.py --add`
- [ ] Я перезагрузил PowerShell
- [ ] Команда `umsfa --help` работает
- [ ] Я протестировал архивирование: `umsfa create . test.ms -p "pass"`
- [ ] Я распаковал архив: `umsfa extract test.ms restored -p "pass"`

---

## 🎉 Готово!

После этого UMSFA полностью готов к использованию!

**Теперь вы можете:**
- ✅ Архивировать папки из любого места
- ✅ Защищать данные AES-256 шифрованием
- ✅ Создавать резервные копии быстро
- ✅ Безопасно передавать файлы

---

## 📚 Полезные ссылки

| Документ | Назначение |
|----------|-----------|
| [WHATS_NEW.md](WHATS_NEW.md) | Что нового в v1.1 |
| [QUICK_START.md](QUICK_START.md) | Быстрый старт |
| [INSTALLATION.md](INSTALLATION.md) | Установка на Windows/Linux/macOS |
| [PATH_USAGE.md](PATH_USAGE.md) | Практические примеры |
| [README.md](README.md) | Основная документация |
| [TECHNICAL.md](TECHNICAL.md) | Техническое описание |
| [INDEX.md](INDEX.md) | Навигация по документам |

---

**Версия:** UMSFA v1.1  
**Дата:** 29.04.2026  
**Статус:** ✅ Полностью готово!

---

## 🚀 Начните прямо сейчас!

```powershell
# Шаг 1: Откройте PowerShell администратором
# (Win + X → Windows PowerShell (администратор))

# Шаг 2: Выполните
cd C:\Users\sstep\Downloads\UMSFA
python setup_path.py --add

# Шаг 3: Закройте PowerShell и откройте новый

# Шаг 4: Используйте
umsfa create my_folder backup.ms -p "password123"
```

**Готово! Теперь UMSFA работает из любого места! 🎉**
