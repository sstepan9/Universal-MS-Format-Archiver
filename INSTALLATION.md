# 🔧 Установка UMSFA в PATH

## 📌 Для Windows

### Вариант 1: Автоматическая установка для текущего пользователя (Рекомендуется)

1. **Откройте обычный PowerShell:**
   - Администратор не нужен для `--scope user`

2. **Перейдите в папку UMSFA:**
   ```powershell
   cd C:\Users\sstep\Downloads\UMSFA
   ```

3. **Запустите установку:**
   ```powershell
   python setup_path.py --add --scope user
   ```

4. **Перезагрузите PowerShell:**
   - Закройте текущее окно
   - Откройте новое окно PowerShell
   - Проверьте: `umsfa --help`

### Вариант 2: Ручная установка (Если Вариант 1 не сработал)

1. **Откройте "Переменные окружения" (Environment Variables):**
   - Нажмите `Win + X` → выберите "System"
   - Или: Откройте "Параметры" → "Система" → "O системе"
   - Нажмите "Дополнительные параметры системы"
   - Нажмите кнопку "Переменные окружения..." внизу

2. **Отредактируйте переменную PATH:**
   - В разделе "Переменные среды пользователя" нажмите "Изменить..."
   - Нажмите "Создать"
   - Добавьте: `C:\Users\sstep\Downloads\UMSFA`
   - Нажмите "OK" три раза

3. **Перезагрузитесь или перезагрузите PowerShell**

### Проверка установки

```powershell
# Проверить статус
python setup_path.py --check

# Или просто попробуйте:
umsfa --help

# Если работает, вы увидите справку
```

---

## 🐧 Для Linux/macOS

### Установка на Linux

1. **Добавьте UMSFA в ~/.bashrc или ~/.zshrc:**

```bash
# Откройте файл конфигурации
nano ~/.bashrc
# или
nano ~/.zshrc

# Добавьте в конец файла:
export PATH="$PATH:/home/sstep/Downloads/UMSFA"

# Сохраните: Ctrl+O, Enter, Ctrl+X
```

2. **Примените изменения:**
```bash
source ~/.bashrc
# или
source ~/.zshrc
```

3. **Проверьте:**
```bash
umsfa.sh --help
```

### Установка на macOS

```bash
# Откройте ~/.zshrc (на современных версиях macOS)
nano ~/.zshrc

# Добавьте:
export PATH="$PATH:/path/to/umsfa"

# Примените:
source ~/.zshrc

# Проверьте:
umsfa.sh --help
```

---

## 🚀 Использование после установки

### Windows

```powershell
# Создание архива из текущей папки
umsfa create -p "MyPassword123"

# Создание архива со сжатием
umsfa create -comp -p "MyPassword123"

# Создание архива с уровнем сжатия 9
umsfa create -comp9 -p "MyPassword123"

# Создание архива с явным путём
umsfa create "C:\Users\User\Documents" backup.ms -p "MyPassword123"

# Информация об архиве
umsfa info backup.ms

# Распаковка
umsfa extract backup.ms restored -p "MyPassword123"

# Справка
umsfa --help
```

### Linux/macOS

```bash
# Используйте umsfa.sh вместо umsfa
umsfa.sh create ~/Documents backup.ms -p "MyPassword123"

# Или добавьте alias
alias umsfa="/path/to/UMSFA/umsfa.sh"

# Тогда сможете использовать просто:
umsfa create ~/Documents backup.ms -p "MyPassword123"
```

---

## 🔒 Защита системных папок

UMSFA имеет встроенную защиту от архивирования системных папок:

```
❌ НЕЛЬЗЯ архивировать:
  - C:\Windows\*
  - C:\Program Files\*
  - C:\ProgramData\*
  - Системные папки Windows

✅ МОЖНО архивировать:
  - C:\Users\YourName\Documents\*
  - C:\Users\YourName\Desktop\*
  - D:\Projects\*
  - E:\Data\*
```

**Если вы попробуете архивировать защищённую папку:**

```powershell
PS> umsfa create C:\Windows backup.ms

❌ Ошибка: Архивирование этого пути запрещено!

🔒 Защита от случайного удаления системных файлов

Защищённые пути:
   - C:\Windows\*
   - C:\Program Files\*
   - C:\ProgramData\*
   - Системные папки Windows
```

---

## 🔧 Удаление из PATH

Если нужно удалить UMSFA из PATH:

### Windows

1. Откройте PowerShell от имени администратора
2. Перейдите: `cd C:\Users\sstep\Downloads\UMSFA`
3. Выполните: `python setup_path.py --remove`
4. Перезагрузите PowerShell

### Linux/macOS

Отредактируйте ~/.bashrc или ~/.zshrc и удалите строку с PATH.

---

## ❓ Часто задаваемые вопросы

### Q: Почему мне нужны права администратора?
**A:** Только если вы хотите писать в системный PATH через `--scope system`. Для `--scope user` права администратора не нужны.

### Q: Можно ли установить для одного пользователя?
**A:** Да. Это теперь основной сценарий: `python setup_path.py --add --scope user`.

### Q: Что если PowerShell говорит "umsfa: The term 'umsfa' is not recognized"?
**A:** Вероятно, PATH не был обновлён. Перезагрузите PowerShell полностью (закройте и откройте заново).

### Q: Как удалить UMSFA из PATH?
**A:** Выполните: `python setup_path.py --remove` от имени администратора.

### Q: Могу ли я переместить папку UMSFA после добавления в PATH?
**A:** Нет, если вы переместите папку, UMSFA перестанет работать. Нужно удалить из PATH и добавить заново.

### Q: Почему нельзя архивировать System32?
**A:** Это защита для предотвращения случайного повреждения системных файлов Windows. Архивируйте пользовательские данные вместо этого.

---

## 🆘 Решение проблем

### Проблема: "python: The term 'python' is not recognized"

**Решение:**
- Переустановите Python
- При установке выберите "Add Python to PATH"

### Проблема: "PermissionError: требуются права администратора"

**Решение:**
- Откройте PowerShell ещё раз ОТ ИМЕНИ АДМИНИСТРАТОРА
- Используйте ручную установку через переменные окружения

### Проблема: UMSFA вызывает ошибку при архивировании

**Проверьте:**
1. Папка существует: `dir "C:\path\to\folder"`
2. У вас есть доступ к папке
3. Это не системная папка (см. защиту выше)
4. Достаточно свободного места на диске

### Проблема: Архив не распаковывается

**Возможные причины:**
- Неправильный пароль
- Архив повреждён
- Недостаточно прав доступа

---

## 📞 Команды помощи

```powershell
# Полная справка
umsfa --help

# Справка по команде архивирования
umsfa create --help

# Справка по распаковке
umsfa extract --help

# Информация об архиве
umsfa info backup.ms
```

---

## ✅ Проверка после установки

После установки проверьте, что всё работает:

```powershell
# 1. Создайте тестовую папку
mkdir test_folder
echo "test" > test_folder\test.txt

# 2. Архивируйте её
umsfa create test_folder test_backup.ms -p "test123"

# 3. Посмотрите информацию
umsfa info test_backup.ms

# 4. Распакуйте
umsfa extract test_backup.ms test_restored -p "test123"

# 5. Проверьте результат
dir test_restored\test_folder
```

Если всё получилось, UMSFA установлен и готов к использованию! 🎉

---

**UMSFA Installation Guide v1.0**  
Дата обновления: 29.04.2026
