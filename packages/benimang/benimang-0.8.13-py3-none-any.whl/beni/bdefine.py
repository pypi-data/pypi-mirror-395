from datetime import datetime, timedelta

# 时间
MILLISECOND = timedelta(milliseconds=1)
SECOND = timedelta(seconds=1)
MINUTE = timedelta(minutes=1)
HOUR = timedelta(hours=1)
DAY = timedelta(days=1)

# 日期
BEGIN_DATETIME = datetime(1970, 1, 1)
BEGIN_DATE = BEGIN_DATETIME.date()
END_DATETIME = datetime(9999, 9, 9)
END_DATE = END_DATETIME.date()

# 大小
KB = 1024
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB
