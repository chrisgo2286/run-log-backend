from datetime import timedelta
from run.models import TrainingBlock

class TrainingBlockData:
    """Class to compile and store run data for given training block"""
    def __init__(self, runs, id):
        self.runs = runs
        self.training_block = TrainingBlock.objects.filter(id=id)[0]
        self.cycle_length = self.training_block.cycleLength
        self.start_date = self.training_block.startDate
        self.end_date = self.training_block.endDate
        self.data = []

    def compile_data(self):
        """Populates data with list of list of runs based on cycle length"""
        runs = self.filter_runs()
        curDate = self.start_date
        cycle_data = []
        while curDate <= self.end_date:
            label = f"{curDate.strftime('%m/%#d')} {curDate.strftime('%a')}"
            data = {"label": label}
            curRun = runs.filter(date=curDate)
            if curRun:
                data["id"] = curRun[0].id
                data["run_type"] = curRun[0].run_type
                data["date"] = curRun[0].date
                data["distance"] = curRun[0].distance
                data["hours"] = curRun[0].hours
                data["minutes"] = curRun[0].minutes
                data["seconds"] = curRun[0].seconds
                data["comment"] = curRun[0].comment
            cycle_data.append(data)

            if len(cycle_data) == self.cycle_length:
                self.data.append(cycle_data)
                cycle_data = []
            curDate = curDate + timedelta(days=1)
        if cycle_data:
            self.data.append(cycle_data)

    def filter_runs(self):
        """Filters runs for start and end dates"""
        return self.runs.filter(date__gte=self.start_date, 
            date__lte=self.end_date)