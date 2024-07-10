from datetime import datetime
from calendar import monthrange

class RunData:
    """Class to compile runs for given month and year"""
    def __init__(self, runs, month, year):
        self.runs = runs
        self.month = month
        self.year = year
        self.data = []

    def compile(self):
        """Compiles all run data"""
        self.filter_by_date()
        for run in self.runs:
            self.compile_single_run(run)
        self.adjust_calendar_start()
        self.adjust_calendar_end()

    def filter_by_date(self):
        """Filters queryset by month and year"""
        self.runs.filter(date__month=self.month)
        self.runs.filter(date__year=self.year)
 
    def compile_single_run(self, run):
        """Creates dict of single run and appends to self.data"""
        self.data.append({
            'run_type': run.run_type,
            'date': run.date,
            'day': run.date.day,
            'distance': run.distance,
            'time': run.time,
            'comment': run.comment
        })

    def adjust_calendar_start(self):
        """Appends blank days prior to start of month for previous month"""
        current_date = datetime.date(self.year, self.month, 1)
        day_of_week = current_date.weekday()
        
        if day_of_week == 6:
            return
        
        for day in range(day_of_week + 1):
            self.data.append({'day': '0'})

    def adjust_calendar_end(self):
        """Appends blank days after end of month for next month"""
        last_day = monthrange(self.year, self.month)[1]
        last_date = datetime.date(self.year, self.month, last_day)
        day_of_week = last_date.weekday()

        if day_of_week == 5:
            return
        elif day_of_week == 6:
            offset = 6
        else:
            offset = 5 - day_of_week

        for day in range(offset):
            self.data.append({'day': '0'})


