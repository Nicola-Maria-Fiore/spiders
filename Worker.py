import pandas as pd

class Worker:

    def __init__(self, jobs, wid):
        self.jobs = jobs
        self.wid = wid


    def start(self):
        print("Worker {}".format(str(self.wid)))
        for j in self.jobs:
            print(j[0])