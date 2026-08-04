# `app/aggregation.py`

Takes the parsed expense list and computes, in plain Python (`statistics` module, no Claude
involved): the total amount, the total per category, and outliers — expenses more than 2
standard deviations from their category's mean (categories with fewer than 2 expenses have no
outliers, since a standard deviation isn't meaningful there). This is the only source of truth
for the numbers that end up in a report; `claude_client.py` never recalculates them.
