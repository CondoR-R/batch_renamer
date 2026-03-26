import pathlib
import typing

from . import exceptions


def _get_forbidden_names() -> list[str]:
    forbidden_names = ["CON", "PRN", "AUX", "NUL"]
    for i in range(1, 10):
        forbidden_names.append(f"COM{i}")
        forbidden_names.append(f"LPT{i}")
    return forbidden_names


FORBIDDEN_NAMES: typing.Final = _get_forbidden_names()


def validate_path(path: str) -> pathlib.Path:
    """
    Проверяет на директорию и существует ли она по указаному пути.
    Если пути не сущестует или по переданному пути находится не директория,
    пробрасывается ошибка.
    :param path str: путь к директории
    :return: pathlib.Path
    """
    p = pathlib.Path(path)
    if not p.exists():
        raise exceptions.PathNotFoundError(p)
    if not p.is_dir():
        raise exceptions.PathNotDirError(p)
    return p


def validate_filename(filename: str):
    """
    Проверяет, является ли имя файла валидным, если валидно - ничего не возвращает,
    если нет - пробрасывает ошибку.
    :param filename str: имя файла.
    :return: None
    """
    # проверка на пустое имя
    if not filename:
        raise exceptions.PatternValidationError("Имя файла не должно быть пустым")

    # проверка на отстуствие точки или пробела в конце
    if filename[-1] == " " or filename[-1] == ".":
        raise exceptions.PatternValidationError(
            "Имя файла не должно оканчиваться точкой или пробелом"
        )

    # проверка на отсутвие запрещенных символов
    for s in '<>:"/\\|?*':
        if s in filename:
            raise exceptions.PatternValidationError(
                f'В имени файла не должен быть символ "{s}"'
            )

    # проверка на запрещенные имена
    name = filename.rsplit(".", 1)[0]
    for f_name in FORBIDDEN_NAMES:
        if name.lower() == f_name.lower():
            raise exceptions.PatternValidationError(
                f"{name} не может быть использовано в качестве имени файла"
            )


def validate_counter_param(param: str) -> tuple[str, int]:
    """
    Валидация параметра для counter
    :param str param: параметр counter, не пустая строка
    :return: символ заполнения пробелов, колличество цифр
    """
    # если не указан тип d (decimal)
    if param[-1] != "d":
        raise exceptions.PatternValidationError(
            "Неверный тип параметра нумерации в паттерне (не указан тип d)"
        )

    # если параметр не подходит под шаблон "{символ заполнеия пробелов}{колличество символов}d"
    if len(param) < 3:
        raise exceptions.PatternValidationError(
            "Параметр паттерна для counter должен соответствовать шаблону"
            '"{символ заполнеия пробелов}{колличество символов}d"'
        )

    symbol = param[0]
    try:
        length = int(param[1:-1])
    except:
        raise exceptions.PatternValidationError(
            f'Длина динамической части в паттерне "{param[1:-1]}" должна быть числом'
        )
    return (symbol, length)
