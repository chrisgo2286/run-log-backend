from datetime import datetime, timedelta, date
from django.db.models import Sum

class WeeklyChart:
    """Class to compile data for Weekly Chart"""
    def __init__(self, start_date, runs):
        self.start_date = start_date
        self.runs = self.filter_runs(runs)
        self.periods = []
        self.data = []

    def compile(self):
        """Compiles periods and data"""
        self.compile_periods()
        self.compile_weekly_data()

    def compile_periods(self):
        """Compiles start and end dates for each week for 6 weeks"""
        start = datetime.strptime(self.start_date, "%m/%d/%Y")
        for i in range(5):
            prev_start = start - timedelta(days=i * 7)
            end = prev_start + timedelta(days=6)
            self.periods.insert(0,{ 'start': prev_start, 'end': end })

    def compile_weekly_data(self):
        """Populates data list with week start date and distances for each 
        period"""
        for period in self.periods:
            runs = self.filter_by_week(period)
            sum = runs.aggregate(Sum('distance'))
            distance = sum['distance__sum']
            label = period['start'].strftime("%b %d")
            self.data.append({ 'label': label, 'distance': distance })

    def filter_by_week(self, period):
        """Returns queryset of runs filtered by start and end date of week"""
        return self.runs.filter(
            date__gte=period['start'], 
            date__lte=period['end']
        )
    
    def filter_runs(self, runs):
        """Returns runs filtered for current dates only"""
        cur_date = date.today()
        return runs.filter(date__lte=cur_date)
