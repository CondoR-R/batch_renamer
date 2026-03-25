import pathlib


class Renamer:
    def __init__(self, path: pathlib.Path, pattern: str):
        self.path = path
        self.pattern = pattern

    def _collect_files(self):
        self.files = [file for file in self.path.glob("*") if file.is_file()]

    def _parse_pattern(self) -> tuple(str, str, str, str):
        prefix = dynamic_part = suffix = extension = None

        pattern_arr = self.pattern.rsplit(".", 1)
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
        self.new_names = []
        for i in range(len(self.files)):
            if dynamic_part == "counter:03d":
                counter = ("0" * (3 - len(str(i + 1))) + str(i + 1))[:3]
                filename = prefix + counter + suffix + "." + extension
                self.new_names.append(filename)

    def _dry_run(self):
        pass

    def execute(self, dry_run: bool):
        self._collect_files()
        self._generate_new_names()
        if dry_run:
            self._dry_run()
