# Data Model

## `reports`

| column           | type      | notes                          |
|------------------|-----------|---------------------------------|
| id               | int, PK   |                                 |
| created_at       | datetime  | defaults to now (UTC)          |
| period_start     | date      | earliest expense date in the CSV |
| period_end       | date      | latest expense date in the CSV   |
| total_amount     | numeric   | sum of all expenses in the report |
| summary_text     | text      | Claude-generated narrative      |
| source_filename  | string    | original uploaded filename      |

## `expenses`

| column      | type    | notes                    |
|-------------|---------|--------------------------|
| id          | int, PK |                          |
| report_id   | int, FK | → `reports.id`           |
| date        | date    |                          |
| category    | string  |                          |
| amount      | numeric |                          |
| description | text    |                          |

One report has many expenses (the rows from the uploaded CSV).
