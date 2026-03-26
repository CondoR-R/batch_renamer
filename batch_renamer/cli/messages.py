import pathlib
import sys

from batch_renamer import exceptions


def show_changes(files: list[pathlib.Path], new_names: list[str]) -> None:
    """
    Выводит в терминал изменения в названиях файлов.
    :param list[pathlib.Path] files: список файлов со старыми названиями
    :param list[str] new_names: список новых названий файлов
    :return: None
    """
    max_len = max(len(file.name) for file in files)
    for i in range(len(files)):
        print(f"{files[i].name:<{max_len}} -> {new_names[i]}")


def get_changes_accept() -> bool:
    """
    Узнает от пользователя, принять ли изменения
    :return: bool
    """
    answer = input("Принять изменения? Y/N: ")
    ok = answer == "Y" or answer == "y"
    return ok


def show_empty_message(dir: pathlib.Path) -> None:
    """
    Сообщает пользователю отсутвие файлов в выбранной директории
    :param pathlib.Path dir: путь к директории
    :return: None
    """
    print(f"В директории {dir} отсутствуют файлы")


def show_sucsess_changes(count: int) -> None:
    """
    Выводит пользователю сообщение о колличестве успешно переименованных файлов.
    Принимает колличество успешно переименованных файлов
    :param int count: колличество успешно переименованных файлов
    :return: None
    """
    print(f"Успешно переименовано {count} файлов")


def show_error(err: exceptions.BatchRenamerError) -> None:
    """
    Выводит сообщение об ошибке.
    :param exceptions.BatchRenamerError err: сообщение об ошибке
    :return: None
    """
    print(f"ОШИБКА: {err}", file=sys.stderr)


def show_warning(message: str) -> None:
    """
    Выводит сообщение с предупреждением
    :param str message: сообщение с предупреждением
    :return: None
    """
    print(f"ПРЕДУПРЕЖДЕНИЕ: {message}", file=sys.stderr)
