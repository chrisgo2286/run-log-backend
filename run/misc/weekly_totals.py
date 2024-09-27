from datetime import datetime, timedelta
from django.db.models import Sum

class WeeklyTotals:
    """Class to compile weekly totals for given month"""
    def __init__(self, runs, month, year):
        self.month = month
        self.year = year
        self.runs = runs
        self.periods = []
        self.data = []

    def compile(self):
        """Compiles periods and data"""
        self.compile_periods()
        self.compile_weekly_totals()

    def compile_periods(self):
        """Compiles start and end dates for each week in month"""
        start_date = datetime(year=self.year, month=self.month, day=1)
        end_date = start_date + timedelta(days=6)
        self.periods.insert(0,{"start": start_date, "end": end_date})
        while end_date.month == self.month:
            start_date = end_date + timedelta(days=1)
            end_date = start_date + timedelta(days=6)
            self.periods.append({"start": start_date, "end": end_date})

    def compile_weekly_totals(self):
        """Compiles total mileage for each weekly period"""
        for period in self.periods:
            runs = self.filter_runs(period["start"], period["end"])
            sum = runs.aggregate(Sum("distance"))
            if sum["distance__sum"]:
                self.data.append(float(sum["distance__sum"]))
            else:
                self.data.append("0")

    def filter_runs(self, start, end):
        """Filters for runs within given dates"""
        return self.runs.filter(date__gte=start, date__lte=end)