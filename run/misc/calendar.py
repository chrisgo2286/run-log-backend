from run.misc.run_data import RunData
from run.misc.weekly_totals import WeeklyTotals

class Calendar:
    """Class to compile data for Calendar Page"""
    def __init__(self, runs, month, year):
        self.runs = runs
        self.month = month
        self.year = year
        self.data = {}

    def compile(self):
        """Compiles run data and weekly totals"""
        runs = self.filter_runs()
        self.compile_run_data(runs)
        self.compile_weekly_totals(runs)
    
    def compile_run_data(self, runs):
        """Compiles run data for each day of month"""
        run_data = RunData(runs, self.month, self.year)
        run_data.compile()
        self.data["runData"] = run_data.data
    
    def compile_weekly_totals(self, runs):
        """Compiles weekly totals for each week of month"""
        weekly_totals = WeeklyTotals(runs, self.month, self.year)
        weekly_totals.compile()   
        self.data["weeklyTotals"] = weekly_totals.data

    def filter_runs(self):
        """Filters runs by month and year"""
        return self.runs.filter(date__month=self.month, 
            date__year=self.year)