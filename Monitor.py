
from multiprocessing import Process
from datetime import datetime
from Worker import Worker
import multiprocessing
import pandas as pd
import math

def job(websites, wid, mins):
    worker = Worker(websites, wid, mins)
    worker.start()

def start(mins):
    input_csv = "resources/input.csv"
    today = datetime.today().date()
    df = pd.read_csv(input_csv)
    df = df.fillna("")
    works = [] 
    for index, row in df.iterrows():
        if row["date"]!="":
            date_obj = datetime.strptime(row["date"], '%Y-%m-%d').date()
            if today==date_obj:
                works.append((index,row["website_ir"]))
    n_works = len(works)

    print("- {} works today {}".format(str(n_works),str(today)))
    if n_works>0:    
        available_cpus = multiprocessing.cpu_count() - 2
        blocks = int(math.ceil(n_works/available_cpus))
        
        last_idx = 0
        processes = []
        for i in range(1,available_cpus+1):
            end_idx = i*blocks
            if end_idx > n_works:
                end_idx = n_works

            sub_works = works.copy()
            sub_works = sub_works[last_idx:i*blocks]
            last_idx = i*blocks

            p = Process(target=job, args=(sub_works,i,mins))
            processes.append(p)
            p.start()

        for pro in processes:
            pro.join()

        print("- {} works done!".format(str(today)))