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

    def filter_by_date(self):
        """Filters queryset by month and year"""
        self.runs.filter(date__month=self.month)
        self.runs.filter(date__year=self.year)
 
    def compile_single_run(self, run):
        """Creates dict of single run and appends to self.data"""
        self.data.append({
            'run_type': run.run_type,
            'date': run.date,
            'distance': run.distance,
            'time': run.time,
            'comment': run.comment
        })
