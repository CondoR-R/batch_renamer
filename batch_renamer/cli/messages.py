import pathlib
import sys

from batch_renamer import exceptions


def show_changes(files: list[pathlib.Path], new_names: list[str]) -> None:
    """
    Выводит в терминал изменения в названиях файлов.
    :param changes:
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
    :return: None
    """
    print(f"В директории {dir} отсутствуют файлы")


def show_sucsess_changes(count: int) -> None:
    print(f"Успешно переименовано {count} файлов")


def show_error(err: exceptions.BatchRenamerError):
    print(f"ОШИБКА: {err}", file=sys.stderr)


def show_warning(message: str) -> None:
    print(f"ПРЕДУПРЕЖДЕНИЕ: {message}", file=sys.stderr)
