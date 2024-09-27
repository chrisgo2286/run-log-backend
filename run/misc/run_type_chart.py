from dateutil.relativedelta import relativedelta
from datetime import date
from django.db.models import Sum
from run.models import RUN_CHOICES

class RunTypeChart:
    """Class to compile data for RunType Chart"""
    def __init__(self, month, year, runs):
        self.month = month
        self.year = year
        self.runs = self.filter_runs_by_period(runs)
        self.data = []
        self.run_types = []

    def compile(self):
        """Compiles all data to list"""
        for run_type in RUN_CHOICES:
            runs = self.runs.filter(run_type=run_type[0])
            distance = self.calc_total_distance(runs)
            self.data.append({"name": run_type[0], "distance": distance})

    def filter_runs_by_period(self, runs):
        """Filters runs by month and year and current dates only"""
        cur_date = date.today()
        return runs.filter(date__lte=cur_date, date__year=self.year, 
            date__month=self.month)

    def calc_total_distance(self, runs):
        """Returns sum of distance for given runs"""
        sum = runs.aggregate(Sum("distance"))
        return sum['distance__sum']