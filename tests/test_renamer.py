import pytest
import pathlib

from batch_renamer import renamer


def _add_files(path: pathlib.Path):
    for i in range(1, 10):
        file = path / f"file-{i}.txt"
        file.write_text(f"file{i}")


def _add_dirs(path: pathlib.Path):
    for i in range(1, 5):
        (path / f"dir-{i}").mkdir()


def _get_files(path: pathlib.Path) -> list[pathlib.Path]:
    files = []
    for file in sorted(path.glob("*")):
        if file.is_file():
            files.append(file)
    return files


def test_collect_files(tmp_path):
    _add_files(tmp_path)
    _add_dirs(tmp_path)
    expected = _get_files(tmp_path)
    r = renamer.Renamer(path=tmp_path, pattern="pattern")
    r._collect_files()
    assert r._files == expected


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("file-{counter:03d}.txt", ("file-", "counter:03d", "", "txt")),
        ("file-{counter:05d}-file.txt", ("file-", "counter:05d", "-file", "txt")),
        ("file.txt", ("file", "", "", "txt")),
        ("photo_{counter}", ("photo_", "counter", "", "")),
        ("{counter}_file.txt", ("", "counter", "_file", "txt")),
        ("archive.tar.gz", ("archive.tar", "", "", "gz")),
        ("file{}.txt", ("file", "", "", "txt")),
        ("prefix{suffix}.ext", ("prefix", "suffix", "", "ext")),
        ("file.", ("file", "", ".", "")),
    ],
)
def test_parse_pattern(tmp_path, pattern, expected):
    r = renamer.Renamer(path=tmp_path, pattern=pattern)
    assert r._parse_pattern() == expected


@pytest.mark.parametrize(
    "param, i, expected",
    [("03d", 1, "001"), ("", 2, "2"), ("d", 3, "3"), ("-4d", 4, "---4")],
)
def test_get_dynamic_counter(tmp_path, param, i, expected):
    r = renamer.Renamer(path=tmp_path, pattern="pattern")
    assert r._get_dynamic_counter(param, i) == expected


@pytest.mark.parametrize(
    "dynamic_part, i, expected",
    [
        ("", 0, ""),
        ("counter", 2, "2"),
        ("counter:d", 3, "3"),
        ("counter:03d", 4, "004"),
    ],
)
def test_get_dynamic_content(tmp_path, dynamic_part, i, expected):
    r = renamer.Renamer(path=tmp_path, pattern="pattern")
    assert r._get_dynamic_content(dynamic_part, i) == expected


@pytest.mark.parametrize(
    "pattern, expected, length",
    [
        ("file-{counter:03d}.txt", [f"file-00{i+1}.txt" for i in range(9)], 9),
        ("file-{counter:d}file.txt", [f"file-{i+1}file.txt" for i in range(100)], 100),
        ("file-{counter:#2d}file.txt", [f"file-#{i+1}file.txt" for i in range(5)], 5),
    ],
)
def test_generate_new_names(tmp_path, pattern, expected, length):
    r = renamer.Renamer(path=tmp_path, pattern=pattern)
    r._files = [tmp_path / f"{i}.txt" for i in range(length)]
    r._generate_new_names()
    assert r._new_names == expected
