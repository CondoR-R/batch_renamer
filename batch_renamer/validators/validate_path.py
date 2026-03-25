import pathlib


def validate_path(path: str) -> pathlib.Path:
    """
    Проверяет на директорию и существует ли она по указаному пути.
    :param path: str
    :return: pathlib.Path
    """
    p = pathlib.Path(path)
    if not p.exists():
        print("путь не существует")
    if not p.is_dir():
        print("это не директория")
    return p
