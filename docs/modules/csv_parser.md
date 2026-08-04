# `app/csv_parser.py`

Parses the uploaded CSV bytes into a list of expense dicts (`date`, `category`, `amount`,
`description`). Raises `InvalidCSVError` (caught in `app/reports.py` and turned into a `400`)
for missing columns, non-numeric amounts, bad dates, or an empty file. Pure function, no I/O
beyond the bytes it's given — easy to unit test without a database or web framework.
