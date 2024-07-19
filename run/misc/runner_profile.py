from datetime import datetime
from calendar import monthrange
from django.db.models import Sum

class RunnerProfile:
    """Class to provide data for runner profile page"""
    def __init__(self, runs):
        self.today = datetime.now()
        self.runs = runs
        self.runs_for_month = self.runs.filter(date__month=self.today.month)
        self.runs_for_year = self.runs.filter(date__year=self.today.year)
        self.data = {
            'monthly_stats': {},
            'yearly_stats': {},
            'monthly_chart': {},
            'weekly_chart': {},
            'pace_chart': {}
        }

    def compile(self):
        """Compiles data for profile page"""
        self.compile_monthly_stats()
        self.compile_yearly_stats()
        self.compile_monthly_chart_data()
        self.compile_weekly_chart_data()
        self.compile_pace_chart_data()

    # MONTHLY STATS
    def compile_monthly_stats(self):
        """Compiles data for monthly stats shown on Profile page"""
        self.get_current_month()
        self.calc_total_monthly_distance()
        self.calc_total_monthly_time()
        self.calc_weekly_average_for_month()
        self.calc_average_pace_for_month()

    def get_current_month(self):
        """Enters current month's full name to Data"""
        self.data['monthly_stats']['current_month'] = self.today.strftime("%B")
    
    def calc_total_monthly_distance(self):
        """Enters total distance run for the month to Data"""
        sum = self.runs_for_month.aggregate(Sum('distance'))
        self.data['monthly_stats']['total_distance'] = float(sum['distance__sum'])
    
    def calc_total_monthly_time(self):
        """Enters total time run for the month to Data"""
        sum = self.runs_for_month.aggregate(Sum('time'))
        self.data['monthly_stats']['total_time'] = float(sum['time__sum'])

    def calc_weekly_average_for_month(self):
        """Enters weekly average km run to Data"""
        num_weeks = self.today.day / 7
        distance = self.data['monthly_stats']['total_distance']
        self.data['monthly_stats']['weekly_average'] = distance / num_weeks
    
    def calc_average_pace_for_month(self):
        """Enters average pace for current month to Data"""
        distance = self.data['monthly_stats']['total_distance'] 
        time = self.data['monthly_stats']['total_time']
        self.data['monthly_stats']['average_page'] = time / distance
    
    # YEARLY STATS
    def compile_yearly_stats(self):
        """Compiles data for yearly stats shown on Profile page"""
        self.get_current_year()
        self.calc_total_yearly_distance()
        self.calc_total_yearly_time()
        self.calc_monthly_average_ytd()
        self.calc_weekly_average_ytd()
        self.calc_average_pace_ytd()

    def get_current_year(self):
        """Enters current full year to Data"""
        self.data['yearly_stats']['current_year'] = self.today.year

    def calc_total_yearly_distance(self):
        """Enters total distance run for year to Data"""
        sum = self.runs_for_year.aggregate(Sum('distance'))
        self.data['yearly_stats']['total_distance'] = float(sum['distance__sum'])

    def calc_total_yearly_time(self):
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
    

    #Monthly Chart Data
    def compile_monthly_chart_data(self):
        pass
    
    def compile_weekly_chart_data(self):
        pass
    
    def compile_pace_chart_data(self):
        pass
    
    