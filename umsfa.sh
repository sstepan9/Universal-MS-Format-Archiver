#!/bin/bash
# Universal MS Format Archiver (UMSFA) - Linux/macOS wrapper
# Этот файл позволяет запускать UMSFA из любого места в системе

# Получение директории где находится этот скрипт
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Ошибка: Python 3 не найден в PATH"
    echo ""
    echo "Решение: Установите Python 3.7 или выше"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  macOS: brew install python3"
    exit 1
fi

# Проверка наличия umsfa.py
if [ ! -f "$SCRIPT_DIR/umsfa.py" ]; then
    echo "❌ Ошибка: umsfa.py не найден в $SCRIPT_DIR"
    exit 1
fi

# Передача всех аргументов Python скрипту
python3 "$SCRIPT_DIR/main.py" "$@"

exit $?
