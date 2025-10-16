from datetime import datetime, timedelta

now = datetime.now()
print(now.second, now.minute, now.hour, now.day, now.month, now.year)

delta = timedelta(seconds=10)
print(now+delta)