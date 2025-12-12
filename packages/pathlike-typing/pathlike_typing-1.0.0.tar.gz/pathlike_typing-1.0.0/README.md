# PathLike Typing Library / Библиотека PathLike Typing

____

# English Documentation

## Overview
`pathlike-typing` is a lightweight Python library that provides a standardized type alias PathLike for representing file system paths in type annotations. It simplifies working with path objects by unifying `Path` (from `pathlib`) and `str` types under a single type hint.

## Installing
```shell
pip install pathlike-typing
```

## Version
Current version: `1.0.0`

## Usage
```python
from pathlib import Path
from pathlike_typing import PathLike

# Use PathLike in type annotations
def read_file(path: PathLike) -> str:
    # Both Path objects and strings are accepted
    with open(path, 'r') as f:
        return f.read()

# Both will work:
read_file(Path("/home/user/file.txt"))
read_file("/home/user/file.txt")
```

## Type Alias
### The library provides one main export:

- `PathLike`: Type alias for `Union[Path, str]`

## Exports
```python
__all__ = ["PathLike", "__version__"]
```

## Why Use This Library?
1. Consistency: Standardizes path type annotations across your codebase
2. Clarity: Makes function signatures clearer about what types of path arguments are accepted
3. Compatibility: Works seamlessly with both pathlib.Path objects and traditional string paths
4. Lightweight: Minimal dependencies and overhead

## License
MIT License - See LICENSE file for details.

----

# Документация на русском языке

## Обзор
`pathlike-typing` — это облегчённая библиотека Python, предоставляющая стандартизированный псевдоним типа PathLike для представления путей к файловой системе в аннотациях типов. Она упрощает работу с объектами путей, объединяя типы `Path` (из `pathlib`) и `str` под единым указанием типа.

## Установка
```shell
pip install pathlike-typing
```

## Версия
Текущая версия: `1.0.0`

## Использование
```python
from pathlib import Path
from pathlike_typing import PathLike

# Используйте PathLike в аннотациях типов
def read_file(path: PathLike) -> str:
    # Поддерживаются как объекты Path, так и строки
    with open(path, 'r') as f:
        return f.read()

# Поддерживаются оба варианта:
read_file(Path("/home/user/file.txt"))
read_file("/home/user/file.txt")
```

## Псевдоним типа
### Библиотека предоставляет один основной экспорт:

- `PathLike`: Псевдоним типа для `Union[Path, str]`

## Экспорт
```python
__all__ = ["PathLike", "__version__"]
```

## Зачем использовать эту библиотеку?

1. Единообразие: Стандартизирует аннотации типов путей в вашей кодовой базе.
2. Ясность: Делает сигнатуры функций более понятными для определения типов принимаемых аргументов путей.
3. Совместимость: Без проблем работает как с объектами pathlib.Path, так и с традиционными строковыми путями.
4. Легковесность: Минимальные зависимости и накладные расходы.

## Лицензия
Лицензия MIT — подробности см. в файле LICENSE.
