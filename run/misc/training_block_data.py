from datetime import timedelta
from run.models import TrainingBlock

class TrainingBlockData:
    """Class to compile and store run data for given training block"""
    def __init__(self, runs, id):
        self.training_block = TrainingBlock.objects.filter(id=id)[0]
        self.cycle_length = self.training_block.cycleLength
        self.start_date = self.training_block.startDate
        self.end_date = self.training_block.endDate
        self.runs = self.filter_runs(runs)
        self.data = {"totals": [], "trainingData": []}
        self.cycle_data = []
        self.cycle_total = 0

    def filter_runs(self, runs):
        """Filters runs for start and end dates"""
        return runs.filter(date__gte=self.start_date, 
            date__lte=self.end_date)

    def compile_data(self):
        """Returns list of cycle data"""
        self.curDate = self.start_date
        while self.curDate <= self.end_date:
            data = self.compile_day_data()
            self.compile_cycle_data(data)
            self.curDate = self.curDate + timedelta(days=1)
        self.add_final_cycle()

    def compile_day_data(self):
        label = f"{self.curDate.strftime('%m/%#d')} {self.curDate.strftime('%a')}"
        return self.add_run_to_data({"label": label})

    def add_run_to_data(self, data):
        curRun = self.runs.filter(date=self.curDate)
        if curRun:
            data = self.add_run(data, curRun[0])
            self.cycle_total += curRun[0].distance
        return data

    def add_run(self, data, run):
        """Adds run to data dict"""
        data["id"] = run.id
        data["run_type"] = run.run_type
        data["date"] = run.date
        data["distance"] = run.distance
        data["hours"] = run.hours
        data["minutes"] = run.minutes
        data["seconds"] = run.seconds
        data["comment"] = run.comment
        return data

    def compile_cycle_data(self, data):
        self.cycle_data.append(data)
        if len(self.cycle_data) == self.cycle_length:
            self.data["trainingData"].append(self.cycle_data)
            self.data["totals"].append(round(self.cycle_total,0))
            self.cycle_data = []
            self.cycle_total = 0

    def add_final_cycle(self):
        if self.cycle_data:
            self.data["trainingData"].append(self.cycle_data)