import pathlib

from . import cli
from . import exceptions


class Renamer:
    def __init__(self, path: pathlib.Path, pattern: str):
        self._path = path
        self._pattern = pattern
        self._files: list[pathlib.Path] = []
        self._new_names: list[str] = []

    def _collect_files(self):
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
        prefix = dynamic_part = suffix = extension = ""

        pattern_arr = self._pattern.rsplit(".", 1)
        if len(pattern_arr) == 2:
            extension = pattern_arr[-1]
        pattern = pattern_arr[0]

        dynamic_start = pattern.find("{")
        dynamic_end = pattern.find("}", dynamic_start)
        if dynamic_start == -1 or dynamic_end == -1:
            prefix = pattern
        else:
            prefix = pattern[:dynamic_start]
            dynamic_part = pattern[dynamic_start + 1 : dynamic_end]
            suffix = pattern[dynamic_end + 1 :]

        return (prefix, dynamic_part, suffix, extension)

    def _generate_new_names(self):
        prefix, dynamic_part, suffix, extension = self._parse_pattern()

        for i in range(len(self._files)):
            if dynamic_part == "counter:03d":
                counter = ("0" * (3 - len(str(i + 1))) + str(i + 1))[:3]
                filename = (
                    prefix + counter + suffix + (("." + extension) if extension else "")
                )
                self._new_names.append(filename)

    def _change_names(self):
        success_count = 0
        for i, file in enumerate(self._files):
            new_name = pathlib.Path(self._path, self._new_names[i])
            try:
                if new_name.exists():
                    # raise exceptions.RenameConflictError(self._files[i], new_name)
                    cli.show_warning(
                        str(exceptions.RenameConflictError(file, new_name))
                    )
                    continue

                file.rename(new_name)
                success_count += 1
            # except exceptions.RenameConflictError as err:
            #     cli.show_warning(str(err))
            #     continue
            except OSError as err:
                cli.show_warning(
                    f"Не удалось получить доступ к файлу {file}: {err}"
                )
        cli.show_sucsess_changes(success_count)

    def execute(self, dry_run: bool):
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
