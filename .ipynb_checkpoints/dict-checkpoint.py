from tvDatafeed import Interval
from datetime import datetime, timedelta

exchange_dict = {
    'QQQ': 'NASDAQ',
    'SPY': 'AMEX',
    'IWM': 'AMEX'
}

freq_dict = {
    'Minute': Interval.in_1_minute,
    '15 minutes': Interval.in_15_minute,
    '30 minutes': Interval.in_30_minute,
    'Hourly': Interval.in_1_hour,
    'Daily': Interval.in_daily,
    'Weekly': Interval.in_weekly,
    'Monthly': Interval.in_monthly
}

freq_name_dict = {
    'Minute': 'minute',
    '15 minutes': '15 minutes',
    '30 minutes': '30 minutes',
    'Hourly': 'hour',
    'Daily': 'day',
    'Weekly': 'Week',
    'Monthly': 'month'
}

timedelta_dict = {
    'Minute': timedelta(seconds=2),
    '15 minutes': timedelta(minutes=2),
    '30 minutes': timedelta(minutes=2),
    'Hourly': timedelta(hours=2),
    'Daily': timedelta(days=2),
    'Weekly': timedelta(weeks=2),
    'Monthly': timedelta(weeks=8)
}