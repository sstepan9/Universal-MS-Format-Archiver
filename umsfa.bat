@echo off
REM Universal MS Format Archiver (UMSFA) - Windows wrapper
REM Этот файл позволяет запускать UMSFA из любого места в системе

setlocal enabledelayedexpansion

REM Получение директории где находится этот скрипт
set SCRIPT_DIR=%~dp0

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка: Python не найден в PATH
    echo.
    echo Решение: Установите Python 3.7 или выше с сайта python.org
    echo При установке выберите "Add Python to PATH"
    exit /b 1
)

REM Проверка наличия umsfa.py
if not exist "%SCRIPT_DIR%umsfa.py" (
    echo ❌ Ошибка: umsfa.py не найден в %SCRIPT_DIR%
    exit /b 1
)

REM Передача всех аргументов Python скрипту
python "%SCRIPT_DIR%main.py" %*

exit /b %ERRORLEVEL%
