import pathlib


class BatchRenamerError(Exception):
    pass


class PathNotFoundError(BatchRenamerError):
    """
    Путь не найден.
    Принимает путь к файлу/директории на котором произошла ошибка
    :param path: pathlib.Path
    """

    def __init__(self, path: pathlib.Path):
        self.path = path

    def __str__(self):
        return f'Путь "{self.path}" не найден.'


class PatternValidationError(BatchRenamerError):
    """
    Неверный формат паттерна.
    """

    def __str__(self):
        return f"Неверный формат паттерна для именования файлов"


class RenameConflictError(BatchRenamerError):
    """
    Ошибка при переименовывании файла (файл с новым именем уже сущестует)
    :param old_name: pathlib.Path
    :param new_name: pathlib.Path
    """

    def __init__(self, old_name: pathlib.Path, new_name: pathlib.Path):
        self.old_name = old_name
        self.new_name = new_name

    def __str__(self):
        return (
            f"Невозможно переименовать файл {self.old_name.name} в {self.new_name.name}. "
            f"Файл с таким именем уже существует"
        )


class FileAccessError(BatchRenamerError):
    """
    Ошибка доступа к файлу
    :param file: pathlib.Path
    """

    def __init__(self, file: pathlib.Path):
        self.file = file

    def __str__(self):
        return f"Не удалось получить доступ к файлу {self.file}"


class PathNotDirError(BatchRenamerError):
    """
    Указанный путь не является директорией
    :param path: pathlib.Path
    """

    def __init__(self, path: pathlib.Path):
        self.path = path

    def __str__(self):
        return f"Путь {self.path} не является директорией"
