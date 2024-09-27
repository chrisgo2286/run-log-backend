from datetime import date
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
        self.add_calendar_days()
        self.adjust_calendar_start()
        self.adjust_calendar_end()        

    def add_calendar_days(self):
        """Fills in days of the month and adds run if present"""
        for day in range(1, monthrange(self.year, self.month)[1] + 1):
            run = self.runs.filter(date__year=self.year, date__month=self.month,
                date__day=day)
            if len(run) > 0:
                self.add_single_run(run[0])
            else:
                curDate = date(self.year, self.month, day)
                self.data.append({'day':day, 'date': curDate})

    def add_single_run(self, run):
        """Creates dict of single run and appends to self.data"""
        self.data.append({
            'id': run.id,
            'run_type': run.run_type,
            'date': run.date,
            'day': run.date.day,
            'distance': run.distance,
            'hours': run.hours,
            'minutes': run.minutes,
            'seconds': run.seconds,
            'comment': run.comment or ""
        })

    def adjust_calendar_start(self):
        """Appends blank days prior to start of month for previous month"""
        current_date = date(self.year, self.month, 1)
        day_of_week = current_date.weekday()
        
        if day_of_week == 6:
            return
        
        for day in range(day_of_week + 1):
            self.data.insert(0, {'day': '0'})

    def adjust_calendar_end(self):
        """Appends blank days after end of month for next month"""
        last_day = monthrange(self.year, self.month)[1]
        last_date = date(self.year, self.month, last_day)
        day_of_week = last_date.weekday()

        if day_of_week == 5:
            return
        elif day_of_week == 6:
            offset = 6
        else:
            offset = 5 - day_of_week

        for _ in range(offset):
            self.data.append({'day': '0'})


