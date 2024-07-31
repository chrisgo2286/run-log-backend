from dateutil.relativedelta import relativedelta
from datetime import datetime
from calendar import monthrange
from django.db.models import Sum

class MonthlyChart:
    """Class to compile data for Monthly Chart"""
    def __init__(self, month, year, runs):
        self.month = month
        self.year = year
        self.runs = runs
        self.data = []
        self.periods = []

    def compile(self):
        """Compiles data needed for MonthlyChart"""
        self.compile_periods()
        self.compile_monthly_data()

    def compile_periods(self):
        """Returns list of 12 months from given period back"""
        self.periods.append({ 'month': self.month, 'year': self.year })
        dateObj = datetime(self.year, self.month, 1)
        for i in range(11):
            prev_period = dateObj - relativedelta(months=1)
            self.periods.append({ 'month': prev_period.month, 'year': prev_period.year })

    def compile_monthly_data(self):
        """Compiles distance and month name for each period"""
        for period in self.periods:
            runs = self.runs.filter(
                date__year=period['year'], 
                date__month=period['month']
            )
            sum = runs.aggregate(Sum('distance'))
            distance = sum['distance__sum']
            dateObj = datetime(period['year'], period['month'], 1)
            label = dateObj.strftime("%B")
            self.data.append({ 'label': label, 'distance': distance })