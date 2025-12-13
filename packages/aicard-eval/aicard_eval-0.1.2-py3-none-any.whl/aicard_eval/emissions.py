import eco2ai
import os
from .utils import read_data

class Emission:
    def __init__(self, project_name="", experiment_description=""):
        self.file_name = "emission.csv"
        self.tracker = eco2ai.Tracker(
            project_name=project_name,
            experiment_description=experiment_description,
            file_name=self.file_name,
        )

    def start(self):
        self.tracker.start()

    def stop(self):
        self.tracker.stop()

    def pop(self):
        with open(self.file_name, "r") as f:
            data = read_data(self.file_name)
        os.remove(self.file_name)
        return data.to_dict()