import csv

import pytest

import main


def _write_csv(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def test_median_report_combines_files(tmp_path):
    file_one = tmp_path / "one.csv"
    file_two = tmp_path / "two.csv"

    _write_csv(
        file_one,
        [
            {"student": "Anna", "coffee_spent": "100"},
            {"student": "Anna", "coffee_spent": "300"},
            {"student": "Boris", "coffee_spent": "50"},
        ],
    )
    _write_csv(
        file_two,
        [
            {"student": "Anna", "coffee_spent": "200"},
            {"student": "Boris", "coffee_spent": "70"},
        ],
    )

    records = main.load_records([str(file_one), str(file_two)])
    rows = main.build_median_coffee_report(records)

    assert rows == [["Anna", 200], ["Boris", 60]]


def test_cli_outputs_table(tmp_path, capsys):
    file_path = tmp_path / "data.csv"
    _write_csv(
        file_path,
        [
            {"student": "Anna", "coffee_spent": "100"},
            {"student": "Anna", "coffee_spent": "300"},
            {"student": "Boris", "coffee_spent": "70"},
        ],
    )

    exit_code = main.main(["--files", str(file_path), "--report", "median-coffee"])
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert "median_coffee_spent" in captured
    assert "Anna" in captured
    assert "Boris" in captured


def test_missing_columns_raise(tmp_path):
    file_path = tmp_path / "bad.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["student"])
        writer.writeheader()
        writer.writerow({"student": "Anna"})

    with pytest.raises(ValueError, match="coffee_spent column is missing"):
        main.load_records([str(file_path)])
