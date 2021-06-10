
from multiprocessing import Process
from datetime import datetime
from Worker import Worker
import multiprocessing
import pandas as pd
import math
import os

def job(websites, wid, mins, out_dir):
    worker = Worker(websites, wid, mins, out_dir)
    worker.start()

def start(mins):
    input_csv = "resources/input.csv"
    today = datetime.today().date()
    df = pd.read_csv(input_csv)
    df = df.fillna("")
    works = [] 
    for _, row in df.iterrows():
        if row["date"]!="":
            date_obj = datetime.strptime(row["date"], '%Y-%m-%d').date()
            if today==date_obj:
                works.append((row["isin"],row["website_ir"]))
    n_works = len(works)

    print("- {} works today {}".format(str(n_works),str(today)))
    if n_works>0:    
        out_dir = str(today)
        if not os.path.exists("results/"+out_dir):
            os.makedirs("results/"+out_dir)

        available_cpus = multiprocessing.cpu_count()
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

            p = Process(target=job, args=(sub_works,i,mins,out_dir))
            processes.append(p)
            p.start()

        for pro in processes:
            pro.join()

        print("- {} works done!".format(str(today)))
