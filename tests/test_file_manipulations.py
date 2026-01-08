from __future__ import annotations

import csv
from pathlib import Path

import pytest

from pytoolbase._optional import OptionalDependencyError
from pytoolbase.configuration_file import EnvFile
from pytoolbase.file_manipulations import (
    copy_file,
    csv_to_xlsx,
    parse_env_csv_list,
    read_excel_columns,
    save_calculated_cells,
)


def test_copy_file(tmp_path: Path) -> None:
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("x", encoding="utf-8")

    out = copy_file(src, dst)
    assert out.exists()
    assert dst.read_text(encoding="utf-8") == "x"


def test_parse_env_csv_list(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"
    env_path.write_text("LIST=a,b, c,,\n", encoding="utf-8")
    vals = parse_env_csv_list(EnvFile(env_path), "LIST")
    assert vals == ["a", "b", "c"]


def test_csv_to_xlsx_and_read_excel_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["h1", "h2"])
        w.writerow(["a", "b"])
        w.writerow(["c", "d"])

    xlsx_path = tmp_path / "out.xlsx"
    csv_to_xlsx(csv_path, xlsx_path)

    rows = read_excel_columns(xlsx_path, [1, 2])
    assert rows[0] == ["h1", "h2"]
    assert rows[1] == ["a", "b"]
    assert rows[2] == ["c", "d"]


def test_save_calculated_cells_requires_xlwings(tmp_path: Path) -> None:
    # xlwings is intentionally not installed in this environment
    xlsx = tmp_path / "file.xlsx"
    xlsx.write_text("not a real xlsx", encoding="utf-8")
    with pytest.raises(OptionalDependencyError):
        save_calculated_cells(xlsx)
