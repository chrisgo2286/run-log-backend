from datetime import datetime
from calendar import monthrange
from django.db.models import Sum

class MonthlyStats():
    """Class to compile data for monthly stats"""
    DATA_KEYS = ['distance', 'time', 'weekly_average', 'pace']

    def __init__(self, month, year, runs):
        self.month = month
        self.year = year
        self.dateObj = datetime(self.year, self.month, 1)
        self.runs = self.filter_runs_by_period(runs)
        self.data = {}

    def compile(self):
        """Compiles data for monthly stats shown on Profile page"""
        self.get_month_name()
        if self.runs:
            self.compile_data()
        else:
            self.input_zero_values()

    def get_month_name(self):
        """Enters month's full name to Data"""
        self.data['current_month'] = self.dateObj.strftime("%B")
    
    def compile_data(self):
        """Compiles distance, time, weekly average and pace"""
        self.calc_distance()
        self.calc_time()
        self.calc_weekly_average()
        self.calc_average_pace()

    def calc_distance(self):
        """Enters total distance run for the month to Data"""
        sum = self.runs.aggregate(Sum('distance'))
        self.data['distance'] = float(sum['distance__sum'])
    
    def calc_time(self):
        """Enters total time run for the month to Data"""
        sum = self.runs.aggregate(Sum('time'))
        self.data['time'] = float(sum['time__sum'])

    def calc_weekly_average(self):
        """Enters weekly average km run to Data"""
        num_weeks = self.get_num_weeks()
        distance = self.data['distance']
        self.data['weekly_average'] = distance / num_weeks

    def get_num_weeks(self):
        """Returns number of weeks in month as float; if current month, then
        only returns number weeks up to current day"""
        if self.is_current_period():
            return datetime.today().day / 7
        days_in_month = monthrange(self.year, self.month)[1]
        return days_in_month / 7

    def is_current_period(self):
        """Returns true if given month and year is current"""
        return (
            datetime.today().month == self.dateObj.month and
            datetime.today().year == self.dateObj.year
        ) 

    def calc_average_pace(self):
        """Enters average pace for current month to Data"""
        self.data['average_pace'] = self.data['time'] / self.data['distance']

    def input_zero_values(self):
        """Enters zero for each field if no runs for that period"""
        for key in self.DATA_KEYS:
            self.data[key] = 0
            
    def filter_runs_by_period(self, runs):
        """Returns queryset of runs for given month and year"""
        return runs.filter(date__month=self.month, date__year=self.year)