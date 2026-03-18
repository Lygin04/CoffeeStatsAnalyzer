import argparse
import csv
import statistics
from dataclasses import dataclass
from typing import Callable, Iterable, List, Mapping, Sequence

from tabulate import tabulate


Record = Mapping[str, object]
ReportRows = List[List[object]]
ReportBuilder = Callable[[Iterable[Record]], ReportRows]


@dataclass(frozen=True)
class ReportDefinition:
    name: str
    headers: Sequence[str]
    builder: ReportBuilder


def _parse_coffee_spent(value: object) -> float:
    if value is None:
        raise ValueError("coffee_spent is required")
    return float(value)


def load_records(file_paths: Iterable[str]) -> List[Record]:
    records: List[Record] = []
    for file_path in file_paths:
        with open(file_path, encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if "coffee_spent" not in row:
                    raise ValueError("coffee_spent column is missing")
                if "student" not in row:
                    raise ValueError("student column is missing")
                normalized = dict(row)
                normalized["coffee_spent"] = _parse_coffee_spent(row["coffee_spent"])
                records.append(normalized)
    return records


def _maybe_int(value: float) -> object:
    if value.is_integer():
        return int(value)
    return value


def build_median_coffee_report(records: Iterable[Record]) -> ReportRows:
    by_student: dict[str, List[float]] = {}
    for record in records:
        student = str(record["student"])
        coffee_spent = float(record["coffee_spent"])
        by_student.setdefault(student, []).append(coffee_spent)

    rows: ReportRows = []
    for student, values in by_student.items():
        median_value = statistics.median(values)
        rows.append([student, _maybe_int(median_value)])

    rows.sort(key=lambda row: (-float(row[1]), row[0]))
    return rows


REPORTS: dict[str, ReportDefinition] = {
    "median-coffee": ReportDefinition(
        name="median-coffee",
        headers=("student", "median_coffee_spent"),
        builder=build_median_coffee_report,
    ),
}


def render_report(report: ReportDefinition, records: Iterable[Record]) -> str:
    rows = report.builder(records)
    return tabulate(rows, headers=report.headers, tablefmt="github")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coffee stats analyzer")
    parser.add_argument("--files", nargs="+", required=True, help="CSV files to read")
    parser.add_argument(
        "--report",
        required=True,
        choices=sorted(REPORTS.keys()),
        help="Report name",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    records = load_records(args.files)
    report = REPORTS[args.report]
    output = render_report(report, records)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
