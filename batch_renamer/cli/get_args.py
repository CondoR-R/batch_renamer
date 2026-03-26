# задание и получение аргументов командной строки
import argparse
import textwrap
import dataclasses


@dataclasses.dataclass()
class Args:
    path: str
    pattern: str
    dry_run: bool


def _add_args(parser: argparse.ArgumentParser) -> None:
    """
    Добавляет доступные аргументы командной строки
    :param argparse.ArgumentParser parser: парсер аргументов командной строки
    :return: None
    """
    parser.add_argument(
        "--path", help="папка с файлами (по умолчанию текущая)", default="."
    )
    parser.add_argument(
        "--pattern",
        help="шаблон имени (например, photo_{counter:03d}.jpg)",
        required=True,
    )
    parser.add_argument(
        "--dry-run",
        help="показать, что будет переименовано, но не применять",
        action="store_true",
    )


def _description() -> str:
    """
    Возвращает текст описания программы при вызове --help
    :return: str
    """
    description = """
        Утилита для пакетного переименовывания файлов.
        В заданной директории по заданному шаблону переименовывет все файлы.
        """
    return textwrap.dedent(description)


def _epilog() -> str:
    """
    Возвращает текст эпилога программы при вызове  --help
    :return: str
    """
    epilog = """
        Переименование необратимо, поэтому перед выполнением следует убедиться в правильности шаблона через --dry-run.
        Пример использования:
        cli --pattern "image_{counter:03d}.png" --dry-run
        cli --path ./docs --pattern "doc_{counter}.pdf"
        """
    return textwrap.dedent(epilog)


def get_args() -> Args:
    """
    Получение аргументов командной строки
    :return: Args
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=_description(),
        epilog=_epilog(),
    )
    _add_args(parser)
    parsed = parser.parse_args()
    if parsed.path == "":
        parser.error("При указании --path значение пути не должно быть пустым")
    if parsed.pattern == "":
        parser.error("Значение для флага --pattern не должно быть пустым")
    args = Args(path=parsed.path, pattern=parsed.pattern, dry_run=parsed.dry_run)
    return args
