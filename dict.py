from tvDatafeed import Interval


exchange_dict = {
    'QQQ': 'NASDAQ',
    'SPY': 'AMEX',
    'IWM': 'AMEX'
}

freq_dict = {
    'Daily': Interval.in_daily,
    'Weekly': Interval.in_weekly,
    'Monthly': Interval.in_monthly
}

freq_name_dict = {
    'Daily': 'day',
    'Weekly': 'Week',
    'Monthly': 'month'
}