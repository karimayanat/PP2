# task1_subtract_days
from datetime import datetime, timedelta
today = datetime.now()
five_days_ago = today - timedelta(days=5)
print("Current date:", today)
print("Five days ago:", five_days_ago)

# task2_relative_dates
from datetime import date, timedelta
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# task3_drop_microseconds
from datetime import datetime
now = datetime.now()
without_ms = now.replace(microsecond = 0)
print("With microseconds:", now)
print("Without microseconds:", without_ms)

# task4_seconds_difference
from datetime import datetime
date1 = datetime(2026, 2, 20, 10, 0, 0)
date2 = datetime(2026, 2, 24, 12, 30, 0)
difference = date2 - date1
seconds = difference.total_seconds()
print("Difference in seconds:", seconds)