# Добавление нового отчета

Добавил новый отчет `total-rows`, который считает количество строк по всем
переданным CSV-файлам. Логика подключается через реестр `REPORTS` в `main.py`.

## Что именно добавлено

В `main.py` добавлена функция:

```python
def build_total_rows_report(records: Iterable[Record]) -> ReportRows:
    records_list = list(records)
    return [["total_rows", len(records_list)]]
```

И зарегистрирован новый отчет в `REPORTS`:

```python
"total-rows": ReportDefinition(
    name="total-rows",
    headers=("metric", "value"),
    builder=build_total_rows_report,
),
```

## Как запускать

Пример команды:

```bash
python main.py --files Example\math.csv Example\physics.csv --report total-rows
```

![Пример отчета total-rows](screenshots/New%20report.png)
