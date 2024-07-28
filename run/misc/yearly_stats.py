from datetime import datetime
from django.db.models import Sum

class YearlyStats():
    """Class to compile data for yearly stats"""
    def __init__(self, year, runs):
        self.year = year
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
        self.data['yearly_stats']['total_distance'] = float(sum['distance__sum'])

    def calc_time(self):
        """Enters total time run for year to Data"""
        sum = self.runs_for_year.aggregate(Sum('time'))
        self.data['yearly_stats']['total_time'] = float(sum['time__sum'])

    def calc_monthly_average_ytd(self):
        """Enters monthly average km run year to date to Data"""
        days_in_month = monthrange(self.today.year, self.today.month)[1]
        fraction_of_month = self.today.day / days_in_month
        months = (self.today.month - 1) + fraction_of_month
        distance = self.data['yearly_stats']['total_distance']
        self.data['yearly_stats']['monthly_average'] = distance / months
    
    def calc_weekly_average_ytd(self):
        """Enters weekly average km run year to date to Data"""
        first_day_of_year = datetime(self.today.year, 1, 1)
        days_elapsed = self.today - first_day_of_year
        weeks = days_elapsed.days / 7
        distance = self.data['yearly_stats']['total_distance']
        self.data['yearly_stats']['weekly_average'] = distance / weeks
    
    def calc_average_pace_ytd(self):
        """Enters average pace ytd to Data"""
        distance = self.data['yearly_stats']['total_distance']
        time = self.data['yearly_stats']['total_time']
        self.data['yearly_stats']['average_pace'] = time / distance
    
    
    
    def filter_runs_by_period(self, runs):
        """Returns queryset of given runs filtered by year"""
        return runs.filter(date__year=self.year)