import pathlib

from . import exceptions


def validate_path(path: str) -> pathlib.Path:
    """
    Проверяет на директорию и существует ли она по указаному пути.
    Если пути не сущестует или по переданному пути находится не директория,
    пробрасывается ошибка.
    :param path: str
    :return: pathlib.Path
    """
    p = pathlib.Path(path)
    if not p.exists():
        raise exceptions.PathNotFoundError(p)
    if not p.is_dir():
        raise exceptions.PathNotDirError(p)
    return p
