import datetime
from datetime import timedelta


def today_of_year():  # 计算今天是今年的多少天
    utc_now = datetime.datetime.utcnow()  # 获取当前UTC时间

    today_cal = datetime.datetime(
        utc_now.year, utc_now.month, utc_now.day, utc_now.hour)+timedelta(hours=8)
    today = datetime.date(today_cal.year, today_cal.month, today_cal.day)
    deltaDetails = utc_now - \
        datetime.datetime(utc_now.year, 1, 1, 0, 0, 0, 0) + \
        timedelta(hours=8)
    deltaDays = deltaDetails.days+1

    days = is_leap_year()
    percent = (deltaDetails.days*86400+deltaDetails.seconds) / \
        (days*86400)  # 计算精确到秒的百分比

    return today, deltaDays, percent


def is_leap_year():  # 判断是否是闰年
    year = (datetime.datetime.utcnow()+timedelta(hours=8)).year
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        days = 366
        return days
    else:
        days = 365
        return days