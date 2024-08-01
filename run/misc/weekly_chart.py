class WeeklyChart:
    """Class to compile data for Weekly Chart"""
    def __init__(self, start_date, runs):
        self.start_date = start_date
        self.runs = runs
        self.periods = []
        self.data = []

    def compile(self):
        """Compiles periods and data"""
        self.compile_periods()
        self.compile_weekly_data()

    def compile_periods(self):
        """Compiles start and end dates for each week for 6 weeks"""
        pass

    def compile_weekly_data(self):
        """Populates data list with week start date and distances for each 
        period"""
        pass
