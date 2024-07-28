from datetime import datetime
from calendar import monthrange
from django.db.models import Sum

class YearlyStats():
    """Class to compile data for yearly stats"""
    def __init__(self, year, runs):
        self.year = year
        self.today = datetime.today()
        self.runs = self.filter_runs_by_period(runs)
        self.data = {}

    def compile(self):
        """Compiles all data for yearly stats to Data"""
        self.calc_distance()
        self.calc_time()
        self.calc_monthly_average_ytd()
        self.calc_weekly_average_ytd()
        self.calc_average_pace_ytd()

    def calc_distance(self):
        """Enters total distance run for year to Data"""
        sum = self.runs.aggregate(Sum('distance'))
        self.data['distance'] = float(sum['distance__sum'])

    def calc_time(self):
        """Enters total time run for year to Data"""
        sum = self.runs.aggregate(Sum('time'))
        self.data['time'] = float(sum['time__sum'])

    def calc_monthly_average_ytd(self):
        """Enters monthly average km run year to date to Data"""
        days_in_month = monthrange(self.today.year, self.today.month)[1]
        fraction_of_month = self.today.day / days_in_month
        months = (self.today.month - 1) + fraction_of_month
        self.data['monthly_average'] = self.data['distance'] / months
    
    def calc_weekly_average_ytd(self):
        """Enters weekly average km run year to date to Data"""
        first_day_of_year = datetime(self.today.year, 1, 1)
        days_elapsed = self.today - first_day_of_year
        weeks = days_elapsed.days / 7
        self.data['weekly_average'] = self.data['total_distance'] / weeks
    
    def calc_average_pace_ytd(self):
        """Enters average pace ytd to Data"""
        self.data['average_pace'] = self.data['time'] / self.data['distance']
    
    def filter_runs_by_period(self, runs):
        """Returns queryset of given runs filtered by year"""
        return runs.filter(date__year=self.year)