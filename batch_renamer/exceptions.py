import pathlib


class BatchRenamerError(Exception):
    pass


class PathNotFoundError(BatchRenamerError):
    """
    Путь не найден.
    Принимает путь к файлу/директории на котором произошла ошибка
    :param pathlib.Path path: путь к файлу/директории
    """

    def __init__(self, path: pathlib.Path):
        self.path = path

    def __str__(self):
        return f'Путь "{self.path}" не найден.'


class PatternValidationError(BatchRenamerError):
    """
    Неверный формат паттерна.
    :param str msg: сообщение для конкретики ошибки паттерна
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"Неверный формат паттерна для именования файлов: {self.msg}"


class RenameConflictError(BatchRenamerError):
    """
    Ошибка при переименовывании файла (файл с новым именем уже сущестует)
    :param pathlib.Path old_name: путь к файлу под старым именем
    :param pathlib.Path new_name: путь к файлу под новым именем
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
    :param pathlib.Path file: путь к файлу
    """

    def __init__(self, file: pathlib.Path):
        self.file = file

    def __str__(self):
        return f"Не удалось получить доступ к файлу {self.file}"


class PathNotDirError(BatchRenamerError):
    """
    Указанный путь не является директорией
    :param pathlib.Path path: путь к ошибочной директории
    """

    def __init__(self, path: pathlib.Path):
        self.path = path

    def __str__(self):
        return f"Путь {self.path} не является директорией"


class ExtensionError(BatchRenamerError):
    """
    Ошибка расширения файла
    :param str msg: описание ошибки, связанной с расширением
    """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
