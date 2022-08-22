from datetime import date, timedelta, datetime
import calendar

ORDER_TIME_PERIOD_RANGES=["THIS_WEEK","THIS_MONTH","THIS_YEAR"]

def get_current_week_dates():
    current_date=date.today()
    weekday = current_date.weekday()
    start_date = current_date - timedelta(days=weekday)
    end_date = current_date + timedelta(days=(6 - weekday))
    return start_date,end_date

def get_current_month_dates():
    month = datetime.now().month
    year = datetime.now().year
    number_of_days = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, number_of_days)
    return start_date,end_date

def get_current_year_dates():
    start_date = date.today().replace(month=1, day=1)
    end_date = date.today().replace(month=12, day=31)
    return start_date,end_date