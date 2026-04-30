# ⚡ UMSFA в PATH — Использование из любого места

## ✅ Успешно добавлено!

После добавления UMSFA в системный PATH вы сможете вызывать его из **любой папки** в системе просто как команду.

---

## 🎯 Быстрые команды

### Основные команды (после добавления в PATH)

```powershell
# Архивирование текущей папки
umsfa create . backup.ms -p "password123"

# Архивирование конкретной папки
umsfa create "C:\Users\User\Documents" docs.ms -p "password123"

# Распаковка архива
umsfa extract backup.ms restored -p "password123"

# Информация об архиве
umsfa info backup.ms

# Справка
umsfa --help
```

---

## 📁 Работа с текущей директорией

### Сценарий 1: Архивирование папки где вы находитесь

```powershell
# Перейти в папку
cd "C:\Users\User\MyProject"

# Архивировать текущую папку (.)
umsfa create . project_backup.ms -p "secure123"

# Проверить архив
umsfa info project_backup.ms

# Распаковать
umsfa extract project_backup.ms project_restored -p "secure123"
```

### Сценарий 2: Архивирование подпапок

```powershell
cd "C:\Users\User\MyProject"

# Архивировать подпапку src
umsfa create src src_backup.ms -p "pass"

# Архивировать подпапку documents с расширенным путём
umsfa create ".\documents\important" important.ms -p "pass"
```

### Сценарий 3: Архивирование с полным путём

```powershell
# Работать можно из любой папки
cd "C:\Downloads"

# Архивировать папку с полным путём
umsfa create "C:\Users\User\MyProject" project.ms -p "pass"

# Результат будет в C:\Downloads\project.ms
```

---

## 🔐 Примеры с паролями

### Интерактивный ввод пароля

```powershell
# Система попросит ввести пароль
umsfa create my_folder backup.ms -i

# Ввод:
# 🔐 Введите пароль: (скрытый ввод)
# 🔐 Подтвердите пароль: (скрытый ввод)
```

### Пароль в команде

```powershell
# Передать пароль в команде
umsfa create my_folder backup.ms -p "MyPassword123!"
```

### Без пароля

```powershell
# Архивировать без шифрования
umsfa create my_folder backup.ms

# Информация покажет:
# Зашифрован: ❌ Нет
```

---

## 🛡️ Защита системных папок

### Защищённые пути (нельзя архивировать)

```
❌ ЗАПРЕЩЕНО:
  - C:\Windows\
  - C:\Program Files\
  - C:\Program Files (x86)\
  - C:\ProgramData\
  - System Volume Information\
  - $Recycle.Bin\
  - PerfLogs\
```

### Если вы случайно попробуете

```powershell
PS C:\> umsfa create C:\Windows test.ms

❌ Ошибка: Архивирование этого пути запрещено!

🔒 Защита от случайного удаления системных файлов
```

### Как обойти (для опытных)

Если вы **действительно** хотите архивировать системные файлы, используйте Python напрямую:

```python
from umsfa import MSArchiver

# Это обойдёт проверку, но ИСПОЛЬЗУЙТЕ С ОСТОРОЖНОСТЬЮ!
archiver = MSArchiver(password="pass")
archiver.archive("C:\Windows", "windows.ms")
```

⚠️ **НЕ ДЕЛАЙТЕ ЭТО, ЕСЛИ НЕ ЗНАЕТЕ ЧТО ВЫ ДЕЛАЕТЕ!**

---

## 📊 Практические примеры

### Пример 1: Резервное копирование документов

```powershell
cd "C:\Users\John\Documents"

# Архивировать текущую папку
umsfa create . Documents_Backup.ms -p "VerySecurePass123!"

# Проверить размер
dir Documents_Backup.ms | Format-Table Name, Length
```

### Пример 2: Резервная копия проекта

```powershell
# Перейти в папку проекта
cd "D:\Projects\MyApp"

# Создать резервную копию
umsfa create . backup.ms -i

# Распаковать на другой машине
# umsfa extract backup.ms restored -p "введённый_пароль"
```

### Пример 3: Отправка зашифрованной папки

```powershell
# Папка с конфиденциальной информацией
cd "C:\Users\User\Confidential"

# Архивировать и зашифровать
umsfa create . confidential.ms -p "UltraSecurePassword2024!"

# Отправить по почте или через облако
# (файл автоматически зашифрован AES-256)
```

### Пример 4: Автоматическое резервное копирование

```powershell
# Создать скрипт backup.ps1
@"
`$folders = @(
    "C:\Users\User\Documents",
    "C:\Users\User\Desktop",
    "C:\Users\User\Downloads"
)

foreach (`$folder in `$folders) {
    `$date = Get-Date -Format "yyyy-MM-dd"
    `$filename = "$(Split-Path `$folder -Leaf)_`$date.ms"
    
    Write-Host "Архивирование `$folder..."
    umsfa create "`$folder" "`$filename" -p "BackupPassword2024"
}
"@ | Out-File backup.ps1

# Запустить скрипт
.\backup.ps1
```

---

## 🚀 Продвинутые использования

### Архивирование с поиском файлов

```powershell
# Архивировать только .txt файлы
# (создайте папку с нужными файлами сначала)
mkdir temp_backup
Get-ChildItem -Filter *.txt | Copy-Item -Destination temp_backup
umsfa create temp_backup txt_files.ms -p "pass"
Remove-Item temp_backup -Recurse
```

### Последовательное архивирование

```powershell
# Архивировать несколько папок
$folders = @("Documents", "Pictures", "Videos")

foreach ($folder in $folders) {
    umsfa create "C:\Users\User\$folder" "$folder.ms" -p "password"
    Write-Host "✅ Архивирована: $folder"
}
```

### Архивирование и проверка

```powershell
# Архивировать
umsfa create my_folder backup.ms -p "pass"

# Проверить информацию
umsfa info backup.ms

# Распаковать для проверки
umsfa extract backup.ms test_extract -p "pass"

# Сравнить размеры
Write-Host "Исходная папка:"
Get-ChildItem my_folder -Recurse | Measure-Object -Sum Length

Write-Host "`nРаспакованная папка:"
Get-ChildItem test_extract -Recurse | Measure-Object -Sum Length
```

---

## 🐍 Использование в Python скриптах

Если добавлены правильно пути Python, можете также импортировать UMSFA:

```python
import sys
sys.path.insert(0, "C:\\Users\\sstep\\Downloads\\UMSFA")
from umsfa import MSArchiver

# Архивирование из текущей директории
archiver = MSArchiver(password="SecurePass")
archiver.archive(".", "current_dir.ms")

# Распаковка
archiver.extract("current_dir.ms", "extracted")
```

---

## 📝 Скрипты для Windows

### batch скрипт (backup.bat)

```batch
@echo off
REM Резервное копирование важных папок

set PASSWORD=MySecurePassword123!
set DATE=%date:~-4%%date:~-10,2%%date:~-7,2%

echo Архивирование документов...
umsfa create "%USERPROFILE%\Documents" "backup_documents_%DATE%.ms" -p "%PASSWORD%"

echo Архивирование рабочего стола...
umsfa create "%USERPROFILE%\Desktop" "backup_desktop_%DATE%.ms" -p "%PASSWORD%"

echo ✅ Готово!
```

### PowerShell скрипт (backup.ps1)

```powershell
# backup.ps1
$password = "MySecurePassword123!"
$date = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "🔄 Начало резервного копирования..."

# Список папок для архивирования
$backupFolders = @(
    "$env:USERPROFILE\Documents",
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\Pictures"
)

foreach ($folder in $backupFolders) {
    if (Test-Path $folder) {
        $name = Split-Path $folder -Leaf
        $filename = "backup_${name}_${date}.ms"
        
        Write-Host "📦 Архивирование: $name"
        umsfa create "$folder" "$filename" -p $password
        Write-Host "✅ Завершено: $filename`n"
    }
}

Write-Host "✨ Все резервные копии созданы!"
```

---

## ⚙️ Интеграция с Git

Если вы используете Git, архивируйте репозиторий перед важными операциями:

```powershell
# В корне репозитория
cd C:\Projects\MyRepo

# Создать резервную копию перед важным merge
umsfa create . "backup_before_merge.ms" -p "pass"

# Если что-то пошло не так:
umsfa extract "backup_before_merge.ms" "restored_repo" -p "pass"
```

---

## 📊 Проверка установки

```powershell
# Проверить что UMSFA в PATH
Get-Command umsfa

# Должно выдать что-то вроде:
# CommandType     Name                Version    Source
# -----------     ----                -------    ------
# ExternalScript  umsfa.bat                      C:\Users\sstep\Downloads\UMSFA\umsfa.bat

# Проверить версию Python
python --version

# Проверить работоспособность
umsfa --help
```

---

## ❓ Часто задаваемые вопросы

### Q: Работает ли UMSFA если я переместил папку?
**A:** Нет, нужно обновить PATH или запустить `setup_path.py` ещё раз.

### Q: Могу ли я удалить исходную папку после архивирования?
**A:** Да, но рекомендуется сначала проверить что архив работает:
```powershell
umsfa info archive.ms
umsfa extract archive.ms test -p "pass"
# Если всё ОК, тогда удаляйте исходную
```

### Q: Как узнать пароль от старого архива?
**A:** К сожалению, невозможно. Пароли не восстанавливаются. Храните пароли в безопасном месте!

### Q: Могу ли я архивировать сетевые диски?
**A:** Да, если к ним есть доступ:
```powershell
umsfa create "\\server\share\folder" network.ms -p "pass"
```

### Q: Что если UMSFA не находится как команда?
**A:** Перезагрузите PowerShell полностью (закройте и откройте заново).

---

## 🔄 Обновление PATH

Если вы обновили Python или переместили UMSFA:

```powershell
# От имени администратора:
python setup_path.py --remove
python setup_path.py --add
```

---

## ✨ Финальные советы

1. **Используйте сильные пароли:** `MyP@ssw0rd!2024!`
2. **Храните пароли:** используйте менеджер паролей
3. **Проверяйте архивы:** `umsfa info` перед удалением
4. **Делайте резервные копии:** архивируйте архивы!
5. **Не забывайте:** потеря пароля = потеря данных

---

**✅ UMSFA готов к использованию из любого места в системе!**

Начните с простой команды:
```powershell
umsfa create . backup.ms -p "test123"
```

---

**UMSFA PATH Usage Guide v1.0**  
Дата: 29.04.2026
