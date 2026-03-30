import pathlib

from . import cli
from . import exceptions
from . import validators


class Renamer:
    def __init__(self, path: pathlib.Path, pattern: str):
        self._path = path
        self._pattern = pattern
        self._files: list[pathlib.Path] = []
        self._new_names: list[str] = []

    def _collect_files(self) -> None:
        """
        Получает файлы в переданной при инициализации директории.
        При отсутствии доступа к файлу выводит предупреждение
        :return: None
        """
        for file in sorted(self._path.glob("*")):
            try:
                if file.is_file():
                    self._files.append(file)
            except OSError as err:
                cli.show_warning(
                    f"Не удалось получить доступ к файлу {file.name}: {err}"
                )
                continue

    def _parse_pattern(self) -> tuple[str, str, str, str]:
        """
        Получает из паттерна данные, нобходимые для формирования новых имен файлов
        :return: prefix, dynamic_part, suffix, extension
        """
        prefix = dynamic_part = suffix = extension = ""

        pattern_arr = self._pattern.rsplit(".", 1)
        if len(pattern_arr) == 2:  # если есть расширение файла в паттерне
            extension = pattern_arr[-1]
        pattern = pattern_arr[0]

        dynamic_start = pattern.find("{")
        dynamic_end = pattern.find("}", dynamic_start)
        if dynamic_start == -1 or dynamic_end == -1:  # отсутсвует динамическая часть
            prefix = pattern
        else:
            prefix = pattern[:dynamic_start]
            dynamic_part = pattern[dynamic_start + 1 : dynamic_end]
            suffix = pattern[dynamic_end + 1 :]

        if len(pattern_arr) == 2 and extension == "":
            suffix = suffix + "."
        return (prefix, dynamic_part, suffix, extension)

    def _get_dynamic_counter(self, param: str, i: int) -> str:
        """
        Получение порядкового номера имени файла
        :param str param: настройка нумерации
        :param int i: номер файла
        """
        # если параметр пустой или указан только тип d (decimal), то порядковый номер - номер файла
        if (not param) or param == "d":
            return str(i)

        symbol, length = validators.validate_counter_param(param)
        counter = (symbol * max(0, length - len(str(i))) + str(i))[:length]
        return counter

    def _dynamic_match_case(self, dynamic_type: str, dynamic_param: str, i: int) -> str:
        """
        Обработка доступных вариаций динамической части паттерна
        :param str dynamic_type: тип динамической части
        :param str dynamic_param: параметр динамической части
        :param int i: индекс файла в списке
        :return: str
        """
        match dynamic_type:
            case "counter":
                return self._get_dynamic_counter(dynamic_param, i)
            case _:
                raise exceptions.PatternValidationError(
                    f'Неизвестный тип динамической части паттерна "{dynamic_type}"'
                )

    def _get_dynamic_content(self, dynamic_part: str, i: int) -> str:
        """
        Получение содержимого динамической части названия файла
        :param str dynamic_part: динамическая часть
        :param int i: номер файла в списке
        :return: str
        """
        if not dynamic_part:
            return ""

        dynamic_arr = dynamic_part.split(":")
        if len(dynamic_arr) < 2:
            dynamic_type = dynamic_arr[0]
            dynamic_param = ""
        else:
            dynamic_type, dynamic_param = dynamic_arr

        dynamic = self._dynamic_match_case(dynamic_type, dynamic_param, i)
        return dynamic

    def _generate_new_names(self) -> None:
        """
        Генерирует новые названия файлов
        :return: None
        """
        prefix, dynamic_part, suffix, extension = self._parse_pattern()

        for i in range(len(self._files)):
            dynamic_content = self._get_dynamic_content(dynamic_part, i + 1)
            filename = (
                prefix
                + dynamic_content
                + suffix
                + (("." + extension) if extension else extension)
            )
            validators.validate_filename(filename)
            self._new_names.append(filename)

    def _change_names(self) -> None:
        """
        Производит переименовывание файлов.
        При конфликте имен или при отсутствии доступа к файлу выводит предупреждения
        :return: None
        """
        success_count = 0
        for i, file in enumerate(self._files):
            new_name = pathlib.Path(self._path, self._new_names[i])
            try:
                if new_name.exists():
                    cli.show_warning(
                        str(exceptions.RenameConflictError(file, new_name))
                    )
                    continue

                file.rename(new_name)
                success_count += 1
            except OSError as err:
                cli.show_warning(f"Не удалось получить доступ к файлу {file}: {err}")
        cli.show_success_changes(success_count)

    def execute(self, dry_run: bool):
        """
        Основной метод класса. Выполяет все действия для переименовывания файлов
        и предпросмотра результата.
        :param bool dry_run: True - показать изменения (не применять их)
        :param bool dry_run: False - применить изменения
        """
        self._collect_files()
        if not len(self._files):
            cli.show_empty_message(self._path)
            return

        self._generate_new_names()
        cli.show_changes(self._files, self._new_names)

        if dry_run:
            return

        ok = cli.get_changes_accept()
        if ok:
            self._change_names()
